# -*- coding: utf-8 -*-
"""
MGPEB - Módulo de Gerenciamento de Pouso e Estabilização de Base
Base Aurora Siger | Missão Marte | Atividade Integradora - Fase 2

=============================================================================
CAMADA 1 - CADASTRO DOS MÓDULOS
=============================================================================

O que esta camada FAZ:
    - guarda os dados planejados de cada módulo (o que foi decidido na Terra)
    - PROVA que esses dados são coerentes, antes de qualquer coisa ser
      construída em cima deles

O que esta camada NÃO FAZ:
    - não autoriza pouso        -> Camada 2 (portas lógicas)
    - não monta fila            -> Camada 3 (ordenação dinâmica)
    - não simula a descida      -> Camada 4 (funções matemáticas)
    - não trata o pós-pouso     -> Camada 5 (estabilização)

Por que separar assim: se o cadastro estiver errado, todas as camadas de
cima vão decidir CERTO em cima de dado ERRADO - e o erro só aparece no
final, onde é caro de achar. Base sólida primeiro.
"""


# =============================================================================
# 1. CONVENÇÃO DE UNIDADES
# =============================================================================
# DECISÃO: todo tempo neste programa é em MINUTOS.
#
# Motivo: o ROADMAP usa duas escalas diferentes - o ETA em horas (T+4) e o
# ciclo de operação em minutos (25 min). Misturar as duas é bug garantido:
# em algum ponto alguém soma 4 com 25 e o programa não reclama.
# Escolhemos minutos porque é a MENOR unidade em uso (a descida dura 7 min),
# e converter para baixo nunca perde informação.
#
# Conversão aplicada no cadastro:  T+0h = 0 | T+0.5h = 30 | T+2h = 120
#                                  T+4h = 240 | T+6h = 360

MINUTOS_POR_HORA = 60


# =============================================================================
# 2. CONSTANTES DE SEGURANÇA (as regras de negócio da missão)
# =============================================================================

# --- Faixas de combustível de descida (ROADMAP secão 2.1) -------------------
# Abaixo de ABORTO não há margem para os retrofoguetes frearem a descida.
# Entre ABORTO e URGENTE dá para pousar, mas o módulo não aguenta mais uma
# volta de órbita - por isso ele fura a fila.
COMBUSTIVEL_ABORTO = 20    # %  -> abaixo disso NÃO é autorizado
COMBUSTIVEL_URGENTE = 50   # %  -> entre 20 e 50 é autorizado, mas fura a fila

# --- Energia elétrica -------------------------------------------------------
# ATENÇÃO: combustível e energia são coisas DIFERENTES.
#   combustível = freia e move (queima, acaba)
#   energia     = faz o módulo pensar e agir (computador, radar, o mecanismo
#                 que ABRE o paraquedas, as válvulas dos retrofoguetes)
# Se a bateria morrer no meio da descida, nada é acionado - mesmo com o
# tanque cheio. Por isso energia também é porta lógica de pouso.
#
# [A JUSTIFICAR NO RELATÓRIO] o valor 30% ainda é escolhido a dedo. A Camada 4
# vai calcular o consumo real dos 7 minutos de descida, e aí este número passa
# a ser DERIVADO em vez de chutado.
ENERGIA_MINIMA = 30        # %

# --- Janela de ângulo de entrada na atmosfera (ROADMAP seção 2) -------------
# Fechado demais: freia rápido demais, o calor e a força G destroem o módulo.
# Aberto demais: ele quica na atmosfera e volta pro espaço.
ANGULO_MIN = 12.0          # graus
ANGULO_MAX = 15.0          # graus

# --- Zona de pouso (ROADMAP seção 4) ----------------------------------------
ALVO_CENTRAL = (100, 100)
OBSTACULOS = [(105, 105), (90, 110), (100, 95)]   # crateras e pedras

# --- Tempos de operação (ROADMAP seção 3) -----------------------------------
DURACAO_DESCIDA = 7        # min - os "sete minutos de terror"
CICLO_OPERACAO = 25        # min - 7 de descida + 18 de limpeza da zona
# NÃO CONFUNDIR: a descida dura 7 min, mas o próximo módulo só pode COMEÇAR
# a dele depois de 25 min.


# =============================================================================
# 3. O CADASTRO
# =============================================================================
# Aqui só entra o que é PLANEJADO - o que foi decidido na Terra, antes de sair.
#
# O que NÃO está aqui, e por quê:
#   clima, falha de sensor, paraquedas travado, estrutura trincada...
#   Esses sinais não são atributos do módulo: eles são o ESTADO DO MUNDO no
#   instante da decisão. Um sistema embarcado não "tem" um clima - ele LÊ um
#   sensor. Quem produz esses valores é o mundo (Camada 2), não o cadastro.
#
# Campos:
#   prioridade_projeto -> a ordem PLANEJADA, por dependência (1 = primeiro).
#                         É um ingrediente da fila, NÃO é a fila.
#   criticidade        -> o que a missão perde se este módulo for DESTRUÍDO.
#                         Responde a outra pergunta, e por isso é outra coluna.
#   tipo_carga         -> usado pelos algoritmos de busca (o enunciado pede
#                         busca "por determinado tipo de carga").
#   eta                -> minuto em que o módulo entra na janela de pouso.
#   tanque_subida      -> SÓ o MAV tem. É o propelente de RETORNO, fabricado
#                         do CO2 marciano já no solo, ao longo de meses.
#                         NÃO entra na autorização de pouso.

modulos = [
    {
        "nome": "MAV",
        "descricao": "Veículo de Subida - fabrica o próprio propelente do CO2 marciano",
        "tipo_carga": "Retorno",
        "prioridade_projeto": 1,
        "criticidade": 4,           # <-- DECISÃO EM ABERTO (ver conversa)
        "combustivel_descida": 75,
        "energia": 90,
        "massa": 18000,
        "eta": 0,                   # T+0h
        "angulo_entrada": 13.0,
        "coord_pouso": (103, 97),
        "tanque_subida": 0,         # pousa VAZIO por projeto - não é defeito
    },
    {
        "nome": "Energia",
        "descricao": "Geração e distribuição elétrica da base",
        "tipo_carga": "Infraestrutura",
        "prioridade_projeto": 2,
        "criticidade": 5,
        "combustivel_descida": 70,
        "energia": 85,
        "massa": 10000,
        "eta": 30,                  # T+0.5h
        "angulo_entrada": 14.0,
        "coord_pouso": (98, 102),
        "tanque_subida": None,
    },
    {
        "nome": "Logística",
        "descricao": "Ferramentas, peças e suprimentos",
        "tipo_carga": "Infraestrutura",
        "prioridade_projeto": 3,
        "criticidade": 3,
        "combustivel_descida": 40,  # <-- de propósito: testa a faixa URGENTE
        "energia": 70,
        "massa": 12000,
        "eta": 240,                 # T+4h
        "angulo_entrada": 14.2,
        "coord_pouso": (95, 95),
        "tanque_subida": None,
    },
    {
        "nome": "Habitação",
        "descricao": "Habitat pressurizado e suporte à vida",
        "tipo_carga": "Suporte à Vida",
        "prioridade_projeto": 4,
        "criticidade": 5,
        "combustivel_descida": 80,
        "energia": 95,
        "massa": 15000,
        "eta": 0,                   # T+0h
        "angulo_entrada": 13.5,
        "coord_pouso": (101, 99),
        "tanque_subida": None,
    },
    {
        "nome": "Suporte Médico",
        "descricao": "Enfermaria e equipamento de diagnóstico",
        "tipo_carga": "Suporte à Vida",
        "prioridade_projeto": 5,
        "criticidade": 4,
        "combustivel_descida": 60,
        "energia": 80,
        "massa": 5000,
        "eta": 120,                 # T+2h
        "angulo_entrada": 12.8,
        "coord_pouso": (105, 105),  # <-- de propósito: cai em cima de cratera
        "tanque_subida": None,
    },
    {
        "nome": "Laboratório",
        "descricao": "Análise de amostras e experimentos científicos",
        "tipo_carga": "Científica",
        "prioridade_projeto": 6,
        "criticidade": 2,
        "combustivel_descida": 90,
        "energia": 60,
        "massa": 7000,
        "eta": 360,                 # T+6h
        "angulo_entrada": 15.5,     # <-- de propósito: fora da janela (>15.0)
        "coord_pouso": (100, 100),
        "tanque_subida": None,
    },
]


# =============================================================================
# 4. VALIDAÇÃO DO CADASTRO
# =============================================================================
# Antes de construir qualquer andar em cima, provar que a base está de pé.
# Cada teste abaixo existe por um motivo concreto, anotado no comentário.

def validar_cadastro(lista):
    """Confere se o cadastro é coerente. Devolve True se passou em tudo."""
    erros = []
    avisos = []

    nomes = []
    prioridades = []

    for m in lista:
        nome = m["nome"]

        # -- nome duplicado esconde módulo: dois "Energia" e um some da fila --
        if nome in nomes:
            erros.append(f"nome repetido: {nome}")
        nomes.append(nome)

        # -- prioridade duplicada torna a ordem ambígua ----------------------
        if m["prioridade_projeto"] in prioridades:
            erros.append(f"{nome}: prioridade {m['prioridade_projeto']} repetida")
        prioridades.append(m["prioridade_projeto"])

        # -- percentual fora de 0..100 quebra as faixas de combustível -------
        for campo in ("combustivel_descida", "energia"):
            if not 0 <= m[campo] <= 100:
                erros.append(f"{nome}: {campo} = {m[campo]} (fora de 0..100)")

        # -- criticidade fora de 1..5 invalida a escala do relatório ---------
        if not 1 <= m["criticidade"] <= 5:
            erros.append(f"{nome}: criticidade {m['criticidade']} fora de 1..5")

        # -- massa e ETA negativos não existem fisicamente -------------------
        if m["massa"] <= 0:
            erros.append(f"{nome}: massa {m['massa']} inválida")
        if m["eta"] < 0:
            erros.append(f"{nome}: eta {m['eta']} negativo")

        # -- coordenada precisa ser um par (x, y) ---------------------------
        if not isinstance(m["coord_pouso"], tuple) or len(m["coord_pouso"]) != 2:
            erros.append(f"{nome}: coord_pouso inválida")

        # -- só o MAV carrega tanque de subida ------------------------------
        if m["tipo_carga"] == "Retorno" and m["tanque_subida"] is None:
            erros.append(f"{nome}: é módulo de Retorno e não tem tanque_subida")
        if m["tipo_carga"] != "Retorno" and m["tanque_subida"] is not None:
            erros.append(f"{nome}: não é de Retorno e tem tanque_subida")

    # -- prioridades precisam formar a sequência 1..N sem buraco ------------
    esperado = list(range(1, len(lista) + 1))
    if sorted(prioridades) != esperado:
        erros.append(f"prioridades {sorted(prioridades)} deveriam ser {esperado}")

    # ------------------------------------------------------------------
    # TESTE ESPECIAL: prioridade e criticidade são colunas independentes?
    #
    # Na 1a versão da tabela, prioridade + criticidade dava 6 em TODAS as
    # linhas. Isso quer dizer que eram o MESMO ranking em escalas invertidas,
    # e uma das duas não acrescentava informação nenhuma ao algoritmo.
    # Este teste existe para o erro não voltar sem ninguém perceber.
    # ------------------------------------------------------------------
    somas = [m["prioridade_projeto"] + m["criticidade"] for m in lista]
    if len(set(somas)) == 1:
        erros.append(
            f"prioridade e criticidade são redundantes: soma {somas[0]} em todas "
            f"as linhas (uma é cópia da outra em escala invertida)"
        )

    # -- avisos: não impedem a execução, mas o relatório precisa saber ------
    if not any(m["combustivel_descida"] < COMBUSTIVEL_ABORTO for m in lista):
        avisos.append(
            "nenhum módulo começa na faixa de ABORTO (<20%) - essa porta lógica "
            "ainda não é exercitada pelo cenário"
        )
    if not any(m["energia"] < ENERGIA_MINIMA for m in lista):
        avisos.append(
            "nenhum módulo começa abaixo da energia mínima (<30%) - essa porta "
            "lógica ainda não é exercitada pelo cenário"
        )

    # -- relatório da validação --------------------------------------------
    print("=" * 74)
    print("VALIDAÇÃO DO CADASTRO")
    print("=" * 74)
    print(f"módulos cadastrados......: {len(lista)}")
    print(f"somas prioridade+critic..: {somas}  ({len(set(somas))} valores distintos)")

    for a in avisos:
        print(f"  [aviso] {a}")

    if erros:
        for e in erros:
            print(f"  [ERRO]  {e}")
        print(f"\nRESULTADO: REPROVADO ({len(erros)} erro(s))")
        return False

    print("\nRESULTADO: APROVADO - o cadastro está coerente.")
    return True


# =============================================================================
# 5. EXIBIÇÃO
# =============================================================================

def mostrar_cadastro(lista):
    """Imprime o cadastro em tabela, na ordem de prioridade de projeto."""
    print()
    print("=" * 74)
    print("CADASTRO DOS MÓDULOS  (ordem = prioridade de projeto)")
    print("=" * 74)
    print(f"{'Pri':>3} {'Módulo':<15} {'Tipo':<16} {'Comb':>5} {'Ener':>5} "
          f"{'Massa':>7} {'Crit':>4} {'ETA':>6}")
    print("-" * 74)

    # ordena por prioridade de projeto SÓ para exibir.
    # ATENÇÃO: isto NÃO é a fila de pouso. A fila é calculada na Camada 3,
    # com o estado real de cada módulo. Esta aqui é a ordem do "manual".
    for m in sorted(lista, key=lambda x: x["prioridade_projeto"]):
        eta_h = m["eta"] / MINUTOS_POR_HORA
        print(f"{m['prioridade_projeto']:>3} {m['nome']:<15} {m['tipo_carga']:<16} "
              f"{m['combustivel_descida']:>4}% {m['energia']:>4}% "
              f"{m['massa']:>7} {m['criticidade']:>3}/5 "
              f"{'T+' + str(eta_h) + 'h':>6}")

    print("-" * 74)
    print(f"massa total a pousar: {sum(m['massa'] for m in lista):,} kg".replace(",", "."))

    mav = [m for m in lista if m["tipo_carga"] == "Retorno"]
    if mav:
        print(f"tanque de subida do {mav[0]['nome']}: {mav[0]['tanque_subida']}% "
              f"(vazio por projeto - enche em meses, no solo)")


# =============================================================================
# 6. EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    print()
    print("MGPEB - Base Aurora Siger")
    print("Camada 1: cadastro\n")

    if validar_cadastro(modulos):
        mostrar_cadastro(modulos)
        print("\nBase sólida. Pronto para a Camada 2 (portas lógicas).")
    else:
        print("\nCadastro reprovado. Nada é construído em cima de dado inválido.")
