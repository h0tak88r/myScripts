# Strings
#Print string
print("Hello, world!")
print('Hello, world!')
print("""This string runs
multiple lines!""")
print("This string is "+"awesome!") #we can also concatenate
print('\n') #new line 
print('Test that new line out.')
#ADVANCED STRINGS
my_name = "Heath"
print(my_name[0]) #first letter
print(my_name[-1]) #last letter
sentence = "This is a sentence."
print(sentence[:4])
print(sentence.split()) #delimeter - default is a space
sentence_split = sentence.split()
sentence_join = ' '.join(sentence_split)
print(sentence_join)
quote = "He said, 'give me all your money'"  #show example
quote = "He said, \"give me all your money\""
print(quote)
too_much_space = "                       hello          "
print(too_much_space.strip())
print("A" in "Apple") #returns true
print("a" in "Apple") #returns false - case sensitive
letter = "A"
word = "Apple"
print(letter.lower() in word.lower()) #improved
movie = "The Hangover"
print("My favorite movie is {}.".format(movie))
print("My favorite movie is %s" % movie)
print(f"My favorite movie is {movie}")
-------------------------------------------------------------
#Math
print(50 + 50) #add
print(50 - 50) #subtract
print(50 * 50) #multiply
print(50 / 50) #divide
print(50 + 50 - 50 * 50 / 50) #PEMDAS
print(50 ** 2) #exponents
print(50 % 6) #modulo - takes what is left over
print(50 / 6) #division with decimals
print(50 // 6) #no remainder
---------------------------------------------------------------
#Variables and Methods
quote = "All is fair in love and war."
print(quote)
print(quote.upper()) #uppercase
print(quote.lower()) #lowercase
print(quote.title()) #title case
print(len(quote)) #counts characters
name = "Heath" #string
age = 33 #int
gpa = 3.7 #float - has a decimal
print(int(age))
print(int(30.1))
print(int(30.9)) - Will it round? No!
print("My name is " + name + " and I am " + str(age) + " years old.")
age +=1
print(age)
birthday = 1
age += birthday
print(age)
-----------------------------------------------------------------------
#Boolean expressions (True or False)
print("Boolean expressions:")
bool1 = True
bool2 = 3*3 == 9
bool3 = False
bool4 = 3*3 != 9
print(bool1,bool2,bool3,bool4)
print(type(bool1))
bool5 = "True"
print(type(bool5))
nl()
#Relational and Boolean operators
greater_than = 7 > 5
less_than = 5 < 7
greater_than_equal_to = 7 >=7
less_than_equal_to = 7 <= 7
test_and = True and True #True
test_and2 = True and False #False
test_or = True or True #True
test_or2 = True or False #True
test_not = not True #False
----------------------------------------------------------------------
#USER INPUT
x = float(input("Give me a number: "))
o = input("Give me an operator: ")
y = float(input("Give me yet another number: "))
if o == "+":
	print(x + y)
elif o == "-":
	print(x - y)
elif o == "/":
	print(x / y)
elif o == "*":
	print(x * y)
elif o == "**":
	print(x ** y)
else:
	print("Unknown operator.")
------------------------------------------------------------------
#Conditional Statements
def drink(money):
	if money >= 2:
		return "You've got yourself a drink!"
	else:
		return "No drink for you!"
print(drink(3))
print(drink(1))
def alcohol(age,money):
	if(age >= 21) and (money >= 5):
		return "We're getting a drink!"
	elif (age >= 21) and (money < 5):
		return "Come back with more money."
	elif (age < 21) and (money >= 5):
		return "Nice try, kid!"
	else:
		return "You're too poor and too young!"
print(alcohol(21,5))
print(alcohol(21,4))
print(alcohol(20,5))
print(alcohol(20,4))
-----------------------------------------------
#Tuples - Do not change, ()
grades = ("a", "b", "c", "d", "f")
grades.pop, grades.append won't work - not mutable
print(grades[1])
-------------------------------------------------
#For loops - start to finish of an iterate
vegetables = ["cucumber", "spinach", "cabbage"]
for x in vegetables:
	print(x)	
#While loops - execute as long as true
i = 1
while i < 10:
	print(i)
	i += 1
--------------------------------------------------
#Functions
print("Here is an example function:")
def who_am_i(): #this is a function without parameters
	name = "Heath"
	age = 30 #local variable
	print("My name is " + name + " and I am " + str(age) + " years old.")
who_am_i()
#adding parameters
def add_one_hundred(num):
	print(num + 100)
add_one_hundred(100)
#multiple parameters
def add(x,y):
	print(x + y)
add(7,7)
def multiply(x,y):
	return x * y
multiply(7,7)
print(multiply(7,7))
]
	print(x ** .5)
    klsquare_root(64)
def nl():
	print('\n')	
nl()
--------------------------------------------------------------
#DICTIONARIES - key/value pairs {}
drinks = {"White Russian": 7, "Old Fashion": 10, "Lemon Drop": 8} #drink is key, price is value
print(drinks)
employees = {"Finance": ["Bob", "Linda", "Tina"], "IT": ["Gene", "Louise", "Teddy"], "HR": ["Jimmy Jr.", "Mort"]}
employees['Legal'] = ["Mr. Frond"] #adds new key:value pair
print(employees)
employees.update({"Sales": ["Andie", "Ollie"]}) #adds new key:value pair
print(employees)
drinks['White Russian'] = 8
print(drinks)
print(drinks.get("White Russian"))
-----------------------------------------------------------------------------------
# Classes and Objects
class Employees:

	def __init__(self, name, department, role, salary, years_employed):
		self.name = name
		self.department = department
		self.role = role
		self.salary = salary
		self.years_employed = years_employed
		
	def eligible_for_retirement(self):
		if self.years_employed >= 20:
			return True
		else:
			return False
------------------------------
from Employees import Employees

e1 = Employees("Bob", "Sales", "Director of Sales", 100000, 20)
e2 = Employees("Linda", "Executive", "CIO", 150000, 10)

print(e1.name)
print(e2.role)
print(e1.eligible_for_retirement())
----------------------------------------------
# Create objects of the Dog class
dog1 = Dog("Buddy", 5)
dog2 = Dog("Max", 3)


# Call methods on the objects
dog1.bark()               # Output: "Woof!"
dog1.display_info()       # Output: "Name: Buddy", "Age: 5"


dog2.bark()               # Output: "Woof!"
dog2.display_info()       # Output: "Name: Max", "Age: 3"
---------------------------------------------------------------------------
#SOCKETS - Sockets can be used to connect two nodes together.  

#!/bin/python3
import socket
HOST = '127.0.0.1'
PORT = 7777
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #af_inet is ipv4, sock stream is a port
s.connect((HOST,PORT))
--------------------------------------------------------------------------------------------
# Open/Read a File
with open("example.txt", "r") as file:
    content = file.read()
    print(content)