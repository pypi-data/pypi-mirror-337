import json
import requests
from AgentEngine.framework.tools import Tool
from AgentEngine.core.utils import MessageObserver, ProcessType


class KBSearchTool(Tool):
    """Knowledge Base Search Tool for performing semantic searches.
    支持中英文的知识库语义搜索工具。
    """

    name = "knowledge_base_search"
    description = "Performs a local knowledge base search based on your query then returns the top search results."
    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"

    supported_languages = {'zh', 'en'}
    messages = {
        'en': {
            'search_failed': 'Search request failed: {}',
            'no_results': 'No results found! Try a less restrictive/shorter query.',
            'search_success': 'Knowledge Base Search Results'
        },
        'zh': {
            'search_failed': '搜索请求失败：{}', 
            'no_results': '未找到结果！请尝试使用更宽泛或更短的搜索词。',
            'search_success': '知识库搜索结果'
        }
    }

    def __init__(self, 
                 index_name: str, 
                 top_k: int = 3, 
                 observer: MessageObserver = None, 
                 base_url: str = "http://localhost:8000", 
                 lang: str = "zh") -> None:
        """Initialize the KBSearchTool.
        
        Args:
            index_name (str): Name of the search index
            top_k (int, optional): Number of results to return. Defaults to 3.
            observer (MessageObserver, optional): Message observer instance. Defaults to None.
            base_url (str, optional): Base URL for the search API. Defaults to "http://localhost:8000".
            lang (str, optional): Language code ('zh' or 'en'). Defaults to 'en'.
        
        Raises:
            ValueError: If language is not supported
        """
        super().__init__()
        self.index_name = index_name
        self.top_k = top_k
        self.observer = observer
        self.base_url = base_url
        
        if lang not in self.supported_languages:
            raise ValueError(f"Language must be one of {self.supported_languages}")
        self.lang = lang

    def forward(self, query: str) -> str:
        # TODO: 后续可更新为混合检索接口
        kb_search_response = requests.get(
            f"{self.base_url}/indices/{self.index_name}/search/semantic",
            params={"query": query, "top_k": self.top_k}
        )
        
        if kb_search_response.status_code != 200:
            raise Exception(self.messages[self.lang]['search_failed'].format(kb_search_response.text))

        kb_search_data = kb_search_response.json()
        kb_search_results = kb_search_data["results"]

        if not kb_search_results:
            raise Exception(self.messages[self.lang]['no_results'])

        search_results_json = [{
            "title": result.get("title", ""),
            "url": result.get("path_or_url", ""),
            "text": result.get("content", ""),
            "published_date": result.get("create_time", ""),
            "filename": result.get("filename", ""),
            "score": result.get("score", 0),
        } for result in kb_search_results]
        
        if self.observer:
            search_results_data = json.dumps(search_results_json)
            self.observer.add_message("", ProcessType.SEARCH_CONTENT, search_results_data)

        processed_results = [f"[{result['title']}]\n{result['content']}" for result in kb_search_results]

        return "## " + self.messages[self.lang]['search_success'] + "\n" + "\n".join(processed_results) + "\n\n"


if __name__ == "__main__":
    try:
        tool = KBSearchTool(index_name="sample_articles", top_k=1, lang='zh')

        query = "what's the meaning of doctor?"
        result = tool.forward(query)
        print(result)
    except Exception as e:
        print(e)

