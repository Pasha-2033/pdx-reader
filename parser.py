import re
from enum import Enum

class connection(Enum):
	bracket = r"\{\}\[\]"
	special = r"\.:@\?\|"
	arithmetic = r"<=>"
	sign = r"-"

	def regex() -> str:
		result = [r"["]
		for field in connection:
			result.append(field.value)
		result.append(r"]")
		return "".join(result)

re_connection = re.compile(connection.regex())
re_empty = re.compile(r"[ \t]")

class token:
	file:	str
	text:	str
	line:	int
	pos:	int
	def __init__(self, file: str, text: str, line: int, pos: int):
		self.file = file
		self.text = text
		self.line = line
		self.pos = pos
	def __str__(self):
		return self.text
	def __repr__(self):
		return f"(file: \"{self.file}\", text: \"{self.text}\", line: {self.line}, pos: {self.pos})"

def parse_line(file: str, text: str, line: int, token_list: list[token]) -> list[token]:
	prev_index = 0
	for index, value in enumerate(text):
		if value == "#":
			token_list.append(token(file, text[index:], line + 1, index + 1))
			break
		elif re_empty.match(value):
			if (prev_index != index):
				token_list.append(token(file, text[prev_index:index], line + 1, prev_index + 1))
				prev_index = index + 1
			else:
				prev_index += 1
		elif re_connection.match(value):
			if prev_index != index:
				token_list.append(token(file, text[prev_index:index], line + 1, prev_index + 1))
			token_list.append(token(file, value, line + 1, index + 1))
			prev_index = index + 1
		elif index == len(text) - 1:
			if prev_index != index:
				token_list.append(token(file, text[prev_index:], line + 1, prev_index + 1))
	return token_list



file = "./test.txt"
with open(file, "r") as f:
	tokens = []
	for index, line in enumerate(f):
		if line[-1] == "\n": #EOF doesn`t have "\n"
			parse_line(file, line[:-1], index, tokens)
		else:
			parse_line(file, line, index, tokens)
	for token in tokens:
		print(token.__repr__())