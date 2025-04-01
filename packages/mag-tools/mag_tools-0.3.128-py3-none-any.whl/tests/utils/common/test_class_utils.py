import unittest
from typing import Optional

from utils.common.class_utils import ClassUtils


class TestClassUtils(unittest.TestCase):
    def test_get_origin_type(self):
        print(ClassUtils.get_origin_type(Optional[str]))
        print(ClassUtils.get_origin_type(Optional[int]))