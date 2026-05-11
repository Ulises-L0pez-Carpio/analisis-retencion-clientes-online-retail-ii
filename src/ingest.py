from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
INTERIM_DIR = ROOT_DIR / "data" / "interim"
DEFAULT_OUTPUT = INTERIM_DIR / "online_retail_ii_ingesta_inicial.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingesta inicial del dataset Online Retail II."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Ruta al archivo Excel original. Si se omite, se detecta automaticamente en data/raw/.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Ruta del archivo CSV de salida en data/interim/.",
    )
    return parser.parse_args()


def detectar_archivo_excel(ruta_entrada: Path | None) -> Path:
    if ruta_entrada is not None:
        ruta_resuelta = ruta_entrada.expanduser().resolve()
        if not ruta_resuelta.exists():
            raise FileNotFoundError(
                f"No se encontro el archivo de entrada: {ruta_resuelta}"
            )
        if ruta_resuelta.suffix.lower() not in {".xlsx", ".xls"}:
            raise ValueError("El archivo de entrada debe ser un Excel con extension .xlsx o .xls.")
        return ruta_resuelta

    candidatos = sorted(RAW_DIR.glob("*.xlsx")) + sorted(RAW_DIR.glob("*.xls"))
    if not candidatos:
        raise FileNotFoundError(
            "No se encontro ningun archivo Excel en data/raw/. "
            "Coloca ahi el archivo original de Online Retail II o usa --input."
        )
    if len(candidatos) > 1:
        nombres = ", ".join(archivo.name for archivo in candidatos)
        raise ValueError(
            "Se encontraron varios archivos Excel en data/raw/. "
            f"Especifica uno con --input. Archivos detectados: {nombres}"
        )
    return candidatos[0].resolve()


def cargar_dataset_desde_excel(ruta_excel: Path) -> tuple[pd.DataFrame, list[str]]:
    hojas = pd.read_excel(ruta_excel, sheet_name=None)
    frames: list[pd.DataFrame] = []

    for nombre_hoja, df_hoja in hojas.items():
        df = df_hoja.copy()
        df["origen_hoja"] = nombre_hoja
        df["archivo_origen"] = ruta_excel.name
        frames.append(df)

    df_combinado = pd.concat(frames, ignore_index=True)

    if "InvoiceDate" in df_combinado.columns:
        df_combinado["InvoiceDate"] = pd.to_datetime(
            df_combinado["InvoiceDate"], errors="coerce"
        )

    return df_combinado, list(hojas.keys())


def construir_resumen_basico(df: pd.DataFrame) -> str:
    lineas: list[str] = []
    lineas.append("Resumen basico del dataset")
    lineas.append(f"- Filas: {df.shape[0]:,}")
    lineas.append(f"- Columnas: {df.shape[1]:,}")
    lineas.append(f"- Columnas detectadas: {', '.join(df.columns)}")
    lineas.append("")
    lineas.append("Tipos de datos:")

    for columna, tipo in df.dtypes.items():
        lineas.append(f"- {columna}: {tipo}")

    lineas.append("")
    lineas.append("Valores nulos por columna:")

    nulos = df.isna().sum().sort_values(ascending=False)
    for columna, cantidad in nulos.items():
        porcentaje = (cantidad / len(df) * 100) if len(df) else 0.0
        lineas.append(f"- {columna}: {cantidad:,} ({porcentaje:.2f}%)")

    if "InvoiceDate" in df.columns:
        fecha_min = df["InvoiceDate"].min()
        fecha_max = df["InvoiceDate"].max()
        lineas.append("")
        lineas.append(f"Rango de fechas detectado: {fecha_min} -> {fecha_max}")

    return "\n".join(lineas)


def guardar_copia_intermedia(df: pd.DataFrame, ruta_salida: Path) -> Path:
    ruta_resuelta = ruta_salida.expanduser().resolve()
    ruta_resuelta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_resuelta, index=False, encoding="utf-8-sig")
    return ruta_resuelta


def main() -> int:
    args = parse_args()

    try:
        ruta_excel = detectar_archivo_excel(args.input)
        df, hojas = cargar_dataset_desde_excel(ruta_excel)
        ruta_salida = guardar_copia_intermedia(df, args.output)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"Archivo fuente: {ruta_excel}")
    print(f"Hojas leidas: {', '.join(hojas)}")
    print("")
    print(construir_resumen_basico(df))
    print("")
    print(f"Archivo intermedio generado: {ruta_salida}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
