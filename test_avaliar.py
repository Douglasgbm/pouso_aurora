"""O roteiro repete a escolha, preserva erros e não bloqueia automações."""
import contextlib
import io
import unittest
from unittest.mock import patch
import avaliar
import ao_vivo


class TestRoteiro(unittest.TestCase):
    def setUp(self):
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def test_menu_repete_terminal_e_painel(self):
        with patch.object(avaliar, 'interativo', return_value=True), patch('builtins.input', side_effect=['1', '2', '0']), patch.object(avaliar, 'caminho_terminal', return_value=0) as terminal, patch.object(avaliar, 'caminho_painel', return_value=0) as painel:
            self.assertEqual(avaliar.menu(), 0)
            terminal.assert_called_once()
            painel.assert_called_once()

    def test_cenario_volta_ao_menu_e_pode_repetir(self):
        with patch.object(avaliar, 'interativo', return_value=True), patch('builtins.input', side_effect=['3', 'urgente', '3', 'normal', '0']), patch.object(avaliar, 'rodar', return_value=0) as rodar:
            self.assertEqual(avaliar.menu(), 0)
            self.assertEqual([c.args[1] for c in rodar.call_args_list], [['ao_vivo.py', 'urgente'], ['ao_vivo.py', 'normal']])

    def test_opcao_invalida_nao_encerra(self):
        with patch.object(avaliar, 'interativo', return_value=True), patch('builtins.input', side_effect=['x', '0']):
            self.assertEqual(avaliar.menu(), 0)

    def test_entrada_fechada_sai_sem_loop(self):
        with patch.object(avaliar, 'interativo', return_value=True), patch('builtins.input', side_effect=EOFError):
            self.assertEqual(avaliar.menu(), 0)

    def test_falha_nao_e_mascarada(self):
        with patch.object(avaliar, 'interativo', return_value=True), patch('builtins.input', return_value='1'), patch.object(avaliar, 'caminho_terminal', return_value=7):
            self.assertEqual(avaliar.menu(), 7)

    def test_comando_interativo_volta_ao_menu(self):
        with patch.object(avaliar, 'interativo', return_value=True), patch.object(avaliar, 'rodar', return_value=0), patch.object(avaliar, 'menu', return_value=0) as menu:
            self.assertEqual(avaliar.main(['ao-vivo', 'urgente', '0']), 0)
            menu.assert_called_once()

    def test_automacao_nao_entra_no_menu(self):
        with patch.object(avaliar, 'interativo', return_value=False), patch.object(avaliar, 'rodar', return_value=0), patch.object(avaliar, 'menu') as menu:
            self.assertEqual(avaliar.main(['ao-vivo', 'urgente', '0']), 0)
            menu.assert_not_called()

    def test_velocidade_invalida(self):
        for valor in ['rapido', '-1', 'nan', 'inf', '-inf']:
            with self.subTest(valor=valor):
                self.assertEqual(ao_vivo.main(['urgente', valor]), 2)

    def test_zero_permite_execucao_sem_espera(self):
        self.assertEqual(ao_vivo.main(['urgente', '0']), 0)


if __name__ == '__main__':
    unittest.main()
