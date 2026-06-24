# Cumulative Cultural Evolution in Structured Populations

Simulation code used in the paper **"Cumulative Cultural Evolution in Structured Populations"** (Leite, Reia, Mesoudi & Campos, 2026).

The model extends the cumulative cultural evolution (CCE) framework proposed by Mesoudi (2011) to populations structured by social networks, examining how network topology, average connectivity, and the social transmission rule (unbiased, indirect bias, and direct bias) affect the accumulation of cultural complexity over time.

## Model overview

In each generation, individuals have an effort budget (`λ`) that can be spent on two activities:

- **Social copying**: reproducing cultural traits acquired by one or more individuals from the previous generation, at a cost `c_s` per trait copied.
- **Innovation**: if effort remains after copying, the individual attempts to acquire new traits on their own, at a cost `c_i` per attempt.

Traits have a fixed fitness (payoff) value, drawn from an exponential distribution squared, multiplied by 2, and rounded. An individual's cultural complexity is the sum of the fitness of all acquired traits, organized into sequential functional levels (the trait at level `s + 1` can only be acquired after level `s`).

Three transmission rules are implemented:

- **`Unbiased`** — each individual copies a single demonstrator chosen at random from the previous generation.
- **`Indirect bias`** — each individual copies all traits of the highest-fitness individual from the previous generation.
- **`Direct bias`** — for each functional level, the individual copies the highest-fitness trait available among all individuals in the previous generation (or neighborhood).

## Repository structure

| File | Description |
|---|---|
| `cumulative_cultural_evolution.py` | Simulation in a homogeneous population (no network structure): every individual can potentially learn from every other individual. |
| `networks_cumulative_cultural_evolution.py` | Simulation on structured networks (Erdős–Rényi, Barabási–Albert, and Watts–Strogatz), for a single average degree value `⟨k⟩`. |
| `parameter_sweep_average_degree.py` | Runs `networks_cumulative_cultural_evolution.py` repeatedly across a list of average degree values. |
| `networks_aggregate_results.py` | Aggregates the `.npz` files produced by `parameter_sweep_average_degree.py` into a single file per topology/transmission rule. |
| `communication_patterns_cumulative_cultural_evolution.py` | Simulation on the eight communication patterns introduced by Mason & Watts (2012), used as a benchmark of structural organization while keeping network size and density fixed. |
| `equilibrium_time.py` | Computes and plots the time to equilibrium (saturation) of mean cultural complexity as a function of average degree, for each topology and transmission rule. |

## Usage

### 1. Homogeneous population

```bash
python cumulative_cultural_evolution.py <simulations_number> <transmission_rule> [r]
```

- `simulations_number`: number of independent runs to be averaged.
- `transmission_rule`: `unbiased`, `indirect_bias`, or `direct_bias`.
- `r` (optional): growth rate of the time-dependent effort budget, which approaches `λ_max` exponentially as cultural complexity increases. If omitted, the budget is fixed (`λ_0 = 1000`, `T = 20`). If provided, the budget grows from `λ_0 = 100` toward `λ_max = 1000` at this rate (`T = 40`).

Without command-line arguments, the script prompts for the same parameters interactively.

Example:

```bash
python cumulative_cultural_evolution.py 1000 direct_bias
python cumulative_cultural_evolution.py 1000 direct_bias 0.01
```

Produces a file `HP_<transmission_rule>.npz` (or `HP_<transmission_rule>_r<r>.npz`) containing mean cultural complexity over time, averaged across simulations.

### 2. Structured networks (single average degree)

```bash
python networks_cumulative_cultural_evolution.py <average_degree> <simulations_number> <topology> <transmission_rule> [r]
```

- `average_degree`: target average degree `⟨k⟩` of the network.
- `topology`: `ER` (Erdős–Rényi), `BA` (Barabási–Albert), or `WS` (Watts–Strogatz, with rewiring probability fixed at 0.1).
- Remaining parameters as above.

Produces `<topology>_<transmission_rule>_<average_degree>.npz` (or with `_r<r>` suffix), containing mean cultural complexity over time and the maximum complexity attained in the final generation, both averaged across simulations.

### 3. Sweep over average degree

Run the script that calls the one above for each value in the list of average degrees:

```bash
python parameter_sweep_average_degree.py <simulations_number> <topology> <transmission_rule> [r]
```

This script runs `networks_cumulative_cultural_evolution.py` for each `average_degree` in `[2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 50, 60, 70, 80, 90]`, producing one `.npz` file per average degree.

### 4. Aggregating results across average degree

After the sweep, aggregate the individual files into a single file per topology/transmission rule:

```bash
python networks_aggregate_results.py
```

The script interactively asks for `topology` and `transmission_rule`, reads all matching `<topology>_<transmission_rule>_<average_degree>.npz` files, and saves `<topology>_<transmission_rule>.npz`, with the list of average degrees and the corresponding mean and maximum complexity curves. This aggregated file is the expected input for `equilibrium_time.py` (step 6).

### 5. Mason–Watts communication patterns

```bash
python communication_patterns_cumulative_cultural_evolution.py <simulations_number> <transmission_rule> [r]
```

Simulates the eight networks A–H (16 nodes, 24 edges each, average degree 3), each designed to maximize or minimize a distinct structural property (betweenness centrality, clustering, closeness centrality, etc.). Produces one `<label>_<transmission_rule>.npz` file per network (`A` through `H`).

### 6. Equilibrium time

```bash
python equilibrium_time.py
```

Reads the aggregated `<topology>_<transmission_rule>.npz` files (step 4) for the three topologies (`ER`, `BA`, `WS`) and the three transmission rules, detects the equilibrium time of each curve — defined as the earliest timestep at which the relative variation within a sliding window of 4 generations falls below 1% — and produces the figure `equilibrium_time.pdf`.

## Notes on parameters

Population size (`N`) and the remaining model parameters (`X`, `c_s`, `c_i`) are set directly inside each script rather than passed as command-line arguments; edit the source code if you need to run with different values.

## Reproducibility

All scripts fix the NumPy and Python `random` module seeds (`seed = 42`) at the start of execution, ensuring reproducible results for any given combination of parameters.

## Reference

Leite, R. N. C. C., Reia, S. M., Mesoudi, A., & Campos, P. R. A. (2026). *Cumulative Cultural Evolution in Structured Populations*. bioRxiv preprint. https://doi.org/10.64898/2026.04.15.718734
