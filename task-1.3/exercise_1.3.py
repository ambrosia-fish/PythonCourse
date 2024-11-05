recipes_list = []
ingredients_list = []
number_of_recipes = int(input("How Many Recipes would you like to add? "))

def take_recipe():
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter cooking time (in minutes): "))
    ingredients = []
   
    n = int(input("How many ingredients are there? "))
    for i in range(n):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient)
    
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    return recipe

for i in range(number_of_recipes):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    else:
        recipe['difficulty'] = 'Hard'
    print("Recipe: " + recipe['name'])
    print("Cooking Time: " + str(recipe['cooking_time']))
    print("Difficulty Level: " + recipe['difficulty'])
    print("Ingredients: ")
    for ingredient in recipe['ingredients']:
        print(ingredient)

print("Ingredients across all recipes:")
print("-------------------------------")
for ingredient in sorted(ingredients_list):
    print(ingredient)