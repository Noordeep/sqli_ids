import re

MAX_ATTACK = 16

def match_words(words, string, score):
	matched = False
	for word in words:
		pattern = re.compile(word)
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

def ruleh1(string):
	words = ["be5d5d37542d75f93a87094459f76678\\W", "e81c4e4f2b7b93b481e13a8553c2ae1b\\W", "a2a551a6458a8de22446cc76d639a9e9 37a6259cc0c1dae299a7866489dff0bd", "like\\W", "a2a551a6458a8de22446cc76d639a9e9 d529e941509eb9e9b9cfaeae1fe7ca23 37a6259cc0c1dae299a7866489dff0bd", "567904efe9e64d9faf3e41ef402cb568\\W"]
	return match_words(words, string, 2)

		

def rule2(string):
	words = ["union", "group by", "order by", "having"]
	return match_words(words, string, 2)

def ruleh2(string):
	words = ["aa252f7bcbb4b8379004aa0c7cf76c10", "db0f6f37ebeb6ea09489124345af2a45 df3f079de6961496f0460dcfdbf9bca3", "70a17ffa722a3985b86d30b034ad06d7 df3f079de6961496f0460dcfdbf9bca3", "061c0f607446c5f26244624e0434c72d"]
	return match_words(words, string, 2)



def rule3(string):
	words = ["declare\\W", "select\\W"]
	return match_words(words, string, 2)

def ruleh3(string):
	words = ["27aec0f4281e186cd83e5d949edd22d5\\W", "99938282f04071859941e18f16efcf42\\W"]
	return match_words(words, string, 2)



def rule4(string):
	words = ["cast\\W", "exec\\W" , "load_file"]
	return match_words(words, string, 2)

def ruleh4(string):
	words = ["54c280558263a67e0a84ba34f625c464\\W", "52fb3679b07eb74d90784e612ca5cb30\\W" , "43d7b4ef7e6729b5c1d81b5f051cffe6"]
	return match_words(words, string, 2)



def rule5(string):
	words = ["drop table", "insert into", "values\\W", "create table", "delete\\W", "update\\W", "bulk insert", "shutdown\\W", "from\\W"]
	return match_words(words, string, 3)

def ruleh5(string):
	words = ["6e9d25362c485bc3c90c818dfac5dc49 aab9e1de16f38176f86d7a92ba337a8d", "e0df5f3dfd2650ae5be9993434e2b2c0 b971be0e2e7176b90d5501eca32a0226", "f09cc7ee3a9a93273f4b80601cafb00c\\W", "76ea0bebb3c22822b4f0dd9c9fd021c5 aab9e1de16f38176f86d7a92ba337a8d", "099af53f601532dbd31e0ea99ffdeb64\\W", "3ac340832f29c11538fbe2d6f75e8bcc\\W", "14f098921bc8c68a8dc0c5529b7013b4 e0df5f3dfd2650ae5be9993434e2b2c0", "5924f03a95ee6f7277e5bdd1e81b8fdc\\W", "d98a07f84921b24ee30f86fd8cd85c3c\\W"]
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
rule_hex = [ruleh1, ruleh2, ruleh3, ruleh4, ruleh5]

def calculate_score(string):
	length = len(rule);
	count = 0
	for i in range(length):
		count = count + rule[i](string)
	print("Score: " + str(count))
	return count

def calculate_score_hex(string, char_score):
	length = len(rule_hex);
	count = char_score
	for i in range(length):
		count = count + rule_hex[i](string)
	print("Score: " + str(count))
	return count