from random import random
from sys import exit

### CONSTANTS ###
# change this value to adjust by how much a student's prob changes when picked
prob_change = 3.0/4.0
default_confirm_msg = "Is this correct? y/n"
data_file = "data.txt"
roster = {}
students = []

### CLASSES ###
class Student(object):
	def __init__(self, name, prob=1, picked=0, absent=False):
		self.name = name
		self.prob = prob
		self.picked = picked
		self.absent = absent
	def __repr__(self):
		# for debug
		return "<%s; %f; %d; %d>" % (self.name, self.prob, self.picked, self.absent)
	def __str__(self):
		# for user output
		return "%s: chosen %d times (absent = %s)" % (self.name, self.picked, self.absent)
	def to_file(self):
		# for file storage
		return "%s; %f; %d; %d" % (self.name, self.prob, self.picked, self.absent)
		

### UTILITY FUNCTIONS ###
def ask():
	return raw_input("> ")

def confirm(msg=default_confirm_msg):
	while True:
		print msg
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
	
	for kid in get_present_students():
		endpoint += get_present_students()[kid].prob
		#print "(%f, %f)" % (startpoint, endpoint)
		if (startpoint <= value <= endpoint):
			chosen = kid
			break
		else:
			startpoint += get_present_students()[kid].prob

	return chosen

def scale():
	# set all prob's back to scale to 100
	for kid in roster:
		roster[kid].prob = 100 * prob_change ** (roster[kid].picked)

	# for all kids who are present, adjust prob. by # of times picked, then scale
	total = 0
	for kid in get_present_students():
			total += get_present_students()[kid].prob
	for kid in get_present_students():
			get_present_students()[kid].prob *= 100.0 / total

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
	while True:
		the_student = pick_kid()

		confirmation = confirm(the_student + " was selected. OK? y/n")

		if confirmation:
			get_present_students()[the_student].picked += 1
			break
		elif not(confirmation):
			print "OK, choosing again."

	scale()
	print the_student
	print roster
	print "----------"
	return the_student

def new_student_list(target_list=students):
		# ask user to input students' names
		print "Input students one at a time, hitting RETURN after each. For example:"
		print "\tAbraham \n\tBeelzebub \n\tCain"
		print "Remember, you must input your students' names exactly as the appear on the roster."
		print "When you're done, just press 'RETURN'"

		temp_students_list = []

		while True:	
			answer = ask()
			if answer != "":
				temp_students_list.append(answer)
			else:
				break

		student_string = "; ".join(temp_students_list)
		# show the user-entered list, ask for confirmation
		print "You provided the following list of students:"
		print "\t", student_string

		confirmation = confirm()
		
		if confirmation:
			target_list = target_list + temp_students_list

			target_list.sort()
			return target_list
		elif not(confirmation):
			# if user does not confirm, ask again
			new_student_list()

def make_roster(input_list=students):
	# populate the roster with the contents of the list of students
	for kid in input_list:
		roster[kid] = Student(kid)

def take_attendance():
	# reset all students to "present"
	for kid in roster:
		roster[kid].absent = False

	# ask user to input absent students
	print "Input absent students one at a time, hitting RETURN after each. For example:"
	print "\tAbraham \n\tBeelzebub \n\tCain"
	print "Remember, you must input your students' names exactly as the appear on the roster."
	print "As a reminder, your roster is:"
	for kid in students:
		print "\t", kid
	print "When you're done (or if no one is absent), just press 'RETURN'"

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
	elif not(confirmation):
		# if user does not confirm, ask again
		take_attendance()

def update_student_list():
	# populate list of student names and sort alphabetically
	for kid in roster:
		students.append(kid)
	students.sort()

def populate_roster():
	roster.clear()

	roster_info = open(data_file)

	for line in roster_info:
		this_line = line.split("; ")
		name = this_line[0]
		prob = float(this_line[1])
		picked = int(this_line[2])
		absent = bool(int(this_line[3]))
		print "name = %r; prob = %r; picked = %r; absent = %r" % (name, prob, picked, absent)
		roster[name] = Student(name, prob, picked, absent)

	update_student_list()

def display_roster():
	for kid in students:
		print "\t", roster[kid]

def last_absent():
	absent_list = []

	for kid in roster:
		if roster[kid].absent:
			absent_list.append(kid)
			
	absent_string = "; ".join(absent_list)

	print "Students absent last time:"
	print "\t", absent_string

def save_data():
	roster_info = open(data_file, "w")
	for kid in roster:
		roster_info.write(roster[kid].to_file())
		roster_info.write("\n")
	roster_info.close

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

### ACTION STARTS HERE ###
print "Hello, and welcome to the Student Picker 5000!"

# ask for user input: new roster, or import from file?
while True:
	print "1. make new roster, 2. use existing roster"
	answer = ask()

	if answer == "1":
		#make_roster(new_student_list())
		print new_student_list()
		print students
		make_roster
		print roster
		break

	elif answer == "2":
		populate_roster()

		last_absent()

		break
	else:
		print "Sorry, I didn't get that. Try again."

# scale the probabilities of the present students
scale()

# for debugging
# print "Roster:", roster
# print "Present:", get_present_students()

# take attendance
# print "Who is absent today?"
# take_attendance()
# scale()

# ask for user input
while True:
	print "1. pick, 2. input absences, 3. view roster, 4. add student(s), 5. exit"
	answer = ask()
	if answer == "1":
		select()
	elif answer == "2":
		take_attendance()
		scale()
	elif answer == "3":
		display_roster()
	elif answer == "4":
		make_roster(new_student_list())
	elif answer == "5":
		save_data()
		exit()
	else:
		print "Sorry, I didn't get that. Try again."	


# some way to save the state
