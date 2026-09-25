github do projeto https://github.com/Douglasgbm/pouso_aurora

# MGPEB — Módulo de Gerenciamento de Pouso e Estabilização de Base

Simulação do pouso autônomo de seis módulos na base Aurora Siger, em Marte.
Atividade Integradora da Fase 2 (PBL).

## Como rodar

    python3 scripts/mgpeb.py          # a missão completa
    python3 scripts/mgpeb.py teste    # a bateria de testes

Sem dependências externas: só a biblioteca padrão do Python 3.

## O que o programa faz, em cinco camadas

Cada camada roda sozinha e só foi construída depois que a de baixo estava provada.

| Camada | O que faz | O que ela responde |
| :---: | :--- | :--- |
| 1 | **Cadastro** dos 6 módulos, com validação | "os dados são coerentes?" |
| 2 | **Dez portas lógicas** (o AND gigante) | "este módulo PODE pousar?" |
| 3 | **Fila dinâmica**, com o relógio andando | "entre os que podem, quem vai AGORA?" |
| 4 | **A descida**, em três estágios de freio | "o pouso deu certo? gastou quanto?" |
| 5 | **Estabilização da base**, sol a sol | "a base fica de pé? quando a tripulação parte?" |

A Camada 1 valida o próprio cadastro antes de qualquer coisa ser construída em cima. As
Camadas 2 e 3 separam as duas perguntas que o combustível responde (segurança *elimina*,
urgência *enfileira*). A Camada 4 traz a física real do pouso — e foi ela que provou que a
regra fixa dos 20% da Camada 2 é insegura para módulos pesados. A Camada 5 fecha a segunda
metade do nome do projeto, que até 25/09/2026 não existia em lugar nenhum.

## Três funções matemáticas, uma por fase

| Fase | Fenômeno | Forma |
| :--- | :--- | :--- |
| espera em órbita | combustível × tempo de espera | **linear** |
| frenagem (7 min) | altura × tempo de descida | **quadrática** |
| já no solo | geração solar × hora do dia | **periódica** |

São fases diferentes da missão, e por isso formas matemáticas diferentes. A quadrática tem a
leitura gráfica mais útil do projeto: **projetar o pouso é fazer o vértice da parábola
coincidir com o solo.** Vértice acima, o módulo para no ar e desperdiça combustível; vértice
abaixo, ele chega ao solo ainda em movimento.

## O documento técnico

O raciocínio completo, com todas as decisões datadas e as tabelas de valores, está no
[ROADMAP.md](ROADMAP.md). O texto abaixo é o registro de como o projeto foi pensado, na ordem
em que foi pensado — inclusive os pontos que depois mudaram de ideia.

---


1. Prioridade de Pouso
É o "quem passa na frente". Não é necessariamente quem chega primeiro, mas quem é mais importante. 
   Exemplo:* Um módulo de Suporte Médico ou Energia tem prioridade maior que um de Laboratório Científico. Se houver um problema na pista, o de energia pousa primeiro para garantir que a base não apague.

2. Nível de Combustível
É a margem de erro. Quanto menos combustível, mais urgente é o pouso.
   Lógica:* Se o módulo A tem 50% de combustível e o B tem 5%, o B precisa de prioridade máxima, senão ele cai como uma pedra.

3. Massa
O peso do módulo. Isso afeta a física do pouso e a estabilidade da base.
   Impacto:* Módulos mais pesados exigem mais potência dos retrofoguetes e podem demorar mais para estabilizar no solo.

4. Criticidade da Carga
É o "o que acontece se isso quebrar?". 
   Exemplo:* Se o módulo de Habitação for perdido, a missão acaba (criticidade altíssima). Se um módulo de Amostras de Solo for perdido, é triste, mas a tripulação continua viva (criticidade média/baixa).

5. Horário Estimado de Chegada (ETA)
É a agenda. Quando o módulo entra na janela de pouso.
   Uso:* Serve para você organizar a fila (Queue) no Python. Você não pode pousar dois módulos no mesmo segundo no mesmo lugar.

Resumindo:
Essas métricas são os "dados" que você vai colocar dentro de uma lista ou classe no Python. Depois, você vai criar a lógica: "Se a criticidade for ALTA e o combustível for BAIXO, mova esse módulo para o topo da fila de pouso".



⚠️ ATENÇÃO AO LER A LISTA ABAIXO: as PRIORIDADES desta lista são as ORIGINAIS, de antes da
decisão de 24/09/2026 que separou prioridade de criticidade. Elas estão mantidas aqui como
registro de como o projeto começou. As prioridades VALENDO são as da seção "PRIORIDADE NÃO É
CRITICIDADE", mais abaixo, e a tabela completa e atual está no ROADMAP, seção 1.

1. Módulo: Habitação (Hab)
*   Prioridade de Pouso: 1 (Máxima). Sem casa, a missão não começa. Ele tem que ser um dos primeiros a tocar o solo.
*   Nível de Combustível: 80%. Como ele é a prioridade 1, a gente assume que ele foi planejado para ter uma margem de segurança alta, mas ele não pode ficar orbitando para sempre.
*   Massa: 15.000 kg. É um dos módulos mais pesados, porque envolve paredes blindadas contra radiação e sistemas de suporte à vida.
*   Criticidade da Carga: Crítica (Nível 5/5). Perda total do habitat = aborto imediato da missão.
*   Horário Estimado de Chegada (ETA): T+0h (Primeira Janela). Ele deve chegar no início da sequência de pousos.

2. Módulo de Energia (Power)
*   Prioridade: 1 (Máxima). Empata com o Habitat. Sem energia, o Habitat não liga o oxigênio.
*   Combustível: 70%.
*   Massa: 10.000 kg. (Pesado, mas menor que o Hab).
*   Criticidade: Crítica (5/5). Sem luz, a base morre.
*   ETA: T+0.5h. (Chega logo após o Hab).

3. Módulo de Suporte Médico (MedBay)
*   Prioridade: 2 (Alta). Importante, mas a galera aguenta algumas horas sem o hospital se tiver oxigênio e luz.
*   Combustível: 60%.
*   Massa: 5.000 kg. (Mais leve, equipamentos precisos).
*   Criticidade: Alta (4/5). Essencial para a sobrevivência a longo prazo.
*   ETA: T+2h.

4. Módulo de Logística (Cargo/Suprimentos)
*   Prioridade: 3 (Média). Comida e peças sobressalentes são vitais, mas não para os primeiros 30 minutos.
*   Combustível: 40%. 
*   Massa: 12.000 kg. (Muito pesado por causa da carga).
*   Criticidade: Média (3/5).
*   ETA: T+4h.

5. Módulo de Laboratório Científico (Science)
*   Prioridade: 4 (Baixa). É o objetivo da missão, mas é o último na escala de sobrevivência.
*   Combustível: 90%. (Está tranquilo na órbita).
*   Massa: 7.000 kg.
*   Criticidade: Baixa/Média (2/5). Se cair, a ciência sofre, mas ninguém morre.
*   ETA: T+6h.

6. Veículo de Subida (MAV — Mars Ascent Vehicle) — ACRESCENTADO EM 24/09/2026
*   O que é: é a "carona de volta". Ele pousa VAZIO e passa meses fabricando o próprio
    propelente a partir do gás carbônico da atmosfera de Marte. Assim ninguém precisa carregar
    da Terra o combustível da viagem de retorno — o que seria caríssimo, porque combustível tem
    massa, e massa exige mais combustível para ser freada na descida.
*   Prioridade: 1 (primeiro a pousar). Não é por ser o mais valioso — é por ser o de MAIOR
    PRAZO. A planta leva meses enchendo o tanque, e a tripulação não pode nem sair da Terra
    antes de os tanques estarem cheios e confirmados. Ele trava tudo que vem depois.
*   Detalhe a justificar: a planta precisa de energia elétrica, e o módulo de Energia pousa
    depois dele. Não é problema — a fila inteira dura uma tarde, o enchimento leva meses.
*   Combustível de descida: 75%. Energia (bateria): 90%. Massa: 18.000 kg — o mais pesado de
    todos, porque é um foguete inteiro mais a planta química, ainda que com os tanques de
    subida vazios.
*   Criticidade: 4/5 — RESOLVIDO EM 25/09/2026. A pergunta em aberto era se ele valia 5/5.
    Resposta: não. Perdê-lo ANTES de a tripulação sair da Terra adia a missão em uma janela de
    lançamento (~26 meses) — custo enorme, mas SEM MORTES. Ele não é 5/5 justamente porque
    existe a regra de só lançar a tripulação com os tanques confirmados cheios; essa regra
    existe PARA rebaixar o risco dele. Energia e Habitação são 5/5 porque a falha delas mata
    gente com a base já ocupada.
*   ETA: T+0 — chega junto com a Habitação, e é o primeiro da fila de projeto.

PREMISSA DA MISSÃO (decidida em 24/09/2026)

A nave mãe FICA EM ÓRBITA. Os seis módulos descem sozinhos, sem piloto e sem controle remoto,
e não voltam — são descartáveis por projeto. A tripulação desce em missão posterior, depois que
tudo estiver no solo e funcionando.

Por que a nave mãe não desce: sair da superfície de Marte de volta para a órbita custa cerca de
4 km/s (na Terra seriam ~9,4 km/s — Marte tem 38% da nossa gravidade e quase nenhuma atmosfera).
Descer a nave inteira significaria pousar todo o combustível da volta e erguer ele de novo. Foi
exatamente esse o debate do programa Apollo nos anos 60, e venceu a opção de deixar a nave
principal em órbita.

Por que os módulos são autônomos: nos 7 minutos da descida, o rádio demora MAIS que isso para ir
e voltar da Terra. Não existe piloto e não existe "abortar por comando" — o módulo decide
sozinho. É essa a razão de existir do MGPEB: ele não ajuda um operador humano, ele É o operador.

DECISÃO (debatida em 24/09/2026) — O COMBUSTÍVEL RESPONDE A DUAS PERGUNTAS DIFERENTES

A gente estava usando o combustível para duas coisas ao mesmo tempo, e por isso o número
parecia se contradizer (20% no código, 50% aqui). Não era erro: eram duas perguntas.

   Pergunta 1 — "esse módulo PODE pousar?"
      É segurança. Responde SIM ou NÃO. É o AND das portas lógicas.

   Pergunta 2 — "entre os que podem, QUEM VAI PRIMEIRO?"
      É ordem de serviço. Responde com uma posição na fila.

A primeira ELIMINA, a segunda ENFILEIRA. Um módulo pode ser importantíssimo e ainda assim
estar proibido de descer; outro pode estar liberado e ficar por último.

Daí saíram três faixas de combustível:

     0% ---------- 20% ---------- 50% ---------- 100%
      |   ABORTA     |   URGENTE    |    NORMAL     |
      |              |              |               |
      pergunta 1     pergunta 2     pergunta 2

- Abaixo de 20%: o módulo NÃO é autorizado a descer — não sobra margem para os retrofoguetes
  frearem a descida. Ele sai da fila e vai para a lista de ALERTA (não é esquecido, é
  monitorado).
- Entre 20% e 50%: o módulo desce, mas FURA A FILA. É a emergência de combustível: ainda dá
  para pousar, mas ele não aguenta esperar outra volta de órbita.
- Acima de 50%: o módulo desce na ordem normal, definida pela prioridade.

Comparação que ajuda: é um aeroporto. O avião que declara emergência de combustível fura a
fila inteira — mas os outros vinte continuam pousando na ordem normal entre si.

REGRA DA FILA — como as duas métricas convivem

   Nível 1 (faixa):      todo módulo URGENTE passa na frente de todo módulo NORMAL.
   Nível 2 (prioridade): dentro da MESMA faixa, prioridade menor primeiro (1 é a máxima).
   Desempate (ETA):      empatou na prioridade, desce quem chega antes à janela de órbita.

Por que assim: IMPORTÂNCIA NÃO É URGÊNCIA. Se o Laboratório (prioridade 4, o menos importante)
estiver com 8% de combustível, ele desce antes da Habitação (prioridade 1) — porque adiar a
Habitação significa apenas ESPERAR, e adiar o Laboratório significa PERDER o módulo.

DECISÃO (24/09/2026) — PRIORIDADE NÃO É CRITICIDADE

Na primeira versão da tabela, as duas colunas somavam 6 em TODAS as linhas (1+5, 1+5, 2+4, 3+3,
4+2). Isso quer dizer que elas eram o mesmo ranking escrito em escalas invertidas: dando uma,
dava para calcular a outra (criticidade = 6 − prioridade). Uma das duas era decorativa.

Agora cada uma responde a uma pergunta diferente:

   CRITICIDADE -> "o que a missão perde se este módulo for DESTRUÍDO?"  (consequência)
   PRIORIDADE  -> "em que ordem o solo precisa RECEBÊ-LOS?"             (sequência)

E a sequência é decidida por DEPENDÊNCIA, não por valor: não é "quem vale mais", é "quem precisa
estar no chão para que o próximo faça sentido".

Ordem nova, com a justificativa de cada um:

   1º MAV            - maior prazo de todos (meses enchendo o tanque) e trava a vinda da tripulação
   2º Energia        - tudo depende dela; sem energia o Habitat não liga o oxigênio
   3º Logística      - traz ferramenta e peça para conectar a energia aos outros módulos
   4º Habitação      - depende de energia ligada e de ferramenta disponível
   5º Suporte Médico - só é necessário quando houver gente na base, e ela chega depois
   6º Laboratório    - é o objetivo da missão, mas nada depende dele

Prova de que a separação funcionou: as somas agora são 7, 7, 6, 9, 9, 8 — não são mais todas 6.
O melhor exemplo é a LOGÍSTICA: criticidade baixa (3) e prioridade alta (3ª de seis). Perder a
logística não mata ninguém, mas ela precisa chegar cedo. Esse par "pouco crítico, muito urgente"
era invisível no modelo antigo — é o melhor argumento para justificar as duas colunas no relatório.

DECISÃO (24/09/2026) — SÃO DOIS TANQUES, NÃO UM

O MAV obrigou a separar duas coisas que estavam num número só:

   COMBUSTÍVEL DE DESCIDA - margem para os retrofoguetes frearem. É o que a tabela sempre teve,
                            e é sobre ele que fala a regra dos 20%. ENTRA na autorização (sinal C).
   TANQUE DE SUBIDA       - só do MAV. Quanto do propelente de retorno já foi fabricado a partir
                            do CO2 marciano. Enche em meses, já no solo. NÃO entra na autorização
                            de pouso — o que ele libera é a partida da tripulação lá da Terra.

Sem essa separação, alguém leria "MAV: tanque vazio" e concluiria que ele deve abortar a descida
— quando na verdade ele pousa com o tanque de subida vazio POR PROJETO.

METRICAS PARA AS PORTAS LOGICAS

1.  Combustível Suficiente (Sinal: C)
2.  Condições Atmosféricas Estáveis (Sinal: A) — Ex: sem tempestade de areia
3.  Área de Pouso Disponível (Sinal: D) — Ex: não tem outro módulo parado no caminho
4.  Integridade dos Sensores (Sinal: S) — Ex: o radar está funcionando

A Lógica (A Regra de Ouro):
Para o pouso ser autorizado, TODAS essas condições precisam ser verdadeiras ao mesmo tempo. Se uma única coisa falhar, o pouso é bloqueado.

Em linguagem de lógica, isso é um AND gigante:
Autorização = C AND A AND D AND S

ATUALIZAÇÃO (25/09/2026): essa lista cresceu para DEZ sinais. Entraram:

    T    terreno validado, sem cratera na coordenada
    θ    ângulo de entrada dentro da janela de segurança (12° a 15°)
    E    energia elétrica suficiente (a bateria é que ACIONA o paraquedas e as válvulas —
         tanque cheio não serve de nada se o computador desligar no meio da descida)
    P    paraquedas operacional
    I    integridade estrutural (a entrada atmosférica castiga o casco)
    ETA  o módulo já chegou à órbita

A expressão oficial:

Autorização = ETA AND C AND E AND A AND D AND S AND T AND θ AND P AND I

E CADA PORTA DEVOLVE DUAS COISAS, NÃO UMA: se passou, e — caso não tenha passado — se a causa
é RECUPERÁVEL ou DEFINITIVA.

    recuperável -> EM ESPERA : tempestade passa, ETA chega, alvo pode ser deslocado.
                               O módulo volta a disputar no próximo ciclo.
    definitiva  -> EM ALERTA : combustível só diminui, e não há quem conserte um radar em
                               Marte. O módulo sai da fila.

Basta UMA causa definitiva para mandar o módulo ao alerta, mesmo que todas as outras falhas
sejam temporárias. Sem isso, as duas listas que o enunciado pede seriam a mesma coisa com dois
nomes. Detalhamento no ROADMAP, seção 2.

- SUGESTAO DE DIFICULDADE

Quer complicar um pouco para ganhar nota extra?
A gente pode criar uma "Regra de Emergência". Tipo: "Se o combustível estiver CRÍTICO (muito baixo), a gente ignora a 'Área de Pouso Disponível' e pousa onde der para não perder a nave".

Aí a lógica vira:
Autorização = (C AND A AND D AND S) OR (Combustível_Crítico AND A AND S)

- IDEIAS GUARDADAS PARA DEPOIS (não implementar agora — base sólida primeiro)

1. Transferência de combustível entre módulos. Se o Laboratório está com 8% e a Habitação com
   80%, transferir 12% deixaria o Laboratório na margem mínima de 20% e salvaria o módulo.
   Existe de verdade em voo (reabastecimento orbital), mas entre módulos já separados e em
   rota de entrada é bem mais complicado. Serve melhor como discussão no RELATÓRIO do que
   como código.
2. A regra de emergência com OR acima (ignorar a área disponível quando o combustível é
   crítico). Decidir se entra: ela AFROUXA a segurança, então precisa de justificativa escrita.
3. ~~Usar a MASSA em alguma decisão~~ — RESOLVIDO EM 25/09/2026, e não por decreto: saiu da
   física. Os retrofoguetes precisam PRIMEIRO anular o peso do módulo, e só o que sobra freia
   de fato: a = (empuxo / massa) − gravidade. Daí sai a cadeia inteira — mais pesado desacelera
   menos, precisa acionar mais alto, queima por mais tempo e gasta mais combustível. O MAV
   (18 t) aciona a 1.691 m e gasta 40,6%; o Suporte Médico (5 t) aciona a 246 m e gasta 5,9%.
   Ver ROADMAP, seção 6.1.