# imports
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker


# engine / base creation
engine = create_engine("mysql://cf-python:password@localhost/task_database")
Base = declarative_base()

# session creation
Session = sessionmaker(bind=engine)
session = Session()

# create Recipe class
class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # def return elements
    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + "-" + self.difficulty + ">"
    
    def __str__(self):
        return (f"Recipe ID: {self.id}\n"
                f"Recipe Name: {self.name}\n"
                f"Ingredients: {self.ingredients}\n"
                f"Cooking Time: {self.cooking_time}\n"
                f"Difficulty: {self.difficulty}")

    # def calculate difficulty            
    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients.split(', '))
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"
    
    # return ingredients as list
    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        return self.ingredients.split(", ")

# create table
Base.metadata.create_all(engine)

# create recipe object from user inputs
def create_recipe():
    name = get_valid_recipe_name()
    cooking_time = get_valid_cooking_time()
    ingredients = []
    difficulty = ""

    n = get_valid_num_ingredients()
    for i in range(n):
        ingredient = get_valid_ingredient_name(f"Enter ingredient {i+1}: ") 
        ingredients.append(ingredient)
    
    # convert ingredient list into str:
    ingredients_str = ", ".join(ingredients)

    recipe_entry = Recipe(
        name=name,
        cooking_time=cooking_time,
        ingredients=ingredients_str
    )

    recipe_entry.calculate_difficulty()

     # add recipe to database
    session.add(recipe_entry)
    session.commit()


# user input functions that request and valid user input for the various variables.
def get_valid_recipe_name():
    while True:
        name = input("What is the title of the recipe? ")
        if len(name.strip()) == 0:
            print("Recipe title cannot be empty.")
            continue
        if len(name.strip()) > 50:
            print("Recipe title must be 50 characters or less.")
            continue
        if not name.replace(" ", "").isalnum():
            print("Recipe name can only contain letters, numbers and spaces.")
            continue
        return name
    
def get_valid_cooking_time():
    while True:
        cooking_time = input("How long is the cooking time, in minutes? ")
        if not cooking_time.isnumeric() or int(cooking_time) <= 0:
            print("Cooking time needs to be a positive integer")
            continue
        return int(cooking_time)
    
def get_valid_num_ingredients():
    while True:
        num_ingredients = input("How many ingredients would you like to add to the recipe? ")
        if not num_ingredients.isnumeric() or int(num_ingredients) <= 0:
            print("Number of ingredients need to be a positive integer.")
            continue
        return int(num_ingredients)
    
def get_valid_ingredient_name(prompt):
    while True:
        ingredient = input(prompt)
        if len(ingredient.strip()) == 0:
            print("Ingredient name cannot be empty.")
            continue
        if not ingredient.replace(" ", "").replace("-", "").isalpha():
            print("Ingredient name should contain only letters, spaces, and/or hyphens.")
            continue
        return ingredient

# view_all_recipes function
def view_all_recipes():
    recipes = session.query(Recipe).all()
    
    if not recipes:
        print("No recipes found.")
        return None
        
    for recipe in recipes:
        print(recipe)
        print("-" * 50) 


def search_recipe():
    count = session.query(Recipe).count()
    if count == 0:
        print("No recipes found.")
        return None
    
    # Get all unique ingredients
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    
    # Split ingredients and add to list if not already present
    for recipe_ingredients in results:
        ingredients_list = recipe_ingredients[0].split(", ")
        for ingredient in ingredients_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    
    for i in range(len(all_ingredients)):
        print(f"{i+1}. {all_ingredients[i]}")

    search_input = input("Enter the number of the ingredients you'd like to search for (separated by spaces): ")
    search_numbers = search_input.split()

    # Validate user inputs
    for num in search_numbers:
        if not num.isnumeric() or int(num) < 1 or int(num) > len(all_ingredients):
            print("Invalid input. Numbers must correspond to the ingredient list.")
            return None

    # for ea
    search_ingredients = [all_ingredients[int(num)-1] for num in search_numbers]
    conditions = []

    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))
    
    results = session.query(Recipe).filter(*conditions).all()

    if not results:
        print("No recipes found with those ingredients.")
        return None

    for recipe in results:
        print(recipe)
        print("-" * 50)

def edit_recipe():
    count = session.query(Recipe).count()
    if count == 0:
        print("No recipes found.")
        return None
    
    results = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, recipe_name in results:
        print(f"{recipe_id}. {recipe_name}")
    
    recipe_id = input("\nEnter recipe ID to edit: ")
    if not recipe_id.isnumeric() or not any(str(id) == recipe_id for id, name in results):
        print("Invalid recipe ID")
        return None

    print("\n1. Name\n2. Ingredients\n3. Cooking Time")
    attribute = input("Enter number of attribute to edit: ")

    if attribute == "1":
        new_name = get_valid_recipe_name()
        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.name: new_name})
    elif attribute == "2":
        ingredients = []
        n = get_valid_num_ingredients()
        for i in range(n):
            ingredients.append(get_valid_ingredient_name(f"Enter ingredient {i+1}: "))
        new_ingredients = ", ".join(ingredients)
        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.ingredients: new_ingredients})
    elif attribute == "3":
        new_time = get_valid_cooking_time()
        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.cooking_time: new_time})
    else:
        print("Invalid attribute number")
        return None


    recipe = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    recipe.calculate_difficulty()
    session.commit()

def delete_recipe():
    count = session.query(Recipe).count()
    if count == 0:
        print("No recipes found.")
        return None
    
    results = session.query(Recipe.id, Recipe.name).all()
    print("List of Recipes:")
    for recipe_id, recipe_name in results:
        print(f"{recipe_id}. {recipe_name}")
    
    recipe_id = input("\nEnter the ID of the recipe you’d like to delete: ")
    
    if not recipe_id.isnumeric() or not any(str(id) == recipe_id for id, name in results):
        print("Invalid recipe ID. Please enter a valid ID from the list.")
        return None
    
    recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    
    confirmation = input(f"Are you sure you want to delete the recipe '{recipe_to_delete.name}' (ID: {recipe_to_delete.id})? (yes/no): ").strip().lower()
    
    if confirmation == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print(f"Recipe '{recipe_to_delete.name}' has been deleted successfully.")
    else:
        print("Recipe deletion canceled.")

def main():
    while True:
        choice = input("\n1. Create Recipe\n2. View All Recipes\n3. Search Recipes\n4. Edit Recipe\n5. Delete Recipe\n6. Exit\nYour choice: ")
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_recipe()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "6":
            break

if __name__ == "__main__":
    main()