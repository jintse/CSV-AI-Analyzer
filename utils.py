import json
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

PROMPT_TEMPLATE = """
    You are a data analysis assistant, and your responses depend on the user's request.
    
    For text-based answers, respond in the following format: 
    {"answer": "<your answer here>"} Example: {"answer": "The product ID with the highest order volume is 'MNWC3-067'"}
    
    If the user requests a table and a text-based answers, respond in the following format: 
    {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...] }, "answer": "<your answer here>"}
    
    If the user's request suits a bar chart and a text-based answers, respond in the following format: 
    {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}, "answer": "<your answer here>"}
    
    If the user's request suits a line chart and a text-based answers, respond in the following format: 
    {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}, "answer": "<your answer here>"}
    
    If the user's request suits a scatter plot and a text-based answers, respond in the following format: 
    {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}, "answer": "<your answer here>"}
    
    Note: Only three types of charts are supported: "bar", "line", and "scatter".
    
    Ensure all outputs are returned as JSON strings. Remember to enclose all strings in the "columns" list and the data list with double quotes.
    Example:
    {"table": {"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}, "answer": "<your answer here>"}
    
    The user request you need to handle is as follows:
    """


def dataframe_agent(openai_api_key, df, query):
    model = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key, openai_api_base="https://api.aigc369.com/v1",
                       temperature=0)
    agent = create_pandas_dataframe_agent(llm=model, df=df,
                                          agent_executor_kwargs={"handle_parsing_errors": True},
                                          verbose=True,)
    prompt = PROMPT_TEMPLATE + query
    response = agent.invoke({"input": prompt})
    response_dict = json.loads(response["output"])
    return response_dict

###test
#import pandas as pd

#df = pd.read_csv("personal_data.csv")
#print(dataframe_agent(openai_api_key=, df=df, query="make a list of engineers"))

