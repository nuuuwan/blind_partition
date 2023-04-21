from functools import cached_property

from gig import Ent, EntType


class Partition:
    def __init__(
        self, region_id: str, sub_region_type: EntType, n_partitions: int
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
