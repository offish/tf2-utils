from unittest import TestCase

from src.tf2_utils import BackpackTF


class TestBackpackTF(TestCase):
    def setUp(cls) -> None:
        cls.bptf = BackpackTF("test")
