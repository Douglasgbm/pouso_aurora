# Parecer final por critério - 13/10/2026

## Conclusão objetiva

**O conteúdo obrigatório da Fase 2 está atendido nos itens abaixo. Não há correção pendente identificada no código, no anexo ou no conteúdo técnico de apoio. O PDF final da colega foi recebido e conferido: RELATORIO_FINAL_EQUIPE.pdf, com revisão em REVISAO_PDF_FINAL.md.**

Este parecer amplia a revisão anterior: confronta diretamente o enunciado original, os oito capítulos fornecidos, o trabalho da Fase 1 no GitHub e a versão atual da Fase 2. O HTML é um extra e recebeu teste pontual de navegação no site publicado.

## Como os critérios foram interpretados

O documento PBL Aurora 2.docx informa **15 pontos totais** e lista três critérios: relatório técnico em PDF, código fonte Python e anexo de estruturas. A tabela fornecida não apresenta pesos individuais nem níveis de desempenho. O checklist abaixo decompõe as exigências textuais, sem inventar pesos. “Atendido” significa que há conteúdo/implementação e evidência verificável; o PDF final da colega também foi conferido, conforme REVISAO_PDF_FINAL.md.

## Checklist completo do enunciado

| ID | Exigência | Evidência conferida | Resultado |
|---|---|---|---|
| 1.1 | Definir os módulos | Energia, Habitação, Logística, Médico e Laboratório; TIPOS/MODULOS; relatório §1 | Atendido |
| 1.2 | Atributos básicos | ID, prioridade, combustível, massa, criticidade e ETA, com tipos e unidades; cadastro de 12 posições | Atendido |
| 1.3 | Fila principal de chegada | fila recebe por ETA e retira pelo índice zero, FIFO; simular | Atendido |
| 1.4 | Listas auxiliares | espera, aptos, pousados e alertas; anexo §2 | Atendido |
| 2.1 | Condições de autorização | combustível, atmosfera, área, sensores e sistemas; autorizar | Atendido |
| 2.2 | Expressão booleana | C AND S AND E AND A AND D; equivalência de De Morgan | Atendido |
| 2.3 | Diagrama visual de portas | portas_logicas.svg integrado no PDF, com AND/OR/NOT e saídas autorizar/adiar | Atendido |
| 3.1 | Python executável | mgpeb.py executado isolado, sem pacotes externos | Atendido |
| 3.2 | Cadastro em estruturas lineares | MODULOS editável, cópias de listas, fila e pilha de histórico | Atendido |
| 3.3 | Busca por características | buscar e buscar_extremo; demonstrações menor combustível, maior prioridade e Médico | Atendido |
| 3.4 | Ordenação da fila de pouso | ordenar por inserção sobre os aptos extraídos da espera; próximo é aptos[0] | Atendido |
| 3.5 | IF/ELIF/ELSE | autorização, evento, acidente e ativação por tipo; coerentes com as portas | Atendido |
| 3.6 | Simplicidade e comentários | núcleo procedural, listas e laços explícitos, sem imports, classes ou bibliotecas avançadas | Atendido |
| 3.7 | Exemplos simples | 14 cenários em exemplos.py, saída atual em exemplos_saida.txt | Atendido |
| 4.1 | Fenômeno escolhido | consumo estimado de combustível em função da duração; hipótese operacional explícita | Atendido |
| 4.2 | Fórmula e parâmetros | C(t)=k*m*t e F(t)=C(t)+R; significado, valores e unidades no §4 | Atendido |
| 4.3 | Gráfico e análise | SVG, tabela de valores, inclinação, intercepto e efeitos de massa/duração/reserva | Atendido |
| 4.4 | Relação com a decisão | mínimo bloqueia insuficientes; margem relativa define urgência entre aptos | Atendido |
| 5.1 | Evolução da computação | válvulas/ENIAC, transistores, circuitos integrados e aplicação embarcada espacial | Atendido |
| 5.2 | Restrições de hardware | memória, processamento, energia, temperatura e radiação; §5 | Atendido |
| 5.3 | Consequências para o programa | custo da busca/ordenação, cópias, crescimento do histórico, validação e limites; §5.1 | Atendido |
| 6.1 | Impactos da área de pouso | terreno, poeira, instalações, interesse científico e proteção planetária; §6 | Atendido |
| 6.2 | Energia, resíduos e recursos | reservas críticas, produção adiável, estoques, recuperação, descarte e extração local | Atendido |
| 6.3 | Social e governança | segurança, treinamento, representação, revisão de regras, transparência e responsabilidades | Atendido |
| E.1 | Conteúdo do relatório técnico | cenário, portas, funções, história/hardware e ESG presentes | Atendido na base de apoio |
| E.2 | PDF entre 5 e 10 páginas | base renderizada com 10 páginas, incluindo anexo | Atendido no PDF final (10 páginas) |
| E.3 | Fonte Python .py | mgpeb.py e exemplos.py incluídos no pacote obrigatório | Atendido |
| E.4 | Anexo com exemplos concretos | §2: cadastro, FIFO, espera, aptos, pousados, alertas e pilha LIFO no cenário urgente | Atendido |

São **28 verificações de requisitos/entregáveis** nesta decomposição. Ela não é uma rubrica numérica criada pela FIAP.

## Conferência com as unidades

Páginas são as páginas dos PDFs fornecidos. Os materiais do curso não foram copiados para os repositórios públicos.

| Unidade | Páginas conferidas relevantes | Correspondência no projeto |
|---|---|---|
| Cap. 1 - A Aurora Ajusta a Trajetória | 8–12, 14–17 | Contexto, articulação de disciplinas e enunciado MGPEB |
| Cap. 2 - A Programação Procedural | 32–35, 36–40, 45–50 | AND, OR e NOT; autorização e diagrama |
| Cap. 3 - As Estruturas Lógicas | 7–10, 13–24, 25–26 | Condicionais, laços e menu contínuo |
| Cap. 4 - As Estruturas Lineares | 32–35, 36–37 | Funções, vetores, pilha LIFO e fila FIFO; conceitos apresentados em C, aplicados a listas Python |
| Cap. 5 - Busca e Ordenação | 17–19, 29–30 | Busca linear, sentinela -1 e ordenação por inserção |
| Cap. 6 - As Funções Aplicadas | 15, 19–21, 35–36 | Funções, parâmetros, reta e modelo simples interpretável |
| Cap. 7 - A Evolução Computacional | 19–23 | ENIAC, transistores, circuitos integrados e miniaturização |
| Cap. 8 - Governança ESG | 11–17, 25–28 | Princípios, transparência, recursos/resíduos e impactos sociais |

As regras específicas de dependência, os cinco tipos, a taxa de consumo e as reservas são escolhas didáticas da equipe, não fatos atribuídos às apostilas. NumPy e Matplotlib podem aparecer no ensino, mas o enunciado não obriga seu uso; as operações aritméticas e o gráfico vetorial já atendem à modelagem solicitada.

## Pontos que poderiam gerar desconto e foram conferidos

- **Cadastro:** não exige formulário interativo; o enunciado pede cadastro em estruturas lineares. O cadastro editável no script satisfaz isso.
- **Fila e prioridade:** FIFO ordena a recepção. A espera conserva os candidatos, e a ordenação dos aptos determina a sequência efetiva de pouso. Não se afirma que um escalonamento por prioridade seja FIFO puro.
- **Busca “rapidamente”:** busca linear é algoritmo clássico ensinado e adequado ao conjunto pequeno. Não é necessário adicionar busca binária sobre dados não ordenados.
- **Criticidade e prioridade:** ambos existem e influenciam os critérios declarados. Criticidade desempata urgentes; tipo e prioridade completam a ordem. Não há obrigação de priorizar sempre um número antes de todas as outras regras.
- **Pilha:** o histórico é copiado em ordem e consultado do mais recente ao mais antigo. Remover o topo não desfaz decisões; isso está explícito no anexo.
- **Fórmula:** consumo é linear e mínimo com reserva é afim. Reserva não é gasta. Com a configuração padrão, consumo de 10 kg, mínimo de 12 kg e faixa urgente de 12 a 15 kg são consistentes.
- **Fenômeno operacional:** o enunciado admite fenômeno físico ou operacional e dá exemplos, sem obrigar simulação de altura, velocidade, paraquedas ou retrofoguetes. O consumo escolhido atende ao escopo.
- **História e hardware:** o relatório conecta a evolução à aplicação embarcada e às escolhas concretas do programa. Não se limita a uma cronologia genérica.
- **ESG:** as três dimensões estão contempladas com medidas para Marte e participação nas decisões. A reflexão solicitada não exige implementar gestão ambiental completa em Python.
- **Bibliotecas:** o núcleo não tem imports. Ferramentas de teste, exportação, PDF e HTML são complementos separados.
- **Limites:** eventos durante a descida são aplicados ao fim; pousos são sequenciais; espera em órbita não consome combustível. São simplificações explícitas, sem contradizer resultados apresentados.
- **Equipe:** Alice, Douglas e Marcelo. Os dois integrantes adicionais da Fase 1 não aparecem na identificação atual.
- **Entregáveis:** guia e revisão ficam separados da base de 10 páginas. Arquivos antigos e slides anteriores estão identificados como históricos.

## Evidência adicional de robustez

Além dos 46 testes Python e das 13 verificações da auditoria, foram executados **400 cenários determinísticos adicionais**, com semente 20261013, de zero a 12 módulos, chegadas variadas, bloqueios, acidentes, falhas e reparos. Foram verificadas 152 descidas nessa amostra.

As verificações exigem preservação dos dados de entrada, repetibilidade, consumo apenas uma vez por descida, reserva preservada, ausência de pousos duplicados, separação entre espera e solo, dependências operacionais válidas, cópia correta da pilha e relógio sem regressão. Todos passaram. O teste está em tools/verificar_invariantes.py e usa apenas a biblioteca padrão, fora do núcleo acadêmico.

```text
python tools/verificar_invariantes.py
node tools/verificar_painel.cjs
```

O segundo comando testa JavaScript com DOM simulado, nos 15 cenários em dois modos; não renderiza CSS. A aparência do modo de leitura ainda requer navegador real. Esta limitação pertence ao extra HTML e não altera o atendimento dos 28 itens obrigatórios acima.

## Situação para entrega

**Implementação obrigatória, anexo e conteúdo técnico: fechados conforme o checklist.** A versão de apoio já satisfaz o conteúdo e o limite de páginas. O PDF final da colega foi recebido, revisado e publicado; resta realizar o envio no portal.

A referência da Fase 1 foi útil para clareza, organização e evidências. Não foram transplantados o limite de páginas, o notebook ou a composição da equipe anterior. A avaliação aqui é de conformidade demonstrada com o material disponível, sem inventar pesos ou uma nota atribuída pelo professor.
