from random import randrange, shuffle, seed
import math
import time
import sys

pos_eff_names = ['muscle_mass', 'body_fat', 'energy', 'stength']
neg_eff_names = ['cancerous', 'impotence', 'diaberes', 'heart_disease']
chem_names = ['Al', 'Na', 'K', 'Ca', 'Mg', 'Fe', 'Zn', 'Cu', 'Mn', 'Se']#, 'Cr', 'Mo', 'F', 'I', 'P', 'S', 'Cl', 'B', 'Si', 'V', 'Co', 'Ni', 'As', 'Cd', 'Hg', 'Pb', 'Sn', 'Ti', 'Al', 'Ag', 'Au', 'Pt', 'Ir', 'Os', 'Rh', 'Ru', 'Re', 'W', 'Ta', 'Hf', 'Th', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
chem_coef_pos = [
    []
]

class Sample:
    def __init__(self, name, pos_eff, neg_eff):
        self.name = name
        self.pos_eff = pos_eff
        self.neg_eff = neg_eff


config = {
    "max_coord": 1000,
    "max_epochs": 10000,
    "n": 8,
    "population_count": 3,
    "split_group": 3,
    "parents_cutoff_percentage": 0.6,
    "min_epochs": 500,
    "ecpoh_interval": 50,
    "cities_names": chem_names,
}
cities_coord = []
for i in range(config["n"]):
    pos_eff = []
    neg_eff = []
    for j in range(len(pos_eff_names)):
        pos_eff.append(randrange(config["max_coord"]))
        neg_eff.append(randrange(config["max_coord"]//10))
    cities_coord.append(Sample(chem_names[i], pos_eff, neg_eff))
config["cities_coord"] = cities_coord


def get_distance(cityId, otherCityId, cities_coord):
    cityCoord = cities_coord[cityId]
    otherCityCoord = cities_coord[otherCityId]
    distance = 0
    for i in range(len(pos_eff_names)):
        distance += (cityCoord.pos_eff[i] - otherCityCoord.pos_eff[i]) ** 2
        distance -= (cityCoord.neg_eff[i] - otherCityCoord.neg_eff[i]) ** 2
    return distance

def evaluate(population, config):
    population_count = len(population)
    cities_coord = config["cities_coord"]
    fitness = {}
    for i in range(population_count):
        cities = population[i]
        single_fitness = 0
        for i in range(1, config["n"]):
            city = cities[i]
            previous_city = cities[i - 1]
            single_fitness -= get_distance(previous_city, city, cities_coord)
        fitness[cities_string(cities)] = single_fitness
    return fitness

def select_parents(population, children, config):
    max_population_count = config["population_count"]
    fitness = evaluate(population, config)
    parents_cutoff = int(max_population_count * config["parents_cutoff_percentage"])
    new_parents = partial_selection(population, fitness, parents_cutoff)

    children_fitness = evaluate(children, config)
    new_parents += partial_selection(children, children_fitness, max_population_count - parents_cutoff)
    fitness.update(children_fitness)

    return {
        "population": new_parents,
        "evaluation": max(fitness.items(), key=lambda x: x[1])[1],
        "fittest_individual": max(fitness.items(), key=lambda x: x[1])[0],
    }


def partial_selection(population, fitness, max_population_count):
    sorted_population = list(sorted(population, key=lambda cities: fitness[cities_string(cities)], reverse=True))
    sorted_population = sorted_population[:max_population_count]

    selection_pool = []
    new_parents = []
    total_distance = 0
    for i in range(max_population_count):
        cities = sorted_population[i]
        total_distance += fitness[cities_string(cities)]
        
    for i in range(max_population_count):
        cities = sorted_population[i]
        selection_percentage = math.ceil(fitness[cities_string(cities)] * 100 / total_distance)
        if selection_percentage:
            selection_pool.extend([cities] * selection_percentage)
        
    for i in range(max_population_count):
        index = randrange(100)
        new_parents.append(selection_pool[index])

    return new_parents

def reproduce(population, config):
    children = []
    n = config["n"]
    split_group = config["split_group"]
    for i in range(1, config["population_count"]):
        split_index = randrange(n)
        split_start = split_index - split_group if split_index >= split_group else split_index
        split_end = split_index if split_index >= split_group else split_index + split_group
        if split_end >= n:
            difference = split_end - n + 1
            split_end -= difference
            split_start -= difference
        parent = population[i]
        other_parent = population[i - 1]

        child = crossover(split_start, split_end, parent, other_parent, config)
        other_child = crossover(split_start, split_end, other_parent, parent, config)
        
        child = insertion_mutation(child, n)
        other_child = insertion_mutation(other_child, n)

        children.append(child)
        children.append(other_child)

    return children

def crossover(split_start, split_end, parent, other_parent, config):
    n = config["n"]
    child_gene_indexes = list(range(split_end, n)) + list(range(0, split_start))
    parent_gene_indexes = child_gene_indexes[:] + list(range(split_start, split_end))
    genes_to_keep = parent[split_start:split_end]
    child = list([-1] * split_start) + genes_to_keep + list([-1] * (n - split_start - len(genes_to_keep)))

    child_index = 0
    for g in parent_gene_indexes:
        new_gene = other_parent[g]
        if new_gene in genes_to_keep:
            continue
        child[child_gene_indexes[child_index]] = new_gene
        child_index += 1

    return child

def insertion_mutation(child, n):
    insertion_index = randrange(n)
    city_index = randrange(n)
    while city_index == insertion_index:
        city_index = randrange(n)

    mutated_child = []
    for i in range(n):
        if i == insertion_index:
            mutated_child.append(child[city_index])
        if i != city_index:
            mutated_child.append(child[i])

    return mutated_child

def cities_string(cities):
    cities = map(str, cities)
    return ", ".join(cities)

def print_result(population_data, names = None):
    print(round(-1 * population_data["evaluation"],2 ))
    print(population_data["fittest_individual"])
    
    if len(sys.argv) > 1 and names:
        for index in population_data["fittest_individual"].split(", "):
            print(names[int(index)])


population = []
cities_list = list(range(config["n"]))

for i in range(config["population_count"]):
    shuffle(cities_list)
    population.append(cities_list[:])

first_evaluation = evaluate(population, config)
fittest_individual = max(first_evaluation.items(), key=lambda x: x[1])
print(round(-1 * fittest_individual[1], 2))
print(fittest_individual[0])

last_best_evalutation = sum(first_evaluation.values())
best_evalutaion = None
min_ecpoh = config["min_epochs"]
ecpoh_interval = config["ecpoh_interval"]
print_indexes = [randrange(min_ecpoh) for _ in range(8)]

for i in range(1, config["max_epochs"] + 1):
    seed(time.time())
    children = reproduce(population, config)
    if i >= min_ecpoh and i % ecpoh_interval == 0:
        if best_evalutaion == last_best_evalutation:
            print_result(population_data, config["cities_names"])
            break
        else:
            last_best_evalutation = best_evalutaion
            print_indexes = [randrange(i, i + ecpoh_interval) for _ in range(4)] 

    population_data = select_parents(population, children, config)
    population = population_data["population"]

    if i in print_indexes:
        print_result(population_data)

    if not best_evalutaion or best_evalutaion < population_data["evaluation"]:
        best_evalutaion = population_data["evaluation"]