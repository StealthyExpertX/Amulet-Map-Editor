import sys
import os

try:
    import api
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

import unittest

from api.selection import SubBox, SelectionBox
from api.chunk import SubChunk
from api import world_loader
from test_utils import get_world_path


class AnvilWorldTestCase(unittest.TestCase):
    def setUp(self):
        self.world = world_loader.loader.load_world(get_world_path("1.12.2 World"))

    def tearDown(self):
        self.world.exit()

    def test_get_block(self):
        self.assertEqual("minecraft:air", self.world.get_block(0, 0, 0))
        self.assertEqual("minecraft:stone", self.world.get_block(1, 70, 3))
        self.assertEqual("minecraft:granite", self.world.get_block(1, 70, 5))
        self.assertEqual("minecraft:polished_granite", self.world.get_block(1, 70, 7))

        with self.assertRaises(IndexError):
            self.world.get_block(300, 300, 300)

    def test_get_blocks(self):
        self.assertIsInstance(
            next(self.world.get_sub_chunks(slice(0, 10), slice(0, 10), slice(0, 10))),
            SubChunk,
        )
        self.assertIsInstance(
            next(self.world.get_sub_chunks(0, 0, 0, 10, 10, 10)), SubChunk
        )
        self.assertIsInstance(
            next(self.world.get_sub_chunks(0, 0, 0, 10, 10, 10, 2, 2, 2)), SubChunk
        )

        with self.assertRaises(IndexError):
            next(self.world.get_sub_chunks())

            next(self.world.get_sub_chunks(slice(0, 10, 2)))
            next(self.world.get_sub_chunks(slice(0, 10, 2), slice(0, 10, 2)))

            next(self.world.get_sub_chunks(0))
            next(self.world.get_sub_chunks(0, 0))
            next(self.world.get_sub_chunks(0, 0, 0))

    def test_clone_operation(self):

        subbx1 = SubBox((1, 70, 3), (1, 70, 4))
        src_box = SelectionBox((subbx1,))

        subbx2 = SubBox((1, 70, 5), (1, 70, 6))
        target_box = SelectionBox((subbx2,))

        self.assertEqual(
            self.world.get_block(1, 70, 3), "minecraft:stone"
        )  # Sanity check
        self.assertEqual(self.world.get_block(1, 70, 5), "minecraft:granite")

        self.world.run_operation_from_operation_name("clone", src_box, target_box)

        self.assertEqual("minecraft:stone", self.world.get_block(1, 70, 5))

        self.world.undo()

        self.assertEqual("minecraft:granite", self.world.get_block(1, 70, 5))

        self.world.redo()

        self.assertEqual("minecraft:stone", self.world.get_block(1, 70, 5))

        self.world.undo()

        self.assertEqual("minecraft:granite", self.world.get_block(1, 70, 5))

    def test_fill_operation(self):

        subbox_1 = SubBox((1, 70, 3), (5, 71, 5))
        box = SelectionBox((subbox_1,))

        self.world.run_operation_from_operation_name("fill", box, "minecraft:stone")

        for x, y, z in box:
            self.assertEqual("minecraft:stone", self.world.get_block(x, y, z))

        self.world.undo()

        self.assertEqual("minecraft:stone", self.world.get_block(1, 70, 3))
        self.assertEqual("minecraft:granite", self.world.get_block(1, 70, 5))


class Anvil2WorldTestCase(unittest.TestCase):
    def setUp(self):
        self.world = world_loader.loader.load_world(get_world_path("1.13 World"))

    def test_get_block(self):
        self.assertEqual("minecraft:air", self.world.get_block(0, 0, 0))
        self.assertEqual("minecraft:stone", self.world.get_block(1, 70, 3))
        self.assertEqual("minecraft:granite", self.world.get_block(1, 70, 5))
        self.assertEqual("minecraft:polished_granite", self.world.get_block(1, 70, 7))

        with self.assertRaises(IndexError):
            self.world.get_block(300, 300, 300)

    def test_get_blocks(self):
        self.assertIsInstance(
            next(self.world.get_sub_chunks(slice(0, 10), slice(0, 10), slice(0, 10))),
            SubChunk,
        )
        self.assertIsInstance(
            next(self.world.get_sub_chunks(0, 0, 0, 10, 10, 10)), SubChunk
        )
        self.assertIsInstance(
            next(self.world.get_sub_chunks(0, 0, 0, 10, 10, 10, 2, 2, 2)), SubChunk
        )

        with self.assertRaises(IndexError):
            next(self.world.get_sub_chunks())

            next(self.world.get_sub_chunks(slice(0, 10, 2)))
            next(self.world.get_sub_chunks(slice(0, 10, 2), slice(0, 10, 2)))

            next(self.world.get_sub_chunks(0))
            next(self.world.get_sub_chunks(0, 0))
            next(self.world.get_sub_chunks(0, 0, 0))

    def test_clone_operation(self):

        subbx1 = SubBox((1, 70, 3), (1, 70, 4))
        src_box = SelectionBox((subbx1,))

        subbx2 = SubBox((1, 70, 5), (1, 70, 6))
        target_box = SelectionBox((subbx2,))

        self.assertEqual(
            "minecraft:stone", self.world.get_block(1, 70, 3)
        )  # Sanity check
        self.assertEqual("minecraft:granite", self.world.get_block(1, 70, 5))

        self.world.run_operation_from_operation_name("clone", src_box, target_box)

        self.assertEqual("minecraft:stone", self.world.get_block(1, 70, 5))

        self.world.undo()

        self.assertEqual("minecraft:granite", self.world.get_block(1, 70, 5))

        self.world.redo()

        self.assertEqual("minecraft:stone", self.world.get_block(1, 70, 5))

        self.world.undo()

        self.assertEqual("minecraft:granite", self.world.get_block(1, 70, 5))

    def test_fill_operation(self):

        subbox_1 = SubBox((1, 70, 3), (5, 71, 5))
        box = SelectionBox((subbox_1,))

        self.world.run_operation_from_operation_name("fill", box, "minecraft:stone")

        for x, y, z in box:
            self.assertEqual(
                "minecraft:stone",
                self.world.get_block(x, y, z),
                f"Failed at coordinate ({x},{y},{z})",
            )

        self.world.undo()

        self.assertEqual("minecraft:stone", self.world.get_block(1, 70, 3))
        self.assertEqual("minecraft:granite", self.world.get_block(1, 70, 5))


if __name__ == "__main__":
    unittest.main()
