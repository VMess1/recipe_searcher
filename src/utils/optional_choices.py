
def allergy_checker():
    """
    Function for checking for allergies or if a vegan or
    vegetarian diet followed, optional field
    """
    print("\nThis is an optional field, to skip"
          + " this question please press enter")
    print("Do you have any allergies you wish to declare or "
          + "follow a vegan or vegetarian diet?"
          + "\nExamples include:\nDairy\nShellfish\nCelery\nGluten\n"
          + "Please enter just one word if answering\n"
          + "If your answer is red meat or tree nut, please type "
          + "red-meat or tree-nut with the hyphen.")
    while True:
        allergies = input("Type here: ")
        allergies = allergies.lower()
        list_of_allergies = ["alcohol", "celery", "crustacean",
                             "dairy", "egg", "fish", "fodmap",
                             "gluten", "mollusk", "mustard",
                             "peanut", "pork", "red-meat",
                             "seasame", "shellfish", "soy",
                             "sulfite", "tree-nut", "wheat"]
        if allergies == "":
            return ""
        elif allergies == "vegan" or allergies == "vegetarian":
            formatted_allergies = f"&health={allergies}"
            return formatted_allergies
        elif allergies in list_of_allergies:
            formatted_allergies = f"&health={allergies}-free"
            return formatted_allergies
        again_message = ("\nSorry I don't recognise your answer, "
                         + f"would you like to see the allergen list? (yes/no): ")
        try_again = input(again_message)
        if try_again == "yes":
            for allergen in list_of_allergies:
                print(allergen.title())
            print("You can always press enter to skip this question")
        elif try_again == "no":
            print("\nYou can always press enter to skip this question\n")
        else:
            print("\nSorry, I don't recongise your answer, let's try again.\n")


def find_meal_type():
    """
    Function to allow user to enter what type of meal the recipe
    searcher returns
    """
    print("\nThis is an optional field, to skip this question press enter")
    while True:
        meal_message = ("What type of meal would you like to make?\n"
                        + "Breakfast\nLunch\nDinner\nSnack\nTeatime\n"
                        + "Type here: ")
        meal_type = input(meal_message)
        meal_type = meal_type.title()
        list_of_meal_types = ["Breakfast",
                              "Lunch",
                              "Dinner",
                              "Snack",
                              "Teatime"]
        if meal_type == "":
            return ""
        elif meal_type == "Tea Time":
            meal_type = "Teatime"
            return "&mealType=" + meal_type
        elif meal_type in list_of_meal_types:
            return "&mealType="+meal_type
        else:
            print("\nOops, I didn't quite understand that. Let's try again")


def time_constraints():
    """
    Function to allow user to specify any time constraints
    """
    print("\nHow many minutes are you willing to spend making the recipe?")
    while True:
        time_message = ("If you have no time constraints then please enter "
                        + "0 to skip this question: ")
        try:
            max_total_time = int(input(time_message))
            if max_total_time == 0:
                return ""
            elif not max_total_time == 0:
                return f"&time=1-{max_total_time}"
        except ValueError:
            print("Oops, please enter a valid integer")


def cuisine_type():
    """
    Function to allow user to enter cusine type and format
    ready for API call
    """
    while True:
        type_message = ("\nWould you like to specify what type of cuisine "
                        + "the recipes are? E.g. Italian, French etc. (yes/no)"
                        + "\nType here: ")
        yes_or_no = input(type_message)
        yes_or_no = yes_or_no.lower()
        list_of_cuisines = ["American", "Asian", "British",
                            "Caribbean", "Central Europe", "Chinese",
                            "Eastern Europe", "French", "Indian",
                            "Italian", "Japanese", "Kosher",
                            "Mediterranean", "Mexican", "Middle Eastern",
                            "Nordic", "South American", "South East Asian"]
        if yes_or_no == "yes":
            print("\nHere's all the different cuisines available to search:")
            for dish in list_of_cuisines:
                print(dish)
            while True:
                cuisine = input("Which cuisine would you like to search?\n"
                                + "Type here: ")
                cuisine = cuisine.title()
                if cuisine in list_of_cuisines:
                    return f"&cuisineType={cuisine}"
                elif cuisine == "":
                    return ""
                else:
                    print("Oops, I didn't quite get that, let's try again.")
                    print("If you want to skip this question press enter.")
        elif yes_or_no == "no":
            return ""
        else:
            print("\nOops, was there a spelling error? Let's try again")


def calorie_range():
    """
    Function to check if user wants to specify calories.
    If specified, results will show calorie content
    """
    while True:
        calorie_message = ("\nWould you like to specifiy the maximum calorie"
                           + " content? (yes/no): ")
        calories = input(calorie_message)
        calories = calories.lower()
        if calories == "no":
            calorie_range = ""
            return calorie_range
        elif calories == "yes":
            while True:
                limit_message = ("What is the maximum calorie content "
                                 + "you would like to search?: ")
                calorie_limit = input(limit_message)
                try:
                    calorie_range = int(calorie_limit)
                    calorie_range = f"&calories=0-{calorie_limit}"
                    return calorie_range
                except ValueError:
                    print("Oops that didn't work, please enter an integer")
        print("Oops, I don't recognise your answer. Maybe something was "
              + "spelled incorrectly, let's try again")


def collect_data_with_kcals(recipes):
    """
    Collecting API results with kcals into a list
    to easily add to a save file
    """
    data = []
    for item in recipes:
        recipe_calories = item['recipe']['calories']
        recipe_yield = item['recipe']['yield']
        data.append(f"Recipe Name: {item['recipe']['label']}")
        data.append(f"Total calorie content: \
                    {round(recipe_calories, 2)} kcals")
        data.append("Calorie content per portion: "
                    + f"{round((recipe_calories / recipe_yield), 2)} kcals")
        data.append('List of Ingredients:')
        for ingredient in (item['recipe']['ingredientLines']):
            data.append(ingredient)
        data.append(f"Link to Full Recipe: {item['recipe']['url']}\n")
        data.append("\n")
    return data


def collect_data_with_kcals_and_time(recipes):
    """
    Collecting API results with kcals into a list
    to easily add to a save file
    """
    data = []
    for item in recipes:
        recipe_calories = item['recipe']['calories']
        recipe_yield = item['recipe']['yield']
        data.append(f"Recipe Name: {item['recipe']['label']}")
        data.append("Total calorie content: "
                    + f"{round(recipe_calories, 2)} kcals")
        data.append("Calorie content per portion: "
                    + f"{round((recipe_calories / recipe_yield), 2)} kcals")
        data.append('List of Ingredients:')
        for ingredient in (item['recipe']['ingredientLines']):
            data.append(ingredient)
        data.append(f"Link to Full Recipe: {item['recipe']['url']}\n")
        data.append("Total Time to Make: "
                    + f"{item['recipe']['totalTime']} minutes")
        data.append("\n")
    return data


def collect_data_without_kcals(recipes):
    """
    Collecting API results without kcals into a list
    to easily add to a save file
    """
    data = []
    for item in recipes:
        data.append(f"Recipe Name: {item['recipe']['label']}")
        data.append('List of Ingredients:')
        for ingredient in (item['recipe']['ingredientLines']):
            data.append(ingredient)
        data.append(f"Link to Full Recipe: {item['recipe']['url']}")
        data.append("\n")
    return data


def collect_data_without_kcals_with_time(recipes):
    """
    Collecting API results without kcals into a list
    to easily add to a save file
    """
    data = []
    for item in recipes:
        data.append(f"Recipe Name: {item['recipe']['label']}")
        data.append('List of Ingredients:')
        for ingredient in (item['recipe']['ingredientLines']):
            data.append(ingredient)
        data.append(f"Link to Full Recipe: {item['recipe']['url']}")
        data.append("Total Time to Make: "
                    + f"{item['recipe']['totalTime']} minutes")
        data.append("\n")
    return data
