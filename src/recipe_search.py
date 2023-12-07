from utils.api_connection import api_call
from utils.optional_choices import (
    allergy_checker,
    find_meal_type,
    time_constraints,
    cuisine_type,
    calorie_range,
    collect_data_with_kcals,
    collect_data_with_kcals_and_time,
    collect_data_without_kcals,
    collect_data_without_kcals_with_time
)


def search_again():
    """
    Function to check if user wants to do the search again
    """
    while True:
        go_again = input("\nWould you like to search again? (yes/no): ")
        go_again = go_again.lower()
        if go_again == "yes":
            return recipe_search()
        elif go_again == "no":
            print("Thanks for using our recipe searcher, hope you come "
                  + "back soon!")
            break
        print("Oops, something went wrong, let's try again")


def save_recipes(recipe_list):
    """
    Function to allow user to optionally save recipes.
    Saves the recipes into a .txt file
    """
    while True:
        save_message = ("\nWould you like to save your results in a file?"
                        + " (yes/no): ")
        save_recipe = input(save_message)
        save_recipe = save_recipe.lower()
        if save_recipe == "yes":
            print("\nWhat name would like to call your file?\nYou can always "
                  + "use the same file name to add to an existing file.")
            name = input("Type here: ")
            file = name.lower() + ".txt"
            with open(file, 'a', encoding="utf-8") as r_file:
                r_file.write("\n".join(recipe_list))
            print("We've now saved this for you. Happy cooking!")
            return search_again()
        elif save_recipe == "no":
            return search_again()
        print("Oops, I didn't quite get that. Let's try again "
              + "(please enter yes or no)")


def recipe_search():
    """
    Function to take all user input from the util optional choice
    functions, calls the API, and returns results
    """
    print("\nHere's a simple recipe searcher based on what ingredient you "
          + "want to use.")
    print("The ingredient is the only required part, but we have a few "
          + "optional questions to get you the best results!")
    print("After getting your results, you also have the option to save "
          + "your search to a file.")
    ingredient = input("What ingredient do you want to use?: ")
    allergy = allergy_checker()
    meal_type = find_meal_type()
    cuisine = cuisine_type()
    calories = calorie_range()
    time = time_constraints()
    try:
        recipes = api_call(ingredient,
                           meal_type,
                           allergy,
                           calories,
                           cuisine,
                           time)
        if recipes == []:
            print("\nSorry there are no recipes containing "
                  + "{} that fit your other criteria".format(ingredient))
            search_again()
        elif calories and time:
            data_for_saving = collect_data_with_kcals_and_time(recipes)
            for item in recipes:
                recipe_calories = item['recipe']['calories']
                recipe_yield = item['recipe']['yield']
                print('\n\nRecipe Name:', item['recipe']['label'])
                print('Total calorie content:',
                      round(recipe_calories, 2), 'kcals')
                print('Calorie content per portion:',
                      round((recipe_calories / recipe_yield), 2), 'kcals')
                print('List of Ingredients:')
                for ingredient in (item['recipe']['ingredientLines']):
                    print(ingredient)
                print('Link to Full Recipe:', item['recipe']['url'])
                print('Total Time to Make:',
                      item['recipe']['totalTime'],
                      'minutes')
            save_recipes(data_for_saving)
        elif calories and not time:
            data_for_saving = collect_data_with_kcals(recipes)
            for item in recipes:
                recipe_calories = item['recipe']['calories']
                recipe_yield = item['recipe']['yield']
                print('\n\nRecipe Name:', item['recipe']['label'])
                print('Total calorie content:',
                      round(recipe_calories, 2), 'kcals')
                print('Calorie content per portion:',
                      round((recipe_calories / recipe_yield), 2), 'kcals')
                print('List of Ingredients:')
                for ingredient in (item['recipe']['ingredientLines']):
                    print(ingredient)
                print('Link to Full Recipe:', item['recipe']['url'])
            save_recipes(data_for_saving)

        elif not calories and time:
            data = collect_data_without_kcals_with_time(recipes)
            for item in recipes:
                print('\nRecipe Name:', item['recipe']['label'])
                print('List of Ingredients:')
                for ingredient in (item['recipe']['ingredientLines']):
                    print(ingredient)
                print('Link to Full Recipe:', item['recipe']['url'])
                print('Total Time to Make:',
                      item['recipe']['totalTime'],
                      'minutes')
            save_recipes(data)

        elif not calories and not time:
            data = collect_data_without_kcals(recipes)
            for item in recipes:
                print('\nRecipe Name:', item['recipe']['label'])
                print('List of Ingredients:')
                for ingredient in (item['recipe']['ingredientLines']):
                    print(ingredient)
                print('Link to Full Recipe:', item['recipe']['url'])
            save_recipes(data)
    except Exception as e:
        print("Sorry, something went wrong! Maybe something was spelled "
              + "incorrectly or included more words. Let's try that again.")
        print("The error raised is:", e)
        search_again()


recipe_search()
