import unittest
from unittest.mock import MagicMock

from adapter.repositories.order_repository import OrderRepository
from core.application.use_cases.order.order_case import OrderCase
from core.domain.entities.order import OrderIN, OrderOUT
from core.domain.exceptions.exception import ObjectNotFound


class TestOrderCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock(spec=OrderRepository)
        self.product_case = OrderCase(db=None)
        self.product_case.repository = self.mock_repo

    def test_get_all(self):
        self.mock_repo.get_all.return_value = ["Order1", "Order2"]
        result = self.product_case.get_all()
        self.assertEqual(result, ["Order1", "Order2"])
        self.mock_repo.get_all.assert_called_once()

    def test_get_by_id_found(self):
        self.mock_repo.get_by_id.return_value = "Order1"
        result = self.product_case.get_by_id(1)
        self.assertEqual(result, "Order1")
        self.mock_repo.get_by_id.assert_called_once_with(1)

    def test_get_by_id_not_found(self):
        self.mock_repo.get_by_id.return_value = None
        with self.assertRaises(ObjectNotFound):
            self.product_case.get_by_id(1)
        self.mock_repo.get_by_id.assert_called_once_with(1)

    def test_update(self):
        order_update_in = MagicMock(spec=OrderIN)
        order_update_in.model_dump.return_value = {"total": 25}

        product_out = MagicMock(spec=OrderOUT)
        self.mock_repo.update.return_value = product_out

        result = self.product_case.update(1, order_update_in)
        self.assertEqual(result, product_out)
        self.mock_repo.update.assert_called_once_with(1, {"total": 25})

    def test_delete(self):
        self.mock_repo.delete.return_value = "Deleted"
        result = self.product_case.delete(1)
        self.assertEqual(result, "Deleted")
        self.mock_repo.delete.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
