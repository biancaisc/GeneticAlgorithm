import math
import random
import copy

f = open("input.in", "r")
g = open("output.out", "w")

# Citirea datelor

nrCromozomi = int(f.readline().strip())
interval = f.readline().strip().split()
capat1, capat2 = int(interval[0]), int(interval[1])

functie = f.readline().strip().split()
a, b, c = int(functie[0]), int(functie[1]), int(functie[2])

precizie = int(f.readline().strip())

probRecomb = int(f.readline().strip())/100
probMutatie = int(f.readline().strip())/100

nrEtape = int(f.readline().strip())

lungime = math.ceil(math.log2((capat2 - capat1)* 10**precizie))
discretizare = (capat2 - capat1)/(2**lungime)

x =[]
cromozomi = []
fit = []
probabilitati = []
evolutie = []
xmax = []
medie = []
ok = 0


def function(x):
    return a*x**2 + b*x + c

def binToDec(nrBinar):
    interval = int(nrBinar, 2)
    return a + interval*discretizare

def decToBin(nrDec):
    interval = math.floor((nrDec - a) / discretizare)
    reprez = format(interval, '0{}b'.format(lungime))
    return reprez

def generate():
    u = []
    for _ in range(nrCromozomi):
        nr = random.random()
        u.append(nr)
    return u

def binaryS(interval, x):
    left = 0
    right = len(interval) - 1

    while left <= right:
        mid = (left + right) // 2

        if interval[mid] <= x < interval[mid + 1]:
            return mid
        elif x < interval[mid]:
            right = mid - 1
        else:
            left = mid + 1

def recombinare(a, b, pos):
    auxa, auxb = a[:pos], b[:pos]
    newa = auxb + a[pos:]
    newb = auxa + b[pos:]
    return newa, newb


for _ in range(nrEtape):

    mostFit = float('-inf')
    worstFit = float('inf')

    if ok == 0:
       # generez codificarile
      for _ in range(nrCromozomi):
         nr = random.uniform(-1, 2)
         numar_formatat = "{:.{}f}".format(nr, precizie)
         x.append(float(numar_formatat))

      for i in range(nrCromozomi):
        reprez = decToBin(x[i])
        cromozomi.append(reprez)
        fitResult = function(x[i])
        fit.append(fitResult)


    if ok == 0:
        for i in range(1, nrCromozomi+1):
            g.write(f"{i}   {cromozomi[i - 1]}   {x[i - 1]}   {fit[i - 1]}\n")
        g.write("\n")

     # Selectia

    fitTotal = sum(fit)
    probabilitati = []

    for i in range(nrCromozomi):
        nr = fit[i]/fitTotal
        probabilitati.append(nr)

        fitValue = fit[i]
        if fitValue > mostFit:
            mostFit = fitValue
            pozMostFit = i

    mostFitCrom = cromozomi[pozMostFit]
    mostFitCromX = x[pozMostFit]

    if(ok == 0):
        for i in range(1, nrCromozomi+1):
            g.write(f"cromozom   {i}   probabilitate   {probabilitati[i - 1]}\n")

    intervale = []
    intervale.append(0)

    for i in range(1, nrCromozomi):
        intervale.append(intervale[i-1] + probabilitati[i-1])

    intervale.append(1)

    if(ok == 0):
        g.write("Intervale probabilitati selectie\n")
        g.write(" ".join([str(nr) for nr in intervale]))
        g.write("\n")

    u = generate()
    pozitii = []

    for i in u:
        pos = binaryS(intervale,i)
        pozitii.append(pos)
        if ok == 0:
            g.write(f"u = {i}  selectam cromozomul {pos + 1}\n")
    if ok == 0:
        g.write("Dupa selectie:\n")

    newCromozomi = []
    newX = []
    newfit = []
    for i,pos in enumerate(pozitii):
        newCromozomi.append(cromozomi[pos])
        newX.append(x[pos])
        newfit.append(fit[pos])

        if ok == 0:
            g.write(f"{i+1} {cromozomi[pos]} x={x[pos]} f={fit[pos]}\n")


    if ok == 0:
        g.write("Probabilitatea de incrucisare 0.25\n")

    u = generate()
    recomb = []
    for i in range(nrCromozomi):
        if u[i] < probRecomb:
            recomb.append(i)
            if ok == 0:
                g.write(f"{i + 1}  {newCromozomi[i]}  u={u[i]} <0.25 participia\n")
        else:
            if ok == 0:
                g.write(f"{i+1} {newCromozomi[i]}  u={u[i]}\n")


    # Recombinarea

    for i in range(0,len(recomb),2):
            if i == len(recomb)-1:
                break
            crom1 = newCromozomi[recomb[i]]
            crom2 = newCromozomi[recomb[i+1]]
            punct = random.randint(0, 21)

            newcrom1, newcrom2 = recombinare(crom1, crom2, punct)

            aux1 = newcrom1[:punct + 1] + "|" + newcrom1[punct + 1:]
            aux2 = newcrom2[:punct + 1] + "|" + newcrom2[punct + 1:]

            auxcrom1 = crom1[:punct + 1] + "|" + crom1[punct + 1:]
            auxcrom2 = crom2[:punct + 1] + "|" + crom2[punct + 1:]



            if ok == 0:
                g.write(f"Recombinare dintre cromozomul {recomb[i] + 1} cu cromozomul {recomb[i+1]+1}\n")
                g.write(f"         {auxcrom1}   {auxcrom2}    punct {punct}\n")
                g.write(f"Rezultat {aux1}   {aux2}\n")

            newCromozomi[recomb[i]] = newcrom1
            newX[recomb[i]] = round(binToDec(newcrom1), precizie)
            newfit[recomb[i]] = function(x[recomb[i]])


            newCromozomi[recomb[i + 1]] = newcrom2
            newX[recomb[i+1]] = round(binToDec(newcrom2), precizie)
            newfit[recomb[i+1]] = function(x[recomb[i+1]])

    # Dupa recombinare


    if ok == 0:
        g.write("Dupa recombinare:\n")
        for i in range(nrCromozomi):
            g.write(f"{i + 1}  {newCromozomi[i]} x={newX[i]}  f={newfit[i]}\n")

    if ok == 0:
        g.write(f"Probabilitate de mutatie pentru fiecare gena {probMutatie}\n")
        g.write("Au fost modificati cromozomii: \n")

    before = []
    after = []
    afterpoz = []
    for i in range(nrCromozomi):
        prob = random.random()
        if prob < probMutatie:
                poz = random.randrange(lungime)
                afterpoz.append(poz)
                before.append(newCromozomi[i])
                if newCromozomi[i][poz] == '0':
                    newCromozomi[i] = newCromozomi[i][:poz] + '1' + newCromozomi[i][poz + 1:]


                else:
                    newCromozomi[i] = newCromozomi[i][:poz] + '0' + newCromozomi[i][poz + 1:]

                after.append(newCromozomi[i])


                newX[i] = binToDec(newCromozomi[i])
                newfit[i] = function(newX[i])
                if ok == 0:
                    g.write(f"{i+1}\n")


    # if ok == 0:
    #     auxiliar = []
    #     for i in range(len(before)):
    #         g.write(f"{before[i]}\n")

    #         for j in range(len(lungime)):
    #             if i != afterpoz[j]:
    #                 auxiliar.append(" ")
    #             else:
    #                 auxiliar.append("*")
    #         g.write()



    if ok == 0:
        g.write("Dupa mutatie:\n")

        for i in range(nrCromozomi):
            g.write(f"{i + 1}  {newCromozomi[i]} x={newX[i]}  f={newfit[i]}\n")


    for i in range(nrCromozomi):
            if newfit[i] < worstFit:
                worstFit = newfit[i]
                pozWorstFit = i

    # schimb cel mai rau cu cel mai bun
    if worstFit < mostFit:
        newCromozomi[pozWorstFit] = mostFitCrom
        newX[pozWorstFit] = mostFitCromX
        newfit[pozWorstFit] = mostFit

    var = max(newX)
    var = round(var, precizie)
    xmax.append(var)

    maxim = max(newfit)
    evolutie.append(maxim)

    var2 = sum(newfit)/len(newfit)
    medie.append(var2)

    cromozomi = copy.deepcopy(newCromozomi)
    x = copy.deepcopy(newX)
    fit = copy.deepcopy(newfit)

    ok = 1

g.write("\n")
for i in (range(len(evolutie))):
    g.write(f"{str(evolutie[i])}  x={str(xmax[i])}   fitMediu={str(medie[i])}\n")