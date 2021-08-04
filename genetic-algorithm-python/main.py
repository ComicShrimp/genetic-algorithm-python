import random
from collections import namedtuple
from random import choices, randint, randrange
from typing import Callable, List, Tuple

genome = List[int]
population = List[genome]
FitnessFunc = Callable[[genome], int]

Thing = namedtuple("Thing", ["name", "value", "weight"])

things = [
    Thing("Laptop", 500, 2200),
    Thing("Headphones", 150, 160),
    Thing("Coffe Mug", 60, 350),
    Thing("Notepad", 40, 333),
    Thing("Water Bottle", 30, 192),
]

more_things = [
    Thing("Mints", 5, 25),
    Thing("Socks", 10, 38),
    Thing("Tissues", 15, 80),
    Thing("Phone", 500, 200),
    Thing("Baseball Cap", 100, 70),
] + things


def generate_genome(length: int) -> genome:
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> population:
    return [generate_genome(genome_length) for _ in range(size)]


def fitness(genome: genome, things: List[Thing], weight_limit: int) -> int:
    if len(genome) != len(things):
        raise ValueError("genome and things must be of the same length")

    weight = 0
    value = 0

    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0

    return value


def selection_pair(population: population, fitness_func: FitnessFunc) -> population:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2,
    )


def single_point_crossover(a: genome, b: genome) -> Tuple[genome, genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be the same length")

    length = len(a)

    if length < 2:
        return a, b

    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(genome: genome, num: int = 1, probability: float = 0.5) -> genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)

    return genome
