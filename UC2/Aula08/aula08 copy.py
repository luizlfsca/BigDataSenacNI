import os
import pandas as pd
import numpy as np

# 1) Caminho do arquivo (string, não DataFrame!)
CSV_PATH = r"C:\Users\luiz.calmeida\Documents\BigDataSenacNI\UC2\Aula06\vendas_2023.csv"

# 2) Leitura do CSV (encoding/separador típicos no Brasil)
df = pd.read_csv(
    CSV_PATH,
    encoding="latin1",     # ou 'cp1252'
    sep=";",               # troque para ',' se necessário
  )


# 3) Nome da coluna de rentabilidade (ajuste se necessário)
COL_RENT = "PER_RENTABILIDADE"  # confirme o nome exato no seu arquivo

if COL_RENT not in df.columns:
    raise KeyError(f"Coluna de rentabilidade '{COL_RENT}' não encontrada. Nomes disponíveis: {list(df.columns)}")

# 4) Converter rentabilidade que está como texto em percentual brasileiro (ex.: '35,6%')
rent_col = (
    df[COL_RENT]
    .astype(str)
    .str.strip()
    .str.replace(".", "", regex=False)   # remove milhares
    .str.replace(",", ".", regex=False)  # vírgula decimal -> ponto
)

rentabilidade = pd.to_numeric(rent_col, errors="coerce")
rentabilidade_array = rentabilidade.dropna().to_numpy(dtype=float)

# 5) Estatísticas (amostrais: ddof=1 costuma ser mais adequado p/ negócio)
media = np.mean(rentabilidade_array)
variancia_amostral = np.var(rentabilidade_array, ddof=1)
desvio_amostral    = np.std(rentabilidade_array, ddof=1)

# Se você quiser as versões populacionais:
variancia_pop = np.var(rentabilidade_array, ddof=0)
desvio_pop    = np.std(rentabilidade_array, ddof=0)

# Coeficiente de Variação (CV) em porcentagem
cv = (desvio_amostral / media) * 100 if media != 0 else np.nan
# Distância da variância em relação à média^2 (equivale ao (CV em fração)^2)
distancia = variancia_amostral / (media ** 2) if media != 0 else np.nan
cvabs=abs(cv)
print("\n--- Análise de Rentabilidade (%) ---")
print(f"Média: {media:.2f}%")
print(f"Variância (amostral): {variancia_amostral:.2f} (p.p.^2)")
print(f"Desvio Padrão (amostral): {desvio_amostral:.2f} p.p.")
print("-" * 100)
print(f"Coeficiente de Variação (CV): {cvabs:.2f}%")
print(f"Distância da Variância / Média²: {distancia:.4f}")

# 6) Classificação de dispersão (usando CV%)
if not np.isnan(cv):
    if cvabs <= 10:
        analise = "Baixa dispersão dos dados em relação à média."
    elif cvabs < 25:
        analise = "Dispersão moderada dos dados em relação à média."
    else:
        analise = "Alta dispersão dos dados em relação à média."
else:
    analise = "CV indefinido (média igual a zero ou dados insuficientes)."

print(f"Conclusão da Dispersão: {analise}")
