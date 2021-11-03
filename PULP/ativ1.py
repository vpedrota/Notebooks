import pulp
import numpy as np
import itertools
import random
import scipy.optimize as optimize
class intervalMatriz:
    
    def __init__(self, lines:int = 0, columns:int = 0):
        self.__lines = lines
        self.__columns = columns
        self.create()

    def see_Intervals(self):
        if(self.__lines <= 0 or self.__columns <= 0):
            raise ValueError("Invalid matriz size!")

        for i in self.__lines:
            for j in self.__columns:
                if(self.matriz[i][j]['end'] < self.matriz[i][j]['initial']):
                    raise ValueError("Invalid interval!")
    
    def create(self):
        self.matriz = [[[] for _ in range(0,self.__lines)] for _ in range(0,self.__columns)]

    def set_element(self, i, j, a, b):

        if(self.__lines <= 0 or self.__columns <= 0):
            raise ValueError("Invalid matriz size!")

        if(i > self.__lines  or j > self.__columns):
            raise ValueError("Invalid matriz size!")

        if(a > b):
            raise ValueError("Invalid interval!")

        self.matriz[i][j] = {'initial': a, 'end': b}
    
    def get_element(self, i, j) -> int:

        if(self.__lines <= 0 or self.__columns <= 0):
            raise ValueError("Invalid matriz size!")

        if(i > self.__lines  or j > self.__columns):
            raise ValueError("Invalid matriz size!")

        return self.matriz[i][j]
        

    def get_lines(self):
        return self.__lines 

    def get_columns(self):
        return self.__columns 

    def get_matriz(self):
        return self.matriz 

    def set_lines(self, lines):
        self.__lines = lines

    def set_columns(self, columns):
        self.__columns = columns

    def set_matriz(self, matriz):
        self.matriz = matriz

class Problem:

    def __init__(self, input = "input.txt", output = "output.txt"):
        
        self.input = input
        self.output = output
        self.arc_input = None
        self.arc_output = None
        self.matriz = None
        self.matrizB = None

    def open_archives(self):
        try:
            self.arc_input = open(self.input, "r")
            self.arc_output = open(self.output, "w")
            print("Succesful!")
            return True
        except FileNotFoundError:
            print("Archive input.txt not found")
            return False
            
    def readMatriz(self):

        m, n = self.arc_input.readline().split(' ')
        m = int(m)
        n = int(n)

        self.matriz = intervalMatriz(m, n)
        self.matrizB = intervalMatriz(1, m)

        for line in range(0, m):
            for col in range(0, n):
                initial, end = self.arc_input.readline().split(' ')
                initial = int(initial)
                end = int(end)
                self.matriz.set_element(line, col, initial, end)     

        for linha in range(0, m):
            initial, end = self.arc_input.readline().split(' ')
            initial = int(initial)
            end = int(end)
            self.matrizB.set_element(linha, 0, initial, end)

        self.arc_input.close()
        

    def solve(self):

        var = []
        for x in range(0, self.matriz.get_columns()): 
            var.append(pulp.LpVariable('x' + str(x+1), cat='Continuous'))

        min = pulp.LpProblem('intro', pulp.LpMinimize)
        max = pulp.LpProblem('intro', pulp.LpMaximize)

        for row in range(0,  self.matriz.get_lines()):
            for i in itertools.product(['initial','end'], repeat=self.matriz.get_columns()):
                aux2 = 0
               
                #lembrar de usar getter and setter aproriadamente
                for col in range(0, self.matriz.get_columns()):
                    aux2 += (self.matriz.get_matriz()[row][col][i[col]]*var[col])
                    print(self.matriz.get_matriz()[row][col][i[col]], var[col])

                min += (aux2 <= self.matrizB.get_element(row, 0)['end'])
                min += (aux2 >= self.matrizB.get_element(row, 0)['initial'])
                max += (aux2 <= self.matrizB.get_element(row, 0)['end'])
                max += (aux2 >= self.matrizB.get_element(row, 0)['initial'])

        for x in range(0, self.matriz.get_columns()):
            min += var[x]
            min.solve()
            self.arc_output.write('x' + str(x + 1) + ': ['  + str(var[x].value()) + ', ')
            max += var[x]
            max.solve()
            self.arc_output.write(str(var[x].value()) + ']\n')
      
        self.arc_output.close()

class Problem2:

    def __init__(self, input = "input.txt", output = "output.txt"):
        self.input = input
        self.output = output
        self.arc_input = None
        self.arc_output = None
        self.matriz = intervalMatriz()
        self.matrizB = intervalMatriz()

    #objctive function, we need to minimize each variable
    def fun(x, i):
        return x[i]

    def open_archives(self):

        try:
            self.arc_input = open(self.input, "r")
            self.arc_output = open(self.output, "w")
            print("Succesful!")
            return True
        except FileNotFoundError:
            print("input file not found")
            return False
            
    def readMatriz(self):

        m, n = self.arc_input.readline().split(' ')
        m = int(m)
        n = int(n)

        self.matriz = intervalMatriz(m, n)
        self.matrizB = intervalMatriz(1, m)

        for line in range(0, m):
            for col in range(0, n):
                initial, end = self.arc_input.readline().split(' ')
                initial = int(initial)
                end = int(end)
                self.matriz.set_element(line, col, initial, end)     


        for linha in range(0, m):
            initial, end = self.arc_input.readline().split(' ')
            initial = int(initial)
            end = int(end)
            self.matrizB.set_element(linha, 0, initial, end)

        self.arc_input.close()

    def constrait(self, x, linha):

        soma = 0
        aux = 0

        for i in range(linha*self.matriz.get_columns(), linha*self.matriz.get_columns() + self.matriz.get_columns()):
            soma += x[i]*x[aux+self.matriz.get_columns()*self.matriz.get_lines()]
            aux+=1

        soma -= x[i+self.matriz.get_columns()+1]

        return soma


    def solve(self):
        #generating some initial values 
        x0 = random.sample(range(0, 10), self.matriz.get_columns())

        #list with the constraints 
        con = []

        #adding constraints 
        for i in range(0, self.matriz.get_lines()):
            con.append({'type': 'eq', 'fun': lambda x: self.constrait(x, i)})


        bnds = [(self.matriz.get_element(i, j)['initial'], self.matriz.get_element(i, j)['end']) for i in range(0, self.matriz.get_lines()) for j in range(0, self.matriz.get_columns())]

        for x in range(0, self.matriz.get_columns()):
            bnds.append((None, None))
        
        for linha in range(0, self.matriz.get_lines):
            bnds.append((self.matrizB.get_element(0, linha)['initial'], self.matrizB.get_element(0, linha)['end']))
            
        res = optimize.minimize(self.fun, x0, options={'disp': True}, constraints=con, bounds=bnds, args=4)

prob = Problem2("input.txt")
if(prob.open_archives()):
    prob.readMatriz()
    prob.solve()
           
