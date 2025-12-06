"""Modelo de gerenciamento de usuários"""

import pandas as pd
from data.manager import DataManager

class UserManager:
    """Gerenciador de usuários"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def verificar_login(self, login, senha):
        """Verifica credenciais de login"""
        if self.data_manager.df_users is None or len(self.data_manager.df_users) == 0:
            return False, None
        
        usuario = self.data_manager.df_users[
            (self.data_manager.df_users['login'] == login) & 
            (self.data_manager.df_users['senha'] == senha)
        ]
        
        if len(usuario) > 0:
            tipo = usuario.iloc[0]['tipo']
            return True, tipo
        return False, None
    
    def obter_usuario(self, login):
        """Obtém dados de um usuário"""
        if self.data_manager.df_users is None:
            return None
        
        usuario = self.data_manager.df_users[self.data_manager.df_users['login'] == login]
        if len(usuario) > 0:
            return usuario.iloc[0].to_dict()
        return None
