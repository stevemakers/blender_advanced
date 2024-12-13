from openai import OpenAI
from datetime import datetime
import json

"""
1 A blender should have the ability to create smoothies from food
2 Smoothies should store information about macronutrients and calories
"""
class Blender():
    def __init__(self):
        self.ingredients = []

    """
    Adds a list of ingredients to the blender
    Ingredient is an array of tuples containing grams and macronutrients
    e.g.
    [
        "oats",
        "blueberries"
    ]
    """
    def add_ingredients(self, ingredients):
        for i in ingredients:
            self.ingredients.append(i)
            
    
    """
    GPT ingredient suggestion and then adds them to blender
    """
    def suggest_and_add_complementary_ingredients(self):
        genius = FoodGeniusAPI()
        complementary_ingredients = genius.suggest_complementary_ingredients(self.ingredients)
        
        for i in complementary_ingredients:
            self.ingredients.append(i)
                
    """
    Blends all the ingredients that have been passed into the blender
    Gets an estimate of the ingredient macros from GPT
    Returns a Smoothie with the combined macronutrients and create_date
    """
    def blend_ingredients(self):
        genius = FoodGeniusAPI()
        macros = genius.get_macros(self.ingredients)
        create_date = datetime.today().strftime("%d/%m/%Y")
        return Smoothie(macros, create_date)

class Smoothie():
    def __init__(self, macros, create_date):
        self.macros = macros
        self.create_date = create_date

class FoodGeniusAPI():
    def __init__(self):
        self.client = OpenAI(api_key="")
        
    def suggest_complementary_ingredients(self, ingredients):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful health assistant."
                },
                {
                    "role": "user",
                    "content": f"I am making a smoothie. Take the following ingredients {ingredients}, and return me a comma seperated string of complementary values. DO NOT return an extraneous text and return only the ingredients"
                }
            ],

        )
        
        return completion.choices[0].message.content.split(', ')
        
    def get_macros(self, ingredients):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful health assistant."
                },
                {
                    "role": "user",
                    "content": f'Return a single json-like object of the combined macros (carbs, protein, fats) of the following ingredients. {ingredients}, ensure the output can be used by json.load() to output a python dict'
                }
            ],
        )
        
        message = completion.choices[0].message.content
        print(message)
        json_acceptable_string = message.replace("'", "\"")
        return json.loads(json_acceptable_string)