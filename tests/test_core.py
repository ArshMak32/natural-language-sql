import unittest
from unittest.mock import patch
from core import execute, benchmark, generate


class SQLTests(unittest.TestCase):
    def test_join_totals(self):
        self.assertEqual(
            execute("SELECT SUM(quantity*unit_price) AS x FROM order_items").iloc[0, 0],
            4030,
        )

    def test_references(self):
        self.assertEqual(benchmark()["correct"], 12)

    def test_attack_queries(self):
        for q in [
            "DELETE FROM orders",
            "SELECT * FROM orders; DROP TABLE orders",
            "SELECT * FROM sqlite_master",
            "SELECT load_extension('x')",
            "SELECT * FROM pragma_database_list",
            "SELECT randomblob(1000000000)",
        ]:
            with self.subTest(q=q), self.assertRaises(Exception):
                execute(q)

    def test_row_limit(self):
        with self.assertRaises(ValueError):
            execute("SELECT * FROM orders", max_rows=1)

    def test_missing_credentials(self):
        with patch.dict("os.environ", {}, clear=True), self.assertRaises(ValueError):
            generate("total revenue")
