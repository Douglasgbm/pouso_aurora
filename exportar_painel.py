"""Exporta os cenários do MGPEB para o painel HTML (painel/dados.js).

Extra da interface: não faz parte do código avaliado. O mgpeb.py não muda.
As regras de pouso NÃO são reescritas aqui: o exportador só "escuta" as
funções que o simular() já chama (aplicar_eventos, ativar, autorizar e
ordenar), copia o que entrou e saiu e devolve a mesma resposta. Assim o
painel mostra exatamente o que o simulador decidiu.

Uso: python3 exportar_painel.py
"""
import contextlib
import copy
import io
import json
from pathlib import Path

with contextlib.redirect_stdout(io.StringIO()):
    import mgpeb as g
    from exemplos import casos

SAIDA = Path(__file__).parent / "painel" / "dados.js"

# Trechos fixos que o autorizar() escreve no motivo, um por porta lógica.
PORTAS = [
    ["combustivel", "Combustível insuficiente"],
    ["saude", "Sensores/sistemas falhos;"],
    ["clima", "Atmosfera inaceitável"],
    ["area", "Área "],
]


def foto_modulos(dados, config):
    # Copia o estado de todos os módulos naquele instante.
    fotos = []
    for m in dados:
        fotos.append({
            "id": m[g.ID], "tipo": m[g.TIPO], "prioridade": m[g.PRIORIDADE],
            "combustivel": m[g.COMBUSTIVEL], "massa": m[g.MASSA],
            "carga": m[g.CARGA], "eta": m[g.ETA],
            "sensores": m[g.SENSORES], "sistemas": m[g.SISTEMAS],
            "estado": m[g.ESTADO], "motivo": m[g.MOTIVO],
            "minimo": g.minimo_seguro(m, config),
        })
    return fotos


def rodar_com_escuta(modulos, eventos, ambiente, config):
    """Roda g.simular() registrando cada passo. Devolve [resultado, passos]."""
    passos = []
    atual = {"tempo": 0.0, "hist": 0}
    originais = {
        "aplicar_eventos": g.aplicar_eventos, "ativar": g.ativar,
        "autorizar": g.autorizar, "ordenar": g.ordenar,
    }

    def escuta_eventos(eventos_, aplicados, dados, ambiente_, historico, tempo):
        # Chamada no fim de uma descida: antes de aplicar os eventos, o estado
        # ainda é o do voo (módulo descendo, área reservada). A foto fica logo
        # depois da linha "iniciou descida", com a hora em que a descida começou.
        for m in dados:
            if m[g.ESTADO] == "descendo":
                passos.append({"tipo": "descida", "tempo": atual["tempo"], "hist": len(historico),
                               "id": m[g.ID], "ambiente": list(ambiente_),
                               "modulos": foto_modulos(dados, config)})
        novo = originais["aplicar_eventos"](eventos_, aplicados, dados, ambiente_, historico, tempo)
        # A foto vem depois das linhas dos eventos que acabaram de ser aplicados.
        atual["tempo"] = tempo
        atual["hist"] = len(novo)
        passos.append({"tipo": "foto", "tempo": tempo, "hist": len(novo),
                       "ambiente": list(ambiente_), "modulos": foto_modulos(dados, config)})
        return novo

    def escuta_ativar(dados, historico):
        novo = originais["ativar"](dados, historico)
        atual["hist"] = len(novo)
        passos.append({"tipo": "ativacao", "tempo": atual["tempo"], "hist": len(novo),
                       "modulos": foto_modulos(dados, config)})
        return novo

    def escuta_autorizar(m, ambiente_, config_):
        motivo = originais["autorizar"](m, ambiente_, config_)
        portas = {}
        for nome, trecho in PORTAS:
            portas[nome] = trecho not in motivo
        passos.append({"tipo": "checagem", "tempo": atual["tempo"], "hist": atual["hist"],
                       "id": m[g.ID], "motivo": motivo, "portas": portas,
                       "combustivel": m[g.COMBUSTIVEL],
                       "minimo": g.minimo_seguro(m, config_),
                       "ambiente": list(ambiente_)})
        return motivo

    def escuta_ordenar(aptos, dados, config_):
        antes = [dados[i][g.ID] for i in aptos]
        resposta = originais["ordenar"](aptos, dados, config_)
        depois = [dados[i][g.ID] for i in aptos]
        passos.append({"tipo": "ordenacao", "tempo": atual["tempo"], "hist": atual["hist"],
                       "antes": antes, "depois": depois})
        return resposta

    g.aplicar_eventos = escuta_eventos
    g.ativar = escuta_ativar
    g.autorizar = escuta_autorizar
    g.ordenar = escuta_ordenar
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            resultado = g.simular(modulos, eventos, ambiente, config)
    finally:
        for nome, funcao in originais.items():
            setattr(g, nome, funcao)
    return [resultado, passos]


def linha_do_tempo(resultado, passos):
    """Intercala os passos escutados com as linhas do histórico, em ordem."""
    historico = resultado[2]
    tempo_da_linha = horario_das_linhas(historico, passos)
    saida = []
    proxima = 0
    for p in passos:
        while proxima < p["hist"]:
            saida.append({"tipo": "log", "tempo": tempo_da_linha[proxima],
                          "texto": historico[proxima]})
            proxima += 1
        item = dict(p)
        del item["hist"]
        saida.append(item)
    while proxima < len(historico):
        saida.append({"tipo": "log", "tempo": tempo_da_linha[proxima],
                      "texto": historico[proxima]})
        proxima += 1
    return saida


def horario_das_linhas(historico, passos):
    # Linhas com "N min:" trazem a hora. As de ativação ("E operacional",
    # "E suspenso: ...") não trazem: recebem a hora da última foto antes delas.
    horas = []
    ultimo = 0.0
    marcos = [[p["hist"], p["tempo"]] for p in passos if p["tipo"] == "foto"]
    for i, linha in enumerate(historico):
        if " min: " in linha:
            ultimo = float(linha.split(" min: ")[0])
        else:
            for limite, tempo in marcos:
                if limite <= i:
                    ultimo = tempo
        horas.append(ultimo)
    return horas


def exportar_caso(nome, modulos, eventos, ambiente, config):
    resultado, passos = rodar_com_escuta(modulos, eventos, ambiente, config)
    if len(resultado) == 0:
        return {"nome": nome, "valido": False}
    dados, espera, historico, alertas, pilha, tempo, amb, pousados = resultado
    return {
        "nome": nome,
        "valido": True,
        "entrada": {
            "modulos": foto_modulos(modulos, config),
            "eventos": [{"tempo": e[0], "tipo": e[1], "valor": e[2], "id": e[3]} for e in eventos],
            "ambiente": list(ambiente),
            "config": {"duracao": config[0], "taxa": config[1],
                       "reserva": config[2], "margem": config[3]},
        },
        "linha_do_tempo": linha_do_tempo(resultado, passos),
        "final": {
            "tempo": tempo,
            "ambiente": list(amb),
            "modulos": foto_modulos(dados, config),
            "espera": [dados[i][g.ID] for i in espera],
            "pousados": [dados[i][g.ID] for i in pousados],
            "alertas": list(alertas),
            "historico": list(historico),
        },
    }


def todos_os_casos():
    lista = [["padrao", copy.deepcopy(g.MODULOS), [], [True, "livre"]]]
    return lista + casos()


def main():
    missoes = []
    for nome, modulos, eventos, ambiente in todos_os_casos():
        missoes.append(exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG))
    SAIDA.parent.mkdir(exist_ok=True)
    texto = json.dumps(missoes, ensure_ascii=False, indent=1)
    SAIDA.write_text("// Gerado por exportar_painel.py: não editar à mão.\n"
                     "window.MISSOES = " + texto + ";\n", encoding="utf-8")
    print(f"{len(missoes)} cenários exportados para {SAIDA}")


if __name__ == "__main__":
    main()
