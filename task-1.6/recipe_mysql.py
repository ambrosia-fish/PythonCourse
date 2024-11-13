import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'cf-python',
    password = 'password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute("""CREATE TABLE IF NOT EXISTS Recipes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
    )
""")

def calculate_difficulty(cooking_time, num_ingredients):
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"
    return difficulty

def create_recipe():
    name = input("What is the name of the recipe? ")
    cooking_time = int(input("How long (in minutes) will this recipe take? "))
    ingredients = []
    difficulty = ""

    n = int(input("How many ingredients are there? "))
    for i in range(n):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient)

    ingredients_str = ", ".join(ingredients)

    difficulty = calculate_difficulty(cooking_time, len(ingredients))

    cursor.execute('INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)', 
    (name, ingredients_str, cooking_time, difficulty))

    conn.commit()

def search_recipe():
    searched_ingredient = input("What ingredient are you searching for? ")
    
    cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", (f'%{searched_ingredient}%',))

    found_recipes = cursor.fetchall()

    for recipe in found_recipes:
        print("==========================")
        print("ID:", recipe[0])
        print("Recipe:", recipe[1])
        print("Ingredients:", recipe[2])
        print("Cooking Time:", recipe[3], "minutes")
        print("Difficulty:", recipe[4])
    
    return

def update_recipe():
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    
    print("Recipe Book:")
    for recipe in results:
        print("==========================")
        print("ID:", recipe[0])
        print("Recipe:", recipe[1])
        print("Ingredients:", recipe[2])
        print("Cooking Time:", recipe[3], "minutes")
        print("Difficulty:", recipe[4])
    
    recipe_id = input("Provide the ID number of the recipe you would like to update: ")

    print("What would you like to update?")
    print("1. Name")
    print("2. Cooking Time")
    print("3. Ingredients")
    print()
    
    choice = int(input("Your choice: "))

    if choice == 1:
        new_name = input("Enter new name: ")
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, recipe_id))
    elif choice == 2:
        new_cooking_time = int(input("What is the new cooking time (in minutes)? "))
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_cooking_time, recipe_id))
    elif choice == 3: 
        ingredients = []

        n = int(input("How many ingredients are there? "))

        for i in range(n):
            ingredient = input(f"Enter ingredient {i+1}: ")
            ingredients.append(ingredient)
        new_ingredients = ", ".join(ingredients)

        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_ingredients, recipe_id))

    if choice in [2, 3]:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        result = cursor.fetchone()
        cooking_time = result[0]
        ingredients = result[1].split(", ")
        
        new_difficulty = calculate_difficulty(cooking_time, len(ingredients))
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))

    conn.commit()
    print("Recipe updated!")

def delete_recipe():
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    
    print("Recipe Book:")
    for recipe in results:
        print("==========================")
        print("ID:", recipe[0])
        print("Recipe:", recipe[1])
        print("Ingredients:", recipe[2])
        print("Cooking Time:", recipe[3], "minutes")
        print("Difficulty:", recipe[4])
    
    recipe_id = input("Enter the ID of the recipe you want to delete: ")
    
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
    conn.commit()
    
    print("Recipe successfully deleted!")
            
def main_menu():
    choice = ''

    while(choice != 'quit'):
        print("Welcome to Josef's recipe book! Pick an option below!")
        print("1. Create new recipe.")
        print("2. Search recipe book.")
        print("3. Update recipe.")
        print("4. Delete recipe")
        print("Type 'quit to close the program.")

        choice = input("Your choice: ")

        if choice == '1':
            create_recipe()
        elif choice =='2':
            search_recipe()
        elif choice == '3':
            update_recipe()
        elif choice == '4':
            delete_recipe()

if __name__ == "__main__":
    main_menu()
