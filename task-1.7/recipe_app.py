# imports
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
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
                f"Cooking Time: {self.cooking_time}")

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
        ingredient = get_valid_ingredient_name() 
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
    
def get_valid_ingredient_name():
    while True:
        ingredient = input(f"Enter ingredient {i+1}: ")
        if len(ingredient.strip()) == 0:
            print("Ingredient name cannot be empty.")
            continue
        if not ingredient.replace(" ", "").replace("-", "").isalpha():
            print("Ingredient name should contain only letters, spaces, and/or hyphens.")
            continue
        return ingredient