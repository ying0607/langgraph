import os
import requests

from dotenv import load_dotenv
load_dotenv("LangGraph/.env")

class AgentBuilder_APIClient:
    def __init__(self):
        self.api_key = os.getenv(
            "AI_SAAS_API_KEY", "http://127.0.0.1:8000"
        )
        self.base_url = os.getenv("AI_SAAS_HOST", "http://127.0.0.1:8000")
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }


    ### For Jason: 確認api呼叫要帶的參數，並與AI SaaS的參數統整
    def query_agentbuilder(self, username, query):
        data = {
            "user": username,
            "query": query
        }

        response = requests.post(
            os.environ["AGENTBUILDER_HOST"],
            json=data,
            timeout=550
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise requests.exceptions.HTTPError(
                f"Error {response.status_code}: {response.text}"
            )

    def _raise_for_status(self, response):
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Error {response.status_code}: {response.text}"
            )
        
# # ai_saas 測試
# if __name__ == "__main__":
#     load_dotenv("/Users/shaw/Documents/Advantech/Opportunity-discover/sales_autogen/.env")
#     client = AgentBuilder_APIClient()
#     print(client.query_agentbuilder('Jason', '研華科技'))
