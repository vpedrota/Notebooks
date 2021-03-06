## Description

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Here we have two files that is an exercise avaliable on: https://docs.google.com/document/d/1Psi2QpcCZ6imjuuEEbXjWa62oySUsPpQd--YRbe-BAQ/edit?usp=sharing

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; On the notebook there are a simple solution wihout verifications and the input requires you to enter using the keyboard.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Both of them find possible solutions to a interval linear algebraic system. The .py one requires an .txt file with the input matrices with the  pattern that you can see below.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; First, you need to enter the matrix dimensions, so the first line represents the matrix dimensions, line and columns respectively and for the next MxN lines after are the interval for each matrix position. After the MxN lines, you need to enter the B matrix, so the next N lines require N intervals. Given a txt file with that pattern the output will be on output.txt.

Sample:

```
2 2  // dimensions line  x  columns 
2 4 
-2 1 
-1 2 
2 4 
-2 2 
-2 2 
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; On the exercise we have two approaches that I am working on, and looking for the future that may I need to use this exercise for some another application I prepared the file to be used as a module. 

## Steps

### 1. Import as a module

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; With the ativ1.py file in the same folder as the file you want to code use ``` import ``` to this as a module.

```
import ativ1 as mod
```

### 2. Instantiate

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; You need instantiate an object of the problem that you want to work on. There are some options that you can choose when you instantiate the problem object, you can change the input and the output file depending how you pass as parameter the input or output file adresses.

```
sample = mod.Problem("input.txt", "another.txt")
```
```
sample = mod.Problem() //by deafult it will be input="input.txt", output="output.txt"
```
```
sample = mod.Problem(output="another.txt")
```
### 3. Read the data and see the output
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Now you can use the functions and you need to take care with some errors that can be raised, I will show some of them. First, you need to use the function ```open_archives()```

If the input file is not found it will raise an error. After that, you only need to call more two functions ```readMatriz()``` and ```solve()```, see the sample below

```
prob = Problem("input.txt")
if(prob.open_archives()):
    prob.readMatriz()
    prob.solve()
```
If want to solve like the problem on the aproach 4 you need to use the following sample

```
prob = Problem2("input.txt")
if(prob.open_archives()):
    prob.readMatriz()
    prob.solve()
```


