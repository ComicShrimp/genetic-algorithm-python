import random
import time
from collections import namedtuple
from random import choices, randint, randrange
from typing import List, Tuple

Product = namedtuple("Product", ["name", "volume", "value"])
Genome = List[int]
Population = List[Genome]

products = [
    Product("Iphone 6", 0.0000899, 2199.12),
    Product("Notebook Dell", 0.00350, 2499.90),
    Product("Tv 42", 0.200, 2999.90),
    Product("TV 50", 0.290, 3999.90),
    Product("TV 55", 0.400, 4346.99),
    Product("Microondas Panasonic", 0.0319, 299.29),
    Product("Microondas LG", 0.0544, 429.90),
    Product("Notebook Asus", 0.527, 3999),
    Product("Microondas Electrolux", 0.0424, 308.66),
    Product("Notebook Lenovo", 0.498, 1999.90),
    Product("Geladeira Consul", 0.870, 1199.89),
    Product("Geladeira Brastemp", 0.635, 849),
    Product("Geladeira Dako", 0.751, 999.90),
    Product("Ventilador Panasonic", 0.496, 199.90),
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

    def __single_point_crossover(self, a: Genome, b: Genome) -> Tuple[Genome, Genome]:
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
    for i, product in enumerate(products):
        if genome[i] == 1:
            result += [product.name]

    return result


def genome_to_values(genome: Genome, products: List[Product]) -> Tuple[float, float]:
    volume = 0
    value = 0
    for i, product in enumerate(products):
        if genome[i] == 1:
            volume += product.volume
            value += product.value

    return volume, value


algorithm = GenecticAlgorithm(
    population_size=10,
    products=products,
    generation_limit=100,
    fitness_limit=24200,
    volume_limit=3,
)
start = time.time()
population, generations = algorithm.run_evolution()
end = time.time()

print(f"number of generations: {generations}")
print(f"time: {end - start}s")
print(f"best solution: {genome_to_things(population[0], products)}")

total_volume, total_value = genome_to_values(population[0], products)
print(f"Total Volume: {total_volume}  -  Total Value: {total_value}")
