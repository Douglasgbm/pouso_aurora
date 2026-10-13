# Missão Aurora Siger - Fase 2

## Módulo de Gerenciamento de Pouso e Estabilização de Base (MGPEB)

A Fase 1 perguntou se a nave estava pronta para decolar. Agora, o problema é decidir **quem pode pousar, quem pousa primeiro e quais módulos conseguem operar na base**. A continuidade é temática; os programas das fases não trocam dados automaticamente.

**Equipe:** Alice Brenda (RM 574916), Douglas Goltz (RM 574439) e Marcelo Santos (RM 576131). Ciência da Computação, FIAP, 2026.

**Versão de referência:** núcleo 1.2; documentação e interface revisadas em 13/10/2026. Consulte [o status](STATUS_ENTREGA.md) antes de usar um relatório antigo.

## Como funciona

1. Cadastra módulos Energia, Habitação, Logística, Médico e Laboratório.
2. Recebe as chegadas em uma fila FIFO e mantém candidatos em espera.
3. Autoriza somente quem atende combustível, sensores, sistemas, atmosfera e área.
4. Ordena apenas os autorizados por urgência e critérios de desempate.
5. Reserva a área e representa uma descida por vez, com consumo estimado.
6. Reavalia dependências na base e registra histórico, alertas e pousados.

**Segurança antes da prioridade:** um módulo com 13 kg pode ter urgência; com 11 kg, ele fica bloqueado. No cenário padrão, o mínimo é 12 kg, calculado por `F(t) = k*m*t + R`. O consumo é `C(t) = k*m*t`: 10 kg para 1000 kg de massa e cinco minutos. A reserva de 2 kg permanece.

A busca é sequencial, a ordenação é por inserção e as estruturas são listas com índices explícitos. O núcleo foi mantido simples e comentado, sem bibliotecas externas. A pilha permite consultar/remover o último registro de uma cópia do histórico; não desfaz um pouso real.

## Executar o código obrigatório

É necessário Python 3. Não há dependências externas para o simulador.

```text
python mgpeb.py
python exemplos.py
```

No macOS, se necessário, use `python3` no lugar de `python`. Execute os comandos dentro da pasta extraída do projeto.

O cenário padrão termina com E, H, G, M e L operacionais, 25 minutos simulados e 20 kg por módulo. `exemplos.py` executa 14 cenários e sua saída deve corresponder a `exemplos_saida.txt`.

## Apresentar: terminal ou HTML

```text
python avaliar.py
```

| Opção | Resultado |
|---|---|
| 1 | Programa principal, 14 cenários ao vivo e testes |
| 2 | Regenera dados e abre o painel HTML |
| 3 | Executa um cenário individual |
| 0 | Encerra |

Após uma execução interativa, o menu volta. Com saída redirecionada, comandos diretos terminam sem perguntar. Falhas não são escondidas pelo loop.

```text
python avaliar.py painel
python ao_vivo.py urgente 0
```

O zero remove as esperas da transmissão. Também é possível abrir `painel/index.html` diretamente: mantenha `dados.js` e `img/` junto dele. O painel reproduz os 15 cenários exportados, sem recalcular decisões em um servidor.

### Leitura da interface

A sala de controle original permanece no computador. O botão **Modo de leitura** organiza informações com textos maiores, quebras de linha e controles de toque. Esse modo inicia automaticamente em janelas pequenas; pode ser alternado manualmente. Clique ou pressione Enter em uma tela da sala para ampliar; Escape fecha. Espaço reproduz/pausa e seta direita avança um fato quando o foco não está num controle de formulário.

Depois de alterar o simulador, regenere os dados com `python exportar_painel.py`.

## Entrega acadêmica e materiais de estudo

| Arquivo | Finalidade |
|---|---|
| [RELATORIO_TECNICO.pdf](RELATORIO_TECNICO.pdf) | Base de apoio de 10 páginas, com anexo na seção 2; a colega da equipe produzirá o PDF final |
| [RELATORIO_TECNICO.md](RELATORIO_TECNICO.md) | Fonte editável do mesmo relatório |
| mgpeb.py, exemplos.py | Código obrigatório e exemplos simples |
| [GUIA_DETALHADO.pdf](docs/GUIA_DETALHADO.pdf) | Material de estudo separado do relatório acadêmico |
| [Conferência da entrega](docs/CONFERENCIA_ENTREGA.md) | Requisito, evidência e situação |
| [Revisão comparativa](docs/REVISAO_COMPARATIVA_2026-10-13.md) | Fases 1 e 2 lado a lado e auditoria atual |
| [Padrão dos próximos PBLs](docs/PADRAO_PBL_AURORA.md) | Base reutilizável de apresentação e fechamento |

HTML e roteiro de apresentação são extras. O enunciado da Fase 2 exige PDF de 5 a 10 páginas, fonte Python e anexo de estruturas; não exige notebook, NumPy ou Matplotlib. O notebook obrigatório da Fase 1 não deve ser confundido com requisito desta fase.

## Evidências e reprodução

```text
python -m unittest -v
python -m pip install -r requirements-relatorio.txt
python auditoria.py .
python gerar_relatorio_pdf.py
python gerar_relatorio_pdf.py --fonte docs/GUIA_DETALHADO.md --destino docs/GUIA_DETALHADO.pdf --titulo "MGPEB - Guia detalhado"
```

São 46 testes Python e 13 verificações da auditoria. ReportLab e svglib servem apenas aos PDFs e à verificação do gerador; não são dependências do núcleo. O manifesto `docs/hashes_validacao.json` identifica os arquivos da versão auditada.

Para repetir a verificação de JavaScript, com Node.js instalado: `node tools/verificar_painel.cjs`. Essa ferramenta de auditoria não é dependência do simulador.

A reprodução do JavaScript foi conferida com DOM simulado, nos 15 cenários, em ambos os modos. Isso não substitui uma conferência visual real do novo layout, que permanece pendente.

## Limites e histórico

Este é um protótipo acadêmico de decisão. Não calcula trajetória, altitude, arrasto, velocidade física, radiação ou geração elétrica. Eventos durante a descida são processados ao fim dela, antes do resultado; não há controle contínuo de voo. Alertas guardam histórico, não apenas falhas atualmente ativas.

`main.py` é um experimento anterior, identificado como histórico. O programa entregue é `mgpeb.py`. Revisões antigas e suas contagens de testes foram reunidas em `docs/historico/`. A Fase 1 está em https://github.com/MRC888/Aurora-PBL-FIAP ; foi preservada sem alterações.
