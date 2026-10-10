"""Roteiro de avaliação do MGPEB: escolha entre o terminal e o painel HTML.

Uso:
    python avaliar.py            (mostra o menu)
    python avaliar.py terminal   (programa principal, 14 cenários ao vivo e testes)
    python avaliar.py ao-vivo urgente   (só a transmissão ao vivo de um cenário)
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
    ["Programa principal: buscas, fila, autorização e relatório", ["mgpeb.py"]],
    ["Os 14 cenários de exemplos.py, transmitidos ao vivo (2x)", ["ao_vivo.py", "--todos", "2"]],
    ["Testes automatizados", ["-m", "unittest"]],
]


def interativo():
    # Sem terminal (saída redirecionada), não há quem aperte Enter.
    return sys.stdin.isatty() and sys.stdout.isatty()


def pausar(mensagem):
    if interativo():
        try:
            input(mensagem)
        except EOFError:
            pass  # entrada fechada: segue sem pausar


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


def escolher_cenario():
    # Importação tardia: o exportador é apenas um complemento do roteiro.
    from exportar_painel import todos_os_casos
    nomes = [caso[0] for caso in todos_os_casos()]
    print("Cenários: " + ", ".join(nomes))
    try:
        nome = input("Cenário (Enter: padrao; 0: voltar): ").strip() or "padrao"
    except EOFError:
        return 0
    if nome == "0":
        return 0
    if nome not in nomes:
        print("Cenário desconhecido. Voltando ao menu.")
        return 0
    return rodar("Simulação ao vivo", ["ao_vivo.py", nome])


def menu():
    if not interativo():
        print("Sem terminal interativo: use 'python avaliar.py terminal' ou 'painel'.")
        return 2
    # Laço, sem recursão: cada rodada termina antes de oferecer a próxima.
    while True:
        print("\nMGPEB - Aurora Siger | Roteiro de avaliação")
        print("  1 - Terminal: programa principal, 14 cenários ao vivo e testes")
        print("  2 - Painel HTML: simulação animada no navegador")
        print("  3 - Rodar um cenário no terminal")
        print("  0 - Sair")
        try:
            escolha = input("Escolha: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAvaliação encerrada.")
            return 0
        if escolha == "0":
            return 0
        if escolha == "1":
            codigo = caminho_terminal()
        elif escolha == "2":
            codigo = caminho_painel()
        elif escolha == "3":
            codigo = escolher_cenario()
        else:
            print("Opção inválida. Escolha 0, 1, 2 ou 3.")
            continue
        if codigo != 0:
            return codigo  # uma falha não pode ser escondida pelo loop
        print("\nExecução concluída. Você pode escolher outra opção.")


def main(argumentos):
    if not argumentos:
        return menu()
    if argumentos[0] == "terminal":
        codigo = caminho_terminal()
    elif argumentos[0] == "ao-vivo":
        codigo = rodar("Simulação ao vivo", ["ao_vivo.py"] + argumentos[1:])
    elif argumentos[0] == "painel":
        codigo = caminho_painel(abrir="--nao-abrir" not in argumentos)
    else:
        print(__doc__)
        return 2
    # Comandos automatizados acabam; no terminal, voltamos à escolha inicial.
    if codigo == 0 and interativo() and "--nao-abrir" not in argumentos:
        return menu()
    return codigo


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
