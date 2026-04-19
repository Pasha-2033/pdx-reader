from lexer import *

#tests
if __name__ == "__main__":
	lf = lex_file("./test.txt")
	fl = filter_lex(lf)
	