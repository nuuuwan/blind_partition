import numpy as np
from gig import Ent


def partition_population(ent_list) -> int:
    return sum([ent.population for ent in ent_list])


def binary_split(splitable_list: list, n1, n2) -> list[list, list]:
    sorted_splitable_list = sorted(
        splitable_list, key=lambda ent: ent.centroid[1]
    )
    total_population = partition_population(sorted_splitable_list)
    split_population = n1 * total_population / (n1 + n2)

    for i, ent in enumerate(sorted_splitable_list):
        if (
            partition_population(sorted_splitable_list[:i])
            >= split_population
        ):
            return sorted_splitable_list[:i], sorted_splitable_list[i:]

    raise Exception('Could not split!')


def build_ent(ent_list: list) -> Ent:
    id = '-'.join([ent.id for ent in ent_list])
    name = '-'.join([ent.name for ent in ent_list])
    centroid = np.mean([ent.centroid for ent in ent_list], axis=0)
    population = partition_population(ent_list)
    return Ent(
        dict(
            id=id,
            name=name,
            centroid=centroid,
            population=population,
        )
    )
