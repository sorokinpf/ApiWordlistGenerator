
#
#	Generate wordlists for API fuzzing from basic wordlists
#

import argparse

#
# ---------------------------CONSTANTS---------------------------
#

# extend noun wordlist with plural form
# now works adding "*ss"->"*sses", "*y"->"*ies", default just add "s"
use_plural_form=1

# format define style of generated words
# camel -> GetCustomerNameById
# lower_chain -> get_customer_name_by_id
# camel_chain -> Get_Customer_Name_By_Id
# upper_chain -> GET_CUSTOMER_NAME_BY_ID

formats = {"camel","lower_chain","camel_chain","upper_chain"}


#
# ----------------------------SHCEME----------------------------
#

# ApiWordlist support schemes in format
# "vpnfbni"
# v - word from verb wordlist
# p - word from prefix wordlist (empty string '' exists in prefix wordlist.So formula without "p" is subset of formula with "p")
# n - word from noun wordlist
# N - word from noun wordlist extend by plural form
# f - word from postfix wordlist (empty string '' exists in postfix wordlist. So formula without "f" is subset of formula with "f")
# B - word "By"
# b - word from by wordlist
# I - word "Id"


#
# -----------------------------CODE-----------------------------
#

# Make list of plural form of noun
def make_plural(nouns):
	arr = []
	for noun in nouns:
		if noun[-1]=='y':
			arr.append(noun[:-1]+"ies")		
		elif noun[-2:] == "ss":
			arr.append(noun+"es")			
		elif noun[-1]=='x':
			arr.append(noun+"es")
		else:
			arr.append(noun+"s")

	return arr

def make_wordlist_single(formula,format):
	verbs = open('verbs','r').read().split('\n')
	nouns = open('nouns','r').read().split('\n')
	prefixes = open('prefix','r').read().split('\n')
	postfixes = open('postfix','r').read().split('\n')
	bys = open('by','r').read().split('\n')
	extened_nouns = make_plural(nouns) + nouns
	formula_parse_table = {'v':verbs,'p':prefixes,'n':nouns,'N':extened_nouns,'f':postfixes,'B':['By'],'b':bys,'I':['Id']}
	
	if format == 'camel':
		l = formula_parse_table[formula[0]]
	elif format == 'lower_chain':
		l = map(lambda x: x.lower(),formula_parse_table[formula[0]])
	elif format == 'camel_chain':
		l = formula_parse_table[formula[0]]
	else:
		l = map(lambda x: x.upper(),formula_parse_table[formula[0]])

	for c in formula[1:]:
		if c not in formula_parse_table:
			print 'uncorrect char %s in formula' % c
			return None
		newList = []
		for s1 in l:
			for s2 in formula_parse_table[c]:
				if s2 == '':
					newList.append(s1)
					continue
				if format == 'camel':
					newList.append(s1+s2)
				elif format == 'lower_chain':
					newList.append(s1+'_'+s2.lower())
				elif format == 'camel_chain':
					newList.append(s1+'_'+s2)
				else:
					newList.append(s1+'_'+s2.upper())
		l = newList
	return l

def make_wordlist(formula,format):
	formulas = formula.split(',')
	res = []
	for f in formulas:
		res+=make_wordlist_single(f,format)
	return res

format_help = '''Define style of generated words.
Possible values:
camel -> GetCustomerNameById
lower_chain -> get_customer_name_by_id
camel_chain -> Get_Customer_Name_By_Id
upper_chain -> GET_CUSTOMER_NAME_BY_ID'''

scheme_help = '''# ApiWordlistGen support schemes in format "vpnfbni,vn,vnBbI", where:
v - word from verb wordlist
p - word from prefix wordlist
n - word from noun wordlist
N - word from noun wordlist extend by plural form (now works adding "*ss"->"*sses", "*y"->"*ies", "*x"-> "*xes", default just add "s")
f - word from postfix wordlist
B - word "By"
b - word from by wordlist
I - word "Id"'''

epilog = '''ApiWordlistGen generates wordlist that contains concatinations of all word combinations that matches formula. If more than one formula separated by comma are specifed, ApiWordlistGen generate one merged list.
Empty strings exists in postfix in prefix wordlists, So list for formula without "p" or "f" is subset of list for formula with "p" or "f".

Example:
python ApiWordlistGen.py -f camel -o out.txt vpnfbni,vn,vnBbI
'''

def main():
	parser = argparse.ArgumentParser(description = 'Generate wordlists for API fuzzing from basic wordlists',formatter_class=argparse.RawTextHelpFormatter,epilog=epilog)
	parser.add_argument('--format','-f', help = format_help,default='camel')
	parser.add_argument('--out','-o',help = 'Name of generated file',default='ApiFuzzList.txt')
	parser.add_argument('formula',help = scheme_help)
	parsed = parser.parse_args()	
	
	formula = parsed.formula
	outfile = parsed.out
	format = parsed.format
	if format not in formats:
		print "incorrect format"
		parser.print_help()
		return -1
	
	l = make_wordlist(formula,format)
	file = open(outfile,'w')
	for line in l:
		file.write(line+"\n")
	file.close()	

if __name__=='__main__':
	main()