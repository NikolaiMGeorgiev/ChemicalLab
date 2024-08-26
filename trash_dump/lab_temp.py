from random import randrange, shuffle, seed
import math
import time
import sys

pos_eff_names = ['muscle_mass', 'body_fat', 'energy', 'stength']
neg_eff_names = ['cancerous', 'impotence', 'diaberes', 'heart_disease']
chem_names = ['Al', 'Na', 'K', 'Ca', 'Mg', 'Fe', 'Zn', 'Cu', 'Mn', 'Se', 'Cr', 'Mo', 'F', 'I', 'P', 'S', 'Cl', 'B', 'Si']
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
    "n": 12,
    "population_count": 3,
    "split_group": 3,
    "parents_cutoff_percentage": 0.6,
    "min_epochs": 1000,
    "ecpoh_interval": 50,
    "chem_names": chem_names,
}
samples = []
for i in range(config["n"]):
    pos_eff = []
    neg_eff = []
    for j in range(len(pos_eff_names)):
        pos_eff.append(randrange(config["max_coord"]))
        neg_eff.append(randrange(config["max_coord"]//10))
    samples.append(Sample(chem_names[i], pos_eff, neg_eff))
config["samples"] = samples


def get_distance(chemId, otherChemId, samples):
    sample = samples[chemId]
    otherSample = samples[otherChemId]
    distance = 0
    for i in range(len(pos_eff_names)):
        distance += (sample.pos_eff[i] - otherSample.pos_eff[i]) ** 2
        distance -= (sample.neg_eff[i] - otherSample.neg_eff[i]) ** 2
    return distance

def evaluate(population, config):
    population_count = len(population)
    samples = config["samples"]
    fitness = {}
    for i in range(population_count):
        chems = population[i]
        single_fitness = 0
        for i in range(1, config["n"]):
            chem = chems[i]
            previous_chem = chems[i - 1]
            single_fitness -= get_distance(previous_chem, chem, samples)
        fitness[chem_string(chems)] = single_fitness
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
    sorted_population = list(sorted(population, key=lambda chems: fitness[chem_string(chems)], reverse=True))
    sorted_population = sorted_population[:max_population_count]

    selection_pool = []
    new_parents = []
    total_distance = 0
    for i in range(max_population_count):
        chems = sorted_population[i]
        total_distance += fitness[chem_string(chems)]
        
    for i in range(max_population_count):
        chems = sorted_population[i]
        selection_percentage = math.ceil(fitness[chem_string(chems)] * 100 / total_distance)
        if selection_percentage:
            selection_pool.extend([chems] * selection_percentage)
        
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
    chem_index = randrange(n)
    while chem_index == insertion_index:
        chem_index = randrange(n)

    mutated_child = []
    for i in range(n):
        if i == insertion_index:
            mutated_child.append(child[chem_index])
        if i != chem_index:
            mutated_child.append(child[i])

    return mutated_child

def chem_string(chems):
    chems = map(str, chems)
    return ", ".join(chems)

def print_result(population_data, names = None):
    print(round(-1 * population_data["evaluation"],2 ))
    print(population_data["fittest_individual"])
    
    for index in population_data["fittest_individual"].split(", "):
        print(names[int(index)])


population = []
chems_list = list(range(config["n"]))

for i in range(config["population_count"]):
    shuffle(chems_list)
    population.append(chems_list[:])

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
            print_result(population_data, config["chem_names"])
            break
        else:
            last_best_evalutation = best_evalutaion
            print_indexes = [randrange(i, i + ecpoh_interval) for _ in range(4)] 

    population_data = select_parents(population, children, config)
    population = population_data["population"]

    if i in print_indexes:
        print_result(population_data, config["chem_names"])

    if not best_evalutaion or best_evalutaion < population_data["evaluation"]:
        best_evalutaion = population_data["evaluation"]