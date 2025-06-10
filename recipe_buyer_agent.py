from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from recipe_finder_tool import RecipeFinderTool
from recipe_finder import RecipeFinder

recipe_finder = RecipeFinder()
recipe_finder_tool = RecipeFinderTool(recipe_finder)

from add_product_tool import AddProductTool
from add_product_impl_llm import AddProductImplLlm

add_product_impl_llm = AddProductImplLlm()
add_product_tool = AddProductTool(add_product_impl_llm)

tools = [recipe_finder_tool.as_langchain_tool(), add_product_tool.as_langchain_tool()]

# recipe_name = "Spaghetti Bolognese"
# user_query=f"""
# I would like to make a {recipe_name}, add what's needed to cart.
# """
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a shopping assistant. You have access to various tools to shop online and access recipes online. "
        "Keep in mind that the online shop is french and that you need to search for simple foods without quantities in them."
        "Even if ingredients from recipes are in english, you should search for terms in french!"
        "In markdown give an overview of what you bought/missing and then a link to the recipe youtube video."),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = ChatOpenAI(model="gpt-4o")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

from driver import SeleniumDriverSingleton
driver = SeleniumDriverSingleton()
driver.access_web_page("https://www.delhaize.be/")
user_query = driver.show_popup_and_get_result()
agent_response = agent_executor.invoke({"input": user_query})
print(agent_response['output'])

from show_result import show_markdown_popup
show_markdown_popup(driver, agent_response['output'])
