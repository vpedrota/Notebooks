import pulp
import numpy as np
import itertools

class intervalMatriz:
    
    def __init__(self, lines:int = 0, columns:int = 0):
        self.__lines = lines
        self.__columns = columns
        self.matriz = []

    def see_Intervals(self):
        if(self.__lines <= 0 or self.__columns <= 0):
            raise ValueError("invalid matriz size!")

        for i in self.__lines:
            for j in self.__columns:
                if(self.matriz[i][j]['end'] < self.matriz[i][j]['initial']):
                    raise ValueError("Invalid interval")

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
        self.matriz = intervalMatriz()
        self.matrizB = intervalMatriz()

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
        print(m, n)
        self.matriz.set_columns(n);
        self.matriz.set_lines(m);
        print(self.matriz.get_lines())

        matriz = [] 
        for line in range(0, m):
            aux = []
            for col in range(0,n):
                initial, end = self.arc_input.readline().split(' ')
                initial = int(initial)
                end = int(end)
                aux.append({'initial':initial, 'end':end})     
            matriz.append(aux)

        self.matriz.set_matriz(matriz)

        matrizB = []

        for linha in range(0, m):
            initial, end = self.arc_input.readline().split(' ')
            initial = int(initial)
            end = int(end)
            matrizB.append({'initial' : initial, 'end' : end}) 

        self.matrizB.set_matriz(matrizB)
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
               
                for col in range(0, self.matriz.get_columns()):
                    aux2 += (self.matriz.get_matriz()[row][col][i[col]]*var[col])
                    print(self.matriz.get_matriz()[row][col][i[col]], var[col])

                min += (aux2 <= self.matrizB.get_matriz()[row]['end'])
                min += (aux2 >= self.matrizB.get_matriz()[row]['initial'])
                max += (aux2 <= self.matrizB.get_matriz()[row]['end'])
                max += (aux2 >= self.matrizB.get_matriz()[row]['initial'])
                
        print(min)

        for x in range(0, self.matriz.get_columns()):
            min += var[x]
            min.solve()
            self.arc_output.write('x' + str(x + 1) + ' está no intervalo: ['  + str(var[x].value()) + ', ')
            max += var[x]
            max.solve()
            self.arc_output.write(str(var[x].value()) + ']\n')
      
        
        self.arc_output.close()
    


prob = Problem("input.txt")
if(prob.open_archives()):
    prob.readMatriz()
    prob.solve()
