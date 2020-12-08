import scanner.scanner_token as st
import os


class Scanner:
    def __init__(self, f_name):
        self.LineNo = 1
        self.TokenBuffer = ''
        self.f_name = f_name
        if os.path.exists(self.f_name):
            self.filepointer = open(self.f_name, "r")
        else:
            self.filepointer = None

    def Exit_Scanner(self):
        if self.filepointer is None:
            self.filepointer.close()

    def GetChar(self):
        Char = self.filepointer.read(1)   # 读取一个字符
        return Char.upper()         # 转化为大写

    def BackChar(self, Char):
        if Char != '':
            # print(self.filepointer.tell())
            self.filepointer.seek(self.filepointer.tell() - 1)
            # print(self.filepointer.tell())

    def AddCharTokenString(self, Char):
        self.TokenBuffer += Char

    def EmptyTokenString(self):
        self.TokenBuffer = ''

    def JudgeKeyToken(self):  # 获取Token
        Token = st.TokenTab.get(self.TokenBuffer,
                                           st.Tokens(st.Token_Type.ERRTOKEN, self.TokenBuffer,
                                                                0.0, None))
        # Token = st.Tokens(st.TokenTab.get(self.TokenBuffer), self.TokenBuffer, 0.0, None)

        return Token

    def GetToken(self):                                 # DFA
        Char = ''
        token = ''
        self.EmptyTokenString()                         # 初始化token为空串
        while True:
            Char = self.GetChar()
            if Char == '':
                token = st.Tokens(st.Token_Type.NONTOKEN, Char, 0.0, None)

                return token
            if Char == '\n':
                self.LineNo += 1
            if ~Char.isspace():
                break
        self.AddCharTokenString(Char)

        if Char.isalpha():                          # 字母打头的字母数字串
            while True:
                Char = self.GetChar()
                if Char.isalnum():                  # 是否是字母数字串
                    self.AddCharTokenString(Char)   # 加入token字符串
                else:
                    break
            self.BackChar(Char)
            token = self.JudgeKeyToken()            # 识别token类型
            token.lexme = self.TokenBuffer          # token的内容

            return token
        
        elif Char.isdigit():                        # 整数或小数
            while True:
                Char = self.GetChar()
                if Char.isdigit():
                    self.AddCharTokenString(Char)
                else:
                    break
            if Char == '.':                         # 识别小数
                self.AddCharTokenString(Char)
                while True:                         # 识别小数部分
                    Char = self.GetChar()
                    if Char.isdigit():
                        self.AddCharTokenString(Char)
                    else:
                        break
            self.BackChar(Char)
            token = st.Tokens(
                st.Token_Type.CONST_ID, self.TokenBuffer, float(self.TokenBuffer), None)

            return token
        else:
            if Char == ';':
                token = st.Tokens(st.Token_Type.SEMICO, Char, 0.0, None)
            elif Char == '(':
                token = st.Tokens(st.Token_Type.L_BRACKET, Char, 0.0, None)
            elif Char == ')':
                token = st.Tokens(st.Token_Type.R_BRACKET, Char, 0.0, None)
            elif Char == ',':
                token = st.Tokens(st.Token_Type.COMMA, Char, 0.0, None)
            elif Char == '+':
                token = st.Tokens(st.Token_Type.PLUS, Char, 0.0, None)
            elif Char == '-':
                Char = self.GetChar()
                if Char == '-':                         # “--”为注释
                    while Char != '\n' and Char != '':  # 注释直接读到行尾并丢弃
                        Char = self.GetChar()       
                    self.BackChar(Char)
                    return self.GetToken()
                else:                                   # 非注释,minus
                    self.BackChar(Char)
                    token = st.Tokens(st.Token_Type.MINUS, '-', 0.0, None)
            elif Char == '/':
                Char = self.GetChar()
                if Char == '/':                         # “//”为注释
                    while Char != '\n' and Char != '':  # 注释直接读到行尾并丢弃
                        Char = self.GetChar()
                    self.BackChar(Char)
                    return self.GetToken()
                else:                                   # 非注释,div
                    self.BackChar(Char)
                    token = st.Tokens(st.Token_Type.DIV, '/', 0.0, None)
            elif Char == '*':
                Char = self.GetChar()
                if Char == '*':                         # 乘方
                    token = st.Tokens(st.Token_Type.POWER, '**', 0.0, None)
                else:                                   # 乘法运算符
                    self.BackChar(Char)
                    token = st.Tokens(st.Token_Type.MUL, '*', 0.0, None)
            else:
                if Char == ' ' or Char == '\n':
                    return self.GetToken()              # 语句结束
                else:
                    token = st.Tokens(st.Token_Type.ERRTOKEN, Char, 0.0, None)
        return token
