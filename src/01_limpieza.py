"""
Limpieza del dataset World Happiness Report 2016.
Replica, con código Python directo y verificado, los pasos que el proyecto guiado
del curso (IBM Generative AI for Data Analytics) describe generar con un LLM:
1. Cargar el CSV.
2. Revisar y corregir tipos de datos.
3. Detectar y tratar valores nulos (imputación con la media), columna por columna
   (no en bloque, para evitar medias sin sentido en columnas no numéricas).
"""
import pandas as pd
import numpy as np

RAW_PATH = "data/2016_raw.csv"
CLEAN_PATH = "data/2016_clean.csv"


def cargar(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, header=0)
    print(f"Cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def revisar_tipos(df: pd.DataFrame) -> pd.DataFrame:
    print("\nTipos de datos antes de limpiar:")
    print(df.dtypes)
    return df.dtypes


def limpiar_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Quita espacios, convierte '' en NaN y castea columnas numéricas que
    hayan quedado como texto (por ejemplo, por espacios extra en los valores)."""
    df = df.copy()
    columnas_numericas = [
        "Happiness Rank", "Happiness Score", "Lower Confidence Interval",
        "Upper Confidence Interval", "Economy (GDP per Capita)", "Family",
        "Health (Life Expectancy)", "Freedom", "Trust (Government Corruption)",
        "Generosity", "Dystopia Residual",
    ]
    for col in columnas_numericas:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip().replace("", np.nan)
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["Country", "Region"]:
        df[col] = df[col].astype(str).str.strip()
    return df


def imputar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    nulos = df.isna().sum()
    nulos = nulos[nulos > 0]
    print("\nColumnas con valores nulos (antes de imputar):")
    print(nulos if len(nulos) else "  (ninguna)")
    for col in nulos.index:
        media = df[col].mean()
        df.fillna({col: media}, inplace=True)
        print(f"  {col}: imputado con la media = {media:.3f}")
    return df


def main():
    df = cargar(RAW_PATH)
    revisar_tipos(df)
    df = limpiar_tipos(df)
    df = imputar_nulos(df)
    print("\nTipos de datos después de limpiar:")
    print(df.dtypes)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"\nGuardado: {CLEAN_PATH}")


if __name__ == "__main__":
    main()
