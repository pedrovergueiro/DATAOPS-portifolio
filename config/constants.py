"""Constantes do sistema"""

TABELA_SIZES = {
    "201": {"size": "#1", "peso": 0.000076},
    "202": {"size": "#2", "peso": 0.000063},
    "203": {"size": "#0", "peso": 0.000096},
    "204": {"size": "#0", "peso": 0.000096},
    "205": {"size": "#2", "peso": 0.000063},
    "206": {"size": "#00", "peso": 0.000121},
    "207": {"size": "#0", "peso": 0.000096},
    "208": {"size": "#3", "peso": 0.000050},
    "209": {"size": "#0", "peso": 0.000096},
    "210": {"size": "#00", "peso": 0.000121},
    "211": {"size": "#0", "peso": 0.000096},
    "212": {"size": "#0", "peso": 0.000096},
    "213": {"size": "#00", "peso": 0.000121},
    "214": {"size": "#4", "peso": 0.000038}
}

MAQUINAS_VALIDAS = [str(i) for i in range(201, 215)]

COLUNAS_DADOS = [
    'maquina', 'rej1_defect', 'rej1_local', 'rej2_defect', 'rej2_local',
    'rej3_defect', 'rej3_local', 'percent_cam_d', 'percent_cam_w',
    'data_hora', 'origem', 'justificativa', 'usuario_reg', 'lote', 
    'numero_caixa', 'size', 'peso'
]

COLUNAS_USUARIOS = ['login', 'senha', 'tipo', 'permissoes', 'primeiro_login']

COLUNAS_LOG = ['acao', 'usuario', 'detalhes', 'data_hora']

USUARIOS_PADRAO = [
    {'login': 'desenvolvedor', 'senha': '010524Np@', 'tipo': 'Desenvolvedor', 'permissoes': True, 'primeiro_login': True},
    {'login': 'coordenador', 'senha': 'coord123', 'tipo': 'Coordenador', 'permissoes': True, 'primeiro_login': True},
    {'login': 'encarregado', 'senha': 'enc123', 'tipo': 'Encarregado', 'permissoes': True, 'primeiro_login': True},
    {'login': 'analista', 'senha': 'ana123', 'tipo': 'Analista', 'permissoes': True, 'primeiro_login': True},
    {'login': 'operador', 'senha': 'oper123', 'tipo': 'Operador', 'permissoes': False, 'primeiro_login': True}
]
