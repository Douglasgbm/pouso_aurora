"""Transmite uma rodada do MGPEB no terminal, como telemetria ao vivo.

Uso:
    python ao_vivo.py                 (rodada padrão)
    python ao_vivo.py urgente         (um cenário de exemplos.py)
    python ao_vivo.py urgente 2       (velocidade 2x; 0 = sem esperas)
    python ao_vivo.py --lista         (lista os cenários)

Extra de apresentação: não faz parte do código avaliado e não muda o
mgpeb.py. A linha do tempo vem do mesmo exportador do painel, que escuta o
simulador enquanto ele roda; o atraso na tela é proporcional ao tempo
simulado. No fim, a transmissão é conferida contra o histórico do simulador.
"""
import contextlib
import copy
import io
import os
import sys
import time

with contextlib.redirect_stdout(io.StringIO()):
    import mgpeb as g
    import exportar_painel as ex

SEG_POR_MIN = 0.5     # 1 minuto simulado = 0,5 s na velocidade 1
ESPERA_MAX = 2.0      # espera longa em órbita, sem voo, é encurtada
PAUSA = {"log": 0.35, "checagem": 0.45, "ordenacao": 0.7}
LARGURA_BARRA = 20

COR = {"verde": "32", "vermelho": "31", "ambar": "33", "ciano": "36", "fraco": "2"}
ROTULOS = [
    ["chegou", "CHEGADA", "ciano"],
    ["iniciou descida", "DESCIDA", "ciano"],
    ["pousado", "POUSO", "verde"],
    ["acidente", "ACIDENTE", "vermelho"],
    ["suspenso", "BASE", "ambar"],      # antes de "operacional": "suspenso: Aguarda Energia operacional"
    ["operacional", "BASE", "verde"],
    ["evento", "EVENTO", "ambar"],
    ["rodada encerrada", "FIM", "fraco"],
]


def pintar(texto, cor, cores):
    if not cores:
        return texto
    return "\x1b[" + COR[cor] + "m" + texto + "\x1b[0m"


def rotulo_do_log(texto):
    for trecho, rotulo, cor in ROTULOS:
        if trecho in texto:
            return rotulo, cor
    return "LOG", "fraco"


def linha(tempo, rotulo, texto, cor, cores):
    return pintar(f"T+{tempo:5.1f} │ {rotulo:<9} │ ", "fraco", cores) + pintar(texto, cor, cores)


def marca(ok, cores):
    return pintar("✓", "verde", cores) if ok else pintar("✗", "vermelho", cores)


def texto_checagem(p, cores):
    v = p["valores"]
    letras = " ".join(nome + marca(v[nome], cores) for nome in ["C", "S", "E", "A", "D"])
    if p["motivo"] == "":
        decisao = pintar("LIBERADO", "verde", cores)
    else:
        decisao = pintar("BLOQUEADO: " + p["motivo"].rstrip("; "), "vermelho", cores)
    sinal = "≥" if v["C"] else "<"
    return f"{p['id']}  {letras} → {decisao}  ({p['combustivel']:.1f} {sinal} {p['minimo']:.1f} kg)"


POR_QUE = {
    "urgencia": "só {a} é urgente",
    "margem": "urgentes, {a} tem margem menor",
    "criticidade": "mesma margem, {a} tem carga mais crítica",
    "tipo": "ordem por tipo",
    "prioridade": "mesmo tipo, {a} tem maior prioridade",
    "empate": "empate, mantém a chegada",
}


def texto_ordenacao(p):
    antes = ",".join(str(i) for i in p["indices_antes"])
    depois = ",".join(str(i) for i in p["indices_depois"])
    texto = f"aptos [{antes}] → [{depois}]"
    if p["comparacoes"]:
        c = p["comparacoes"][0]
        texto += f" · {c['a']} antes de {c['b']}: " + POR_QUE[c["criterio"]].format(a=c["a"])
    return texto


def esperar(segundos, velocidade):
    if velocidade > 0 and segundos > 0:
        time.sleep(segundos / velocidade)


def animar_descida(inicio, fim, velocidade, cores, saida):
    # Barra que avança junto com o relógio simulado da descida.
    duracao = (fim - inicio) * SEG_POR_MIN / velocidade
    passos = LARGURA_BARRA
    for k in range(1, passos + 1):
        tempo = inicio + (fim - inicio) * k / passos
        barra = "█" * k + "░" * (passos - k)
        saida.write("\r" + pintar(f"        │ {'':<9} │ ", "fraco", cores) +
                    pintar(f"[{barra}] T+{tempo:5.1f}", "ciano", cores))
        saida.flush()
        time.sleep(duracao / passos)
    saida.write("\r" + " " * 60 + "\r")


def transmitir(missao, velocidade=1.0, cores=False, saida=None):
    """Mostra a linha do tempo exportada. Devolve [linhas do histórico, relógios]."""
    saida = saida or sys.stdout
    ao_vivo = velocidade > 0 and saida.isatty() if hasattr(saida, "isatty") else False
    linhas, relogios = [], []
    tempo_ant, descendo = 0.0, False
    escrever = lambda texto: (saida.write(texto + "\n"), saida.flush())
    for p in missao["linha_do_tempo"]:
        if p["tempo"] > tempo_ant:
            if descendo and ao_vivo:
                animar_descida(tempo_ant, p["tempo"], velocidade, cores, saida)
            else:
                lacuna = (p["tempo"] - tempo_ant) * SEG_POR_MIN
                esperar(lacuna if descendo else min(lacuna, ESPERA_MAX), velocidade)
            tempo_ant = p["tempo"]
        if p["tipo"] == "descida":
            descendo = True
        elif p["tipo"] == "foto":
            descendo = descendo and any(m["estado"] == "descendo" for m in p["modulos"])
        elif p["tipo"] == "log":
            rotulo, cor = rotulo_do_log(p["texto"])
            escrever(linha(p["tempo"], rotulo, p["texto"], cor, cores))
            linhas.append(p["texto"])
            relogios.append(p["tempo"])
            esperar(PAUSA["log"], velocidade)
        elif p["tipo"] == "checagem":
            escrever(linha(p["tempo"], "CHECAGEM", texto_checagem(p, cores), "fraco", cores))
            relogios.append(p["tempo"])
            esperar(PAUSA["checagem"], velocidade)
        elif p["tipo"] == "ordenacao":
            escrever(linha(p["tempo"], "ORDENAÇÃO", texto_ordenacao(p), "ciano", cores))
            relogios.append(p["tempo"])
            esperar(PAUSA["ordenacao"], velocidade)
    # Coerência: o que foi transmitido é o histórico que o simulador gravou.
    oficial = missao["final"]["historico"]
    if linhas == oficial:
        escrever(pintar(f"✓ transmissão conferida: {len(linhas)} eventos idênticos ao histórico do simulador", "verde", cores))
    else:
        escrever(pintar("✗ transmissão DIVERGE do histórico do simulador", "vermelho", cores))
    return [linhas, relogios]


def caso_por_nome(nome):
    for caso in ex.todos_os_casos():
        if caso[0] == nome:
            return caso
    return None


def main(argumentos):
    if argumentos and argumentos[0] == "--lista":
        for caso in ex.todos_os_casos():
            print(caso[0])
        return 0
    nome = argumentos[0] if argumentos else "padrao"
    velocidade = float(argumentos[1]) if len(argumentos) > 1 else 1.0
    caso = caso_por_nome(nome)
    if caso is None:
        print("Cenário desconhecido:", nome, "(use --lista)")
        return 2
    # Sem terminal interativo (saída redirecionada), não há o que animar.
    if not sys.stdout.isatty():
        velocidade = 0
    cores = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
    if cores and os.name == "nt":
        os.system("")  # liga as cores ANSI no console do Windows
    nome, modulos, eventos, ambiente = caso
    print(f"MGPEB ao vivo · cenário {nome} · velocidade {velocidade:g}x")
    print()
    missao = ex.exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG)
    linhas, _ = transmitir(missao, velocidade, cores)
    # O relatório oficial do simulador, igual ao que mgpeb.py imprime.
    print()
    print("Relatório do simulador (mgpeb.relatorio):")
    g.relatorio(g.simular(copy.deepcopy(modulos), copy.deepcopy(eventos), list(ambiente), g.CONFIG))
    return 0 if linhas == missao["final"]["historico"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
