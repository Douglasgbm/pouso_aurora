# Cenários de estudo separados do código principal.
import mgpeb as g


def montar(id, tipo, fuel=30.0, massa=1000.0, carga=1, eta=0.0,
           sensores=True, sistemas=True, acidente=False, prioridade=1):
    return [id, tipo, prioridade, fuel, massa, carga, eta,
            sensores, sistemas, acidente, "", ""]


def casos():
    normal = [montar("E", "Energia"), montar("H", "Habitação"),
              montar("G", "Logística"), montar("M", "Médico"),
              montar("L", "Laboratório")]
    # Cada caso: nome, módulos, eventos, ambiente [clima aceitável, área].
    return [
        ["normal", normal, [], [True, "livre"]],
        ["urgente", [montar("E", "Energia"), montar("M", "Médico", fuel=13.0)], [], [True, "livre"]],
        ["insuficiente", [montar("E", "Energia", fuel=11.0)], [], [True, "livre"]],
        ["sensores", [montar("E", "Energia", sensores=False)], [], [True, "livre"]],
        ["clima", normal, [], [False, "livre"]],
        ["area", normal, [], [True, "ocupada"]],
        ["duas_urgencias", [montar("E", "Energia", fuel=13.0),
                            montar("M", "Médico", fuel=13.0, carga=5)], [], [True, "livre"]],
        ["chegada_futura", [montar("E", "Energia", eta=20.0)], [], [True, "livre"]],
        ["ativacao_dependente", [montar("L", "Laboratório", fuel=12.0),
             montar("H", "Habitação", eta=20.0), montar("E", "Energia", eta=20.0)], [], [True, "livre"]],
        ["evento_clima", normal, [[10.0, "clima", True, ""]], [False, "livre"]],
        ["acidente", [montar("E", "Energia", acidente=True),
                      montar("H", "Habitação")], [], [True, "livre"]],
    ]


if __name__ == "__main__":
    # Importar mgpeb já exibe a rodada padrão; abaixo ficam os 11 cenários.
    for caso in casos():
        print("\n===", caso[0], "===")
        g.relatorio(g.simular(caso[1], caso[2], caso[3], g.CONFIG))
