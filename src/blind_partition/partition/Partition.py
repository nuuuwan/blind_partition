from functools import cached_property

from gig import Ent, EntType

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

    @cached_property
    def sub_region_ent_list(self) -> list[Ent]:
        sub_region_ents_all = Ent.list_from_type(self.sub_region_type)
        sub_region_ents = [
            ent for ent in sub_region_ents_all if self.region_id in ent.id
        ]
        return sub_region_ents

    @cached_property
    def ents(self) -> list[Ent]:
        ent_list_list = partition_utils.split(
            self.sub_region_ent_list, self.n_partitions
        )
        ents = [
            partition_utils.build_ent(ent_list) for ent_list in ent_list_list
        ]
        return ents
