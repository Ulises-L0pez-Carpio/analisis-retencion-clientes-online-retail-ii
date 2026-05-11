from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DEFAULT_INPUT_CUSTOMERS = PROCESSED_DIR / "clientes__base_analitica__v1.parquet"
DEFAULT_INPUT_TRANSACTIONS = PROCESSED_DIR / "transacciones__compras_validas__v1.parquet"
DEFAULT_OUTPUT = PROCESSED_DIR / "cohortes__retencion_mensual__v1.parquet"

REQUIRED_CUSTOMER_COLUMNS = {
    "customer_id",
    "primary_country",
    "n_countries",
    "has_multiple_countries",
    "first_purchase_month",
}

REQUIRED_TRANSACTION_COLUMNS = {
    "customer_id",
    "invoice_no",
    "invoice_month",
    "quantity",
    "line_revenue_gbp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera la primera base de cohortes de retencion mensual."
    )
    parser.add_argument(
        "--customers",
        type=Path,
        default=DEFAULT_INPUT_CUSTOMERS,
        help="Ruta al parquet de base analitica de clientes.",
    )
    parser.add_argument(
        "--transactions",
        type=Path,
        default=DEFAULT_INPUT_TRANSACTIONS,
        help="Ruta al parquet de compras validas.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Ruta de salida del parquet de cohortes.",
    )
    return parser.parse_args()


def cargar_parquet_validado(
    ruta_entrada: Path, columnas_requeridas: set[str], descripcion: str
) -> pd.DataFrame:
    ruta_resuelta = ruta_entrada.expanduser().resolve()
    if not ruta_resuelta.exists():
        raise FileNotFoundError(f"No se encontro {descripcion}: {ruta_resuelta}")

    df = pd.read_parquet(ruta_resuelta)
    columnas_faltantes = sorted(columnas_requeridas - set(df.columns))
    if columnas_faltantes:
        faltantes = ", ".join(columnas_faltantes)
        raise ValueError(
            f"Faltan columnas requeridas en {descripcion}: {faltantes}"
        )

    return df


def month_strings_to_index(series: pd.Series) -> pd.Series:
    dt = pd.to_datetime(series.astype("string") + "-01", errors="coerce")
    return dt.dt.year * 12 + dt.dt.month


def construir_grilla_observable(
    cohort_sizes: pd.DataFrame, max_activity_month: str
) -> pd.DataFrame:
    max_period = pd.Period(str(max_activity_month), freq="M")
    records: list[dict[str, object]] = []

    for cohort in cohort_sizes.to_dict("records"):
        cohort_period = pd.Period(str(cohort["cohort_month"]), freq="M")
        for cohort_index, activity_period in enumerate(
            pd.period_range(cohort_period, max_period, freq="M")
        ):
            row = cohort.copy()
            row["activity_month"] = str(activity_period)
            row["cohort_index"] = cohort_index
            records.append(row)

    return pd.DataFrame.from_records(records)


def construir_actividad_cliente_mes(
    customers: pd.DataFrame, transactions: pd.DataFrame
) -> pd.DataFrame:
    customer_cols = customers.loc[
        :,
        [
            "customer_id",
            "primary_country",
            "n_countries",
            "has_multiple_countries",
            "first_purchase_month",
        ],
    ].copy()

    activity = (
        transactions.groupby(["customer_id", "invoice_month"], as_index=False)
        .agg(
            n_orders=("invoice_no", "nunique"),
            n_lines=("invoice_no", "size"),
            total_quantity=("quantity", "sum"),
            total_revenue_gbp=("line_revenue_gbp", "sum"),
        )
        .merge(customer_cols, on="customer_id", how="inner")
    )

    activity["cohort_month"] = activity["first_purchase_month"].astype("string")
    activity["activity_month"] = activity["invoice_month"].astype("string")

    activity["cohort_index"] = (
        month_strings_to_index(activity["activity_month"])
        - month_strings_to_index(activity["cohort_month"])
    ).astype("Int64")

    return activity


def agregar_metricas_cohorte(
    cohort_sizes: pd.DataFrame,
    activity: pd.DataFrame,
    group_cols: list[str],
    country_value_col: str,
    scope_name: str,
) -> pd.DataFrame:
    activity_grouped = (
        activity.groupby(group_cols + ["activity_month", "cohort_index"], as_index=False)
        .agg(
            n_customers_active=("customer_id", "nunique"),
            n_multicountry_customers_active=("has_multiple_countries", "sum"),
            n_orders=("n_orders", "sum"),
            n_lines=("n_lines", "sum"),
            total_quantity=("total_quantity", "sum"),
            total_revenue_gbp=("total_revenue_gbp", "sum"),
        )
    )

    cohort_base = construir_grilla_observable(
        cohort_sizes=cohort_sizes,
        max_activity_month=str(activity["activity_month"].max()),
    ).merge(
        activity_grouped,
        on=group_cols + ["activity_month", "cohort_index"],
        how="left",
    )

    int_metric_cols = [
        "n_customers_active",
        "n_multicountry_customers_active",
        "n_orders",
        "n_lines",
        "total_quantity",
    ]
    for column in int_metric_cols:
        cohort_base[column] = cohort_base[column].fillna(0)

    cohort_base["total_revenue_gbp"] = cohort_base["total_revenue_gbp"].fillna(0.0)
    active_customers = cohort_base["n_customers_active"].astype("Float64")
    active_customers_nonzero = active_customers.where(active_customers > 0)
    cohort_size = cohort_base["cohort_size"].astype("Float64")

    cohort_base["retention_rate"] = (active_customers / cohort_size).fillna(0.0)
    cohort_base["avg_revenue_per_active_customer_gbp"] = (
        cohort_base["total_revenue_gbp"] / active_customers_nonzero
    ).fillna(0.0)
    cohort_base["avg_orders_per_active_customer"] = (
        cohort_base["n_orders"] / active_customers_nonzero
    ).fillna(0.0)
    cohort_base["avg_lines_per_active_customer"] = (
        cohort_base["n_lines"] / active_customers_nonzero
    ).fillna(0.0)

    cohort_base["cohort_scope"] = scope_name
    cohort_base["country"] = cohort_base[country_value_col].astype("string")

    return cohort_base


def construir_base_cohortes(
    customers: pd.DataFrame, transactions: pd.DataFrame
) -> pd.DataFrame:
    activity = construir_actividad_cliente_mes(customers, transactions)

    cohort_sizes_all = (
        customers.groupby("first_purchase_month", as_index=False)
        .agg(
            cohort_size=("customer_id", "nunique"),
            cohort_multicountry_customers=("has_multiple_countries", "sum"),
        )
        .rename(columns={"first_purchase_month": "cohort_month"})
        .assign(scope_key="ALL_COUNTRIES")
    )

    activity_all = activity.assign(scope_key="ALL_COUNTRIES")
    cohorts_all = agregar_metricas_cohorte(
        cohort_sizes=cohort_sizes_all,
        activity=activity_all,
        group_cols=["scope_key", "cohort_month"],
        country_value_col="scope_key",
        scope_name="all_countries",
    )

    cohort_sizes_country = (
        customers.groupby(["primary_country", "first_purchase_month"], as_index=False)
        .agg(
            cohort_size=("customer_id", "nunique"),
            cohort_multicountry_customers=("has_multiple_countries", "sum"),
        )
        .rename(columns={"first_purchase_month": "cohort_month"})
    )

    cohorts_country = agregar_metricas_cohorte(
        cohort_sizes=cohort_sizes_country,
        activity=activity,
        group_cols=["primary_country", "cohort_month"],
        country_value_col="primary_country",
        scope_name="primary_country",
    )

    cohortes = pd.concat([cohorts_all, cohorts_country], ignore_index=True, sort=False)

    cohortes["cohort_scope"] = cohortes["cohort_scope"].astype("string")
    cohortes["country"] = cohortes["country"].astype("string")
    cohortes["cohort_month"] = cohortes["cohort_month"].astype("string")
    cohortes["activity_month"] = cohortes["activity_month"].astype("string")
    cohortes["cohort_index"] = cohortes["cohort_index"].astype("Int64")
    cohortes["cohort_size"] = cohortes["cohort_size"].astype("Int64")
    cohortes["cohort_multicountry_customers"] = cohortes[
        "cohort_multicountry_customers"
    ].astype("Int64")
    cohortes["n_customers_active"] = cohortes["n_customers_active"].astype("Int64")
    cohortes["n_multicountry_customers_active"] = cohortes[
        "n_multicountry_customers_active"
    ].astype("Int64")
    cohortes["n_orders"] = cohortes["n_orders"].astype("Int64")
    cohortes["n_lines"] = cohortes["n_lines"].astype("Int64")
    cohortes["total_quantity"] = cohortes["total_quantity"].astype("Int64")
    cohortes["retention_rate"] = cohortes["retention_rate"].astype("Float64")
    cohortes["avg_revenue_per_active_customer_gbp"] = cohortes[
        "avg_revenue_per_active_customer_gbp"
    ].astype("Float64")
    cohortes["avg_orders_per_active_customer"] = cohortes[
        "avg_orders_per_active_customer"
    ].astype("Float64")
    cohortes["avg_lines_per_active_customer"] = cohortes[
        "avg_lines_per_active_customer"
    ].astype("Float64")

    ordered_columns = [
        "cohort_scope",
        "country",
        "cohort_month",
        "activity_month",
        "cohort_index",
        "cohort_size",
        "cohort_multicountry_customers",
        "n_customers_active",
        "n_multicountry_customers_active",
        "retention_rate",
        "n_orders",
        "n_lines",
        "total_quantity",
        "total_revenue_gbp",
        "avg_revenue_per_active_customer_gbp",
        "avg_orders_per_active_customer",
        "avg_lines_per_active_customer",
    ]

    cohortes = (
        cohortes.loc[:, ordered_columns]
        .sort_values(["cohort_scope", "country", "cohort_month", "cohort_index"])
        .reset_index(drop=True)
    )
    return cohortes


def guardar_parquet(df: pd.DataFrame, ruta_salida: Path) -> Path:
    ruta_resuelta = ruta_salida.expanduser().resolve()
    ruta_resuelta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta_resuelta, index=False)
    return ruta_resuelta


def construir_resumen(df: pd.DataFrame, ruta_salida: Path) -> str:
    lineas: list[str] = []
    lineas.append("Resumen de base de cohortes")
    lineas.append(f"- Filas generadas: {len(df):,}")
    lineas.append(
        f"- Cohortes globales: {int((df['cohort_scope'] == 'all_countries').sum()):,}"
    )
    lineas.append(
        f"- Cohortes por pais: {int((df['cohort_scope'] == 'primary_country').sum()):,}"
    )
    lineas.append(f"- Primer cohort_month: {df['cohort_month'].min()}")
    lineas.append(f"- Ultimo activity_month: {df['activity_month'].max()}")
    lineas.append(f"- Archivo generado: {ruta_salida}")
    return "\n".join(lineas)


def main() -> int:
    args = parse_args()

    try:
        customers = cargar_parquet_validado(
            args.customers, REQUIRED_CUSTOMER_COLUMNS, "la base analitica de clientes"
        )
        transactions = cargar_parquet_validado(
            args.transactions,
            REQUIRED_TRANSACTION_COLUMNS,
            "la base de compras validas",
        )
        cohortes = construir_base_cohortes(customers, transactions)
        ruta_salida = guardar_parquet(cohortes, args.output)
    except (FileNotFoundError, ValueError, ImportError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(construir_resumen(cohortes, ruta_salida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
