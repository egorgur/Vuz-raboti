import pytest
from .entities import TChessField


@pytest.fixture
def board():
    return [[TChessField(r, c) for c in range(8)] for r in range(8)]
