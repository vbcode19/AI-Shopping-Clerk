from termcolor import colored
from add_product_impl import AddProductImpl
from openai import OpenAI # type: ignore
from enum import Enum

class LlmModels(Enum):
    GPT40MINI = "gpt-4o-mini"
    GPT40 = "gpt-4o"

class AddProductImplLlm(AddProductImpl):
    def __init__(self):
        super().__init__()

        self._client = OpenAI()
        self._model = LlmModels.GPT40MINI

    def process(self, request: str) -> str:
        try:
            response = self._client.responses.create(
                model=self._model.value,
                input=request
            )
            return response.output_text
        except Exception as e:
            print(colored(f"OpenAI: {e}", "red"))
            raise

    def add_product_condition(self, product_name, product_name_to_search):
        query = f"""\
        Given this product name: {product_name} does it fit what I was searching for: {product_name_to_search}
        Answer only with true or false
        """

        response = self.process(query).lower()
        if "true" in response:
            print(colored(f"LLm validated {product_name} for search: {product_name_to_search}", "green"))
            return True
        
        return False

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    add_product_impl_llm = AddProductImplLlm()
    add_product_impl_llm.add_product_by_name("pomme")
    input("Press Enter to close browser and end script...")
else:
    from dotenv import load_dotenv
    load_dotenv()
    print(f"Importing module: {__name__}...")

