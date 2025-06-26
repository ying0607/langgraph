from langgraph.checkpoint.memory import InMemorySaver 
from langgraph_swarm import create_swarm
from LangGraph.agents import create_agent

import io
import logging
import sys

logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv(".env")


checkpoint = InMemorySaver()

async def call_langGraph_agents(thread_id:str, user_query: str):

    config = {"configurable": {"thread_id": thread_id}}
    
    #  建立 Sub-Agents
    customerLeadAgent_node = create_agent("Customer_Lead_Agent", parallel_tool_calling=False)
    customerProfileAgent_node = create_agent("Customer_Profile_Agent", parallel_tool_calling=False)
    customerOrderAgent_node = create_agent("Customer_Order_Agent", parallel_tool_calling=False)
    recommendation_node = create_agent("Personalize_Recommendation_Agent", parallel_tool_calling=False)
    supervisor_node = create_agent("Supervisor", parallel_tool_calling=False)

    multi_conversation = create_swarm(
        agents=[supervisor_node, customerLeadAgent_node, customerProfileAgent_node, customerOrderAgent_node, recommendation_node],
        default_active_agent="Supervisor",
    )

    app = multi_conversation.compile(checkpointer=checkpoint)   
    response = await app.ainvoke(
        {"messages": [{
            "role": "user",
            "content": user_query
        }]},
        config,
    )

    # Display in Logger
    logger.info("\n\n===============🌐 Start of Pretty Print in LangGraph Workflow  🌐===============")
    for m in response["messages"]:
        print(m.pretty_print())
        # buf = io.StringIO()
        # sys_stdout = sys.stdout
        # sys.stdout = buf
        # m.pretty_print()
        # sys.stdout = sys_stdout
        # logger.info(
        #     "\n%s\n%s",
        #     buf.getvalue().strip(),
        #     "================================================================================"
        # )
    logger.info("\n\n================🌐 End of Pretty Print in LangGraph Workflow  🌐================")

    final_response = response['messages'][-1].content

    return final_response
