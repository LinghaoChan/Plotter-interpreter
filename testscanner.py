import scanner.scanner_token as scanner_token
import scanner.scannerprocess as scannerprocess

f_name = 'graphic.txt'
scanner = scannerprocess.Scanner(f_name)

if scanner.filepointer is not None:
    print("token_type           lexeme          value       ptr")
    print("------------------------------------------------------")
    while True:                                                             # 一次读入一个token
        token = scanner.GetToken()                                          # 以空格分开
        if token.type != scanner_token.Token_Type.NONTOKEN:
            print("{:20s}|{:12s}|{:12f}|{}".format(
                token.type, token.lexeme, token.value, token.funcptr))
        else:
            break
    print("The text has", scanner.LineNo, "lines.")
else:
    print("File open failed")
