import random
from operator import itemgetter

# I will keep a table of each product length so that when I cross over, I will only change the cities where the products are sold.
# For productA, if the element value is 0, it will be understood that the item is sold in the city of x1, if it is 1 x2, if 2 is x3, if 3 is x4, if 4 is x5.
# At the same time, the price of product A will be given for the city of x1 in index 0 of the priceA array.
# x2 = In the 1st index, that is, priceA or priceB.., the price in the city x2 for that product will be kept in the 1st index.
# this logic will be applied based on all products and cities.

priceA = [1, 4, 6, 4, 4]
priceB = [3, 8, 2, 5, 15]
priceC = [3, 12, 3, 5, 5]
priceD = [2, 6, 10, 2, 4]
priceE = [10, 5, 12, 6, 3]

allPrice = []
allPrice.append(priceA)
allPrice.append(priceB)
allPrice.append(priceC)
allPrice.append(priceD)
allPrice.append(priceE)
#print(allPrice)

# we do it randomly at the beginning to fill in how much of which product is sold in which city
# I will determine in which city I will sell each of the A, B, C, D, and E products as I divide the matching matrix by product

def createMatchMatrix():
    productA = []  # 30     length has to be 30, can't be more or less
    productB = []  # 40
    productC = []  # 20
    productD = []  # 40
    productE = []  # 20
    for i in range(40):
        if i < 30:
            productA.append(random.randint(0, 4))
            if i < 20:
                productC.append(random.randint(0, 4))
                productE.append(random.randint(0, 4))
        productB.append(random.randint(0, 4))
        productD.append(random.randint(0, 4))
    """ print(len(productA), "productA:", productA)
    print(len(productB), "productB:", productB)
    print(len(productC), "productC:", productC)
    print(len(productD), "productD:", productD)
    print(len(productE), "productE:", productE)"""
    allProduct = []
    allProduct.append(productA)
    allProduct.append(productB)
    allProduct.append(productC)
    allProduct.append(productD)
    allProduct.append(productE)
    return allProduct


def printMatrix(products):
    print("    x1     x2     x3     x4     x5")
    productName = ["A", "B", "C", "D", "E"]
    for i in range(5):
        print(productName[i], end="   ")
        for j in range(5):
            itemNum = products[i].count(j)
            print(itemNum, end="      ")
        print()




def findf2or3Rate(xn):
    difference = max(xn) - min(xn)
    f2rate = 0
    if difference == 0:
        f2rate = 0.2
    elif difference < 20 and difference > 0:
        f2rate = difference / 100
    return f2rate


def fitness(products,prices):
    #soft contrains
    fbase = 0 #Case 0: fbase calculation

    f2 = 0 #Case 2 variables
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    fx1base = 0
    fx2base = 0
    fx3base = 0
    fx4base = 0
    fx5base = 0 #Case 2 variables

    # Case 1: all cities visited
    flag = [0,0,0,0,0]
    f1 = 0
    for i in range(5):
        x1.append(products[i].count(0)) # calculation of parameters required for case 2
        x2.append(products[i].count(1))
        x3.append(products[i].count(2))
        x4.append(products[i].count(3))
        x5.append(products[i].count(4))
        fx1base = fx1base + x1[i] * prices[i][0]
        fx2base = fx2base + x2[i] * prices[i][1]
        fx3base = fx3base + x3[i] * prices[i][2]
        fx4base = fx4base + x4[i] * prices[i][3]
        fx5base = fx5base + x5[i] * prices[i][4] #end of case 2
        for j in range(5):
            p = prices[i][j] # case 0 fbase calculation
            itemNum = products[i].count(j)
            fbase = fbase + (p * itemNum) #case 0 fbase calculation
            if (products[i].count(j) > 0): #case 1 check
                flag[j] = 1

    if (flag.count(0) == 0): #case 1 check
        f1 = 100

    #Case 2: For each city, the same quantity of each product is sold

    f2 = f2 + fx1base * findf2or3Rate(x1)
    f2 = f2 + fx2base * findf2or3Rate(x2)
    f2 = f2 + fx3base * findf2or3Rate(x3)
    f2 = f2 + fx4base * findf2or3Rate(x4)
    f2 = f2 + fx5base * findf2or3Rate(x5)
   # Situation 3: A balanced amount of items sold in all cities (best case 30 items sold in all)
     #for this, let's create an array where we keep the total amount of products sold in all cities
    f3 = 0
    Cities = [sum(x1), sum(x2), sum(x3), sum(x4), sum(x5)]
    f3 = f3 + fbase * findf2or3Rate(Cities)
    print("fbase:", fbase)
    print("f1:", f1)
    print("f2:", f2)
    print("f3:", f3)
    return fbase + f1 + f2 + f3

test = createMatchMatrix()
printMatrix(test)
print(fitness(test,allPrice))
#generate solution
population = []
for i in range(1000):
    population.append(createMatchMatrix())

maxResult = 0
resultMatrix = []


for i in range(10000):
    ranked = []
    for item in population:
        ranked.append([fitness(item,allPrice),item])

    temp = ranked
    sorted(ranked, key=itemgetter(0))
    #print(f"=== Gen {i} best solutions ===")
    #print(ranked[len(ranked)-1][0]) #, printMatrix(ranked[len(ranked)-1][1])
    if maxResult < ranked[len(ranked)-1][0]:
        maxResult = ranked[len(ranked)-1][0]
        resultMatrix = ranked[len(ranked)-1][1]
    #cross-over:
    if ranked[len(ranked)-1][0] >= 1400:
        break
    bestStates = ranked[-100:-1]# I chose the genes to cross over from the top 100 matrices
    gens = []
    for g in bestStates:
        for i in range(5):
            for j in range(40):
                if i == 0 and j <30:
                    gens.append(g[1][i][j])
                elif i == 1 and j <40:
                    gens.append(g[1][i][j])
                elif i == 2 and j <20:
                    gens.append(g[1][i][j])
                elif i == 3 and j <40:
                    gens.append(g[1][i][j])
                elif i == 4 and j <20:
                    gens.append(g[1][i][j])
    newGen = []
    for _ in range(1000):
        A = []  # 30    length has to be 30, can't be more or less
        B = []  # 40
        C = []  # 20
        D = []  # 40
        E = []  # 20
        all = []
        for i in range(40):
            if i < 30:
                A.append(random.choice(gens))
                if i < 20:
                    if random.randint(0, 10) == 1:
                        C.append(1)  # mutation
                    else:
                        C.append(random.choice(gens))
                    if random.randint(0, 10) == 1:
                        E.append(0)  # mutation
                    elif random.randint(0, 10) < 3:
                        E.append(2) #mutation
                    else:
                        E.append(random.choice(gens))
            if random.randint(0, 10) == 1:
                B.append(4) # mutation
            else:
                B.append(random.choice(gens))
            D.append(random.choice(gens))
        all.append(A)
        all.append(B)
        all.append(C)
        all.append(D)
        all.append(E)
        newGen.append(all)
    population = newGen



print("The max gain found and the corresponding matrix.")
print("The max gain:", maxResult)
print(printMatrix(resultMatrix))



