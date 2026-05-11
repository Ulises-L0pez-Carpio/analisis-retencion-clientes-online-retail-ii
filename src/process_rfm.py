from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DEFAULT_INPUT = PROCESSED_DIR / "transacciones__compras_validas__v1.parquet"
DEFAULT_OUTPUT = PROCESSED_DIR / "rfm__segmentacion_clientes__v1.parquet"

REQUIRED_COLUMNS = {
    "invoice_no",
    "invoice_datetime",
    "quantity",
    "unit_price_gbp",
    "customer_id",
    "line_revenue_gbp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera la capa RFM a nivel cliente desde compras validas."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Ruta al parquet de compras validas.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Ruta de salida para la segmentacion RFM.",
    )
    return parser.parse_args()


def cargar_compras_validas(ruta_entrada: Path) -> pd.DataFrame:
    ruta_resuelta = ruta_entrada.expanduser().resolve()
    if not ruta_resuelta.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo de compras validas: {ruta_resuelta}"
        )

    df = pd.read_parquet(ruta_resuelta)
    columnas_faltantes = sorted(REQUIRED_COLUMNS - set(df.columns))
    if columnas_faltantes:
        faltantes = ", ".join(columnas_faltantes)
        raise ValueError(
            "Faltan columnas requeridas para construir la capa RFM: "
            f"{faltantes}"
        )

    return df


def validar_compras_validas(df: pd.DataFrame) -> None:
    invalid_mask = (
        df["customer_id"].isna()
        | (df["quantity"] <= 0)
        | (df["unit_price_gbp"] <= 0)
        | df["invoice_no"].astype("string").str.startswith("C", na=False)
    )

    if invalid_mask.any():
        n_invalid = int(invalid_mask.sum())
        raise ValueError(
            "La entrada para RFM debe venir solo con compras validas. "
            f"Se detectaron {n_invalid:,} filas invalidas."
        )


def construir_orders(df: pd.DataFrame) -> pd.DataFrame:
    orders = (
        df.groupby(["customer_id", "invoice_no"], as_index=False)
        .agg(
            order_datetime=("invoice_datetime", "max"),
            order_revenue_gbp=("line_revenue_gbp", "sum"),
        )
        .sort_values(["customer_id", "order_datetime", "invoice_no"])
        .reset_index(drop=True)
    )
    return orders


def asignar_quintil(series: pd.Series, higher_is_better: bool) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    rank_pct = numeric.rank(method="average", pct=True, ascending=higher_is_better)
    bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    scores = pd.cut(rank_pct, bins=bins, labels=[1, 2, 3, 4, 5], include_lowest=True)
    return scores.astype("Int64")


def asignar_segmento(row: pd.Series) -> str:
    r_score = int(row["r_score"])
    f_score = int(row["f_score"])
    m_score = int(row["m_score"])

    if r_score >= 4 and f_score >= 4 and m_score >= 4:
        return "champions"
    if r_score >= 3 and f_score >= 4 and m_score >= 3:
        return "loyal_customers"
    if r_score >= 4 and f_score >= 2 and m_score >= 2:
        return "potential_loyalists"
    if r_score <= 2 and (f_score >= 3 or m_score >= 3):
        return "at_risk"
    return "hibernating"


def construir_base_rfm(df: pd.DataFrame) -> pd.DataFrame:
    compras_validas = df.copy()
    compras_validas["invoice_datetime"] = pd.to_datetime(
        compras_validas["invoice_datetime"], errors="coerce"
    )

    validar_compras_validas(compras_validas)
    orders = construir_orders(compras_validas)

    snapshot_datetime = orders["order_datetime"].max()
    snapshot_date = snapshot_datetime.normalize()
    snapshot_date_str = snapshot_date.strftime("%Y-%m-%d")

    rfm = (
        orders.groupby("customer_id", as_index=False)
        .agg(
            first_purchase_datetime=("order_datetime", "min"),
            last_purchase_datetime=("order_datetime", "max"),
            frequency_orders=("invoice_no", "nunique"),
            monetary_gbp=("order_revenue_gbp", "sum"),
        )
    )

    rfm["snapshot_datetime"] = snapshot_datetime
    rfm["snapshot_date"] = pd.Series([snapshot_date_str] * len(rfm), dtype="string")
    rfm["recency_days"] = (
        snapshot_date - rfm["last_purchase_datetime"].dt.normalize()
    ).dt.days.astype("Int64")

    rfm["r_score"] = asignar_quintil(rfm["recency_days"], higher_is_better=False)
    rfm["f_score"] = asignar_quintil(rfm["frequency_orders"], higher_is_better=True)
    rfm["m_score"] = asignar_quintil(rfm["monetary_gbp"], higher_is_better=True)
    rfm["rfm_score"] = (
        rfm["r_score"].astype("string")
        + rfm["f_score"].astype("string")
        + rfm["m_score"].astype("string")
    ).astype("string")
    rfm["rfm_segment"] = rfm.apply(asignar_segmento, axis=1).astype("string")

    rfm["customer_id"] = rfm["customer_id"].astype("Int64")
    rfm["frequency_orders"] = rfm["frequency_orders"].astype("Int64")
    rfm["monetary_gbp"] = rfm["monetary_gbp"].astype("Float64")

    ordered_columns = [
        "customer_id",
        "snapshot_datetime",
        "snapshot_date",
        "first_purchase_datetime",
        "last_purchase_datetime",
        "recency_days",
        "frequency_orders",
        "monetary_gbp",
        "r_score",
        "f_score",
        "m_score",
        "rfm_score",
        "rfm_segment",
    ]

    return (
        rfm.loc[:, ordered_columns]
        .sort_values(["customer_id"])
        .reset_index(drop=True)
    )


def guardar_parquet(df: pd.DataFrame, ruta_salida: Path) -> Path:
    ruta_resuelta = ruta_salida.expanduser().resolve()
    ruta_resuelta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta_resuelta, index=False)
    return ruta_resuelta


def construir_resumen(df_rfm: pd.DataFrame, ruta_salida: Path) -> str:
    lineas: list[str] = []
    lineas.append("Resumen de segmentacion RFM")
    lineas.append(f"- Clientes segmentados: {len(df_rfm):,}")
    lineas.append(f"- Snapshot del dataset: {df_rfm['snapshot_datetime'].max()}")
    lineas.append(
        f"- Clientes champions: {int((df_rfm['rfm_segment'] == 'champions').sum()):,}"
    )
    lineas.append(
        f"- Clientes at_risk: {int((df_rfm['rfm_segment'] == 'at_risk').sum()):,}"
    )
    lineas.append(f"- Archivo generado: {ruta_salida}")
    return "\n".join(lineas)


def main() -> int:
    args = parse_args()

    try:
        df = cargar_compras_validas(args.input)
        rfm = construir_base_rfm(df)
        ruta_salida = guardar_parquet(rfm, args.output)
    except (FileNotFoundError, ValueError, ImportError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(construir_resumen(rfm, ruta_salida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
