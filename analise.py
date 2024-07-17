import numpy
from tabulate import tabulate
import matplotlib.pyplot as plt

class Teste:
    def __init__(self, niter:int, npop:int, c1:float, c2:float, melhores:list):
        self.npop = npop
        self.niter = niter
        self.c1 = c1
        self.c2 = c2
        self.melhores = melhores
        self.media = numpy.mean(self.melhores)
        self.desvio = numpy.std(self.melhores)
    

testes = list()

for i in range(1,19):
    file_path = "testes/instancia/teste" + str(i) + ".txt"
    npop = numpy.loadtxt(file_path, delimiter=';', skiprows=0, max_rows=1, dtype=int)
    niter = numpy.loadtxt(file_path, delimiter=';', skiprows=1, max_rows=1, dtype=int)
    c1 = numpy.loadtxt(file_path, delimiter=';', skiprows=2, max_rows=1, dtype=float)
    c2 = numpy.loadtxt(file_path, delimiter=';', skiprows=3, max_rows=1, dtype=float)
    melhores = numpy.loadtxt(file_path, delimiter=';', skiprows=5, dtype=float)
    teste = Teste(niter, npop, c1, c2, melhores)
    testes.append(teste)


testes = sorted(testes, key=lambda teste: teste.media, reverse=False)
    
data = []
for teste in testes:
    t = [teste.niter, teste.npop, teste.c1, teste.c2, teste.media, teste.desvio]
    data.append(t)

print(tabulate(data, headers=['Iterações', 'População', 'C1', 'C2', 'Media', 'Desvio'], tablefmt='orgtbl'))

data_melhor = numpy.loadtxt("testes/instancia/arquivo_saida.txt", delimiter=';', skiprows=1, dtype=float)

y = [[],[],[],[]]
for d in data_melhor:
    y[0].append(d[0])
    y[1].append(d[1])
    y[2].append(d[2])
    y[3].append(d[3])

plt.plot(y[0], label="Melhor")
plt.plot(y[1], label="Pior")
plt.plot(y[2], label="Média")
plt.plot(y[3], label="Desvio")
plt.xlabel("Iteração")
plt.ylabel("Aptidão")
plt.legend()
plt.show()

execucoes_melhor = numpy.genfromtxt("testes/instancia/teste_melhor.txt", delimiter=';', dtype=None)

gf_execucoes = plt.subplot()
gf_execucoes.set_xlabel("Iterações")
gf_execucoes.set_ylabel("Aptidão")

for i in range(1,11):
    ex = [exec[1] for exec in execucoes_melhor if (exec[0] == i)]
    gf_execucoes.plot(ex, label=("Execução" + str(i)))

plt.legend()
plt.show()