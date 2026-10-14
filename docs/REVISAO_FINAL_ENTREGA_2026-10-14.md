# Revisão final de entrega - 14/10/2026

## Resultado e versão examinada

A revisão não encontrou falha impeditiva no código obrigatório ou divergência dos resultados entre Python e HTML. O relatório disponível cobre os seis tópicos e os três entregáveis do enunciado. Foram repetidas as validações e ampliada a inspeção do painel em navegador real.

PDF examinado: RELATORIO_FINAL_EQUIPE.pdf, 10 páginas, SHA-256 c997861e6b543b60c9d10d35c57bc1de9cc88fa085054d733cb55c32d895fa6d. É idêntico ao arquivo Aurora Siger - Fase 2.pdf encontrado na Área de Trabalho e aos downloads públicos dos dois repositórios. Não foi localizado outro PDF da Alice na Área de Trabalho, Downloads ou pasta Fase 2. A referência a um novo ajuste final ainda precisa ser associada a um arquivo diferente, caso exista; esta revisão não afirma ter examinado uma versão não recebida.

Base do código examinada: MRC888 b6d35b6c2fdc80f6180ab555ce2b573da0ef46d9 e Douglasgbm 43b02fedd3c307ffa717976b0ea12a6ece404287. Ambos possuíam a mesma árvore 3393bb7ebafbb5f2f933bb3be6965a2eb19fb3b6 antes deste registro. Nenhuma alteração no simulador, nos dados do painel ou no PDF foi necessária nesta rodada.

## Correspondência entre os materiais

| Exigência | PDF da equipe | Código e apresentação | Resultado |
|---|---|---|---|
| Equipe | p. 1, Alice Brenda 574916, Douglas Goltz 574439, Marcelo Santos 576131 | README identifica os mesmos três integrantes | Coerente |
| Cenário e atributos | p. 2, cinco tipos, massa, combustível, prioridade, criticidade e ETA | TIPOS, MODULOS e posições nomeadas | Coerente |
| Estruturas e anexo | p. 3, anexo integrado, FIFO, listas e pilha | fila de chegadas, espera, aptos, pousados, alertas e cópia LIFO do histórico | Atendido; ver observação editorial |
| Portas lógicas | p. 4, C AND S AND E AND A AND D; De Morgan | autorizar bloqueia cada condição; HTML agrupa sensores e sistemas na porta de saúde, detalhando os cinco valores | Coerente |
| Python e prioridade | p. 5, segurança antes de ordenação, urgência e desempates | busca linear, busca de extremos, inserção; aptos ordenados sem alterar cadastro | Coerente |
| Matemática | p. 6, C=kmt e F=C+R; gráfico linear e afim | taxa .002, massa 1000, duração 5: consumo 10, mínimo 12; margem urgente até 25% | Coerente |
| Evolução e hardware | p. 7 | Limitações relacionadas a buscas, ordenação, memória e confiabilidade; não promete proteção física inexistente | Atendido |
| ESG | p. 8 | Ambiente, recursos, produção, resíduos, participação, transparência e responsabilidades; propostas distinguidas da implementação | Atendido |
| Evidências | p. 9, 46 testes, 13 verificações, 14 exemplos, 32 combinações | Todos repetidos com sucesso; 15 cenários HTML incluem padrão | Coerente; texto de pendência visual está desatualizado |
| Extra e links | p. 10, HTML como complemento | Site e código acessíveis; README contém acesso direto ao painel e ao PDF | Atendido |
| Limite do relatório | 10 páginas contando capa e anexo | Guia de estudo e revisão separados do relatório de entrega | Atendido |

## Verificações executadas nesta rodada

- 46 testes Python: 22 do núcleo, 11 do exportador, 4 da transmissão e 9 do menu; todos aprovados.
- 13 verificações da auditoria: incluem 32 combinações booleanas, 120 permutações de prioridade, limites de combustível, falhas e recuperação, saída salva e gerador; todas aprovadas.
- 400 cenários adicionais determinísticos, semente 20261013, com 152 descidas: integridade das entradas, determinismo, consumo, reserva, ausência de duplicações, dependências, pilha e relógio aprovados.
- 15 cenários JavaScript em dois modos de tela com DOM simulado: aprovados. Não equivale a teste visual de CSS.
- Exportação real repetida: painel/dados.js permaneceu byte a byte idêntico, confirmando que os dados publicados correspondem ao Python atual.
- Site público: HTML, dados.js e imagem sala.png baixados e comparados integralmente com o repositório, sem diferenças.
- PDF baixado dos dois Gits: idêntico ao original local. Links relativos do README apontam para arquivos existentes.
- Manifesto SHA-256 conferido para todos os arquivos listados antes das atualizações documentais desta rodada.

## Conferência adicional em navegador real

Na sala de controle, foram selecionados os 15 cenários e avançada a linha do tempo até o resultado final. Tempo, espera e ordem dos pousados exibidos concordam com o exportador. Casos representativos:

| Cenário | Tempo | Resultado observado |
|---|---:|---|
| Padrão/normal | 25 min | E, H, G, M, L; 20 kg por módulo |
| Urgente | 10 min | M antes de E; Médico 3 kg e Energia 20 kg |
| Insuficiente | 0 min | Nenhum pouso; módulo em espera com 11 kg |
| Clima / área | 0 min | Módulos em espera; atmosfera ruim / área ocupada |
| Ativação dependente | 30 min | Pousos L, E, H; ativação respeita dependências |
| Acidente | 5 min | Área obstruída, Habitação em espera, nenhum pouso bem-sucedido |
| Falha na base | 26 min | Histórico de pousos preservado; suspensão após falha |
| Recuperação da base | 30 min | Módulos recuperados, sem novos pousos |
| Falha durante descida | 5 min | Energia pousada, suspensa por sensor; não operacional |

Também foram acionados modo de leitura, reinício, próximo fato, velocidade 4x e reprodução. A linha do tempo avançou e os estados mudaram. Sala de controle e modo de leitura foram inspecionados visualmente. Nenhum erro ou aviso de console foi capturado durante a conferência. O escopo é o navegador disponível; não foram testados todos os dispositivos ou motores de navegador.

## Qualidade dos comentários

mgpeb.py possui 18 funções e 71 comentários identificados pelo tokenizer. A qualidade foi verificada por leitura, não apenas pela contagem: explica o mapa dos 12 campos e suas unidades, validação, ausência de mutação nas entradas, FIFO, LIFO, critérios de desempate, dependências, reserva, sequência dos eventos e término do laço. As etapas principais de simulação estão explicadas junto às operações. O núcleo permanece sem imports, classes ou bibliotecas avançadas. Os comentários não prometem comportamento diferente do observado.

O menu avaliar.py preserva a escolha entre terminal, HTML e cenário, volta em loop em terminal interativo e encerra corretamente em automação/EOF. O exportador explica por que escuta as funções originais e restaura suas referências mesmo quando há falha. Não foi necessário acrescentar comentários redundantes apenas para aumentar sua quantidade.

## Ajustes documentais realizados

Atualizados README, status e parecer por critério para incluir esta revisão e retirar a pendência antiga de inspeção visual do HTML. Corrigida a distinção entre evidências da base de apoio e as páginas do PDF da equipe. Os relatórios anteriores permanecem como registros históricos.

## Dois detalhes do PDF a conferir na versão ajustada

1. Página 3: o desenho coloca fila=[0,1] e espera=[0,1] sob o mesmo instante. O texto descreve corretamente a transferência FIFO; explicitar “fila antes da transferência” e “espera após a transferência” evita leitura como estado simultâneo. O resultado do cenário está correto.
2. Página 9: a frase de que a revisão visual permanece pendente é um registro anterior à publicação e aos testes de navegador. Para um PDF atualizado de entrega, substituir por uma descrição da verificação realizada, sem prometer cobertura de todos os dispositivos.

O arquivo da Alice foi preservado. Os dois detalhes não modificam o código nem os cálculos, mas impedem afirmar que não há qualquer ajuste editorial. Se a colega enviou outro arquivo, ele precisa ser identificado e revisado antes de substituir a versão atual.

## Entrega

Entregar o PDF da equipe, mgpeb.py e exemplos.py, com exemplos_saida.txt como evidência útil. O anexo já integra a página 3; HTML é um extra. Conferir no portal se os arquivos devem ser enviados individualmente ou em ZIP. O README e o status não constituem confirmação de submissão. A avaliação é de conformidade demonstrada, não de nota garantida.
