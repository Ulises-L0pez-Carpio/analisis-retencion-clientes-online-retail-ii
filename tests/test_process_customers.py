from __future__ import annotations

import unittest

import pandas as pd

from src.process_customers import construir_base_clientes


class ProcessCustomersTests(unittest.TestCase):
    def test_construir_base_clientes_calcula_metricas_principales(self) -> None:
        df = pd.DataFrame(
            {
                "invoice_no": pd.Series(["10001", "10001", "10002", "10003"], dtype="string"),
                "stock_code": pd.Series(["A", "B", "A", "C"], dtype="string"),
                "quantity": pd.Series([1, 2, 1, 3], dtype="Int64"),
                "invoice_datetime": pd.to_datetime(
                    [
                        "2011-01-01 10:00:00",
                        "2011-01-01 10:00:00",
                        "2011-01-11 10:00:00",
                        "2011-02-01 09:00:00",
                    ]
                ),
                "unit_price_gbp": [5.0, 2.5, 5.0, 4.0],
                "customer_id": pd.Series([12345, 12345, 12345, 99999], dtype="Int64"),
                "country": pd.Series(["France", "France", "France", "Spain"], dtype="string"),
                "line_revenue_gbp": pd.Series([5.0, 5.0, 5.0, 12.0], dtype="Float64"),
            }
        )

        resultado = construir_base_clientes(df)
        cliente = resultado.loc[resultado["customer_id"] == 12345].iloc[0]

        self.assertEqual(len(resultado), 2)
        self.assertEqual(cliente["primary_country"], "France")
        self.assertEqual(int(cliente["n_orders"]), 2)
        self.assertEqual(int(cliente["n_lines"]), 3)
        self.assertEqual(int(cliente["n_unique_products"]), 2)
        self.assertEqual(int(cliente["total_quantity"]), 4)
        self.assertAlmostEqual(float(cliente["total_revenue_gbp"]), 15.0)
        self.assertEqual(int(cliente["recency_days"]), 21)
        self.assertTrue(bool(cliente["is_repeat_customer"]))
        self.assertAlmostEqual(float(cliente["avg_days_between_orders"]), 10.0)

    def test_construir_base_clientes_marca_clientes_multicountry(self) -> None:
        df = pd.DataFrame(
            {
                "invoice_no": pd.Series(["10001", "10002", "10003"], dtype="string"),
                "stock_code": pd.Series(["A", "B", "C"], dtype="string"),
                "quantity": pd.Series([1, 1, 1], dtype="Int64"),
                "invoice_datetime": pd.to_datetime(
                    ["2011-01-01 10:00:00", "2011-01-02 10:00:00", "2011-01-03 10:00:00"]
                ),
                "unit_price_gbp": [5.0, 7.0, 6.0],
                "customer_id": pd.Series([12345, 12345, 12345], dtype="Int64"),
                "country": pd.Series(["France", "France", "Spain"], dtype="string"),
                "line_revenue_gbp": pd.Series([5.0, 7.0, 6.0], dtype="Float64"),
            }
        )

        resultado = construir_base_clientes(df)
        cliente = resultado.iloc[0]

        self.assertEqual(int(cliente["n_countries"]), 2)
        self.assertTrue(bool(cliente["has_multiple_countries"]))
        self.assertEqual(cliente["primary_country"], "France")
        self.assertEqual(int(cliente["primary_country_line_count"]), 2)


if __name__ == "__main__":
    unittest.main()
