from __future__ import annotations

import unittest

import pandas as pd

from src.process_cohorts import construir_base_cohortes


class ProcessCohortsTests(unittest.TestCase):
    def test_construir_base_cohortes_calcula_retencion_global(self) -> None:
        customers = pd.DataFrame(
            {
                "customer_id": pd.Series([1, 2, 3], dtype="Int64"),
                "primary_country": pd.Series(["France", "Spain", "France"], dtype="string"),
                "n_countries": pd.Series([1, 1, 1], dtype="Int64"),
                "has_multiple_countries": [False, False, False],
                "first_purchase_month": pd.Series(["2021-01", "2021-01", "2021-02"], dtype="string"),
            }
        )

        transactions = pd.DataFrame(
            {
                "customer_id": pd.Series([1, 1, 2, 3, 3], dtype="Int64"),
                "invoice_no": pd.Series(["A1", "A2", "B1", "C1", "C2"], dtype="string"),
                "invoice_month": pd.Series(["2021-01", "2021-02", "2021-01", "2021-02", "2021-03"], dtype="string"),
                "quantity": pd.Series([1, 1, 1, 1, 1], dtype="Int64"),
                "line_revenue_gbp": pd.Series([10.0, 20.0, 15.0, 12.0, 14.0], dtype="Float64"),
            }
        )

        cohortes = construir_base_cohortes(customers, transactions)
        global_rows = cohortes[cohortes["cohort_scope"] == "all_countries"].copy()

        row = global_rows[
            (global_rows["cohort_month"] == "2021-01")
            & (global_rows["activity_month"] == "2021-02")
        ].iloc[0]

        self.assertEqual(int(row["cohort_size"]), 2)
        self.assertEqual(int(row["n_customers_active"]), 1)
        self.assertAlmostEqual(float(row["retention_rate"]), 0.5)
        self.assertEqual(int(row["cohort_index"]), 1)

    def test_construir_base_cohortes_usa_primary_country_para_segmentacion(self) -> None:
        customers = pd.DataFrame(
            {
                "customer_id": pd.Series([1], dtype="Int64"),
                "primary_country": pd.Series(["France"], dtype="string"),
                "n_countries": pd.Series([2], dtype="Int64"),
                "has_multiple_countries": [True],
                "first_purchase_month": pd.Series(["2021-01"], dtype="string"),
            }
        )

        transactions = pd.DataFrame(
            {
                "customer_id": pd.Series([1, 1], dtype="Int64"),
                "invoice_no": pd.Series(["A1", "A2"], dtype="string"),
                "invoice_month": pd.Series(["2021-01", "2021-02"], dtype="string"),
                "quantity": pd.Series([1, 1], dtype="Int64"),
                "line_revenue_gbp": pd.Series([10.0, 20.0], dtype="Float64"),
            }
        )

        cohortes = construir_base_cohortes(customers, transactions)
        country_rows = cohortes[cohortes["cohort_scope"] == "primary_country"].copy()

        self.assertEqual(country_rows["country"].unique().tolist(), ["France"])
        self.assertEqual(int(country_rows.iloc[0]["cohort_multicountry_customers"]), 1)
        self.assertEqual(int(country_rows.iloc[0]["n_multicountry_customers_active"]), 1)

    def test_construir_base_cohortes_rellena_con_ceros_meses_observables(self) -> None:
        customers = pd.DataFrame(
            {
                "customer_id": pd.Series([1], dtype="Int64"),
                "primary_country": pd.Series(["France"], dtype="string"),
                "n_countries": pd.Series([1], dtype="Int64"),
                "has_multiple_countries": [False],
                "first_purchase_month": pd.Series(["2021-01"], dtype="string"),
            }
        )

        transactions = pd.DataFrame(
            {
                "customer_id": pd.Series([1, 1], dtype="Int64"),
                "invoice_no": pd.Series(["A1", "A2"], dtype="string"),
                "invoice_month": pd.Series(["2021-01", "2021-03"], dtype="string"),
                "quantity": pd.Series([1, 1], dtype="Int64"),
                "line_revenue_gbp": pd.Series([10.0, 20.0], dtype="Float64"),
            }
        )

        cohortes = construir_base_cohortes(customers, transactions)
        row = cohortes[
            (cohortes["cohort_scope"] == "primary_country")
            & (cohortes["country"] == "France")
            & (cohortes["cohort_month"] == "2021-01")
            & (cohortes["activity_month"] == "2021-02")
        ].iloc[0]

        self.assertEqual(int(row["cohort_index"]), 1)
        self.assertEqual(int(row["n_customers_active"]), 0)
        self.assertEqual(int(row["n_orders"]), 0)
        self.assertEqual(int(row["n_lines"]), 0)
        self.assertEqual(int(row["total_quantity"]), 0)
        self.assertAlmostEqual(float(row["total_revenue_gbp"]), 0.0)
        self.assertAlmostEqual(float(row["retention_rate"]), 0.0)
        self.assertAlmostEqual(float(row["avg_revenue_per_active_customer_gbp"]), 0.0)


if __name__ == "__main__":
    unittest.main()
