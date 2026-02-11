import re
from enum import Enum

class token:
	def __init__(self, text: str, line: int, pos: int, file: str):
		self.text = text
		self.line = line
		self.pos = pos
		self.file = file
	def __str__(self):
		return self.text
class block:
	def __init__(self, tokens: list[token] = []):
		self.tokens = tokens
		create_sub_blocks()
	def create_sub_blocks(self):
		self.sub_blocks = []
		start = 0
		
		

def is_comment(t: token) -> bool:
	return t.text.startswith("#")
def is_atom(t: token) -> bool:
	return bool(re.match(r"\w+", t.text))
def is_connection(t: token) -> bool:
	return bool(re.match(r"[=></\\\.|:@]", t.text))


class num_state(Enum):
	value = r"\d+"
	value_connection = r"\."
	value_sign_or_connection = r"\.|\-"
def may_be_numeric(tokens: list[token], start: int = 0) -> int:
	i = start
	while (i < len(tokens)):
		if not re.match(r"(\d+)|[\.-]", tokens[i].text):
			break
		i = i + 1
	return i - start
def numeric_until(tokens: list[token]) -> int:
	expected = num_state.value
	for i in range(len(tokens) - 1, -1, -1):
		if re.match(expected.value, tokens[i].text):
			if expected == num_state.value:
				expected = num_state.value_sign_or_connection
			elif expected == num_state.value_connection:
				expected = num_state.value
			elif re.match(num_state.value_connection.value, tokens[i].text):
				expected = num_state.value
			else:
				expected = num_state.value_connection
		else:
			return len(tokens) - i - 1
	return len(tokens)

			
			
	


def check_expr(tokens: list[token]) -> token | None:
	if not len(tokens):
		return None
	#atom
	if len(tokens) == 1:
		return None if is_atom(tokens[0]) else tokens[0]
	#expr connection expr
	#"expr"
	#{expr}
	#[expr]





	
	

	


non_valuable_separation = [" ", "\t"]
separation = ["=", "{", "}", ">", "<", "[", "]", ".", "|", ":", "@", "?", '"', "-", "\\"]
def line_to_tokens(text: str, line_num: int, file: str) -> list[token]:
	tokens = []
	last_index = 0
	for i in range(len(text)):
		if text[i] == "#":
			tokens.append(token(text[i:], line_num, i, file))
			return tokens
		elif text[i] in non_valuable_separation:
			if i != last_index:
				tokens.append(token(text[last_index:i], line_num, last_index, file))
			last_index = i + 1
		elif text[i] in separation:
			if i != last_index:
				tokens.append(token(text[last_index:i], line_num, last_index, file))
			tokens.append(token(text[i], line_num, i, file))
			last_index = i + 1
	if last_index != len(text):
		tokens.append(token(text[last_index:], line_num, last_index, file))
	return tokens

file = "./test.txt"
with open(file, "r") as f:
	num_expr = [
		token("1", 0, 0, ""), 
		token(".", 0, 0, ""),
		token("2", 0, 0, ""), 
	]
	print(
		may_be_numeric(
			num_expr,
			0
		)
	)
	print(
		numeric_until(num_expr)
	)
	text = f.read()
	lines = text.split("\n")
	#lines = [l for l in lines if l]
	for i in range(len(lines)):
		ll = line_to_tokens(lines[i], i, file)
		if len(ll):
			for t in ll:
				print(f"'{t}'", end=" ")
			print()