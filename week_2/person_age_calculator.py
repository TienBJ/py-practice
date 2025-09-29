# # Example of encapsulation in Python

# class BankAccount:
#     def __init__(self, owner, balance):
#         self.owner = owner
#         self.__balance = balance

#     @property
#     def balance(self):
#         return self.__balance
    
#     @balance.setter
#     def balance(self, amount):
#         if amount >= 0:
#             self.__balance = amount
#         else:
#             print("Invalid balance. Balance must be positive.")


# acct = BankAccount("Tien", 1000)
# print(acct.balance)
# acct.balance = 2000
# print(acct.balance)
# acct.balance = -500  # This should trigger the validation message

# Example of inheritance in Python

# class Animal:
#     def __init__(self, name):
#         self.name = name
        
#     def speak(self):
#         return "Some sound"
    

# class Dog(Animal):
#     def speak(self):
#         return "Woof!"
    
# class Cat(Animal):
#     def speak(self):
#         return "Meow!"
    
# animals = [Dog("Buddy"), Cat("Whiskers")]
# for animal in animals:
#     print(f"{animal.name} says {animal.speak()}")

# Example of Abstraction in Python

# from abc import ABC, abstractmethod


# class Animal(ABC):
#     @abstractmethod 
#     def speak(self):
#         pass

# class Dog(Animal):
#     def speak(self):
#         return "Woof!"
    
# class Cat(Animal):
#     def speak(self):
#         return "Meow!"
    
    
# dog = Dog()
# print(dog.speak())
from datetime import datetime

class Person:
    def __init__(self, name, country, dob):
        self.name = name
        self.country = country
        self.dob = dob

    def calculate_age(self):
        current_year = datetime.now().year
        birth_year = int(self.dob.split('-')[2])
        return current_year - birth_year

person = Person("Tien", "Vietnam", "27-01-2003")
print(person.calculate_age())