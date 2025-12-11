
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1) Ler e preparar
caminho_csv = "C:/Users/luiz.calmeida/Documents/BigDataSenacNI/UC2/Aula06/vendas_2023.csv"

df = pd.read_csv(
    caminho_csv,
    encoding='latin1',
    sep=';',
    engine='python',
    on_bad_lines='warn'
)

# Converter PER_RENTABILIDADE (string de %) para float
x = (
    df['PER_RENTABILIDADE'].astype(str).str.strip()
    .str.replace('%', '', regex=False)
    .str.replace('.', '', regex=False)     # remove milhar
    .str.replace(',', '.', regex=False)    # vírgula -> ponto
)
x = pd.to_numeric(x, errors='coerce')
x_valid = x.dropna()

# ---------- Função utilitária para estatísticas ----------
def resumo(series: pd.Series, titulo: str):
    s = series.dropna()
    media = s.mean()
    mediana = s.median()
    moda_s = s.mode()
    moda = moda_s.iloc[0] if not moda_s.empty else np.nan

    q1 = s.quantile(0.25)
    q2 = s.quantile(0.50)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr

    variancia = s.var()             # amostral (ddof=1)
    desvio = s.std()                # amostral
    cv = (desvio / media) * 100 if media != 0 else np.nan
    skew = s.skew()
    kurt_excesso = s.kurt()         # excesso de curtose (0 ~ normal)

    print(f"\n---- {titulo} ----")
    print(f"N observações: {s.size}")
    print(f"Mínimo: {s.min():.6f} | Máximo: {s.max():.6f}")
    print(f"Média: {media:.6f}")
    print(f"Mediana: {mediana:.6f}")
    print(f"Moda: {moda:.6f}" if not np.isnan(moda) else "Moda: (sem moda)")
    print(f"Q1: {q1:.6f} | Q2: {q2:.6f} | Q3: {q3:.6f}")
    print(f"IQR: {iqr:.6f}")
    print(f"Limite Inferior (Tukey): {lim_inf:.6f}")
    print(f"Limite Superior (Tukey): {lim_sup:.6f}")
    print(f"Variância (amostral): {variancia:.6f}")
    print(f"Desvio padrão (amostral): {desvio:.6f}")
    print(f"Coeficiente de variação (%): {cv:.6f}")
    print(f"Assimetria (skew): {skew:.6f}")
    print(f"Curtose (excesso): {kurt_excesso:.6f}  (0 ~ normal)")
    return lim_inf, lim_sup

# 2) Estatísticas BRUTAS
lim_inf, lim_sup = resumo(x_valid, "Estatísticas BRUTAS de PER_RENTABILIDADE")

# 3) Quantos outliers?
n_outliers_inf = (x_valid < lim_inf).sum()
n_outliers_sup = (x_valid > lim_sup).sum()
print(f"\nOutliers abaixo do limite: {n_outliers_inf}")
print(f"Outliers acima do limite:  {n_outliers_sup}")

# 4) Filtrar outliers (versão "limpa")
x_clean = x_valid[(x_valid >= lim_inf) & (x_valid <= lim_sup)]

# 5) Estatísticas SEM OUTLIERS
_ = resumo(x_clean, "Estatísticas SEM OUTLIERS (Tukey)")

# 6) Visualizações (antes vs depois)
p1_raw, p99_raw = x_valid.quantile([0.01, 0.99])
p1_clean, p99_clean = x_clean.quantile([0.01, 0.99])

plt.figure(figsize=(12, 5))

# Histograma bruto
plt.subplot(1, 2, 1)
plt.hist(x_valid, bins=50, color="#4C78A8", edgecolor="white")
plt.title("Histograma (BRUTO)")
plt.xlabel("PER_RENTABILIDADE")
plt.ylabel("Frequência")
plt.xlim(p1_raw, p99_raw)

# Histograma sem outliers
plt.subplot(1, 2, 2)
plt.hist(x_clean, bins=50, color="#F58518", edgecolor="white")
plt.title("Histograma (SEM OUTLIERS)")
plt.xlabel("PER_RENTABILIDADE")
plt.ylabel("Frequência")
plt.xlim(p1_clean, p99_clean)

plt.tight_layout()
plt.show()

# 7) Boxplots para comparação
plt.figure(figsize=(8, 4))
plt.boxplot([x_valid, x_clean], vert=True, patch_artist=True,
            labels=["Bruto", "Sem outliers"],
            boxprops=dict(facecolor="#4C78A8"),
            medianprops=dict(color="black"))
plt.title("Boxplot: Bruto vs Sem Outliers")
plt.ylabel("PER_RENTABILIDADE")
plt.show()

# 8) (Opcional) Investigar registros extremos para auditoria
# Mostra os 10 menores e 10 maiores valores para você olhar no CSV original
print("\nMenores valores (para checar possíveis erros):")
print(x_valid.nsmallest(10))
print("\nMaiores valores (para checar possíveis erros):")
print(x_valid.nlargest(10))
