import subprocess
import sys

if len(sys.argv) not in (4, 5):
    sys.exit(1)

simulations_number = sys.argv[1]

topology = sys.argv[2]

transmission_rule = sys.argv[3]

r = sys.argv[4] if len(sys.argv) == 5 else None

average_degrees = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 50, 60, 70, 80, 90]

executable = sys.executable

for average_degree in average_degrees:
    print(f'Average degree = {average_degree}')

    cmd = [executable, 'networks_cumulative_cultural_evolution.py', str(average_degree), str(simulations_number), topology, transmission_rule]

    if r is not None:
        cmd.append(r)

    subprocess.run(cmd)
