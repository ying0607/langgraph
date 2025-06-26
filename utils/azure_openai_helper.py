import os
from langchain_openai import AzureChatOpenAI

def get_azure_openai_instance(deployment_name: str, temperature: int, parallel_tool_calling: bool = None) -> AzureChatOpenAI:
    '''
    Get the Azure OpenAI chat instance based on the deployment name and temperature
    '''
 
    from dotenv import load_dotenv
    load_dotenv("LangGraph/.env")

    # # LangSmith Tracing
    # os.environ["LANGSMITH_TRACING"] = "true"  # Change false to true when needed
    # LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY')
 
    if parallel_tool_calling is None:
 
        return AzureChatOpenAI(
                    deployment_name=deployment_name,
                    temperature=temperature,
                    openai_api_version="2024-08-01-preview",
                    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                    openai_api_key=os.getenv('AZURE_OPENAI_API_KEY'),
                )
    
    else:
 
        return AzureChatOpenAI(
                    deployment_name=deployment_name,
                    temperature=temperature,
                    openai_api_version="2024-08-01-preview",
                    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                    openai_api_key=os.getenv('AZURE_OPENAI_API_KEY'),
                    parallel_tool_calls=parallel_tool_calling
                )