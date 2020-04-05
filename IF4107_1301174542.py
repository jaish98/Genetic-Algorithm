from numpy.random import randint
from random import random

################################################################################################################
Jumlah_Populasi = 10
Start_Rule_Count = 4
Prob_M = 0.02
loop = 6000
################################################################################################################

def Populasi(kesehatan, individu):
    return (kesehatan[individu] / sum(kesehatan))

def Fitness(individu, datalatih):
    benar = 0;
    for i in range(0, len(datalatih)):
        ans = jawab(individu, datalatih[i]);
        if (ans == datalatih[i][14]):
            benar += 1;

    return benar / len(datalatih);


def jawab(individu, question):
    answer = -1;
    for rule in range(0, int(len(individu) / 15)):
        isValid = True;

        for j in range(0, (len(question) - 1)):
            if (question[j] == 1 and individu[(rule * 15) + j] != 1):
                isValid = False;
                break;

        if (isValid):
            answer = rule
            break;

    if (answer == -1):
        return int(individu[len(individu) - 1] == 0);
    else:
        return individu[answer * 15 + 14];


def Crossover1(parent, anak, titik1, titik2):
    for i in range(titik2[0], titik2[1] + 1):
        anak.pop(titik2[0]);

    for i in range(titik1[0], titik1[1] + 1):
        anak.insert(titik2[0] + (i - titik1[0]), parent[0][i]);

    return anak;


def Crossover2(parent, anak, titik2):
    for i in range(titik2[0], titik2[1] + 1):
        anak[i] = parent[1][i];
    return anak;


def Mutation(individu):
    for ind in range(0, len(individu)):
        if (random() <= Prob_M):
            individu[ind] = int(individu[ind] == 0);

    return individu


def ParentSelection(kesehatan):
    individu = 0
    rand = random() * sum(kesehatan);
    while 0 < rand:
        rand -= kesehatan[individu];
        individu += 1

    return individu - 1


# Fungsi untuk load data latih
def load(fileLok):
    arrlatih = loadText(fileLok);
    latih = [ubahKeBiner(data) for data in arrlatih];
    return latih;


# Fungsi untuk load data
def loadText(fileLok):
    f = open(fileLok, "r");
    dataString = [];
    kalimat = f.readline();
    while (kalimat != ""):
        kalimat = kalimat.replace("\n", "")
        dataString.append(kalimat);
        kalimat = f.readline();
    f.close();
    return dataString;


def ubahKeBiner(Kalimat):
    arrKalimat = Kalimat.split("\t");
    gen = [0] * 15
    if (arrKalimat[0].upper() == "NORMAL"):
        gen[0] = 1;
    elif (arrKalimat[0].upper() == "RENDAH"):
        gen[1] = 1;
    elif (arrKalimat[0].upper() == "TINGGI"):
        gen[2] = 1;

    if (arrKalimat[1].upper() == "PAGI"):
        gen[3] = 1;
    elif (arrKalimat[1].upper() == "SIANG"):
        gen[4] = 1;
    elif (arrKalimat[1].upper() == "SORE"):
        gen[5] = 1;
    elif (arrKalimat[1].upper() == "MALAM"):
        gen[6] = 1;

    if (arrKalimat[2].upper() == "HUJAN"):
        gen[7] = 1;
    elif (arrKalimat[2].upper() == "BERAWAN"):
        gen[8] = 1;
    elif (arrKalimat[2].upper() == "CERAH"):
        gen[9] = 1;
    elif (arrKalimat[2].upper() == "RINTIK"):
        gen[10] = 1;

    if (arrKalimat[3].upper() == "NORMAL"):
        gen[11] = 1;
    elif (arrKalimat[3].upper() == "RENDAH"):
        gen[12] = 1;
    elif (arrKalimat[3].upper() == "TINGGI"):
        gen[13] = 1;

    if (len(arrKalimat) == 5 and arrKalimat[4].upper() == "YA"):
        gen[14] = 1;
    else:
        gen[14] = 0;
    return gen;


def Buatindividuvidu():
    return randint(0, 2, 15 * randint(1, Start_Rule_Count))


def switch(x):
    temp = x[0];
    x[0] = x[1];
    x[1] = temp;

def PanjangOrtu(idx):
    return len(populasi[idx]);

def randomTitik(ortu):
    t = [0, 0];
    while (t[0] == t[1] or abs(t[0] - t[1]) < 4):
        t[0] = randint(0, len(ortu));
        t[1] = randint(0, len(ortu));

    if (t[0] > t[1]):
        switch(t);
    return t;


def randomTitik2(t):
    r = randint(0, 3) - 1;
    if (r == 0):
        return t;
    elif (r == -1):
        return [t[1] - 2, t[1]]
    else:
        return [t[0], t[0] + 2];


def duplicate(obj):
    items = []
    for item in obj:
        items.append(item);
    return items;


def cut(child):
    for c in child:
        cl = (len(c) % 15);
        if (cl != 0):
            for i in range(0, cl):
                c.pop();


def survivor(individu):
    min = 1;
    urutan = 0;
    myFit = Fitness(individu, latih);

    if (isExist(individu)):
        return;

    for i in range(0, len(fitness)):
        if (fitness[i] < min):
            min = fitness[i];
            urutan = i;
        elif (fitness[i] == min and random() < 0.3):
            urutan = i;

    if (myFit >= min):
        populasi[urutan] = individu;
        fitness[urutan] = myFit;


def isExist(child):
    exist = False;
    for individu in populasi:
        if (len(individu) == len(child)):
            exist = True;
            for i in range(0, len(child)):
                if (child[i] != individu[i]):
                    exist = False;
                    break;
        else:
            exist = False;
        if (exist):
            break;

    return exist;


def answerToString(ans):
    if (ans == 1):
        return "Terbang (1)";
    else:
        return "Tidak Terbang (0)";


###############################################################################################################
latih = load("data_latih_opsi_1.txt");
uji = load("data_uji_opsi_1.txt");

bestFit = 0;
bestindividu = [];

while bestFit < 0.8:
    print("Start Running, Best Fit : ", bestFit)
    populasi = [Buatindividuvidu() for i in range(0, Jumlah_Populasi)];
    fitness = [Fitness(individu, latih) for individu in populasi];
    if (bestFit != 0):
        survivor(bestindividu);
    for i in range(0, loop):
        ortu = [ParentSelection(fitness), ParentSelection(fitness)];
        while (ortu[1] == ortu[0]):
            ortu = [ParentSelection(fitness), ParentSelection(fitness)];
        if (PanjangOrtu(ortu[0]) > PanjangOrtu(ortu[1])):
            switch(ortu);
        titik = randomTitik(populasi[ortu[0]]);
        titik2 = randomTitik2(titik);
        child = [duplicate(populasi[ortu[0]]), duplicate(populasi[ortu[1]])];
        parent = [populasi[ortu[0]], populasi[ortu[1]]]
        child[1] = Crossover1(parent, child[1], titik, titik2);
        child[0] = Crossover2(parent, child[0], titik2);
        cut(child);
        child[0] = Mutation(child[0]);
        child[1] = Mutation(child[1]);
        survivor(child[0]);
        survivor(child[1]);
        maximum = -1;
        urutan = 0;
        minLen = 0;
        for j in range(0, len(fitness)):
            if (fitness[j] > maximum):
                maximum = fitness[j];
                urutan = j;
                minLen = len(populasi[j]);
            elif (fitness[j] == maximum):
                if (len(populasi[j]) < minLen):
                    urutan = j;
                    minLen = len(populasi[j]);
        bestindividu = populasi[urutan];
        bestFit = fitness[urutan];

print("Total Loop = ", i, ", Current Best Fit", 100 * fitness[urutan], "% Accuracy");
maximum = -1;
urutan = 0;
minLen = 1000;
for i in range(0, len(fitness)):
    if (fitness[i] > maximum):
        maximum = fitness[i];
        urutan = i;
        minLen = len(populasi[i])
    elif (fitness[i] == maximum):
        if (len(populasi[i]) < minLen):
            urutan = i;
            minLen = len(populasi[i])

print("Hasil Desision Tree :")
print(populasi[urutan]);
print("Fitness = " + str(maximum));
print("Rule = " + str(len(populasi[urutan]) / 15));
print("jawaban soal : ");
answer = [jawab(populasi[urutan], tes) for tes in uji]
stringA = [answerToString(ans) for ans in answer]

f.close()