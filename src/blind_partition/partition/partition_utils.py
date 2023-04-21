import json

import numpy as np
from gig import Ent
from utils import TSVFile


def partition_population(ent_list) -> int:
    return sum([ent.population for ent in ent_list])


def binary_split(splitable_list: list, n: int) -> list[list, list]:
    assert n >= 2
    sorted_splitable_list = sorted(
        splitable_list, key=lambda ent: ent.centroid[1]
    )
    total_population = partition_population(sorted_splitable_list)
    n1 = int(n / 2)
    split_population = n1 * total_population / (n)

    for i, ent in enumerate(sorted_splitable_list):
        if (
            partition_population(sorted_splitable_list[:i])
            >= split_population
        ):
            return [sorted_splitable_list[:i], sorted_splitable_list[i:]]

    raise Exception('Could not split!')


def split(splitable_list: list, n: int) -> list[list]:
    if n == 1:
        return [splitable_list]
    elif n == 2:
        return binary_split(splitable_list, n)
    else:
        n1 = int(n / 2)
        n2 = n - n1
        split_list1, split_list2 = binary_split(splitable_list, n)
        return split(split_list1, n1) + split(split_list2, n2)


def build_ent(ent_list: list) -> Ent:
    id = '-'.join([ent.id for ent in ent_list])
    name = '-'.join([ent.name for ent in ent_list])
    centroid = list(np.mean([ent.centroid for ent in ent_list], axis=0))
    population = partition_population(ent_list)
    return Ent(
        dict(
            id=id,
            name=name,
            centroid=centroid,
            population=population,
        )
    )


def store_ents(ent_list, tsv_file):
    d_list = [ent.d for ent in ent_list]
    TSVFile(tsv_file).write(d_list)


def ent_from_d(d):
    return Ent(
        dict(
            id=d['id'],
            name=d['name'],
            centroid=json.loads(d['centroid']),
            population=int(d['population']),
        )
    )


def load_ents(tsv_file):
    d_list = TSVFile(tsv_file).read()
    return [ent_from_d(d) for d in d_list]
