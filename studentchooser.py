from random import random
from sys import exit

### CONSTANTS ###
# change this value to adjust by how much a student's prob changes when picked
prob_change = 3.0/4.0

### CLASSES ###
class Student(object):
	def __init__(self, name):
		self.name = name
		self.absent = False
		self.prob = 1
		self.picked = 0
	def __repr__(self):
		return "<%s, %f, picked = %f, absent = %d>" % (self.name, self.prob, self.picked, self.absent)
	def __str__(self):
		return "<%s, %f, picked = %f, absent = %d>" % (self.name, self.prob, self.picked, self.absent)

### UTILITY FUNCTIONS ###
def ask():
	return raw_input("> ")

def confirm():
	while True:
		print "Is this correct? y/n"
		answer = ask()
		if answer == "y" or answer == "Y" or answer == "yes" or answer == "Yes" or answer == "YES":
			return True
		elif answer == "n" or answer == "N" or answer == "no" or answer == "No" or answer == "NO":
			return False
		else:
			print "Sorry, I didn't get that. Try again."

### FUNCTIONS ###
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

def get_present_students():
	present_kids = {}
	for kid in roster:
		if not(roster[kid].absent):
			present_kids[kid] = roster[kid]
	return present_kids

def mark_absent(abs_list):
	if abs_list:
		for kid in abs_list:
			if roster.get(kid):
				roster[kid].absent = True
			else:
				print "ERRROR! One or more of your names was not recognized. Please try again.\n"
				take_attendance()

def select():
	the_student = pick_kid()
	scale()
	print the_student
	print roster
	print "----------"
	return the_student

def take_attendance():
	# reset all students to "present"
	for kid in roster:
		roster[kid].absent = False

	# ask user to input absent students
	print "Input absent students one at a time, hitting RETURN after each. For example:"
	print "\tAbraham \n\tBeelzebub \n\tCain"
	print "Remember, you must input your students' names exactly as the appear on the roster."
	print "As a reminder, your roster is:"
	for kid in roster:
		print "\t", kid
	print "If no one is absent, just press 'RETURN'"

	absent_list = []

	while True:	
		answer = ask()
		if answer != "":
			if roster.get(answer):
				absent_list.append(answer)
			else:
				print "Not a vaild student name, please try again."
		else:
			break

	absent_string = "; ".join(absent_list)
	# show the user-entered list, ask for confirmation
	print "You said the following students are absent:"
	print "\t", absent_string

	confirmation = confirm()
	
	if confirmation:
		# if user confirms, set specified students to "absent"
		mark_absent(absent_list)

		# update list of present students for use in selection
		present_students = get_present_students()
	elif not(confirmation):
		# if user does not confirm, ask again
		take_attendance()


### TROUBLESHOOTING/TESTING FUNCTIONS ###
def test_always(kid):
	for i in range(0,10000):
		the_student = select()
		if the_student == kid:
			print "PANIC!"
			break

def test_never(kid):
	for i in range(0,10000):
		the_student = select()
		print "%d: %s" % (i, the_student)
		if the_student == kid:
			print "PANIC!"
			break

def multi_test(x):
	for i in range(0,x):
		print "%d: %s" % (i, select())
		#print roster
		#print "-----------"

# make a debug function that will display all of the probabilities?

### ACTION STARTS HERE ###
# list of students (later, will get this from user input)
students = ["ali", "ben", "chuck", "dave"]
#, "erin", "samer", "eric", "merlin", "arthur", "rachel", "carlos", "sindhu"]

# make an empty dict.
roster = {}
present_students = {}

# populate that dict. with all students equally weighted
# --> ONLY FOR FIRST CREATION OF THE LIST! OTHERWISE, WILL GET VALUES FROM TEXT FILE!
for kid in students:
	roster[kid] = Student(kid)

# make a list of students who are present
present_students = get_present_students()

# scale the probabilities of the present students
scale()

# for debugging
print "Roster:", roster
print "Present:", present_students

print "Hello, and welcome to the Student Picker 5000!"

absent_list = []
for kid in roster:
	if roster[kid].absent:
		absent_list.append(kid)
		
absent_string = "; ".join(absent_list)

print "Students absent last time:"
print "\t", absent_string

# ask for user input
while True:
	print "1. pick, 2. input absences, 3. exit"
	answer = ask()
	if answer == "1":
		#select()
		test_never("ben")
	elif answer == "2":
		take_attendance()
		present_students = get_present_students()
		scale()
		print present_students
	elif answer == "3":
		exit()
	else:
		print "Sorry, I didn't get that. Try again."	


# some way to save the state

# notification of who is absent
