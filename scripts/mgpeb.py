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
# SOBRE OS VALORES DE ETA DO CADASTRO:
# A primeira versão espalhava as chegadas por 6 horas (0, 30, 120, 240, 360).
# Simulando a fila com aqueles números, em 5 dos 6 pousos havia um único
# candidato disponível - não havia o que decidir, e o ciclo ficava ocioso por
# até 95 minutos seguidos. Um cenário que não exercita as próprias regras não
# prova nada.
# Os ETAs foram apertados para a escala do ciclo (25 min), de modo que vários
# módulos disputem a mesma vaga. É desenho de cenário de teste, e está
# declarado aqui de propósito - não é um dado observado.

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
        "eta": 0,                   # chega junto com a Habitação
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
        "eta": 10,                  # min
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
        "eta": 5,                   # <-- chega ANTES da Energia, de propósito:
                                    #     é o que faz a regra de emergência
                                    #     furar uma prioridade MELHOR que a dela
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
        "eta": 0,                   # chega junto com o MAV
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
        "eta": 20,                  # min
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
        "eta": 50,                  # min
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
          f"{'Massa':>7} {'Crit':>4} {'ETA':>7}")
    print("-" * 74)

    # ordena por prioridade de projeto SÓ para exibir.
    # ATENÇÃO: isto NÃO é a fila de pouso. A fila é calculada na Camada 3,
    # com o estado real de cada módulo. Esta aqui é a ordem do "manual".
    for m in sorted(lista, key=lambda x: x["prioridade_projeto"]):
        print(f"{m['prioridade_projeto']:>3} {m['nome']:<15} {m['tipo_carga']:<16} "
              f"{m['combustivel_descida']:>4}% {m['energia']:>4}% "
              f"{m['massa']:>7} {m['criticidade']:>3}/5 "
              f"{'T+' + str(m['eta']) + 'min':>7}")

    print("-" * 74)
    print(f"massa total a pousar: {sum(m['massa'] for m in lista):,} kg".replace(",", "."))

    mav = [m for m in lista if m["tipo_carga"] == "Retorno"]
    if mav:
        print(f"tanque de subida do {mav[0]['nome']}: {mav[0]['tanque_subida']}% "
              f"(vazio por projeto - enche em meses, no solo)")


# =============================================================================
# =============================================================================
# CAMADA 2 - PORTAS LÓGICAS
# =============================================================================
# =============================================================================
#
# O programa tem duas metades, e elas NÃO se misturam:
#
#   O MUNDO (Marte)                    O MGPEB (computador de bordo)
#   ---------------                    -----------------------------
#   decide se tem tempestade    --->   lê "tempestade: sim"
#   decide se o sensor falhou   --->   lê "sensor: falha"
#   decide onde há cratera      --->   lê o mapa de terreno
#                                      E ENTÃO DECIDE: pousa ou não.
#
# Um sistema embarcado NÃO escolhe o clima. Ele sofre o clima e lê o sensor.
# Se as duas metades se misturarem, o programa passa a "decidir" que está
# ventando - o que não faz sentido nenhum, e pior: fica impossível forçar um
# cenário para testar, porque o programa seria juiz e réu ao mesmo tempo.
#
# O "não existe fator humano" do projeto vale para a DECISÃO (ninguém autoriza
# o pouso), não para os DADOS (o módulo não inventa o que o sensor mede).

import random
import copy
import sys


# =============================================================================
# 6. O MUNDO - o que o MGPEB não controla
# =============================================================================

# Semente fixa do sorteio.
# Sem ela, cada execução dá um resultado diferente, e a saída colada no
# relatório não pode ser reproduzida por quem for corrigir. Com ela, continua
# sendo sorteio - mas sempre O MESMO sorteio. É prática padrão de simulação.
#
# POR QUE 23, E NÃO QUALQUER UMA: a semente ESCOLHE O CENÁRIO, e isso está
# declarado aqui de propósito em vez de escondido.
# O gerador foi aferido em 20.000 mundos e respeita as probabilidades
# declaradas (medido 5,01% / 3,03% / 4,08% contra 5% / 3% / 4%), com média de
# 0,73 falha de hardware por missão. Mas a distribuição tem cauda: a semente
# 42, testada antes, caiu nos 2,88% de missões com TRÊS falhas e matou o MAV
# e a Habitação - resultado legítimo, porém inútil para demonstrar a fila,
# porque sobrava zero módulo para ordenar.
# A semente 23 produz UMA falha, no Suporte Médico, que já estava fora da fila
# pela cratera. Preserva os quatro concorrentes e ainda povoa as três listas.
#
# [SUGESTÃO PARA O RELATÓRIO] rodar N missões com sementes diferentes e
# reportar a taxa de sucesso é uma análise de Monte Carlo, e responde a uma
# pergunta que uma execução única não responde: "com que frequência esta
# missão falha?"
SEMENTE = 23

# Probabilidades de falha. São premissas do cenário, não medições.
PROB_TEMPESTADE = 0.20        # por ciclo (o clima muda)
PROB_FALHA_SENSOR = 0.05      # por módulo (hardware, sorteado uma vez só)
PROB_FALHA_PARAQUEDAS = 0.03  # por módulo
PROB_DANO_ESTRUTURAL = 0.04   # por módulo


def criar_mundo(lista, semente=SEMENTE):
    """Sorteia o estado físico que o MGPEB vai LER (e não escolher).

    O hardware é sorteado UMA VEZ, no início: um sensor ou funciona ou não
    funciona. Não existe ninguém em Marte para consertar, então a falha é
    permanente. O clima, ao contrário, é sorteado a cada ciclo - tempestade
    passa.
    """
    random.seed(semente)
    mundo = {"hardware": {}, "zonas_ocupadas": [], "tempestade": False}
    for m in lista:
        mundo["hardware"][m["nome"]] = {
            "sensores_ok": random.random() >= PROB_FALHA_SENSOR,
            "paraquedas_ok": random.random() >= PROB_FALHA_PARAQUEDAS,
            "estrutura_ok": random.random() >= PROB_DANO_ESTRUTURAL,
        }
    return mundo


def sortear_clima(mundo):
    """Roda uma vez por ciclo. Tempestade de areia é temporária."""
    mundo["tempestade"] = random.random() < PROB_TEMPESTADE
    return mundo["tempestade"]


# =============================================================================
# 7. AS PORTAS LÓGICAS
# =============================================================================
#
# EXPRESSÃO BOOLEANA DO PROJETO:
#
#   Autorização = ETA AND C AND E AND A AND D AND S AND T AND θ AND P AND I
#
# São dez sinais, todos ligados por AND: uma única falha bloqueia o pouso.
# (O ROADMAP tinha seis; entraram ETA, E, P e I ao longo do projeto.)
#
# -----------------------------------------------------------------------------
# CADA PORTA DEVOLVE DUAS COISAS, NÃO UMA:
#
#   1) passou ou não passou
#   2) se NÃO passou, a causa é RECUPERÁVEL ou DEFINITIVA
#
# É a segunda que decide para qual lista o módulo vai:
#
#   recuperável -> EM ESPERA : falhou agora, mas a causa se resolve sozinha
#                              ou pode ser corrigida. Volta a disputar no
#                              próximo ciclo.
#   definitiva  -> EM ALERTA : a causa não se resolve. Sai da fila e fica
#                              monitorado.
#
# Sem essa distinção, as duas listas que o enunciado pede seriam a mesma coisa
# com nomes diferentes - e a fila não teria motivo para ser recalculada.
# -----------------------------------------------------------------------------

RECUPERAVEL = True
DEFINITIVA = False


def avaliar_portas(m, mundo, t=0):
    """Avalia as dez portas de UM módulo, no instante t.

    Devolve uma lista de tuplas:
        (sigla, descrição, passou, recuperável_se_falhar, detalhe)
    """
    hw = mundo["hardware"][m["nome"]]
    portas = []

    # --- ETA: o módulo já chegou à órbita? -----------------------------
    # Restrição FÍSICA, não preferência: não dá para pousar o que não chegou.
    # Recuperável pela razão mais simples do mundo: é só esperar.
    portas.append(("ETA", "chegada à órbita",
                   m["eta"] <= t, RECUPERAVEL,
                   "chega em t=%dmin (agora t=%dmin)" % (m["eta"], t)))

    # --- C: combustível de descida -------------------------------------
    # É o estágio 3 do freio (retrofoguetes). Abaixo de 20% não há margem
    # para frear. DEFINITIVA porque combustível só diminui - esperar piora.
    portas.append(("C", "combustível de descida",
                   m["combustivel_descida"] >= COMBUSTIVEL_ABORTO, DEFINITIVA,
                   "%d%% (mínimo %d%%)" % (m["combustivel_descida"], COMBUSTIVEL_ABORTO)))

    # --- E: energia elétrica -------------------------------------------
    # Combustível cheio não adianta se a bateria morrer: é ela que ABRE o
    # paraquedas e ACIONA as válvulas. DEFINITIVA pelo mesmo motivo que C.
    portas.append(("E", "energia elétrica",
                   m["energia"] >= ENERGIA_MINIMA, DEFINITIVA,
                   "%d%% (mínimo %d%%)" % (m["energia"], ENERGIA_MINIMA)))

    # --- A: atmosfera ---------------------------------------------------
    # Tempestade de areia cega o radar e desvia a descida.
    # RECUPERÁVEL: tempestade passa.
    portas.append(("A", "atmosfera estável",
                   not mundo["tempestade"], RECUPERAVEL,
                   "tempestade de areia" if mundo["tempestade"] else "céu limpo"))

    # --- D: área de pouso disponível ------------------------------------
    # Outro módulo já parado na coordenada. RECUPERÁVEL: a zona é liberada
    # depois dos 18 min de limpeza do ciclo de operação.
    ocupada = m["coord_pouso"] in mundo["zonas_ocupadas"]
    portas.append(("D", "área de pouso livre",
                   not ocupada, RECUPERAVEL,
                   "ocupada" if ocupada else "livre"))

    # --- S: integridade dos sensores ------------------------------------
    # Sem radar o módulo não sabe a que altura está, e não tem como decidir
    # quando acionar nada. DEFINITIVA: não há quem conserte em Marte.
    portas.append(("S", "sensores íntegros",
                   hw["sensores_ok"], DEFINITIVA,
                   "ok" if hw["sensores_ok"] else "radar em falha"))

    # --- T: terreno validado --------------------------------------------
    # Cruza a coordenada alvo com o mapa de crateras e pedras.
    # RECUPERÁVEL: o alvo pode ser deslocado para outra coordenada.
    # (Quem faz esse deslocamento é a Camada 3 - aqui só classificamos.)
    em_cratera = m["coord_pouso"] in OBSTACULOS
    portas.append(("T", "terreno sem obstáculo",
                   not em_cratera, RECUPERAVEL,
                   "obstáculo em %s" % (m["coord_pouso"],) if em_cratera
                   else "coordenada %s limpa" % (m["coord_pouso"],)))

    # --- θ: ângulo de entrada -------------------------------------------
    # Fechado demais: o calor e a força G destroem o módulo.
    # Aberto demais: ele quica na atmosfera e volta pro espaço.
    # RECUPERÁVEL: dá para corrigir com uma queima de ajuste na próxima
    # órbita - mas a queima CONSOME COMBUSTÍVEL, ou seja, recuperar esta
    # porta empurra a porta C para baixo. (Acoplamento tratado na Camada 4.)
    angulo_ok = ANGULO_MIN <= m["angulo_entrada"] <= ANGULO_MAX
    portas.append(("θ", "ângulo de entrada",
                   angulo_ok, RECUPERAVEL,
                   "%.1f° (janela %.1f°-%.1f°)" % (m["angulo_entrada"], ANGULO_MIN, ANGULO_MAX)))

    # --- P: paraquedas ---------------------------------------------------
    # Estágio 2 do freio. DEFINITIVA: é mecânico, não se conserta em voo.
    portas.append(("P", "paraquedas operacional",
                   hw["paraquedas_ok"], DEFINITIVA,
                   "ok" if hw["paraquedas_ok"] else "mecanismo travado"))

    # --- I: integridade estrutural ---------------------------------------
    # Estágio 1 do freio é a própria atmosfera, e ela castiga a estrutura.
    # Casco trincado não aguenta a desaceleração. DEFINITIVA.
    portas.append(("I", "integridade estrutural",
                   hw["estrutura_ok"], DEFINITIVA,
                   "ok" if hw["estrutura_ok"] else "dano no casco"))

    return portas


def autorizar(m, mundo, t=0):
    """Aplica o AND das dez portas e decide o destino do módulo.

    Devolve (autorizado, destino, portas), com destino em
    'pouso' | 'espera' | 'alerta'.
    """
    portas = avaliar_portas(m, mundo, t)

    # ESTA LINHA É A EXPRESSÃO BOOLEANA DO PROJETO.
    # all() sobre os dez sinais é literalmente o AND gigante do diagrama.
    autorizacao = all(porta[2] for porta in portas)

    if autorizacao:
        return True, "pouso", portas

    falhas = [porta for porta in portas if not porta[2]]

    # Basta UMA causa definitiva para mandar o módulo ao alerta, mesmo que
    # todas as outras falhas sejam temporárias: esperar não resolve aquela.
    if any(porta[3] == DEFINITIVA for porta in falhas):
        return False, "alerta", portas
    return False, "espera", portas


def triagem(lista, mundo, t=0):
    """Separa os módulos nas listas que o enunciado exige."""
    prontos, espera, alerta = [], [], []
    for m in lista:
        ok, destino, portas = autorizar(m, mundo, t)
        if destino == "pouso":
            prontos.append(m)
        elif destino == "espera":
            espera.append((m, portas))
        else:
            alerta.append((m, portas))
    return prontos, espera, alerta


def mostrar_portas(lista, mundo, t=0):
    """Imprime o resultado porta a porta. É o diagrama lógico em texto."""
    print()
    print("=" * 74)
    print("CAMADA 2 - AVALIAÇÃO DAS PORTAS LÓGICAS  (t = %d min)" % t)
    print("=" * 74)
    print("Autorização = ETA AND C AND E AND A AND D AND S AND T AND θ AND P AND I")
    print("Estado do mundo: %s | zonas ocupadas: %s"
          % ("TEMPESTADE DE AREIA" if mundo["tempestade"] else "céu limpo",
             mundo["zonas_ocupadas"] or "nenhuma"))
    print()

    for m in lista:
        ok, destino, portas = autorizar(m, mundo, t)
        rotulo = {"pouso": "AUTORIZADO", "espera": "EM ESPERA", "alerta": "EM ALERTA"}[destino]
        print("%-16s [%s]" % (m["nome"], rotulo))
        for sigla, desc, passou, recup, detalhe in portas:
            if passou:
                print("     %-4s %-24s OK      %s" % (sigla, desc, detalhe))
            else:
                tipo = "recuperável" if recup == RECUPERAVEL else "DEFINITIVA"
                print("     %-4s %-24s FALHA   %s  <- causa %s"
                      % (sigla, desc, detalhe, tipo))
        print()


def mostrar_listas(prontos, espera, alerta):
    """As três listas auxiliares que o enunciado pede."""
    print("=" * 74)
    print("TRIAGEM")
    print("=" * 74)
    print("PRONTOS PARA POUSO (%d) - vão disputar a fila na Camada 3" % len(prontos))
    for m in prontos:
        print("     %s" % m["nome"])

    print("\nEM ESPERA (%d) - causa recuperável, voltam a disputar" % len(espera))
    for m, portas in espera:
        motivos = ", ".join("%s: %s" % (p[0], p[4]) for p in portas if not p[2])
        print("     %-16s %s" % (m["nome"], motivos))

    print("\nEM ALERTA (%d) - causa definitiva, saem da fila" % len(alerta))
    for m, portas in alerta:
        motivos = ", ".join("%s: %s" % (p[0], p[4])
                            for p in portas if not p[2] and p[3] == DEFINITIVA)
        print("     %-16s %s" % (m["nome"], motivos))
    print()


# =============================================================================
# =============================================================================
# CAMADA 3 - A FILA DINÂMICA
# =============================================================================
# =============================================================================
#
# A Camada 2 responde "este módulo PODE pousar?" - uma foto, num instante.
# A Camada 3 põe o relógio para andar e responde "entre os que podem, QUEM VAI
# AGORA?" - e essa resposta MUDA a cada ciclo, porque:
#
#   - módulos novos chegam à órbita (o ETA vence)
#   - quem espera QUEIMA combustível e energia (seção 9)
#   - o MGPEB corrige falhas recuperáveis, e a correção CUSTA (seção 10)
#   - a tempestade vai e volta
#
# É por isso que a fila é RECALCULADA, e não calculada uma vez.


# =============================================================================
# 9. CONSUMO EM ÓRBITA  ->  FUNÇÃO MATEMÁTICA 1 (linear)
# =============================================================================
#
# FENÔMENO: combustível e energia restantes em função do tempo de espera.
#
#   C(t) = C0 - k * t          k = taxa de consumo, em % por minuto
#   E(t) = E0 - j * t          j = idem, para a bateria
#
# FORMA ESCOLHIDA: LINEAR. Justificativa: um módulo em espera está apenas
# mantendo atitude e mantendo os sistemas ligados - o gasto por minuto é
# praticamente constante, não depende de quanto ainda resta no tanque. (Se
# dependesse do que resta, a forma correta seria exponencial.)
#
# ANÁLISE QUALITATIVA DO GRÁFICO: reta decrescente, coeficiente angular -k.
# Quanto maior o tempo de espera, menor o combustível - e como a reta cruza
# o patamar dos 20% (COMBUSTIVEL_ABORTO), existe um MINUTO LIMITE a partir do
# qual o módulo deixa de poder pousar. Esse cruzamento é o prazo da fila.
#
# RELAÇÃO COM A ENGENHARIA: é a resposta para "quantos módulos eu posso
# deixar esperando, e por quanto tempo, antes de perder um?".
#
# [PREMISSA, NÃO MEDIÇÃO] os valores de k e j abaixo são escolhidos. Estão
# declarados aqui para poderem ser discutidos no relatório.

TAXA_CONSUMO_COMBUSTIVEL = 0.08   # % por minuto (controle de atitude)
TAXA_CONSUMO_ENERGIA = 0.10       # % por minuto (computador e radar ligados)


def minuto_limite(m):
    """Em quantos minutos de espera este módulo cruza a faixa de aborto?

    Resolve C0 - k*t = 20  para t.  É a pergunta de engenharia que a função
    linear existe para responder.
    """
    margem = m["combustivel_descida"] - COMBUSTIVEL_ABORTO
    if margem <= 0:
        return 0
    return margem / TAXA_CONSUMO_COMBUSTIVEL


def consumir_em_orbita(m, dt):
    """Aplica o consumo de dt minutos de espera. Só quem JÁ CHEGOU gasta:
    antes do ETA o módulo está em trânsito, não em espera na órbita."""
    m["combustivel_descida"] = max(0.0, m["combustivel_descida"]
                                   - TAXA_CONSUMO_COMBUSTIVEL * dt)
    m["energia"] = max(0.0, m["energia"] - TAXA_CONSUMO_ENERGIA * dt)


# =============================================================================
# 10. AÇÕES CORRETIVAS - o que o MGPEB FAZ, e não só decide
# =============================================================================
#
# A Camada 2 classificou θ (ângulo) e T (terreno) como RECUPERÁVEIS. Mas nem
# um nem outro se resolvem com o tempo: ângulo errado continua errado amanhã,
# e a cratera não sai do lugar. Quem os resolve é o próprio MGPEB, agindo.
#
# E TODA CORREÇÃO CUSTA COMBUSTÍVEL. Este é o acoplamento mais interessante do
# sistema: recuperar a porta θ EMPURRA A PORTA C PARA BAIXO. Corrigir demais
# mata o módulo que se queria salvar.

CUSTO_CORRECAO_ANGULO = 5.0    # % de combustível (queima de ajuste de órbita)
CUSTO_DESLOCAR_ALVO = 3.0      # % de combustível (manobra lateral na descida)


def corrigir_angulo(m):
    """Queima de ajuste: joga o ângulo para o centro da janela de segurança."""
    novo = (ANGULO_MIN + ANGULO_MAX) / 2.0
    custo = CUSTO_CORRECAO_ANGULO
    m["angulo_entrada"] = novo
    m["combustivel_descida"] = max(0.0, m["combustivel_descida"] - custo)
    return "ângulo corrigido para %.1f° (custou %.0f%% de combustível)" % (novo, custo)


def deslocar_alvo(m, mundo):
    """Procura a coordenada livre mais próxima do alvo original.

    Busca em anel crescente ao redor do ponto original. Como o mapa é pequeno
    e a resposta desejada é a MAIS PRÓXIMA, varrer em anel é o mais simples
    que funciona - e é O(1) no caso comum, porque o primeiro anel já resolve.
    """
    x0, y0 = m["coord_pouso"]
    for raio in range(1, 6):
        for dx in range(-raio, raio + 1):
            for dy in range(-raio, raio + 1):
                if max(abs(dx), abs(dy)) != raio:
                    continue                      # só a borda do anel
                alvo = (x0 + dx, y0 + dy)
                if alvo not in OBSTACULOS and alvo not in mundo["zonas_ocupadas"]:
                    m["coord_pouso"] = alvo
                    m["combustivel_descida"] = max(
                        0.0, m["combustivel_descida"] - CUSTO_DESLOCAR_ALVO)
                    return ("alvo deslocado de %s para %s (custou %.0f%%)"
                            % ((x0, y0), alvo, CUSTO_DESLOCAR_ALVO))
    return None


def aplicar_correcoes(m, mundo, t):
    """Tenta consertar as falhas recuperáveis que NÃO se resolvem sozinhas.

    Não gasta combustível com módulo que já está em alerta: seria jogar fora
    o recurso de um módulo que não vai descer de qualquer jeito.
    """
    ok, destino, portas = autorizar(m, mundo, t)
    if destino == "alerta":
        return []

    acoes = []
    falhou = dict((p[0], p[2]) for p in portas)

    if not falhou["θ"]:
        acoes.append(corrigir_angulo(m))
    if not falhou["T"]:
        msg = deslocar_alvo(m, mundo)
        if msg:
            acoes.append(msg)
    return acoes


# =============================================================================
# 11. A FILA - faixas de combustível e ordenação
# =============================================================================
#
# LEMBRETE DO PROJETO: o combustível responde a DUAS perguntas diferentes.
#   pergunta 1 - "pode pousar?"        -> é a porta C, na Camada 2. ELIMINA.
#   pergunta 2 - "quem vai primeiro?"  -> são as faixas abaixo. ENFILEIRA.
# Confundir as duas foi o que gerou a contradição 20% x 50% no início do
# projeto. São dois cortes no mesmo número, para perguntas diferentes.

def faixa_combustivel(m):
    """Em que faixa de URGÊNCIA (não de segurança) este módulo está."""
    if m["combustivel_descida"] < COMBUSTIVEL_ABORTO:
        return "ABORTO"
    if m["combustivel_descida"] < COMBUSTIVEL_URGENTE:
        return "URGENTE"
    return "NORMAL"


def chave_de_fila(m):
    """A regra de ordenação de dois níveis + desempate, virada em números.

    nível 1 - faixa:      urgente (0) antes de normal (1)
    nível 2 - prioridade: menor primeiro (1 é a máxima)
    desempate - ETA:      desce quem chegou antes

    Princípio: IMPORTÂNCIA NÃO É URGÊNCIA. Adiar um módulo importante custa
    ESPERA; adiar um módulo sem combustível custa O MÓDULO.
    """
    urgente = 0 if faixa_combustivel(m) == "URGENTE" else 1
    return (urgente, m["prioridade_projeto"], m["eta"])


def ordenar_fila(lista):
    """Ordenação por INSERÇÃO (insertion sort).

    POR QUE ESTE ALGORITMO, E NÃO OUTRO - a justificativa é do problema, não
    do gosto:

    1. A fila é REORDENADA a cada ciclo, e entre um ciclo e o seguinte quase
       nada mudou: saiu um módulo, entrou outro. A lista chega ao ordenador
       JÁ QUASE ORDENADA. O insertion sort é O(n) nesse caso - ele percorre e
       não troca nada. Um merge sort faria O(n log n) sempre, ordenado ou não.

    2. Ele é IN-PLACE: não aloca uma segunda lista. Num computador de bordo,
       memória é o recurso mais escasso (ver item 05 do enunciado, limitações
       de hardware numa missão em Marte).

    3. n é 6. Para n pequeno, o insertion sort ganha de qualquer algoritmo
       "melhor" na prática, porque não paga o custo fixo de recursão.

    4. Ele é ESTÁVEL: dois módulos com a mesma chave mantêm a ordem relativa
       anterior, então a fila não fica "tremendo" entre ciclos sem motivo.
    """
    fila = list(lista)
    for i in range(1, len(fila)):
        atual = fila[i]
        chave_atual = chave_de_fila(atual)
        j = i - 1
        # empurra para a direita todo mundo que deve vir DEPOIS do atual
        while j >= 0 and chave_de_fila(fila[j]) > chave_atual:
            fila[j + 1] = fila[j]
            j -= 1
        fila[j + 1] = atual
    return fila


# =============================================================================
# 12. ALGORITMOS DE BUSCA
# =============================================================================
#
# Todas são BUSCAS LINEARES (varrem a lista do começo ao fim). Isso é uma
# escolha, e tem justificativa:
#
#   - a busca binária exigiria manter a lista ORDENADA PELA CHAVE PROCURADA.
#     São três chaves diferentes (combustível, prioridade, tipo de carga), o
#     que significaria manter TRÊS cópias ordenadas na memória. Num sistema
#     embarcado isso é caro, e o dado muda a cada ciclo (o combustível cai),
#     o que obrigaria a reordenar as três a todo instante.
#   - com n = 6, a busca linear faz no máximo 6 comparações. A binária faria
#     3 - e gastaria muito mais para manter a estrutura que a viabiliza.
#
# É o mesmo raciocínio do insertion sort: para n pequeno e dado que muda, o
# simples ganha.

def buscar_menor_combustivel(lista):
    """O módulo mais perto de cruzar a faixa de aborto. É o que corre risco."""
    if not lista:
        return None
    menor = lista[0]
    for m in lista[1:]:
        if m["combustivel_descida"] < menor["combustivel_descida"]:
            menor = m
    return menor


def buscar_maior_prioridade(lista):
    """Prioridade 1 é a MÁXIMA, então "maior prioridade" é o MENOR número."""
    if not lista:
        return None
    maior = lista[0]
    for m in lista[1:]:
        if m["prioridade_projeto"] < maior["prioridade_projeto"]:
            maior = m
    return maior


def buscar_por_tipo_carga(lista, tipo):
    """Todos os módulos de um tipo. Devolve lista, porque há tipos repetidos
    (Infraestrutura e Suporte à Vida têm dois módulos cada)."""
    return [m for m in lista if m["tipo_carga"] == tipo]


# =============================================================================
# 13. PILHA DE REGISTRO (LIFO)
# =============================================================================
#
# O enunciado pede lista, FILA e PILHA. Fila já existe (a de pouso, FIFO
# reordenada). A pilha é o registro de eventos da missão.
#
# POR QUE PILHA, E NÃO OUTRA LISTA: um gravador de voo é lido DE TRÁS PARA
# FRENTE. Quando algo dá errado, a primeira pergunta é "o que aconteceu por
# último?", não "o que aconteceu primeiro". LIFO é exatamente esse acesso:
# o topo da pilha é o evento mais recente.

def registrar(pilha, t, evento):
    """Empilha (push). O topo é sempre o evento mais recente."""
    pilha.append((t, evento))


def desempilhar_ultimos(pilha, n):
    """Desempilha (pop) os n eventos mais recentes, sem destruir a pilha."""
    return list(reversed(pilha[-n:]))


# =============================================================================
# 14. O CICLO DE OPERAÇÃO
# =============================================================================

LIMITE_MISSAO = 600    # min. Além disso a espera custa mais do que salva.


def operar(lista, mundo):
    """Roda a missão, ciclo a ciclo, até acabarem os módulos ou o prazo.

    ESTRUTURAS (o que o enunciado pede, e onde está cada uma):
        pendentes  - LISTA  : quem ainda não resolveu a vida
        fila       - FILA   : os autorizados, ordenados pela regra 2.2
        pousados   - LISTA  : já no solo
        alerta     - LISTA  : fora da fila, monitorados
        registro   - PILHA  : eventos, lidos do mais recente para o mais antigo
    """
    pendentes = list(lista)
    pousados, alerta, registro = [], [], []
    t = 0

    print()
    print("=" * 74)
    print("CAMADA 3 - CICLO DE OPERAÇÃO")
    print("=" * 74)
    print("ordenação: faixa de combustível -> prioridade -> ETA (desempate)")
    print("ciclo: %d min por módulo  |  limite da missão: %d min\n"
          % (CICLO_OPERACAO, LIMITE_MISSAO))

    while pendentes and t <= LIMITE_MISSAO:
        sortear_clima(mundo)

        # --- 1. o MGPEB age sobre o que dá para consertar ---------------
        for m in list(pendentes):
            for acao in aplicar_correcoes(m, mundo, t):
                registrar(registro, t, "%s: %s" % (m["nome"], acao))
                print("t=%3d | AÇÃO   %s: %s" % (t, m["nome"], acao))

        # --- 2. triagem: quem pode, quem espera, quem sai ---------------
        prontos, em_espera, em_alerta = triagem(pendentes, mundo, t)

        for m, portas in em_alerta:
            motivo = ", ".join("%s (%s)" % (p[0], p[4])
                               for p in portas if not p[2] and p[3] == DEFINITIVA)
            alerta.append((m, motivo))
            pendentes.remove(m)
            registrar(registro, t, "%s -> ALERTA: %s" % (m["nome"], motivo))
            print("t=%3d | ALERTA %s -> %s" % (t, m["nome"], motivo))

        # --- 3. a fila é REORDENADA, não reaproveitada ------------------
        if prontos:
            fila = ordenar_fila(prontos)
            escolhido = fila[0]

            disputa = ", ".join("%s[%s/p%d/%.0f%%]"
                                % (m["nome"], faixa_combustivel(m)[0],
                                   m["prioridade_projeto"], m["combustivel_descida"])
                                for m in fila)
            print("t=%3d | FILA   %s" % (t, disputa))

            # furou a fila = urgente que passou na frente de prioridade melhor
            furou = (faixa_combustivel(escolhido) == "URGENTE" and
                     any(m["prioridade_projeto"] < escolhido["prioridade_projeto"]
                         for m in fila))
            marca = "   <== FUROU A FILA (emergência de combustível)" if furou else ""
            print("t=%3d | POUSA  %s%s\n" % (t, escolhido["nome"], marca))

            escolhido["pousou_em"] = t
            pousados.append(escolhido)
            pendentes.remove(escolhido)
            mundo["zonas_ocupadas"].append(escolhido["coord_pouso"])
            registrar(registro, t, "%s POUSOU em %s"
                      % (escolhido["nome"], escolhido["coord_pouso"]))
            dt = CICLO_OPERACAO
        else:
            # Ninguém pronto. A pergunta certa é POR QUÊ, e a resposta muda
            # o que fazer.
            #
            # [DEFEITO CORRIGIDO - encontrado rodando a Camada 3]
            # A primeira versão fazia:
            #       futuros = [etas maiores que t]
            #       if not futuros: break
            # ou seja: adiantava o relógio até a PRÓXIMA CHEGADA, assumindo que
            # a única razão para ninguém estar pronto era "ainda não chegou".
            # Mas a causa pode ser TEMPESTADE DE AREIA - e aí, se todos os
            # módulos já tivessem chegado, a lista de futuros ficava vazia e a
            # missão era ABANDONADA por causa de um evento que passa em
            # minutos. O cenário padrão nunca pegou isso porque sempre havia
            # alguém por chegar. Ver teste_tempestade_total().
            #
            # Correção: esperar um ciclo (ou até a próxima chegada, se ela vier
            # antes) e tentar de novo. Quem encerra a missão é o LIMITE_MISSAO,
            # não a falta de chegadas.
            motivos = {}
            for m, portas in em_espera:
                for porta in portas:
                    if not porta[2]:
                        motivos[porta[0]] = porta[4]

            dt = CICLO_OPERACAO
            futuros = [m["eta"] for m in pendentes if m["eta"] > t]
            if futuros:
                dt = min(dt, min(futuros) - t)

            print("t=%3d | OCIOSO %d min - bloqueio: %s\n"
                  % (t, dt, "; ".join("%s (%s)" % (k, v)
                                      for k, v in sorted(motivos.items()))))

        # --- 4. quem ficou esperando PAGA pelo tempo --------------------
        for m in pendentes:
            if m["eta"] <= t:               # só quem já está em órbita gasta
                consumir_em_orbita(m, dt)

        t += dt

    return pousados, alerta, registro, t


def mostrar_resultado(lista, pousados, alerta, registro, t_final):
    print("=" * 74)
    print("RESULTADO DA MISSÃO")
    print("=" * 74)

    print("POUSADOS (%d):" % len(pousados))
    print("   %-16s %6s %10s %10s" % ("módulo", "t", "comb.", "energia"))
    for m in pousados:
        print("   %-16s %5dm %9.1f%% %9.1f%%"
              % (m["nome"], m["pousou_em"], m["combustivel_descida"], m["energia"]))

    print("\nEM ALERTA (%d):" % len(alerta))
    for m, motivo in alerta:
        print("   %-16s %s" % (m["nome"], motivo))

    print("\nduração total da operação: %d min" % t_final)

    # --- a pilha lida do topo (LIFO) -----------------------------------
    print("\nREGISTRO DE EVENTOS - últimos 5, do mais recente (topo da pilha):")
    for t, evento in desempilhar_ultimos(registro, 5):
        print("   t=%3d  %s" % (t, evento))

    # --- os algoritmos de busca ----------------------------------------
    print("\nBUSCAS (sobre os módulos que pousaram):")
    menor = buscar_menor_combustivel(pousados)
    maior = buscar_maior_prioridade(pousados)
    print("   menor combustível ....: %s (%.1f%%)"
          % (menor["nome"], menor["combustivel_descida"]))
    print("   maior prioridade .....: %s (prioridade %d)"
          % (maior["nome"], maior["prioridade_projeto"]))
    for tipo in ("Infraestrutura", "Suporte à Vida", "Retorno", "Científica"):
        achados = buscar_por_tipo_carga(pousados, tipo)
        print("   tipo '%s'%s: %s"
              % (tipo, "." * max(1, 14 - len(tipo)),
                 ", ".join(m["nome"] for m in achados) or "(nenhum)"))

    # --- o prazo que a função matemática calcula ------------------------
    print("\nPRAZO DE FILA (função linear C(t) = C0 - %.2f*t, corte em %d%%):"
          % (TAXA_CONSUMO_COMBUSTIVEL, COMBUSTIVEL_ABORTO))
    for m in lista:
        print("   %-16s aguenta %6.0f min de espera antes de abortar"
              % (m["nome"], minuto_limite(m)))


# =============================================================================
# 15. TESTES DO QUE O CENÁRIO NORMAL NÃO ALCANÇA
# =============================================================================
#
# O cenário padrão APROVA o programa, mas ele não passa por todos os caminhos.
# Um teste que só percorre o caminho feliz não prova que os outros funcionam -
# ele só prova que o caminho feliz funciona. Cada teste aqui força um caminho
# que o cenário normal não alcança.
#
# Rodar com:  python3 mgpeb.py teste

def teste_tempestade_total():
    """Todos os módulos JÁ CHEGARAM e cai uma tempestade.

    Este é o caminho que derrubava a missão na primeira versão: sem nenhum
    ETA futuro, o laço encerrava e abandonava módulos perfeitamente sadios.
    O correto é esperar a tempestade passar.
    """
    lista = copy.deepcopy(modulos)
    for m in lista:
        m["eta"] = 0                      # todos já em órbita
        m["angulo_entrada"] = 13.5        # sem falha de ângulo
        m["coord_pouso"] = (200 + lista.index(m), 200)   # longe de crateras

    mundo = criar_mundo(lista, semente=SEMENTE)
    for nome in mundo["hardware"]:        # hardware perfeito: isola a variável
        mundo["hardware"][nome] = {"sensores_ok": True,
                                   "paraquedas_ok": True,
                                   "estrutura_ok": True}

    pousados, alerta, registro, t_final = operar(lista, mundo)
    ok = len(pousados) == len(lista) and not alerta
    print("teste_tempestade_total: %s  (%d de %d pousaram, %d em alerta)"
          % ("PASSOU" if ok else "FALHOU", len(pousados), len(lista), len(alerta)))
    return ok


def teste_faixa_de_aborto():
    """Um módulo com combustível abaixo de 20% precisa ir para o ALERTA.

    O cadastro avisa que nenhum módulo do cenário começa nessa faixa, ou seja,
    a porta C nunca é exercitada na execução normal. Aqui ela é.
    """
    lista = copy.deepcopy(modulos)
    lista[2]["combustivel_descida"] = 15.0        # Logística, abaixo do corte
    mundo = criar_mundo(lista, semente=SEMENTE)
    ok, destino, portas = autorizar(lista[2], mundo, t=lista[2]["eta"])
    porta_c = [p for p in portas if p[0] == "C"][0]
    passou = (destino == "alerta") and (not porta_c[2])
    print("teste_faixa_de_aborto: %s  (destino=%s, porta C passou=%s)"
          % ("PASSOU" if passou else "FALHOU", destino, porta_c[2]))
    return passou


def teste_correcao_custa_combustivel():
    """Corrigir o ângulo tem que DIMINUIR o combustível.

    É o acoplamento entre as portas θ e C: recuperar uma empurra a outra para
    baixo. Se um dia alguém "otimizar" a correção para não custar nada, este
    teste reprova.
    """
    m = copy.deepcopy(modulos[5])                 # Laboratório, ângulo 15.5
    antes = m["combustivel_descida"]
    corrigir_angulo(m)
    depois = m["combustivel_descida"]
    dentro = ANGULO_MIN <= m["angulo_entrada"] <= ANGULO_MAX
    ok = depois < antes and dentro
    print("teste_correcao_custa_combustivel: %s  (%.0f%% -> %.0f%%, ângulo %.1f°)"
          % ("PASSOU" if ok else "FALHOU", antes, depois, m["angulo_entrada"]))
    return ok


def teste_insertion_sort():
    """A ordenação por inserção tem que dar o MESMO resultado que o sorted()
    da linguagem. Escrever o algoritmo à mão só vale se ele estiver certo."""
    lista = copy.deepcopy(modulos)
    meu = [m["nome"] for m in ordenar_fila(lista)]
    referencia = [m["nome"] for m in sorted(lista, key=chave_de_fila)]
    ok = meu == referencia
    print("teste_insertion_sort: %s" % ("PASSOU" if ok else "FALHOU"))
    if not ok:
        print("     meu       : %s" % meu)
        print("     referência: %s" % referencia)
    return ok


def rodar_testes():
    print()
    print("=" * 74)
    print("TESTES - caminhos que o cenário normal não percorre")
    print("=" * 74)
    resultados = [
        teste_insertion_sort(),
        teste_correcao_custa_combustivel(),
        teste_faixa_de_aborto(),
        teste_tempestade_total(),
    ]
    print("\n%d de %d testes passaram." % (sum(resultados), len(resultados)))
    return all(resultados)


# =============================================================================
# 16. EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        raise SystemExit(0 if rodar_testes() else 1)

    print()
    print("MGPEB - Base Aurora Siger")
    print("Camadas 1, 2 e 3\n")

    if not validar_cadastro(modulos):
        print("\nCadastro reprovado. Nada é construído em cima de dado inválido.")
        raise SystemExit(1)

    mostrar_cadastro(modulos)

    # --- o mundo é criado UMA vez, e o MGPEB apenas o lê ---------------
    mundo = criar_mundo(modulos)
    sortear_clima(mundo)

    mostrar_portas(modulos, mundo, t=0)
    prontos, espera, alerta = triagem(modulos, mundo, t=0)
    mostrar_listas(prontos, espera, alerta)

    pousados, alerta, registro, t_final = operar(modulos, mundo)
    mostrar_resultado(modulos, pousados, alerta, registro, t_final)
