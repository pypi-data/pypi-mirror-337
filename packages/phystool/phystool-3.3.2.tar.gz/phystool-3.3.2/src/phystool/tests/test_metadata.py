from unittest import TestCase

from phystool.tags import Tags
from phystool.metadata import Metadata
from phystool.pdbfile import VALID_TYPES


class TestMetadata(TestCase):
    @classmethod
    def setUp(cls):
        cls._metadata = Metadata()

    def test_filter(self):
        include_tags = Tags.validate("A1,B1")
        exclude_tags = Tags.validate("C2")

        filtered = self._metadata.filter(
            "",
            VALID_TYPES,
            include_tags,
            exclude_tags
        )
        self.assertEqual(len(filtered), 2)
        for pdb_file in filtered:
            self.assertTrue(pdb_file.tags.exclude(Tags({})))
            self.assertTrue(pdb_file.tags.exclude(exclude_tags))
            self.assertTrue(pdb_file.tags.include(include_tags))
            self.assertTrue(pdb_file.tags.include(Tags({})))
