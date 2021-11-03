import pulp
import numpy as np
import itertools
import scipy.optimize as optimize

#Interval matrix
class intervalMatrix:
    
    def __init__(self, lines:int = 0, columns:int = 0):
        self.__lines = lines
        self.__columns = columns
        self.create()

    #verify the intervals, see if a <= b
    def see_Intervals(self):
        if(self.__lines <= 0 or self.__columns <= 0):
            raise ValueError("Invalid matrix size!")

        for i in self.__lines:
            for j in self.__columns:
                if(self.matrix[i][j]['end'] < self.matrix[i][j]['initial']):
                    raise ValueError("Invalid interval!")
    
    #create the structure
    def create(self):
        self.matrix = [[[] for _ in range(0,self.__lines)] for _ in range(0,self.__columns)]

    #set a new element with the pattern
    def set_element(self, i, j, a, b):

        if(self.__lines <= 0 or self.__columns <= 0):
            raise ValueError("Invalid matrix size!")

        if(i > self.__lines  or j > self.__columns):
            raise ValueError("Invalid matrix size!")

        if(a > b):
            raise ValueError("Invalid interval!")

        self.matrix[i][j] = {'initial': a, 'end': b}
    
    #return the element
    def get_element(self, i, j) -> int:

        if(self.__lines <= 0 or self.__columns <= 0):
            raise ValueError("Invalid matrix size!")

        if(i > self.__lines  or j > self.__columns):
            raise ValueError("Invalid matrix size!")

        return self.matrix[i][j]
        

    #some getters and setters

    def get_lines(self):
        return self.__lines 

    def get_columns(self):
        return self.__columns 

    def get_matrix(self):
        return self.matrix 

    def set_lines(self, lines):
        self.__lines = lines

    def set_columns(self, columns):
        self.__columns = columns

    def set_matrix(self, matrix):
        self.matrix = matrix

#Class that solve the problem described on the aproach 1
class Problem:

    def __init__(self, input = "input.txt", output = "output.txt"):
        
        self.input = input
        self.output = output
        self.arc_input = None
        self.arc_output = None
        self.matrix = None
        self.matrixB = None

    #open the files and see if everything is okay 
    #raise an error if the file is not found
    def open_archives(self):
        try:
            self.arc_input = open(self.input, "r")
            self.arc_output = open(self.output, "w")
            print("Successful!")
            return True
        except FileNotFoundError:
            print("Archive input.txt not found!")
            return False

    #read all the values and store to be used later, see if everything is on the pattern described        
    def readMatrix(self):

        m, n = self.arc_input.readline().split(' ')
        m = int(m)
        n = int(n)

        self.matrix = intervalMatrix(m, n)
        self.matrixB = intervalMatrix(1, m)

        for line in range(0, m):
            for col in range(0, n):
                initial, end = self.arc_input.readline().split(' ')
                initial = int(initial)
                end = int(end)
                self.matrix.set_element(line, col, initial, end)     

        for line in range(0, m):
            initial, end = self.arc_input.readline().split(' ')
            initial = int(initial)
            end = int(end)
            self.matrixB.set_element(line, 0, initial, end)

        self.arc_input.close()
        
    #solve the given problem using PULP
    def solve(self):

        var = []
        for x in range(0, self.matrix.get_columns()): 
            var.append(pulp.LpVariable('x' + str(x+1), cat='Continuous'))

        min = pulp.LpProblem('intro', pulp.LpMinimize)
        max = pulp.LpProblem('intro', pulp.LpMaximize)

        for row in range(0,  self.matrix.get_lines()):
            for i in itertools.product(['initial','end'], repeat=self.matrix.get_columns()):
                aux2 = 0
               
                #lembrar de usar getter and setter aproriadamente
                for col in range(0, self.matrix.get_columns()):
                    aux2 += (self.matrix.get_matrix()[row][col][i[col]]*var[col])
                    print(self.matrix.get_matrix()[row][col][i[col]], var[col])

                min += (aux2 <= self.matrixB.get_element(row, 0)['end'])
                min += (aux2 >= self.matrixB.get_element(row, 0)['initial'])
                max += (aux2 <= self.matrixB.get_element(row, 0)['end'])
                max += (aux2 >= self.matrixB.get_element(row, 0)['initial'])

        for x in range(0, self.matrix.get_columns()):
            min += var[x]
            min.solve()
            self.arc_output.write('x' + str(x + 1) + ': ['  + str(var[x].value()) + ', ')
            max += var[x]
            max.solve()
            self.arc_output.write(str(var[x].value()) + ']\n')
      
        self.arc_output.close()

#Class that solve the exercise on the approach 4
class Problem2:

    def __init__(self, input = "input.txt", output = "output.txt"):
        self.input = input
        self.output = output
        self.arc_input = None
        self.arc_output = None
        self.matrix = intervalMatrix()
        self.matrixB = intervalMatrix()

    #objective function, we need to minimize each variable
    def fun(self, x, i):
        return x[i]
    
    #objective function, we need to minimize each variable
    def less_fun(self, x, i):
        return -x[0]

    #open the files and raise an error if the file is not found
    def open_archives(self):

        try:
            self.arc_input = open(self.input, "r")
            self.arc_output = open(self.output, "w")
            print("Successful!")
            return True
        except FileNotFoundError:
            print("input file not found!")
            return False
            
    #read all tha values and store to be used later
    def readMatrix(self):

        m, n = self.arc_input.readline().split(' ')
        m = int(m)
        n = int(n)

        self.matrix = intervalMatrix(m, n)
        self.matrixB = intervalMatrix(1, m)

        for line in range(0, m):
            for col in range(0, n):
                initial, end = self.arc_input.readline().split(' ')
                initial = int(initial)
                end = int(end)
                self.matrix.set_element(line, col, initial, end)     


        for line in range(0, m):
            initial, end = self.arc_input.readline().split(' ')
            initial = int(initial)
            end = int(end)
            self.matrixB.set_element(line, 0, initial, end)

        self.arc_input.close()

    #return the constraints to be used on scipy optimize
    def constraints(self, x, line):

        sum = 0
        aux = 0

        aux_list = []

        for j in range(0, self.matrix.get_columns()):
            aux_list.append(x[j])

        for i in range(self.matrix.get_columns() + line*self.matrix.get_columns(), line*self.matrix.get_columns() + 2*self.matrix.get_columns()):
            sum += x[i]*aux_list[aux]
            aux+=1

        sum -= x[6]

        return sum


    #solve the problem using scipy optimize
    def solve(self):
 
        #list with the constraints 
        con = []

        #adding constraints 
        for i in range(0, self.matrix.get_lines()):
            con.append({'type': 'eq', 'fun': lambda x: self.constraints(x, i)})

        print(con)
        bnds = [(self.matrix.get_element(i, j)['initial'], self.matrix.get_element(i, j)['end']) for i in range(0, self.matrix.get_lines()) for j in range(0, self.matrix.get_columns())]
       
        for x in range(0, self.matrix.get_columns()):
            bnds.insert(0, (None, None))
        
        for line in range(0, self.matrix.get_lines()):
            bnds.append((self.matrixB.get_element(line, 0)['initial'], self.matrixB.get_element(line, 0)['end']) )

        print(bnds)

        #generating some initial values 
        x0 = np.full((1, len(bnds)), 1)

        for element in range(0, self.matrix.get_columns()):
            res = optimize.minimize(self.fun, x0, options={'disp': False}, bounds=bnds, args=element)
            x = res.x
            self.arc_output.write('x' + str(element + 1) + ': ['  + str(x[element]) + ', ')
            res = optimize.minimize(self.less_fun, x0, options={'disp': False}, bounds=bnds, args=element)
            x = res.x
            self.arc_output.write(str(x[element]) + ']\n')

        self.arc_output.close()

prob = Problem("input.txt")
if(prob.open_archives()):
    prob.readMatrix()
    prob.solve()
           
