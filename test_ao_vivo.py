"""Critérios da transmissão ao vivo no terminal (ao_vivo.py)."""
import contextlib
import copy
import io
import unittest
from pathlib import Path

with contextlib.redirect_stdout(io.StringIO()):
    import mgpeb as g
    import exportar_painel as ex
    import ao_vivo


class TestAoVivo(unittest.TestCase):
    def transmitir(self, caso):
        nome, modulos, eventos, ambiente = caso
        saida = io.StringIO()
        missao = ex.exportar_caso(nome, modulos, eventos, ambiente, g.CONFIG)
        linhas, relogios = ao_vivo.transmitir(missao, velocidade=0, cores=False, saida=saida)
        return linhas, relogios, saida.getvalue()

    def test_1_transmite_exatamente_o_historico(self):
        for caso in ex.todos_os_casos():
            with self.subTest(nome=caso[0]):
                linhas, _, _ = self.transmitir(caso)
                puro = g.simular(copy.deepcopy(caso[1]), copy.deepcopy(caso[2]),
                                 list(caso[3]), g.CONFIG)
                self.assertEqual(linhas, puro[2])

    def test_2_relogio_nunca_volta(self):
        for caso in ex.todos_os_casos():
            with self.subTest(nome=caso[0]):
                _, relogios, _ = self.transmitir(caso)
                self.assertEqual(relogios, sorted(relogios))
                self.assertGreater(len(relogios), 0)

    def test_3_sem_cores_quando_pedido(self):
        _, _, texto = self.transmitir(ex.todos_os_casos()[0])
        self.assertNotIn("\x1b[", texto)
        self.assertIn("CHECAGEM", texto)
        self.assertIn("conferida", texto)

    def test_4_todos_os_cenarios_reproduzem_exemplos_saida(self):
        # Ao vivo, os 14 relatórios têm de ser a mesma saída de exemplos.py.
        saida = io.StringIO()
        historicos_ok, relatorios = ao_vivo.transmitir_todos(velocidade=0, cores=False, saida=saida)
        self.assertTrue(historicos_ok)
        with open(Path(__file__).parent / "exemplos_saida.txt", encoding="utf-8") as arquivo:
            self.assertEqual(relatorios, arquivo.read())
        self.assertEqual(saida.getvalue().count("transmissão conferida"), 14)


if __name__ == "__main__":
    unittest.main()
