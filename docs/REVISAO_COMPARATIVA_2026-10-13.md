# Aurora: revisão comparativa e fechamento
## Fase 1 como referência de qualidade | Fase 2 revisada

**Data:** 13 de outubro de 2026

**Equipe da Fase 2:** Alice Brenda (RM 574916), Douglas Goltz (RM 574439) e Marcelo Santos (RM 576131).

### Parecer

Nos requisitos obrigatórios verificados, não foi identificado defeito conhecido de implementação. A Fase 2 tem código, exemplos, anexo e conteúdo de apoio coerentes entre si. A suíte passou em 46 testes, a auditoria passou em 13 verificações e os exemplos salvos correspondem à execução atual. Isso sustenta o uso acadêmico do protótipo nos cenários analisados, sem garantir nota ou ausência absoluta de defeitos.

A revisão preservou o núcleo e a estrutura do HTML do Douglas. As mudanças desta rodada concentram-se em documentação, organização, identificação da equipe e geração dos PDFs. A Fase 1 orientou a clareza da apresentação e das evidências. Conforme orientação de Marcelo, a identidade visual dos PDFs de apoio acompanha o HTML da Fase 2.

### O que ainda falta

A colega da equipe fará o PDF final. RELATORIO_TECNICO.pdf é uma base de apoio atualizada, com dez páginas, e não uma entrega final aprovada. Quando o PDF final chegar, será necessário conferir seu conteúdo contra esta versão. Também permanece pendente a conferência visual do novo modo de leitura do HTML em navegador real. O HTML é um extra.

### Como ler

Este documento apresenta as fontes, compara as fases, explica as regras auditadas, lista as mudanças e registra as evidências e limitações. O guia detalhado explica o programa passo a passo. O arquivo STATUS_ENTREGA.md indica a referência atual.

<!-- PAGE BREAK -->

## 1. Qual versão da Fase 1 foi usada

Foi consultado o repositório indicado pela orientação de Marcelo: https://github.com/MRC888/Aurora-PBL-FIAP . A referência é o commit e29672498086ae3018909fbddf1c60e9cfa0699b e o documento docs/Aurora-2.0.pdf, com 15 páginas. A nota 10 foi informada por Marcelo; não foi consultado o portal acadêmico.

A comparação de bytes confirmou que esse PDF é idêntico ao arquivo local Aurora final version.pdf. O arquivo local Aurora 3.0.pdf não foi adotado como autoridade apenas por ter numeração maior. O ZIP antigo da Fase 1 também não foi usado como fonte principal: contém uma interface de entrada anterior à versão do GitHub.

O código atual da Fase 1 recebe cinco entradas e calcula integridade operacional. O ZIP antigo pede seis entradas, incluindo integridade informada manualmente. Escolher a fonte certa evita transportar uma descrição desatualizada para a comparação. A Fase 1 foi preservada sem alterações.

### Fontes da conferência

| Fonte | Uso na revisão |
|---|---|
| GitHub da Fase 1: PDF, README, código, notebook e testes | Organização, narrativa, exemplos e versão de referência |
| PBL Aurora 1.docx | Separar exigências da Fase 1 das atuais |
| PBL Aurora 2.docx | Matriz dos seis itens e formatos de entrega |
| main dos dois repositórios da Fase 2 | Base atual antes da revisão |
| Código, exemplos, testes, SVG, HTML e Markdown/PDF | Coerência da implementação com a explicação |
| Pastas da Fase 2 no OneDrive | Identificar materiais históricos e preparar referência atual |

### Rastreabilidade

SHA-256 do PDF de referência da Fase 1:

```text
ab784c82975903141c760e73ca2a9eae526
004739430c08a487430ef120f8313
```

O hash está quebrado em duas linhas apenas para caber na página; sua concatenação identifica o arquivo. A base da revisão da Fase 2 no repositório do Douglas é 1ea80a59e93d3a87c80aae9b2dc172811fa1e096. No repositório de Marcelo, é 44960447bcdf7c89ba47d8da27ce03a14470f0ce. Históricos diferentes podem conter arquivos idênticos. O manifesto docs/hashes_validacao.json registra o conteúdo desta revisão.

<!-- PAGE BREAK -->

## 2. Os trabalhos lado a lado

| Critério | Fase 1 no GitHub | Fase 2 revisada |
|---|---|---|
| Pergunta central | A nave pode decolar? | Quem pode pousar e operar? |
| Entradas | Cinco telemetrias; integridade calculada | Listas de módulos, eventos, ambiente e configuração |
| Segurança | Condições obrigatórias antes da decisão | Cinco condições obrigatórias antes de ordenar aptos |
| Matemática | Energia inicial, perdas e saldo | Consumo linear e mínimo com reserva afim |
| Resultado explicado | Diagnóstico e decisão de decolagem | Motivos, histórico, fila, pousados e estado operacional |
| Exemplos | Cenários e missão demonstrados | 14 exemplos Python e 15 cenários no painel |
| Forma de estudar | README, notebook, PDF e evidências | README, guia detalhado, PDF de apoio e testes |
| Entrega exigida | PDF e Git público com notebook | PDF de 5 a 10 páginas, Python e anexo |
| Equipe | Cinco integrantes | Alice, Douglas e Marcelo |
| Continuidade | Preparação da viagem | Pouso e estabilização da base |

### O padrão que foi mantido

A documentação apresenta o problema antes do código, nomeia as entradas, informa unidades e limites, explica decisões e mostra um resultado reproduzível. O leitor consegue ir da explicação ao comando de execução e conferir a saída. O README da Fase 2 passou a reunir esse percurso e os links dos materiais atuais.

A Fase 1 não é copiada literalmente. Seu PDF de 15 páginas ultrapassaria o limite da Fase 2. Seu notebook não é exigido pelo enunciado atual. Sua equipe de cinco pessoas não deve aparecer na identificação desta fase. Os programas têm continuidade temática, sem integração automática de dados entre eles.

### Identidade do PDF de apoio

A referência visual é o painel HTML: fundo escuro #0c0b1e, superfícies #06141c, ciano #46f0ff e rosa #ff3d7f. A capa usa uma moldura de monitor e detalhes dessas cores. As páginas internas claras e acentos mais escuros favorecem leitura e impressão. A colega pode adaptar a diagramação do PDF final; os itens e evidências devem permanecer.

Um padrão permanente foi registrado em docs/PADRAO_PBL_AURORA.md para orientar os próximos PBLs: conferir enunciado, mapear requisitos, explicar hipóteses, verificar resultados e separar histórico de material atual.

<!-- PAGE BREAK -->

## 3. Conferência técnica do MGPEB

### Dados, decisões e ordenação

O cadastro representa cada módulo em uma lista de 12 campos. As chegadas entram em fila FIFO e vão para espera. A lista de aptos contém somente os autorizados. A busca sequencial e a ordenação por inserção deixam os passos visíveis para estudo. Empates completos conservam a ordem de entrada.

A autorização exige combustível suficiente, sensores e sistemas saudáveis, atmosfera aceitável e área livre. Foram verificadas as 32 combinações booleanas. O diagrama expressa a mesma regra, incluindo a equivalência de De Morgan: NOT(NOT S OR NOT E) = S AND E.

Urgência nunca permite um pouso inseguro. Entre aptos, menor margem tem preferência quando há urgência; empates urgentes consideram criticidade. A ordem por tipo e os demais desempates seguem o código. A prioridade numérica maior tem preferência no critério correspondente. As 120 permutações do conjunto auditado produziram a ordem esperada.

### Matemática e unidades

O consumo estimado é C(t) = k*m*t. Com k = 0,002 kg/(kg.min), massa de 1.000 kg e tempo de 5 min, o consumo é 10 kg. O mínimo para autorização é F(t) = C(t) + R = 12 kg, com reserva de 2 kg. C é linear; F é afim. A reserva não é consumo adicional de descida.

Com combustível inicial de 30 kg, restam 20 kg por módulo. O cenário normal termina em 25 min com cinco módulos operacionais. A fronteira de autorização foi conferida em 11,999 kg, 12 kg, 15 kg e 15,001 kg: 11,999 bloqueia; 12 e 15 são urgentes; 15,001 já supera a margem de 25%. Não há NumPy ou Matplotlib no núcleo; o gráfico do relatório é SVG e representa a fórmula didática.

### Estabilização e eventos

Pouso e operação são estados diferentes. Energia saudável permite operar os dependentes; Laboratório também depende de Habitação. Falhas após o pouso suspendem os módulos afetados e seus dependentes. Reparos podem restaurar a operação sem novo pouso ou consumo. Um acidente não é desfeito por reparo de sistemas.

A descida é uma transição indivisível: eventos previstos durante ela são processados no fim, antes do resultado. Isso está explicado no relatório. Os alertas persistem como histórico, mesmo após recuperação. A pilha demonstra LIFO numa cópia do histórico; retirar uma consulta não reverte o mundo simulado.

### Limites preservados

Não há cálculo físico de trajetória, altitude, arrasto ou probabilidade de acidente. Não há consumo em órbita, radiação simulada ou redundância de hardware. ESG é reflexão de projeto, com propostas ainda não implementadas. Essas limitações não devem ser ocultadas na apresentação.

<!-- PAGE BREAK -->

## 4. Mudanças realizadas e motivo

| Encontrado | Alteração | Por quê |
|---|---|---|
| Guia ainda identificado como versão 1.1 e com trechos de contagens antigas | Versão, data e suíte atualizadas; correções antigas identificadas como anteriores | Evitar estudar uma descrição ultrapassada |
| Necessidade de confirmar equipe | Alice, Douglas e Marcelo, com os RMs | Não copiar os cinco integrantes da Fase 1 |
| README com informações dispersas | Fluxo, comandos, resultado esperado, menu e mapa de materiais reunidos | Facilitar execução e apresentação |
| Documentação sem detalhamento do modo de leitura | Comportamento, atalhos e limite da validação registrados | Explicar o extra sem alegar teste visual inexistente |
| PDFs precisavam refletir as fontes atuais | Regeneração do relatório de apoio e guia | Manter PDF e Markdown coerentes |
| Preferência visual esclarecida por Marcelo | Tema do HTML aplicado aos PDFs de apoio | Dar continuidade à interface do projeto |
| Revisões antigas junto dos documentos atuais | Transferidas para docs/historico, com aviso | Preservar memória sem confundir o status |
| main.py podia ser confundido com entrada atual | Aviso de experimento anterior adicionado | Direcionar para mgpeb.py e avaliar.py |
| Necessidade de base para próximos PBLs | Padrão permanente e matriz atual registrados | Repetir o processo de qualidade |
| Pastas antigas do OneDrive | Referência atual separada e índice de leitura | Evitar escolher um PDF ou slide antigo por engano |

### O que esta revisão preservou

Não houve mudança na semântica de mgpeb.py, na fórmula de combustível ou nos critérios de ordenação. A estrutura visual do HTML do Douglas, os cenários, a escolha terminal/painel e o retorno ao menu foram preservados. Os dados do painel foram regenerados para confirmar que correspondem ao exportador atual.

O modo de leitura foi incorporado em uma revisão anterior do HTML; nesta rodada ele foi documentado e exercitado novamente com DOM simulado. As correções de validação, suspensão e recuperação também são anteriores e foram novamente verificadas. O relatório não atribui essas implementações à rodada atual.

### Organização da entrega

O material atual no OneDrive fica em Fase 2/Aurora 2/Versao atual - 2026-10-13. O código obrigatório é separado dos documentos de apoio. O PDF final continua sob responsabilidade da colega. Guias, auditorias e slides não devem ser somados ao limite do relatório acadêmico.

As apresentações de 7 e 8 de outubro são históricas e não foram reeditadas nesta revisão. Elas podem conter números ou status antigos; o guia e o comparativo atuais devem orientar o estudo. Há aviso junto do índice da pasta para evitar usá-las como fonte atual sem revisão.

<!-- PAGE BREAK -->

## 5. Evidências e conclusão da auditoria

| Verificação | Resultado e alcance |
|---|---|
| Suíte Python da Fase 2 | 46 aprovados: 22 núcleo, 11 exportador, 4 transmissão, 9 roteiro |
| Auditoria adicional | 13 verificações aprovadas, incluindo 32 combinações e 120 permutações |
| Código em pasta isolada | mgpeb.py e exemplos.py executam sem dependências externas |
| Exemplos salvos | 14 cenários, saída UTF-8 idêntica à execução |
| Cenário padrão | 25 min, cinco operacionais, 20 kg por módulo |
| Transmissão direta | Cenário urgente executado com espera zero |
| Exportação do painel | 15 cenários; dados regenerados sem divergência |
| JavaScript com DOM simulado | 15 cenários nos dois modos; alternância, teclado, avanço e transformações |
| Fase 1 | Sete testes aprovados; PDF do Git confirmado como referência |
| Documentos | PDF de apoio com dez páginas; guia separado; renderização para inspeção |
| Referências científicas | Links primários conferidos; pressupostos separados de fatos citados |

### Como reproduzir

```text
python -m unittest -v
python mgpeb.py
python exemplos.py
python ao_vivo.py urgente 0
python exportar_painel.py
python -m pip install -r requirements-relatorio.txt
python auditoria.py .
```

A evidência resumida está em docs/evidencias_revisao_2026-10-13.json. O manifesto de SHA-256 identifica os arquivos auditados e permite comparar as cópias. Aprovação em testes significa aprovação nesses testes, não comprovação de todos os comportamentos possíveis.

### Fontes científicas do relatório de apoio

Computer History Museum, história do ENIAC: https://www.computerhistory.org/revolution/story/78 . NASA, computação espacial: https://www.nasa.gov/directorates/stmd/nasa-industry-advance-high-performance-spaceflight-computing/ . NASA, componentes do Perseverance: https://science.nasa.gov/mission/mars-2020-perseverance/rover-components/ . NASA/JPL, proteção planetária: https://planetaryprotection.jpl.nasa.gov/ . Consulta em 13/10/2026.

### Parecer final e próximos passos

O conjunto obrigatório verificado está coerente para servir de base ao fechamento acadêmico. Não foi reproduzido erro de lógica que exija alteração do núcleo nesta rodada. A prioridade é a colega produzir o PDF final e a equipe conferir seu conteúdo, identificação e regras do portal antes do envio.

A revisão visual do HTML permanece aberta: a ferramenta bloqueou a abertura do arquivo local, e testes com DOM simulado não avaliam CSS, legibilidade, recortes ou comportamento real de foco. Não se declarou essa etapa concluída. O extra pode ser conferido abrindo o painel no computador da equipe.

