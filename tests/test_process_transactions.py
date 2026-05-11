from __future__ import annotations

import unittest

import pandas as pd

from src.process_transactions import (
    agregar_columnas_derivadas,
    construir_base_compras_validas,
    eliminar_duplicados_exactos,
    normalizar_columnas,
)


class ProcessTransactionsTests(unittest.TestCase):
    def test_normalizar_columnas_aplica_mapeo_canonico(self) -> None:
        df = pd.DataFrame(
            {
                "Invoice": ["10001"],
                "StockCode": ["ABC"],
                "Description": ["Producto"],
                "Quantity": [2],
                "InvoiceDate": ["2011-01-01 10:00:00"],
                "Price": [3.5],
                "Customer ID": [12345],
                "Country": ["France"],
                "origen_hoja": ["Year 2010-2011"],
                "archivo_origen": ["online_retail_II.xlsx"],
            }
        )

        resultado = normalizar_columnas(df)

        self.assertIn("invoice_no", resultado.columns)
        self.assertIn("unit_price_gbp", resultado.columns)
        self.assertIn("customer_id", resultado.columns)
        self.assertNotIn("Invoice", resultado.columns)
        self.assertEqual(str(resultado.loc[0, "invoice_no"]), "10001")

    def test_compra_valida_excluye_cancelacion_precio_no_positivo_y_cliente_nulo(self) -> None:
        df = pd.DataFrame(
            {
                "invoice_no": pd.Series(["10001", "C10002", "10003", "10004"], dtype="string"),
                "stock_code": pd.Series(["A", "B", "C", "D"], dtype="string"),
                "description": pd.Series(["a", "b", "c", "d"], dtype="string"),
                "quantity": pd.Series([2, -1, 1, 1], dtype="Int64"),
                "invoice_datetime": pd.to_datetime(
                    ["2011-01-01", "2011-01-02", "2011-01-03", "2011-01-04"]
                ),
                "unit_price_gbp": [3.0, 2.0, 0.0, 1.0],
                "customer_id": pd.Series([12345, 12346, 12347, pd.NA], dtype="Int64"),
                "country": pd.Series(["France", "France", "Germany", "Spain"], dtype="string"),
                "source_sheet": pd.Series(["Y1", "Y1", "Y2", "Y2"], dtype="string"),
                "source_file": pd.Series(["f.xlsx", "f.xlsx", "f.xlsx", "f.xlsx"], dtype="string"),
            }
        )

        resultado = agregar_columnas_derivadas(df)
        compras_validas = construir_base_compras_validas(resultado)

        self.assertEqual(len(compras_validas), 1)
        self.assertEqual(str(compras_validas.iloc[0]["invoice_no"]), "10001")

    def test_eliminar_duplicados_exactos_devuelve_conteo_correcto(self) -> None:
        df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})

        resultado, removidos = eliminar_duplicados_exactos(df)

        self.assertEqual(removidos, 1)
        self.assertEqual(len(resultado), 2)


if __name__ == "__main__":
    unittest.main()
