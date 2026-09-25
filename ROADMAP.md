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




-------------------------------------------------------------------------------------------

## Definições Técnicas - Fase 2 (Lógica de Pouso e Priorização)

### 0. Premissa da Missão (decidida em 24/09/2026)

A **nave mãe permanece em órbita** durante toda a operação. Os módulos descem sozinhos, sem
piloto e sem controle remoto, e **não retornam** — são descartáveis por projeto.

**Por que a nave mãe não desce:** o combustível da volta teria que ser carregado na descida e
erguido de novo, e cada quilo de combustível extra exige mais combustível para ser freado. Sair
da superfície de Marte até a órbita custa cerca de **4 km/s** de Δv (contra ~9,4 km/s na Terra,
já que Marte tem 38% da nossa gravidade e quase nenhuma atmosfera). A arquitetura padrão —
a mesma escolhida no programa Apollo nos anos 60, no debate do *rendezvous* em órbita — separa
o que desce do que leva a tripulação para casa.

**Por que os módulos são autônomos:** nos 7 minutos da descida, o sinal de rádio demora mais do
que isso para ir e voltar da Terra. Não existe piloto, não existe "abortar por comando" — o
módulo decide sozinho, embarcado. **É essa a razão de existir do MGPEB: ele não assessora um
operador humano, ele é o operador.**

**Tripulação:** desce em missão posterior, depois que os seis módulos estiverem no solo e
operacionais. Por isso nenhum módulo desta fase é tripulado.

### 1. Métricas dos Módulos (Dados de Simulação)
Para a implementação do algoritmo de fila e priorização, foram definidos os seguintes parâmetros para cada módulo:

| Módulo | Prioridade | Comb. de descida | Energia | Massa (kg) | Criticidade | ETA (min) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Veículo de Subida (MAV)** | 1 | 75% | 90% | 18.000 | 4/5 | T+0 |
| **Energia** | 2 | 70% | 85% | 10.000 | 5/5 | T+10 |
| **Logística** | 3 | 40% | 70% | 12.000 | 3/5 | T+5 |
| **Habitação** | 4 | 80% | 95% | 15.000 | 5/5 | T+0 |
| **Suporte Médico** | 5 | 60% | 80% | 5.000 | 4/5 | T+20 |
| **Laboratório** | 6 | 90% | 60% | 7.000 | 2/5 | T+50 |

*Nota: O Módulo de Logística possui combustível reduzido para exercitar a faixa "urgente" no
código, e chega antes da Energia de propósito — é o que faz a regra de emergência furar uma
prioridade melhor que a dela. Ver a seção 2.3.*

**Duas colunas novas em relação à primeira versão:**

- **Energia** (bateria): combustível e energia elétrica são coisas diferentes. Combustível
  *freia e move*; energia faz o módulo *pensar e agir* — é ela que aciona o mecanismo do
  paraquedas e as válvulas dos retrofoguetes. Bateria morta no meio da descida significa que
  nada é acionado, mesmo com o tanque cheio.
- **ETA em minutos**: toda unidade de tempo do projeto é minuto. O ROADMAP antes misturava
  horas no ETA com minutos no ciclo de operação, e essa mistura é bug garantido.

#### 1.1 A prioridade foi redefinida (decisão de 24/09/2026)

Na primeira versão, `prioridade + criticidade = 6` em **todos** os módulos — as duas colunas
eram o mesmo ranking escrito em escalas invertidas, e uma delas não acrescentava informação
nenhuma ao algoritmo. Foram separadas:

- **Criticidade** responde *"o que a missão perde se este módulo for destruído?"* (consequência)
- **Prioridade** responde *"em que ordem o solo precisa recebê-los?"* (sequência)

E a sequência é decidida por **dependência**, não por valor: não é "quem vale mais", é "quem
precisa estar no chão para que o próximo faça sentido".

| Ordem | Módulo | Justificativa da posição |
| :---: | :--- | :--- |
| 1º | **MAV** | É o item de **maior prazo**: ele fabrica o próprio combustível a partir do CO₂ da atmosfera marciana, e a planta leva **meses** enchendo os tanques. A tripulação não pode nem sair da Terra antes dos tanques estarem cheios e confirmados — então ele trava todo o resto. A Energia chega 25 min depois, muito antes de a planta precisar dela. |
| 2º | **Energia** | Tudo depende dela. O próprio README já dizia: *"sem energia, o Habitat não liga o oxigênio"*. Um habitat sem energia é uma caixa de metal fechada. |
| 3º | **Logística** | Traz ferramenta e peça para conectar a energia aos demais módulos. Precisa estar no solo **antes** de haver trabalho a fazer. |
| 4º | **Habitação** | Depende de energia ligada e de ferramenta disponível para ser comissionada. |
| 5º | **Suporte Médico** | Só passa a ser necessário quando houver gente na base — e a tripulação desce em missão posterior. |
| 6º | **Laboratório** | É o objetivo científico da missão, mas nada depende dele. Último. |

**Prova de que a separação funcionou:** as somas agora são 7, 7, 6, 9, 9, 8 (antes eram 6 em
todas as linhas). O caso mais eloquente é a **Logística**: criticidade **baixa** (3) e prioridade
**alta** (3ª de seis) — perder a Logística não mata ninguém, mas ela precisa chegar cedo. Esse
par "pouco crítico, muito urgente na sequência" era **invisível** no modelo antigo, e é o melhor
argumento para justificar a existência das duas colunas.

#### 1.2 Combustível de descida × tanque de subida (duas variáveis diferentes)

O MAV obrigou a renomear uma coluna e criar outra:

| Variável | O que mede | Participa da autorização de pouso? |
| :--- | :--- | :---: |
| **Combustível de descida** | Margem para os retrofoguetes frearem a descida. É o que sempre esteve na tabela — a regra dos 20% sempre falou disto. | **Sim** (é o sinal C) |
| **Tanque de subida** (só do MAV) | Percentual de enchimento da planta de ISRU, que fabrica propelente a partir do CO₂ marciano. Enche ao longo de **meses**, já no solo. | **Não** |

O tanque de subida **não entra na lógica de pouso** — ele é um estado *pós-pouso*. O que ele
controla é outra coisa, fora do escopo desta fase: a **autorização de partida da tripulação da
Terra**. Sem renomear, alguém leria "MAV: tanque vazio" e concluiria que ele deve abortar a
descida, quando na verdade ele pousa com os tanques de subida vazios **por projeto**.

#### 1.3 Valores do MAV (decidido em 25/09/2026)

A criticidade do MAV era a última pergunta em aberto da tabela. **Resposta: 4/5.**

Perdê-lo *antes* de a tripulação sair da Terra adia a missão em **uma janela de lançamento
(~26 meses)** — custo enorme, mas **sem mortes**. Ele não é 5/5 justamente porque existe a
regra de só lançar a tripulação com os tanques de subida confirmados cheios; essa regra existe
*para* rebaixar o risco dele. Energia e Habitação são 5/5 porque a falha delas mata gente com a
base já ocupada.

⚠️ **Correção de um erro da seção 1.1:** aquele texto afirma que as somas de
`prioridade + criticidade` são "7, 7, 6, 9, 9, 8". Os cinco últimos números estão certos, mas o
primeiro é do MAV — cuja criticidade ainda não tinha sido decidida quando a frase foi escrita.
Além disso, soma 7 com prioridade 1 exigiria criticidade **6**, que não existe numa escala de
1 a 5. Com o MAV em 4/5, a sequência correta é **5, 7, 6, 9, 9, 8** — cinco valores distintos,
e o argumento original (as colunas não são redundantes) continua de pé.

### 2. Lógica de Autorização de Pouso (Portas Lógicas)
O pouso só é autorizado se todas as condições críticas forem verdadeiras (Lógica AND).

**Variáveis de Entrada:**
- **C (Combustível):** Nível suficiente para a descida (**≥ 20%** — ver as faixas em 2.1).
- **A (Atmosfera):** Condições climáticas estáveis (sem tempestades).
- **D (Disponibilidade):** Área de pouso livre de outros módulos.
- **S (Sensores):** Integridade dos sistemas de radar e navegação.
- **T (Terreno):** Coordenada de pouso validada como plana e segura.
- **$\theta$ (Ângulo):** Ângulo de entrada na atmosfera dentro da janela de segurança ($12^\circ$ a $15^\circ$).

**Sinais acrescentados em 25/09/2026:**
- **E (Energia elétrica):** bateria suficiente para acionar paraquedas e retrofoguetes (≥ 30%).
- **P (Paraquedas):** mecanismo de abertura operacional.
- **I (Integridade estrutural):** casco sem trinca — a entrada atmosférica castiga a estrutura.
- **ETA:** o módulo já chegou à órbita. É **pré-condição**, não critério de desempate (ver 2.3).

**Expressão Booleana (oficial):**
`Autorização = ETA AND C AND E AND A AND D AND S AND T AND θ AND P AND I`

São dez sinais ligados por AND: **uma única falha bloqueia o pouso**. No código
(`scripts/mgpeb.py`, seção 7) isso é literalmente um `all()` sobre as dez portas.

#### 2.0.1 Cada porta devolve DUAS coisas, não uma

Uma porta não responde só "passou / não passou". Ela responde também **se a causa da falha é
recuperável ou definitiva** — e é a segunda resposta que decide para qual lista o módulo vai:

| Porta | Se falhar, a causa é | Por quê |
| :---: | :--- | :--- |
| ETA | recuperável | é só esperar |
| A | recuperável | tempestade passa |
| D | recuperável | a zona é limpa em 18 min |
| T | recuperável | o alvo pode ser deslocado (custa 3% de combustível) |
| θ | recuperável | queima de ajuste corrige (custa 5% de combustível) |
| C | **definitiva** | combustível só diminui; esperar piora |
| E | **definitiva** | a bateria só descarrega enquanto não há rede |
| S | **definitiva** | não há quem conserte um radar em Marte |
| P | **definitiva** | mecânico, não se conserta em voo |
| I | **definitiva** | idem |

**Basta uma causa definitiva** para mandar o módulo ao alerta, mesmo que todas as outras falhas
sejam temporárias. Sem essa distinção, as listas "em espera" e "em alerta" que o enunciado exige
seriam a mesma coisa com dois nomes, e a fila não teria motivo para ser recalculada.

#### 2.0.2 O mundo e o MGPEB são metades separadas

O programa tem duas metades que **não se misturam**:

```
   O MUNDO (Marte)                    O MGPEB (computador de bordo)
   ---------------                    -----------------------------
   decide se tem tempestade    --->   lê "tempestade: sim"
   decide se o sensor falhou   --->   lê "sensor: falha"
                                      E ENTÃO DECIDE: pousa ou não.
```

Um sistema embarcado **não escolhe o clima** — ele sofre o clima e lê o sensor. O "não existe
fator humano" do projeto vale para a **decisão** (ninguém autoriza o pouso), não para os
**dados** (o módulo não inventa o que o sensor mede). Se as metades se misturarem, o programa
vira juiz e réu, e fica impossível forçar um cenário para testar.

O sorteio usa **semente fixa (23)**, para que a saída colada no relatório seja reproduzível. O
gerador foi aferido em 20.000 mundos e respeita as probabilidades declaradas (medido 5,01% /
3,03% / 4,08% contra 5% / 3% / 4% de falha de sensor, paraquedas e estrutura), com média de
0,73 falha de hardware por missão.

### 2.1 As Três Faixas de Combustível (decidido em 24/09/2026)

O combustível responde a **duas perguntas diferentes**, e misturá-las foi o que gerou a
contradição entre os 20% do código e os 50% do README:

| Pergunta | Natureza | O que produz |
| :--- | :--- | :--- |
| **1. O módulo PODE pousar?** | Segurança — **elimina** | Um booleano (o AND acima) |
| **2. Entre os que podem, QUEM VAI PRIMEIRO?** | Operação — **enfileira** | Uma posição na fila |

```
  0% ---------- 20% ---------- 50% ---------- 100%
   |   ABORTA     |   URGENTE    |    NORMAL     |
   |              |              |               |
   pergunta 1     pergunta 2     pergunta 2
```

| Faixa | Condição | Efeito |
| :--- | :---: | :--- |
| **Aborto** | `combustível < 20%` | **Não autorizado.** `C = False`. Sai da fila e vai para a lista de **alerta**. |
| **Urgente** | `20% ≤ combustível < 50%` | Autorizado, mas **fura a fila** (emergência de combustível). |
| **Normal** | `combustível ≥ 50%` | Autorizado, entra na ordem normal por prioridade. |

**Justificativa dos cortes:** abaixo de 20% não há margem para os retrofoguetes frearem a
descida (aborta-se para não perder a nave no solo); entre 20% e 50% ainda dá para pousar, mas
o módulo não sobrevive a mais uma volta de órbita — por isso ele passa na frente.

### 2.2 Regra de Ordenação da Fila (decidido em 24/09/2026)

Critério de ordenação em **dois níveis, com desempate**:

| Nível | Critério | Regra |
| :---: | :--- | :--- |
| 1º | **Faixa de combustível** | Todo módulo **urgente** vem antes de todo módulo **normal**. |
| 2º | **Prioridade** | Dentro da mesma faixa, prioridade **menor** primeiro (1 é a máxima). |
| Desempate | **ETA** | Empate na prioridade: desce quem chega antes à janela de órbita. |

**Analogia que sustenta a regra:** num aeroporto, o avião que declara emergência de
combustível fura a fila inteira, mas os demais continuam pousando na ordem normal entre si.

**Princípio:** *importância não é urgência*. Adiar a Habitação significa **esperar**; adiar um
módulo sem combustível significa **perder** o módulo.

⚠️ Com as prioridades todas distintas (1 a 6), **o desempate por ETA nunca dispara**. Ele
continua na regra como critério de reserva, para o caso de dois módulos empatarem no futuro.

### 2.3 O ETA é PRÉ-CONDIÇÃO, não desempate (decidido em 25/09/2026)

Na primeira versão da regra 2.2, o ETA aparecia como **critério de desempate** — ou seja, como
uma *preferência*: "empatou, eu escolho quem chegou antes". Isso é erro de categoria, e é o
terceiro da mesma família no projeto:

1. O combustível respondia a duas perguntas (resolvido em 24/09);
2. Prioridade e criticidade eram a mesma coluna (resolvido em 24/09);
3. **O ETA estava classificado como preferência quando é restrição física.**

Chegar não é preferência. Um módulo **não pode** pousar antes de existir na janela de órbita, do
mesmo jeito que não pode pousar sem combustível. O ETA pertence ao **AND da autorização**, junto
com C, A, D, S, T e θ. O próprio enunciado resolve a dúvida ao pedir *"horário estimado de
chegada **à órbita**"*: os módulos vêm da Terra em lançamentos separados (são 67 toneladas, não
cabem num foguete só) e chegam em momentos diferentes.

**Por que os valores de ETA foram apertados.** Os ETAs originais (0, 30, 120, 240, 360 min)
espalhavam as chegadas por 6 horas contra um ciclo de operação de 25 minutos. Simulando a fila
com eles, **em 5 dos 6 pousos havia um único candidato disponível** — não havia o que ordenar, e
o ciclo ficava ocioso por até 95 minutos seguidos. Pior: a Logística, único módulo na faixa
urgente e razão de existir da regra "fura a fila", chegava em T+4h **sem ninguém para furar**.
Um cenário que não exercita as próprias regras não prova nada. Os novos valores (0, 5, 10, 20,
50) põem vários módulos disputando a mesma vaga.

**Fila resultante — o que a simulação produziu de fato:**

```
t=  0 min | tempestade de areia bloqueia todos     -> ocioso 5 min
t=  5 min | Logística[URGENTE/p3], MAV[p1], Habitação[p4]
          | POUSA Logística  <== FUROU A FILA
t= 30 min | MAV[p1], Energia[p2], Habitação[p4]    -> POUSA MAV
t= 55 min | Energia[p2], Habitação[p4], Lab[p6]    -> POUSA Energia
t= 80 min | Habitação[p4], Laboratório[p6]         -> POUSA Habitação
t=105 min | Laboratório[p6]                        -> POUSA Laboratório
```

| | ordem |
| :--- | :--- |
| **do manual** (prioridade) | MAV → Energia → Logística → Habitação |
| **decidida pelo algoritmo** | MAV → **Logística** → Energia → Habitação |

As duas divergem, e é essa divergência que justifica a existência do algoritmo. Com os ETAs
antigos elas eram **idênticas** — a fila dinâmica devolvia exatamente o que a ordem do manual já
dizia, e todo o mecanismo era decorativo.

### 2.4 A quebra da cadeia de dependência, justificada (25/09/2026)

A seção 2.2 deixou em aberto: a regra de emergência faz a Logística pousar antes da Energia,
quebrando a cadeia de dependência. Isso é aceitável? **Sim, e o motivo é preciso:**

> A cadeia de dependência é sobre **ordem de comissionamento** — a ordem em que os módulos são
> *ligados e conectados*. Não é sobre ordem de **pouso**. Nada é comissionado durante a fase de
> pouso: os seis descem numa tarde e ficam parados no solo, e a tripulação só chega meses depois.
> Logo, pousar a Logística antes da Energia **não custa nada**.
>
> A única dependência que é de fato um **prazo** é a do **MAV**: a planta de propelente leva
> meses enchendo, e o relógio dela só começa quando ele toca o solo. Essa não pode ser furada.

Resultado: **cinco das seis prioridades são preferências baratas de romper; uma é um prazo real.**
O algoritmo pode furar a fila à vontade, menos com o MAV.

Isso deixou de ser afirmação e virou demonstração na Camada 5 (seção 7): lá a cadeia **não** pode
ser furada, e o programa mostra a Habitação descarregando a bateria até a rede elétrica existir.

### 3. Parâmetros de Tempo e Astrodinâmica
- **Tempo de Descida (EDL):** Aproximadamente **7 minutos** — os "sete minutos de terror" das
  missões reais da NASA: o intervalo entre o topo da atmosfera e o solo, em que a sonda age
  sozinha porque o sinal de rádio demora mais que isso para ir e voltar da Terra.
- **Ciclo de Operação:** **25 minutos por módulo** = 7 min de descida + 18 min de intervalo de
  segurança para limpeza da zona de pouso. ⚠️ Não confundir os dois números: a **descida** dura
  7 min, mas o próximo módulo só pode começar a sua depois de 25 min.
- **Consequência para a fila:** o 5º módulo da fila espera **100 minutos** em órbita — e é
  esperando que ele queima combustível (ver seção 5).
- **Janela de Órbita:** O pouso depende da posição da nave mãe em relação ao alvo; a perda da janela implica em nova órbita completa.

### 4. Sistema de Coordenadas e Local de Pouso
O sistema utiliza coordenadas cartesianas (X, Y) para mapear a zona de pouso.
- **Alvo Central:** (100, 100).
- **Validação de Terreno:** O sistema cruza a coordenada de descida com uma matriz de riscos (obstáculos como crateras e pedras). Se a coordenada coincidir com um obstáculo, a variável **T** torna-se `False`, bloqueando o pouso.

### 5. Fenômeno Escolhido para a Modelagem Matemática (item 04 do enunciado)

**Fenômeno:** *combustível restante em função do tempo de espera em órbita.*

Ele apareceu sozinho durante o debate da fila: a ordem de pouso importa porque **cada módulo
queima combustível enquanto espera a sua vez**. Com o ciclo de 25 min por módulo, o 5º da fila
espera 100 minutos — e chega na hora da descida com menos combustível do que tinha quando a
fila foi montada.

Por que esse fenômeno é bom para o trabalho:
- Liga direto na decisão de engenharia: permite responder *"a partir de que minuto o módulo X
  cai na faixa de aborto (< 20%)?"* — ou seja, qual é o **prazo máximo** da fila.
- Explica por que a fila precisa ser **reordenada**, e não calculada uma vez só.
- Dá um gráfico decrescente, com análise qualitativa fácil de defender.

**DECIDIDO em 25/09/2026: são TRÊS funções, em três formas diferentes.**

O enunciado pede "pelo menos um fenômeno". O projeto acabou com três, cada um de uma fase
diferente da missão — e, por natureza, cada um numa forma matemática diferente:

| # | Fase | Fenômeno | Forma | Onde no código |
| :---: | :--- | :--- | :--- | :--- |
| 1 | espera em órbita | combustível × tempo | **linear** | seção 9 |
| 2 | frenagem (7 min) | altura × tempo | **quadrática** | seção 17 |
| 3 | no solo | geração solar × hora | **periódica** | seção 20 |

**Função 1 — linear.** `C(t) = C₀ − k·t`, com k = 0,08 %/min.
Forma linear porque o módulo em espera está apenas mantendo atitude e sistemas ligados: o gasto
por minuto é constante, **não depende de quanto ainda resta no tanque**. (Se dependesse, a forma
correta seria exponencial — e é por isso que a exponencial foi descartada.)
*Análise:* reta decrescente de coeficiente angular −k. Como ela cruza o patamar dos 20%, existe
um **minuto limite** a partir do qual o módulo deixa de poder pousar: `minuto_limite()` resolve
`C₀ − k·t = 20`. É o prazo da fila. A Logística aguenta 250 min de espera; o Laboratório, 762.

**Função 2 — quadrática.** `h(t) = h₀ − v₀·t + ½·a·t²`.
Forma quadrática porque o empuxo dos retrofoguetes é constante, logo a desaceleração é constante,
logo a posição varia com o **quadrado** do tempo.
*Análise:* parábola com concavidade **para cima**. O módulo desce cada vez mais devagar até o
vértice, onde v = 0. **Projetar o pouso é fazer o vértice da parábola coincidir com o solo** —
vértice acima, o módulo para no ar e desperdiça combustível; vértice abaixo, ele chega ao solo
ainda em movimento. Daí saem a altura de ignição `h₀ = v₀²/(2a)` e o tempo de queima `t = v₀/a`.

**Função 3 — periódica.** `P(h) = P_max · sen(π·h/T)` durante o dia, 0 à noite.
O painel gera em função do ângulo do Sol sobre o horizonte: zero ao nascer, máximo ao meio-dia,
zero ao pôr do sol.
*Alternativa sem trigonometria:* `P(h) = P_max · 4h(T−h)/T²`, uma parábola que vale 0 nas pontas
e exatamente P_max no meio-dia. As duas curvas diferem no máximo **5,2%**, e a parábola entrega
4,5% mais energia no total do dia. As duas estão implementadas (`comparar_curvas_solares()`).
*Análise:* metade do sol é noite, com geração **nula** — e é por isso que a bateria existe: ela
atravessa a noite. Se o consumo diário passar da geração diária, o saldo é negativo e existe um
prazo, exatamente como na função 1.

### 6. A Descida — os sete minutos (definido em 25/09/2026)

Até a Camada 3 o pouso era um booleano: autorizado ou não. Na Camada 4 ele **acontece**, em
**três estágios de freio**, cada um entregando ao próximo:

| Estágio | Mecanismo | De → para | O que decide |
| :---: | :--- | :--- | :--- |
| 1 | atmosfera (escudo térmico) | 125 km, 5.400 m/s → 11 km | o **ângulo** de entrada |
| 2 | paraquedas | 11 km → altura de ignição | limite de 470 m/s (acima, rasga) |
| 3 | retrofoguetes | ignição → solo, 0 m/s | a **massa** e o **combustível** |

**Por que o estágio 3 é obrigatório em Marte:** a atmosfera de lá tem menos de 1% da densidade
da Terra. Mesmo com o paraquedas aberto, o módulo ainda cai a ~100 m/s (360 km/h) — queda mortal.
Os últimos metros são freados **a foguete**. É exatamente para isso que serve o combustível de
descida; ele não é "combustível para voar", é o **estágio 3 do freio**. A regra dos 20% ganha
significado físico aqui.

**Por que a janela de ângulo tem os dois lados:** fechado demais, o calor e a força G destroem o
módulo; aberto demais, ele quica na atmosfera e volta para o espaço. E há um terceiro efeito, que
fecha o teto da janela: entrada mais fechada significa menos tempo freando na atmosfera, logo
chegada mais rápida aos 11 km — acima de 15° a velocidade passa do limite e **o paraquedas
rasga**.

#### 6.1 A massa finalmente decide alguma coisa

Este era um item em aberto: *"massa não é usada por nenhum algoritmo"*. Resolvido, e não por
decreto — saiu da física:

```
a = (empuxo / massa) − gravidade
```

Os retrofoguetes precisam **primeiro anular o peso**; só o que sobra freia de fato. Daí sai a
cadeia inteira: **mais pesado → desacelera menos → aciona mais alto → queima mais tempo → gasta
mais combustível**.

| Módulo | Massa | Desaceleração | Aciona a | Queima | Gasta |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Suporte Médico | 5.000 kg | 20,29 m/s² | 246 m | 4,9 s | 5,9% |
| Laboratório | 7.000 kg | 13,43 m/s² | 372 m | 7,4 s | 8,9% |
| Energia | 10.000 kg | 8,29 m/s² | 603 m | 12,1 s | 14,5% |
| Logística | 12.000 kg | 6,29 m/s² | 795 m | 15,9 s | 19,1% |
| Habitação | 15.000 kg | 4,29 m/s² | 1.166 m | 23,3 s | 28,0% |
| MAV | 18.000 kg | 2,96 m/s² | 1.691 m | 33,8 s | 40,6% |

#### 6.2 ACHADO: a regra fixa dos 20% é insegura

A coluna "Gasta" acima **contradiz a porta C**. Ela usa 20% para todos os módulos, mas o valor
real exigido vai de 5,9% a 40,6%. A regra erra **nos dois sentidos**:

- **Frouxa para os pesados:** autoriza o MAV com 25% (25 > 20) e ele **cai**, porque frear
  18 toneladas exige 40,6%.
- **Rigorosa para os leves:** rejeitaria o Suporte Médico com 19% quando ele só precisa de 5,9%.

Isso não é hipótese: está provado por `teste_regra_fixa_de_20_por_cento_e_insegura()`.

**Solução adotada — arquitetura de dois estágios**, que é o que sistemas embarcados reais fazem:

1. **Filtro barato** — a porta C, corte fixo de 20%, aplicada a *todos* os módulos a *cada*
   ciclo. Uma comparação.
2. **Checagem cara** — `combustivel_minimo_real()`, que resolve a física da frenagem, aplicada
   *só* ao candidato escolhido, *só* quando ele vai descer.

A porta C **não foi alterada**. Ela continua sendo o que era, e passa a ser honestamente o que
é: uma aproximação rápida, não uma garantia.

### 7. Estabilização da Base (definido em 25/09/2026)

O projeto se chama "Módulo de Gerenciamento de Pouso **e Estabilização de Base**". Até 25/09 a
segunda metade do nome não existia em lugar nenhum — nem aqui, nem no README, nem no código.

**Tempo:** a convenção de minutos foi **mantida**. O programa conta tudo em minutos por dentro;
o "sol" (o dia marciano, 24h39min = 1479,6 min) é só **rótulo de exibição**. Guardar numa unidade
única e converter na hora de exibir é o que evita somar horas com minutos.

#### 7.1 Dano do pouso vem da desaceleração

O dano não vem da sobra de combustível — ela não tem ligação física com o estresse estrutural.
Quem castiga a estrutura é a **força G**, e ela já está calculada na seção 6.1.

Isso produz uma **inversão útil para o relatório**: os módulos **leves freiam muito mais forte**
(Laboratório a 13,43 m/s² contra o MAV a 2,96) e sofrem mais dano, **mesmo gastando menos
combustível**. É um trade-off real de engenharia, saído da conta e não de uma escolha de projeto.

#### 7.2 Energia no solo: a função 3 decidindo algo

| Módulo | Gera/sol | Consome/sol | Saldo | Autonomia sem rede |
| :--- | ---: | ---: | ---: | :--- |
| MAV | 15,0% | 6,0% | +9,0% | indefinida |
| Logística | 10,0% | 3,0% | +7,0% | indefinida |
| Energia | 8,3% | 5,0% | +3,3% | indefinida |
| Habitação | 12,5% | 15,0% | **−2,5%** | **35 sols** |
| Laboratório | 5,8% | 8,0% | **−2,2%** | **25 sols** |

A Habitação é o maior consumidor (suporte à vida em espera) e **não se sustenta sozinha**. Ela
tem 35 sols de autonomia — e é isso que dá urgência real ao comissionamento da Energia.

#### 7.3 Comissionamento: aqui a cadeia de dependência NÃO pode ser furada

Durante o pouso, furar a ordem não custava nada (seção 2.4). Aqui custa: um módulo não pode ser
comissionado antes das suas dependências.

| Módulo | Depende de | Sols de trabalho | Ficou pronto |
| :--- | :--- | :---: | :---: |
| Logística | — | 1 | sol 1 |
| Energia | — | 3 (+1 por dano leve) | sol 4 |
| MAV | Energia | 2 | sol 6 |
| Habitação | Energia, Logística | 5 | sol 9 |
| Laboratório | Energia | 4 (+1 por dano leve) | sol 9 |

#### 7.4 O tanque de subida sai do papel

Era o último campo morto do cadastro (a massa era o outro, resolvida em 6.1). A planta de ISRU
fabrica o propelente de retorno a partir do CO₂ marciano, mas precisa de energia elétrica — então
só começa depois da rede existir.

```
começa no sol 6  ->  0,25% por sol  ->  400 sols  ->  tanque cheio no sol 406 (~13,7 meses)
```

**É essa data que libera a partida da tripulação da Terra** — ninguém sai de casa antes de o
transporte de volta estar confirmado cheio. E é por isso que o MAV é prioridade 1: não por valer
mais, mas por ter o **maior prazo**.

### 8. Defeitos encontrados rodando o código (registro)

Os dois defeitos abaixo **passaram no cenário feliz** e só apareceram quando a camada rodou de
verdade. Ambos estão trancados por teste.

**8.1 — A tempestade que abandonava a missão.** Quando ninguém estava pronto, o laço adiantava o
relógio até a próxima *chegada* e, se não houvesse nenhuma, encerrava com `break`. Isso assume que
a única razão para ninguém estar pronto é "ainda não chegou". Mas a razão pode ser **tempestade de
areia** — e aí, com todos os módulos já em órbita, cinco módulos sadios eram descartados por um
evento que passa em minutos. Provado por regressão: com o defeito, 1 de 6 pousaram; corrigido,
6 de 6.

**8.2 — Atualização sequencial onde deveria ser simultânea.** O comissionamento consultava a lista
de comissionados *viva* dentro do laço, então um módulo processado depois no mesmo sol enxergava
uma dependência recém-concluída e já começava a contar, enquanto um processado antes não enxergava.
Resultado: **a resposta mudava conforme a ordem da lista** (invertendo a lista, o MAV ficava pronto
no sol 5 em vez do 6). Um sol é um instante de decisão: todos precisam ver o mesmo estado.

### 9. Pontos em Aberto (checklist)

**Decisões de modelagem:**
- [x] ~~Prioridade × Criticidade redundantes~~ — 24/09, seção 1.1.
- [x] ~~Definir os valores do MAV~~ — 25/09, seção 1.3. Criticidade **4/5**.
- [x] ~~A coluna ETA ficou incoerente com a nova ordem~~ — 25/09, seção 2.3. O ETA virou
      pré-condição e os valores foram apertados para a escala do ciclo.
- [x] ~~Massa não é usada por nenhum algoritmo~~ — 25/09, seção 6.1.
- [x] ~~Justificar que a regra de emergência quebra a cadeia de dependência~~ — 25/09,
      seção 2.4, demonstrado na seção 7.3.
- [x] ~~Definir a forma da função matemática~~ — 25/09, seção 5. São **três**: linear,
      quadrática e periódica.
- [x] ~~Definir onde o tanque de subida do MAV é usado~~ — 25/09, seção 7.4.
- [ ] Decidir se a regra de emergência com **OR** entra (ver README, "sugestão de
      dificuldade"). Ela **afrouxa** a segurança, então precisa de justificativa escrita.
- [ ] Revisar as premissas numéricas que foram **escolhidas, não medidas**, e justificá-las no
      relatório: taxas de consumo (0,08 e 0,10 %/min), custo das correções (5% e 3%),
      probabilidades de falha (5% / 3% / 4%), empuxo (120 kN) e taxa do ISRU (0,25%/sol).

**Código (`scripts/mgpeb.py`):** — todos concluídos em 25/09
- [x] ~~Cadastrar o MAV e aplicar as prioridades novas~~
- [x] ~~Trocar os 5 blocos repetidos por um laço~~
- [x] ~~Implementar A, D e S~~ — e mais E, P, I e ETA: são **dez** sinais
- [x] ~~Criar fila, pilha e as listas de pousados / em espera / em alerta~~
- [x] ~~Algoritmos de busca~~ — menor combustível, maior prioridade, por tipo de carga
- [x] ~~Algoritmo de ordenação~~ — insertion sort escrito à mão, com justificativa
- [x] ~~Corrigir os dois defeitos do fim do arquivo antigo~~ — o arquivo foi substituído
- [x] ~~O cenário não testa a faixa de aborto~~ — coberto por `teste_faixa_de_aborto()`
- [ ] O `scripts/main.py` antigo ainda está no repositório. Decidir se é removido ou se fica
      como registro da primeira versão.

**Relatório (entregável 1, 5 a 10 páginas) — nada feito ainda:**
- [ ] Diagrama(s) de portas lógicas — exigido explicitamente. Hoje são **dez** sinais (seção 2).
- [ ] Seção de contextualização histórica e de arquitetura (item 05 do enunciado).
- [ ] Limitações de hardware numa missão em Marte e o impacto nas escolhas de algoritmo.
      *(Há material pronto: a escolha do insertion sort e das buscas lineares está justificada
      no código por critérios de memória e de dado que muda — é exatamente o que este item pede.)*
- [ ] **Seção de ESG e governança da base Aurora Siger** — exigida e ainda sem nenhuma nota.
- [ ] Anexo descrevendo o uso de listas, filas e pilhas (entregável 3).
- [ ] Análise de Monte Carlo (opcional, alto retorno): rodar N missões com sementes diferentes e
      reportar a taxa de sucesso. Responde "com que frequência esta missão falha?", que uma
      execução única não responde.
