from random import randrange, shuffle, seed, uniform
import math
import time

"""
chem_pos_coef = {}
for c in chem_names:
    pos_vals = [randrange(1, 10) for _ in range(len(pos_eff_names))]
    neg_vals = [randrange(1, 10) for _ in range(len(neg_eff_names))]
    pos_vals_total = sum(pos_vals)
    neg_vals_total = sum(neg_vals)
    chem_pos_eff[c] = [round(x / pos_vals_total, 2) for x in pos_vals]
    chem_neg_eff[c] = [round(x / neg_vals_total, 2) for x in neg_vals]
    chem_pos_coef[c] = [round(uniform(0, 1), 1) for _ in range(config["chems_count"])]

print(chem_pos_eff)
print(chem_neg_eff)
print(chem_pos_coef)
"""

class Lab:
    def __init__(self):
        self.config = {
            "min_epochs": 50,
            "epoch_interval": 100,
            "tolerance": 200,
            "max_epochs": 1000,
        }
        self.pos_eff_names = ['muscle_mass', 'body_fat', 'energy', 'stength']
        self.neg_eff_names = ['cancer', 'impotence', 'diabetes', 'heart_disease']
        self.all_chem_names = ['Al', 'Na', 'K', 'Cr', 'Co', 'Ni', 'As', 'Cd', 'Hg', 'Pb', 'Sn', 'Ti', 'Al', 'Ag', 'Au', 'Pt', 'Ir', 'Os', 'Rh', 'Ru', 'Re', 'W', 'Ta', 'Hf', 'Th', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        self.chem_pos_eff = {'Al': [0.26, 0.3, 0.22, 0.22], 'Na': [0.5, 0.17, 0.11, 0.22], 'K': [0.22, 0.11, 0.28, 0.39], 'Cr': [0.29, 0.25, 0.14, 0.32], 'Co': [0.15, 0.3, 0.33, 0.22], 'Ni': [0.37, 0.11, 0.11, 0.42], 'As': [0.25, 0.25, 0.12, 0.38], 'Cd': [0.14, 0.43, 0.14, 0.29], 'Hg': [0.5, 0.1, 0.3, 0.1], 'Pb': [0.18, 0.41, 0.14, 0.27], 'Sn': [0.13, 0.3, 0.17, 0.39], 'Ti': [0.18, 0.09, 0.32, 0.41], 'Ag': [0.29, 0.14, 0.24, 0.33], 'Au': [0.14, 0.1, 0.33, 0.43], 'Pt': [0.13, 0.35, 0.3, 0.22], 'Ir': [0.39, 0.06, 0.33, 0.22], 'Os': [0.07, 0.29, 0.36, 0.29], 'Rh': [0.06, 0.12, 0.41, 0.41], 'Ru': [0.32, 0.32, 0.24, 0.12], 'Re': [0.4, 0.1, 0.3, 0.2], 'W': [0.4, 0.2, 0.25, 0.15], 'Ta': [0.1, 0.33, 0.43, 0.14], 'Hf': [0.19, 0.33, 0.22, 0.26], 'Th': [0.25, 0.08, 0.33, 0.33], 'U': [0.29, 0.14, 0.14, 0.43], 'Np': [0.06, 0.25, 0.19, 0.5], 'Pu': [0.23, 0.46, 0.08, 0.23], 'Am': [0.24, 0.21, 0.27, 0.27], 'Cm': [0.47, 0.05, 0.11, 0.37], 'Bk': [0.27, 0.33, 0.27, 0.13], 'Cf': [0.12, 0.31, 0.5, 0.06], 'Es': [0.27, 0.09, 0.36, 0.27], 'Fm': [0.41, 0.41, 0.06, 0.12], 'Md': [0.33, 0.29, 0.21, 0.17], 'No': [0.4, 0.13, 0.07, 0.4], 'Lr': [0.23, 0.15, 0.15, 0.46], 'Rf': [0.28, 0.12, 0.24, 0.36], 'Db': [0.26, 0.37, 0.21, 0.16], 'Sg': [0.36, 0.18, 0.18, 0.27], 'Bh': [0.26, 0.32, 0.16, 0.26], 'Hs': [0.06, 0.47, 0.18, 0.29], 'Mt': [0.33, 0.13, 0.13, 0.4], 'Ds': [0.19, 0.33, 0.24, 0.24], 'Rg': [0.26, 0.26, 0.42, 0.05], 'Cn': [0.37, 0.21, 0.32, 0.11], 'Nh': [0.17, 0.25, 0.33, 0.25], 'Fl': [0.23, 0.35, 0.23, 0.19], 'Mc': [0.27, 0.27, 0.18, 0.27], 'Lv': [0.21, 0.27, 0.27, 0.24], 'Ts': [0.08, 0.08, 0.42, 0.42], 'Og': [0.35, 0.1, 0.4, 0.15]}
        self.chem_neg_eff = {'Al': [0.18, 0.09, 0.55, 0.18], 'Na': [0.41, 0.12, 0.41, 0.06], 'K': [0.06, 0.18, 0.29, 0.47], 'Cr': [0.12, 0.47, 0.12, 0.29], 'Co': [0.31, 0.44, 0.06, 0.19], 'Ni': [0.19, 0.29, 0.23, 0.29], 'As': [0.25, 0.17, 0.33, 0.25], 'Cd': [0.21, 0.29, 0.29, 0.21], 'Hg': [0.12, 0.38, 0.12, 0.38], 'Pb': [0.32, 0.04, 0.28, 0.36], 'Sn': [0.05, 0.38, 0.24, 0.33], 'Ti': [0.12, 0.38, 0.12, 0.38], 'Ag': [0.23, 0.23, 0.23, 0.31], 'Au': [0.3, 0.26, 0.3, 0.15], 'Pt': [0.17, 0.29, 0.38, 0.17], 'Ir': [0.31, 0.21, 0.24, 0.24], 'Os': [0.05, 0.26, 0.21, 0.47], 'Rh': [0.2, 0.35, 0.15, 0.3], 'Ru': [0.18, 0.29, 0.47, 0.06], 'Re': [0.28, 0.28, 0.39, 0.06], 'W': [0.47, 0.32, 0.16, 0.05], 'Ta': [0.35, 0.39, 0.13, 0.13], 'Hf': [0.1, 0.7, 0.1, 0.1], 'Th': [0.28, 0.5, 0.17, 0.06], 'U': [0.17, 0.39, 0.11, 0.33], 'Np': [0.16, 0.47, 0.32, 0.05], 'Pu': [0.18, 0.47, 0.24, 0.12], 'Am': [0.04, 0.38, 0.25, 0.33], 'Cm': [0.07, 0.27, 0.6, 0.07], 'Bk': [0.35, 0.22, 0.3, 0.13], 'Cf': [0.33, 0.3, 0.11, 0.26], 'Es': [0.31, 0.17, 0.21, 0.31], 'Fm': [0.21, 0.21, 0.5, 0.07], 'Md': [0.37, 0.21, 0.11, 0.32], 'No': [0.43, 0.21, 0.21, 0.14], 'Lr': [0.42, 0.05, 0.42, 0.11], 'Rf': [0.27, 0.36, 0.09, 0.27], 'Db': [0.17, 0.23, 0.3, 0.3], 'Sg': [0.23, 0.23, 0.27, 0.27], 'Bh': [0.41, 0.23, 0.27, 0.09], 'Hs': [0.33, 0.17, 0.17, 0.33], 'Mt': [0.13, 0.27, 0.07, 0.53], 'Ds': [0.22, 0.39, 0.06, 0.33], 'Rg': [0.24, 0.21, 0.27, 0.27], 'Cn': [0.33, 0.4, 0.2, 0.07], 'Nh': [0.2, 0.35, 0.35, 0.1], 'Fl': [0.17, 0.39, 0.17, 0.26], 'Mc': [0.14, 0.07, 0.29, 0.5], 'Lv': [0.47, 0.07, 0.33, 0.13], 'Ts': [0.2, 0.27, 0.13, 0.4], 'Og': [0.13, 0.33, 0.2, 0.33]}
        self.chem_pos_coef = {'Al': [0.1, 0.2, 0.7, 0.7, 0.0, 0.5], 'Na': [0.3, 0.1, 0.1, 0.3, 0.3, 0.8], 'K': [0.5, 0.0, 0.1, 0.3, 0.6, 0.4], 'Cr': [0.5, 0.1, 0.2, 0.0, 0.8, 0.9], 'Co': [0.8, 0.4, 0.4, 0.4, 0.5, 0.6], 'Ni': [0.1, 0.7, 0.2, 1.0, 0.3, 0.0], 'As': [0.4, 0.2, 0.8, 0.9, 0.2, 0.5], 'Cd': [0.3, 0.2, 0.1, 0.4, 0.0, 0.5], 'Hg': [0.7, 0.2, 0.6, 0.0, 0.4, 0.7], 'Pb': [0.5, 0.2, 0.7, 0.7, 0.4, 0.1], 'Sn': [0.9, 0.8, 0.7, 0.7, 0.1, 0.5], 'Ti': [0.6, 0.5, 0.6, 1.0, 0.6, 0.1], 'Ag': [0.6, 0.1, 0.9, 0.2, 1.0, 0.3], 'Au': [0.3, 0.4, 0.9, 0.2, 0.6, 0.8], 'Pt': [0.3, 0.7, 0.2, 1.0, 0.6, 0.7], 'Ir': [0.6, 0.8, 0.1, 0.1, 0.6, 0.8], 'Os': [0.9, 0.3, 0.3, 0.3, 0.3, 0.7], 'Rh': [0.5, 0.4, 0.6, 0.5, 0.4, 0.1], 'Ru': [0.3, 0.7, 0.1, 0.7, 0.8, 0.5], 'Re': [0.6, 0.5, 0.9, 0.9, 0.9, 0.0], 'W': [0.9, 0.0, 0.2, 0.8, 0.7, 1.0], 'Ta': [0.6, 0.4, 0.5, 0.6, 0.7, 0.7], 'Hf': [0.5, 0.1, 0.2, 0.8, 0.1, 0.2], 'Th': [0.7, 0.2, 0.4, 0.2, 0.6, 0.7], 'U': [0.3, 0.4, 1.0, 0.1, 0.1, 0.1], 'Np': [0.2, 0.4, 0.4, 0.4, 0.5, 0.1], 'Pu': [0.4, 1.0, 0.3, 0.4, 0.5, 0.3], 'Am': [0.5, 0.2, 0.5, 0.2, 0.0, 0.9], 'Cm': [0.6, 0.2, 0.4, 0.9, 0.5, 0.4], 'Bk': [0.8, 0.7, 0.0, 0.5, 0.3, 0.6], 'Cf': [0.6, 0.6, 0.6, 0.8, 0.7, 0.7], 'Es': [0.9, 0.2, 0.8, 0.2, 1.0, 0.5], 'Fm': [0.1, 0.1, 0.2, 0.5, 0.9, 0.0], 'Md': [0.1, 0.7, 0.9, 0.4, 0.7, 0.1], 'No': [0.1, 0.7, 0.6, 0.1, 0.8, 0.4], 'Lr': [0.3, 0.1, 0.0, 0.2, 0.9, 0.1], 'Rf': [0.1, 0.7, 0.2, 0.6, 0.2, 0.6], 'Db': [0.0, 1.0, 0.6, 0.0, 0.6, 0.9], 'Sg': [0.3, 0.3, 0.2, 0.4, 0.2, 1.0], 'Bh': [0.9, 0.9, 0.7, 0.6, 0.7, 0.4], 'Hs': [1.0, 0.8, 0.7, 0.6, 0.9, 0.2], 'Mt': [0.8, 0.6, 0.3, 0.2, 0.2, 0.7], 'Ds': [0.4, 0.3, 0.3, 0.5, 0.2, 0.0], 'Rg': [0.6, 0.8, 1.0, 0.5, 0.4, 0.6], 'Cn': [0.1, 0.0, 0.6, 0.1, 0.5, 0.1], 'Nh': [0.8, 0.7, 0.3, 0.0, 0.1, 0.8], 'Fl': [0.4, 0.2, 0.1, 0.2, 0.4, 0.7], 'Mc': [0.0, 0.7, 0.5, 0.7, 0.7, 0.4], 'Lv': [0.7, 0.9, 0.9, 0.8, 0.5, 0.6], 'Ts': [1.0, 0.0, 0.0, 0.0, 0.3, 0.8], 'Og': [0.9, 0.2, 0.9, 0.0, 0.3, 1.0]}
        self.max_coeff = 1000
        self.population_count =  10
        self.population = []

    def configure(self, chems, max_by_property):
        self.max_by_property = max_by_property
        self.chem_names = chems
        self.chems_count = len(chems)
        self.split_group = 4 if self.chems_count > 6 else 2
        self.parents_cutoff = 4
        self.generate_population()

    def generate_population(self):
        chems_list = list(range(len(self.chem_names)))
        for _ in range(self.population_count):
            shuffle(chems_list)
            self.population.append(chems_list[:])

    def evaluate(self, population):
        fitness = {}
        for i in range(len(population)):
            chem_ids = population[i]
            single_fitness = 0
            for j in range(1, self.chems_count):
                curr_id = chem_ids[j]
                prev_id = chem_ids[j - 1]
                single_fitness -= self.get_coeff(self.chem_names[curr_id], self.chem_names[prev_id], j)
            fitness[self.chem_string(chem_ids)] = single_fitness
        return fitness

    def select_parents(self, children):
        fitness = self.evaluate(self.population)
        new_parents = self.partial_selection(self.population, fitness, self.chems_count)

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
        if (len(sorted_population) < max_population_count):
            max_population_count = len(sorted_population)

        selection_pool = []
        new_parents = []
        total_coef = sum(fitness[self.chem_string(chems)] for chems in sorted_population)
            
        for i in range(max_population_count):
            chems = sorted_population[i]
            selection_percentage = math.ceil(fitness[self.chem_string(chems)] * 100/total_coef)
            if selection_percentage:
                selection_pool.extend([chems] * selection_percentage)
            
        for i in range(max_population_count):
            new_parents.append(selection_pool[randrange(100)])

        return new_parents

    def reproduce(self):
        children = []
        split_group = self.split_group - 1
        for i in range(1, self.population_count):
            split_index = randrange(self.chems_count)
            split_start = split_index - split_group if split_index >= split_group else split_index
            split_end = split_index if split_index >= split_group else split_index + split_group
            if split_end >= self.chems_count:
                difference = split_end - self.chems_count+1
                split_end -= difference
                split_start -= difference
            parent = self.population[i]
            other_parent = self.population[i - 1]

            # Crossover
            child = other_parent[:split_start] + parent[split_start:split_end] + other_parent[split_end:]
            other_child = parent[:split_start] + other_parent[split_start:split_end] + parent[split_end:]
            
            self.insertion_mutation(child)
            self.insertion_mutation(other_child)

            children.append(child)
            children.append(other_child)

        return children

    def insertion_mutation(self, child):
        insertion_index = randrange(self.chems_count)
        chem_index = randrange(self.chems_count)
        
        while chem_index == insertion_index:
            chem_index = randrange(self.chems_count)

        child[insertion_index], child[chem_index] = child[chem_index], child[insertion_index]

    def get_coeff(self, chem_name, other_chem_name, position):
        pos_coeff = sum(map(lambda x: (x[0]-x[1]) ** 2, zip(self.chem_pos_eff[chem_name], self.chem_pos_eff[other_chem_name])))
        neg_coeff = sum(map(lambda x: (x[0]-x[1]) ** 2, zip(self.chem_neg_eff[chem_name], self.chem_neg_eff[other_chem_name])))
        max_property_index = self.pos_eff_names.index(self.max_by_property)
        return ((self.chem_pos_eff[chem_name][max_property_index] 
                 - self.chem_neg_eff[chem_name][max_property_index]) 
                 + (pos_coeff - neg_coeff) * self.chem_pos_coef[chem_name][position])

    def get_substance_properties(self, substance):
        properties = {name: 0 for name in list(self.pos_eff_names) + list(self.neg_eff_names)}
        for chem_pos in range(len(substance)):
            chem_name = substance[chem_pos]
            for effect_pos in range(len(self.pos_eff_names)):
                effect_name = self.pos_eff_names[effect_pos]
                properties[effect_name] += self.chem_pos_eff[chem_name][effect_pos] * self.chem_pos_coef[chem_name][chem_pos]
            for effect_pos in range(len(self.neg_eff_names)):
                effect_name = self.neg_eff_names[effect_pos]
                properties[effect_name] += self.chem_neg_eff[chem_name][effect_pos] * self.chem_pos_coef[chem_name][chem_pos]
        for property in properties.keys():
            properties[property] = round(properties[property] * 100/self.chems_count)
        return properties

    def chem_string(self, chems):
        return ", ".join(map(str, chems))

    def print_result(self, population_data, names=None):
        print(round(population_data["evaluation"], 2))
        print(population_data["fittest_individual"])
        print(",".join([names[int(index)] for index in population_data["fittest_individual"].split(", ")]))

    def experiment(self, max_by_property, chems):
        self.configure(chems, max_by_property)

        min_ecpoh = self.config["min_epochs"]
        epoch_interval = self.config["epoch_interval"]
        tolerance_left = self.config["tolerance"]
        first_evaluation = self.evaluate(self.population)
        best_evalutaion = None
        last_best_evalutation = sum(first_evaluation.values())

        for i in range(1, self.config["max_epochs"] + 1):
            seed(time.time())
            children = self.reproduce()
            if i >= min_ecpoh and i % epoch_interval == 0:
                # self.print_result(population_data, self.chem_names)
                if best_evalutaion == last_best_evalutation:
                    tolerance_left -= epoch_interval
                    if (tolerance_left <= 0):
                        substance = [self.chem_names[int(index)] for index in population_data["fittest_individual"].split(", ")]
                        return {
                            "substance": substance,
                            "properties": self.get_substance_properties(substance)
                        } 
                else:
                    tolerance_left = self.config["tolerance"]
                    last_best_evalutation = best_evalutaion

            population_data = self.select_parents(children)
            self.population = population_data["population"]

            # if (i == 1):
            #     self.print_result(population_data, self.chem_names)

            if not best_evalutaion or best_evalutaion < population_data["evaluation"]:
                best_evalutaion = population_data["evaluation"]
        
            substance = [self.chem_names[int(index)] for index in population_data["fittest_individual"].split(", ")]
            return {
                "substance": substance,
                "properties": self.get_substance_properties(substance)
            } 