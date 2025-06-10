import requests
from typing import Optional
from recipe import Recipe

class RecipeFinder:
    API_URL = "https://www.themealdb.com/api/json/v1/1/search.php"

    def _fetch_recipe(self, recipe_name: str) -> Optional[Recipe]:
        params = {"s": recipe_name}
        response = requests.get(self.API_URL, params=params)
        data = response.json()

        meals = data.get("meals")
        if not meals:
            return None

        meal = meals[0]

        name = meal["strMeal"]
        instructions = meal["strInstructions"].strip()
        youtube_link = meal.get("strYoutube")

        ingredients = []
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ing and ing.strip():
                entry = f"{measure.strip()} {ing.strip()}" if measure and measure.strip() else ing.strip()
                ingredients.append(entry)

        return Recipe(name=name, ingredients=ingredients, instructions=instructions, youtube_link=youtube_link)
    
    def find_recipe(self, recipe_name: str) -> Optional[Recipe]:
        return self._fetch_recipe(recipe_name)

# Example usage:
if __name__ == "__main__":
    recipe_finder = RecipeFinder()
    recipe = recipe_finder.find_recipe("Spaghetti Bolognese")
    if recipe:
        print(recipe.to_json())
    else:
        print("Recipe not found.")
else:
    print(f"Importing module: {__name__}...")
