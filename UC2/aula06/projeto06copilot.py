import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração visual
sns.set(style='whitegrid', palette='deep')
plt.rcParams['figure.figsize'] = (10, 6)

# === 1) Ler CSV corretamente (separador ';', encoding 'latin1') ===
df = pd.read_csv(
    'vendas_2023.csv',
    sep=';',
    encoding='latin1',
    on_bad_lines='skip'  # ignora linhas quebradas
)

# === 2) Converter datas ===
# Se houver horas (ex.: 15/05/2023 10:32), troque o format para '%d/%m/%Y %H:%M:%S' ou use dayfirst=True sem format
df['DTA_ENTRADA_SAIDA'] = pd.to_datetime(
    df['DTA_ENTRADA_SAIDA'],
    format='%d/%m/%Y',   # ajuste se houver horário
    errors='coerce'
)
df = df.dropna(subset=['DTA_ENTRADA_SAIDA'])

# === 3) Converter VAL_VENDA para número (tratando formato brasileiro) ===
df['VAL_VENDA'] = (
    df['VAL_VENDA'].astype(str)
    .str.replace('R$', '', regex=False).str.strip()
    .str.replace('.', '', regex=False)   # remove separador de milhar
    .str.replace(',', '.', regex=False)  # vírgula -> ponto decimal
)
df['VAL_VENDA'] = pd.to_numeric(df['VAL_VENDA'], errors='coerce')
df = df.dropna(subset=['VAL_VENDA'])

# === 4) Filtrar período de março a dezembro ===
mask_mar_dez = df['DTA_ENTRADA_SAIDA'].dt.month.between(3, 12)
df = df[mask_mar_dez].copy()

# === 5) Agregar para faturamento mensal ===
fat_mensal = (
    df.groupby(df['DTA_ENTRADA_SAIDA'].dt.to_period('M'))['VAL_VENDA']
    .sum()
    .reset_index()
)
fat_mensal['Data'] = fat_mensal['DTA_ENTRADA_SAIDA'].dt.to_timestamp()
fat_mensal['MesLabel'] = fat_mensal['Data'].dt.strftime('%b/%Y')  # ex.: Mar/2023

# Verifique rapidamente:
print(fat_mensal)

serie = fat_mensal['VAL_VENDA']
descr = serie.describe()  # count, mean, std, min, quartis, max

cv = serie.std(ddof=1) / serie.mean()  # Coeficiente de Variação (volatilidade relativa)
skewness = serie.skew()                 # Assimetria: >0 cauda à direita; <0 cauda à esquerda
kurtosis = serie.kurtosis()             # Curtose: >0 mais "pontudo"; <0 mais "plano"

print('===== ESTATÍSTICA DESCRITIVA =====')
print(descr)
print(f'Coeficiente de variação (CV): {cv:.3f}')
print(f'Assimetria (skewness): {skewness:.3f}')
print(f'Curtose (kurtosis): {kurtosis:.3f}')

# Histograma + KDE para visualizar a distribuição dos meses
sns.histplot(serie, kde=True, bins=6, color='#1f77b4')
plt.title('Distribuição do Faturamento Mensal (Mar–Dez)')
plt.xlabel('Faturamento mensal (R$)')
plt.ylabel('Contagem de meses')
plt.tight_layout()
plt.show()

fat_mensal = fat_mensal.sort_values('Data').copy()
fat_mensal['MoM_%'] = fat_mensal['VAL_VENDA'].pct_change() * 100
fat_mensal['Acumulado'] = fat_mensal['VAL_VENDA'].cumsum()

print('===== VARIAÇÃO MENSAL (MoM) =====')
print(fat_mensal[['MesLabel', 'VAL_VENDA', 'MoM_%']])

# Gráfico linha do faturamento
sns.lineplot(data=fat_mensal, x='MesLabel', y='VAL_VENDA', marker='o')
plt.title('Faturamento Mensal (Mar–Dez)')
plt.xlabel('Mês')
plt.ylabel('Faturamento (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico da variação MoM
sns.barplot(data=fat_mensal, x='MesLabel', y='MoM_%', color='#ff7f0e')
plt.axhline(0, color='black', linewidth=1)
plt.title('Variação Percentual Mensal (MoM)')
plt.xlabel('Mês')
plt.ylabel('MoM (%)')
plt.xticks(rotation=45)
plt.tight_layout()

# Índice do mês para regressão (1, 2, 3, ... na ordem)
fat_mensal['MesIndex'] = np.arange(1, len(fat_mensal) + 1)

# Ajuste linear: y = a*x + b
a, b = np.polyfit(fat_mensal['MesIndex'], fat_mensal['VAL_VENDA'], 1)
y_pred = a * fat_mensal['MesIndex'] + b

# R² da regressão
ss_res = np.sum((fat_mensal['VAL_VENDA'] - y_pred) ** 2)
ss_tot = np.sum((fat_mensal['VAL_VENDA'] - fat_mensal['VAL_VENDA'].mean()) ** 2)
r2 = 1 - ss_res/ss_tot

print(f'Tendência linear: y = {a:.2f}*Mes + {b:.2f} (R² = {r2:.3f})')

# Plot com tendência
plt.plot(fat_mensal['MesLabel'], fat_mensal['VAL_VENDA'], marker='o', label='Real')
plt.plot(fat_mensal['MesLabel'], y_pred, color='red', linestyle='--', label='Tendência linear')
plt.title('Faturamento com Tendência Linear')
plt.xlabel('Mês')
plt.ylabel('Faturamento (R$)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Média móvel de 3 meses (suavização)
fat_mensal['MM_3'] = fat_mensal['VAL_VENDA'].rolling(window=3, min_periods=1).mean()
fat_mensal['Residuo'] = fat_mensal['VAL_VENDA'] - fat_mensal['MM_3']

print('===== VOLATILIDADE (Resíduo vs Média Móvel) =====')
print(fat_mensal[['MesLabel', 'VAL_VENDA', 'MM_3', 'Residuo']])

plt.plot(fat_mensal['MesLabel'], fat_mensal['VAL_VENDA'], marker='o', label='Real')
plt.plot(fat_mensal['MesLabel'], fat_mensal['MM_3'], marker='o', label='Média móvel (3m)')
plt.title('Suavização por Média Móvel (3 meses)')
plt.xlabel('Mês'); plt.ylabel('Faturamento (R$)')
plt.legend(); plt.xticks(rotation=45); plt.tight_layout(); plt.show()

sns.barplot(data=fat_mensal, x='MesLabel', y='Residuo', color='#2ca02c')
plt.axhline(0, color='black')
plt.title('Resíduos (Real – Média Móvel)')
plt.xlabel('Mês'); plt.ylabel('Resíduo (R$)')

q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
iqr = q3 - q1
lim_inf, lim_sup = q1 - 1.5*iqr, q3 + 1.5*iqr

fat_mensal['Zscore'] = (fat_mensal['VAL_VENDA'] - serie.mean()) / serie.std(ddof=1)
fat_mensal['Outlier_IQR'] = (fat_mensal['VAL_VENDA'] < lim_inf) | (fat_mensal['VAL_VENDA'] > lim_sup)
fat_mensal['Outlier_Z3'] = fat_mensal['Zscore'].abs() >= 3

print('===== OUTLIERS =====')
print(fat_mensal[['MesLabel', 'VAL_VENDA', 'Zscore', 'Outlier_IQR', 'Outlier_Z3']])

# Boxplot para visualizar valores atípicos
sns.boxplot(x=np.zeros(len(serie)), y=serie)
plt.title('Boxplot do Faturamento Mensal (Mar–Dez)')
plt.ylabel('Faturamento (R$)')
plt.xticks([]); plt.tight_layout(); plt.show()

# Série diária de faturamento
fat_diario = (
    df.groupby(df['DTA_ENTRADA_SAIDA'].dt.to_period('D'))['VAL_VENDA']
    .sum()
    .reset_index()
)
fat_diario['Data'] = fat_diario['DTA_ENTRADA_SAIDA'].dt.to_timestamp()
fat_diario['Mes'] = fat_diario['Data'].dt.to_period('M')

# Estatística de volatilidade por mês (CV diário dentro de cada mês)
vol_mensal = fat_diario.groupby('Mes')['VAL_VENDA'].agg(['mean','std','count']).reset_index()
vol_mensal['CV_diario'] = vol_mensal['std'] / vol_mensal['mean']

print('===== VOLATILIDADE DIÁRIA POR MÊS =====')
print(vol_mensal)

# Gráfico do CV diário por mês
vol_mensal['MesLabel'] = vol_mensal['Mes'].dt.strftime('%b/%Y')
sns.barplot(data=vol_mensal, x='MesLabel', y='CV_diario', color='#9467bd')
plt.title('Volatilidade Diária por Mês (CV)')
plt.xlabel('Mês'); plt.ylabel('CV diário')
plt.xticks(rotation=45); plt.tight_layout(); plt.show()

# Autocorrelação (lag-1) da série diária — proxy de dependência temporal
ac1_daily = fat_diario['VAL_VENDA'].autocorr(lag=1)

if 'QUANTIDADE' in df.columns:
    # Converter QUANTIDADE para numérico (se necessário)
    df['QUANTIDADE'] = pd.to_numeric(df['QUANTIDADE'], errors='coerce')
    df = df.dropna(subset=['QUANTIDADE'])

    # Agregar por mês
    agg = df.groupby(df['DTA_ENTRADA_SAIDA'].dt.to_period('M')).agg(
        Faturamento=('VAL_VENDA', 'sum'),
        Qty=('QUANTIDADE', 'sum')
    ).reset_index()
    agg['Data'] = agg['DTA_ENTRADA_SAIDA'].dt.to_timestamp()
    agg['PrecoMedio'] = agg['Faturamento'] / agg['Qty']

    print('===== Faturamento, Quantidade e Preço Médio por Mês =====')
    print(agg[['Data','Faturamento','Qty','PrecoMedio']])

    # Correlação
    corr = agg[['Faturamento','Qty','PrecoMedio']].corr()
    print('\nCorrelação:\n', corr)

    # Heatmap da correlação
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlação entre Faturamento, Quantidade e Preço Médio')
    plt.tight_layout(); plt.show()

if 'NOME_CATEGORIA' in df.columns:
    cat_mensal = (
        df.groupby([df['DTA_ENTRADA_SAIDA'].dt.to_period('M'), 'NOME_CATEGORIA'])['VAL_VENDA']
        .sum()
        .reset_index()
    )
    cat_mensal['MesLabel'] = cat_mensal['DTA_ENTRADA_SAIDA'].dt.strftime('%b/%Y')

    # Top categorias (por faturamento total)
    top_cats = (cat_mensal.groupby('NOME_CATEGORIA')['VAL_VENDA'].sum()
                .sort_values(ascending=False).head(5).index.tolist())
    cat_top = cat_mensal[cat_mensal['NOME_CATEGORIA'].isin(top_cats)]

    sns.lineplot(data=cat_top, x='MesLabel', y='VAL_VENDA', hue='NOME_CATEGORIA', marker='o')
    plt.title('Top Categorias por Faturamento (Mar–Dez)')
    plt.xlabel('Mês'); plt.ylabel('Faturamento (R$)')
