from collections import namedtuple
from random import choices
from typing import List

Product = namedtuple("Product", ["name", "volume", "value"])
Genome: List[int]
Population: List[Genome]


class GenecticAlgorithm:
    population: Population
    products: List[Product]
    generation_limit: int
    fitness_limit: int

    def __init__(
        self,
        population_size: int,
        products: List[Product],
        generation_limit: int,
        fitness_limit: int,
    ) -> None:
        self.products = products
        self.population = self.__generate_population(
            population_size, len(self.products)
        )
        self.generation_limit = generation_limit
        self.fitness_limit = fitness_limit

    def __generate_genome(self, length: int) -> Genome:
        return choices([0, 1], k=length)

    def __generate_population(self, size: int, genome_length: int) -> Population:
        return [self.__generate_genome(genome_length) for _ in range(size)]
