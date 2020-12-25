# Plotter-interpreter
***Description: The project realizes an interpreter designed for a Function-Drawing-Language.***

## 1. Environment and Requirement

**Operating System**: Windows10

**Tools**: Visual Studio Code

**Requirement**: Python >= 3.8.0, Numpy >= 1.18.5, Matplotlib >= 3.2.1

## 2. The Architecture

```
│-- run.py                  (entrance of the program)
│-- test.txt                (test examples)
│-- testparser.py           (test program for parser)
│-- testscanner.py          (test program for scanner)
├─Parser                    (grammer analysis)
│  │-- parserParser.py      (grammer analysis module)
│  │-- parser_exprnode.py   (define the data structure of grammer tree node)
├─scanner                   (scanner analysis)
│  │-- scannerprocessor.py  (scanner analysis module)
│  │-- token.py             (define the data structure of tokens)
└─semantic                  (semantic analysis)
   │-- semantic.py          (semantic analysis module)
```

## 3. Scanner

+ Class Token

  For each type of token, an abstract data type needs to be defined to storage. I defines its data structure as the class **Tokens**, which includes 4 members: type, lexeme, value, and funcptr, which are used to represent the type of token, Content, value and function pointer.

+ DFA of Scanner

  <img src="image\1.png" alt="1" style="zoom:35%;" />

+ Details 

  * In the construction of the token table, this article uses the functions in the package **numpy** instead of the functions in the package **math**.
  * A method BackChar is defined to implement the character rollback operation while reading file.


## 4. Parser

+ **Class ExprNode**

  In order to construct the syntax tree, I designed the abstract data type of the syntax tree node as ExprNode, which supports realizing the definition of functions, operators and operands.

+ **Function**

  It can calculate the line number through $self.scanner.LineNo$, and can report an error when $token.type != ttype$.

+ **Grammar Tree**

  It prints the syntax tree by designing a pre-order traversal algorithm.

## 5. Semantic

+ **Class Semantic**
  * Class Semantic is an inheritance of the class Parser.
  * According to the parameters extracted by the **ROT**, **SCALE**, and **Origin** methods, they are turned into the member variables of the object, and the drawing is realized through the **FOR** statement.

+ **Attention**

  The formula for the rotation of $x$ and $y$ coordinates is shown in **formula 1**. In the implementation process, the intermediate variable $tmp$ must be used to temporarily store $x$.			

$$
\begin{eqnarray}
\begin{bmatrix} x'\\ y'\\\end{bmatrix}=
\begin{bmatrix}   cos\theta & sin\theta \\  -sin\theta & cos\theta \\     \end{bmatrix}
\begin{bmatrix} x\\ y\\\end{bmatrix}\tag 1
\end{eqnarray}
$$

## 6. Results

+ **Examples 1:**

  ```bash
  rot is 0;
  origin is (0, 0);
  scale is (2,2+2*5+9-1);
  for T from 1 to 3*(1+3**3) step 1 draw (t,-ln(t));
  scale is (20,0.1);
  for T from 0 to 8 step 0.1 draw (t,exp(t));
  scale is (2,1);
  for T from 0 to 300 step 1 draw (t,0);
  for T from 0 to 300 step 1 draw (0,t);
  for T from 0 to 120 step 1 draw (t,t);  --sss
  scale is (2,0.1);
  for T from 0 to 55 step 1 draw (t,-(t*t));   //sss
  scale is (10,5);
  for T from 0 to 60 step 1 draw (t,sqrt(t));
  ```

  <img src="image\Figure_1.svg" alt="Figure_1" style="zoom:67%;" />

+ **Examples 2:**

  ```bash
  rot is 0;
  origin is (0, 0);
  scale is (100,100);
  for t from 0 to pi*20 step Pi/50 draw ((1-1/(10/7))*cos(T)+1/(10/7)*cos(-T*(((10/7)-1))), (1-1/(10/7))*sin(T)+1/(10/7)*sin(-T*((10/7)-1)));
  origin is (500,500);
  scale is (100,100/3);
  rot is pi/2;
  for T from -pi to pi step pi/50 draw (cos(t),sin(t));
  rot is pi/2 + 2*pi/3;
  for T from -pi to pi step pi/50 draw (cos(t),sin(t));
  rot is pi/2 - 2*pi/3;
  for T from -pi to pi step pi/50 draw (cos(t),sin(t));
  ```

<img src="image\Figure_2.svg" alt="Figure_2" style="zoom:67%;" />