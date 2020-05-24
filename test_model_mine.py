from datetime import date, timedelta

import pytest

# from model import ...
from model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "small-table", 20, date.today())
    line = OrderLine("order-ref", "small-table", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def test_allocating_to_a_batch_with_less_quantity_than_required_by_line():
    batch = Batch("batch-001", "small-table", qty=1, eta=date.today())
    line = OrderLine("order-ref", "small-table", 2)

    try:
        batch.allocate(line)
    except Batch.InsufficentQuantityException:
        assert True

    assert batch.available_quantity == 1


def test_can_allocate_if_quantity_equal_to_required():
    batch = Batch("batch-001", "small-table", qty=2, eta=date.today())
    line = OrderLine("order-ref", "small-table", 2)

    batch.allocate(line)

    assert batch.available_quantity == 0
