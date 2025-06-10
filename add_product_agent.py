from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

from add_product_tool import AddProductTool
from add_product_impl_llm import AddProductImplLlm

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

add_product_impl_llm = AddProductImplLlm()
add_product_tool = AddProductTool(add_product_impl_llm)

tools = [add_product_tool.as_langchain_tool()]

product_name = ["pomme", "boeuf"]
user_query=f"""
I want to add the following products to my cart: {product_name}
Explain what you did briefly.
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a shopping assistant. You have access to various tools to shop online."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
agent_response = agent_executor.invoke({"input": user_query})
print(agent_response['output'])
