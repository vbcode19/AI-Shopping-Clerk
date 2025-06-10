HEAD
# AI-Shopping-Clerk
# ai-shopping-clerk

## What it does

Accesses a grocery shopping website and prompts you to enter a recipe name you want to make.

Afterwards, the agent will add the recipe's ingredients to the cart.


```

## Details

It has two main langchain tools:
- `recipe_finder_tool.py`: Uses https://www.themealdb.com API to find the ingredients of a recipe.
- `add_product_tool.py`: Uses Selenium to interact with the webpage and add ingredients to the cart.
>>>>>>> e950382 (Initial commit)
