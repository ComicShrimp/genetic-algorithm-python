from random import choices
from typing import List


genome = List[int]

def generate_genome(length: int) -> genome:
    return choices([0, 1], k=length)