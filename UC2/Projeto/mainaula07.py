# Importe o seu módulo.
# Assumimos aqui que 'statistic.py' está no mesmo diretório.
import pandas as pd
import numpy as np

from statcaula07 import calcular_medidas_descritivas, gerar_painel_boxplot

# 1. Definir o caminho do arquivo
# Ajuste o caminho para onde o seu arquivo está
caminho_csv = "C:/Users/luiz.calmeida/Documents/BigDataSenacNI/UC2/Aula06/vendas_2023.csv" 

# 2. Carregar os dados
try:
    df = pd.read_csv(caminho_csv,
        encoding='latin1',   # ou 'cp1252'
        sep=';',             # troque para ',' se o seu arquivo for realmente separado por vírgula
        engine='python',     # ajuda em casos com campos complexos
        on_bad_lines='warn'  # não quebra se houver linha malformada
    )

    
    rent_col = (
        df['PER_RENTABILIDADE']
        .astype(str)                 # garante string
        .str.strip()                 # remove espaços
        .str.replace('%', '', regex=False)  # remove percentuais
        .str.replace('.', '', regex=False)  # remove separador de milhar
        .str.replace(',', '.', regex=False) # troca vírgula por ponto
    )

    
    # Converte para float; erros viram NaN
    rentabilidade = pd.to_numeric(rent_col, errors='coerce')


    
    # 3. Preparar o array para a análise
    rentabilidade_array = (rentabilidade.dropna().to_numpy(dtype=float))
    
    # 4. Chamar a função de cálculo do seu módulo
    medidas_calculadas = calcular_medidas_descritivas(rentabilidade_array)
    
    # 5. Chamar a função de visualização do seu módulo
    if medidas_calculadas:
        gerar_painel_boxplot(
            rentabilidade_array, 
            medidas_calculadas, 
            titulo_boxplot='Boxplot de Preços (vendas_produtos.csv)', 
            caminho_salvar='Relatorio_Precos.png'
        )

except FileNotFoundError:
    print(f"Erro: O arquivo {caminho_csv} não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")