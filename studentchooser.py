from random import random
from sys import exit

# change this value to adjust by how much a student's prob changes when picked
prob_change = 3.0/4.0

def ask():
	return raw_input("> ")

def pick_kid():
	value = random() * 100
	startpoint = 0
	endpoint = 0
	
	for kid in present_students:
		endpoint += present_students[kid].prob
		#print "(%f, %f)" % (startpoint, endpoint)
		if (startpoint <= value <= endpoint):
			chosen = kid
			present_students[kid].picked += 1
			break
		else:
			startpoint += present_students[kid].prob

	return chosen

def scale():
	# set all prob's back to scale to 100
	for kid in roster:
		roster[kid].prob = 100 * prob_change ** (roster[kid].picked)
		# print roster[kid].name, roster[kid].prob
	# for all kids who are present, adjust prob. by # of times picked, then scale
	total = 0
	for kid in present_students:
			total += present_students[kid].prob
	for kid in present_students:
			present_students[kid].prob *= 100.0 / total

def take_attendance():
	present_kids = {}
	for kid in roster:
		if not(roster[kid].absent):
			present_kids[kid] = roster[kid]
	return present_kids

def select():
	the_student = pick_kid()
	scale()
	print the_student
	print roster
	print "----------"
	return the_student

# TESTING FUNCTIONS
def test_always(kid):
	for i in range(0,10000):
		the_student = select()
		if the_student == kid:
			print "PANIC!"
			break

def test_never(kid):
	for i in range(0,10000):
		the_student = select()
		print i
		if the_student == kid:
			print "PANIC!"
			break

def multi_test(x):
	for i in range(0,x):
		print "%d: %s" % (i, select())
		#print roster
		#print "-----------"

# make a debug function that will display all of the prob's

# how do i change how a Student object prints?
class Student(object):
	def __init__(self, name):
		self.name = name
		self.absent = False
		self.prob = 1
		self.picked = 0
	def __repr__(self):
		return "<%s, %f, absent = %d>" % (self.name, self.prob, self.absent)
	def __str__(self):
		return "<%s, %f, absent = %d>" % (self.name, self.prob, self.absent)

# list of students (later, will get this from user input)
students = ["ali", "ben", "chuck", "dave"]
#, "erin", "samer", "eric", "merlin", "arthur", "rachel", "carlos", "sindhu"]

# make an empty dict.
roster = {}
present_students = {}

# populate that dict. with all students equally weighted
for kid in students:
	roster[kid] = Student(kid)

# make a list of students who are present
present_students = take_attendance()

# scale the probabilities of the present students
scale()

# for debugging
print "Roster:", roster
print "Present:", present_students

while True:
	print "1. pick, 2. input absences, 3. exit"
	answer = ask()
	if answer == "1":
		select()
	elif answer == "2":
		print "You picked #2!"
	elif answer == "3":
		exit()
	else:
		print "Sorry, I didn't get that. Try again."	



# some way to save the state

# some way to input absence

# some way to check if student is absent

# notification of who is absent

