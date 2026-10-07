# Partes 5 e 6 — MGPEB / Aurora Siger

Rascunho histórico, incorporado e condensado em `../RELATORIO_TECNICO.md` em 6 de outubro de 2026. Para a entrega, usar o relatório integrado. A numeração corresponde ao enunciado da atividade. As propostas de operação da base apresentadas abaixo não devem ser confundidas com funcionalidades já implementadas no simulador.

## 5. Contextualização do MGPEB à luz da evolução da computação

### Dos computadores de propósito geral aos sistemas embarcados

Os primeiros computadores eletrônicos de propósito geral demonstraram que uma mesma máquina poderia executar diferentes sequências de operações para resolver problemas. O ENIAC é um exemplo desse período: utilizava válvulas e sua programação inicial envolvia a configuração de conexões e chaves. Embora permitisse automatizar cálculos, seu porte e suas necessidades de operação estavam distantes das exigências de um equipamento instalado em uma nave. [Computer History Museum — ENIAC](https://www.computerhistory.org/revolution/story/78).

A evolução das válvulas para transistores e circuitos integrados contribuiu para reduzir o tamanho dos equipamentos e ampliar as possibilidades de processamento. Essa transformação permitiu incorporar computadores a máquinas e veículos. Nesses sistemas embarcados, o processamento atende funções específicas, como interpretar sensores e comandar equipamentos. O Apollo Guidance Computer exemplifica essa aplicação espacial: participou dos cálculos de orientação, navegação e controle das missões Apollo. A confiabilidade, porém, depende também de projeto, testes e mecanismos de recuperação, e não apenas da miniaturização. [NASA — computação espacial](https://www.nasa.gov/directorates/stmd/nasa-industry-advance-high-performance-spaceflight-computing/).

O MGPEB representa didaticamente essa integração entre dados e decisões. Ele recebe informações dos módulos e do ambiente, verifica condições obrigatórias, organiza os candidatos ao pouso e registra os resultados. As expressões booleanas permitem transformar critérios de segurança em decisões verificáveis. Por exemplo, um módulo com prioridade elevada continua bloqueado quando seus sensores são indicados como falhos. O programa simula essas informações; não recebe sinais de sensores reais nem controla uma nave.

### Limitações de hardware em uma missão a Marte

Uma missão espacial precisa equilibrar capacidade de processamento, memória, energia disponível e resistência ao ambiente. Como exemplo concreto, o Perseverance utiliza um processador RAD750 tolerante à radiação, com operação de até 200 MHz, 256 MB de memória dinâmica e 2 GB de memória flash. Possui dois elementos computacionais, permitindo recorrer a uma unidade reserva. Esses valores caracterizam esse rover, sem estabelecer uma configuração obrigatória para a base Aurora. [NASA — componentes do Perseverance](https://science.nasa.gov/mission/mars-2020-perseverance/rover-components/).

Para o MGPEB, essas restrições sugerem cuidados distintos. A memória limita o volume de módulos, alertas e eventos que pode permanecer armazenado. O processamento disponível limita o trabalho realizável em cada ciclo de decisão. O consumo de energia e o controle de temperatura exigem planejamento das atividades dos equipamentos. A exposição à radiação demanda componentes adequados e estratégias para lidar com falhas. O exemplo do Perseverance reúne proteção à radiação, redundância e monitoramento de energia e temperatura. [NASA — componentes do Perseverance](https://science.nasa.gov/mission/mars-2020-perseverance/rover-components/).

### Consequências para as escolhas do protótipo

Na implementação atual, cada módulo é representado por uma lista de atributos. A fila organiza a entrada dos módulos conforme sua chegada; em seguida, os candidatos aptos são ordenados pelas regras do projeto. Listas auxiliares registram espera, pousos e alertas. A pilha permite consultar os eventos do mais recente para o mais antigo. Essas estruturas tornam o fluxo compreensível e permitem acompanhar manualmente uma simulação pequena.

A busca linear percorre os registros até encontrar o módulo desejado. Quando se procura um valor extremo, o programa compara os elementos sem precisar ordenar toda a coleção. A ordenação por inserção reorganiza os índices dos candidatos aptos, preservando o cadastro principal. Para o cenário de cinco módulos, essas escolhas favorecem a compreensão e a revisão das regras. Se a quantidade de módulos aumentar, a ordenação por inserção poderá exigir um número de comparações que cresce aproximadamente com o quadrado da quantidade de candidatos, no pior caso.

O código também possui custos que precisam ser reconhecidos: a função `quantidade` percorre a lista para contar elementos, várias operações concatenam ou reconstroem listas e o histórico acumula eventos. Portanto, a simplicidade didática não comprova eficiência de memória ou de processamento. Uma adaptação para hardware limitado precisaria medir esses custos, reduzir cópias desnecessárias e definir limites de armazenamento e uma política de preservação dos registros importantes.

A organização em funções de validação, autorização, busca e ordenação facilita a identificação de erros. A verificação dos dados antes da simulação e os testes de cenários adversos contribuem para avaliar o comportamento do protótipo. Entretanto, os indicadores booleanos de sensores e sistemas apenas representam condições simuladas: não implementam redundância física, correção de erros de memória ou tolerância à radiação. Assim, o MGPEB permite estudar princípios de organização e confiabilidade, enquanto um sistema de voo exigiria desenvolvimento e validação específicos.

## 6. Princípios ESG na concepção da base Aurora

### Ambiental: área de pouso e uso responsável de recursos

Na base Aurora, a escolha da área de pouso deve conciliar segurança operacional e preservação do ambiente marciano. Como proposta de projeto, a equipe deve avaliar estabilidade e inclinação do terreno, obstáculos, distância das instalações e consequências da dispersão de poeira e detritos. Também deve identificar regiões de interesse científico e evitar que pousos, descarte ou atividades de extração comprometam futuras observações e amostras.

Esse cuidado inclui a proteção planetária. A NASA trabalha para evitar contaminação biológica de outros corpos celestes por material terrestre e a contaminação da Terra em missões de retorno. Para a Aurora, propõe-se aplicar esse princípio ao planejamento da limpeza dos equipamentos, contenção de resíduos e separação entre áreas operacionais e áreas de pesquisa. Essas medidas são diretrizes conceituais, não procedimentos de descontaminação implementados pelo MGPEB. [NASA/JPL — proteção planetária](https://planetaryprotection.jpl.nasa.gov/).

A gestão energética proposta deve manter um balanço entre geração, armazenamento e consumo, reservando capacidade para suporte à vida, comunicação e atividades críticas. Atividades adiáveis, como parte da produção e dos experimentos, devem ser programadas conforme a disponibilidade de recursos. Caso sejam utilizados painéis solares, o planejamento deve considerar períodos de baixa geração e manutenção. O código já representa uma dependência operacional do módulo Energia, mas não calcula geração elétrica, baterias ou consumo dos equipamentos.

Para água, materiais e resíduos, propõe-se controlar estoques, reduzir desperdícios, recuperar recursos quando tecnicamente viável e separar resíduos reutilizáveis daqueles que exigem contenção. A produção local deve priorizar necessidades justificadas, manutenção e reparo de equipamentos. O uso de recursos marcianos deve ser precedido de avaliação do gasto de energia, dos resíduos gerados e da alteração do local de extração. Utilizar um recurso local não garante, por si só, sustentabilidade.

### Social: segurança, necessidades essenciais e participação

As decisões de pouso afetam as condições de vida da futura comunidade. Por isso, a distribuição de recursos e as prioridades devem considerar necessidades essenciais, risco de perda de cargas e dependências entre os módulos. No protótipo, a urgência de combustível influencia a ordem somente entre módulos aptos: ela não elimina os bloqueios de segurança. Essa separação ajuda a discutir como atender uma necessidade urgente sem expor toda a operação a uma condição inaceitável.

Para a base, propõem-se treinamento dos operadores, procedimentos acessíveis, divisão de responsabilidades e canais para relatar falhas sem retaliação. Representantes das áreas médica, técnica, científica e de habitação devem participar da definição de prioridades. As decisões devem considerar os impactos sobre todos os ocupantes, incluindo quem depende de atendimento médico ou de recursos essenciais, evitando que influência pessoal substitua critérios conhecidos.

### Governança: decisões explicáveis e responsabilidades definidas

A governança da Aurora deve estabelecer quem define as regras, quem autoriza mudanças e quem revisa ocorrências. Propõe-se que alterações em limites de segurança e critérios de prioridade tenham justificativa registrada e revisão por outro integrante responsável. Durante emergências, procedimentos previamente acordados devem orientar a ação imediata, com análise posterior das decisões e de suas consequências.

O MGPEB oferece uma base para essa transparência ao registrar eventos, estados e motivos de bloqueio. Esses registros ajudam a explicar resultados, mas o histórico atual permanece em memória e não constitui um registro permanente protegido contra alterações. Como evolução, seria necessário armazenar registros com horário, identificação do módulo, motivo e versão das regras aplicadas, além de definir acesso, preservação e revisão. Dados pessoais e médicos devem ter acesso restrito, mesmo quando os critérios gerais de decisão forem transparentes.

Como acompanhamento da base, a equipe pode propor indicadores de energia disponível para emergências, recuperação de água, resíduos armazenados, incidentes e bloqueios de pouso por motivo. Metas e limites dependeriam das características da missão. A revisão periódica desses indicadores, com participação da comunidade, permitiria corrigir prioridades e avaliar se as decisões tecnológicas atendem à segurança, ao uso responsável de recursos e à preservação científica do ambiente.

---

Nota de revisão: os links sustentam os exemplos históricos e espaciais. As propostas de gestão da base são formulações para o cenário didático. Antes da versão final, conferir a terminologia com o material das disciplinas e integrar este texto ao limite de 5 a 10 páginas do relatório completo.
