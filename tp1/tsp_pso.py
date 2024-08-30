import random
import numpy
import numpy.random as npr
import sys

class Grafo:
    def __init__(self, num_cidades:int, distancias:list):
        self.num_cidades = num_cidades
        self.distancias = distancias

    def gera_solucao_aleatoria(self) -> list:
        #considerando um grafo completo
        cidades = list(range(0,self.num_cidades))
        return npr.permutation(cidades)
    
    def calcula_fitness(self, solucao) -> float:
        fitness = 0
        for i in range(self.num_cidades):
            fitness += self.distancias[solucao[i-1]][solucao[i]]
        return fitness
    
class Particula:
    def __init__(self, solucao:list, fitness:float):
        self.solucao = solucao
        self.fitness = fitness
        self.melhor_pessoal = solucao.copy()
        self.fitness_melhor_pessoal = fitness
        self.velocidade = []

    def set_nova_solucao(self, nova_solucao:list, fitness:float):
        self.solucao = nova_solucao
        self.fitness = fitness

    def set_novo_melhor_pessoal(self, novo_melhor_pessoal:list, fitness:float):
        self.melhor_pessoal = novo_melhor_pessoal
        self.fitness_melhor_pessoal = fitness

    def set_velocidade(self, velocidade):
        self.velocidade = velocidade

class Pso:
    def __init__(self, grafo:Grafo, tamanho_populacao:int, iteracoes:int, c1:float, c2:float):
        self.grafo = grafo
        self.tamanho_populacao = tamanho_populacao
        self.iteracoes = iteracoes
        self.c1 = c1
        self.c2 = c2

        self.particulas = []

        for i in range(self.tamanho_populacao):
            solucao = self.grafo.gera_solucao_aleatoria()
            fitness = self.grafo.calcula_fitness(solucao)
            particula = Particula(solucao, fitness)
            self.particulas.append(particula)

        self.melhor_global = min(self.particulas, key = lambda p : p.fitness)

    def set_melhor_global(self, melhor_global:Particula):
        self.melhor_global = melhor_global

    def get_melhor_global(self) -> Particula:
        return self.melhor_global
    
    def rodar_algoritmo(self):

        for loop in range(self.iteracoes):
            for particula in self.particulas:
                if (particula.fitness < particula.fitness_melhor_pessoal):
                    particula.set_novo_melhor_pessoal(particula.solucao, particula.fitness)

                if particula.fitness < self.melhor_global.fitness:
                    self.set_melhor_global(particula)

                particula.velocidade = []
                velocidade_temp = []

                solucao_global = list(self.melhor_global.solucao)
                solucao_pessoal = list(particula.melhor_pessoal)
                solucao_atual = list(particula.solucao)
                
                for i in range(self.grafo.num_cidades):
                    if (solucao_atual[i] != solucao_pessoal[i]):
                        transposicao = (i, solucao_pessoal.index(solucao_atual[i]))
                        velocidade_temp.append(transposicao)

                r1 = random.random()
                cr1 = round(r1 * self.c1)
                if (len(velocidade_temp) > cr1):
                    velocidade_temp = random.sample(velocidade_temp, cr1)
                
                particula.velocidade.extend(velocidade_temp)
                velocidade_temp = []

                for i in range(self.grafo.num_cidades):
                    if (solucao_atual[i] != solucao_global[i]):
                        transposicao = (i, solucao_global.index(solucao_atual[i]))
                        velocidade_temp.append(transposicao)

                r2 = random.random()
                cr2 = round(r2 * self.c2)
                if (len(velocidade_temp) > cr2):
                    velocidade_temp = random.sample(velocidade_temp, cr2)

                particula.velocidade.extend(velocidade_temp)

                for transposicao in particula.velocidade:
                    aux = particula.solucao[transposicao[0]]
                    particula.solucao[transposicao[0]] = particula.solucao[transposicao[1]]
                    particula.solucao[transposicao[1]] = aux

                particula.fitness = self.grafo.calcula_fitness(particula.solucao)
                
            print(f"Melhor Fitness: {self.melhor_global.fitness}")
            

def ler_arquivo(file_path:str) -> Grafo:
    num_cidades = numpy.loadtxt(file_path, delimiter=' ', skiprows=0, max_rows=1, dtype=int)
    cordenadas = numpy.loadtxt(file_path, delimiter=' ', skiprows=1, dtype=int)

    distancias = list()

    for i in range(num_cidades):
        dist = list()
        for j in range(num_cidades):
            xd = cordenadas[i][0] - cordenadas[j][0]
            yd = cordenadas[i][1] - cordenadas[j][1]
            dist.append(numpy.sqrt((xd * xd) + (yd * yd)))
        distancias.append(dist)

    grafo = Grafo(num_cidades, distancias)
    return grafo


file_path = sys.argv[1]
tamanho_populacao = int(sys.argv[2])
iteracoes = int(sys.argv[3])
c1 = float(sys.argv[4])
c2 = float(sys.argv[5])

grafo = ler_arquivo(file_path)
sol = grafo.gera_solucao_aleatoria()
fit = grafo.calcula_fitness(sol)

pso = Pso(grafo, tamanho_populacao, iteracoes, c1, c2)
pso.rodar_algoritmo()
print("Melhor = ", pso.get_melhor_global().solucao)