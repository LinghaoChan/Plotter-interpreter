import numpy as np
import sys
import Parser.parser_exprnode as pn
import scanner.token as st


class Parser(object):
    """
    语法分析器主体
    遵循的文法：
    Program  →  { Statement SEMICO } 
    Statement →  OriginStatment | ScaleStatment |  RotStatment    | ForStatment
    OriginStatment → ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET
    ScaleStatment  → SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET
    RotStatment → ROT IS Expression
    Expression 	→ Term   { ( PLUS | MINUS ) Term } 
    Term       	→ Factor { ( MUL | DIV ) Factor }
    Factor  	→ ( PLUS | MINUS ) Factor | Component
    Component 	→ Atom [ POWER Component ]
    Atom → CONST_ID
          | T
          | FUNC L_BRACKET Expression R_BRACKET
          | L_BRACKET Expression R_BRACKET 
    """
    def __init__(self, scanner):
        self.scanner = scanner
        self.token = None
        self.x_origin = 0
        self.y_origin = 0
        self.x_scale = 1
        self.y_scale = 1
        self.rot = 0
        self.x_ptr = None
        self.y_ptr = None
        self.Tvalue = 0

    def getinto(self, x):
        # print("Begin analysing", str(x))
        pass

    def exitmodule(self, x):
        # print("Finished analysing", str(x))
        pass

    def tokenMatchedSuccessed(self, x):
        print('Match token', str(x))

    def printtree(self, x):
        self.PreorderPrintTree(x, 1)
    
    # 打印语法树,前序遍历
    def PreorderPrintTree(self, node, index_range): 
        for i in range(index_range):
            print('---  ', end=' ')
        if node.item == st.Token_Type.PLUS:
            print('+ ')
        elif node.item == st.Token_Type.MINUS:
            print('- ')
        elif node.item == st.Token_Type.FUNC:
            print("{} ".format(node.functionpointer))
        elif node.item == st.Token_Type.CONST_ID:
            print('{:4f} '.format(node.value))
        elif node.item == st.Token_Type.DIV:
            print("/ ")
        elif node.item == st.Token_Type.POWER:
            print("** ")
        elif node.item == st.Token_Type.MUL:
            print('* ')
        elif node.item == st.Token_Type.T:
            # node('{} '.format(root.value))           # 打印T的范围
            pass
        else:
            print("Type error.")
            sys.exit(0)
        if node.item == st.Token_Type.CONST_ID or node.item == st.Token_Type.T:
            return
        elif node.item == st.Token_Type.FUNC:
            self.PreorderPrintTree(node.middle, index_range + 1)
        else:
            self.PreorderPrintTree(node.left, index_range + 1)
            self.PreorderPrintTree(node.right, index_range + 1)

    # 语法分析器测试入口
    def Parser(self):
        self.getinto("Parser")
        if self.scanner.filepointer is None:
            print("File open error.")
        else:
            self.GetToken()
            self.Program()
            self.scanner.Exit_Scanner()
            self.exitmodule("Parser")
            # print(self.x_origin, self.y_origin)

    # Program  →  { Statement SEMICO }
    def Program(self): 
        self.getinto("The Program")
        while self.token.type != st.Token_Type.SEMICO:
            self.Statement()                                    # Statement
            self.MatchToken(st.Token_Type.SEMICO)    # SEMICO
            self.tokenMatchedSuccessed("; ")
        self.exitmodule("The Program")

    # Statement →  OriginStatment | ScaleStatment | RotStatment | ForStatment
    def Statement(self):
        self.getinto("The Statement")             # 查找对应产生式, FIRST SET
        if self.token.type == st.Token_Type.ORIGIN:
            self.OriginStatement()
        elif self.token.type == st.Token_Type.SCALE:
            self.ScaleStatement()
        elif self.token.type == st.Token_Type.ROT:
            self.RotStatement()
        elif self.token.type == st.Token_Type.FOR:
            self.ForStatement()
        else:
            print(self.token.type)
            print("Error line number：", self.scanner.LineNo, " dosen't expected token： ", self.token.lexeme)
            self.scanner.Exit_Scanner()
            sys.exit(1)
        self.exitmodule("The Statement")

    # OriginStatment → ORIGIN IS  L_BRACKET Expression COMMA Expression R_BRACKET
    def OriginStatement(self):
        self.getinto("The OriginStatement")
        self.MatchToken(st.Token_Type.ORIGIN)
        self.tokenMatchedSuccessed("ORIGIN")
        self.MatchToken(st.Token_Type.IS)
        self.tokenMatchedSuccessed("IS")
        self.MatchToken(st.Token_Type.L_BRACKET)
        self.tokenMatchedSuccessed("(")
        tmp = self.Expression()
        self.x_origin = tmp.GetValue()
        self.MatchToken(st.Token_Type.COMMA)
        self.tokenMatchedSuccessed(",")
        tmp = self.Expression()
        self.y_origin = tmp.GetValue()
        self.MatchToken(st.Token_Type.R_BRACKET)
        self.tokenMatchedSuccessed(")")
        self.exitmodule("The OriginStatement")

    # ScaleStatment  → SCALE IS  L_BRACKET Expression COMMA Expression R_BRACKET
    def ScaleStatement(self):
        self.getinto("The ScaleStatement")
        self.MatchToken(st.Token_Type.SCALE)
        self.tokenMatchedSuccessed("SCALE")
        self.MatchToken(st.Token_Type.IS)
        self.tokenMatchedSuccessed("IS")
        self.MatchToken(st.Token_Type.L_BRACKET)
        self.tokenMatchedSuccessed("(")
        tmp = self.Expression()
        self.x_scale = tmp.GetValue()
        self.MatchToken(st.Token_Type.COMMA)
        self.tokenMatchedSuccessed(",")
        tmp = self.Expression()
        self.y_scale = tmp.GetValue()
        self.MatchToken(st.Token_Type.R_BRACKET)
        self.tokenMatchedSuccessed(")")
        self.exitmodule("The ScaleStatement")

    # ForStatment  → FOR T FROM Expression TO Expression STEP Expression DRAW L_BRACKET Expression COMMA Expression R_BRACKET
    def ForStatement(self):
        self.getinto("The ForStatement")
        start = 0.0
        end = 0.0
        step = 0.0
        self.MatchToken(st.Token_Type.FOR)
        self.tokenMatchedSuccessed("FOR")
        self.MatchToken(st.Token_Type.T)
        self.tokenMatchedSuccessed("T")
        self.MatchToken(st.Token_Type.FROM)
        self.tokenMatchedSuccessed("FROM")
        start_ptr = self.Expression()
        start = start_ptr.GetValue()                    # 绘图起始点
        self.MatchToken(st.Token_Type.TO)
        self.tokenMatchedSuccessed("TO")
        end_ptr = self.Expression()
        end = end_ptr.GetValue()                        # 绘图终点
        self.MatchToken(st.Token_Type.STEP)
        self.tokenMatchedSuccessed("STEP")
        step_ptr = self.Expression()
        step = step_ptr.GetValue()                      # 间隔
        self.Tvalue = np.arange(start, end, step)       # numpy类型传给matplotlib绘图
        self.MatchToken(st.Token_Type.DRAW)
        self.tokenMatchedSuccessed("DRAW")
        self.MatchToken(st.Token_Type.L_BRACKET)
        self.tokenMatchedSuccessed("(")
        self.x_ptr = self.Expression()
        self.x_ptr = self.x_ptr.value
        # print(self.x_ptr)
        self.MatchToken(st.Token_Type.COMMA)
        self.tokenMatchedSuccessed(",")
        self.y_ptr = self.Expression()
        self.y_ptr = self.y_ptr.value
        # print(self.y_ptr)
        self.MatchToken(st.Token_Type.R_BRACKET)
        self.tokenMatchedSuccessed(")")
        self.exitmodule("The ForStatement")

    # RotStatment → ROT IS Expression
    def RotStatement(self):
        self.getinto("The RotStatement")
        self.MatchToken(st.Token_Type.ROT)
        self.tokenMatchedSuccessed("ROT")
        self.MatchToken(st.Token_Type.IS)
        self.tokenMatchedSuccessed("IS")
        tmp = self.Expression()
        self.rot = tmp.GetValue()
        self.exitmodule("The RotStatement")

    # Expression → Term { ( PLUS | MINUS ) Term }
    def Expression(self):
        self.getinto("The Expression")
        left = self.Term()
        while self.token.type == st.Token_Type.PLUS or self.token.type == st.Token_Type.MINUS:
            tmp = self.token.type
            self.MatchToken(tmp)
            right = self.Term()
            left = self.MakeExprNode(tmp, left, right)
        self.printtree(left)           # 打印表达式语法树
        self.exitmodule("The Expression")
        # print(left)
        return left

    # Term → Factor { ( MUL | DIV ) Factor }
    def Term(self):
        left = self.Factor()
        while self.token.type == st.Token_Type.MUL or self.token.type == st.Token_Type.DIV:
            tmp = self.token.type
            self.MatchToken(tmp)
            right = self.Factor()
            left = self.MakeExprNode(tmp, left, right)     # 左节点指向新的复介电
        # print(left)
        return left                                         # 返回父节点

    # Factor → ( PLUS | MINUS ) Factor | Component
    def Factor(self):
        if self.token.type == st.Token_Type.PLUS:
            self.MatchToken(st.Token_Type.PLUS)
            right = self.Factor()                       # 右侧是Factor
            left = None                                 # 加号的左侧是空，不需要处理
            right = self.MakeExprNode(
                st.Token_Type.PLUS, left, right)
        elif self.token.type == st.Token_Type.MINUS:
            self.MatchToken(st.Token_Type.MINUS)
            right = self.Factor()                       # 右侧是Factor
            left = pn.ExprNode(st.Token_Type.CONST_ID)
            left.value = 0.0                            # 减号的左侧是0.0，将负数升级为表达式
            right = self.MakeExprNode(
                st.Token_Type.MINUS, left, right)
        else:
            right = self.Component()
        return right

    # Component → Atom [ POWER Component ]
    def Component(self):
        left = self.Atom()
        if self.token.type == st.Token_Type.POWER:
            self.MatchToken(st.Token_Type.POWER)
            right = self.Component()            # 递归生成右结点
            left = self.MakeExprNode(           # 构造树：Atom —— POWER —— Component
                st.Token_Type.POWER, left, right)
        return left

    # Atom → CONST_ID
    #       | T
    #       | FUNC L_BRACKET Expression R_BRACKET
    #       | L_BRACKET Expression R_BRACKET 
    def Atom(self):
        if self.token.type == st.Token_Type.CONST_ID:
            tmp = self.token.value                         # 获取当前常数具体值
            self.MatchToken(st.Token_Type.CONST_ID)
            node = self.MakeExprNode_CONST(
                st.Token_Type.CONST_ID, tmp)    # 构造这个常数节点
        elif self.token.type == st.Token_Type.T:
            self.MatchToken(st.Token_Type.T)
            if len(self.Tvalue) == 1:
                node = self.MakeExprNode_CONST(
                    st.Token_Type.T, 0.0)
            else:
                node = self.MakeExprNode_CONST(
                    st.Token_Type.T, self.Tvalue)
        elif self.token.type == st.Token_Type.FUNC:  # FUNC L_BRACKET Expression R_BRACKET
            temp_ptr = self.token.funcptr
            self.MatchToken(st.Token_Type.FUNC)
            self.MatchToken(st.Token_Type.L_BRACKET)
            self.tokenMatchedSuccessed("(")
            tmp = self.Expression()
            node = self.MakeExprNode(
                st.Token_Type.FUNC, temp_ptr, tmp)  # FUNC, 函数指针, 函数内部
            self.MatchToken(st.Token_Type.R_BRACKET)
            self.tokenMatchedSuccessed(")")
        elif self.token.type == st.Token_Type.L_BRACKET:
            self.MatchToken(st.Token_Type.L_BRACKET)
            self.tokenMatchedSuccessed("(")
            node = self.Expression()
            self.MatchToken(st.Token_Type.R_BRACKET)
            self.tokenMatchedSuccessed(")")
        else:
            print(self.token.type)
            print("Error line number: ", self.scanner.LineNo, " dosen't expected token: ", self.token.lexeme)
            self.scanner.Exit_Scanner()
            sys.exit(1)
        # print(node)
        return node

    def MakeExprNode(self, item, left, right):
        expr = pn.ExprNode(item)
        if item == st.Token_Type.FUNC:
            expr.functionpointer = left             # 函数功能计算
            expr.middle = right              # 操作数集合numpy.array
        else:
            expr.left = left
            expr.right = right
        expr.GetValue()                      # 计算左右孩子的操作结果
        return expr

    def MakeExprNode_CONST(self, item, value):
        expr = pn.ExprNode(item)
        expr.value = value
        return expr

    def GetToken(self):
        self.token = self.scanner.GetToken()
        while self.token.type == st.Token_Type.NONTOKEN:
            self.token = self.scanner.GetToken()
        if self.token == st.Token_Type.ERRTOKEN:
            print(self.token.type)
            print("Error line number：", self.scanner.LineNo, " token error ", self.token.lexeme)
            self.scanner.Exit_Scanner()
            sys.exit(1)

    def MatchToken(self, ttype):
        if self.token.type != ttype:
            print(self.token.type)
            print("Error line number：", self.scanner.LineNo, " dosen't expected token ", self.token.lexeme)
            self.scanner.Exit_Scanner()
            sys.exit(1)
        if ttype == st.Token_Type.SEMICO:
            self.scanner.filepointer.readline()
            last = self.scanner.filepointer.tell()
            next_line = self.scanner.filepointer.readline()   # 读取到分号，判断文件是否结束
            if len(next_line) == 0:
                return
            else:
                self.scanner.filepointer.seek(last)
        self.GetToken()               # 取下个操作符放入self.token
