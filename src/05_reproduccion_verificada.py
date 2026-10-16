"""
Reproducción directa, sin LLM, de los mismos gráficos que el agente
LangChain + watsonx genera en 04_agente_langchain_watsonx.py -- para poder
verificar y correr el proyecto sin necesitar credenciales de watsonx.

Mismos 4 "tasks" del lab + los 3 ejercicios propuestos.
"""
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/student-mat.csv"
IMG_DIR = "img"


def cargar():
    return pd.read_csv(DATA_PATH)


def task1_genero(df):
    counts = df["sex"].value_counts()
    fig, ax = plt.subplots()
    counts.plot(kind="bar", ax=ax, color=["#4C78A8", "#F58518"])
    ax.set_title("Conteo de alumnos por género")
    ax.set_xlabel("Género")
    ax.set_ylabel("Cantidad")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/task1_genero.png", dpi=150)
    plt.close(fig)
    return counts


def task2_walc_genero(df):
    # Barras, no pie: un pie de promedios no es correcto (no son partes de un todo).
    promedio = df.groupby("sex")["Walc"].mean()
    fig, ax = plt.subplots()
    promedio.plot(kind="bar", ax=ax, color=["#4C78A8", "#F58518"])
    ax.set_title("Consumo de alcohol en fin de semana (Walc), promedio por género")
    ax.set_ylabel("Walc promedio (1-5)")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/task2_walc_genero.png", dpi=150)
    plt.close(fig)
    return promedio


def task3_freetime_g3(df):
    fig, ax = plt.subplots()
    df.boxplot(column="G3", by="freetime", ax=ax)
    ax.set_title("Nota final (G3) por nivel de tiempo libre")
    ax.set_xlabel("freetime (1=poco, 5=mucho)")
    ax.set_ylabel("G3")
    plt.suptitle("")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/task3_freetime_g3.png", dpi=150)
    plt.close(fig)


def task4_alcohol_g3(df):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(df["Dalc"], df["G3"], alpha=0.3)
    axes[0].set_xlabel("Dalc (alcohol entre semana)")
    axes[0].set_ylabel("G3")
    axes[0].set_title(f"Dalc vs G3 (r={df['Dalc'].corr(df['G3']):.2f})")
    axes[1].scatter(df["Walc"], df["G3"], alpha=0.3, color="#F58518")
    axes[1].set_xlabel("Walc (alcohol fin de semana)")
    axes[1].set_ylabel("G3")
    axes[1].set_title(f"Walc vs G3 (r={df['Walc'].corr(df['G3']):.2f})")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/task4_alcohol_g3.png", dpi=150)
    plt.close(fig)


def ejercicio1_educacion_padres(df):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(df["Medu"], df["G3"], alpha=0.3)
    axes[0].set_xlabel("Medu (educación de la madre)")
    axes[0].set_ylabel("G3")
    axes[0].set_title(f"r={df['Medu'].corr(df['G3']):.2f}")
    axes[1].scatter(df["Fedu"], df["G3"], alpha=0.3, color="#F58518")
    axes[1].set_xlabel("Fedu (educación del padre)")
    axes[1].set_ylabel("G3")
    axes[1].set_title(f"r={df['Fedu'].corr(df['G3']):.2f}")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/ej1_educacion_padres.png", dpi=150)
    plt.close(fig)


def ejercicio2_internet(df):
    promedio = df.groupby("internet")["G3"].mean()
    fig, ax = plt.subplots()
    promedio.plot(kind="bar", ax=ax, color=["#F58518", "#4C78A8"])
    ax.set_title("Nota final (G3) promedio: con/sin internet en casa")
    ax.set_ylabel("G3 promedio")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/ej2_internet.png", dpi=150)
    plt.close(fig)
    return promedio


def ejercicio3_ausencias(df):
    fig, ax = plt.subplots()
    ax.scatter(df["absences"], df["G3"], alpha=0.3)
    ax.set_xlabel("absences")
    ax.set_ylabel("G3")
    r = df["absences"].corr(df["G3"])
    ax.set_title(f"Ausencias vs. nota final (r={r:.2f})")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}/ej3_ausencias.png", dpi=150)
    plt.close(fig)
    return r


def main():
    df = cargar()
    print(f"Filas: {len(df)} (esperado: 395)")
    print("\nTask 1 - conteo por género:")
    print(task1_genero(df))
    print("\nTask 2 - Walc promedio por género:")
    print(task2_walc_genero(df))
    task3_freetime_g3(df)
    task4_alcohol_g3(df)
    ejercicio1_educacion_padres(df)
    print("\nEjercicio 2 - G3 promedio con/sin internet:")
    print(ejercicio2_internet(df))
    r = ejercicio3_ausencias(df)
    print(f"\nEjercicio 3 - correlación absences vs G3: {r:.2f}")
    print(f"\nAlumnos con G3 = 0: {(df['G3'] == 0).sum()}")


if __name__ == "__main__":
    main()
