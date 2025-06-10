import json
from typing import List, Optional

class Recipe:
    def __init__(self, name: str, ingredients: List[str], instructions: str, youtube_link: Optional[str]):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.youtube_link = youtube_link

    def __str__(self):
        return f"Recipe: {self.name}\nIngredients:\n" + \
               "\n".join(f"- {i}" for i in self.ingredients) + \
               f"\n\nInstructions:\n{self.instructions}\n\nVideo: {self.youtube_link or 'N/A'}"

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "youtube_link": self.youtube_link
        }

    @staticmethod
    def from_json(data: str) -> 'Recipe':
        obj = json.loads(data)
        return Recipe(
            name=obj["name"],
            ingredients=obj["ingredients"],
            instructions=obj["instructions"],
            youtube_link=obj.get("youtube_link")
        )