import Parser.parserParser as pp
import scanner.token as st
import numpy as np
import sys
import matplotlib.pyplot as plt


class Semantic(pp.Parser):
    def init(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def calc(self, x, y):
        # print(x)
        # print(y)
        x *= self.x_scale
        y *= self.y_scale
        y = -y                                      # y轴是反向的
        tmp = x * np.cos(self.rot) + y * np.sin(self.rot)
        y = - x * np.sin(self.rot) + y * np.cos(self.rot)
        x = tmp                                         # 这里不能写两句，要分开写，用tmp寄存
        # print(x)
        # print(y)
        x += self.x_origin
        y += self.y_origin
        return x, y

    def Draw(self):
        x, y = self.calc(self.x_ptr, self.y_ptr)
        self.ax.scatter(x, y)

    def Statement(self):                    # 重写Statement方法
        self.getinto("Statement")
        if self.token.type == st.Token_Type.ORIGIN:
            self.OriginStatement()
        elif self.token.type == st.Token_Type.SCALE:
            self.ScaleStatement()
        elif self.token.type == st.Token_Type.FOR:
            self.ForStatement()
            self.Draw()                     # 增加绘图语句
        elif self.token.type == st.Token_Type.ROT:
            self.RotStatement()
        else:
            print(self.token.type)
            print("出错行号：", self.scanner.LineNo, " 与期望记号不符 ", self.token.lexeme)
            self.scanner.Exit_Scanner()
            sys.exit(1)
        self.exitmodule("Statement")

    def Parser(self):                       # 重写Parser方法
        self.getinto("Parser")
        if self.scanner.filepointer is None:
            print("文件打开失败")
        else:
            self.GetToken()
            self.Program()
            plt.show()
            self.scanner.Exit_Scanner()
            self.exitmodule("Parser")
