import math
import os
import statistics
from unittest import TestCase

from gig import EntType

from blind_partition import Partition
from blind_partition.partition import partition_utils

(
    TEST_REGION_ID,
    TEST_SUB_REGION_TYPE,
    TEST_N_PARTITIONS,
    TEST_NEW_ENT_TYPE_NAME,
) = (
    'LK-11',
    EntType('dsd'),
    2,
    'dsd2',
)
TEST_PARTITION = Partition(
    TEST_REGION_ID,
    TEST_SUB_REGION_TYPE,
    TEST_N_PARTITIONS,
    TEST_NEW_ENT_TYPE_NAME,
)


class TestPartition(TestCase):
    def test_init(self):
        partition = TEST_PARTITION
        self.assertEqual(partition.region_id, TEST_REGION_ID)

    def test_sub_region_ent_list(self):
        partition = TEST_PARTITION
        self.assertEqual(len(partition.sub_region_ent_list), 13)

    def test_ents(self):
        partition = TEST_PARTITION
        self.assertEqual(len(partition.ents), 2)


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
            partition.sub_region_ent_list, 2
        )

        d = math.log(
            partition_utils.partition_population(ent_list1)
            / partition_utils.partition_population(ent_list2),
            2,
        )
        self.assertLess(abs(d), 0.2)

    def test_split(self):
        partition = TEST_PARTITION
        n = 5
        ent_list_list = partition_utils.split(
            partition.sub_region_ent_list, n
        )
        population_list = [
            partition_utils.partition_population(ent_list)
            for ent_list in ent_list_list
        ]
        mean = statistics.mean(population_list)
        stdev = statistics.stdev(population_list)
        cov = stdev / mean
        self.assertEqual(len(population_list), n)
        self.assertLess(cov, 0.2)

    def test_build_ent(self):
        partition = TEST_PARTITION
        ent_list1, _ = partition_utils.binary_split(
            partition.sub_region_ent_list, 2
        )
        ent1 = partition_utils.build_ent(ent_list1)
        self.assertEqual(
            ent1.population, partition_utils.partition_population(ent_list1)
        )

    def test_store_load_ents(self):
        partition = TEST_PARTITION
        ents = partition.ents
        tsv_file = os.path.join('data', 'test_ent.tsv')
        partition_utils.store_ents(ents, tsv_file)
        ents2 = partition_utils.load_ents(tsv_file)
        self.assertEqual(ents, ents2)
