import re
from enum import Enum
from utilities import reverse_begin, forward_begin

class connection(Enum):
	bracket		= r"\{\}\[\]"
	special		= r"\.:@\?\|"
	arithmetic	= r"<=>"
	sign		= r"\-"
	string		= r"\"\\"

	def regex() -> str:
		return r"[" + r"".join([field.value for field in connection]) + r"]"

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
		return self.value #f"(value: \"{self.value}\", line: {self.line}, pos: {self.pos})"

def lex_comment(text: str, pos_offset: int, line: int, token_list: list[token] = []) -> list[token]:
	last_index = len(token_list)
	prev_index = len(text)
	for index, value, it in reverse_begin(text):
		if value == "#":
			token_list.insert(last_index, token(text[index:prev_index], line, pos_offset + index))
			prev_index = index
		elif value == "\n":
			token_list.insert(last_index, token(value, line, pos_offset + index))
			prev_index = index
	return token_list

def lex_line(text: str, line: int, token_list: list[token] = []) -> list[token]:
	prev_index = 0
	string_started = False
	screen = 0
	for index, value, it in forward_begin(text):
		if value == "\"" and not screen % 2:
			string_started = not string_started
		if value == "#" and not string_started:
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
		if value == "\\":
			screen += 1
		else:
			screen = 0
	return token_list

def lex_file(path: str, token_list: list[token] = []) -> list[token]:
	with open(path) as f:
		for index, line in enumerate(f):
			lex_line(line, index, token_list)
	return token_list

def filter_string(token_list: list[token]) -> int:
	screen = 0
	for index, tok, it in forward_begin(token_list, 1):
		if tok.value == "\"" and not screen % 2:
			return index + 1
		elif tok.value == "\\":
			screen += 1
		else:
			screen = 0
	return len(token_list)
def filter_lex(token_list: list[token]) -> list[token]:
	for index, tok, it in forward_begin(token_list):
		if tok.value == "\"":
			it.set_index(index + filter_string(token_list[index:]) - 1)
		elif re_empty.match(tok.value):
			del token_list[index]
			it.set_index(index - 1)
	return token_list

#tests
if __name__ == "__main__":
	toks = lex_file("./test.txt")
	#for t in toks:
	#	print(t.__repr__())
	vals = filter_lex(toks)
	for t in vals:
		#for v in t:
			#print(f"({v.value})")
		print(t.__repr__())
