import sys
"""
Author: Sharon Lee
This program takes inputs from a patient- first name, last name and 
DNA sequence in the hopes of identifying the person's classficiation 
and disease status for Huntington's disease. Huntington's disease is a 
dominant, progressive neurodegenerative disease where the person has a 
mutant form of the protein HTT. Mutant form of HTT protein is caused by 
too many repeats of CAG in that HTT gene. After running this program,
the output is expected to be: first name, last name, DNA sequence, number 
of CAG repeats, classification and disease status. 

"""
def test(did_pass):
	""" Print the result of a test. """
	linenum = sys._getframe(1).f_lineno # Get the caller's line number.
	if did_pass:
		msg = "Test at line {0} ok.".format(linenum)
	else:
		msg = ("Test at line {0} FAILED.".format(linenum))
	print(msg)

def test_suite():
	""" 
	Run the suite of tests for code in this module (this file).
	"""
	#provided test cases
	test(countCAG("C") == 0)
	test(countCAG("CAGCA") == 1)
	test(countCAG("CAGCATCAGCAGCAG") == 1) #see specs
	test(countCAG("CAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCA"
	"GCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCA") == 41)
	test(prediction(27) == ('Intermediate', 'Unaffected'))
	test(prediction(34) == ('Intermediate', 'Unaffected'))
	test(prediction(38) == ('Reduced Penetrance', 'Somewhat Affected'))
	test(prediction(45) == ('Full Penetrance', 'Affected'))

	#self test cases
	test(countCAG("") == 0)
	test(countCAG("CA") == 0)
	test(countCAG("AGCCAGCAGCA") == 0)
	test(countCAG("CAGCAGCAGCA") == 3)
	test(countCAG("CAGCAGCAACAGCAG") != 4)
	test(countCAG("GGGCAGCAGCAGCAGCAGCAGCAGCAGCAGGGGCAGCAGCAGCAGCAGCAGCAGCA"
	"GCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCA") != 41)
	test(prediction(-10) == ("Error! The number of CAGs you entered is invalid"))
	test(prediction(10) == ('Normal', 'Unaffected'))
	test(prediction(26) == ('Normal', 'Unaffected'))
	test(prediction(27) != ('Normal', 'Unaffected'))
	test(prediction(28) == ('Intermediate', 'Unaffected'))
	test(prediction(35) != ('Reduced Penetrance', 'Somewhat Affected'))
	test(prediction(36) == ('Reduced Penetrance', 'Somewhat Affected'))
	test(prediction(39) != ('Full Penetrance', 'Affected'))
	test(prediction(40) == ('Full Penetrance', 'Affected'))

def countCAG(dna):
	"""
	This function counts the number of consecutive CAGs in the given sequence. 
	To loop through the sequence in codon fashion (3 nucleotides at once), I 
	set up the for loop to increment by 3. Since the function is supposed to 
	count consecutive CAGs, 2 temp variables are set up: curr_3nt and next_3nt.
	these two variables are substrings of the given DNA sequence- curr_3nt is 
	the current 3 nucleotides reading from position i to i+3, and next_3nt is 
	the next 3 nucleorides reading from position i+3 to i+6. 4 cases are considered-
	1. if both current and next 3 nucleotides are CAG, CAGcount is incremented by 1.
		continue with the for loop.
	2. if case 1 doesn't pass, but if current 3 nucleotides are CAG and we are reaching
		the end of the given dna sequence, CAG count plus 1 and exit out the for loop.
	3. if none of the above, but current 3 nucleotides are CAG but not the next 3, 
		CAG count plus 1 and exit out of for loop.
	4. if current 3 nucleotides is not CAG, break 	
	CAGcounts is then returned as an integer. 
	"""
	dna_length = len(dna)
	CAGcounts = 0
	CAG = "CAG"

	for i in range(0, dna_length-1, 3):
		curr_3nt = dna[i:i+3]
		next_3nt = dna[i+3: i+6]
#		print(curr_3nt)
#		print(next_3nt)

		if curr_3nt == CAG and next_3nt == CAG:
#			print(i, "first if case")
			CAGcounts += 1
		elif curr_3nt == CAG and i+3 <= dna_length:
#			print(i, "second if")
			CAGcounts += 1
			break
		elif curr_3nt == CAG and next_3nt != CAG:
#			print(i, "3rd if case")
			CAGcounts += 1
			break
		elif curr_3nt != CAG:
			break
#	print(CAGcounts)
	return CAGcounts


def prediction(numCAG):
	"""
	This function takes in the parameter numCAG, which is the number of 
	consecutive CAGs, and return the classfication and disease status based 
	on the number of consecutive CAGs.
	The status goes by the chart:
	< 27	Normal				unaffected
	27-35	Intermediate		unaffected 
	36-39	Reduced Penetrance  somewhat affected 
	>39		Full Penetrance  	affected
	"""
	if numCAG >= 0: 
		if numCAG < 27:
			return ('Normal', 'Unaffected')
		elif numCAG >= 27 and numCAG <= 35:
			return ('Intermediate', 'Unaffected')
		elif numCAG >= 36 and numCAG <= 39:
			return ('Reduced Penetrance', 'Somewhat Affected')
		elif numCAG > 39:
			return ('Full Penetrance', 'Affected')
	else:
		return ("Error! The number of CAGs you entered is invalid")

def get_input():
	"""
	This function prompts the command asking for the user to provide their
	information- first name, last name and DNA sequence. The inputs are stored 
	in a tuple to be used in other functions later.
	"""
	first_name = input("Please enter your first name:")
	last_name = input("Please enter your last name:")
	DNA_info = input("Please enter your DNA sequence:")

	patient_info = (first_name, last_name, DNA_info)

	return patient_info


def main():
	info = get_input()
	counts = countCAG(info[2])
	classification = prediction(counts)
	final_result = (info, counts, classification)
	print("Final Result for ", info[0], info[1], "with DNA sequence-", 
		info[2], ": has", counts, "CAG repeats, the classfication is",
		classification[0], ", and the disease status is", classification[1],
		".")


if __name__== "__main__":
	main()
	test_suite()