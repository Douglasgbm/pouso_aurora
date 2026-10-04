# MGPEB - Aurora Siger: versão didática, sem cálculo aeroespacial real.
# Listas e índices traduzem os vetores ensinados em C (Cap. 4, p. 36).
# Cada módulo é uma linha com os campos abaixo, sempre na mesma ordem.
ID = 0
TIPO = 1
PRIORIDADE = 2
COMBUSTIVEL = 3  # kg
MASSA = 4       # kg
CARGA = 5       # criticidade: 1 a 5
ETA = 6         # instante de chegada, em minutos desde o início
SENSORES = 7
SISTEMAS = 8
ACIDENTE = 9     # resultado de exemplo, não uma falha aleatória
ESTADO = 10
MOTIVO = 11

TIPOS = ["Energia", "Habitação", "Logística", "Médico", "Laboratório"]
# Configuração hipotética: duração min, taxa kg/(kg*min), reserva kg,
# margem relativa para urgência. Massa constante durante a descida.
CONFIG = [5.0, 0.002, 2.0, 0.25]


def quantidade(lista):
    total = 0
    for elemento in lista:
        total = total + 1
    return total


def retirar(lista, posicao):
    # Reconstrói a lista sem uma posição; não utiliza remove ou pop.
    nova = []
    for i in range(quantidade(lista)):
        if i != posicao:
            nova = nova + [lista[i]]
    return nova


def ultimo_evento(pilha):
    if quantidade(pilha) == 0:
        return "Pilha de consulta vazia"
    return pilha[quantidade(pilha) - 1]


def desfazer_consulta(pilha):
    # Devolve a pilha sem o topo. Nunca modifica pouso ou combustível.
    return retirar(pilha, quantidade(pilha) - 1)


def numero_valido(valor, minimo):
    # Faixa de entrada didática: [mínimo, 1 bilhão), exclui NaN/inf.
    # type() e comparações são demonstrados nos Caps. 3 e 6.
    if type(valor) != int and type(valor) != float:
        return False
    return valor >= minimo and valor < 1000000000


def validar(modulos, eventos, ambiente, config):
    if quantidade(config) != 4 or quantidade(ambiente) != 2:
        return False
    for valor in config:
        if not numero_valido(valor, 0):
            return False
    if config[0] == 0 or config[1] == 0 or config[2] == 0:
        return False
    if type(ambiente[0]) != bool:
        return False
    if ambiente[1] != "livre" and ambiente[1] != "ocupada" and ambiente[1] != "obstruída":
        return False
    for i in range(quantidade(modulos)):
        m = modulos[i]
        if quantidade(m) != 12 or type(m[ID]) != str or m[ID] == "":
            return False
        if m[TIPO] not in TIPOS:
            return False
        for campo in [COMBUSTIVEL, MASSA, ETA]:
            if not numero_valido(m[campo], 0):
                return False
        if m[MASSA] == 0:
            return False
        for campo in [PRIORIDADE, CARGA]:
            if type(m[campo]) != int or m[campo] < 1 or m[campo] > 5:
                return False
        for campo in [SENSORES, SISTEMAS, ACIDENTE]:
            if type(m[campo]) != bool:
                return False
        for j in range(i):
            if modulos[j][ID] == m[ID]:
                return False
    for e in eventos:
        # Evento: [instante min, tipo, valor, ID (para reparação)].
        if quantidade(e) != 4 or not numero_valido(e[0], 0):
            return False
        if e[1] == "area":
            if e[2] != "livre" and e[2] != "ocupada" and e[2] != "obstruída":
                return False
        elif e[1] == "clima" or e[1] == "sensores" or e[1] == "sistemas":
            if type(e[2]) != bool:
                return False
            if e[1] != "clima" and buscar(modulos, ID, e[3]) == -1:
                return False
        else:
            return False
    return True


def buscar(lista, campo, valor):
    # Busca linear por ID ou tipo; -1 significa não encontrado.
    for i in range(quantidade(lista)):
        if lista[i][campo] == valor:
            return i
    return -1


def buscar_extremo(lista, campo, maior):
    # Usar COMBUSTIVEL/False para menor ou PRIORIDADE/True para maior.
    melhor = -1
    for i in range(quantidade(lista)):
        if melhor == -1:
            melhor = i
        elif maior and lista[i][campo] > lista[melhor][campo]:
            melhor = i
        elif not maior and lista[i][campo] < lista[melhor][campo]:
            melhor = i
    return melhor


def minimo_seguro(m, config):
    # Função afim em tempo: taxa * massa * duração + reserva.
    return config[1] * m[MASSA] * config[0] + config[2]


def autorizar(m, ambiente, config):
    # Motivo vazio significa apto. TODOS os critérios são obrigatórios.
    motivo = ""
    if m[COMBUSTIVEL] < minimo_seguro(m, config):
        motivo = motivo + "Combustível insuficiente; "
    if not m[SENSORES] or not m[SISTEMAS]:
        motivo = motivo + "Sensores/sistemas falhos; "
    if not ambiente[0]:
        motivo = motivo + "Atmosfera inaceitável; "
    if ambiente[1] != "livre":
        motivo = motivo + "Área " + ambiente[1] + "; "
    return motivo


def ordem_tipo(tipo):
    for i in range(quantidade(TIPOS)):
        if TIPOS[i] == tipo:
            return i
    return 5


def vem_antes(a, b, config):
    # Chamado somente entre aptos: urgência nunca autoriza insegurança.
    margem_a = (a[COMBUSTIVEL] - minimo_seguro(a, config)) / minimo_seguro(a, config)
    margem_b = (b[COMBUSTIVEL] - minimo_seguro(b, config)) / minimo_seguro(b, config)
    urgente_a = margem_a <= config[3]
    urgente_b = margem_b <= config[3]
    if urgente_a != urgente_b:
        return urgente_a
    if urgente_a:
        if margem_a != margem_b:
            return margem_a < margem_b
        if a[CARGA] != b[CARGA]:
            return a[CARGA] > b[CARGA]
    if a[TIPO] != b[TIPO]:
        return ordem_tipo(a[TIPO]) < ordem_tipo(b[TIPO])
    return a[PRIORIDADE] > b[PRIORIDADE]


def ordenar(aptos, modulos, config):
    # Inserção manual (Cap. 5, p. 29-30). Empates preservam entrada.
    for i in range(1, quantidade(aptos)):
        chave = aptos[i]
        j = i - 1
        while j >= 0 and vem_antes(modulos[chave], modulos[aptos[j]], config):
            aptos[j + 1] = aptos[j]
            j = j - 1
        aptos[j + 1] = chave


def existe_operacional(modulos, tipo):
    for m in modulos:
        if m[TIPO] == tipo and m[ESTADO] == "operacional":
            return True
    return False


def ativar(modulos, historico):
    mudou = True
    while mudou:
        mudou = False
        for m in modulos:
            if m[ESTADO] == "pousado":
                if m[TIPO] == "Energia":
                    pode = True  # Energia da BASE ativa autonomamente.
                elif m[TIPO] == "Laboratório":
                    pode = existe_operacional(modulos, "Energia") and existe_operacional(modulos, "Habitação")
                else:
                    pode = existe_operacional(modulos, "Energia")
                if pode:
                    m[ESTADO] = "operacional"
                    m[MOTIVO] = ""
                    historico = historico + [m[ID] + " operacional"]
                    mudou = True
                else:
                    m[MOTIVO] = "Aguarda Energia operacional"
                    if m[TIPO] == "Laboratório":
                        m[MOTIVO] = "Aguarda Energia e Habitação operacionais"
    return historico


def simular(modulos, eventos, ambiente, config):
    if not validar(modulos, eventos, ambiente, config):
        print("Entrada inválida. Confira campos, unidades, faixas e IDs únicos.")
        return []
    # Cópia manual: repetir exemplos não altera dados de entrada.
    dados = []
    for m in modulos:
        linha = []
        for valor in m:
            linha = linha + [valor]
        linha[ESTADO] = "órbita"
        linha[MOTIVO] = ""
        dados = dados + [linha]
    ambiente = [ambiente[0], ambiente[1]]
    aplicados = []
    for e in eventos:
        aplicados = aplicados + [False]
    tempo = 0.0
    fila = []       # FIFO das chegadas; índices apontam para dados.
    espera = []     # Lista elegível; pode ser priorizada por urgência.
    historico = []
    alertas = []
    continuar = True
    while continuar:
        # Eventos vencidos: processa por instante; empates seguem a entrada.
        while True:
            proximo = -1
            for i in range(quantidade(eventos)):
                if not aplicados[i] and eventos[i][0] <= tempo:
                    if proximo == -1 or eventos[i][0] < eventos[proximo][0]:
                        proximo = i
            if proximo == -1:
                break
            e = eventos[proximo]
            if e[1] == "clima":
                ambiente[0] = e[2]
            elif e[1] == "area":
                ambiente[1] = e[2]
            else:
                pos = buscar(dados, ID, e[3])
                if e[1] == "sensores":
                    dados[pos][SENSORES] = e[2]
                else:
                    dados[pos][SISTEMAS] = e[2]
            aplicados[proximo] = True
            historico = historico + [f"{tempo:.1f} min: evento {e[1]}"]
        # Enfileira chegadas por ETA; no mesmo instante mantém o cadastro.
        while True:
            pos = -1
            for i in range(quantidade(dados)):
                if dados[i][ESTADO] == "órbita" and dados[i][ETA] <= tempo:
                    if pos == -1 or dados[i][ETA] < dados[pos][ETA]:
                        pos = i
            if pos == -1:
                break
            dados[pos][ESTADO] = "espera"
            fila = fila + [pos]
            historico = historico + [f"{tempo:.1f} min: {dados[pos][ID]} chegou"]
        while quantidade(fila) > 0:
            espera = espera + [fila[0]]  # Primeiro a entrar, primeiro a sair.
            fila = retirar(fila, 0)
        historico = ativar(dados, historico)
        aptos = []
        for pos in espera:
            m = dados[pos]
            m[MOTIVO] = autorizar(m, ambiente, config)
            if m[MOTIVO] == "":
                aptos = aptos + [pos]
            else:
                alerta = m[ID] + ": " + m[MOTIVO]
                if alerta not in alertas:
                    alertas = alertas + [alerta]
        if quantidade(aptos) > 0:
            ordenar(aptos, dados, config)
            pos = aptos[0]
            ambiente[1] = "reservada"
            for i in range(quantidade(espera)):
                if espera[i] == pos:
                    espera = retirar(espera, i)
                    break
            m = dados[pos]
            m[ESTADO] = "descendo"
            historico = historico + [f"{tempo:.1f} min: {m[ID]} iniciou descida"]
            # Consumo executado separado da autorização, com mesma lei linear.
            consumo = m[MASSA] * config[1] * config[0]
            m[COMBUSTIVEL] = m[COMBUSTIVEL] - consumo
            tempo = tempo + config[0]
            if m[ACIDENTE]:
                m[ESTADO] = "acidente"
                m[MOTIVO] = "Acidente: área obstruída"
                ambiente[1] = "obstruída"
                alertas = alertas + [m[ID] + ": " + m[MOTIVO]]
            else:
                m[ESTADO] = "pousado"
                ambiente[1] = "livre"  # Transferência hipotética para a base.
            historico = historico + [f"{tempo:.1f} min: {m[ID]} {m[ESTADO]}"]
        else:
            futuro = -1
            for m in dados:
                if m[ESTADO] == "órbita" and (futuro == -1 or m[ETA] < futuro):
                    futuro = m[ETA]
            for i in range(quantidade(eventos)):
                if not aplicados[i] and (futuro == -1 or eventos[i][0] < futuro):
                    futuro = eventos[i][0]
            if futuro == -1:
                continuar = False  # Todos bloqueados e sem eventos: encerra.
            else:
                tempo = futuro  # Esperar em órbita não consome combustível.
    historico = historico + [f"{tempo:.1f} min: rodada encerrada"]
    pilha = []
    for evento in historico:
        pilha = pilha + [evento]  # Empilhar; última entrada é o topo.
    # Resultado: módulos, espera, histórico, alertas, pilha, tempo, ambiente.
    return [dados, espera, historico, alertas, pilha, tempo, ambiente]


def relatorio(resultado):
    if quantidade(resultado) == 0:
        return
    print("Tempo final (min):", resultado[5], "| Área:", resultado[6][1])
    print("Pousados (inclui operacionais):")
    for m in resultado[0]:
        if m[ESTADO] == "pousado" or m[ESTADO] == "operacional":
            print(" ", m[ID], m[TIPO])
    print("Operacionais:")
    for m in resultado[0]:
        if m[ESTADO] == "operacional":
            print(" ", m[ID], m[TIPO])
    print("Aguardando ou com impedimento:")
    for m in resultado[0]:
        if m[ESTADO] != "operacional":
            print(" ", m[ID], m[ESTADO], m[MOTIVO])
    print("Combustível restante (kg):")
    for m in resultado[0]:
        print(" ", m[ID], round(m[COMBUSTIVEL], 2))
    print("Alertas históricos:")
    for alerta in resultado[3]:
        print(" ", alerta)
    print("Eventos:")
    for evento in resultado[2]:
        print(" ", evento)


# Dados iniciais editáveis. Execute este arquivo com: python mgpeb.py
# ID, tipo, prioridade, combustível kg, massa kg, carga, ETA min,
# sensores, sistemas, acidente, estado inicial, motivo inicial.
MODULOS = [
    ["E", "Energia", 1, 30.0, 1000.0, 1, 0.0, True, True, False, "", ""],
    ["H", "Habitação", 1, 30.0, 1000.0, 1, 0.0, True, True, False, "", ""],
    ["G", "Logística", 1, 30.0, 1000.0, 1, 0.0, True, True, False, "", ""],
    ["M", "Médico", 1, 30.0, 1000.0, 1, 0.0, True, True, False, "", ""],
    ["L", "Laboratório", 1, 30.0, 1000.0, 1, 0.0, True, True, False, "", ""],
]
print("Consulta: índice do menor combustível:", buscar_extremo(MODULOS, COMBUSTIVEL, False))
print("Consulta: índice da maior prioridade:", buscar_extremo(MODULOS, PRIORIDADE, True))
print("Consulta: índice do tipo Médico:", buscar(MODULOS, TIPO, "Médico"))
RESULTADO = simular(MODULOS, [], [True, "livre"], CONFIG)
relatorio(RESULTADO)
