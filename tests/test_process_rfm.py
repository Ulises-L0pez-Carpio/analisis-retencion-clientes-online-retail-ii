from __future__ import annotations

import unittest

import pandas as pd

from src.process_rfm import construir_base_rfm


class ProcessRfmTests(unittest.TestCase):
    def test_construir_base_rfm_calcula_metricas_y_scores(self) -> None:
        df = pd.DataFrame(
            {
                "invoice_no": pd.Series(
                    ["A-001", "A-001", "A-002", "B-001", "X-001", "D-001", "E-001"],
                    dtype="string",
                ),
                "invoice_datetime": pd.to_datetime(
                    [
                        "2011-01-01 10:00:00",
                        "2011-01-01 10:00:00",
                        "2011-02-09 09:00:00",
                        "2011-01-28 11:00:00",
                        "2011-02-01 08:30:00",
                        "2011-02-07 12:00:00",
                        "2011-02-10 15:00:00",
                    ]
                ),
                "quantity": pd.Series([1, 2, 1, 1, 2, 1, 3], dtype="Int64"),
                "unit_price_gbp": [10.0, 5.0, 20.0, 5.0, 7.5, 8.0, 12.0],
                "customer_id": pd.Series([1, 1, 1, 2, 3, 4, 5], dtype="Int64"),
                "line_revenue_gbp": pd.Series(
                    [10.0, 10.0, 20.0, 5.0, 15.0, 8.0, 36.0], dtype="Float64"
                ),
            }
        )

        resultado = construir_base_rfm(df)
        cliente_1 = resultado.loc[resultado["customer_id"] == 1].iloc[0]
        cliente_5 = resultado.loc[resultado["customer_id"] == 5].iloc[0]

        self.assertEqual(len(resultado), 5)
        self.assertEqual(str(cliente_1["snapshot_date"]), "2011-02-10")
        self.assertEqual(int(cliente_1["recency_days"]), 1)
        self.assertEqual(int(cliente_1["frequency_orders"]), 2)
        self.assertAlmostEqual(float(cliente_1["monetary_gbp"]), 40.0)
        self.assertEqual(str(cliente_1["rfm_score"]), "455")
        self.assertEqual(str(cliente_1["rfm_segment"]), "champions")
        self.assertEqual(int(cliente_5["recency_days"]), 0)
        self.assertEqual(int(cliente_5["r_score"]), 5)

    def test_construir_base_rfm_segmenta_cliente_de_una_sola_compra(self) -> None:
        df = pd.DataFrame(
            {
                "invoice_no": pd.Series(["A-001", "B-001"], dtype="string"),
                "invoice_datetime": pd.to_datetime(
                    ["2011-01-01 10:00:00", "2011-02-01 10:00:00"]
                ),
                "quantity": pd.Series([1, 1], dtype="Int64"),
                "unit_price_gbp": [5.0, 10.0],
                "customer_id": pd.Series([10, 20], dtype="Int64"),
                "line_revenue_gbp": pd.Series([5.0, 10.0], dtype="Float64"),
            }
        )

        resultado = construir_base_rfm(df)

        self.assertEqual(len(resultado), 2)
        self.assertTrue(resultado["rfm_segment"].notna().all())
        self.assertTrue(resultado["rfm_score"].notna().all())

    def test_construir_base_rfm_rechaza_filas_invalidas(self) -> None:
        df = pd.DataFrame(
            {
                "invoice_no": pd.Series(["A-001", "C-002"], dtype="string"),
                "invoice_datetime": pd.to_datetime(
                    ["2011-01-01 10:00:00", "2011-02-01 10:00:00"]
                ),
                "quantity": pd.Series([1, -1], dtype="Int64"),
                "unit_price_gbp": [5.0, 10.0],
                "customer_id": pd.Series([10, 20], dtype="Int64"),
                "line_revenue_gbp": pd.Series([5.0, -10.0], dtype="Float64"),
            }
        )

        with self.assertRaisesRegex(ValueError, "compras validas"):
            construir_base_rfm(df)


if __name__ == "__main__":
    unittest.main()
