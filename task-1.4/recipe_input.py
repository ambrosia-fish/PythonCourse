import pickle
filename = input("Enter the filename where your recipes are stored: ")

def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = 'Easy'
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = 'Medium'
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = 'Intermediate'
    else:
        difficulty = 'Hard'
    return difficulty

def take_recipe():
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter cooking time (in minutes): "))
    ingredients = []
   
    n = int(input("How many ingredients are there? "))
    for i in range(n):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient)
   
    difficulty = calc_difficulty(cooking_time, ingredients)
   
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }
   
    return recipe

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
except:  
    print("An error occurred while reading the file.")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
else:
    file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

number_of_recipes = int(input("How Many Recipes would you like to add? "))
for i in range(number_of_recipes):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:  
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)
   
    print("\nRecipe:", recipe['name'])
    print("Cooking Time:", recipe['cooking_time'])
    print("Ingredients:", recipe['ingredients'])
    print("Difficulty:", recipe['difficulty'])

data = {
    'recipes_list': recipes_list,
    'all_ingredients': all_ingredients
}

with open(filename, 'wb') as file:
    pickle.dump(data, file)

# Added this code so we can test if it works by printing out all recipe_list data
print("\nPrinting file contents:")
with open(filename, 'rb') as file:
    saved_data = pickle.load(file)

print("\nAll Recipes:")
for recipe in saved_data['recipes_list']:
    print("\nName:", recipe['name'])
    print("Cooking Time:", recipe['cooking_time'])
    print("Ingredients:", recipe['ingredients'])
    print("Difficulty:", recipe['difficulty'])

print("\nAll Ingredients:", saved_data['all_ingredients'])