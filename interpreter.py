####################################
# DIGITS
####################################
DIGITS = '0123456789' 



####################################
# ERRORS
####################################
class Error:
    def __init__(self, positionStarts, positionEnds, errorName, details):
        self.positionStarts = positionStarts
        self.positionEnds = positionEnds
        self.errorName = errorName
        self.details = details
    
    def asString(self):
        result = f'{self.errorName}: {self.details}\n'
        result += f'File {self.positionStarts.fileName}, line {self.positionStarts.line + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, details, positionStarts, positionEnds):
        super().__init__(positionStarts, positionEnds, 'Illegal Character', details)


####################################
# TOKENS
####################################

class Position:
    def __init__(self, index, line, column, fileName, fileText):
        self.index = index
        self.line = line
        self.column = column
        self.fileName = fileName
        self.fileText = fileText
    
    def advance(self, currentChar):
        self.index += 1
        self.column += 1

        if currentChar == '\n':
            self.line += 1
            self.col += 0
        return self
    def copy(self):
        return Position(self.index, self.line, self.column, self.fileName, self.fileText)



####################################
# TOKENS
####################################

tokenType_INT = 'integer'
tokenType_FLOAT = 'float'
tokenType_PLUS = 'plus'
tokenType_MINUS = 'minus'
tokenType_MUL = 'multiply'
tokenType_DIV = 'division'
tokenType_LPAREN = 'leftParenthesis'
tokenType_RPAREN = 'rightParenthesis'


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}' 

class Lexer:
    def __init__(self, fileName, text):
        self.fileName = fileName
        self.text = text
        self.pos = Position(-1, 0, -1, fileName, text)
        self.currentChar = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.index] if self.pos.index < len(self.text) else None
    
    def makeTokens(self):
        tokens = []

        while self.currentChar != None:
            if self.currentChar in ' ':
                self.advance()
            elif self.currentChar in DIGITS:
                tokens.append(self.makeNumber())            
            elif self.currentChar == '+':
                tokens.append(Token(tokenType_PLUS))
                self.advance()
            elif self.currentChar == '-':
                tokens.append(Token(tokenType_MINUS))
                self.advance()
            elif self.currentChar == '*':
                tokens.append(Token(tokenType_MUL))
                self.advance()
            elif self.currentChar == '/':
                tokens.append(Token(tokenType_DIV))
                self.advance()
            elif self.currentChar == '(':
                tokens.append(Token(tokenType_LPAREN))
                self.advance()
            elif self.currentChar == ')':
                tokens.append(Token(tokenType_RPAREN))
                self.advance()
            else:
                #return error
                positionStart = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(positionStart, self.pos, "'" + char + "'")

        return tokens, None
    
    def makeNumber(self):
        numStr = ''
        dotCount = 0
        while self.currentChar != None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if dotCount == 1: break
                dotCount+=1
                numStr+='.'
            else:
                numStr += self.currentChar
            self.advance()

        if dotCount == 0:
            return Token(tokenType_INT, int(numStr))
        else:
            return Token(tokenType_FLOAT, float(numStr))

####################################
# NODES
####################################

class NumberNode:
    def __init__(self, tokens):
        self.tokens = tokens
    def __repr__(self):
        return f'{self.tokens}'

class BinaryOperationNode:
    def __init__(self, leftNode, operatorToken, rightNode):
        self.leftNode = leftNode
        self.operatorToken = operatorToken
        self.rightNode = rightNode

    def __repr__(self):
        return f'{self.leftNode}, {self.operatorToken}, {self.rightNode}'

####################################
# PARSER
####################################

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.tokenIndex = -1
        self.advance()
    
    def advance(self):
        self.tokenIndex += 1
        if self.tokenIndex < len(self.tokens):
            self.currentToken = self.tokens[self.tokenIndex]
        return self.currentToken

    ###########################################################

    def parse(self):
        res = self.expression()
        return res



    def factor(self):
        token = self.currentToken

        if token.type in (tokenType_INT, tokenType_FLOAT):
            self.advance()
            return NumberNode(token)


    def term(self):
        return self.binaryOperation(self.factor, (tokenType_MUL, tokenType_DIV))

    def expression(self):
        return self.binaryOperation(self.term, (tokenType_PLUS, tokenType_MINUS))

    def binaryOperation(self, func, ops):
        '''
        func = it is a function, that whether it is the term or factor we are looking for.
        ops = operation tokens like, PLUS, MINUS, DIV, MILTIPLICATION
        '''
        leftFactor = func()

        while self.currentToken.type in ops:
            operatorToken = self.currentToken
            self.advance()
            rightFactor = func()
            leftFactor = BinaryOperationNode(leftFactor,operatorToken,rightFactor)

        return leftFactor

####################################
# MAIN RUN ENVIRONMENT
####################################

def run(fileName, text):
    #Generate toekns
    lexer = Lexer(fileName, text)
    tokens, error = lexer.makeTokens()
    if error: return None, error

    #Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    return ast, None


