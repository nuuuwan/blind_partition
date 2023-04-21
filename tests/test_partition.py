import math
from unittest import TestCase

from gig import EntType

from blind_partition import Partition
from blind_partition.partition import partition_utils

TEST_REGION_ID, TEST_SUB_REGION_TYPE, TEST_N_PARTITIONS = (
    'LK-11',
    EntType('dsd'),
    2,
)
TEST_PARTITION = Partition(
    TEST_REGION_ID, TEST_SUB_REGION_TYPE, TEST_N_PARTITIONS
)


class TestPartition(TestCase):
    def test_init(self):
        partition = TEST_PARTITION
        self.assertEqual(partition.region_id, TEST_REGION_ID)

    def test_sub_region_ent_list(self):
        partition = TEST_PARTITION
        self.assertEqual(len(partition.sub_region_ent_list), 13)


class TestPartitionUtils(TestCase):
    def test_partition_population(self):
        partition = TEST_PARTITION
        self.assertEqual(
            partition_utils.partition_population(
                partition.sub_region_ent_list
            ),
            2323964,
        )

    def test_binary_split(self):
        partition = TEST_PARTITION
        ent_list1, ent_list2 = partition_utils.binary_split(
            partition.sub_region_ent_list, 1, 1
        )

        for ent in ent_list1:
            print(ent.name)
        print('...')
        for ent in ent_list2:
            print(ent.name)

        d = math.log(
            partition_utils.partition_population(ent_list1)
            / partition_utils.partition_population(ent_list2),
            2,
        )
        print(d)
        self.assertLess(abs(d), 0.2)
