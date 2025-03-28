from openai import OpenAI
from rich.markdown import Markdown
from rich.live import Live
from .web_search import WebSearch
from .db import Database


class TAClient:
    def __init__(self):
        self.db = Database()
        self.api_key = self.db.get_config("api_key")
        self.base_url = self.db.get_config("base_url") or "https://api.deepseek.com"
        self.model = self.db.get_config("model") or "deepseek-chat"

        if not self.api_key:
            raise ValueError("API_KEY 未设置，请使用 'ta config' 命令进行配置")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.web_search = WebSearch()

    def chat(self, question: str, live: Live = None, use_search: bool = False) -> str:
        response_text = ""
        try:
            messages = []

            if use_search:
                # Perform web search
                search_results = self.web_search.search(question)
                if search_results:
                    # Create context from search results
                    context = "Based on the following search results:\n\n" + "\n".join(
                        search_results
                    )
                    context += f"\n\nPlease answer this question: {question}"
                    messages.append({"role": "user", "content": context})
                else:
                    messages.append({"role": "user", "content": question})
            else:
                messages.append({"role": "user", "content": question})

            for chunk in self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                stream=True,
                temperature=0.7,
                top_p=0.95,
            ):
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content
                    if live:
                        live.update(Markdown(response_text))
            return response_text
        except Exception as e:
            raise Exception(f"Error during chat: {e}")
