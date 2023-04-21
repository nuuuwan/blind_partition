import os
import shutil
from functools import cached_property

from gig import Ent, EntType
from utils import JSONFile

from blind_partition.partition import partition_utils


class Partition:
    def __init__(
        self,
        region_id: str,
        sub_region_type: EntType,
        n_partitions: int,
        new_ent_type_name: str,
    ):
        self.region_id = region_id
        self.sub_region_type = sub_region_type
        self.n_partitions = n_partitions
        self.new_ent_type_name = new_ent_type_name

    @cached_property
    def data_path(self):
        return os.path.join('data', f'{self.new_ent_type_name}')

    @cached_property
    def sub_region_ent_list(self) -> list[Ent]:
        sub_region_ents_all = Ent.list_from_type(self.sub_region_type)
        sub_region_ents = [
            ent for ent in sub_region_ents_all if self.region_id in ent.id
        ]
        return sub_region_ents

    @cached_property
    def ent_list_list(self) -> list[list]:
        return partition_utils.split(
            self.sub_region_ent_list, self.n_partitions
        )

    @cached_property
    def ents(self) -> list[Ent]:
        ents = [
            partition_utils.build_ent(
                f'{self.new_ent_type_name}-{x[0]}', x[1]
            )
            for x in enumerate(self.ent_list_list)
        ]
        return ents

    def build(self):
        if os.path.exists(self.data_path):
            shutil.rmtree(self.data_path)
        os.mkdir(self.data_path)

        tsv_path = os.path.join(self.data_path, 'ents.tsv')
        partition_utils.store_ents(self.ents, tsv_path)

        gdf_list = []
        for ent, ent_list in zip(self.ents, self.ent_list_list):
            id = ent.id
            polygon_list = partition_utils.get_merged_polygon_list(ent_list)
            polygon_path = os.path.join(
                self.data_path, f'polygon_list.{id}.json'
            )
            JSONFile(polygon_path).write(polygon_list)

            gdf = partition_utils.polygon_list_to_geojson(polygon_list)
            geojson_path = os.path.join(self.data_path, f'geojson.{id}.json')
            gdf.to_file(geojson_path, driver='GeoJSON')

            gdf_list.append(gdf)

        png_path = os.path.join(self.data_path, 'map.png')
        partition_utils.draw_all(gdf_list, png_path)
