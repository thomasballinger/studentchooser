from random import random

students = ["ali", "ben", "chuck", "dave", "erin"]
class_size = len(students)
prob_change = 0.05
# to-do: populate from list 'students'
roster = {"ali": 1, "ben": 1, "chuck": 1, "dave": 1, "erin": 1}

def pick_kid():
	value = random()
	startpoint = 0
	endpoint = 0

	for kid in students:
		endpoint += roster[kid]
		#print "(%f, %f)" % (startpoint, endpoint)
		if startpoint <= value <= endpoint:
			chosen = kid
			if roster[kid] - prob_change < 0:
				roster[kid] = 0
			else:
				roster[kid] -= prob_change
			break
		else:
			startpoint += roster[kid]

	#print value
	#print roster
	return chosen


def scale():
	total = sum(roster.values())
	for kid in roster:
		roster[kid] *= 1.0 / total

def select():
	#print roster
	the_student = pick_kid()
	scale()
	return the_student

scale()

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
		#print "--------"
		if the_student == kid:
			print "PANIC!"
			break

def multi_test(x):
	for i in range(0,x):
		print select()



# some way to save the state

# some way to input absence

# some way to check if student is absent

# notification of who is absent