import pickle
filename = input("Enter the filename where your recipes are stored: ")

def display_recipe(recipe):
    print("\nRecipe:", recipe['name'])
    print("Cooking Time:", recipe['cooking_time'])
    print("Ingredients:", recipe['ingredients'])
    print("Difficulty:", recipe['difficulty'])


def search_ingredient(data):
    print("All avialable ingredients: ")
    for index, ingredient in enumerate(data['all_ingredients']):
        print(str(index) + ". " + ingredient)
    
    try:
        ingredient_idx = int(input("\nEnter the number of the ingredient you want to search: "))
        ingredient_searched = data['all_ingredients'][ingredient_idx]
    except:
        print("Invalid. Enter a number from the list")
        return
    else:
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        print(data)
except FileNotFoundError:
    print("File not found")
except:
    print("An error occurred attempting to read this file")
else:
    search_ingredient(data)