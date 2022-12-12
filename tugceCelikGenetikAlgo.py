import random
from operator import itemgetter

#her bir ürün uzunluğunda tablo tutucam bu sayede cross over yaptığımda sadece ürünlerin satıldığı şehirleri değiştireceğim
#productA için eleman değeri 0 ise o elemanın x1 şehrinde satıldığı anlaşılacaktır, 1 ise x2, 2 ise x3, 3 ise x4, 4 ise x5.
#Aynı zamanda  priceA dizisinin 0 ıncı indexinde x1'in şehri için A ürününün fiyatı verilecektir.
#x2 = 1. index yani priceA veya priceB.. de 1. indexinde o ürün için x2 şehrindeki fiyat tutulacak
#bu mantık tüm ürünler ve şehirler bazında uygulanacaktır.

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

#hangi ürünün hangi şehirde ne kadar satıldığını doldurmayı başlangıçta random olarak yapıyoruz
#ben eşleştirme matrisini ürün bazında böldüğüm için A,B,C,D,E ürünlerinin her birini hangi şehirde satacağımı belirleyeceğim

def createMatchMatrix():
    productA = []  # 30     uzunluğu 30 olmak zorunda fazla ya da az olamaz
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
    fbase = 0 #Durum 0: fbase hesabı

    f2 = 0 #Durum 2  değişkenleri
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    fx1base = 0
    fx2base = 0
    fx3base = 0
    fx4base = 0
    fx5base = 0 #Durum 2 değişkenleri

    #Durum 1: tüm şehirlerin ziyaret edilmesi
    flag = [0,0,0,0,0]
    f1 = 0
    for i in range(5):
        x1.append(products[i].count(0)) #durum 2 için gereken parametrelerin hesabı
        x2.append(products[i].count(1))
        x3.append(products[i].count(2))
        x4.append(products[i].count(3))
        x5.append(products[i].count(4))
        fx1base = fx1base + x1[i] * prices[i][0]
        fx2base = fx2base + x2[i] * prices[i][1]
        fx3base = fx3base + x3[i] * prices[i][2]
        fx4base = fx4base + x4[i] * prices[i][3]
        fx5base = fx5base + x5[i] * prices[i][4] #durum 2 sonu
        for j in range(5):
            p = prices[i][j] #durum 0 fbase hesabı
            itemNum = products[i].count(j)
            fbase = fbase + (p * itemNum) #durum 0 fbase hesabı
            if (products[i].count(j) > 0): #durum 1 kontrolu
                flag[j] = 1

    if (flag.count(0) == 0): #durum 1 kontrolu
        f1 = 100

    #Durum 2: Her bir şehir için, Her üründen aynı miktarda satılması

    f2 = f2 + fx1base * findf2or3Rate(x1)
    f2 = f2 + fx2base * findf2or3Rate(x2)
    f2 = f2 + fx3base * findf2or3Rate(x3)
    f2 = f2 + fx4base * findf2or3Rate(x4)
    f2 = f2 + fx5base * findf2or3Rate(x5)
    # Durum 3: Tüm şehirlerde dengeli miktarda ürün satılması durumu (en iyi durum hepsinde 30 ürün satılması)
    #bunun için tüm şehirlerde satılan toplam ürün miktarlarını tuttuğumuz bir dizi oluşturalım
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
    bestStates = ranked[-100:-1] #cross over yapılacak genleri en iyi 100 matristen seçtim
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
        A = []  # 30     uzunluğu 30 olmak zorunda fazla ya da az olamaz
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



