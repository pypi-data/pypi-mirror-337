from typing import List, Optional, Dict

from openai.types.chat.chat_completion_message import ChatCompletionMessage

from AgentEngine.framework import Tool
from AgentEngine.framework.models import OpenAIServerModel, ChatMessage, parse_tool_args_if_needed
from AgentEngine.core.utils.observer import MessageObserver, ProcessType


class OpenAIModel(OpenAIServerModel):
    def __init__(self, observer: MessageObserver, *args, **kwargs):
        self.observer = observer
        super().__init__(*args, **kwargs)

    def __call__(
        self,
        messages: List[Dict[str, str]],
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        **kwargs,
    ) -> ChatMessage:
        completion_kwargs = self._prepare_completion_kwargs(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools_to_call_from=tools_to_call_from,
            model=self.model_id,
            custom_role_conversions=self.custom_role_conversions,
            convert_images_to_image_urls=True,

            **kwargs,
        )

        # 模型流式输出
        response = self.client.chat.completions.create(stream=True, **completion_kwargs)

        chunk_list = []
        token_join = []
        role = None

        # 重置输出模式
        self.observer.current_mode = ProcessType.MODEL_OUTPUT_THINKING
        for chunk in response:
            new_token = chunk.choices[0].delta.content
            if new_token is not None:
                print(new_token, end="")
                self.observer.add_model_new_token(new_token)
                token_join.append(new_token)
                role = chunk.choices[0].delta.role
            chunk_list.append(chunk)

        # 发送结束标记
        self.observer.flush_remaining_tokens()

        model_output = "".join(token_join)

        if chunk_list[-1].usage is not None:
            self.last_input_token_count = chunk_list[-1].usage.prompt_tokens
            self.last_output_token_count = chunk_list[-1].usage.total_tokens
        else:
            self.last_input_token_count = 0
            self.last_output_token_count = 0

        message = ChatMessage.from_dict(
            ChatCompletionMessage(
                role=role if role else "assistant",  # 如果没有明确角色，默认使用 "assistant"
                content=model_output
            ).model_dump(include={"role", "content", "tool_calls"})
        )

        message.raw = response
        if tools_to_call_from is not None:
            return parse_tool_args_if_needed(message)
        return message
