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

| Módulo | Prioridade | Comb. de descida | Massa (kg) | Criticidade | ETA (h) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Veículo de Subida (MAV)** | 1 | *a definir* | *a definir* | *a definir* | *a definir* |
| **Energia** | 2 | 70% | 10.000 | 5/5 | T+0.5 |
| **Logística** | 3 | 40% | 12.000 | 3/5 | T+4 |
| **Habitação** | 4 | 80% | 15.000 | 5/5 | T+0 |
| **Suporte Médico** | 5 | 60% | 5.000 | 4/5 | T+2 |
| **Laboratório** | 6 | 90% | 7.000 | 2/5 | T+6 |

*Nota: O Módulo de Logística possui combustível reduzido para testar a lógica de "prioridade emergencial" no código.*

⚠️ **Os valores do MAV ainda não foram definidos** — e a criticidade dele é uma pergunta em
aberto: se ele for destruído **antes** de a tripulação descer, a missão é **adiada**, não há
perda de vidas. Isso é 5/5 ou menos?

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

### 2. Lógica de Autorização de Pouso (Portas Lógicas)
O pouso só é autorizado se todas as condições críticas forem verdadeiras (Lógica AND).

**Variáveis de Entrada:**
- **C (Combustível):** Nível suficiente para a descida (**≥ 20%** — ver as faixas em 2.1).
- **A (Atmosfera):** Condições climáticas estáveis (sem tempestades).
- **D (Disponibilidade):** Área de pouso livre de outros módulos.
- **S (Sensores):** Integridade dos sistemas de radar e navegação.
- **T (Terreno):** Coordenada de pouso validada como plana e segura.
- **$\theta$ (Ângulo):** Ângulo de entrada na atmosfera dentro da janela de segurança ($12^\circ$ a $15^\circ$).

**Expressão Booleana:**
`Autorização = C AND A AND D AND S AND T AND θ`

⚠️ O protótipo atual (`scripts/main.py`) implementa apenas **T, θ e C**. As variáveis **A**
(atmosfera), **D** (área disponível) e **S** (sensores) ainda não existem no código — hoje o
documento e o programa dizem coisas diferentes.

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

**Fila resultante com os dados da tabela 1** (supondo que todos passem na segurança):

| Ordem | Módulo | Por quê |
| :---: | :--- | :--- |
| 1º | Logística | Único na faixa **urgente** (40%) — fura a fila |
| 2º | MAV | Prioridade 1 |
| 3º | Energia | Prioridade 2 |
| 4º | Habitação | Prioridade 4 |
| 5º | Suporte Médico | Prioridade 5 |
| 6º | Laboratório | Prioridade 6 |

⚠️ **Tensão descoberta ao montar esta fila:** a Logística fura a fila por combustível e acaba
pousando **antes da Energia** — ou seja, a regra de emergência **quebra a cadeia de dependência**
que define a prioridade. Isso é aceitável (melhor pousar fora de ordem do que perder o módulo),
mas precisa ser justificado por escrito, e não descoberto pelo avaliador.

⚠️ Com as prioridades agora todas distintas (1 a 6), **o desempate por ETA nunca dispara**. Ele
continua na regra como critério de reserva, para o caso de dois módulos empatarem no futuro.

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

**A DECIDIR:** qual forma de função usar.
- **Linear** — `C(t) = C₀ − k·t` (consumo constante por minuto). Simples, honesta, e provavelmente
  compatível com o capítulo da matéria.
- **Exponencial** — `C(t) = C₀ · e^(−k·t)` (consumo proporcional ao que resta).
Escolher UMA, definir o `k`, justificar a escolha e analisar o gráfico.

### 6. Pontos em Aberto (checklist do que ainda falta)

**Decisões de modelagem:**
- [x] ~~Prioridade × Criticidade redundantes~~ — **resolvido em 24/09**: separadas em consequência
      × sequência (seção 1.1).
- [ ] **Definir os valores do MAV** (combustível de descida, massa, ETA, ângulo, coordenada) e
      decidir a **criticidade** dele: perdê-lo antes da tripulação descer adia a missão, não mata
      ninguém — isso é 5/5?
- [ ] **A coluna ETA ficou incoerente com a nova ordem.** Os ETAs atuais (Habitação T+0,
      Logística T+4…) foram escritos para a ordem antiga. E há um problema de fundo: **ETA é uma
      restrição física, não uma preferência** — um módulo não pode pousar antes de chegar à
      janela de órbita. Hoje a Logística é a 1ª da fila e só aparece em T+4. Ou os ETAs são
      reescritos para acompanhar a sequência, ou o algoritmo passa a tratar o ETA como um
      bloqueio ("ainda não chegou, não pode descer").
- [ ] **Massa não é usada por nenhum algoritmo.** Dar uma função a ela ou justificar a presença.
- [ ] **Justificar por escrito** que a regra de emergência pode quebrar a cadeia de dependência
      (ver o aviso na seção 2.2).
- [ ] Definir a forma da função matemática (seção 5).
- [ ] Decidir se a regra de emergência com OR entra (ver README, "sugestão de dificuldade").
- [ ] Definir onde o **tanque de subida** do MAV é usado (seção 1.2) — ele não entra no pouso;
      decidir se fica só como texto no relatório ou se vira um segundo estágio simulado.

**Código (`scripts/main.py`):**
- [ ] ⚠️ **O código ainda tem a tabela antiga**: 5 módulos e as prioridades velhas (1, 1, 2, 3, 4).
      Falta cadastrar o **MAV** e aplicar as prioridades novas da seção 1.1.
- [ ] Trocar os 5 blocos repetidos (`apto0`…`apto4`) por um **laço** sobre a lista.
- [ ] Implementar **A, D e S** — hoje só T, θ e C existem no código.
- [ ] Criar as estruturas que o enunciado exige: **fila** de autorização, **pilha**, e as listas
      auxiliares de **pousados**, **em espera** e **em alerta**.
- [ ] **Algoritmos de busca**: menor combustível, maior prioridade, por tipo de carga.
- [ ] **Algoritmo de ordenação** aplicando a regra 2.2 (hoje a fila está escrita à mão).
- [ ] Corrigir dois defeitos no fim do arquivo: o `apto2` (Suporte Médico) é impresso como
      "Módulo Suprimentos", e a lista final imprime fora da ordem de prioridade (3 → 4 → 2).
- [ ] O cenário não testa a faixa de aborto: nenhum módulo tem combustível abaixo de 20%.

**Relatório (entregável 1, 5 a 10 páginas):**
- [ ] Diagrama(s) de portas lógicas — exigido explicitamente, ainda não existe.
- [ ] Seção de contextualização histórica e de arquitetura (item 05).
- [ ] Limitações de hardware numa missão em Marte e o impacto nas escolhas de algoritmo.
- [ ] **Seção de ESG e governança da base Aurora Siger** — exigida e ainda sem nenhuma nota.
- [ ] Anexo descrevendo o uso de listas, filas e pilhas (entregável 3).
