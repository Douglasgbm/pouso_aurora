# MGPEB - Revisão e correções da Fase 2
## Atualização da revisão rigorosa - 6 de outubro de 2026

**Repositório de destino:** https://github.com/Douglasgbm/pouso_aurora

**Base original:** cbaf4d0. **Versão corrigida local:** 1.2, branch correcao-fase2.

### Parecer atualizado

Os problemas de comportamento reproduzidos na auditoria foram corrigidos na cópia local destinada ao repositório do Douglas. A validação passou em 21 testes automatizados e nas 13 verificações agrupadas da auditoria externa. A documentação incorpora as partes 5 e 6, diagrama vetorial, referências clicáveis e exemplos atualizados. A revisão original é preservada nas páginas seguintes como registro histórico; suas reprovações descrevem o estado anterior, não esta versão corrigida.

Não há falhas conhecidas restantes nos cenários verificados. Isso não garante nota 10 nem cobre todas as entradas possíveis. Faltam os nomes completos e RMs da equipe para finalizar a identificação da entrega. O PDF técnico permanece separado deste relatório de revisão, respeitando o limite acadêmico de 5 a 10 páginas.

### O que mudou e por quê

| Achado | Alteração aplicada | Resultado esperado |
|---|---|---|
| A1 - operação incompatível com falhas | Reavaliação de saúde e dependências; estado suspenso e recuperação | Falhas interrompem a operação afetada; reparos não repetem o pouso |
| A2 - TypeError em dados inválidos | Tipos e formatos conferidos antes da travessia | Entrada malformada retorna aviso e lista vazia |
| A3 - links truncados | Expressão regular corrigida e PDF regenerado | Destinos completos nas referências |
| A4 - saída antiga | 14 cenários e saída UTF-8 reproduzível | Resultado salvo igual à execução atual |
| A5 - diagrama e ESG | Figura AND/NOT e reflexão ampliada sobre ambiente, recursos e governança | Respostas explícitas aos itens 5 e 6 do enunciado |
| A6 - apresentação | Gráfico e legenda juntos; ligação entre hardware e algoritmos | Leitura e justificativas técnicas mais claras |

As correções de código e documentação foram incorporadas da versão 35798e8 de MRC888/pouso_aurora, preservando seu histórico. Nesta etapa, acrescentaram-se quatro testes, auditoria executável no repositório e este registro de integração. Não se atribui a esta etapa a autoria de mudanças que já existiam na cópia privada.

<!-- PAGE BREAK -->

## Validação, limites e publicação

### Como comprovar o resultado

1. Executar `python -m unittest -v`: 21 testes aprovados, contra oito na versão original.
2. Instalar as dependências documentais e executar `python auditoria.py .`: 13 grupos aprovados, contra cinco antes das correções. O script retorna código de erro se algum grupo reprovar.
3. Executar os exemplos: 14 cenários, saída salva conferida byte a byte em UTF-8.
4. Conferir o PDF técnico: dez páginas, diagrama gráfico e URLs completas. A revisão e o guia de estudo são anexos separados, fora desse limite.

Os novos testes desta etapa verificam 120 permutações dos candidatos, eventos empatados respeitando a ordem cadastrada, falha da Habitação suspendendo somente os dependentes necessários e posterior recuperação, além de simulação e pilha vazias. A cobertura já incorporada verifica as 32 combinações booleanas, limites de combustível, entradas inválidas, falha de Energia, redundância, reparo e preservação de acidentes.

O JSON de evidências identifica o commit-base e informa quando a árvore tem alterações locais. O arquivo de hashes identifica os arquivos efetivamente testados. Não confundir o commit-base registrado antes da gravação do commit final com o conteúdo corrigido: o pacote de entrega inclui o commit final e os arquivos completos.

### Decisões didáticas mantidas

A descida continua atômica: um evento previsto durante o pouso é processado no ciclo seguinte. Eventos com mesmo horário mantêm a ordem de cadastro; todos os eventos vencidos são aplicados antes da reavaliação do estado. Falha e reparo processados no mesmo ciclo ficam registrados, mas pode não haver estado intermediário de suspensão. A espera não consome combustível; acidentes são indicados nos dados. ESG e proteção planetária são propostas de concepção, não mecanismos implementados pelo Python.

As listas e laços foram mantidos para corresponder ao estágio do curso. A contagem prévia em buscar mantém custo linear mesmo no primeiro item; concatenações repetidas podem ser quadráticas. Isso está documentado como limitação e não impede o uso com poucos módulos. Não foram introduzidas bibliotecas avançadas no simulador.

### Situação do GitHub e pendências

A cópia corrigida está pronta para integração, mas não foi publicada no repositório do Douglas. O conector retornou permissão de leitura e ausência de escrita; o Git local também não possui autenticação disponível. O pacote contém o código completo, o histórico Git exportado e um patch para permitir a integração por quem tem acesso. A main remota permanece em cbaf4d0 até essa integração.

A identificação dos integrantes ainda depende de nomes completos e RMs, que não foram inventados. Com esses dados e a publicação autorizada por credencial com escrita, as pendências conhecidas da entrega podem ser encerradas. A decisão de nota cabe à FIAP.

<!-- PAGE BREAK -->

# Registro histórico da revisão original
## Repositório Douglasgbm/pouso_aurora

**Data:** 6 de outubro de 2026

**Versão auditada:** cbaf4d0de7f54e1f2fc0c2863adbfe4e472ae6c9

**Origem:** https://github.com/Douglasgbm/pouso_aurora

### 1. Parecer

O núcleo de autorização e ordenação funciona nos casos conferidos, mas esta versão ainda contém falhas de validação e coerência dos estados em solo, além de pendências documentais relevantes. Não recomendo considerá-la pronta para entrega sem tratar os achados desta revisão.

Os oito testes fornecidos pelo repositório passaram. Uma auditoria externa acrescentou 13 verificações agrupadas: cinco foram aprovadas e oito identificaram problemas. Esses números não são uma nota; várias verificações reprovadas representam manifestações da mesma falha. A cobertura adicional inclui 32 combinações de autorização, quatro limites de combustível e 120 permutações de cinco candidatos.

A versão do Douglas ainda corresponde ao mesmo commit usado como origem da cópia privada. As correções da versão 1.1 estão em MRC888/pouso_aurora, commit 35798e8, e não estão presentes no repositório aqui auditado. Os relatórios dessas duas versões devem permanecer identificados separadamente.

### Escopo e método

Foram conferidos o simulador, exemplos, testes, saída salva, relatório Markdown, PDF, gerador, instruções e planejamento. O PDF original tem dez páginas. O código do repositório foi preservado; os scripts e resultados de auditoria estão separados.

O enunciado da atividade orientou a avaliação de requisitos. Também foram consultadas páginas específicas dos capítulos 4 e 5 disponíveis na pasta Fase 2 do OneDrive, para conferir a correspondência dos conceitos de estruturas lineares, busca e inserção. Isso não equivale a uma revisão integral de todas as apostilas nem a uma previsão da nota que a FIAP atribuirá.

As prioridades abaixo indicam a ordem recomendada de correção. São problemas de um protótipo acadêmico, sem avaliação de segurança de uma missão real.

<!-- PAGE BREAK -->

## 2. Achados de comportamento

### A1. Estado operacional incompatível com falhas — prioridade alta de correção

**Local:** mgpeb.py, função ativar, linhas 201 a 223; aplicação de eventos, linhas 263 a 273, na versão auditada.

**Causa:** a função de ativação avalia somente módulos no estado pousado e não reavalia sensores ou sistemas ao ativar. Módulos já operacionais não são suspensos quando um evento modifica sua saúde. A busca por dependências considera apenas tipo e estado operacional.

**Reprodução 1:** cadastrar Energia, pousar e aplicar `[6, "sistemas", False, "E"]`. O resultado final contém sistemas=False e estado=operacional.

**Reprodução 2:** cadastrar Energia e Habitação e aplicar a falha da Energia no minuto 11. Ambos permanecem operacionais, embora a dependência da Habitação esteja falha.

**Reprodução 3:** aplicar `[3, "sensores", False, "E"]` durante a descida de Energia. A descida atômica termina no minuto 5; o evento é aplicado e, mesmo com sensores=False, o módulo é ativado.

**Consequência:** a saída pode afirmar que a base está estabilizada quando os próprios dados indicam impedimento. O terceiro caso não exige reação durante a descida: mesmo mantendo a hipótese atômica, é necessário conferir as condições no momento da ativação.

**Correção recomendada:** definir estados de suspensão, reavaliar saúde e dependências em solo e permitir recuperação por evento de reparo, sem novo pouso. Garantir que acidentes não sejam recuperados como uma simples falha de sistemas. A cópia privada já contém uma implementação dessa regra e testes correspondentes.

### A2. Entradas malformadas interrompem a simulação — prioridade média

**Local:** mgpeb.py, validar, a partir da linha 61; quantidade, a partir da linha 23.

**Causa:** a validação tenta contar elementos antes de verificar se recebeu listas. Isso se aplica tanto aos argumentos principais quanto às linhas de módulos e eventos.

**Reproduções:** `simular(None, [], [True, "livre"], CONFIG)`, módulos iguais a `[42]` ou uma lista de eventos contendo `42` causam TypeError.

**Consequência:** entradas inválidas nem sempre produzem o aviso e retorno vazio descritos nas instruções. O contrato é atendido apenas para parte dos erros.

**Correção recomendada:** validar contêineres, linhas, tamanhos e depois campos, nessa ordem. Acrescentar testes com None, números e linhas incompletas, sem depender apenas de valores numéricos fora da faixa.

<!-- PAGE BREAK -->

## 3. Achados documentais e de entrega

### A3. Links do PDF estão truncados — prioridade média

**Local:** gerar_relatorio_pdf.py, converter_inline; referências do PDF, página 10.

A expressão regular usa entidades HTML dentro de uma classe de caracteres. Isso faz caracteres como t, l e g encerrarem indevidamente a URL capturada. Para o endereço da NASA Science, o gerador produz um destino de link limitado a `https://science.nasa.`.

O problema foi confirmado nas anotações do PDF já salvo: os cinco links encontrados apontam para destinos truncados, como `https://www.compu` e `https://sma.nasa.`. O texto visual pode parecer completo, mas o clique não leva à fonte pretendida.

**Recomendação:** corrigir a expressão, regenerar o documento e conferir as URLs completas nas anotações do arquivo. A versão privada já possui essa correção.

### A4. Arquivo de exemplos não corresponde à versão atual — prioridade baixa

**Local:** exemplos_saida.txt.

O conteúdo não decodifica como UTF-8 e difere da execução atual de exemplos.py. O arquivo inclui saídas antigas, enquanto a execução atual produz onze cenários. Isso reduz a utilidade do arquivo como evidência reproduzível e pode corromper acentos em editores que assumem UTF-8.

**Recomendação:** regenerar com `python -X utf8 exemplos.py > exemplos_saida.txt` e comparar os bytes com uma nova execução. Evitar editar manualmente esse resultado.

### A5. Diagramas e conteúdo ESG precisam de reforço — prioridade média acadêmica

O relatório mostra a regra booleana por expressão e esquema ASCII, sem símbolos gráficos de portas. A lógica é verificável, mas uma figura com entradas, porta AND e saída atende de forma mais clara ao requisito visual do enunciado.

A reflexão ESG menciona proteção planetária, segurança e registros, mas trata pouco os critérios de escolha da área de pouso, gestão de água e resíduos, produção local e mecanismos de participação. O enunciado pede esses pontos explicitamente. A seção deve responder às perguntas com propostas identificadas como tais, sem atribuí-las ao código.

### A6. Identificação e apresentação final — prioridade baixa

A capa mantém um campo para preencher os integrantes. O gráfico matemático está na página 5 e a legenda aparece na página 6. As duas partes devem ser mantidas juntas para facilitar a leitura. As seções históricas existem, mas o texto sobre hardware pode explicar melhor custos concretos da implementação, em vez de apenas justificar a simplicidade.

<!-- PAGE BREAK -->

## 4. O que foi confirmado como correto

### Autorização

As 32 combinações de combustível suficiente, sensores, sistemas, atmosfera e área foram conferidas. Somente todas as condições verdadeiras autorizam o pouso. A função pode registrar vários motivos de bloqueio na mesma avaliação.

### Limites de combustível

Com massa de 1.000 kg, duração de cinco minutos, taxa de 0,002 e reserva de 2 kg, o consumo é 10 kg e o mínimo é 12 kg. Foram conferidos 11,999 kg, 12 kg, 15 kg e 15,001 kg: o primeiro é bloqueado; os dois intermediários são aptos e urgentes; o último é apto, sem urgência.

### Ordenação

Foram testadas as 120 permutações de cinco candidatos com atributos fixos, incluindo Médico com 13 kg e Laboratório com 12 kg. Todas chegaram à mesma sequência esperada: Laboratório, Médico, Energia, Habitação e Logística. A suíte original também confere estabilidade em empate completo e desempates por criticidade e prioridade.

Esse teste confirma o conjunto de candidatos e critérios utilizados. Não demonstra todas as combinações possíveis de massas, margens e eventos.

### Pousos, acidentes e dados

O caso sequencial conferido mantém dois pousos em dez minutos. Um módulo acidentado não volta a operacional por um simples evento de sistemas. Os testes fornecidos conferem preservação das entradas, unicidade, espera, consumo, dependências iniciais e consulta de pilha.

### Resultado consolidado da auditoria externa

| Grupo | Resultado |
|---|---|
| Tabela-verdade, fronteiras, permutações, acidente e sequência | 5 verificações aprovadas |
| Contêiner, linha de módulo e linha de evento malformados | 3 verificações reprovadas, relacionadas a A2 |
| Falha própria, dependência e falha ao fim da descida | 3 verificações reprovadas, relacionadas a A1 |
| Saída salva e URL integral | 2 verificações reprovadas, relacionadas a A4 e A3 |

Os resultados completos estão em evidencias.json; o script auditoria.py permite repetir a análise sobre a pasta de um clone. O script também carrega o gerador para conferir links, portanto utiliza as dependências documentais.

<!-- PAGE BREAK -->

## 5. Atendimento ao enunciado e às disciplinas

| Requisito | Situação na versão do Douglas |
|---|---|
| Módulos e atributos | Cinco tipos e atributos principais presentes |
| Fila, espera, pousados e alertas | Presentes; a fila de chegada é transitória, e a espera participa da priorização |
| Expressões e portas lógicas | Expressão correta; recomendável substituir ASCII por diagrama gráfico |
| Python, busca e ordenação | Implementados; falhas em validação e operação após eventos |
| Função matemática e análise | Fórmula, unidades, tabela e gráfico coerentes com o modelo declarado |
| História e hardware | Seções presentes; ampliar a ligação com custos concretos do código |
| ESG | Presente, mas incompleto nas perguntas específicas do enunciado |
| PDF de 5 a 10 páginas | Dez páginas, dentro do limite; links e legenda precisam de ajuste |
| Anexo de estruturas | Pode ser atendido pela seção 2; identificar explicitamente facilita a avaliação |

### Conferência pontual das apostilas

No capítulo 4, páginas físicas 36 e 37, foram confirmados vetores, pilha LIFO e fila FIFO em exemplos de C. No capítulo 5, página 17, foi confirmada busca linear; nas páginas 29 e 30, ordenação por inserção. Portanto, há correspondência conceitual com o protótipo. A implementação em listas Python adapta esses conceitos, sem equivaler literalmente à representação de um array ou lista encadeada em C.

A consulta não confirmou uma regra da FIAP proibindo append, dicionários ou classes. Essas restrições aparecem na suíte AST e nas convenções herdadas do projeto. Não devem ser apresentadas como obrigação da faculdade sem indicação explícita no material ou orientação do professor.

### Um detalhe importante de complexidade

O capítulo apresenta busca linear com melhor caso constante quando o primeiro elemento é encontrado. No código, porém, `range(quantidade(lista))` conta toda a lista antes da busca. Assim, mesmo encontrar a primeira posição exige uma travessia prévia. A ordem de crescimento dessa implementação permanece linear nesse caso.

Além disso, reconstruir listas por concatenações sucessivas pode gerar trabalho quadrático, pois cada inclusão copia elementos. Para poucos módulos isso pode ser aceitável como exercício, mas não sustenta uma afirmação de eficiência para hardware espacial. Essas observações são justificativas de projeto, não exigência de introduzir estruturas avançadas.

<!-- PAGE BREAK -->

## 6. Limites, comparação das versões e encaminhamento

### Simplificações legítimas, desde que declaradas

A descida é atômica, a espera em órbita não gasta combustível e os acidentes são indicados pelos cenários. A pilha serve para consultar registros em ordem inversa; retirar o topo não desfaz um pouso. O histórico fica em memória. O cadastro é editado em listas, sem interface gráfica. Essas decisões não são falhas por si só no escopo didático.

O arquivo main.py é um experimento antigo, separado do MGPEB atual. O ROADMAP contém propostas e anotações que não representam necessariamente o produto implementado. A apresentação deve explicar o programa atual sem incorporar verbalmente funcionalidades desses materiais históricos.

### Comparação de versões

| Aspecto | Douglas: cbaf4d0 | Cópia privada: 35798e8 |
|---|---|---|
| Testes e exemplos | 8 testes; 11 cenários | 17 testes; 14 cenários |
| Validação de contêineres | Pode lançar TypeError | Tipos conferidos antes da travessia |
| Falhas na base | Estado pode permanecer operacional | Suspensão e recuperação por saúde e dependências |
| Diagrama | Esquema textual | Figura vetorial AND/NOT |
| Referências no PDF | Links truncados | Links corrigidos |
| Partes 5 e 6 | Conteúdo anterior resumido | Conteúdo ampliado e integrado |
| Guia de estudo | Ausente | Guia detalhado separado, com 13 páginas |

### Ordem recomendada de trabalho

1. Resolver A1 e A2 e acrescentar testes que reproduzam as falhas.
2. Corrigir os links e regenerar a saída dos exemplos.
3. Completar o diagrama e a reflexão ESG, vinculando texto e implementação.
4. Preencher integrantes, manter gráfico e legenda juntos e conferir o PDF final.
5. Se a equipe optar por aproveitar a versão privada, revisar suas mudanças antes de incorporá-las ao repositório coletivo.

Esta revisão não publicou mudanças no repositório do Douglas. A identificação explícita dos commits evita atribuir a ele correções que existem somente na cópia privada. A revisão é válida para o commit auditado; uma atualização posterior requer conferir o novo conteúdo.

### Materiais salvos no OneDrive

A pasta de relatórios contém esta revisão, suas evidências, o relatório técnico e o guia da cópia privada, além de uma cópia do PDF original do Douglas para comparação. Os nomes indicam a origem e o commit de cada versão. Os arquivos locais foram copiados e verificados; a disponibilidade no OneDrive web depende da sincronização do aplicativo.
