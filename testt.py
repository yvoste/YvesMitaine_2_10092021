import random


m = 0

n = 0


for i in range(5):

    listeDe = []

    j = 0

    

    while j < 10000:

        listeDe.append(random.randint(1, 6))

        j += 1

        

    sousEchantillonDe = random.sample(listeDe, 1000)

    

    m += listeDe.count(6)/10000

    n += sousEchantillonDe.count(4)/1000

    

print("m =", m/5, "et n =", n/5)