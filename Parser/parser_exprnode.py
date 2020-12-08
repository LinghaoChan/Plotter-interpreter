import scanner.token as st


class ExprNode(object):
    """
    语法树的结点数据类型，封装为对象。
    如果该结点是双目运算符，则分配左右孩子；
    Data Structure: 
    ----------------------------------------------
    |  Operator  |   left   |   right  |  value  |
    ----------------------------------------------
    如果是常数/变量结点，就是叶子结点，只需要value(变量是Tvalue，一个np.array)；
    Data Structure: 
    ----------------------
    |  item  |   value   |
    ----------------------
    如果是函数类型，则分配函数运算和操作数。
    Data Structure: 
    -------------------------------------------------------
    |  Function  |  functionpointer  |  middle  |  value  |
    -------------------------------------------------------
    """
    def __init__(self, item):
        self.item = item
        # 确定双目运算符的左右孩子
        if self.item == st.Token_Type.PLUS or self.item == st.Token_Type.MINUS or self.item == st.Token_Type.MUL or self.item == st.Token_Type.DIV or self.item == st.Token_Type.POWER:
            self.left = None
            self.right = None
        elif self.item == st.Token_Type.FUNC:        # 函数类型
            self.middle = None
            self.functionpointer = None

        self.value = None

    def GetValue(self):                                         # 依据不同的操作符进行运算
        if self.item == st.Token_Type.PLUS:
            self.value = self.left.value + self.right.value
        elif self.item == st.Token_Type.MUL:
            self.value = self.left.value * self.right.value
        elif self.value == st.Token_Type.POWER:
            self.value = self.left.value ** self.right.value
        elif self.item == st.Token_Type.DIV:
            self.value = self.left.value / self.right.value
        elif self.item == st.Token_Type.MINUS:
            self.value = self.left.value - self.right.value
            
        elif self.item == st.Token_Type.FUNC:
            self.value = self.functionpointer(self.middle.value)       # 完成函数计算功能
        return self.value
