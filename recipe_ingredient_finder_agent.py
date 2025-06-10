from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

from recipe_finder_tool import RecipeFinderTool
from recipe_finder import RecipeFinder

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

recipe_finder = RecipeFinder()
recipe_finder_tool = RecipeFinderTool(recipe_finder)

tools = [recipe_finder_tool.as_langchain_tool()]

recipe_name = "Spaghetti Bolognese"
user_query=f"""
List the ingredients of the following recipe: {recipe_name}.
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a shopping assistant. You have access to various tools to shop online and access recipes online."),
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
