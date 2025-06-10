#example 1
# class Dog:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def call_dog(self):
#         print(f"Come here, {self.name}!")

#     def speak(self):
#         print("bark bark bark")

# dog1 = Dog("Spot", 2)
# dog1.call_dog()
# dog1.speak()
# print(f"dog1's name is {dog1.name}.")

# dog2 = Dog("Wally", 4)
# dog2.call_dog()
# dog2.age += 1
# print(dog2.age)

class Dog:
    _count = 0  

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Dog._count += 1 

    def call_dog(self):
        print(f"Come here, {self.name}!")

    def speak(self):
        print("bark bark bark")

    @classmethod
    def get_dog_count(cls):
        return cls._count

# Create a couple of dogs
dog1 = Dog("Spot", 2)
dog1.call_dog()
dog1.speak()
print(f"dog1's name is {dog1.name}.")

dog2 = Dog("Wally", 4)
dog2.call_dog()
dog2.age += 1
print(f"dog2's new age: {dog2.age}")

print(f"Total dogs created: {Dog.get_dog_count()}")  

class BigDog(Dog): # inherits from Dog
    def __init__(self, name, age): 
        # Call the parent class's __init__ to set name/age
        super().__init__(name, age) 

    def fetch(self):
        print("Got it.")

    def speak(self):
        print("Woof Woof Woof") # overrides Dog.speak()

    def speak_verbose(self):
        # call Dog.speak(), then BigDog.speak()
        super().speak()
        self.speak()

dog3 = BigDog("Butch", 3)
dog3.call_dog()
dog3.speak()
dog3.speak_verbose()

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14 * self.radius ** 2

    @property
    def diameter(self):
        return 2 * self.radius
c = Circle(3)
print(c.area)    
print(c.diameter) 