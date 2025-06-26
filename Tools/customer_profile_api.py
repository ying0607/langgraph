from typing import Annotated
from langchain_core.tools import tool
from LangGraph.utils.AI_SaaS_utils.ai_saas_agent_builder_api import AgentBuilder_APIClient
from LangGraph.utils.set_thread_id_folder import get_userID_config

from dotenv import load_dotenv
load_dotenv("LangGraph\.env")

@tool
def test_profile_api(
    question: Annotated[str, "User's query about customer's profile."],
):
    """
    Tool to execute api calling to obtain personalize recommendation result.
    """    
    try:
        # calling AI-SaaS AgentBuilder API
        client = AgentBuilder_APIClient()
        config = get_userID_config(result = "id")
        result = client.query_agentbuilder(config, question)
        answer = result.get("response", {}).get("answer", "AgentBuilder has no content to display for this inquiry.")
        return {"result": answer}
    except Exception as e:
        return {"result": "An issue occurred during the agent call using AgentBuilder. Please contact a developer for assistance."}