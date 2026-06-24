import numpy as np
import random
import sys

np.random.seed(42)
random.seed(42)

if len(sys.argv) in (3, 4):
    simulations_number = int(sys.argv[1])

    transmission_rule = sys.argv[2]

    r = float(sys.argv[3]) if len(sys.argv) == 4 else None

else:
    simulations_number = int(input('Simulations number: '))

    transmission_rule = input('Transmission rule: ')

    r_input = input('r: ').strip()

    r = float(r_input) if r_input else None

# Trait fitness generation

def generate_trait_fitness(X):
    raw = np.random.exponential(scale = 1.0, size = X)

    trait_fitness = np.round(2 * (raw ** 2)).astype(int)

    return trait_fitness

# Individual initialization

def initialize_individual():
    return {'traits': {}, 'individual_fitness': 0}

# Individual fitness calculation

def calculate_individual_fitness(individual, trait_fitness):
    individual_fitness = 0

    for s, x in individual['traits'].items():
        individual_fitness += trait_fitness[x]

    individual['individual_fitness'] = int(individual_fitness)

# Transmission rules

def unbiased_transmission(previous_population):
    individual_to_copy = random.choice(previous_population)

    return individual_to_copy['traits'].copy()

def indirect_bias_transmission(previous_population):
    individual_to_copy = max(previous_population, key = lambda i: i['individual_fitness'])

    return individual_to_copy['traits'].copy()

def direct_bias_transmission(previous_population, trait_fitness):
    traits_to_copy = {}

    max_s = 1

    for individual in previous_population:
        if individual['traits']:
            max_s = max(max_s, max(individual['traits'].keys()))

    for s in range(1, max_s + 1):
        possible_traits = []

        for individual in previous_population:
            if s in individual['traits']:
                possible_traits.append([individual['traits'][s], trait_fitness[individual['traits'][s]]])

        if possible_traits:
            best_trait = max(possible_traits, key = lambda t: t[1])[0]

            traits_to_copy[s] = best_trait

    return traits_to_copy

# Innovation

def innovation(individual, trait_fitness, effort_left, c_i, X):
    s = max(individual['traits'].keys()) + 1 if individual['traits'] else 1

    while effort_left >= c_i:
        x = random.randrange(X)

        if trait_fitness[x] > 0:
            individual['traits'][s] = x

            effort_left -= c_i

            s += 1

        else:
            effort_left -= c_i

    return effort_left

# Simulation

def run_model(N, T, X, l_0, c_s, c_i, transmission_rule, r = None, l_max = None):
    mean_cultural_complexities = []

    trait_fitness = generate_trait_fitness(X)

    # First generation

    population = [initialize_individual() for _ in range(N)]

    for individual in population:
        innovation(individual, trait_fitness, l_0, c_i, X)

        calculate_individual_fitness(individual, trait_fitness)

    mean_cultural_complexity = np.mean([individual['individual_fitness'] for individual in population])

    mean_cultural_complexities.append(mean_cultural_complexity)

    # Next generations

    for t in range(1, T):
        if r is not None:
            l = l_0 + (l_max - l_0) * (1 - np.exp(-r * mean_cultural_complexity))

        else:
            l = l_0

        new_population = []

        if transmission_rule == 'unbiased':
            traits_to_copy = unbiased_transmission(population)

        elif transmission_rule == 'indirect_bias':
            traits_to_copy = indirect_bias_transmission(population)

        elif transmission_rule == 'direct_bias':
            traits_to_copy = direct_bias_transmission(population, trait_fitness)

        for i in range(N):
            individual = initialize_individual()

            effort = l

            for s, x in traits_to_copy.items():
                if effort < c_s:
                    break

                else:
                    individual['traits'][s] = x

                    effort -= c_s

            innovation(individual, trait_fitness, effort, c_i, X)

            calculate_individual_fitness(individual, trait_fitness)

            new_population.append(individual)

        population = new_population

        mean_cultural_complexity = np.mean([individual['individual_fitness'] for individual in population])

        mean_cultural_complexities.append(mean_cultural_complexity)

    return mean_cultural_complexities

# Parameters

N = 100

X = 100

c_s = 5

c_i = 10

if r is None:
    T = 20

    l_0 = 1000

    l_max = None

else:
    T = 40

    l_0 = 100

    l_max = 1000

# Run simulations

mean_cultural_complexities = []

for s in range(simulations_number):
    mean_cultural_complexities.append(run_model(N, T, X, l_0, c_s, c_i, transmission_rule, r = r, l_max = l_max))

# Save results

output_filename = f'HP_{transmission_rule}' if r is None else f'HP_{transmission_rule}_r{r}'

save_data = dict(
    N = N, T = T, X = X, l_0 = l_0, c_s = c_s, c_i = c_i,

    simulations_number = simulations_number,

    mean_cultural_complexities = np.mean(mean_cultural_complexities, axis = 0)
)

if r is not None:
    save_data['r'] = r

    save_data['l_max'] = l_max

np.savez(output_filename, **save_data)
