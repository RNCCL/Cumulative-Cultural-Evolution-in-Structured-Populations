import numpy as np

average_degrees = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 50, 60, 70, 80, 90]

topology = input('Topology: ')

transmission_rule = input('Transmission rule: ')

average_degree_mean_cultural_complexities, average_degree_maximum_cultural_complexities = [], []

for average_degree in average_degrees:
    filename = f'{topology}_{transmission_rule}_{average_degree}.npz'

    try:
        data = np.load(filename)

        average_degree_mean_cultural_complexities.append(data['average_degree_mean_cultural_complexities'])

        average_degree_maximum_cultural_complexities.append(data['average_degree_maximum_cultural_complexity'])

    except FileNotFoundError:
        print(f'File not found: {filename}')

        continue

np.savez(
    f'{topology}_{transmission_rule}.npz',

    N = data['N'], T = data['T'], X = data['X'], l_0 = data['l_0'], c_s = data['c_s'], c_i = data['c_i'],

    simulations_number = data['simulations_number'],

    average_degrees = average_degrees,

    average_degree_mean_cultural_complexities = average_degree_mean_cultural_complexities,

    average_degree_maximum_cultural_complexities = average_degree_maximum_cultural_complexities
)
