# This code generally gives the core this system to work
import numpy as np 
from cvxpy import * 


def optim(Nutritional_need ,Nutrition_matrix, cost, lam, upper_constraints = 0, addition_feature =[]):
	#Nutritional_need is the need for each person
	#Nutrition_matrix is a matrix with nutrition values as its entries 
	#cost is the monetary cost of each of the nutrition 
	#lam is relative weights of each of ingredients
	#Upper_constraints is the amount of ingredients already in the each of the value 
	#Additional Features are addtional features this is a list of functions which returns cvxpy

	N = Nutritional_need.size 
	M = len(addition_feature)
	Amount = Variable(N)
	#Exception Clauses ////
	Nut = Nutrition_matrix*Amount

	V = lam[0]*sum_squares(Nutrition_matrix*Amount - Nutritional_need) * lam[1]*norm(Amount,1)+ lam[2]*kron(Amount,cost)
	if M != 0:
		for i in range(M):
			V = lam[(3+i)]*addition_feature[i](Amount)

	Prob = Problem(Minimize(V), Amount>= upper_constraints)
	Prob.solve()
	return([Amount, Nut])
