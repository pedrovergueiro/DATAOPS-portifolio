"""Sistema de Predição Inteligente usando Machine Learning"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import json
import os


class PredicaoInteligente:
    """Sistema de IA para predição de defeitos e análise preditiva"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.modelo_treinado = False
        self.historico_predicoes = []
        
    def analisar_padroes_maquina(self, maquina):
        """Analisa padrões históricos de uma máquina específica"""
        if self.data_manager.df is None or len(self.data_manager.df) == 0:
            return None
        
        # Filtrar dados da máquina
        df_maquina = self.data_manager.df[self.data_manager.df['maquina'] == maquina].copy()
        
        if len(df_maquina) == 0:
            return None
        
        # Análise de padrões
        analise = {
            'maquina': maquina,
            'total_registros': len(df_maquina),
            'defeitos_mais_comuns': self._analisar_defeitos_comuns(df_maquina),
            'locais_mais_problematicos': self._analisar_locais_problematicos(df_maquina),
            'media_rejeicao': self._calcular_media_rejeicao(df_maquina),
            'tendencia': self._analisar_tendencia(df_maquina),
            'horarios_criticos': self._analisar_horarios_criticos(df_maquina),
            'score_qualidade': self._calcular_score_qualidade(df_maquina)
        }
        
        return analise
    
    def prever_proximo_defeito(self, maquina):
        """Prevê qual será o próximo defeito mais provável"""
        if self.data_manager.df is None or len(self.data_manager.df) == 0:
            return None
        
        # Filtrar últimos 100 registros da máquina
        df_maquina = self.data_manager.df[self.data_manager.df['maquina'] == maquina].copy()
        
        if len(df_maquina) < 10:
            return {"erro": "Dados insuficientes para predição (mínimo 10 registros)"}
        
        # Pegar últimos registros
        df_recente = df_maquina.tail(100)
        
        # Coletar todos os defeitos
        defeitos = []
        for col in ['rej1_defect', 'rej2_defect', 'rej3_defect']:
            if col in df_recente.columns:
                defeitos.extend(df_recente[col].dropna().tolist())
        
        # Remover valores vazios e N/A
        defeitos = [d for d in defeitos if d and str(d).strip() and str(d).upper() != 'N/A']
        
        if not defeitos:
            return {"erro": "Nenhum defeito registrado"}
        
        # Análise de frequência
        contador = Counter(defeitos)
        defeitos_ordenados = contador.most_common(5)
        
        # Calcular probabilidades
        total = sum(contador.values())
        predicoes = []
        
        for defeito, freq in defeitos_ordenados:
            probabilidade = (freq / total) * 100
            predicoes.append({
                'defeito': defeito,
                'probabilidade': round(probabilidade, 2),
                'ocorrencias': freq,
                'nivel_risco': self._classificar_risco(probabilidade)
            })
        
        # Análise de tendência temporal
        tendencia = self._analisar_tendencia_temporal(df_recente)
        
        return {
            'maquina': maquina,
            'predicoes': predicoes,
            'defeito_mais_provavel': predicoes[0] if predicoes else None,
            'tendencia': tendencia,
            'confianca': self._calcular_confianca(len(df_recente)),
            'recomendacao': self._gerar_recomendacao(predicoes[0] if predicoes else None)
        }
    
    def detectar_anomalias(self, maquina=None):
        """Detecta anomalias nos dados de produção usando análise estatística"""
        if self.data_manager.df is None or len(self.data_manager.df) == 0:
            return []
        
        df = self.data_manager.df.copy()
        
        if maquina:
            df = df[df['maquina'] == maquina]
        
        if len(df) < 30:
            return []
        
        anomalias = []
        
        # 1. Detectar picos de rejeição
        for col in ['percent_cam_d', 'percent_cam_w']:
            if col in df.columns:
                valores = pd.to_numeric(df[col], errors='coerce').dropna()
                if len(valores) > 0:
                    media = valores.mean()
                    desvio = valores.std()
                    limite_superior = media + (2 * desvio)
                    
                    # Encontrar valores anômalos
                    anomalos = df[pd.to_numeric(df[col], errors='coerce') > limite_superior]
                    
                    for _, row in anomalos.iterrows():
                        anomalias.append({
                            'tipo': 'pico_rejeicao',
                            'maquina': row.get('maquina', 'N/D'),
                            'metrica': col,
                            'valor': float(row[col]),
                            'limite_esperado': round(limite_superior, 2),
                            'data_hora': row.get('data_hora', 'N/D'),
                            'severidade': 'ALTA' if float(row[col]) > limite_superior * 1.5 else 'MÉDIA'
                        })
        
        # 2. Detectar mudanças bruscas de padrão
        if 'data_hora' in df.columns:
            df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
            df = df.sort_values('data_hora')
            
            # Analisar últimos 7 dias vs 7 dias anteriores
            hoje = datetime.now()
            ultimos_7_dias = df[df['data_hora'] >= (hoje - timedelta(days=7))]
            dias_anteriores = df[(df['data_hora'] >= (hoje - timedelta(days=14))) & 
                                (df['data_hora'] < (hoje - timedelta(days=7)))]
            
            if len(ultimos_7_dias) > 0 and len(dias_anteriores) > 0:
                for col in ['percent_cam_d', 'percent_cam_w']:
                    if col in df.columns:
                        media_recente = pd.to_numeric(ultimos_7_dias[col], errors='coerce').mean()
                        media_anterior = pd.to_numeric(dias_anteriores[col], errors='coerce').mean()
                        
                        if not pd.isna(media_recente) and not pd.isna(media_anterior):
                            variacao = ((media_recente - media_anterior) / media_anterior) * 100
                            
                            if abs(variacao) > 30:  # Mudança de mais de 30%
                                anomalias.append({
                                    'tipo': 'mudanca_padrao',
                                    'maquina': maquina or 'TODAS',
                                    'metrica': col,
                                    'variacao_percentual': round(variacao, 2),
                                    'media_recente': round(media_recente, 2),
                                    'media_anterior': round(media_anterior, 2),
                                    'severidade': 'ALTA' if abs(variacao) > 50 else 'MÉDIA'
                                })
        
        # 3. Detectar defeitos repetitivos
        for col in ['rej1_defect', 'rej2_defect', 'rej3_defect']:
            if col in df.columns:
                defeitos_recentes = df.tail(20)[col].dropna().tolist()
                if defeitos_recentes:
                    contador = Counter(defeitos_recentes)
                    for defeito, freq in contador.items():
                        if freq >= 10:  # Mesmo defeito 10+ vezes em 20 registros
                            anomalias.append({
                                'tipo': 'defeito_repetitivo',
                                'maquina': maquina or 'N/D',
                                'defeito': defeito,
                                'frequencia': freq,
                                'percentual': round((freq / len(defeitos_recentes)) * 100, 2),
                                'severidade': 'ALTA'
                            })
        
        return anomalias
    
    def recomendar_acoes(self, maquina):
        """Recomenda ações baseadas em análise de dados"""
        analise = self.analisar_padroes_maquina(maquina)
        predicao = self.prever_proximo_defeito(maquina)
        anomalias = self.detectar_anomalias(maquina)
        
        if not analise:
            return []
        
        recomendacoes = []
        
        # Recomendações baseadas em score de qualidade
        score = analise.get('score_qualidade', 0)
        if score < 70:
            recomendacoes.append({
                'prioridade': 'ALTA',
                'tipo': 'manutencao',
                'acao': f'Máquina {maquina} com score baixo ({score}%) - Realizar manutenção preventiva',
                'impacto': 'Redução de até 40% nos defeitos'
            })
        
        # Recomendações baseadas em defeitos comuns
        defeitos_comuns = analise.get('defeitos_mais_comuns', [])
        if defeitos_comuns:
            defeito_principal = defeitos_comuns[0]
            recomendacoes.append({
                'prioridade': 'MÉDIA',
                'tipo': 'treinamento',
                'acao': f'Defeito "{defeito_principal["defeito"]}" representa {defeito_principal["percentual"]}% - Treinar operadores',
                'impacto': 'Redução de 20-30% neste defeito específico'
            })
        
        # Recomendações baseadas em horários críticos
        horarios = analise.get('horarios_criticos', [])
        if horarios:
            recomendacoes.append({
                'prioridade': 'MÉDIA',
                'tipo': 'processo',
                'acao': f'Horários críticos identificados: {", ".join([h["periodo"] for h in horarios[:2]])} - Aumentar supervisão',
                'impacto': 'Melhoria de 15-25% na qualidade'
            })
        
        # Recomendações baseadas em anomalias
        if anomalias:
            anomalias_altas = [a for a in anomalias if a.get('severidade') == 'ALTA']
            if anomalias_altas:
                recomendacoes.append({
                    'prioridade': 'URGENTE',
                    'tipo': 'investigacao',
                    'acao': f'{len(anomalias_altas)} anomalias de alta severidade detectadas - Investigar imediatamente',
                    'impacto': 'Prevenção de perdas significativas'
                })
        
        # Recomendações baseadas em tendência
        tendencia = analise.get('tendencia', {})
        if tendencia.get('direcao') == 'piorando':
            recomendacoes.append({
                'prioridade': 'ALTA',
                'tipo': 'intervencao',
                'acao': f'Tendência de piora detectada ({tendencia.get("variacao", 0)}%) - Intervenção necessária',
                'impacto': 'Evitar degradação contínua'
            })
        
        return recomendacoes
    
    def gerar_relatorio_ia(self, maquina=None):
        """Gera relatório completo com insights de IA"""
        if maquina:
            maquinas = [maquina]
        else:
            # Todas as máquinas
            if self.data_manager.df is None or len(self.data_manager.df) == 0:
                return None
            maquinas = self.data_manager.df['maquina'].unique().tolist()
        
        relatorio = {
            'data_geracao': datetime.now().isoformat(),
            'maquinas_analisadas': len(maquinas),
            'analises': [],
            'resumo_geral': {}
        }
        
        for maq in maquinas:
            analise = self.analisar_padroes_maquina(maq)
            predicao = self.prever_proximo_defeito(maq)
            anomalias = self.detectar_anomalias(maq)
            recomendacoes = self.recomendar_acoes(maq)
            
            if analise:
                relatorio['analises'].append({
                    'maquina': maq,
                    'analise': analise,
                    'predicao': predicao,
                    'anomalias': anomalias,
                    'recomendacoes': recomendacoes
                })
        
        # Resumo geral
        if relatorio['analises']:
            scores = [a['analise']['score_qualidade'] for a in relatorio['analises']]
            relatorio['resumo_geral'] = {
                'score_medio': round(np.mean(scores), 2),
                'melhor_maquina': max(relatorio['analises'], key=lambda x: x['analise']['score_qualidade'])['maquina'],
                'pior_maquina': min(relatorio['analises'], key=lambda x: x['analise']['score_qualidade'])['maquina'],
                'total_anomalias': sum(len(a['anomalias']) for a in relatorio['analises']),
                'total_recomendacoes': sum(len(a['recomendacoes']) for a in relatorio['analises'])
            }
        
        return relatorio
    
    # Métodos auxiliares privados
    
    def _analisar_defeitos_comuns(self, df):
        """Analisa defeitos mais comuns"""
        defeitos = []
        for col in ['rej1_defect', 'rej2_defect', 'rej3_defect']:
            if col in df.columns:
                defeitos.extend(df[col].dropna().tolist())
        
        defeitos = [d for d in defeitos if d and str(d).strip() and str(d).upper() != 'N/A']
        
        if not defeitos:
            return []
        
        contador = Counter(defeitos)
        total = len(defeitos)
        
        return [
            {
                'defeito': defeito,
                'ocorrencias': freq,
                'percentual': round((freq / total) * 100, 2)
            }
            for defeito, freq in contador.most_common(5)
        ]
    
    def _analisar_locais_problematicos(self, df):
        """Analisa locais mais problemáticos"""
        locais = []
        for col in ['rej1_local', 'rej2_local', 'rej3_local']:
            if col in df.columns:
                locais.extend(df[col].dropna().tolist())
        
        locais = [l for l in locais if l and str(l).strip() and str(l).upper() != 'N/A']
        
        if not locais:
            return []
        
        contador = Counter(locais)
        total = len(locais)
        
        return [
            {
                'local': local,
                'ocorrencias': freq,
                'percentual': round((freq / total) * 100, 2)
            }
            for local, freq in contador.most_common(3)
        ]
    
    def _calcular_media_rejeicao(self, df):
        """Calcula média de rejeição"""
        cam_d = pd.to_numeric(df['percent_cam_d'], errors='coerce').mean()
        cam_w = pd.to_numeric(df['percent_cam_w'], errors='coerce').mean()
        
        return {
            'cam_d': round(cam_d, 2) if not pd.isna(cam_d) else 0,
            'cam_w': round(cam_w, 2) if not pd.isna(cam_w) else 0,
            'media_geral': round((cam_d + cam_w) / 2, 2) if not pd.isna(cam_d) and not pd.isna(cam_w) else 0
        }
    
    def _analisar_tendencia(self, df):
        """Analisa tendência de melhora ou piora"""
        if len(df) < 20:
            return {'direcao': 'dados_insuficientes'}
        
        # Comparar primeira metade com segunda metade
        meio = len(df) // 2
        primeira_metade = df.iloc[:meio]
        segunda_metade = df.iloc[meio:]
        
        media_primeira = pd.to_numeric(primeira_metade['percent_cam_d'], errors='coerce').mean()
        media_segunda = pd.to_numeric(segunda_metade['percent_cam_d'], errors='coerce').mean()
        
        if pd.isna(media_primeira) or pd.isna(media_segunda):
            return {'direcao': 'indeterminado'}
        
        variacao = ((media_segunda - media_primeira) / media_primeira) * 100
        
        if variacao > 10:
            direcao = 'piorando'
        elif variacao < -10:
            direcao = 'melhorando'
        else:
            direcao = 'estavel'
        
        return {
            'direcao': direcao,
            'variacao': round(variacao, 2)
        }
    
    def _analisar_horarios_criticos(self, df):
        """Analisa horários com mais problemas"""
        if 'data_hora' not in df.columns:
            return []
        
        df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
        df['hora'] = df['data_hora'].dt.hour
        
        # Agrupar por período do dia
        periodos = {
            'Madrugada (00-06h)': (0, 6),
            'Manhã (06-12h)': (6, 12),
            'Tarde (12-18h)': (12, 18),
            'Noite (18-24h)': (18, 24)
        }
        
        resultados = []
        for periodo, (inicio, fim) in periodos.items():
            df_periodo = df[(df['hora'] >= inicio) & (df['hora'] < fim)]
            if len(df_periodo) > 0:
                media_rej = pd.to_numeric(df_periodo['percent_cam_d'], errors='coerce').mean()
                if not pd.isna(media_rej):
                    resultados.append({
                        'periodo': periodo,
                        'media_rejeicao': round(media_rej, 2),
                        'registros': len(df_periodo)
                    })
        
        # Ordenar por média de rejeição
        resultados.sort(key=lambda x: x['media_rejeicao'], reverse=True)
        return resultados
    
    def _calcular_score_qualidade(self, df):
        """Calcula score de qualidade (0-100)"""
        if len(df) == 0:
            return 0
        
        # Fatores que influenciam o score
        media_rej = self._calcular_media_rejeicao(df)
        media_geral = media_rej['media_geral']
        
        # Score baseado em rejeição (quanto menor, melhor)
        # 0% rejeição = 100 pontos
        # 10% rejeição = 0 pontos
        score = max(0, 100 - (media_geral * 10))
        
        return round(score, 2)
    
    def _analisar_tendencia_temporal(self, df):
        """Analisa tendência temporal dos defeitos"""
        if len(df) < 10:
            return 'dados_insuficientes'
        
        # Últimos 5 vs 5 anteriores
        ultimos_5 = df.tail(5)
        anteriores_5 = df.iloc[-10:-5]
        
        defeitos_recentes = []
        defeitos_anteriores = []
        
        for col in ['rej1_defect', 'rej2_defect', 'rej3_defect']:
            if col in df.columns:
                defeitos_recentes.extend(ultimos_5[col].dropna().tolist())
                defeitos_anteriores.extend(anteriores_5[col].dropna().tolist())
        
        if not defeitos_recentes or not defeitos_anteriores:
            return 'indeterminado'
        
        # Comparar diversidade de defeitos
        diversidade_recente = len(set(defeitos_recentes))
        diversidade_anterior = len(set(defeitos_anteriores))
        
        if diversidade_recente > diversidade_anterior:
            return 'aumentando_variedade'
        elif diversidade_recente < diversidade_anterior:
            return 'concentrando_defeitos'
        else:
            return 'estavel'
    
    def _classificar_risco(self, probabilidade):
        """Classifica nível de risco baseado em probabilidade"""
        if probabilidade >= 50:
            return 'CRÍTICO'
        elif probabilidade >= 30:
            return 'ALTO'
        elif probabilidade >= 15:
            return 'MÉDIO'
        else:
            return 'BAIXO'
    
    def _calcular_confianca(self, num_registros):
        """Calcula nível de confiança da predição"""
        if num_registros >= 100:
            return 'ALTA'
        elif num_registros >= 50:
            return 'MÉDIA'
        elif num_registros >= 20:
            return 'BAIXA'
        else:
            return 'MUITO_BAIXA'
    
    def _gerar_recomendacao(self, predicao):
        """Gera recomendação baseada na predição"""
        if not predicao:
            return "Sem recomendações disponíveis"
        
        defeito = predicao.get('defeito', '')
        probabilidade = predicao.get('probabilidade', 0)
        
        recomendacoes_por_defeito = {
            'Amassada': 'Verificar pressão das ferramentas e ajustar se necessário',
            'Apara Retida': 'Limpar sistema de remoção de aparas e verificar sucção',
            'Barra Colada': 'Verificar temperatura e lubrificação do processo',
            'Cápsula Fina': 'Ajustar espessura do material e verificar calibração',
            'Dente': 'Verificar alinhamento das ferramentas de corte',
            'Furo': 'Inspecionar punções e substituir se desgastados',
            'Rachada': 'Verificar velocidade do processo e qualidade do material',
            'Short': 'Ajustar alimentação de material e verificar setup',
            'Suja': 'Aumentar frequência de limpeza e verificar lubrificação'
        }
        
        recomendacao_base = recomendacoes_por_defeito.get(defeito, 'Monitorar processo e investigar causa raiz')
        
        if probabilidade >= 50:
            return f"URGENTE: {recomendacao_base} (Probabilidade: {probabilidade}%)"
        elif probabilidade >= 30:
            return f"ATENÇÃO: {recomendacao_base} (Probabilidade: {probabilidade}%)"
        else:
            return f"PREVENTIVO: {recomendacao_base} (Probabilidade: {probabilidade}%)"


# Instância global
predicao_ia = None

def inicializar_ia(data_manager):
    """Inicializa sistema de IA"""
    global predicao_ia
    predicao_ia = PredicaoInteligente(data_manager)
    return predicao_ia

