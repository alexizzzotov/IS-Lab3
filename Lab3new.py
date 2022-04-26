from random import randint

class Chromosome:   # класс, включающий методы алгоритма
    def __init__(self, size, gene_pool):   # инициализация
        self.rating = 0
        self.size = size
        self.genes = bytearray(size)
        if gene_pool is not None:
            self.set_random_genes(gene_pool)

    def set_random_genes(self, gene_pool):   # функция для создания случайной хромосомы
        gene_pool_range = len(gene_pool) - 1
        for i in range(self.size):
            rand_pos = randint(0, gene_pool_range)
            self.genes[i] = gene_pool[rand_pos]

def create_population(pop_size, chromo_size, genes):   # функция заполнения популяции 
    population = [None] * pop_size
    for i in range(pop_size):
        population[i] = Chromosome(chromo_size, gene_pool)

    return population

def calc_rating(population, final_chromo):   # функция для вычисления рейтинга 
    for chromo in population:
        chromo.rating = chromo.size
        for i in range(chromo.size):
            if chromo.genes[i] == final_chromo[i]:
                chromo.rating -= 1

def sort_population(population):   # сортировка хромосом по рейтингу 
    size = len(population)
    repeat = True
    while repeat:
        repeat = False
        for i in range(0, size - 1):
            bubble = population[i]
            if (bubble.rating > population[i + 1].rating):
                population[i] = population[i + 1]
                population[i + 1] = bubble
                repeat = True
    
def select(population, survivors):   # селекция (отбираем лучшую половину популяции)
    size = len(survivors)
    for i in range(size):
        survivors[i] = population[i]

def repopulate(population, parents, children_count):   # функция, заполняющая вторую половину популяции
    pop_size = len(population)
    while children_count < pop_size:
        p1_pos = get_parent_index(parents, None)
        p2_pos = get_parent_index(parents, p1_pos)
        p1 = parents[p1_pos]
        p2 = parents[p2_pos]
        population[children_count] = cross(p1, p2)
        population[children_count + 1] = cross(p2, p1)
        children_count += 2

def get_parent_index(parents, exclude_index):   # функция, возвращающая индекс случайно выбранного родителя
    size = len(parents)
    while True:
        index = randint(0, size - 1)
        if exclude_index is None or exclude_index != index:
            return index

def cross(chromo1, chromo2):   # скрещивание (одноточечный кроссинговер)
    size = chromo1.size
    point = randint(0, size - 1)
    child = Chromosome(size, None)
    for i in range(point):
        child.genes[i] = chromo1.genes[i]
    for i in range(point, size):
        child.genes[i] = chromo2.genes[i]

    return child

def mutate(population, chromo_count, gene_count, gene_pool):   # мутация
    pop_size = len(population)
    gene_pool_size = len(gene_pool)
    for i in range(chromo_count):
        chromo_pos = randint(0, pop_size - 1)
        chromo = population[chromo_pos]
        for j in range(gene_count):
            gene_pos = randint(0, gene_pool_size - 1)
            gene = gene_pool[gene_pos]
            gene_pos = randint(0, chromo.size - 1)
            chromo.genes[gene_pos] = gene

def print_population(population):   # вывод популяции
    i = 0
    for chromo in population:
        i += 1
        print(str(i).center(2) + '. ' + str(chromo.rating) + ': ' + chromo.genes.decode())

gene_pool = bytearray(b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')   # строка со всеми возможными генами
final_chromo = bytearray(b'MIR')  # финальная последовательность для сравнения
chromo_size = len(final_chromo)   # длина хромосомы
population_size = 20              # размер популяции
survivors = [None] * (population_size // 2)   # список для лучшей половины (в функции селекции)
population = create_population(population_size, chromo_size, gene_pool)   # формирование популяции

iteration_count = 0   # счетчик итераций

while True:   # основной цикл
    iteration_count += 1
    calc_rating(population, final_chromo)
    sort_population(population)
    print('*** ' + str(iteration_count) + ' ***')
    print_population(population)
    if population[0].rating == 0:
        break
    select(population, survivors)
    repopulate(population, survivors, population_size // 2)
    mutate(population, 10, 1, gene_pool)
