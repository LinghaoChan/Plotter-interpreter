import scanner.scannerprocessor as sp
import Parser.parserParser as pp


file_name = 'test.txt'
scanner = sp.Scanner(file_name)
parser = pp.Parser(scanner)
parser.Parser()