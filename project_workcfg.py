import requests

#This programme uses f-strings rather than the .format() method, just to make code more concise. Can be easily changed!

def api_call(ingredient, meal_type="", allergy="", calories="", cuisine=""): 
    """Function to connect to the Edamam API and return results"""

    #as the ingredient parameter is the only required input, the other parameters are set to an empty string
    #this empty string then doesn't alter the url to make the API call still work
    #in the 'url' there's a backslash and this allows to write the code over multiple lines without changing the code
    app_id = "f0658537"
    app_key = "192de87bcacd81d0ab71035e57b2a00c"
    url = f'https://api.edamam.com/api/recipes/v2?type=public&q={ingredient}&app_id={app_id}&app_key=\
        {app_key}{allergy}{cuisine}{meal_type}{calories}'
    response = requests.get(url) #creates a response OBJECT, has to be converted to be able to read the data
    recipe = response.json() #converts the API response object into a readable JSON data (similar to dict)
    return recipe['hits']


def allergy_checker():
    """Function for checking for allergies or if a vegan or vegetarian diet followed, optional field"""

    print("\nThis is an optional field, to skip this question please press enter")
    print("Do you have any allergies you wish to declare or follow a vegan or vegetarian diet?\
    \nExamples include:\nDairy\nShellfish\nCelery\nGluten\nPlease enter just one word if answering\n\
If your answer is red meat or tree nut, please type red-meat or tree-nut with the hyphen.")
    while True:
        allergies = input("Type here: ")  
        #the \n creates a new line when run, putting 1 \ allows to write this code over multiple lines without
        #changing how it displays to the user
        allergies = allergies.lower()  #taking the input and making it lower case to check the string easily
        list_of_allergies = ["alochol", "celery", "crustacean", "dairy", "egg", "fish", "fodmap",
                            "gluten", "mollusk", "mustard", "peanut", "pork", "red-meat", "seasame",
                              "shellfish","soy", "sulfite", "tree-nut", "wheat"]        
        if allergies == "":
            formatted_allergies = ""
            return formatted_allergies
        elif allergies == "vegan" or allergies == "vegetarian":
            formatted_allergies = f"&health={allergies}"
            return formatted_allergies
        elif allergies in list_of_allergies:
            formatted_allergies = f"&health={allergies}-free"
            return formatted_allergies
        try_again = input("Sorry I don't recognise your answer, would you like to see the allergen list?: ")
        if try_again == "yes":
            print("\n")
            for allergen in list_of_allergies:
                print(allergen.title())
            print("You can always press enter to skip this question")
        elif try_again == "no":
            print("\nYou can always press enter to skip this question\n")
        else:
            print("\nSorry, I don't recongise your answer, let's try again.\n")


def find_meal_type():
    """Function to allow user to enter what type of meal the recipe searcher returns """

    print("\nThis is an optional field, to skip this question please press enter")
    while True:
        meal_type = input("What type of meal would you like to make?\nBreakfast\nLunch\nDinner\nSnack\nTeatime\nType here: ")
        meal_type = meal_type.title() #capitalises the input which is the required format for api call
        list_of_meal_types = ["Breakfast", "Lunch", "Dinner", "Snack", "Teatime"]
        if meal_type == "":
            return ""
        elif meal_type == "Tea Time":
            meal_type = "Teatime"
            return"&mealType="+meal_type
        elif meal_type in list_of_meal_types:
            return "&mealType="+meal_type
        else:
            print("\nOops, I didn't quite understand that. Let's try again")


def cuisine_type():
    """Function to allow user to enter cusine type and format ready for API call"""

    while True:
        print("\nWould you like to specify what type of cuisine the recipes are? E.g. Italian, French etc. (yes/no)")
        yes_or_no = input("Type here: ")
        yes_or_no = yes_or_no.lower()
        list_of_cuisines = ["American", "Asian", "British", "Caribbean", "Central Europe", "Chinese",
                            "Eastern Europe", "French", "Indian", "Italian", "Japanese", "Kosher",
                            "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "South American",
                            "South East Asian"]
        if yes_or_no == "yes":
            print("\nHere's all the different cuisines available to search (there's quite a few!)")
            for dish in list_of_cuisines:
                print(dish)
            while True:
                cuisine = input("Which cuisine would you like to search?\nType here: ")
                cuisine = cuisine.title()
                if cuisine in list_of_cuisines:
                    return f"&cuisineType={cuisine}"
                else:
                    print("Oops, I didn't quite get that, let's try again")
        elif yes_or_no == "no":
            cuisine = ""
            return cuisine
        else:
            print("Oops, was there a spelling error? Let's try again")



def calorie_range():
    """Function to check if user wants to specify calories, if specified, results will show calorie content"""

#this while loop is added so that actions only occur if 'yes' or 'no' specified
    while True:
        calories = input("\nWould you like to specifiy the maximum calorie content? (yes/no): ")
        calories = calories.lower()
        if calories == "no":
            calorie_range = ""
            return calorie_range #this ends the while loop 
        elif calories == "yes":
            while True: #this second while loop only allows integer values and not text.
                calorie_limit = input("What is the maximum calorie content you would like to search?: ")
                try:
                    calorie_range = int(calorie_limit)
                    calorie_range = f"&calories=0-{calorie_limit}" 
                    return calorie_range #this also ends the while loop
                except ValueError:
                    print("Oops that didn't work, please enter an integer not text")
        print("Oops, I don't recognise your answer. Maybe something was spelled incorrectly, let's try again")
        #this last statement will keep looping back until the user inputs something correctly    


def collect_data_with_kcals(recipes):
    """Collecting API results with kcals into a a list to easily add to a save file"""

    data = []
    for item in recipes:
        data.append(f"Recipe Name: {item['recipe']['label']}")
        data.append(f"{round(item['recipe']['calories'], 2)} kcals")
        data.append(f"{round((item['recipe']['calories'] / item['recipe']['yield']), 2)} kcals")
        data.append('List of Ingredients:')
        for ingredient in (item['recipe']['ingredientLines']):
            data.append(ingredient)
        data.append(f"Link to Full Recipe: {item['recipe']['url']}\n")
        data.append("\n")
        #this is just the same data we printed out in the results. Used .append() method to add to a list
    return data     


def collect_data_without_kcals(recipes):
    """Collecting API results without kcals into a a list to easily add to a save file"""

    data = []
    for item in recipes:
        data.append(f"Recipe Name: {item['recipe']['label']}")
        data.append('List of Ingredients:')
        for ingredient in (item['recipe']['ingredientLines']):
            data.append(ingredient)
        data.append(f"Link to Full Recipe: {item['recipe']['url']}")
        data.append("\n")
        #this is just the same data we printed out in the results. Used .append() method to add to a list
    return data  


def search_again():
    """Function to check if user wants to do the search again"""

    #this while loop means users can only enter 'yes' or 'no' and will loop back if spelling error
    while True:
        go_again = input("\nWould you like to use the search again? (yes/no): ")
        go_again = go_again.lower()
        if go_again == "yes":
            return recipe_search()
        elif go_again == "no":
            print("Thanks for using our recipe searcher, hope you come back soon!")
            break
        print("Oops, something went wrong, let's try again")


def save_recipes(list):
    """Function to allow user to optionally save recipes. Allows user input for name. """

    #this while loop means users can only enter 'yes' or 'no' and will loop back if spelling error
    while True: 
        save_recipe = input("\nWould you like to save your results in a file? (yes/no): ")
        save_recipe = save_recipe.lower()
        if save_recipe == "yes":
            print("\nWhat name would like to call your file?\
                  \nYou can always use the same file name to add to an existing file.")
            name = input("Type here: ")
            file = name.lower() + ".txt"
            with open(file, 'a', encoding="utf-8") as r_file:
                r_file.write("\n".join(list))       
                #"\n".join(list) bit of code takes each item in the list and "joins" it with a new line (\n)
                # this just helps the formatting when writing the file and will automatically save in the style as it's printed on screen
                # the file is open in 'a' mode which is append mode. This means it will not overwrite a file
                # and will add it to the bottom instead, allowing users to just create 1 file if they want
            print("We've now saved this for you. Happy cooking!")
            return search_again()
        elif save_recipe == "no":
            return search_again()
        print("Oops, I didn't quite get that. Let's try again (please enter yes or no)")


def recipe_search():
    """Function to take all user input , call the API, and return results"""

    print("\nHere's a simple recipe searcher based on what ingredient you want to use.")
    print("The ingredient is the only required part, but we have a few optional questions to get you the best results!")
    print("After getting your results, you also have the option to save your search to a file.")
    ingredient = input("What ingredient do you want to use?: ")
    allergy = allergy_checker()
    meal_type = find_meal_type()
    cuisine = cuisine_type()
    calories = calorie_range()
    #this following try and except block of code will make it so instead of getting a syntax error, 
    # we account for any API calls that don't work without displaying the status_code to the user
    try:  
        recipes = api_call(ingredient, meal_type, allergy, calories, cuisine)
        if calories:
            data_for_saving = collect_data_with_kcals(recipes)
            for item in recipes:
                print('\n\nRecipe Name:', item['recipe']['label'])
                print('Total calorie content:', round(item['recipe']['calories'], 2),'kcals')
                print('Calorie content per portion:', round((item['recipe']['calories'] / item['recipe']['yield']), 2),'kcals')
                print('List of Ingredients:')
                for ingredient in (item['recipe']['ingredientLines']):
                    print(ingredient)
                print('Link to Full Recipe:', item['recipe']['url'])
            save_recipes(data_for_saving)
        else:
            data = collect_data_without_kcals(recipes)
            for item in recipes:
                print('\nRecipe Name:', item['recipe']['label'])
                print('List of Ingredients:')
                for ingredient in (item['recipe']['ingredientLines']):
                    print(ingredient)
                print('Link to Full Recipe:', item['recipe']['url'])
            save_recipes(data)
    except:
        print("Sorry, something went wrong! Maybe something was spelled incorrectly or included more words. Let's try that again.")


recipe_search()