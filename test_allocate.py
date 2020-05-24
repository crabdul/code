from datetime import date, timedelta

import pytest

# from model import ...
from model import Batch, OrderLine, OutOfStock, allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("order-1", "RETRO-CLOCK", 50)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 50
    assert shipment_batch.available_quantity == 100


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch1", "small-fork", 10, eta=today)
    allocate(OrderLine("order-1", "small-fork", 10), [batch])

    with pytest.raises(OutOfStock, match="small-fork"):
        allocate(OrderLine("order-1", "small-fork", 1), [batch])
