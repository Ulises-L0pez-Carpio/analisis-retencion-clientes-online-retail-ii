from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
INTERIM_DIR = ROOT_DIR / "data" / "interim"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DEFAULT_INPUT = INTERIM_DIR / "online_retail_ii_ingesta_inicial.csv"
DEFAULT_OUTPUT_GENERAL = PROCESSED_DIR / "transacciones__base_general__v1.parquet"
DEFAULT_OUTPUT_VALID = PROCESSED_DIR / "transacciones__compras_validas__v1.parquet"

RENAME_MAP = {
    "Invoice": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_datetime",
    "Price": "unit_price_gbp",
    "Customer ID": "customer_id",
    "Country": "country",
    "origen_hoja": "source_sheet",
    "archivo_origen": "source_file",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera datasets procesados de transacciones a partir de la capa interim."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Ruta al CSV intermedio de entrada.",
    )
    parser.add_argument(
        "--output-general",
        type=Path,
        default=DEFAULT_OUTPUT_GENERAL,
        help="Ruta de salida para la base general procesada.",
    )
    parser.add_argument(
        "--output-valid",
        type=Path,
        default=DEFAULT_OUTPUT_VALID,
        help="Ruta de salida para la base de compras validas.",
    )
    return parser.parse_args()


def cargar_interim(ruta_entrada: Path) -> pd.DataFrame:
    ruta_resuelta = ruta_entrada.expanduser().resolve()
    if not ruta_resuelta.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo interim de entrada: {ruta_resuelta}"
        )

    df = pd.read_csv(ruta_resuelta, parse_dates=["InvoiceDate"])
    return df


def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    columnas_faltantes = sorted(set(RENAME_MAP) - set(df.columns))
    if columnas_faltantes:
        faltantes = ", ".join(columnas_faltantes)
        raise ValueError(
            "Faltan columnas requeridas para construir la capa processed: "
            f"{faltantes}"
        )

    df_norm = df.rename(columns=RENAME_MAP).copy()

    df_norm["invoice_no"] = df_norm["invoice_no"].astype("string")
    df_norm["stock_code"] = df_norm["stock_code"].astype("string")
    df_norm["description"] = df_norm["description"].astype("string")
    df_norm["country"] = df_norm["country"].astype("string")
    df_norm["source_sheet"] = df_norm["source_sheet"].astype("string")
    df_norm["source_file"] = df_norm["source_file"].astype("string")

    df_norm["invoice_datetime"] = pd.to_datetime(
        df_norm["invoice_datetime"], errors="coerce"
    )
    df_norm["quantity"] = pd.to_numeric(df_norm["quantity"], errors="coerce").astype("Int64")
    df_norm["unit_price_gbp"] = pd.to_numeric(
        df_norm["unit_price_gbp"], errors="coerce"
    )
    df_norm["customer_id"] = pd.to_numeric(
        df_norm["customer_id"], errors="coerce"
    ).astype("Int64")

    return df_norm


def eliminar_duplicados_exactos(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    filas_antes = len(df)
    df_sin_dup = df.drop_duplicates().copy()
    duplicados_removidos = filas_antes - len(df_sin_dup)
    return df_sin_dup, duplicados_removidos


def agregar_columnas_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    df_der = df.copy()

    df_der["invoice_date"] = df_der["invoice_datetime"].dt.date.astype("string")
    df_der["invoice_month"] = (
        df_der["invoice_datetime"].dt.to_period("M").astype("string")
    )

    df_der["is_missing_customer_id"] = df_der["customer_id"].isna()
    df_der["is_cancellation"] = df_der["invoice_no"].str.startswith("C", na=False)
    df_der["has_negative_quantity"] = df_der["quantity"] < 0
    df_der["has_nonpositive_unit_price"] = df_der["unit_price_gbp"] <= 0
    df_der["is_valid_purchase"] = (
        ~df_der["is_missing_customer_id"]
        & ~df_der["is_cancellation"]
        & (df_der["quantity"] > 0)
        & (df_der["unit_price_gbp"] > 0)
    )
    df_der["line_revenue_gbp"] = df_der["quantity"].astype("Float64") * df_der["unit_price_gbp"]

    return df_der


def construir_base_compras_validas(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["is_valid_purchase"]].copy()


def guardar_parquet(df: pd.DataFrame, ruta_salida: Path) -> Path:
    ruta_resuelta = ruta_salida.expanduser().resolve()
    ruta_resuelta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta_resuelta, index=False)
    return ruta_resuelta


def construir_resumen(
    filas_interim: int,
    duplicados_removidos: int,
    base_general: pd.DataFrame,
    compras_validas: pd.DataFrame,
    ruta_general: Path,
    ruta_valid: Path,
) -> str:
    lineas: list[str] = []
    lineas.append("Resumen de procesamiento")
    lineas.append(f"- Filas en interim: {filas_interim:,}")
    lineas.append(f"- Duplicados exactos removidos: {duplicados_removidos:,}")
    lineas.append(f"- Filas en base general: {len(base_general):,}")
    lineas.append(f"- Filas en compras validas: {len(compras_validas):,}")
    lineas.append(f"- Clientes unicos en compras validas: {compras_validas['customer_id'].nunique():,}")
    lineas.append(f"- Paises en compras validas: {compras_validas['country'].nunique():,}")
    lineas.append(f"- Archivo base general: {ruta_general}")
    lineas.append(f"- Archivo compras validas: {ruta_valid}")
    return "\n".join(lineas)


def main() -> int:
    args = parse_args()

    try:
        df_interim = cargar_interim(args.input)
        filas_interim = len(df_interim)
        df_normalizado = normalizar_columnas(df_interim)
        base_general, duplicados_removidos = eliminar_duplicados_exactos(df_normalizado)
        base_general = agregar_columnas_derivadas(base_general)
        compras_validas = construir_base_compras_validas(base_general)
        ruta_general = guardar_parquet(base_general, args.output_general)
        ruta_valid = guardar_parquet(compras_validas, args.output_valid)
    except (FileNotFoundError, ValueError, ImportError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(construir_resumen(
        filas_interim=filas_interim,
        duplicados_removidos=duplicados_removidos,
        base_general=base_general,
        compras_validas=compras_validas,
        ruta_general=ruta_general,
        ruta_valid=ruta_valid,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
