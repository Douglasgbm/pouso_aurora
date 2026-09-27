Atividade Integradora: Módulo de Gerenciamento de Pouso e Estabilização de Base (MGPEB)
Requisitos da Equipe
Cada equipe deverá:

01. Modelar o cenário de pouso e fila de módulos

Definir um conjunto de módulos de pouso (ex: habitação, energia, laboratório científico, logística e suporte médico);
Descrever atributos básicos para cada módulo: prioridade de pouso, nível de combustível, massa, criticidade da carga e horário estimado de chegada à órbita;
Organizar os módulos em estruturas de dados lineares: uma fila (queue) principal para autorização de pouso e listas auxiliares para módulos já pousados, em espera ou em alerta.

02. Definir e representar regras de decisão usando portas lógicas

Especificar condições críticas para autorizar ou bloquear o pouso (combustível, condições atmosféricas, disponibilidade da área e integridade dos sensores);
Traduzir essas condições em expressões booleanas e representá-las via diagramas de portas lógicas (AND, OR, NOT, etc.), detalhando o processo de decisão do sistema.

03. Implementar, em Python, um protótipo do MGPEB
Desenvolver um script em Python que:

Cadastre os módulos definidos pela equipe em estruturas lineares (listas, filas e pilhas);
Implemente algoritmos de busca para localizar rapidamente módulos com determinada característica (por exemplo: menor combustível, maior prioridade e determinado tipo de carga);
Aplique algoritmos de ordenação para reorganizar a fila de pouso conforme os critérios escolhidos;
Simule a autorização de pouso com base nas regras lógicas definidas, utilizando estruturas condicionais (IF, ELIF e ELSE) que reflitam as funções booleanas modeladas anteriormente.
O código deve ser simples, bem comentado e coerente com os conteúdos vistos até o momento, sem utilização de bibliotecas avançadas além das necessárias para entrada, saída e manipulação básica de dados.

04. Modelar funções matemáticas aplicadas ao pouso ou estabilização da base
Escolha do Fenômeno: Escolher pelo menos um fenômeno físico ou operacional relevante para o pouso ou para a estabilização da base (ex: altura em função do tempo de descida, variação da temperatura externa com o tempo, consumo de combustível em função da velocidade ou geração de energia solar ao longo do dia);
Representação Matemática: Representar esse fenômeno por meio de funções matemáticas compatíveis com o conteúdo da disciplina (função linear, quadrática, exponencial etc.), indicando a fórmula utilizada, o significado dos parâmetros e uma análise qualitativa do gráfico (incluindo o que acontece quando as variáveis aumentam ou diminuem);
Relação com a Engenharia: Relacionar essa modelagem às decisões de engenharia do MGPEB, argumentando, por exemplo, como a função auxilia na definição do melhor momento para acionar retrofoguetes, abrir paraquedas ou limitar a quantidade de módulos pousando ao mesmo tempo.

05. Contextualizar o MGPEB à luz da evolução da computação
Histórico e Evolução: Produzir uma seção textual relacionando o sistema projetado com a história e evolução dos computadores, destacando como os primeiros computadores de propósito geral abriram caminho para sistemas embarcados de alta confiabilidade;
Limitações de Hardware: Analisar quais limitações de hardware seriam típicas de uma missão em Marte (memória, processamento, consumo de energia, tolerância à radiação etc.);
Impacto nas Escolhas Técnicas: Discutir de que forma essas limitações influenciam as escolhas de algoritmos, estruturas de dados e estratégias de programação adotadas pela equipe.
Objetivos de Aprendizagem do PBL
Ao concluir o PBL, o aluno deverá ser capaz de:

Integração de Conhecimentos: Compreender e explicar, em linguagem técnica, como o processo de pouso de uma missão interplanetária exige a integração de múltiplas camadas de ciência da computação e áreas correlatas.
Lógica e Implementação: Reconhecer o papel das portas lógicas e funções booleanas na definição de regras de decisão embarcadas, relacionando-as à implementação de algoritmos em Python (condições, laços e funções).
Domínio de DSA: Demonstrar domínio prático no uso de estruturas lineares e algoritmos básicos de busca e ordenação para organizar dados de telemetria, módulos de pouso, alarmes e recursos, justificando as escolhas por critérios de desempenho e clareza.
Modelagem Matemática: Construir e analisar modelos de funções matemáticas aplicadas a fenômenos da missão, interpretando gráficos e conectando resultados a decisões de engenharia (estimativas de tempo, energia ou risco operacional).
Visão de Hardware e Governança: Desenvolver uma visão crítica sobre as arquiteturas de hardware que tornam esse tipo de sistema possível e incorporar princípios ESG à concepção de soluções tecnológicas.

Entregáveis da Fase 2

01. Relatório técnico em PDF (5 a 10 páginas), contendo:

Descrição do cenário de pouso e dos módulos definidos;
Diagrama(s) de portas lógicas com as principais regras de decisão;
Modelagem das funções matemáticas escolhidas, com explicações e análises;
Seção de contextualização histórica/arquitetural do sistema;
Seção de reflexão sobre ESG e governança na base Aurora Siger.

02. Código fonte em Python (.py):

Protótipo do MGPEB organizado, comentado e executável com exemplos simples.

03. Anexo de estruturas de dados:

Descrição de como listas, filas e pilhas foram utilizadas no projeto, com exemplos concretos 
(pode ser parte do relatório).
