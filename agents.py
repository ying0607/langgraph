from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool

from LangGraph.prompts.specialized_agent_prompt import (
    get_supervisor_prompt,
    get_customer_lead_prompt,
    get_customer_profile_prompt,
    get_customer_order_prompt,
    get_personalize_recommendation_prompt,
)

from LangGraph.utils.azure_openai_helper import get_azure_openai_instance
from LangGraph.Tools.customerLeadAgentTool import customer_lead_process_tool
from LangGraph.Tools.customer_profile_api import test_profile_api
from LangGraph.Tools.customer_order_tool import customer_order_process_tool
from LangGraph.Tools.aws_recommendation_api import test_recommendation_api
from LangGraph.Tools.supervisorTool import prepare_dict_answer
 

# sub-agents for different inquery scenario
def create_agent(agent_name: str, parallel_tool_calling:bool): 

    llm = get_azure_openai_instance(
                                deployment_name='gpt-4o', 
                                temperature=0,
                                parallel_tool_calling=parallel_tool_calling
                                )
 
    match agent_name:
        
        case "Supervisor":
            supervisor_prompt = get_supervisor_prompt()
            supervisor = create_react_agent(
                model=llm,
                tools=[prepare_dict_answer, 
                       create_handoff_tool(agent_name="Customer_Lead_Agent"), 
                       create_handoff_tool(agent_name="Customer_Profile_Agent"),
                       create_handoff_tool(agent_name="Customer_Order_Agent"),
                       create_handoff_tool(agent_name="Personalize_Recommendation_Agent")],
                name="Supervisor",
                prompt=(supervisor_prompt)
            )
            return supervisor
        
 
        case "Customer_Lead_Agent":
            customer_lead_prompt = get_customer_lead_prompt()
            customer_lead_agent = create_react_agent(
                model=llm,
                tools=[customer_lead_process_tool, 
                       create_handoff_tool(agent_name="Supervisor"), 
                       create_handoff_tool(agent_name="Customer_Profile_Agent"),
                       create_handoff_tool(agent_name="Customer_Order_Agent"),
                       create_handoff_tool(agent_name="Personalize_Recommendation_Agent")],
                name="Customer_Lead_Agent",
                prompt=(customer_lead_prompt)
            )
            return customer_lead_agent
 
 
        case "Customer_Profile_Agent":
            customer_profile_prompt = get_customer_profile_prompt()
            customer_profile_agent = create_react_agent(
                model=llm,
                tools=[test_profile_api, 
                       create_handoff_tool(agent_name="Supervisor"), 
                       create_handoff_tool(agent_name="Customer_Lead_Agent"),
                       create_handoff_tool(agent_name="Customer_Order_Agent"),
                       create_handoff_tool(agent_name="Personalize_Recommendation_Agent")],
                name="Customer_Profile_Agent",
                prompt=(customer_profile_prompt)
            )
            return customer_profile_agent
        

        case "Customer_Order_Agent":
            customer_order_prompt = get_customer_order_prompt()
            customer_order_agent = create_react_agent(
                model=llm,
                tools=[customer_order_process_tool, 
                       create_handoff_tool(agent_name="Supervisor"), 
                       create_handoff_tool(agent_name="Customer_Lead_Agent"),
                       create_handoff_tool(agent_name="Customer_Profile_Agent"),
                       create_handoff_tool(agent_name="Personalize_Recommendation_Agent")],
                name="Customer_Order_Agent",
                prompt=(customer_order_prompt)
            )
            return customer_order_agent
 
 
        case "Personalize_Recommendation_Agent":
            personalize_recommendation_prompt = get_personalize_recommendation_prompt()
            personalize_recommendation_agent = create_react_agent(
                model=llm,
                tools=[test_recommendation_api,
                       create_handoff_tool(agent_name="Supervisor"), 
                       create_handoff_tool(agent_name="Customer_Lead_Agent"), 
                       create_handoff_tool(agent_name="Customer_Profile_Agent"),
                       create_handoff_tool(agent_name="Customer_Order_Agent")],
                       
                name="Personalize_Recommendation_Agent",
                prompt=(personalize_recommendation_prompt)
            )
            return personalize_recommendation_agent














































































