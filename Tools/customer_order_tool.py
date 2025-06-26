import os
import pandas as pd

from typing import Literal
from langchain_core.messages import AIMessage
from langgraph.graph import MessagesState, START, END
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph
from typing import Annotated
import json

from langgraph.types import Checkpointer

import io
import logging
import sys

logger = logging.getLogger(__name__)

from LangGraph.utils.AI_SaaS_utils.ai_saas_denodo_api import APIClient
from langchain_core.tools import tool
from LangGraph.prompts.customer_order_prompt import (
    question_analyzer_agent_prompt,
    keywords_agent_prompt,
    sql_agent_prompt, 
    denodo_data_agent_prompt,
    get_dataframe_agent_prompt,
    result_agent_prompt
)
from LangGraph.utils.azure_openai_helper import get_azure_openai_instance

from LangGraph.utils.set_thread_id_folder  import get_userID_config
config = ""

from dotenv import load_dotenv
load_dotenv("LangGraph\.env")


unparallel_model = get_azure_openai_instance(
                                deployment_name='gpt-4o', 
                                temperature=0,
                                parallel_tool_calling=False
                                )

model = get_azure_openai_instance(
                                deployment_name='gpt-4o',
                                temperature=0,
                                )

def create_graph():

    question_analyzer_node = create_agent("question_analyzer_agent")
    keywords_node = create_agent("keywords_agent")
    sql_agent_node = create_agent("sql_agent")
    denodo_data_agent_node = create_agent("denodo_data_agent")
    dataframe_agent_node = create_agent("dataframe_agent")
    result_agent_node = create_agent("result_agent")
    
    workflow = StateGraph(MessagesState) # GraphState
    workflow.add_edge(START, "question_analyzer_agent")
    workflow.add_node("question_analyzer_agent", question_analyzer_node)
    workflow.add_node("keywords_agent", keywords_node)
    workflow.add_node("sql_agent", sql_agent_node)
    workflow.add_node("denodo_data_agent", denodo_data_agent_node)
    workflow.add_node("dataframe_agent", dataframe_agent_node)
    workflow.add_node("result_agent", result_agent_node)

    workflow.add_edge("question_analyzer_agent", "keywords_agent")
    workflow.add_edge("keywords_agent", "sql_agent")
    workflow.add_edge("sql_agent", "denodo_data_agent")
    workflow.add_edge("denodo_data_agent", "dataframe_agent")
    workflow.add_edge("dataframe_agent", "result_agent")
    workflow.add_edge("result_agent", END)

    graph = workflow.compile()

    return graph


@tool
def customer_order_process_tool(
    user_query: Annotated[str, "it is the user query that only align to Customer Order request."]
):
    """
    use this tool to invoke the graph and obtain the answer that can answer Customer Order related query.
    Args:
        user_query (str) :
        the user query that only align to Customer Order request.
    Returns:
        A customer order relate information prepared in MS adaptive card json format data.
    """

    # print(f"user_query: {user_query} successfully send into customer_order_process_tool tool call")
    logger.info(f"user_query: {user_query} successfully send into customer_order_process_tool tool call\n")


    # Initialize langGraph workflow
    graph = create_graph()
    
    config = get_userID_config(result = "id")
    folder_path = os.path.join("LangGraph", "Data", config)

    # 如果資料夾不存在，就建立；否則不做任何事
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        # print(f"\n\n\n\n資料夾已建立：{folder_path}")
        logger.info(f"資料夾已建立：{folder_path}\n")
    else:
        # print(f"\n\n\n\n資料夾已存在，無需重新建立：{folder_path}")
        logger.info(f"資料夾已存在，無需重新建立：{folder_path}\n")

    # activate(invoke) the graph
    response = graph.invoke(
        {"messages":user_query},
    )

    logger.info("\n\n===========✴️ Start of Pretty Print in customer_order_process_tool ✴️===========")
    for m in response["messages"]:
        print(m.pretty_print())
    logger.info("\n\n============✴️ End of Pretty Print in customer_order_process_tool ✴️============")
    
    # 創建並執行完整的 LangGraph 流程
    final_response = response["messages"][-1].content
    
    # 返回結果
    return final_response


ai_saas_client = APIClient()
@tool
def denodo_data(
    sql_query: Annotated[str, "SQL Query to save csv file, please only keep the SQL Query in string."],
    Tran_Type: Annotated[str, "You will get 'Tran_Type' from key word set, it ususally is one of [booking, Shipment, Backlog], if you don't know, just assign None. MOST IMPORTANTLY, PLEASE MAKE SURE THE Tran_Type column looks like 'Tran_Type' in the sql query."],
    customername: Annotated[str, "You will get customername from key word set, it should be the customer's name, if you don't know, just assign None. Please assign with the python None dtype instead of string type. Can't assign like 'None'"] = None,
    po_no: Annotated[str, "You will get po_no from key word set, if you don't know, just assign None. Please assign with the python None dtype instead of string type. Can't assign like 'None'"] = None
):  
    """
    Tool to access to Denodo DB with SQL Query and save csv file
    """ 
    config = get_userID_config(result = "id")

    keywords = {
        "Tran_Type": Tran_Type,
        "customername": customername,
        "po_no": po_no
    }

    segments = [
        str(keywords[k]).replace(" ", "_")
        for k in ("Tran_Type", "customername", "po_no")
        if keywords[k] is not None
    ]

    # 用底線串起來，組成檔名
    file_name = f"LangGraph/Data/{config}/{'_'.join(segments)}.csv"
    denodoserver_name = os.getenv("DENODOSERVER_DATABASE")

    try:

        data = ai_saas_client.query_database(denodoserver_name, sql_query)
                
        # Convert the JSON response to a DataFrame
        df = pd.DataFrame(data['data'])

        if df.empty:
            logger.info("Error: Data is empty after executing SQL Query on DenodoDB.")
            return json.dumps({"message": f"Error: Data is empty after executing SQL Query on DenodoDB."}, ensure_ascii=False)

        df.to_csv(file_name, index=False, encoding="utf-8-sig")

        return json.dumps({"csv file path" : f"{file_name}"}, ensure_ascii=False)
        
        # return f"output csv file name is {file_name} **. Following agent please write an pandas dataframe code with the precise naming format to access and manipulate this csv file. "
    
    except Exception as e:
        print(f"Error executing query: {e}")
        logger.info("Error executing SQL Query on DenodoDB.")
        return json.dumps({"message": f"Error executing query: {str(e)}."}, ensure_ascii=False)


from langchain_experimental.utilities import PythonREPL
repl = PythonREPL()
@tool
def code_execution_tool(
    code: Annotated[str, "Python code string which should be executed in tool"],
):
    """
    use this tool to execute python code 
    """

    logger.info(f"code_execution_tool is called with code: {code}\n")
    outcome = repl.run(code)

    logger.info(f"Executed outcome is: {outcome}\n")
    
    return json.dumps({"Python Code": f"Executed python code is: {code}",
                       "Outcome": f"Outcome after executing python code is: {outcome}"}, ensure_ascii=False )


@tool
def result_analyzation():
    """
    Reads the output CSV file, formats the data as a Markdown table, and returns it.
    """

    # Function to format the values as accounting format with $ sign
    def accounting_format(val):
        # Round to the nearest integer
        val = round(val)
        
        if val < 0:
            return "${:,.0f}".format(abs(val))  # Negative values with parentheses
        else:
            return "${:,.0f}".format(val)

    config = get_userID_config(result = "id")
    file_name = f"LangGraph/Data/{config}/customer_order_output.csv"

    if pd.read_csv(file_name).empty:
        logger.info("Error: Dataframe is empty")
        return json.dumps({"message": "Error: Dataframe is empty"}, ensure_ascii=False)
    else:
        df = pd.read_csv(file_name)

        for col in ['US Amount', 'Qty', 'Unit Price']:
            if col in df.columns:
                df[col] = df[col].apply(accounting_format)

        df = df.rename(columns={
            "Shipment Total":    "Shipment Total（USD）",
            "US Amount":         "US Amount（USD）",
            "Qty Total":         "Qty Total",
            "Qty":               "Qty",
            "Unit Price":        "Unit Price（USD）"
        })

        # prepare_adaptive_card
        columns = df.columns.tolist()
        data_values = df.values.tolist()
        body = []

        # 1) Create a header row as a single ColumnSet
        header_columns = []
        for col_name in columns:
            header_columns.append({
                "type": "Column",
                "width": "stretch",  # or "auto"
                "items": [
                    {
                        "type": "TextBlock",
                        "text": col_name,
                        "weight": "bolder",
                        "wrap": True
                    }
                ]
            })
        body.append({
            "type": "ColumnSet",
            "columns": header_columns
        })
        
        # 2) Create one ColumnSet per data row
        for row in data_values:
            row_columns = []
            for cell_value in row:
                row_columns.append({
                    "type": "Column",
                    "width": "stretch",  # or "auto"
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": str(cell_value),
                            "wrap": True
                        }
                    ]
                })
            body.append({
                "type": "ColumnSet",
                "columns": row_columns
            })

        # 3) Build the final Adaptive Card
        adaptive_card = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.0",
            "body": body
        }

        with open(f"LangGraph/Data/{config}/customer_order_result.json", 'w', encoding='utf-8') as json_file:
            json.dump(adaptive_card, json_file, ensure_ascii=False, indent=4)
        
    # # ------------------------- Token Checkout -------------------------
    # # 先放上來跑測試，後續再確認更好的解決方式
    # import tiktoken
    # enc = tiktoken.encoding_for_model("gpt-4o")
    # tokens = enc.encode(adaptive_card)

    # if tokens > 4090:
    #     logger.info("Error: response exceeds token limit")
    #     return json.dumps({"message": "Error: response exceeds token limit"}, ensure_ascii=False)
    # else:
    #     return f"{adaptive_card}"

    return adaptive_card 


def create_agent(agent_name: str):
    config = get_userID_config(result = "id")
    match agent_name:

        case "question_analyzer_agent":
            question_analyzer_agent = create_react_agent(
                model, 
                tools=[], 
                prompt=question_analyzer_agent_prompt
            )

            def question_analyzer_node(state: MessagesState) -> Command[Literal["keywords_agent"]]:
                
                logger.info(f"===============🔄️ {config} - Question Analyzer Agent Processing in Customer Order Workflow 🔄️===============")
                result = question_analyzer_agent.invoke(state)
                print(f"\n===============✴️ {config} - Output from Question Analyzer Agent is ✴️===============\n", result["messages"][-1].content)
                
                return Command(
                    update={
                        "messages": [
                            AIMessage(content=result["messages"][-1].content, name="question_analyzer_agent")
                        ]
                    },
                    goto="keywords_agent",
                )
            
            return question_analyzer_node


        case "keywords_agent":
            keywords_agent = create_react_agent(
                model, 
                tools=[], 
                prompt=keywords_agent_prompt
            )

            def keywords_node(state: MessagesState) -> Command[Literal["sql_agent"]]:

                logger.info(f"===============🔄️ {config} - Keywords Agent Processing in Customer Order Workflow 🔄️===============")
                result = keywords_agent.invoke(state)
                print(f"\n===============✴️ {config} - Output from Keywords Agent is ✴️===============\n", result["messages"][-1].content)
                
                return Command(
                    update={
                        "messages": [
                            AIMessage(content=result["messages"][-1].content, name="keywords_agent")
                        ]
                    },
                    goto="sql_agent",
                )
            
            return keywords_node
    

        case "sql_agent":
            sql_agent = create_react_agent(
                model, 
                tools=[], 
                prompt=sql_agent_prompt
            )

            def sql_node(state: MessagesState) -> Command[Literal["denodo_data_agent"]]:
                
                clean_messages = state["messages"][-1].content 
                logger.info(f"===============🔄️ {config} - SQL Agent Processing in Customer Order Workflow 🔄️===============")
                result = sql_agent.invoke({"messages": [{
                                                    "role": "user",
                                                    "content": clean_messages
                                                }]},)
                print(f"\n===============✴️ {config} - Output from SQL Agent is ✴️===============\n", result["messages"][-1].content)

                return Command(
                    update={
                        "messages": [
                            AIMessage(content=result["messages"][-1].content, name="sql_agent")
                        ]
                    },
                    goto="denodo_data_agent",
                )
            
            return sql_node

        case "denodo_data_agent":
            denodo_data_agent = create_react_agent(
                unparallel_model, 
                tools=[denodo_data], 
                prompt= denodo_data_agent_prompt 

            )

            def denodo_data_agent_node(state: MessagesState) -> Command[Literal["dataframe_agent"]]:
                clean_messages = state["messages"][-1].content      
                
                logger.info(f"===============🔄️ {config} - Denodo Data Agent Processing in Customer Order Workflow 🔄️===============")
                result = denodo_data_agent.invoke({"messages": [{
                                                    "role": "user",
                                                    "content": clean_messages
                                                }]},)
                print(f"\n===============✴️ {config} - Output from Denodo Data Agent is ✴️===============\n", result["messages"][-1].content)

                return Command(
                    update={
                        "messages": [
                            AIMessage(content=result["messages"][-1].content, name="denodo_data_agent")
                        ]
                    },
                    goto="dataframe_agent",
                )
            
            return denodo_data_agent_node

        case "dataframe_agent":
            dataframe_agent_prompt = get_dataframe_agent_prompt()    

            dataframe_agent = create_react_agent(
                unparallel_model, 
                tools=[code_execution_tool], 
                prompt=dataframe_agent_prompt
            )

            def dataframe_agent_node(state: MessagesState) -> Command[Literal["result_agent"]]:
                
                # 再確認一下這邊 INVOKE 的 INPUT MESSAGES
                user_messages = "User's Query is: " + state["messages"][0].content
                analyzed_question = "Information about solving user's query: " + state["messages"][1].content
                csv_file_info = "The path of csv files storing datasets: " + state["messages"][4].content
                clean_messages =  user_messages + "\n" + analyzed_question + "\n" + csv_file_info

                logger.info(f"===============🔄️ {config} - Dataframe Agent Processing in Customer Order Workflow 🔄️===============")
                result = dataframe_agent.invoke({"messages": [{
                                                    "role": "user",
                                                    "content": clean_messages
                                                }]},)
                print(f"\n===============✴️ {config} - Output from Dataframe Agent is ✴️===============\n", result["messages"][-1].content)

                return Command(
                    update={
                        "messages": [
                            AIMessage(content=result["messages"][-1].content, name="dataframe_agent")
                        ]
                    },
                    goto= "result_agent",
                )

            return dataframe_agent_node
    

        case "result_agent":
            result_agent = create_react_agent(
                unparallel_model, 
                tools=[result_analyzation], 
                prompt=result_agent_prompt
            )

            def result_agent_node(state: MessagesState) -> Command[Literal["__end__"]]:
                
                logger.info(f"===============🔄️ {config} - Result Agent Processing in Customer Order Workflow 🔄️===============")
                result = result_agent.invoke(state)
                print(f"\n===============✴️ {config} - Output from Result Agent is ✴️===============\n", result["messages"][-1].content)
                
                return Command(
                    update={
                        "messages": [
                            AIMessage(content=result["messages"][-1].content, name="result_agent")
                        ]
                    },
                    goto=END,
                )
            
            return result_agent_node