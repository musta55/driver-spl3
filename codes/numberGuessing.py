class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return "Woof!"

    def greet(self):
        return f"Hello, I'm {self.name} and I'm {self.age} years old."


# Creating instances (objects) of the Dog class
dog1 = Dog("Buddy", 3)
dog2 = Dog("Charlie", 5)

# Accessing object attributes and methods
print(dog1.name)        # Output: Buddy
print(dog2.age)         # Output: 5

print(dog1.bark())      # Output: Woof!
print(dog2.greet())     # Output: Hello, I'm Charlie and I'm 5 years old.
