# RASCUNHO ANTERIOR: experimento de descida física, não usado pelo MGPEB atual.
# Seus parâmetros são didáticos e não representam uma trajetória validada.
# Para estudar fila, autorização e dependências, execute mgpeb.py.

# --- ESTADOS DO MÓDULO ---
energia = 100               # Energia inicial (%)
integridade = 100           # Integridade física inicial (%)
sistemas_online = True      # Sistemas gerais operacionais
sensores_online = True      # Sensores operacionais
coleta_temperatura = True   # Telemetria de temperatura ativa

# --- SISTEMA DE PROPULSÃO (RETROFOGUETES) ---
consumo_por_segundo = 15.0   # Quanto combustível o motor gasta por segundo ativo (kg/s)
empuxo_foguete = 12000.0     # Força dos motores em Newtons (precisa ser maior que o Peso para frear)
propulsor_ativo = False      # Controle se o jogador/sistema ligou os retrofoguetes


# --- FÍSICA E AMBIENTE ---
G = 3.71                    # Gravidade de Marte (m/s²)
DENSIDADE_ATM_MARTE = 0.016 # Densidade atmosférica média (kg/m³)

# --- DINÂMICA DE VOO (Valores Iniciais) ---
altura = 1000.0             # Altura inicial (m)
velocidade = 37.0           # Velocidade vertical inicial (m/s) - caindo
velocidade_kmh = velocidade * 3.6

# --- CONTROLE DE POUSO ---
altura_abertura = 500.0     # Altura alvo para abrir paraquedas (m)
paraquedas_aberto = False   # Estado do paraquedas
area_paraquedas = 50.0      # Área do paraquedas (m²) para cálculo de arrasto
coeficiente_arrasto = 0.4   # Começa baixo (módulo), aumenta com paraquedas
velocidade_terminal = 5.0   # Velocidade segura para o toque no solo (m/s)

# --- TEMPO E SIMULAÇÃO ---
tempo = 0.0                 # Cronômetro da simulação (s)
intervalo = 0.1             # Passo de tempo (s) - 0.1s deixa a simulação mais suave que 1.0s

# --- DINÂMICA DE POUSO ---
desaceleracao = 2.0          # Desaceleração proporcionada pelo paraquedas (m/s²)

# --- AMBIENTE DE MARTE ---
TEMPERATURA_MEDIA_MARTE = -63.0  # Temperatura média na superfície (°C)
temperatura_externa = -50.0      # Temperatura atual medida pelo sensor (°C)

# --- SISTEMA TÉRMICO ---
temperatura_interna = 20.0       # Temperatura interna inicial (°C)
limite_temperatura_interna = 50.0 # Temperatura máxima suportada pelos circuitos (°C)


altura_ligar_retro = 450.0
velocidade_ligar_retro = 8.0
velocidade_desligar_retro = 5.0
coeficiente_arrasto_paraquedas = 1.5  # valor de exemplo, a justificar no trabalho



from collections import deque

# =====================================================================
# DEFINIÇÃO DOS MÓDULOS (Com Angulação e Local de Pouso)
# =====================================================================

modulo_energia = {
    "nome": "Módulo de Energia",
    "prioridade_pouso": 1,
    "massa_modulo": 1200,           
    "combustivel": 450.0,           
    "criticidade_carga": "Máxima",  
    "horario_orbita": "14:15:00",
    "angulo_entrada": -12.5,        # Ângulo de entrada na atmosfera (graus)
    "local_alvo": "Chryse Planitia",# Coordenadas geográficas seguras
    "coordenadas": "22.4° N, 49.9° W"
}

modulo_habitacao = {
    "nome": "Módulo de Habitação",
    "prioridade_pouso": 2,
    "massa_modulo": 1500,           
    "combustivel": 400.0,
    "criticidade_carga": "Alta",
    "horario_orbita": "14:20:00",
    "angulo_entrada": -12.1,
    "local_alvo": "Chryse Planitia",# Pousa perto do módulo de energia
    "coordenadas": "22.5° N, 49.8° W"
}

modulo_logistica = {
    "nome": "Módulo de Logística",
    "prioridade_pouso": 3,
    "massa_modulo": 1000,           
    "combustivel": 350.0,
    "criticidade_carga": "Alta",
    "horario_orbita": "14:35:00",
    "angulo_entrada": -11.8,
    "local_alvo": "Isidis Planitia",
    "coordenadas": "12.9° N, 88.5° E"
}

modulo_medico = {
    "nome": "Módulo de Suporte Médico",
    "prioridade_pouso": 3,          
    "massa_modulo": 950,
    "combustivel": 380.0,
    "criticidade_carga": "Média",   
    "horario_orbita": "14:40:00",
    "angulo_entrada": -12.0,
    "local_alvo": "Isidis Planitia",# Pousa junto com a logística
    "coordenadas": "12.8° N, 88.6° E"
}

modulo_laboratorio = {
    "nome": "Laboratório Científico",
    "prioridade_pouso": 4,          
    "massa_modulo": 1100,
    "combustivel": 350.0,
    "criticidade_carga": "Regular", 
    "horario_orbita": "14:55:00",
    "angulo_entrada": -13.0,        # Ângulo ligeiramente mais íngreme
    "local_alvo": "Jezero Crater",  # Terreno científico acidentado
    "coordenadas": "18.38° N, 77.58° E"
}

# =====================================================================
# ORGANIZAÇÃO NAS ESTRUTURAS DE DADOS LINEARES
# =====================================================================

# Fila (Queue) Principal para autorização de pouso (FIFO: First-In, First-Out)
# Já inseridos respeitando a ordem lógica de prioridade de pouso
fila_autorizacao_pouso = deque([
    modulo_energia, 
    modulo_habitacao, 
    modulo_logistica, 
    modulo_medico, 
    modulo_laboratorio
])

# Listas Auxiliares para o controle de tráfego aéreo marciano
modulos_pousados = []  # Armazenará os módulos após o sucesso da simulação de descida
modulos_em_espera = [] # Módulos aguardando liberação da pista ou órbita segura
modulos_em_alerta = [] # Módulos com problemas (ex: pouco combustível ou superaquecimento)
massa_modulo = modulo_energia["massa_modulo"]
combustivel = modulo_energia["combustivel"]

# =====================================================================
# SIMULAÇÃO DE DESCIDA E POUSO
# =====================================================================
while altura > 0:
    # Abre o paraquedas ao atingir a altitude definida.
    if not paraquedas_aberto and altura <= altura_abertura and sensores_online:
        paraquedas_aberto = True
        print(f"Paraquedas aberto a {altura:.1f} m")

    # Liga e desliga o retrofoguete usando limites diferentes.
    if (
        not propulsor_ativo
        and altura <= altura_ligar_retro
        and velocidade > velocidade_ligar_retro
        and combustivel > 0
        and sistemas_online
        and sensores_online
    ):
        propulsor_ativo = True
        print(f"Retrofoguete ligado a {altura:.1f} m")
    elif propulsor_ativo and (
        velocidade <= velocidade_desligar_retro or combustivel <= 0
    ):
        propulsor_ativo = False
        print(f"Retrofoguete desligado a {altura:.1f} m")

    # Calcula o arrasto do paraquedas.
    forca_arrasto = 0.0
    if paraquedas_aberto:
        forca_arrasto = (
            0.5
            * DENSIDADE_ATM_MARTE
            * coeficiente_arrasto_paraquedas
            * area_paraquedas
            * velocidade**2
        )

    # Calcula o consumo e o empuxo médio neste intervalo.
    tempo_motor = 0.0
    if propulsor_ativo and combustivel > 0:
        tempo_motor = min(intervalo, combustivel / consumo_por_segundo)

    empuxo_medio = empuxo_foguete * (tempo_motor / intervalo)
    combustivel = max(
        0.0,
        combustivel - consumo_por_segundo * tempo_motor
    )

    # Velocidade positiva aponta para baixo; arrasto e empuxo freiam a descida.
    aceleracao = G - (forca_arrasto + empuxo_medio) / massa_modulo
    velocidade_anterior = velocidade
    velocidade_nova = max(0.0, velocidade + aceleracao * intervalo)

    # Atualiza a altura usando a velocidade média do intervalo.
    distancia = (velocidade_anterior + velocidade_nova) / 2 * intervalo

    if distancia >= altura:
        # Ajusta o último passo para terminar exatamente no solo.
        fracao = altura / distancia
        velocidade = velocidade_anterior + (
            velocidade_nova - velocidade_anterior
        ) * fracao
        tempo += intervalo * fracao
        altura = 0.0
    else:
        altura -= distancia
        velocidade = velocidade_nova
        tempo += intervalo

print(f"Tempo de descida: {tempo:.1f} s")
print(f"Combustível restante: {combustivel:.1f} kg")
print(f"Velocidade no toque: {velocidade:.1f} m/s")
print(f"Velocidade no toque: {velocidade * 3.6:.1f} km/h")