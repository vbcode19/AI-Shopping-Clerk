from termcolor import colored
import inspect
from langchain_core.tools import Tool
from add_product_impl_llm import AddProductImplLlm

class AddProductTool():
    def __init__(self, add_product_impl):
        super().__init__()
        self._add_product_impl = add_product_impl

    def add_product(self, input=None, print_trace=False) -> bool:
        func_name = inspect.currentframe().f_code.co_name
        print(colored(f"func: {func_name} ---> Working...", 'yellow'))
        if not isinstance(input, str):
            raise TypeError(f"Expected a str got {input}")
        return self._add_product_impl.add_product_by_name(input)

    def as_langchain_tool(self):
        return Tool.from_function(
            func=self.add_product,
            name="add_product",
            description="" \
            "Adds a given product to cart given its name. The input is the name of the food as a string. " \
            "If the product is found/not found it should return True or False."
        )
    
if __name__ == "__main__":
    add_product_impl_llm = AddProductImplLlm()
    tool = AddProductTool(add_product_impl_llm)
    tool_func = tool.as_langchain_tool()
    output = tool_func.invoke("pomme", print_trace=True)
    print(colored(f"Output {output}", 'yellow'))
else:
    print(f"Importing module: {__name__}...")

