"""Critérios de aceite do exportador do painel (andar 0 da interface)."""
import contextlib
import copy
import io
import unittest

with contextlib.redirect_stdout(io.StringIO()):
    import mgpeb as g
    import exportar_painel as ex


def rodar_puro(modulos, eventos, ambiente):
    with contextlib.redirect_stdout(io.StringIO()):
        return g.simular(copy.deepcopy(modulos), copy.deepcopy(eventos),
                         list(ambiente), g.CONFIG)


class TestExportarPainel(unittest.TestCase):
    def setUp(self):
        self.casos = ex.todos_os_casos()

    def test_1_escuta_nao_altera_o_resultado(self):
        for nome, modulos, eventos, ambiente in self.casos:
            with self.subTest(nome=nome):
                puro = rodar_puro(modulos, eventos, ambiente)
                escutado, passos = ex.rodar_com_escuta(copy.deepcopy(modulos),
                                                       copy.deepcopy(eventos),
                                                       list(ambiente), g.CONFIG)
                self.assertEqual(escutado, puro)
                self.assertGreater(len(passos), 0)

    def test_1b_funcoes_originais_restauradas(self):
        antes = [g.aplicar_eventos, g.ativar, g.autorizar, g.ordenar]
        ex.exportar_caso(*self.casos[0], g.CONFIG)
        self.assertEqual([g.aplicar_eventos, g.ativar, g.autorizar, g.ordenar], antes)

    def test_2_historico_completo_e_na_ordem(self):
        for nome, modulos, eventos, ambiente in self.casos:
            with self.subTest(nome=nome):
                missao = ex.exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG)
                logs = [p["texto"] for p in missao["linha_do_tempo"] if p["tipo"] == "log"]
                self.assertEqual(logs, rodar_puro(modulos, eventos, ambiente)[2])

    def test_2b_horario_nunca_volta(self):
        for nome, modulos, eventos, ambiente in self.casos:
            with self.subTest(nome=nome):
                missao = ex.exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG)
                horas = [p["tempo"] for p in missao["linha_do_tempo"]]
                self.assertEqual(horas, sorted(horas))

    def test_3_estado_final_bate(self):
        for nome, modulos, eventos, ambiente in self.casos:
            with self.subTest(nome=nome):
                puro = rodar_puro(modulos, eventos, ambiente)
                final = ex.exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG)["final"]
                self.assertEqual(final["tempo"], puro[5])
                self.assertEqual(final["ambiente"], puro[6])
                self.assertEqual(final["alertas"], puro[3])
                for exportado, m in zip(final["modulos"], puro[0]):
                    self.assertEqual(exportado["id"], m[g.ID])
                    self.assertEqual(exportado["estado"], m[g.ESTADO])
                    self.assertEqual(exportado["motivo"], m[g.MOTIVO])
                    self.assertEqual(exportado["combustivel"], m[g.COMBUSTIVEL])
                self.assertEqual(final["pousados"], [puro[0][i][g.ID] for i in puro[7]])
                self.assertEqual(final["espera"], [puro[0][i][g.ID] for i in puro[1]])

    def test_4_checagem_traz_o_motivo_do_autorizar(self):
        # Cada porta apagada precisa ter o seu texto no motivo devolvido.
        vistos = set()
        for nome, modulos, eventos, ambiente in self.casos:
            missao = ex.exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG)
            for p in missao["linha_do_tempo"]:
                if p["tipo"] != "checagem":
                    continue
                self.assertEqual(p["motivo"] == "", all(p["portas"].values()))
                for porta, trecho in ex.PORTAS:
                    if not p["portas"][porta]:
                        vistos.add(porta)
                        self.assertIn(trecho, p["motivo"])
        # Os cenários exercitam as quatro portas fechadas pelo menos uma vez.
        self.assertEqual(vistos, {"combustivel", "saude", "clima", "area"})

    def test_4b_descida_vem_depois_da_ordenacao(self):
        missao = ex.exportar_caso(*[c for c in self.casos if c[0] == "urgente"][0], g.CONFIG)
        tipos = [p["tipo"] if p["tipo"] != "log" else p["texto"] for p in missao["linha_do_tempo"]]
        i = tipos.index("ordenacao")
        self.assertEqual(tipos[i + 1], "0.0 min: M iniciou descida")
        ordem = [p for p in missao["linha_do_tempo"] if p["tipo"] == "ordenacao"][0]
        self.assertEqual(ordem["depois"], ["M", "E"])

    def test_6_foto_durante_a_descida(self):
        # Cada descida tem uma foto do estado durante o voo, logo após o início.
        total = 0
        for nome, modulos, eventos, ambiente in self.casos:
            with self.subTest(nome=nome):
                passos = ex.exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG)["linha_do_tempo"]
                inicios = [i for i, p in enumerate(passos)
                           if p["tipo"] == "log" and p["texto"].endswith("iniciou descida")]
                descidas = [i for i, p in enumerate(passos) if p["tipo"] == "descida"]
                self.assertEqual([i + 1 for i in inicios], descidas)
                for i in descidas:
                    p = passos[i]
                    quem = passos[i - 1]["texto"].split(" min: ")[1].split()[0]
                    self.assertEqual(p["id"], quem)
                    self.assertEqual(p["tempo"], passos[i - 1]["tempo"])
                    self.assertEqual(p["ambiente"][1], "reservada")
                    self.assertEqual([m["id"] for m in p["modulos"] if m["estado"] == "descendo"], [quem])
                    total += 1
        self.assertGreater(total, 20)


    def test_7_criterio_da_ordem_concorda_com_vem_antes(self):
        # O "porquê" exibido no painel não pode divergir da regra do simulador.
        from itertools import permutations
        from exemplos import montar
        casos = list(self.casos)
        mods = [montar("E", "Energia"), montar("H", "Habitação"),
                montar("G", "Logística"), montar("M", "Médico", fuel=13.0, carga=5),
                montar("L", "Laboratório", fuel=14.0, prioridade=3)]
        for i, ordem in enumerate(permutations(mods)):
            casos.append(["perm%d" % i, [list(m) for m in ordem], [], [True, "livre"]])
        vistos = set()
        for nome, modulos, eventos, ambiente in casos:
            missao = ex.exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG)
            for p in missao["linha_do_tempo"]:
                if p["tipo"] != "ordenacao":
                    continue
                linhas = {a["id"]: a for a in p["aptos"]}
                self.assertEqual([a["id"] for a in p["aptos"]], p["depois"])
                def linha(id_):
                    # Cadastro do módulo com o combustível do instante da ordenação.
                    m = list([m for m in modulos if m[g.ID] == id_][0])
                    m[g.COMBUSTIVEL] = linhas[id_]["combustivel"]
                    return m
                for par in p["comparacoes"]:
                    la, lb = linha(par["a"]), linha(par["b"])
                    vistos.add(par["criterio"])
                    self.assertFalse(g.vem_antes(lb, la, g.CONFIG), (nome, par))
                    if par["criterio"] == "empate":
                        self.assertFalse(g.vem_antes(la, lb, g.CONFIG), (nome, par))
                    else:
                        self.assertTrue(g.vem_antes(la, lb, g.CONFIG), (nome, par))
        self.assertTrue({"urgencia", "tipo"} <= vistos, vistos)

    def test_7b_justificativa_exata_de_cada_criterio(self):
        # Casos isolados: a ordem correta não basta; o motivo também deve ser.
        from exemplos import montar
        pares = [
            ("urgencia", montar("A", "Médico", fuel=13), montar("B", "Energia", fuel=30)),
            ("margem", montar("A", "Médico", fuel=13), montar("B", "Energia", fuel=14)),
            ("criticidade", montar("A", "Médico", fuel=13, carga=5), montar("B", "Energia", fuel=13, carga=1)),
            ("tipo", montar("A", "Energia", fuel=30), montar("B", "Médico", fuel=30)),
            ("prioridade", montar("A", "Médico", fuel=30, prioridade=5), montar("B", "Médico", fuel=30, prioridade=1)),
            ("empate", montar("A", "Médico", fuel=30), montar("B", "Médico", fuel=30)),
        ]
        for criterio, a, b in pares:
            with self.subTest(criterio=criterio):
                missao = ex.exportar_caso(criterio, [a, b], [], [True, "livre"], g.CONFIG)
                ordem = next(p for p in missao["linha_do_tempo"] if p["tipo"] == "ordenacao")
                self.assertEqual(ordem["comparacoes"], [{"a": "A", "b": "B", "criterio": criterio}])
                self.assertEqual(ordem["indices_depois"], [0, 1])
                for item, m in zip(ordem["aptos"], [a, b]):
                    esperado = (m[g.COMBUSTIVEL] - 12.0) / 12.0
                    self.assertAlmostEqual(item["margem"], esperado)
                    self.assertEqual(item["urgente"], esperado <= .25)

    def test_8_expressao_booleana_da_checagem(self):
        # C AND (S AND E) AND A AND D tem de dar o mesmo que o autorizar devolveu.
        for nome, modulos, eventos, ambiente in self.casos:
            passos = ex.exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG)["linha_do_tempo"]
            for p in passos:
                if p["tipo"] != "checagem":
                    continue
                v = p["valores"]
                self.assertEqual(v["S"] and v["E"], p["portas"]["saude"])
                expr = v["C"] and v["S"] and v["E"] and v["A"] and v["D"]
                self.assertEqual(expr, p["motivo"] == "", (nome, p))


if __name__ == "__main__":
    unittest.main()
