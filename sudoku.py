# -*- coding: utf-8 -*-
from collections import defaultdict
import math
import itertools
import time
import argparse

#parser.add_argument('--foo', help='foo help')

row = "ABCDEFGHI"
col = "123456789"

class csp:
    	
	def __init__(self, variables, domains, constraints):
		self.variables = variables
		self.domains = domains
		self.constraints = constraints
	
	def solved(self):
		return not any(len(self.domains[var])!=1 for var in self.variables)
	
	def __str__(self):
		output=""
		for i in range(0,9):
			if(i%3==0 and i!=0):
				output+=("- - - + - - - + - - - \n")
			for j in range(0,9):
				var="ABCDEFGHI"[i]+"123456789"[j]
				if(j%3==0 and j!=0):
					output+="| "
				if len(self.domains[var])==1:
					value=self.domains[var].pop()
					output+=str(value) + " "
					self.domains[var].add(value)
				else:
					output+='X '
			output+="\n"
		return(output)

def AC3 (csp, queue=None):
 	
	def arc_reduce(x,y):
		removals=[]
		change=False
		for vx in csp.domains[x].copy():
			found=False

			for vy in csp.domains[y]:
				if diff(vx,vy):
					found=True
			if(not found):
				csp.domains[x].remove(vx)	
				removals.append((x,vx))
				change=True

		return change,removals
	removals=[]
	
	if queue is None:
		queue=[]
		for x in csp.variables:
			queue = queue + [(x, y) for y in csp.constraints[x]]

	while queue:
		x,y= queue.pop()

		b,r=arc_reduce(x,y)
		
		if r:
			removals.extend(r)
		if(b):
    		#nao é arc consistente
			if(len(csp.domains[x])==0):
				return False, removals
			#Checar vizinhança ao remover valores
			else:
				queue = queue + [(x, z) for z in csp.constraints[x] if z!=y]

	return True, removals

def diff(x,y):
	return (x!=y)

def readCSPFromFile(pathToFile):
	#returno de todas as restrições binárias que contem variaveis
	
	def constraints(x, listOfNeighbours):
    	# {y : xRy}
		constrain_to = set()
		for pair in listOfNeighbours:
			if x in pair:
				if x==pair[0]:
					constrain_to.add(pair[1])
				elif x==pair[1]:
					constrain_to.add(pair[0])
		return constrain_to

	#ler o sukoku para a segunda lista
	
	with open(pathToFile) as file:
		matrix = [[int(x) if x.isdigit() else 0 for x in line.strip() if x.isdigit() or x=="X"] for line in file if "-" not in line]
	
	neighbours=[]
	for r in "ABCDEFGHI":
		row = [r+c for c in "123456789"]
		neighbours.extend(itertools.combinations(row, 2))

	for c in "123456789":
		col = [r+c for r in "ABCDEFGHI"]
		neighbours.extend(itertools.combinations(col, 2))
	
	for y in range(0,9,3):
		for x in range(0,9,3):
			box=["ABCDEFGHI"[i+y]+"123456789"[x+j] for i in range(0,3) for j in range(0,3)]
			neighbours.extend(itertools.combinations(box, 2))

	# Listagem de string:"A1", "A2",... "I9"
	variables = [x+y for x in "ABCDEFGHI" for y in "123456789"]
	
	# Dicionario {Variavel : Dominio(Variavel)}
	domains={"ABCDEFGHI"[y]+"123456789"[x]:{1,2,3,4,5,6,7,8,9} if matrix[y][x]==0 else {matrix[y][x]} for y in range(0,9) for x in range(0,9)}
	
	constraints = {x:constraints(x, neighbours) for x in variables}
	
	return csp(variables,domains,constraints)

def selectUnassignedVariable(csp,assigned):
	for var in csp.variables:
		if var not in assigned: return var

#sem ordenação
def OrderDomainValues(csp, assignment, var):
	values = [val for val in csp.domains[var]] 
	return values

def backTrackingSearch(csp): #retorna solução ou falha
	return backtrack({},csp)


def backtrack(assignment, csp): #retorna solução ou falha
	if csp.solved():
		return csp

	var = selectUnassignedVariable(csp, assignment)
	
	for value in OrderDomainValues(csp, assignment, var):
    	
		assignment[var] = value

		removals = [(var, a) for a in csp.domains[var] if a != value]
		
		#Assumir que Var = Value => D(Var) = Value
		csp.domains[var] = {value}

		consistent, removed = AC3(csp, [(x,var) for x in csp.constraints[var]])
		#Se valores forem removidos pelo AC3, adivionar a lista para ser restaurados
		if removed:
			removals.extend(removed)
		
		#Se AC3 consistente
		if(consistent):
			#continue a busca
			result = backtrack(assignment,csp)
			#Se não houver falha, retornar a solução.
			if(result!=False):
				return result
		
		#Se o CSP nao for AC3 consistente, restaures os valores removidos pela inferencia
		for variable, value in removals:
			csp.domains[variable].add(value)

	#Incapaz de  encontrar solução disponível para  este caminho, retornar um passo e tentar caminho diferente
	del assignment[var]
	return False

parser = argparse.ArgumentParser(description='Sudoku Solver')
parser.add_argument("file_path")
parser.parse_args()

def main():
	args = parser.parse_args()
	Sudoku = readCSPFromFile(args.file_path)

	print("Sudoku Inicial: {}\n".format(args.file_path))
	print(Sudoku)
	print(30*'-')
	AC3(Sudoku)

	print("Tentativa com AC-3 \n")
	
	if(Sudoku.solved()):
		print("Solução Sudoku com apenas o método AC-3: ")
		print(Sudoku)
	else:
		print("Sudoku parcialmente resolvido por AC-3")
		print(Sudoku)
		
		print("Tentando pelo método de backtracking...")
		solution = backTrackingSearch(Sudoku)
		
		if(solution):
			print("Solução encontrada por backtracking: \n")
			print(solution)
		else:
			print("A busca backtrack  não conseguiu encontrar a solução.")

if __name__ == "__main__":
	main()