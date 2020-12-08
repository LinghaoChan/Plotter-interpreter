import scanner.scannerprocess as sp
import Parser.parserParser as pp

file_name = 'graphic.txt'
scanner = sp.Scanner(file_name)
parser = pp.Parser(scanner)
parser.Parser()
