from typing import Dict, Tuple, Any, Union

from pywce.modules import ISessionManager, client
from pywce.src.constants import EngineConstants, SessionConstants, TemplateConstants
from pywce.src.exceptions import EngineInternalException, EngineResponseException
from pywce.src.models import WorkerJob, HookArg
from pywce.src.services import HookService
from pywce.src.templates import EngineTemplate
from pywce.src.utils.engine_logger import pywce_logger
from pywce.src.utils.engine_util import EngineUtil
from pywce.src.utils.hook_util import HookUtil


class MessageProcessor:
    """
        Main message processor class

        Processes current message against templates
        Processes all templates hooks
    """
    CURRENT_TEMPLATE: EngineTemplate
    CURRENT_STAGE: str
    HOOK_ARG: HookArg
    IS_FIRST_TIME: bool = False
    IS_FROM_TRIGGER: bool = False

    # (input: str, data: dict)
    USER_INPUT: Tuple[Any, Any]

    def __init__(self, data: WorkerJob):
        self.data = data
        self.user = data.user
        self.config = data.engine_config
        self.whatsapp = data.engine_config.whatsapp
        self.payload = data.payload

        self.session_id = self.user.wa_id
        self.session: ISessionManager = self.config.session_manager.session(session_id=self.session_id)

        self.logger = pywce_logger(__name__)

    def _get_stage_template(self, template_stage_name: str) -> EngineTemplate:
        tpl = self.config.storage_manager.get(template_stage_name)
        if tpl is None:
            raise EngineInternalException(message=f"Template {template_stage_name} not found")
        return tpl

    def _get_current_template(self) -> None:
        current_stage_in_session = self.session.get(session_id=self.session_id, key=SessionConstants.CURRENT_STAGE)

        if current_stage_in_session is None:
            self.CURRENT_STAGE = self.config.start_template_stage

            self.CURRENT_TEMPLATE = self._get_stage_template(self.CURRENT_STAGE)
            self.IS_FIRST_TIME = True

            self.session.save(session_id=self.session_id, key=SessionConstants.CURRENT_STAGE, data=self.CURRENT_STAGE)
            self.session.save(session_id=self.session_id, key=SessionConstants.PREV_STAGE, data=self.CURRENT_STAGE)
            return

        self.CURRENT_STAGE = current_stage_in_session
        self.CURRENT_TEMPLATE = self._get_stage_template(current_stage_in_session)

    def _check_if_trigger(self, possible_trigger_input: str = None) -> None:
        if possible_trigger_input is None:
            return

        for trigger in self.config.storage_manager.triggers():
            if EngineUtil.has_triggered(trigger, possible_trigger_input):
                self.CURRENT_TEMPLATE = self._get_stage_template(trigger.next_stage)
                self.CURRENT_STAGE = trigger.next_stage
                self.IS_FROM_TRIGGER = True
                self.session.save(session_id=self.session_id, key=SessionConstants.CURRENT_STAGE,
                                  data=self.CURRENT_STAGE)
                self.logger.debug("Template change from trigger. Stage: " + trigger.next_stage)
                return

        # TODO: check if current msg id is null, throw Ambiguous old webhook exc

    def _get_message_body(self) -> None:
        """
        Extracts message body from webhook

        For type that cannot be processed easily e.g. MEDIA, LOCATION_REQUEST & FLOW
        the raw response data will be available under `USER_INPUT[1]` & `HookArg.additional_data` in hooks.

        For normal text messages & or buttons - the user selection or input will be available in `USER_INPUT[0]` &
        `HookArg.user_input` in hooks.

        If the resulting `USER_INPUT[0]` is None -> it signifies that user message cannot be processed e.g. Image

        Returns:
            None
        """

        match self.payload.typ:
            case client.MessageTypeEnum.TEXT:
                self.USER_INPUT = (self.payload.body.get("body"), None)
                self._check_if_trigger(self.USER_INPUT[0])

            case client.MessageTypeEnum.BUTTON | client.MessageTypeEnum.INTERACTIVE_BUTTON | \
                 client.MessageTypeEnum.INTERACTIVE_LIST:
                if "text" in self.payload.body:
                    self.USER_INPUT = (self.payload.body.get("text"), None)
                    self._check_if_trigger(self.USER_INPUT[0])
                else:
                    # for interactive button & list
                    self.USER_INPUT = (str(self.payload.body.get("id")), self.payload.body)
                    self._check_if_trigger(self.USER_INPUT[0])

            case client.MessageTypeEnum.LOCATION:
                self.USER_INPUT = (None, self.payload.body)

            case client.MessageTypeEnum.INTERACTIVE:
                self.USER_INPUT = (None, self.payload.body)

            case client.MessageTypeEnum.IMAGE | client.MessageTypeEnum.STICKER | \
                 client.MessageTypeEnum.DOCUMENT | client.MessageTypeEnum.AUDIO | client.MessageTypeEnum.VIDEO:
                self.USER_INPUT = (None, self.payload.body)

            case client.MessageTypeEnum.INTERACTIVE_FLOW:
                self.USER_INPUT = (self.payload.body.get("screen"), self.payload.body)

            case _:
                raise EngineResponseException(message="Unsupported response, kindly provide a valid response",
                                              data=self.CURRENT_STAGE)

    def _check_for_session_bypass(self) -> None:
        if self.CURRENT_TEMPLATE.session is False:
            self.IS_FROM_TRIGGER = False
            self.session.save(session_id=self.session_id, key=SessionConstants.CURRENT_STAGE,
                              data=self.CURRENT_STAGE)

    def _check_save_checkpoint(self) -> None:
        if self.CURRENT_TEMPLATE.checkpoint is True:
            self.session.save(session_id=self.session_id, key=SessionConstants.LATEST_CHECKPOINT,
                              data=self.CURRENT_STAGE)

    def _check_template_params(self, template: EngineTemplate = None) -> None:
        tpl = template or self.CURRENT_TEMPLATE
        self.HOOK_ARG.from_trigger = self.IS_FROM_TRIGGER

        if tpl.params is not None:
            self.HOOK_ARG.params.update(tpl.get(TemplateConstants.PARAMS))

    def _ack_user_message(self) -> None:
        # a fire & forget approach
        mark_as_read = self.config.read_receipts is True or self.CURRENT_TEMPLATE.acknowledge is True

        if mark_as_read is True:
            try:
                self.whatsapp.mark_as_read(self.user.msg_id)
            except:
                self.logger.warning("Failed to ack user message", stack_info=True)

    async def process_dynamic_route_hook(self) -> Union[str, None]:
        """
        Router hook is used to check next-route flow, instead of using templates-level defined common, it
        reroutes / redirects / jumps to the response of the `router` hook.

        Router hook should return route stage inside the additional_data with key **EngineConstants.DYNAMIC_ROUTE_KEY**

        :return: str or None
        """

        if self.CURRENT_TEMPLATE.router is not None:
            try:
                self._check_template_params()

                result = await HookUtil.process_hook(
                    hook=self.CURRENT_TEMPLATE.router,
                    arg=self.HOOK_ARG,
                    external=self.config.ext_hook_processor
                )

                return result.additional_data.get(EngineConstants.DYNAMIC_ROUTE_KEY)

            except:
                self.logger.error("Failed to do dynamic route hook", stack_info=True)

        return None

    async def process_pre_hooks(self, next_stage_template: Dict = None) -> None:
        """
        Process all templates hooks before message response is generated
        and send back to user

        :param next_stage_template: for processing next stage templates else use current stage templates
        :return: None
        """
        await HookService.process_global_hooks("pre", self.HOOK_ARG)

        self._check_template_params(next_stage_template)

        if self.CURRENT_TEMPLATE.on_generate is not None:
            await HookUtil.process_hook(hook=self.CURRENT_TEMPLATE.on_generate,
                                        arg=self.HOOK_ARG,
                                        external=self.config.ext_hook_processor
                                        )

    async def process_post_hooks(self) -> None:
        """
        Process all hooks soon after receiving message from user.

        This processes the previous message which was processed & generated for sending
        to user

        ---

        e.g. Generate stage A templates -> process all A's pre-hooks -> send to user.

        User responds to A message -> Engine processes A post-hooks.

        ---

        Return:
             None
        """
        await HookService.process_global_hooks("post", self.HOOK_ARG)

        self._ack_user_message()
        self._check_template_params()

        if self.CURRENT_TEMPLATE.on_receive is not None:
            await HookUtil.process_hook(hook=self.CURRENT_TEMPLATE.on_receive,
                                        arg=self.HOOK_ARG,
                                        external=self.config.ext_hook_processor
                                        )

        if self.CURRENT_TEMPLATE.middleware is not None:
            await HookUtil.process_hook(hook=self.CURRENT_TEMPLATE.middleware,
                                        arg=self.HOOK_ARG,
                                        external=self.config.ext_hook_processor
                                        )

        if self.CURRENT_TEMPLATE.prop is not None:
            self.session.save_prop(
                session_id=self.session_id,
                prop_key=self.CURRENT_TEMPLATE.prop,
                data=self.USER_INPUT[0]
            )

    def setup(self) -> None:
        """
            Should be called before any other methods are called.

            Called after object instantiation.

            :return: None
        """
        self._get_current_template()
        self._get_message_body()
        self._check_for_session_bypass()
        self._check_save_checkpoint()

        self.HOOK_ARG = HookArg(
            session_id=self.session_id,
            session_manager=self.session,
            user=self.user,
            user_input=self.USER_INPUT[0],
            additional_data=self.USER_INPUT[1]
        )
