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

Base.metadata.create_all(engine)