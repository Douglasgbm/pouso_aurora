"""Validação externa: unittest/AST não fazem parte do código do aluno."""
import ast
from itertools import product, permutations
import contextlib
import copy
import io
from pathlib import Path
import unittest

with contextlib.redirect_stdout(io.StringIO()):
    import mgpeb as g
    from exemplos import casos, montar


class TestMGPEB(unittest.TestCase):
    def rodar(self, nome):
        for caso in casos():
            if caso[0] == nome:
                return g.simular(caso[1], caso[2], caso[3], g.CONFIG)
        self.fail("Caso inexistente")

    def inicios(self, resultado):
        return [e.split(" min: ")[1].split()[0] for e in resultado[2] if "iniciou descida" in e]

    def test_normal(self):
        s = self.rodar("normal")
        self.assertEqual(self.inicios(s), ["E", "H", "G", "M", "L"])
        self.assertTrue(all(m[g.ESTADO] == "operacional" for m in s[0]))
        self.assertEqual(s[5], 25.0)
        self.assertEqual(s[7], [0, 1, 2, 3, 4])
        self.assertTrue(all(m[g.COMBUSTIVEL] == 20.0 for m in s[0]))

    def test_impedimentos_obrigatorios(self):
        for nome in ["insuficiente", "sensores", "clima", "area"]:
            with self.subTest(nome=nome):
                s = self.rodar(nome)
                self.assertEqual(self.inicios(s), [])
                self.assertEqual(len(s[1]), len(s[0]))
                self.assertEqual(s[5], 0.0)
                self.assertEqual(s[7], [])
                self.assertTrue(all(m[g.MOTIVO] for m in s[0]))
        m = montar("X", "Médico", fuel=1.0, sensores=False, sistemas=False)
        motivo = g.autorizar(m, [False, "ocupada"], g.CONFIG)
        for termo in ["Combustível", "Sensores", "Atmosfera", "Área"]:
            self.assertIn(termo, motivo)
        s = g.simular([m, montar("E", "Energia")], [], [True, "livre"], g.CONFIG)
        self.assertEqual(self.inicios(s), ["E"])
        self.assertEqual(s[0][0][g.COMBUSTIVEL], 1.0)

    def test_urgencia_comparavel_e_desempates(self):
        self.assertEqual(self.inicios(self.rodar("urgente")), ["M", "E"])
        self.assertEqual(self.inicios(self.rodar("duas_urgencias")), ["M", "E"])
        a = montar("A", "Energia", fuel=13.0)
        b = montar("B", "Médico", fuel=26.0, massa=2200.0)
        self.assertTrue(g.vem_antes(a, b, g.CONFIG))  # margem relativa igual; tipo desempata
        b[g.CARGA] = 5
        self.assertTrue(g.vem_antes(b, a, g.CONFIG))
        c = montar("C", "Energia", fuel=13.0)
        ordem = [1, 0]
        g.ordenar(ordem, [a, c], g.CONFIG)
        self.assertEqual(ordem, [1, 0])  # empate completo conserva entrada
        c[g.PRIORIDADE] = 5
        ordem = [0, 1]
        g.ordenar(ordem, [a, c], g.CONFIG)
        self.assertEqual(ordem, [1, 0])

    def test_eta_e_ponto_fixo(self):
        s = self.rodar("chegada_futura")
        self.assertEqual(s[5], 25.0)
        self.assertEqual(s[0][0][g.COMBUSTIVEL], 20.0)
        s = self.rodar("ativacao_dependente")
        self.assertEqual(self.inicios(s), ["L", "E", "H"])
        self.assertTrue(all(m[g.ESTADO] == "operacional" for m in s[0]))
        self.assertLess(s[2].index("E operacional"), s[2].index("L operacional"))
        s = g.simular([montar("M", "Médico", fuel=12.0)], [], [True, "livre"], g.CONFIG)
        self.assertEqual(s[0][0][g.ESTADO], "pousado")
        self.assertEqual(s[0][0][g.COMBUSTIVEL], 2.0)
        self.assertIn("Aguarda Energia", s[0][0][g.MOTIVO])
        # Lista invertida: Laboratório só ativa após outra passagem.
        dados = [montar("L", "Laboratório"), montar("H", "Habitação"), montar("E", "Energia")]
        for m in dados:
            m[g.ESTADO] = "pousado"
        g.ativar(dados, [])
        self.assertTrue(all(m[g.ESTADO] == "operacional" for m in dados))

    def test_eventos_e_acidente(self):
        self.assertEqual(self.rodar("evento_clima")[5], 35.0)
        s = self.rodar("acidente")
        self.assertEqual(s[6][1], "obstruída")
        self.assertEqual(s[0][1][g.ESTADO], "espera")
        s = g.simular([montar("E", "Energia", sensores=False)],
                      [[3.0, "sensores", True, "E"]], [True, "livre"], g.CONFIG)
        self.assertEqual(s[0][0][g.ESTADO], "operacional")
        self.assertEqual(s[5], 8.0)
        s = g.simular([montar("E", "Energia", acidente=True), montar("H", "Habitação")],
                      [[10.0, "area", "livre", ""]], [True, "livre"], g.CONFIG)
        self.assertEqual(s[0][1][g.ESTADO], "pousado")
        # Ordem dos eventos por instante, mesmo com entrada fora de ordem.
        s = g.simular([montar("E", "Energia")],
                      [[2.0, "clima", True, ""], [1.0, "clima", False, ""]],
                      [False, "livre"], g.CONFIG)
        self.assertEqual(s[0][0][g.ESTADO], "operacional")

    def test_conservacao_consultas_e_sem_repeticao(self):
        for caso in casos():
            original = copy.deepcopy(caso)
            s = g.simular(caso[1], caso[2], caso[3], g.CONFIG)
            self.assertEqual(caso, original)
            self.assertEqual(len(s[0]), len({m[g.ID] for m in s[0]}))
            self.assertEqual(set(s[1]), {i for i,m in enumerate(s[0]) if m[g.ESTADO] == "espera"})
            self.assertEqual(len(s[1]), len(set(s[1])))
            self.assertEqual(len(s[3]), len(set(s[3])))
            self.assertEqual(s[4], s[2])
            copia = copy.deepcopy(s)
            topo = g.ultimo_evento(s[4])
            s[4] = g.desfazer_consulta(s[4])
            self.assertEqual(topo, copia[4][-1])
            self.assertEqual(s[0:4], copia[0:4])
            self.assertEqual(s[5:], copia[5:])
        dados = [montar("E", "Energia", sensores=False)]
        s = g.simular(dados, [[1.0, "clima", True, ""], [2.0, "clima", True, ""]], [True, "livre"], g.CONFIG)
        self.assertEqual(len(s[3]), 1)
        self.assertEqual(s[5], 2.0)

    def test_buscas_e_validacao(self):
        lista = [montar("E", "Energia", fuel=12.0), montar("M", "Médico", prioridade=5)]
        self.assertEqual(g.buscar(lista, g.TIPO, "Médico"), 1)
        self.assertEqual(g.buscar(lista, g.TIPO, "Laboratório"), -1)
        self.assertEqual(g.buscar_extremo(lista, g.COMBUSTIVEL, False), 0)
        self.assertEqual(g.buscar_extremo(lista, g.PRIORIDADE, True), 1)
        self.assertEqual(g.buscar_extremo([], g.PRIORIDADE, True), -1)
        for campo, valor in [(g.MASSA, 0), (g.COMBUSTIVEL, -1), (g.ETA, -1),
                             (g.MASSA, float("nan")), (g.COMBUSTIVEL, float("inf"))]:
            dados = [montar("E", "Energia")]
            dados[0][campo] = valor
            self.assertFalse(g.validar(dados, [], [True, "livre"], g.CONFIG))
        self.assertFalse(g.validar([lista[0], lista[0]], [], [True, "livre"], g.CONFIG))
        self.assertFalse(g.validar(lista, [], [True, "livre"], [0, 0.002, 2, 0.25]))

    def test_entradas_malformadas(self):
        bons = [[montar("E", "Energia")], [], [True, "livre"], list(g.CONFIG)]
        for pos in range(4):
            for valor in (None, 42, True, "abc", {}, ()):
                args = copy.deepcopy(bons)
                args[pos] = valor
                with self.subTest(pos=pos, valor=valor), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(g.simular(*args), [])
        for pos in (0, 1):
            for linha in (None, 42, True, "abc", {}, (), [], [1]):
                args = copy.deepcopy(bons)
                args[pos] = [linha]
                with self.subTest(pos=pos, linha=linha), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(g.simular(*args), [])

    def test_campos_e_alvos_invalidos(self):
        for campo, valor in [(g.ID, []), (g.TIPO, []), (g.ESTADO, 42),
                             (g.MOTIVO, None), (g.SENSORES, 1), (g.SISTEMAS, 0)]:
            dados = [montar("E", "Energia")]
            dados[0][campo] = valor
            self.assertFalse(g.validar(dados, [], [True, "livre"], g.CONFIG))
        for evento in [[0, "clima", True, "E"], [0, "area", "livre", "E"],
                       [0, "sistemas", True, "inexistente"], [0, "sensores", True, []],
                       [0, [], True, ""], [0, "clima", 1, ""]]:
            self.assertFalse(g.validar([montar("E", "Energia")], [evento], [True, "livre"], g.CONFIG))

    def test_tabela_verdade_completa(self):
        for c, s, e, a, d in product((False, True), repeat=5):
            m = montar("E", "Energia", fuel=12 if c else 11, sensores=s, sistemas=e)
            with self.subTest(condicoes=(c, s, e, a, d)):
                self.assertEqual(g.autorizar(m, [a, "livre" if d else "ocupada"], g.CONFIG) == "",
                                 all((c, s, e, a, d)))

    def test_limites_combustivel(self):
        for fuel, apto, urgente in [(11.999, False, None), (12, True, True),
                                    (15, True, True), (15.001, True, False)]:
            m = montar("M", "Médico", fuel=fuel)
            self.assertEqual(g.autorizar(m, [True, "livre"], g.CONFIG) == "", apto)
            if apto:
                self.assertEqual(g.vem_antes(m, montar("E", "Energia"), g.CONFIG), urgente)
                r = g.simular([m], [], [True, "livre"], g.CONFIG)
                self.assertGreaterEqual(r[0][0][g.COMBUSTIVEL], g.CONFIG[2])

    def test_falha_base_e_propagacao(self):
        s = self.rodar("falha_energia_base")
        self.assertTrue(all(m[g.ESTADO] == "suspenso" for m in s[0]))
        self.assertEqual(s[7], [0, 1, 2, 3, 4])
        self.assertEqual(s[1], [])
        self.assertEqual(len(self.inicios(s)), 5)
        self.assertIn("Sensores/sistemas", s[0][0][g.MOTIVO])
        self.assertIn("Aguarda Energia", s[0][1][g.MOTIVO])
        self.assertTrue(all(m[g.COMBUSTIVEL] == 20 for m in s[0]))
        self.assertEqual(len(s[3]), 5)

    def test_recuperacao_sem_novo_pouso(self):
        s = self.rodar("recuperacao_energia_base")
        self.assertTrue(all(m[g.ESTADO] == "operacional" and m[g.MOTIVO] == "" for m in s[0]))
        self.assertEqual(s[7], [0, 1, 2, 3, 4])
        self.assertEqual(len(self.inicios(s)), 5)
        self.assertTrue(all(m[g.COMBUSTIVEL] == 20 for m in s[0]))
        self.assertEqual(s[5], 30)
        self.assertEqual(s[2].count("E operacional"), 2)
        self.assertEqual(s[2].count("L operacional"), 2)
        # Os alertas anteriores continuam disponíveis como histórico.
        self.assertEqual(len(s[3]), 5)

    def test_falha_durante_descida_impede_ativacao(self):
        s = self.rodar("falha_sensores_na_descida")
        self.assertEqual(s[5], 5)
        self.assertEqual(s[7], [0])
        self.assertEqual(s[0][0][g.ESTADO], "suspenso")
        self.assertNotIn("E operacional", s[2])
        self.assertTrue(any("previsto: 3.0" in e and "5.0 min:" in e for e in s[2]))

    def test_dependencias_ordem_inversa_e_redundancia(self):
        dados = [montar("L", "Laboratório"), montar("H", "Habitação"), montar("E", "Energia")]
        for m in dados:
            m[g.ESTADO] = "pousado"
        hist = g.ativar(dados, [])
        self.assertEqual(hist, ["E operacional", "H operacional", "L operacional"])
        dados[1][g.SENSORES] = False
        hist = g.ativar(dados, hist)
        self.assertEqual([m[g.ESTADO] for m in dados], ["suspenso", "suspenso", "operacional"])
        copia = list(hist)
        self.assertEqual(g.ativar(dados, hist), copia)  # sem registros repetidos
        dados[1][g.SENSORES] = True
        self.assertEqual(g.ativar(dados, hist)[-2:], ["H operacional", "L operacional"])
        # Um segundo módulo Energia saudável mantém o fornecimento.
        dados = [montar("E1", "Energia"), montar("E2", "Energia"), montar("H", "Habitação")]
        s = g.simular(dados, [[16, "sistemas", False, "E1"]], [True, "livre"], g.CONFIG)
        self.assertEqual([m[g.ESTADO] for m in s[0]], ["suspenso", "operacional", "operacional"])

    def test_acidente_nao_e_recuperado_com_evento_sistemas(self):
        s = g.simular([montar("E", "Energia", acidente=True)],
                      [[6, "sistemas", True, "E"]], [True, "livre"], g.CONFIG)
        self.assertEqual(s[0][0][g.ESTADO], "acidente")
        self.assertEqual(s[7], [])
        self.assertEqual(s[6][1], "obstruída")

    def test_todas_permutacoes_candidatos(self):
        mods = [montar("E", "Energia"), montar("H", "Habitação"),
                montar("G", "Logística"), montar("M", "Médico", fuel=13),
                montar("L", "Laboratório", fuel=12)]
        for entrada in permutations(range(5)):
            ordem = list(entrada)
            g.ordenar(ordem, mods, g.CONFIG)
            self.assertEqual(ordem, [4, 3, 0, 1, 2])

    def test_eventos_empatados_respeitam_cadastro(self):
        for valores in ([False, True], [True, False]):
            eventos = [[6, "sistemas", valor, "E"] for valor in valores]
            s = g.simular([montar("E", "Energia")], eventos, [True, "livre"], g.CONFIG)
            self.assertEqual(s[0][0][g.SISTEMAS], valores[-1])
            self.assertEqual(s[0][0][g.ESTADO], "operacional" if valores[-1] else "suspenso")
            self.assertEqual(len(self.inicios(s)), 1)

    def test_falha_habitacao_isola_dependencia_laboratorio(self):
        mods = [montar("E", "Energia"), montar("H", "Habitação"),
                montar("M", "Médico"), montar("L", "Laboratório")]
        eventos = [[21, "sensores", False, "H"]]
        s = g.simular(mods, eventos, [True, "livre"], g.CONFIG)
        self.assertEqual([m[g.ESTADO] for m in s[0]],
                         ["operacional", "suspenso", "operacional", "suspenso"])
        s = g.simular(mods, eventos + [[22, "sensores", True, "H"]], [True, "livre"], g.CONFIG)
        self.assertTrue(all(m[g.ESTADO] == "operacional" for m in s[0]))
        self.assertEqual(len(self.inicios(s)), 4)
        self.assertTrue(all(m[g.COMBUSTIVEL] == 20 for m in s[0]))

    def test_simulacao_e_pilha_vazias(self):
        s = g.simular([], [], [True, "livre"], g.CONFIG)
        self.assertEqual(s[0], [])
        self.assertEqual(s[1], [])
        self.assertEqual(s[7], [])
        self.assertEqual(s[5], 0)
        self.assertEqual(g.buscar([], g.ID, "E"), -1)
        self.assertEqual(g.desfazer_consulta([]), [])
        self.assertEqual(g.ultimo_evento([]), "Pilha de consulta vazia")

    def test_recursos_do_codigo_estudantil(self):
        arvore = ast.parse(Path(g.__file__).read_text(encoding="utf-8"))
        proibidos = (ast.Import, ast.ImportFrom, ast.Dict, ast.Set, ast.Tuple,
                     ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp,
                     ast.Lambda, ast.Raise, ast.Try, ast.ClassDef)
        self.assertFalse(any(isinstance(n, proibidos) for n in ast.walk(arvore)))
        self.assertFalse(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                             for n in ast.walk(arvore)))


if __name__ == "__main__":
    unittest.main()
