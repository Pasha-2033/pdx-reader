import re
from enum import Enum
from utilities import renumerate, nenumerate

class connection(Enum):
	bracket = r"\{\}\[\]"
	special = r"\.:@\?\|\"\\"
	arithmetic = r"<=>"
	sign = r"\-"

	def regex() -> str:
		result = [r"["]
		for field in connection:
			result.append(field.value)
		result.append(r"]")
		return "".join(result)

re_connection = re.compile(connection.regex())
re_empty = re.compile(r"[\s\n]") #TODO: rename

class token:
	value:		str
	line:		int
	pos:		int
	def __init__(self, value: str, line: int, pos: int):
		self.value = value
		self.line = line
		self.pos = pos
	def __str__(self):
		return self.value
	def __repr__(self):
		return f"(value: \"{self.value}\", line: {self.line}, pos: {self.pos})"

class block:
	token_list:	list[token]
	path:		str
	def __init__(self, path: str, token_list: list[token] = []):
		self.token_list = token_list
		self.path = path

def lex_comment(text: str, pos_offset: int, line: int, token_list: list[token] = []) -> list[token]:
	last_index = len(token_list)
	prev_index = len(text)
	for index, value in renumerate(text):
		if value == '#':
			token_list.insert(last_index, token(text[index:prev_index], line, pos_offset + index))
			prev_index = index
		elif value == '\n':
			token_list.insert(last_index, token(value, line, pos_offset + index))
			prev_index = index
	return token_list

def lex_line(text: str, line: int, token_list: list[token] = []) -> list[token]:
	prev_index = 0
	for index, value in enumerate(text):
		if value == '#':
			if prev_index != index:
				token_list.append(token(text[prev_index:index], line, prev_index))
			lex_comment(text[index:], index, line, token_list)
			break
		elif re_empty.match(value):
			if (prev_index != index):
				token_list.append(token(text[prev_index:index], line, prev_index))
				prev_index = index + 1
			else:
				prev_index += 1
			token_list.append(token(value, line, prev_index))
		elif re_connection.match(value):
			if prev_index != index:
				token_list.append(token(text[prev_index:index], line, prev_index))
			token_list.append(token(value, line, index))
			prev_index = index + 1
		elif index == len(text) - 1:
			token_list.append(token(text[prev_index:], line, prev_index))
	return token_list

def lex_file(path: str, token_list: list[token] = []) -> block:
	with open(path, "r") as f:
		for index, line in enumerate(f):
			lex_line(line, index, token_list)
	return block(path, token_list)

class atomic_number:
	token_list:	list[token]
	def __init__(self, token_list: list[token]):
		self.token_list = token_list
	def __repr__(self):
		return f"(list: \"{self.token_list}\")"

#temp
def find_numbers(token_list: list[token]) -> list[atomic_number]:
	nums = []
	length = 0
	for index, value in enumerate(token_list):
		if re.match(r"[\d+\-\.]", value.value):
			length += 1
		elif length:
			nums.append(atomic_number(token_list[index - length:index]))
			length = 0
		if index == len(token_list) - 1 and length:
			nums.append(atomic_number(token_list[-length:]))
	return nums
#temp
def find_connections(token_list: list[token]):
	toks = []
	for t in token_list:
		if re.match(r"[ \t]", t.value):
			toks.append(t)
		elif re.match(r"[=><]", t.value):
			toks.append(t)
		elif toks:
			print(toks)
			toks = []

class word:
	token_list: list[token]
	def __init__(self, token_list: list[token]):
		self.token_list = token_list
	def __str__(self):
		val = ""
		for t in self.token_list:
			val += t.value
		return val

#tests
if __name__ == "__main__":
	path = "./test.txt"
	b = lex_file(path)
	for t in b.token_list:
		print(t.__repr__())
	print("--------------------------")
	n = find_numbers(b.token_list)
	print(word([token("var", 0, 0), token(":", 0, 0), token("myvar", 0, 0)]))
