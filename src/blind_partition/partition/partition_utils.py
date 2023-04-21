import colorsys
import json
import random

import geopandas as gpd
import numpy as np
import shapely
from gig import Ent
from matplotlib import pyplot as plt
from shapely.ops import unary_union
from utils import TSVFile


def get_random_color():
    h = random.random()
    hls = (h, 0.5, 1.0)
    rgb = colorsys.hls_to_rgb(*hls)
    hex = '#%02x%02x%02x' % tuple([int(255 * x) for x in rgb])
    return hex


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


def build_ent(id, ent_list: list) -> Ent:
    sorted_names_and_population = sorted(
        [(ent.name, ent.population) for ent in ent_list],
        key=lambda x: x[1],
        reverse=True,
    )
    name = sorted_names_and_population[0][0]
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


def get_merged_polygon_list(ent_list):
    all_polygon_list = []
    for ent in ent_list:
        polygon_list = list(
            map(
                lambda polygon_data: shapely.Polygon(polygon_data).buffer(
                    0.00001
                ),
                ent.get_raw_geo(),
            )
        )
        all_polygon_list += polygon_list
    shape = unary_union(all_polygon_list)

    polygon_list = (
        list(shape.geoms)
        if isinstance(shape, shapely.MultiPolygon)
        else [shape]
    )
    return [list(polygon.exterior.coords) for polygon in polygon_list]


def polygon_list_to_geojson(polygon_list) -> gpd.GeoDataFrame:
    polygon_list_ = [shapely.Polygon(polygon) for polygon in polygon_list]
    return gpd.GeoDataFrame(
        geometry=polygon_list_,
        crs='epsg:4326',
    )


def draw(gdf, ax):
    gdf.plot(ax=ax, color=get_random_color())


def draw_all(gdf_list, png_path):
    fig, ax = plt.subplots()
    for gdf in gdf_list:
        draw(gdf, ax)
    plt.savefig(png_path)
