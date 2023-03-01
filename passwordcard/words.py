#This program enable you to generate pronounceable - not always i admit - words with custom and/or random properties. It can for instance be used to make passwords which are easy to memorize.

import random
###Vars. You can freely add vowels, consonant and syllabes without changing the program
v = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
c = ['a','e','i','o','u']
s = []
for a in v:
	for b in c:
		s.append(a+b)
		
###Config: fill each list with 0 and 1, if you want 2/3 of probability take [0,1,1], for 1/4 take [0,1,0,0] for example.
start_vowel = [0,1] #Probability to get a word starting by a vowel
end_consonant = [0,1] #Probability to get a word ending by a consonant

#This function generate a word with a fixed or random number of syllabe, based on the above-written properties
def gen_word(nbr = 0):  #nbr = number of syllabes
	if nbr == 0:
		nbr = random.randint(1, 10)
	word = ""
	for a in range(nbr):
		word += random.sample(s, 1)[0]
	if random.choice(start_vowel) == 1:
		word = random.sample(c, 1)[0] + word
	if random.choice(end_consonant) == 1:
		word += random.sample(v, 1)[0]
	return word
#This function retun a list of nbr words with sy syllabes (if sy = 0, the number of syllabe is random)	
def gen_x_words(nbr, sy = 0):
	result = []
	for a in range(nbr):
		result.append(gen_word(sy))
	return result