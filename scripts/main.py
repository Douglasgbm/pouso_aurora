modulos_espera = [
    {
        "nome": "Habitação", 
        "prioridade": 1, 
        "combustivel": 80, 
        "massa": 15000, 
        "criticidade": 5, 
        "eta": 0, 
        "angulo_entrada": 13.5, 
        "coord_pouso": (101, 99)
    },
    {
        "nome": "Energia", 
        "prioridade": 1, 
        "combustivel": 70, 
        "massa": 10000, 
        "criticidade": 5, 
        "eta": 0.5, 
        "angulo_entrada": 14.0, 
        "coord_pouso": (98, 102)
    },
    {
        "nome": "Suporte Médico", 
        "prioridade": 2, 
        "combustivel": 60, 
        "massa": 5000, 
        "criticidade": 4, 
        "eta": 2, 
        "angulo_entrada": 12.8, 
        "coord_pouso": (105, 105) # Coloquei um erro aqui pra gente testar depois
    },
    {
        "nome": "Logística", 
        "prioridade": 3, 
        "combustivel": 40, 
        "massa": 12000, 
        "criticidade": 3, 
        "eta": 4, 
        "angulo_entrada": 14.2, 
        "coord_pouso": (95, 95)
    },
    {
        "nome": "Laboratório", 
        "prioridade": 4, 
        "combustivel": 90, 
        "massa": 7000, 
        "criticidade": 2, 
        "eta": 6, 
        "angulo_entrada": 15.5, # Ângulo fora da janela (Erro)
        "coord_pouso": (100, 100)
    },
]

# --- CONSTANTES DE SEGURANÇA (Regras de Negócio) ---
ALVO_CENTRAL = (100, 100)
OBSTACULOS = [(105, 105), (90, 110), (100, 95)] # Coordenadas de crateras/pedras
ANGULO_MIN = 12.0
ANGULO_MAX = 15.0
COMBUSTIVEL_MINIMO = 20 # Porcentagem mínima para autorizar descida
apto0 = False
apto1 = False
apto2 = False
apto3 = False
apto4 = False

# --- VALIDAÇÃO DETALHADA DO MÓDULO 0 ---
m0 = modulos_espera[0]

if m0["coord_pouso"] in OBSTACULOS:
    print(f"Módulo {m0['nome']}: BLOQUEADO - Obstáculo no terreno!")
elif m0["angulo_entrada"] < ANGULO_MIN or m0["angulo_entrada"] > ANGULO_MAX:
    print(f"Módulo {m0['nome']}: BLOQUEADO - Ângulo de entrada fora da janela!")
elif m0["combustivel"] < COMBUSTIVEL_MINIMO:
    print(f"Módulo {m0['nome']}: BLOQUEADO - Combustível insuficiente!")
else:
    print(f"Módulo {m0['nome']}: Pouso AUTORIZADO")
    apto0 = True

# --- VALIDAÇÃO DETALHADA DO MÓDULO 1 ---
m1 = modulos_espera[1]
if m1["coord_pouso"] in OBSTACULOS:
    print(f"Módulo {m1['nome']}: BLOQUEADO - Obstáculo no terreno!")
elif m1["angulo_entrada"] < ANGULO_MIN or m1["angulo_entrada"] > ANGULO_MAX:
    print(f"Módulo {m1['nome']}: BLOQUEADO - Ângulo de entrada fora da janela!")
elif m1["combustivel"] < COMBUSTIVEL_MINIMO:
    print(f"Módulo {m1['nome']}: BLOQUEADO - Combustível insuficiente!")
else:
    print(f"Módulo {m1['nome']}: Pouso AUTORIZADO")
    apto1 = True

# --- VALIDAÇÃO DETALHADA DO MÓDULO 2 ---
m2 = modulos_espera[2]
if m2["coord_pouso"] in OBSTACULOS:
    print(f"Módulo {m2['nome']}: BLOQUEADO - Obstáculo no terreno!")
elif m2["angulo_entrada"] < ANGULO_MIN or m2["angulo_entrada"] > ANGULO_MAX:
    print(f"Módulo {m2['nome']}: BLOQUEADO - Ângulo de entrada fora da janela!")
elif m2["combustivel"] < COMBUSTIVEL_MINIMO:
    print(f"Módulo {m2['nome']}: BLOQUEADO - Combustível insuficiente!")
else:
    print(f"Módulo {m2['nome']}: Pouso AUTORIZADO")
    apto2 = True
    
# --- VALIDAÇÃO DETALHADA DO MÓDULO 3 ---
m3 = modulos_espera[3]
if m3["coord_pouso"] in OBSTACULOS:
    print(f"Módulo {m3['nome']}: BLOQUEADO - Obstáculo no terreno!")
elif m3["angulo_entrada"] < ANGULO_MIN or m3["angulo_entrada"] > ANGULO_MAX:
    print(f"Módulo {m3['nome']}: BLOQUEADO - Ângulo de entrada fora da janela!")
elif m3["combustivel"] < COMBUSTIVEL_MINIMO:
    print(f"Módulo {m3['nome']}: BLOQUEADO - Combustível insuficiente!")
else:
    print(f"Módulo {m3['nome']}: Pouso AUTORIZADO")
    apto3 = True

# --- VALIDAÇÃO DETALHADA DO MÓDULO 4 ---
m4 = modulos_espera[4]
if m4["coord_pouso"] in OBSTACULOS:
    print(f"Módulo {m4['nome']}: BLOQUEADO - Obstáculo no terreno!")
elif m4["angulo_entrada"] < ANGULO_MIN or m4["angulo_entrada"] > ANGULO_MAX:
    print(f"Módulo {m4['nome']}: BLOQUEADO - Ângulo de entrada fora da janela!")
elif m4["combustivel"] < COMBUSTIVEL_MINIMO:
    print(f"Módulo {m4['nome']}: BLOQUEADO - Combustível insuficiente!")
else:
    print(f"Módulo {m4['nome']}: Pouso AUTORIZADO")
    apto4 = True

print("\n--- FILA DE POUSO PRIORITÁRIA ---")

# Lógica simples: Se Habitação e Energia estão aptos, Habitação vai primeiro (é a base)
if apto0 and apto1:
    print("1º Pouso: Módulo Habitação (Prioridade Máxima)")
    print("2º Pouso: Módulo Energia")
elif apto0:
    print("1º Pouso: Módulo Habitação")
elif apto1:
    print("1º Pouso: Módulo Energia")
else:
    print("Nenhum módulo de prioridade 1 apto para pouso imediato.")

# Depois a gente checa os outros (Logística, etc)
if apto3:
    print("Próximo na fila: Módulo Logística")
if apto4:
    print("Próximo na fila: Módulo Científico")
if apto2:
    print("Próximo na fila: Módulo Suprimentos")