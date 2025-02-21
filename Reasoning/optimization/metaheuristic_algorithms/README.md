Metaheuristic algorithms are a class of optimization algorithms that are used to find solutions to complex problems
They are designed to find good solutions to problems that are difficult to solve to optimality, often with limited resources

Metaheuristics are typically defined by their heuristic nature, emphasizing exploration and exploitation  <b><i>(trial and error)</i> without necessarily modeling the objective function probabilistically or statistically</b>

# characteristics of metaheuristic algorithms
* <b>Stochastic </b> \
They start by generating random results, which helps them avoid premature convergence.
* <b>Derivative-free </b> \
They don't require calculating derivatives in the search space, which makes them simpler and more flexible.
* <b>Balance exploration and profit </b> \
They examine interesting regions of the search space, then perform local searches in those regions.

# examples of metaheuristic algorithms include: 
## Evolutionary Algorithms
Inspired by natural evolution processes like mutation, recombination, and selection.
* <b>Genetic Algorithm (GA) </b> \
Inspired by natural selection and genetics, GA starts by randomly generating a population of solutions, then evolves it using operators like selection, crossover, and mutation.
* <b>Differential Evolution (DE)</b> \
Focuses on population-based optimization with differences between vectors driving evolution.

## Swarm Intelligence-Based Algorithms
Inspired by the collective behavior of social animals or organisms.
* <b><a href="https://github.com/pankajr141/experiments/blob/master/Reasoning/optimization/metaheuristic_algorithms/ch1_particle_swarm_optimization.mdx" target="_blank">Particle Swarm Optimization (PSO)</a></b> \
Inspired by the collective behaviour of social organisms, PSO starts by randomly generating a swarm of particles, each representing a potential solution.
* <b><a href="https://github.com/pankajr141/experiments/blob/master/Reasoning/optimization/metaheuristic_algorithms/ch2_ant_colony_optimization.mdx" target="_blank">Ant Colony Optimization (ACO)</a></b>\
Mimics the behavior of ants finding the shortest path to food sources.
* <b>Artificial Bee Colony (ABC): </b> \
Inspired by the foraging behavior of bees.
* <b>Firefly Algorithm: </b> \
Based on the flashing behavior of fireflies to attract others.

## Physics-Based Algorithms
Inspired by physical processes and phenomena.
* <b>Simulated Annealing (SA) </b> \
Inspired by the annealing process in metallurgy, SA starts by randomly generating an initial solution, then gradually reduces the temperature of the system.
* <b>Gravitational Search Algorithm (GSA) </b> \
Simulates the motion of masses under gravitational attraction.
* <b>Harmony Search (HS) </b> \
Based on musical improvisation processes.

## Biology-Inspired Algorithms
Based on biological processes or mechanisms.
* <b>Genetic Programming (GP) </b> \
Similar to genetic algorithms but evolves computer programs.
* <b>Immune Algorithm </b> \
Mimics the behavior of the immune system in detecting and eliminating pathogens.
* <b>Bacterial Foraging Optimization </b> \
Simulates the movement of bacteria searching for nutrients.

## Nature-Inspired Algorithms
Inspired by natural phenomena or behaviors not specific to biology or physics.
* <b>Cuckoo Search (CS) </b> \
Based on the brood parasitism of certain cuckoo species.
* <b>Grey Wolf Optimizer (GWO) </b> \
Simulates the leadership hierarchy and hunting mechanism of grey wolves.
* <b>Bat Algorithm </b> \
Inspired by the echolocation behavior of bats.

## Human-Inspired Algorithms
Inspired by human problem-solving behavior.
* <b>Tabu Search (TS) </b> \
Inspired by the concept of memory in human decision-making, TS starts by randomly generating an initial solution, then searches the neighbourhood of the solution by applying operators like swapping or reversing.
* <b>Teaching-Learning-Based Optimization (TLBO) </b> \
Models the teaching and learning process in a classroom.
* <b>Cultural Algorithm </b> \
Uses cultural evolution to guide the search process.

## Hybrid Algorithms
Combine features of multiple metaheuristics to leverage their strengths.
* <b>Hybrid GA-PSO </b> \
Combines genetic algorithms and particle swarm optimization.
* <b>ACO-PSO Hybrid </b> \
Combines ant colony optimization and particle swarm optimization.
