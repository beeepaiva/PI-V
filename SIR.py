import random
import sys
import copy
random.seed(None)

# População de indivúduos suscetíveis, número de infectados, recuperados com imunidade e de mortos.

# Os recuperados com imunidade não podem ser reinfectados e não podem infectar outros. A mesma regra acima vale para os mortos.

# As seguintes características devem ser parametrizáveis:
# A taxa de infecção (probabilidade de um infectado infectar um indivíduo suscetível)
# A taxa de recuperação
# O tamanho do tabuleiro (quantidade de células)
# O tamanho de cada célula
# A taxa de mortalidade da infecção (probabilidade de um infectado morrer)

# A parametrização por ser através de atributos de classe, parâmetros de função ou variáveis, mas o ideal seria através de uma interface gráfica na tela da simulação.

# NODE
# Each node can be either:
# 1 = Susceptible
# 2 = Infected
# 3 = Immune (got it once)
# 4 = Dead
# 0 = Empty


class Node:

    condition = None
    x = 0
    y = 0
    recoveryProgress = 0
    unchecked = True

    def __init__(self, condition=None):
        if condition is not None:
            self.condition = condition
        else:
            self.condition = 0
        self.x = 0
        self.y = 0
        self.recoveryProgress = 0

    # Define node location on map
    def set_location (self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

    def set_recoveryProgress(self, recoveryProgress):
        self.recoveryProgress = recoveryProgress

    def set_unchecked(self, status):
        self.unchecked = status

    # Define node condition
    def set_condition(self, num):
        if num == 0 or num == 1 or num == 2 or num == 3 or num == 4:
            self.condition = num
        else:
            sys.stderr.write('Unknown condition')
            # Sets to empty
            self.condition = 0

    # Move to node
    def move(self, condition, recoveryProgress):
        self.condition = condition
        self.recoveryProgress = recoveryProgress
        self.unchecked = False


# MAP
# Represents the simulation surface (height x width)
class Map:

    height = 100
    width = 100
    surface = []

    pop = 0
    susceptible = 0
    infected = 0
    immune = 0
    dead = 0
    empty = 0

    # Rates (infection, recovery and death)
    infectionRate = 10  # % chance of getting infected
    recoveryTime = 10  # turns
    mortalityRate = 2  # % chance of death

    turnCount = 0

    # Contructor
    def __init__(self):
        # Randomly fills in conditions
        for x in range(self.width):
            row = []
            for y in range(self.height):
                i = random.randint(0, 1000)
                if i <= 299:
                    row.append(Node(1))
                    self.susceptible += 1
                elif i <= 300:
                    row.append(Node(2))
                    self.infected += 1
                else:
                    row.append(Node(0))
                    self.empty += 1

            self.surface.append(row)

        self.pop = self.susceptible + self.infected

        print('Surface populated')
        print('Susceptible: ', self.susceptible)
        print('Infected: ', self.infected)
        print('Empty spaces: ', self.empty)
        print('Width: ', len(self.surface))
        print('Row height of 5: ', len(self.surface[5]))

    def get_surface(self):
        return self.surface

    # Every turn checks each cell and it's neighbors
    def turn(self):
        self.turnCount += 1
        # print(self.turnCount)
        surface = self.surface
        [[self.verifica_vizinhos(x, y, surface[x][y]) for y in range(0, self.height)] for x in range(0, self.width)]
        [[self.reset_nodes(surface[x][y]) for y in range(0, self.height)] for x in range(0, self.width)]

    # Resets node unchecked status
    def reset_nodes(self, node):
        node.unchecked = True

    # Returns neighbors
    def get_vizinhos(self, x, y):
        cima = self.surface[x][(y - 1) % self.height]
        cima_direita = self.surface[(x + 1) % self.width][(y - 1) % self.height]
        direita = self.surface[(x + 1) % self.width][y]
        baixo_direita = self.surface[(x + 1) % self.width][(y + 1) % self.height]
        baixo = self.surface[x][(y + 1) % self.height]
        baixo_esquerda = self.surface[(x - 1) % self.width][(y + 1) % self.height]
        esquerda = self.surface[(x - 1) % self.width][y]
        cima_esquerda = self.surface[(x - 1) % self.width][(y - 1) % self.height]

        vizinhos = [cima, cima_direita, direita, baixo_direita, baixo, baixo_esquerda, esquerda, cima_esquerda]
        return vizinhos

    def verifica_vizinhos(self, x, y, node):
        # If empty, do nothing
        if node.condition == 0 or node.condition == 4:
            return

        # If infected, add recovery day
        if node.condition == 2 and node.unchecked:
            node.recoveryProgress += 1

        # Check if recovered
        if node.recoveryProgress == self.recoveryTime:
            if random.randint(0, 100) <= self.mortalityRate:
                node.recoveryProgress = 0
                node.set_condition(4)  # Died
                self.dead += 1
                self.infected -= 1
            else:
                node.recoveryProgress = 0
                node.set_condition(3)  # Recovered
                self.immune += 1
                self.infected -= 1

        neighbors = self.get_vizinhos(x, y)
        susceptible = []
        empty = []

        # Fills in condition vectors
        for viz in neighbors:
            if viz.condition == 1:
                susceptible.append(viz)
            elif viz.condition == 0:
                empty.append(viz)

        size_empty = len(empty)
        size_susceptible = len(susceptible)

        # Infect adjacent
        if node.condition == 2 and size_susceptible != 0:
            for susc in susceptible:
                if random.randint(0, 100) <= self.infectionRate:
                    susc.set_condition(2)
                    self.susceptible -= 1
                    self.infected += 1

        # Move to empty space
        if len(empty) == 0:
            return
        else:
            empty[random.randint(0, (size_empty - 1))].move(node.condition, node.recoveryProgress)
            node.set_condition(0)
            node.set_recoveryProgress(0)


