import re

MAX_ATTACK = 16

def match_words(words, string, score):
	matched = False
	for word in words:
		pattern = re.compile(word, re.IGNORECASE)
		match = pattern.search(string)
		if(match):
			matched = True
			break
	if(matched):
		return score
	else:
		return 0


def rule1(string):
	words = ["and\\W", "or\\W", "is null", "like\\W", "is not null", "where\\W"]
	return match_words(words, string, 2)
	

def rule2(string):
	words = ["union", "group by", "order by", "having"]
	return match_words(words, string, 2)


def rule3(string):
	words = ["declare\\W", "select\\W"]
	return match_words(words, string, 2)


def rule4(string):
	words = ["cast\\W", "exec\\W" , "load_file"]
	return match_words(words, string, 2)


def rule5(string):
	words = ["drop table", "insert into", "values\\W", "create table", "delete\\W", "update\\W", "bulk insert", "shutdown\\W", "from\\W"]
	return match_words(words, string, 3)


def rule6(string):
	words = ["--", "%2D%2D", "/*", "*/"]
	return match_words(words, string, 1)


def rule7(string):
	words = ["'", "%27", "\\x22", "%22", "char\\W"]
	return match_words(words, string, 1)


def rule8(string):
	words = [";", "%3B"]
	return match_words(words, string, 1)


def rule9(string):
	words = ["\\(", "%28", "\\)", "%29", "@", "%40"]
	return match_words(words, string, 1)


def rule10(string):
	words = ["=", "%3D"]
	return match_words(words, string, 1)

def rule11(string):
	words1 = ["version\\(", "version%28", "user\\(", "user%28", "system_user\\(", "system_user%28"]
	words2 = ["database\\(", "database%28", "@@hostname", "%40%40hostname", "@@basedir"]
	words3 = ["%40%40basedir", "@@tmpdir", "%40%40tmpdir", "@@datadir", "%40%40datadir"]
	words = words1 + words2 + words3
	return match_words(words, string, 2)


rule = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10]


def calculate_score(string):
	length = len(rule);
	count = 0
	for i in range(length):
		count = count + rule[i](string)
	print("Score: " + str(count))
	return count

