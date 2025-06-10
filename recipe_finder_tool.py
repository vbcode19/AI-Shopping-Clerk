from termcolor import colored
import inspect
from langchain_core.tools import Tool
from recipe_finder import RecipeFinder
import json

class RecipeFinderTool():
    def __init__(self, recipe_finder):
        super().__init__()
        self._recipe_finder = recipe_finder

    def find_recipe(self, input=None, print_trace=False) -> dict:
        func_name = inspect.currentframe().f_code.co_name
        print(colored(f"func: {func_name} ---> Working...", 'yellow'))
        if not isinstance(input, str):
            raise TypeError(f"Expected a str got {input}")
        recipe = self._recipe_finder.find_recipe(input)
        if recipe:
            return recipe.to_json()
        print(colored(f"Recipe {input} not found!", "red"))
        return {}

    def as_langchain_tool(self):
        return Tool.from_function(
            func=self.find_recipe,
            name="find_recipe",
            description=(
                "Searches for a recipe by name and returns its details as a JSON object. "
                "The input is a string representing the recipe name (e.g., 'Spaghetti Bolognese').\n\n"
                "The output is a JSON object with the following fields:\n"
                "  - name: string, the name of the recipe\n"
                "  - ingredients: list of strings, each string is an ingredient with quantity (e.g., '2 eggs')\n"
                "  - instructions: string, step-by-step cooking instructions\n"
                "  - youtube_link: string or null, a link to a YouTube video for the recipe\n\n"
                "If the recipe is not found, an empty JSON object `{}` is returned."
            )
        )
    
if __name__ == "__main__":
    recipe_finder = RecipeFinder()
    tool = RecipeFinderTool(recipe_finder)
    tool_func = tool.as_langchain_tool()
    output = tool_func.invoke("Spaghetti Bolognese", print_trace=True)
    print(colored(f"Output {json.dumps(output, indent=2)}", 'green'))
else:
    print(f"Importing module: {__name__}...")

