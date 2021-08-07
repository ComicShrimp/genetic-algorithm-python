from collections import namedtuple
from random import choices
from typing import List

Product = namedtuple("Product", ["name", "volume", "value"])
Genome: List[int]


class GenecticAlgorithm:
    genome: Genome
    population: List[Genome]
    products: List[Product]

    def __init__(self) -> None:
        pass

    def __create_genome(length: int) -> Genome:
        return choices([0, 1], k=length)
