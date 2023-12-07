import requests
import os
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')


def api_call(ingredient,
             meal_type="",
             allergy="",
             calories="",
             cuisine="",
             time=""):
    """Function to connect to the Edamam API and return results"""
    app_id = APP_ID
    app_key = APP_KEY
    url = f'https://api.edamam.com/api/recipes/v2?type=public&q=\
            {ingredient}&app_id={app_id}&app_key=\
            {app_key}{allergy}{cuisine}{meal_type}{calories}{time}'
    response = requests.get(url)
    recipe = response.json()
    return recipe['hits']
