import pandas as pd
import requests
from io import StringIO


def obter_dados_csv(produto, ano):
    # URL fixa para o CSV
    base_url = 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv'
    
    # Baixar o conteúdo do CSV
    response = requests.get(base_url)
    
    if response.status_code != 200:
        raise Exception(f"Falha ao baixar o arquivo CSV da URL: {base_url}")
    
    # Ler o CSV diretamente da resposta
    df = pd.read_csv(StringIO(response.text), delimiter=';')
    
    # Limpar os nomes das colunas
    df.columns = df.columns.str.strip()
    
    # Verifica se as colunas 'id' e 'control' existem antes de tentar removê-las
    for col in ['id', 'control']:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # Filtra os dados com base no produto e ano fornecidos
    df_filtrado = df[(df['produto'] == produto) & (df.columns.str.contains(str(ano)))]
    
    # Converte para o formato longo
    df_melted = pd.melt(df_filtrado, id_vars=["produto"], var_name="ano", value_name="quantidade")

    # Ordena os dados por produto e ano
    df_melted.sort_values(['produto', 'ano'], inplace=True)

    return df_melted