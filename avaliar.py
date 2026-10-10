"""Roteiro de avaliação do MGPEB: escolha entre o terminal e o painel HTML.

Uso:
    python avaliar.py            (mostra o menu)
    python avaliar.py terminal   (simulação, 14 cenários e testes no terminal)
    python avaliar.py painel     (regenera os dados e abre o painel no navegador)

Este roteiro só chama os programas do projeto, na ordem certa, e mostra
cada comando antes de executá-lo; ele não faz parte do protótipo avaliado.
Usa apenas a biblioteca padrão do Python.
"""
import subprocess
import sys
import webbrowser
from pathlib import Path

PASTA = Path(__file__).resolve().parent
PAINEL = PASTA / "painel" / "index.html"

ETAPAS_TERMINAL = [
    ["Rodada padrão: buscas, fila, autorização e relatório", ["mgpeb.py"]],
    ["Os 14 cenários de estudo", ["exemplos.py"]],
    ["Testes automatizados", ["-m", "unittest"]],
]


def interativo():
    # Sem terminal (saída redirecionada), não há quem aperte Enter.
    return sys.stdin.isatty() and sys.stdout.isatty()


def pausar(mensagem):
    if interativo():
        input(mensagem)


def rodar(titulo, argumentos):
    # -X utf8 deixa os acentos iguais em qualquer sistema operacional.
    comando = [sys.executable, "-X", "utf8"] + argumentos
    print()
    print("=" * 70)
    print(titulo)
    print("$ python " + " ".join(argumentos))
    print("=" * 70, flush=True)
    resultado = subprocess.run(comando, cwd=PASTA)
    if resultado.returncode != 0:
        print(f"\nA etapa falhou (código {resultado.returncode}). Avaliação interrompida.")
    return resultado.returncode


def caminho_terminal():
    total = len(ETAPAS_TERMINAL)
    for numero, (titulo, argumentos) in enumerate(ETAPAS_TERMINAL, start=1):
        codigo = rodar(f"[{numero}/{total}] {titulo}", argumentos)
        if codigo != 0:
            return codigo
        if numero < total:
            pausar("\nEnter para a próxima etapa...")
    print("\nTodas as etapas do terminal terminaram sem erro.")
    return 0


def caminho_painel(abrir=True):
    codigo = rodar("[1/2] Exportar os cenários do simulador para o painel",
                   ["exportar_painel.py"])
    if codigo != 0:
        return codigo
    print()
    print("=" * 70)
    print("[2/2] Abrir o painel no navegador")
    print("=" * 70)
    print("O painel só reproduz as decisões que o mgpeb.py acabou de exportar.")
    print("Controles: espaço reproduz/pausa, → avança um fato, clique numa tela amplia.")
    print("Arquivo:", PAINEL)
    if abrir and not webbrowser.open(PAINEL.as_uri()):
        print("Não foi possível abrir o navegador; abra o arquivo acima com dois cliques.")
    return 0


def menu():
    print("MGPEB - Aurora Siger | Roteiro de avaliação")
    print()
    print("  1 - Terminal: simulação, 14 cenários e testes")
    print("  2 - Painel HTML: simulação animada no navegador")
    print()
    if not interativo():
        print("Sem terminal interativo: use 'python avaliar.py terminal' ou 'painel'.")
        return 2
    escolha = input("Escolha 1 ou 2: ").strip()
    if escolha == "1":
        return caminho_terminal()
    if escolha == "2":
        return caminho_painel()
    print("Opção inválida.")
    return 2


def main(argumentos):
    if not argumentos:
        return menu()
    if argumentos[0] == "terminal":
        return caminho_terminal()
    if argumentos[0] == "painel":
        # --nao-abrir serve para conferir o roteiro sem abrir o navegador.
        return caminho_painel(abrir="--nao-abrir" not in argumentos)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
