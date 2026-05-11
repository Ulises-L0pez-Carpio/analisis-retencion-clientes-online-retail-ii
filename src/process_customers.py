from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DEFAULT_INPUT = PROCESSED_DIR / "transacciones__compras_validas__v1.parquet"
DEFAULT_OUTPUT = PROCESSED_DIR / "clientes__base_analitica__v1.parquet"

REQUIRED_COLUMNS = {
    "invoice_no",
    "stock_code",
    "quantity",
    "invoice_datetime",
    "unit_price_gbp",
    "customer_id",
    "country",
    "line_revenue_gbp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera la base analitica a nivel cliente desde compras validas."
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
        help="Ruta de salida para la base analitica de clientes.",
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
            "Faltan columnas requeridas para construir la base de clientes: "
            f"{faltantes}"
        )

    return df


def construir_primary_country(df: pd.DataFrame) -> pd.DataFrame:
    country_stats = (
        df.groupby(["customer_id", "country"], as_index=False)
        .agg(
            country_line_count=("invoice_no", "size"),
            country_order_count=("invoice_no", "nunique"),
            country_revenue_gbp=("line_revenue_gbp", "sum"),
            last_country_purchase_datetime=("invoice_datetime", "max"),
        )
        .sort_values(
            [
                "customer_id",
                "country_line_count",
                "country_order_count",
                "country_revenue_gbp",
                "last_country_purchase_datetime",
                "country",
            ],
            ascending=[True, False, False, False, False, True],
        )
    )

    primary_country = (
        country_stats.drop_duplicates(subset=["customer_id"], keep="first")
        .loc[
            :,
            [
                "customer_id",
                "country",
                "country_line_count",
                "country_order_count",
            ],
        ]
        .rename(
            columns={
                "country": "primary_country",
                "country_line_count": "primary_country_line_count",
                "country_order_count": "primary_country_order_count",
            }
        )
    )

    country_summary = (
        df.groupby("customer_id", as_index=False)
        .agg(n_countries=("country", "nunique"))
        .assign(has_multiple_countries=lambda x: x["n_countries"] > 1)
    )

    return primary_country.merge(country_summary, on="customer_id", how="left")


def construir_orders(df: pd.DataFrame) -> pd.DataFrame:
    orders = (
        df.groupby(["customer_id", "invoice_no"], as_index=False)
        .agg(
            order_datetime=("invoice_datetime", "max"),
            order_revenue_gbp=("line_revenue_gbp", "sum"),
            order_quantity=("quantity", "sum"),
        )
    )

    orders["order_date"] = orders["order_datetime"].dt.normalize()
    orders["order_month"] = orders["order_datetime"].dt.to_period("M").astype("string")
    return orders


def calcular_promedio_dias_entre_pedidos(order_datetimes: pd.Series) -> float | pd.NA:
    ordered = pd.Series(order_datetimes).sort_values().drop_duplicates()
    if len(ordered) < 2:
        return pd.NA

    diffs = ordered.diff().dropna().dt.total_seconds() / 86400
    return float(diffs.mean())


def construir_base_clientes(df: pd.DataFrame) -> pd.DataFrame:
    compras_validas = df.copy()
    compras_validas["invoice_datetime"] = pd.to_datetime(
        compras_validas["invoice_datetime"], errors="coerce"
    )

    orders = construir_orders(compras_validas)

    customer_line_metrics = (
        compras_validas.groupby("customer_id", as_index=False)
        .agg(
            n_lines=("invoice_no", "size"),
            n_unique_products=("stock_code", "nunique"),
            total_quantity=("quantity", "sum"),
            total_revenue_gbp=("line_revenue_gbp", "sum"),
            avg_line_revenue_gbp=("line_revenue_gbp", "mean"),
            avg_unit_price_gbp=("unit_price_gbp", "mean"),
        )
    )

    customer_order_metrics = (
        orders.groupby("customer_id", as_index=False)
        .agg(
            first_purchase_datetime=("order_datetime", "min"),
            last_purchase_datetime=("order_datetime", "max"),
            n_orders=("invoice_no", "size"),
            n_order_days=("order_date", "nunique"),
            n_active_months=("order_month", "nunique"),
            avg_order_value_gbp=("order_revenue_gbp", "mean"),
            avg_quantity_per_order=("order_quantity", "mean"),
        )
    )

    avg_days_between_orders = (
        orders.groupby("customer_id")["order_datetime"]
        .apply(calcular_promedio_dias_entre_pedidos)
        .rename("avg_days_between_orders")
        .reset_index()
    )

    country_metrics = construir_primary_country(compras_validas)

    snapshot_datetime = compras_validas["invoice_datetime"].max()
    snapshot_date = snapshot_datetime.normalize()
    snapshot_date_str = snapshot_date.strftime("%Y-%m-%d")
    snapshot_month = snapshot_datetime.to_period("M").strftime("%Y-%m")

    customer_base = (
        customer_order_metrics
        .merge(customer_line_metrics, on="customer_id", how="left")
        .merge(country_metrics, on="customer_id", how="left")
        .merge(avg_days_between_orders, on="customer_id", how="left")
    )

    customer_base["first_purchase_date"] = customer_base["first_purchase_datetime"].dt.strftime(
        "%Y-%m-%d"
    ).astype("string")
    customer_base["first_purchase_month"] = (
        customer_base["first_purchase_datetime"].dt.to_period("M").astype("string")
    )
    customer_base["last_purchase_date"] = customer_base["last_purchase_datetime"].dt.strftime(
        "%Y-%m-%d"
    ).astype("string")
    customer_base["last_purchase_month"] = (
        customer_base["last_purchase_datetime"].dt.to_period("M").astype("string")
    )

    customer_base["snapshot_datetime"] = snapshot_datetime
    customer_base["snapshot_date"] = pd.Series(
        [snapshot_date_str] * len(customer_base), dtype="string"
    )
    customer_base["snapshot_month"] = pd.Series(
        [snapshot_month] * len(customer_base), dtype="string"
    )

    customer_base["customer_age_days"] = (
        snapshot_date - customer_base["first_purchase_datetime"].dt.normalize()
    ).dt.days.astype("Int64")
    customer_base["customer_lifetime_days"] = (
        customer_base["last_purchase_datetime"].dt.normalize()
        - customer_base["first_purchase_datetime"].dt.normalize()
    ).dt.days.astype("Int64")
    customer_base["recency_days"] = (
        snapshot_date - customer_base["last_purchase_datetime"].dt.normalize()
    ).dt.days.astype("Int64")

    customer_base["is_repeat_customer"] = customer_base["n_orders"] > 1
    customer_base["avg_days_between_orders"] = customer_base[
        "avg_days_between_orders"
    ].astype("Float64")

    customer_base["customer_id"] = customer_base["customer_id"].astype("Int64")
    customer_base["n_orders"] = customer_base["n_orders"].astype("Int64")
    customer_base["n_order_days"] = customer_base["n_order_days"].astype("Int64")
    customer_base["n_active_months"] = customer_base["n_active_months"].astype("Int64")
    customer_base["n_lines"] = customer_base["n_lines"].astype("Int64")
    customer_base["n_unique_products"] = customer_base["n_unique_products"].astype("Int64")
    customer_base["total_quantity"] = customer_base["total_quantity"].astype("Int64")

    ordered_columns = [
        "customer_id",
        "primary_country",
        "n_countries",
        "has_multiple_countries",
        "primary_country_line_count",
        "primary_country_order_count",
        "first_purchase_datetime",
        "first_purchase_date",
        "first_purchase_month",
        "last_purchase_datetime",
        "last_purchase_date",
        "last_purchase_month",
        "snapshot_datetime",
        "snapshot_date",
        "snapshot_month",
        "customer_age_days",
        "customer_lifetime_days",
        "recency_days",
        "n_orders",
        "n_order_days",
        "n_active_months",
        "n_lines",
        "n_unique_products",
        "total_quantity",
        "total_revenue_gbp",
        "avg_order_value_gbp",
        "avg_line_revenue_gbp",
        "avg_unit_price_gbp",
        "avg_quantity_per_order",
        "avg_days_between_orders",
        "is_repeat_customer",
    ]

    customer_base = customer_base.loc[:, ordered_columns].sort_values(
        ["customer_id"]
    ).reset_index(drop=True)

    return customer_base


def guardar_parquet(df: pd.DataFrame, ruta_salida: Path) -> Path:
    ruta_resuelta = ruta_salida.expanduser().resolve()
    ruta_resuelta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta_resuelta, index=False)
    return ruta_resuelta


def construir_resumen(df_clientes: pd.DataFrame, ruta_salida: Path) -> str:
    lineas: list[str] = []
    lineas.append("Resumen de base analitica de clientes")
    lineas.append(f"- Filas generadas: {len(df_clientes):,}")
    lineas.append(f"- Clientes multicountry: {int(df_clientes['has_multiple_countries'].sum()):,}")
    lineas.append(f"- Fecha minima de primera compra: {df_clientes['first_purchase_datetime'].min()}")
    lineas.append(f"- Fecha maxima de ultima compra: {df_clientes['last_purchase_datetime'].max()}")
    lineas.append(f"- Snapshot del dataset: {df_clientes['snapshot_datetime'].max()}")
    lineas.append(f"- Archivo generado: {ruta_salida}")
    return "\n".join(lineas)


def main() -> int:
    args = parse_args()

    try:
        df = cargar_compras_validas(args.input)
        customer_base = construir_base_clientes(df)
        ruta_salida = guardar_parquet(customer_base, args.output)
    except (FileNotFoundError, ValueError, ImportError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(construir_resumen(customer_base, ruta_salida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
