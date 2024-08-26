from random import randrange, shuffle, seed
import math
import time
import sys

pos_eff_names = ['muscle_mass', 'body_fat', 'energy', 'stength']
neg_eff_names = ['cancer', 'impotence', 'diaberes', 'heart_disease']
chem_names = ['Al', 'Na', 'K', 'Cr', 'Co', 'Ni', 'As', 'Cd', 'Hg', 'Pb', 'Sn', 'Ti', 'Al', 'Ag', 'Au', 'Pt', 'Ir', 'Os', 'Rh', 'Ru', 'Re', 'W', 'Ta', 'Hf', 'Th', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']


class Sample:
    def __init__(self, name, pos_eff, neg_eff):
        self.name = name
        self.pos_eff = pos_eff
        self.neg_eff = neg_eff

    def get_coeff(self, otherSample):
        pos_coeff = sum(map(lambda x: (x[0] - x[1]) ** 2, zip(self.pos_eff, otherSample.pos_eff)))
        neg_coeff = sum(map(lambda x: (x[0] - x[1]) ** 2, zip(self.neg_eff, otherSample.neg_eff)))
        return pos_coeff - neg_coeff


class Lab:
    def __init__(self, chems):
        self.max_coeff = 1000
        self.chems_count = 7
        self.population_count =  4
        self.split_group = 4
        self.parents_cutoff = 4
        self.chem_names = chems
        self.samples = []
        self.population = []
        self.generate_samples()
        self.generate_population()

    def generate_samples(self):
        for i in range(self.chems_count):
            pos_eff = [randrange(self.max_coeff) for _ in range(len(pos_eff_names))]
            neg_eff = [randrange(self.max_coeff) for _ in range(len(pos_eff_names))]
            self.samples.append(Sample(self.chem_names[i], pos_eff, neg_eff))

    def generate_population(self):
        chems_list = list(range(self.chems_count))
        for _ in range(self.population_count):
            shuffle(chems_list)
            self.population.append(chems_list[:])

    def evaluate(self, population):
        fitness = {}
        for i in range(self.population_count):
            chem_ids = population[i]
            single_fitness = 0
            for i in range(1, self.chems_count):
                curr_id = chem_ids[i]
                prev_id = chem_ids[i - 1]
                single_fitness -= self.samples[curr_id].get_coeff(self.samples[prev_id])
            fitness[self.chem_string(chem_ids)] = single_fitness
        return fitness

    def select_parents(self, children):
        fitness = self.evaluate(self.population)
        new_parents = self.partial_selection(self.population, fitness, self.chems_count)#self.parents_cutoff)

        children_fitness = self.evaluate(children)
        new_parents += self.partial_selection(children, children_fitness, self.population_count - self.parents_cutoff)
        fitness.update(children_fitness)

        best_fitness = max(fitness.items(), key=lambda x: x[1])
        return {
            "population": new_parents,
            "evaluation": best_fitness[1],
            "fittest_individual": best_fitness[0],
        }


    def partial_selection(self, population, fitness, max_population_count):
        sorted_population = list(sorted(population, key=lambda chems: fitness[self.chem_string(chems)], reverse=True))
        sorted_population = sorted_population[:max_population_count]

        selection_pool = []
        new_parents = []
        total_coef = sum(fitness[self.chem_string(chems)] for chems in sorted_population)
            
        for i in range(max_population_count):
            chems = sorted_population[i]
            selection_percentage = math.ceil(fitness[self.chem_string(chems)] * 100 / total_coef)
            if selection_percentage:
                selection_pool.extend([chems] * selection_percentage)
            
        for i in range(max_population_count):
            new_parents.append(selection_pool[randrange(100)])

        return new_parents

    def reproduce(self):
        children = []
        split_group = self.split_group
        for i in range(1, self.population_count):
            split_index = randrange(self.chems_count)
            split_start = split_index - split_group if split_index >= split_group else split_index
            split_end = split_index if split_index >= split_group else split_index + split_group
            if split_end >= self.chems_count:
                difference = split_end - self.chems_count + 1
                split_end -= difference
                split_start -= difference
            parent = self.population[i]
            other_parent = self.population[i - 1]

            child = self.crossover(split_start, split_end, parent, other_parent)
            other_child = self.crossover(split_start, split_end, other_parent, parent)
            
            child = self.insertion_mutation(child)
            other_child = self.insertion_mutation(other_child)

            children.append(child)
            children.append(other_child)

        return children

    def crossover(self, split_start, split_end, parent, other_parent):
        child_gene_indexes = list(range(split_end, self.chems_count)) + list(range(0, split_start))
        parent_gene_indexes = child_gene_indexes[:] + list(range(split_start, split_end))
        genes_to_keep = parent[split_start:split_end]
        child = list([-1] * split_start) + genes_to_keep + list([-1] * (self.chems_count - split_start - len(genes_to_keep)))
        
        child_index = 0
        for g in parent_gene_indexes:
            new_gene = other_parent[g]
            if new_gene in genes_to_keep:
                continue
            child[child_gene_indexes[child_index]] = new_gene
            child_index += 1

        return child

    def insertion_mutation(self, child):
        insertion_index = randrange(self.chems_count)
        chem_index = randrange(self.chems_count)
        
        while chem_index == insertion_index:
            chem_index = randrange(self.chems_count)

        mutated_child = []
        for i in range(self.chems_count):
            if i == insertion_index:
                mutated_child.append(child[chem_index])
            if i != chem_index:
                mutated_child.append(child[i])

        return mutated_child

    def chem_string(self, chems):
        chems = map(str, chems)
        return ", ".join(chems)

    def print_result(self, population_data, names = None):
        print(round(-1 * population_data["evaluation"], 2))
        print(population_data["fittest_individual"])
        for index in population_data["fittest_individual"].split(", "):
            print(names[int(index)])

config = {
    "min_epochs": 500,
    "ecpoh_interval": 50,
    "max_epochs": 10000,
}

def experiment():
    min_ecpoh = config["min_epochs"]
    ecpoh_interval = config["ecpoh_interval"]
    lab = Lab(chem_names)

    first_evaluation = lab.evaluate(lab.population)
    fittest_individual = max(first_evaluation.items(), key=lambda x: x[1])
    print(round(-1 * fittest_individual[1], 2))
    print(fittest_individual[0])

    best_evalutaion = None
    last_best_evalutation = sum(first_evaluation.values())
    print_indexes = [randrange(min_ecpoh) for _ in range(8)]

    for i in range(1, config["max_epochs"] + 1):
        seed(time.time())
        children = lab.reproduce()
        if i >= min_ecpoh and i % ecpoh_interval == 0:
            if best_evalutaion == last_best_evalutation:
                lab.print_result(population_data, lab.chem_names)
                break
            else:
                last_best_evalutation = best_evalutaion
                print_indexes = [randrange(i, i + ecpoh_interval) for _ in range(4)] 

        population_data = lab.select_parents(children)
        lab.population = population_data["population"]

        if i in print_indexes:
            lab.print_result(population_data, lab.chem_names)

        if not best_evalutaion or best_evalutaion < population_data["evaluation"]:
            best_evalutaion = population_data["evaluation"]

experiment()