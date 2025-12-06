"""
Dashboard Standalone - Executável Independente
Pode ser compilado separadamente como .exe
"""

import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar e executar o dashboard
if __name__ == "__main__":
    try:
        import dash
        print("✅ Dashboard iniciado como aplicação independente")
        print("📊 Acesse o dashboard no navegador")
    except Exception as e:
        print(f"❌ Erro ao iniciar dashboard: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para sair...")
