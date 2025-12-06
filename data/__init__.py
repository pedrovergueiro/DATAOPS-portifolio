"""Camada de dados"""

from .manager import DataManager
from .loader import carregar_dataframe_seguro
from .saver import salvar_dataframe_seguro

__all__ = ['DataManager', 'carregar_dataframe_seguro', 'salvar_dataframe_seguro']
