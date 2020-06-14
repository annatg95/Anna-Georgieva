

# Define the Class 'veryBigsnake'

class veryBigSnake:

   # constructor
   def __init__(self, name = "Peter Python",type = "python"):
      # initialise properties
      self.name = name
      self.type = type
      print "New snake in da house!"
	  
   # function to set name
   def set_snake_name(self, name):
      self.name = name
	  
   # function to set type
   def set_snake_type(self, type):
      self.type = type
	  
   # function to log name and type
   def who_am_i(self):
      print "my name is " + self.name + ", I'm a " + self.type + " and I'm perfect for you! Take me home today!"
	  
   # destructor
   def __del__(self):
      print "Just killed the snake named " + self.name + ", who was a " + self.type + " ... Ouch!"
	  
# create a new class named evenBiggerSnake that inherits from the 'base' class veryBigSnake

class evenBiggerSnake(veryBigSnake):

   # constructor
   # accepts name, age and type as arguments
   def __init__(self,name="Paula Python", type = "python", age= "2"):
      self.name = name
      self.age = age
      self.type = type
      print "The World welcomes a new, improved snake"

   # defining a new who_am_i function for this derived class
   def who_am_i(self):
      print "My name is " + self.name + ", I'm a " + self.type + " and I'm " + self.age + " years old"
   
# the type function allows us to tell whether something is a class or an instance

alpha = veryBigSnake("Steve Smoothy","smooth snake")
beta = evenBiggerSnake("Steve Serpent","giant mythical serpent","very old")

del alpha
del beta

# and that concludes the overview of defining classes in Python
# Thanks to the the author of the originals, icarus!



