# Importe o seu módulo.
# Assumimos aqui que 'statistic.py' está no mesmo diretório.
import pandas as pd
from statistic import calcular_medidas_descritivas, gerar_painel_boxplot

# 1. Definir o caminho do arquivo
# Ajuste o caminho para onde o seu arquivo está
caminho_csv = "C:/Users/luiz.calmeida/Documents/BigDataSenacNI/UC2/Aula03/vendas_produtos.csv" 

# 2. Carregar os dados
try:
    df = pd.read_csv(caminho_csv)
    
    # 3. Preparar o array para a análise
    precos_array = df['preco'].values
    
    # 4. Chamar a função de cálculo do seu módulo
    medidas_calculadas = calcular_medidas_descritivas(precos_array)
    
    # 5. Chamar a função de visualização do seu módulo
    if medidas_calculadas:
        gerar_painel_boxplot(
            precos_array, 
            medidas_calculadas, 
            titulo_boxplot='Boxplot de Preços (vendas_produtos.csv)', 
            caminho_salvar='Relatorio_Precos.png'
        )

except FileNotFoundError:
    print(f"Erro: O arquivo {caminho_csv} não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")