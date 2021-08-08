import random
import time
from collections import namedtuple
from random import choices, randint, randrange
from typing import List, Tuple

Product = namedtuple("Product", ["name", "volume", "value"])
Genome = List[int]
Population = List[Genome]

products = [
    Product("Laptop", 2200, 500),
    Product("Headphones", 160, 150),
    Product("Coffe Mug", 350, 60),
    Product("Notepad", 333, 40),
    Product("Water Bottle", 192, 30),
]


class GenecticAlgorithm:
    population_size: int
    products: List[Product]
    generation_limit: int
    fitness_limit: int
    volume_limit: int
    num_mutations: int
    probability: float

    def __init__(
        self,
        population_size: int,
        products: List[Product],
        generation_limit: int,
        fitness_limit: int,
        volume_limit: int,
        num_mutations: int = 1,
        propability: float = 0.5,
    ) -> None:
        self.population_size = population_size
        self.products = products
        self.generation_limit = generation_limit
        self.fitness_limit = fitness_limit
        self.volume_limit = volume_limit
        self.num_mutations = num_mutations
        self.probability = propability

    def __generate_genome(self, length: int) -> Genome:
        return choices([0, 1], k=length)

    def __generate_population(self) -> Population:
        return [
            self.__generate_genome(len(self.products))
            for _ in range(self.population_size)
        ]

    def __fitness_function(self, genome: Genome) -> int:
        volume = 0
        value = 0

        for i, product in enumerate(self.products):
            if genome[i] == 1:
                volume += product.volume
                value += product.value

                if volume > self.volume_limit:
                    return 0

        return value

    def __selection_pair(self, population: Population) -> Population:
        return choices(
            population=population,
            weights=[self.__fitness_function(genome) for genome in population],
            k=2,
        )

    def __single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
        length = len(a)

        if length < 2:
            return a, b

        p = randint(1, length - 1)
        return a[0:p] + b[p:], b[0:p] + a[p:]

    def __mutation(self, genome: Genome) -> Genome:
        for _ in range(self.num_mutations):
            index = randrange(len(genome))
            genome[index] = (
                genome[index]
                if random.random() > self.probability
                else abs(genome[index] - 1)
            )

        return genome

    def run_evolution(self) -> Tuple[Population, int]:
        population = self.__generate_population()

        for i in range(self.generation_limit):
            population = sorted(
                population,
                key=lambda genome: self.__fitness_function(genome),
                reverse=True,
            )

            if self.__fitness_function(population[0]) >= self.fitness_limit:
                break

            next_generation = population[0:2]

            for j in range(int(len(population) / 2) - 1):
                parents = self.__selection_pair(population)
                offspring_a, offspring_b = self.__single_point_crossover(
                    parents[0], parents[1]
                )
                offspring_a = self.__mutation(offspring_a)
                offspring_b = self.__mutation(offspring_b)
                next_generation += [offspring_a, offspring_b]

            population = next_generation

        population = sorted(
            population, key=lambda genome: self.__fitness_function(genome), reverse=True
        )

        return population, i


def genome_to_things(genome: Genome, products: List[Product]) -> List[Product]:
    result = []
    for i, thing in enumerate(products):
        if genome[i] == 1:
            result += [thing.name]

    return result


algorithm = GenecticAlgorithm(10, products, 100, 740, 3000)
start = time.time()
population, generations = algorithm.run_evolution()
end = time.time()

print(f"number of generations: {generations}")
print(f"time: {end - start}s")
print(f"best solution: {genome_to_things(population[0], products)}")
