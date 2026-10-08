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


if __name__ == "__main__":
    unittest.main()
