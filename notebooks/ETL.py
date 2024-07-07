from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
# --------------------------------------------------------------------- # 
import re
import requests


class ConvertPriceToNumber(BaseEstimator, TransformerMixin):

    """
    Elimina caracteres não numéricos e realiza a conversão do dtype para float da coluna.
    
    Parâmetros:
    column: column of str
        Nome da coluna: Book_Price

    Métodos:
        fit: Método utilizado para conformidade com o pipeline do Scikit-Learn. Não realiza nenhuma ação.
        transform: Aplica a transformação para os valores na coluna especificada.
    """

    def __init__(self, column_name):
        self.column_name = column_name
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()  # Copiando o input do dataframe para evitar modificar o original.

        df[self.column_name] = df[self.column_name].str.replace(r'[^\d.]', '', regex=True)
        df[self.column_name] = df[self.column_name].astype(float)

        return df


class TransformPriceIntoReal(BaseEstimator, TransformerMixin):

    """
    Cria nova coluna com o valor do livro na cotação BRL (REAL)
    
    Parâmetros:
    column: column of str
        Nome da coluna: Book_Price

    Métodos:
        fit: Método utilizado para conformidade com o pipeline do Scikit-Learn. Não realiza nenhuma ação.
        transform: Realiza o calculo da cotação de EUR para BRL e cria a coluna com o valor cotado.
    """

    def __init__(self, column_name):
        self.column_name = column_name

    
    def fit(self, X, y=None):
        return self
    
    # Função para obter a taxa de câmbio atual do EUR para BRL
    def get_exchange_rate(self):
        url = 'https://api.exchangerate-api.com/v4/latest/EUR'

        response = requests.get(url)
        data = response.json()

        return data['rates']['BRL']

    def transform(self, X):
        df = X.copy()  # Copiando o input do dataframe para evitar modificar o original.

        # Obter a taxa de câmbio atual
        exchange_rate = self.get_exchange_rate()

        df["Book_Price_BR"] = df[self.column_name] * exchange_rate

        return df


class ConvertRatingToNumber(BaseEstimator, TransformerMixin):

    """
    Converte os valores por seus respectivos valores numéricos e realiza a alteração do dtype para int.
    
    Parâmetros:
    column: column of str
        Nome da coluna: Book_Rating

    Métodos:
        fit: Método utilizado para conformidade com o pipeline do Scikit-Learn. Não realiza nenhuma ação.
        transform: Aplica a transformação para os valores na coluna especificada.
    """

    def __init__(self, column_name):

        self.column_name = column_name
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        
        df = X.copy()  # Copiando o input do dataframe para evitar modificar o original.

        rating_map = { 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5 }

        # Convertendo os valores para numéricos utilizando a função map.
        df[self.column_name] = df[self.column_name].str.lower().map(rating_map)
        df[self.column_name] = df[self.column_name].astype(int)

        return df
    
    
class QuantityBookAvailable(BaseEstimator, TransformerMixin):

    """
    Cria nova coluna com o valor em quantidade disponível no estoque do livro.
    
    Parâmetros:
    column: column of str
        Nome da coluna: Book_Stock

    Métodos:
        fit: Método utilizado para conformidade com o pipeline do Scikit-Learn. Não realiza nenhuma ação.
        transform: Aplica a transformação para os valores na coluna especificada.
    """

    def __init__(self, column_name):

        self.column_name = column_name
    
    def fit(self, X, y=None):
        return self
    
    def extract_numbers(self, text): # realizando um regex para pegar os valores numéricos da string depois da primeira aparição de ()
        match = re.search(r'\((\d+)', text)
        return match.group(1) if match else 0

    def transform(self, X):
        
        df = X.copy()  # Copiando o input do dataframe para evitar modificar o original.

        # Criando nova coluna com a quantidade de itens no estoque e convertendo o dtype para int
        df["Book_Stock_Available"] = df[self.column_name].apply(self.extract_numbers).astype(int)

        return df
    
class TransformBookStock(BaseEstimator, TransformerMixin):

    """
    Altera a coluna para uma coluna do dtype bool caso esteja no estoque o livro.
    
    Parâmetros:
    column: column of str
        Nome da coluna: Book_Stock

    Métodos:
        fit: Método utilizado para conformidade com o pipeline do Scikit-Learn. Não realiza nenhuma ação.
        transform: Aplica a transformação para os valores na coluna especificada.
    """

    def __init__(self, column_name):

        self.column_name = column_name
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        
        df = X.copy()  # Copiando o input do dataframe para evitar modificar o original.
        df[self.column_name] = np.where(df[self.column_name].str.contains("In"), True, False).astype(bool)

        return df
    
class ChangeOrderColumns(BaseEstimator, TransformerMixin):

    """
    Altera a ordem das colunas de exibição do dataframe.
    
    Parâmetros:
    columns: list of column

    Métodos:
        fit: Método utilizado para conformidade com o pipeline do Scikit-Learn. Não realiza nenhuma ação.
        transform: Realiza a alteração das ordens das colunas.
    """

    def __init__(self, column_names):

        self.column_names = column_names
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        
        df = X.copy()  # Copiando o input do dataframe para evitar modificar o original.

        df = df[self.column_names]

        return df

