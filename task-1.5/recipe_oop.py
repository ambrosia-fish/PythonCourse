class Recipe(object):
   all_ingredients = []
   def __init__(self, name):
      
       self.name = name
       self.cooking_time = 0    
       self.ingredients = []
       self.difficulty = None
    
    def calculate_difficulty(self):
    if self.cooking_time < 10 and len(self.ingredients) < 4:
        return "Easy"
    elif self.cooking_time < 10 and len(self.ingredients) >= 4:
        return "Medium"
    elif self.cooking_time >= 10 and len(self.ingredients) < 4:
        return "Intermediate"
    else:
        return "Hard"
  
   def set_name(self, name):
       self.name = name
  
   def get_name(self):
       return self.name
  
   def set_cooking_time(self, cooking_time):
       self.cooking_time = cooking_time
       self.difficulty = self.calculate_difficulty()
       
   def get_cooking_time(self):
       return self.cooking_time
       

  
   def get_difficulty(self):
    if self.difficulty is None:
        self.difficulty = self.calculate_difficulty()
    return self.difficulty
  
   def add_ingredients(self, *new_ingredients):
       for ingredient in new_ingredients:
           self.ingredients.append(ingredient)
       self.difficulty = self.calculate_difficulty()
       self.update_all_ingredients()
  
   def get_ingredients(self):
       return self.ingredients
  
   def search_ingredient(self, ingredient):
       return ingredient in self.ingredients
  
   def update_all_ingredients(self):
       for ingredient in self.ingredients:
           if ingredient not in Recipe.all_ingredients:
               Recipe.all_ingredients.append(ingredient)
  
   def __str__(self):
       output = "\n" + "=" * 40 + "\n"
       output += f"Recipe: {self.name}\n"
       output += f"Cooking Time (min): {self.cooking_time}\n"
       output += f"Difficulty: {self.difficulty}\n"
       output += f"Ingredients:\n"
       for ingredient in self.ingredients:
           output += f"- {ingredient}\n"
       output += "=" * 40
       return output

def recipe_search(data, search_term):
   for recipe in data:
       if recipe.search_ingredient(search_term):
           print(recipe)

tea = Recipe("Tea")
tea.set_cooking_time(5)
tea.add_ingredients("Tea Leaves", "Water", "Milk", "Sugar")

coffee = Recipe("Coffee")
coffee.set_cooking_time(5)
coffee.add_ingredients("Coffee Beans", "Water", "Milk", "Sugar")

cake = Recipe("Cake")
cake.set_cooking_time(50)
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.set_cooking_time(5)
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")

recipe_list = [tea, coffee, cake, banana_smoothie]

print("Recipes containing Water:")
recipe_search(recipe_list, "Water")

print("\nRecipes containing Sugar:")
recipe_search(recipe_list, "Sugar")

print("\nRecipes containing Bananas:")
recipe_search(recipe_list, "Bananas")