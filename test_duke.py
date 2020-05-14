import random

import pytest

from duke import *


def test_prepend_tab():
    assert prepend_tab("hello") == "\thello"