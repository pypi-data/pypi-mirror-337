from enum import Enum
import json
import re  # 新增导入
from collections import deque  # 导入双端队列


class ProcessType(Enum):
    STEP_COUNT = "step_count"                           # 当前处于agent的哪一步
    MODEL_OUTPUT_THINKING = "model_output_thinking"     # 模型流式输出，思考内容
    MODEL_OUTPUT_CODE = "model_output_code"             # 模型流式输出，代码内容
    PARSE = "parse"                                     # 代码解析结果
    EXECUTION_LOGS = "execution_logs"                   # 代码执行结果
    AGENT_NEW_RUN = "agent_new_run"                     # Agent基本信息打印
    FINAL_ANSWER = "final_answer"                       # 最终总结字样
    ERROR = "error"                                     # 异常字段
    SEARCH_CONTENT = "search_content"                   # 工具中的搜索内容
    OTHER = "other"                                     # 临时的其他字段
    TOKEN_COUNT = "token_count"                         # 记录每一个step使用的token数



class MessageObserver:
    def __init__(self, lang = "zh"):
        # 统一输出给前端的字符串，改为队列
        self.message_query = []

        # 控制输出语言
        self.lang = lang
        
        # 初始化消息类型到转换函数的映射
        self._init_message_transformers()
        
        # 双端队列用于存储和分析最近的tokens
        self.token_buffer = deque()
        
        # 当前输出模式：默认为思考模式
        self.current_mode = ProcessType.MODEL_OUTPUT_THINKING
        
        # 代码块标记模式
        self.code_pattern = re.compile(r"代码(：|:)\s*```")

    def _init_message_transformers(self):
        """初始化消息类型到转换函数的映射"""
        self.message_transformers = {
            ProcessType.AGENT_NEW_RUN: self._transform_agent_new_run,
            ProcessType.STEP_COUNT: self._transform_step_count,
            ProcessType.PARSE: self._transform_parse,
            ProcessType.EXECUTION_LOGS: self._transform_execution_logs,
            ProcessType.FINAL_ANSWER: self._transform_final_answer,
            ProcessType.OTHER: self._transform_none_process,
            ProcessType.SEARCH_CONTENT: self._transform_none_process,
            ProcessType.TOKEN_COUNT: self._transform_none_process,
            ProcessType.ERROR: self._transform_none_process,
        }
        
        # 语言相关的模板字符串
        self.templates = {
            "zh": {
                "step": "\n**步骤 {0}** \n",
                "parse": "\n🛠️ 使用Python解释器执行代码\n",
                "logs": "\n📝 执行日志\n",
                "final": "\n**最终回答:** \n{0}\n",
                "error": "\n💥 Error\n"
            },
            "en": {
                "step": "\n**Step {0}** \n",
                "parse": "\n🛠️ Used tool python_interpreter\n",
                "logs": "\n📝 Execution Logs\n",
                "final": "\n**Final answer:** \n{0}\n",
                "error": "\n💥 错误\n"
            }
        }

    def add_model_new_token(self, new_token):
        """
        获取模型的流式输出，使用双端队列实时分析和分类token
        """
        
        # 将新token添加到缓冲区
        self.token_buffer.append(new_token)
        
        # 将缓冲区拼接成文本进行检查
        buffer_text = ''.join(self.token_buffer)
        
        # 查找代码块标记
        match = self.code_pattern.search(buffer_text)
        
        if match:
            # 找到了代码块标记
            match_start = match.start()
            
            # 将匹配位置之前的内容作为思考发送
            prefix_text = buffer_text[:match_start]
            if prefix_text:
                self.message_query.append(Message(ProcessType.MODEL_OUTPUT_THINKING, prefix_text).to_json())
            
            # 将匹配部分及之后的内容作为代码发送
            code_text = buffer_text[match_start:]
            if code_text:
                self.message_query.append(Message(ProcessType.MODEL_OUTPUT_CODE, code_text).to_json())
            
            # 切换模式
            self.current_mode = ProcessType.MODEL_OUTPUT_CODE
            
            # 清空缓冲区
            self.token_buffer.clear()
        else:
            # 未找到代码块标记，从队首取出并发送一个token（如果缓冲区长度超过一定大小）
            max_buffer_size = 10  # 设置最大缓冲区大小，可以根据需要调整
            while len(self.token_buffer) > max_buffer_size:
                oldest_token = self.token_buffer.popleft()
                self.message_query.append(Message(self.current_mode, oldest_token).to_json())

    def flush_remaining_tokens(self):
        """
        将双端队列中剩余的token发送出去
        """
        if not self.token_buffer:
            return
            
        # 将缓冲区拼接成文本
        buffer_text = ''.join(self.token_buffer)
        self.message_query.append(Message(self.current_mode, buffer_text).to_json())
    
        # 清空缓冲区
        self.token_buffer.clear()

    def add_message(self, agent_name, process_type, content: str):
        """添加消息到队列"""
        if process_type in self.message_transformers:
            transformer = self.message_transformers[process_type]
            formatted_content = transformer(content)
            self.message_query.append(Message(process_type, formatted_content).to_json())
    
    def _get_template(self, key):
        """获取当前语言对应的模板"""
        language = self.lang if self.lang in self.templates else "en"
        return self.templates[language][key]

    def _transform_none_process(self, content: str):
        """返回任意消息，不做处理"""
        return content

    def _transform_agent_new_run(self, content: str):
        """转换agent新运行的消息"""
        return f"\n\n{content}\n\n"

    def _transform_step_count(self, content: str):
        """转换步骤计数的消息"""
        return self._get_template("step").format(content)

    def _transform_parse(self, content: str):
        """转换解析结果的消息"""
        return self._get_template("parse") + f"```python\n{content}\n```\n"

    def _transform_execution_logs(self, content: str):
        """转换执行日志的消息"""
        return self._get_template("logs") + f"```bash\n{content}\n```\n"

    def _transform_final_answer(self, content: str):
        """转换最终答案的消息"""
        return self._get_template("final").format(content)

    def _transform_error(self, content: str):
        """转换最终答案的消息"""
        return self._get_template("error").format(content)

    def get_cached_message(self):
        cached_message = self.message_query
        self.message_query = []
        return cached_message


# 固定MessageObserver的输出格式
class Message:
    def __init__(self, message_type: ProcessType, content):
        self.message_type = message_type
        self.content = content

    # 生成json格式，并转成字符串
    def to_json(self):
        return json.dumps({
            "type": self.message_type.value,
            "content": self.content
        }, ensure_ascii=False)

