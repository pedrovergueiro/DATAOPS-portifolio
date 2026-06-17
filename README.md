# Sistema de Gestão de Produção — ACG Capsules

Durante meu estágio em Melhoria Contínua na ACG Capsules, uma multinacional do setor farmacêutico, percebi que o controle de produção era feito em planilhas e anotações manuais. Erros aconteciam, rastreabilidade era difícil e os gestores precisavam perguntar pros operadores pra saber o que estava acontecendo no chão de fábrica.

Desenvolvi esse sistema pra mudar isso.

## O que o sistema faz

- **Controle de produção por lote** — registro de cada lote de cápsulas com quantidade, turno, operador responsável e status
- **Rastreio completo de lotes** — histórico de ponta a ponta desde o início até o fim da produção
- **Relatórios de turno** — gerados automaticamente ao encerrar o turno, sem depender de ninguém preencher nada
- **Dashboard pra gestores** — painel visual pra gerente e coordenador de produção acompanharem os indicadores em tempo real, sem precisar interromper os operadores

## O que foi mais desafiador

Nunca tinha trabalhado num ambiente industrial. Antes de escrever uma linha de código, passei tempo entendendo o processo de fabricação, os turnos, a linguagem do setor. O sistema precisava ser simples o suficiente pra operadores de chão de fábrica usarem sem treinamento intensivo — e isso foi o ponto mais difícil de acertar.

A parte técnica de compilar tudo num executável standalone (sem precisar instalar Python na máquina do cliente) também me deu trabalho.

## Stack
Python · tkinter · PyInstaller

## Período
Estágio em Melhoria Contínua — ACG Capsules (out/2025 – mar/2026)
