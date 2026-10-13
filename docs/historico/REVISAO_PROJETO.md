> Registro da revisão da versão 1.1. A revisão atual está em REVISAO_RIGOROSA_DOUGLAS.md.

# Revisão do MGPEB — 6 de outubro de 2026

## Atualização após as correções da versão 1.1

Os achados 1 a 3 da revisão abaixo foram tratados: reavaliação de saúde e dependências com suspensão/recuperação, validação dos tipos antes de percorrer listas e regeneração da saída dos exemplos em UTF-8. O esquema ASCII foi substituído pelo diagrama `portas_logicas.svg` (AND/NOT). A capa ainda depende da identificação da equipe.

Validação atual: 17 testes aprovados e 14 cenários executados; os testes incluem 32 combinações booleanas, quatro limites de combustível, entradas malformadas, falha e recuperação da Energia, dependências em ordem inversa, módulo Energia alternativo e preservação do acidente. O relatório acadêmico permanece com 10 páginas. O guia separado explica os comportamentos e as mudanças em detalhe.

O restante deste documento preserva a revisão anterior como registro dos problemas e de suas reproduções. As quantidades de oito testes e onze cenários abaixo descrevem a versão anterior, não o estado atual.

Escopo: código atual, exemplos, testes, experimento anterior, planejamento, instruções, relatório e geração do PDF. Os achados do simulador referem-se ao código herdado do commit `cbaf4d0`; `mgpeb.py` não foi alterado nesta entrega.

## Consideração geral

O projeto tem uma base didática consistente: distingue autorização e prioridade, aplica uma função afim ao combustível e demonstra busca, ordenação e estruturas lineares. O relatório atualizado incorpora evolução da computação, limitações de hardware e ESG. Ainda existem pendências de comportamento e apresentação; a aprovação nos testes existentes não torna o trabalho automaticamente pronto para entrega.

## Achados, por prioridade

### 1. Falhas após o pouso não atualizam o estado operacional — prioridade média

**Local:** `mgpeb.py`, aplicação de eventos em `simular` e ativação em `ativar` (linhas 263–273 e 201–223 na versão revisada).

**Reprodução:** `simular([montar("E", "Energia")], [[6, "sistemas", False, "E"]], [True, "livre"], CONFIG)` termina com `SISTEMAS=False` e `ESTADO="operacional"`.

**Impacto:** o relatório de resultados pode apresentar como operacional um módulo com sistemas falhos. Outros módulos podem continuar considerando sua dependência satisfeita. Também é possível uma falha aplicada no final da descida anteceder uma ativação que não reavalia esses campos.

**Recomendação:** definir a abrangência dos eventos. Se forem admitidos após o pouso, reavaliar saúde e dependências operacionais e testar a perda do módulo Energia. Se representarem somente condições de autorização, rejeitar ou tratar explicitamente eventos fora dessa fase. A escolha muda o modelo e deve ser acordada antes de alterar o algoritmo.

### 2. A validação pressupõe estruturas iteráveis — prioridade média

**Local:** `mgpeb.py`, `validar` e `quantidade` (a partir das linhas 61 e 23).

**Reprodução:** `simular([42], [], [True, "livre"], CONFIG)` e uma lista de eventos contendo `42` causam `TypeError: 'int' object is not iterable`.

**Impacto:** o comportamento contraria a expectativa geral de rejeição de entradas inválidas com aviso e lista vazia. A conferência de tamanho acontece antes de conferir se os contêineres são listas.

**Recomendação:** validar os tipos de `modulos`, `eventos`, `ambiente`, `config` e de suas linhas antes das travessias. Incluir testes de entradas malformadas, preservando o nível de Python adotado pelo curso.

### 3. Saída salva dos exemplos está desatualizada — prioridade baixa

**Local:** `exemplos_saida.txt`.

**Evidência:** o arquivo não decodifica como UTF-8 e difere da execução atual de `exemplos.py`. Inclui saída da demonstração principal antes dos cenários, embora a importação atual não execute essa demonstração.

**Impacto:** leitores podem ver acentos corrompidos e resultados que não correspondem à versão atual.

**Recomendação:** regenerar a saída dos onze cenários em UTF-8 e declarar o comando de geração. O arquivo foi preservado nesta entrega para manter separadas a revisão e uma correção posterior do material de exemplos.

## Conferência dos requisitos

| Item | Evidência | Consideração |
|---|---|---|
| 1. Cenário e módulos | Cinco tipos, atributos, chegada, espera, pousados e alertas | Atendido no cenário didático. A fila FIFO é transitória; a lista de espera e os aptos implementam a decisão por prioridade |
| 2. Portas lógicas | Expressão AND e representação textual no relatório | Melhorar antes da entrega: substituir o esquema ASCII por diagrama gráfico de portas, com entradas e saída identificadas. Não é necessário usar portas adicionais sem necessidade lógica |
| 3. Protótipo Python | Busca linear, extremos, inserção, listas, fila, pilha e condicionais | Implementado; considerar os dois achados de comportamento acima |
| 4. Funções aplicadas | Fórmulas, unidades, gráfico, tabela e relação com autorização | Coerente com a fórmula usada. Coeficientes são hipotéticos; não representa trajetória |
| 5. Evolução da computação | História, exemplo espacial, limitações e custos das escolhas | Incorporado às seções 5 e 5.1, com fontes |
| 6. ESG | Área de pouso, recursos, pessoas, participação e rastreabilidade | Incorporado à seção 6; propostas distinguidas de funcionalidades |
| PDF de 5 a 10 páginas | PDF regenerado: 10 páginas | Dentro do limite. A capa ainda pede nomes da equipe |
| Anexo de estruturas | Seção 2 identificada como anexo integrado | Descreve usos concretos e operações; pode permanecer no relatório |

## Simplificações que a equipe precisa explicar

- **Eventos durante a descida:** são aplicados ao final dela. É uma hipótese declarada de transição atômica, não reação em tempo real.
- **Espera em órbita:** não consome combustível. Assim, esperar não torna automaticamente um módulo mais urgente no modelo.
- **Prioridade:** fora da urgência, o tipo antecede a prioridade numérica. Um valor 5 não supera por si só a ordem padrão de tipos diferentes.
- **Pilha:** é uma cópia do histórico, consultada em ordem inversa; retirar o topo não desfaz um pouso. O enunciado não exige desfazer ações.
- **Memória e tempo:** concatenação e reconstrução de listas, contagem por laço e duplicação do histórico têm custo. O objetivo principal é pedagógico, sem medições de desempenho em hardware embarcado.
- **Cadastro:** ocorre por edição das listas; não há menu interativo. O enunciado fornecido não exige interface gráfica ou formulário.

## Organização e rastreabilidade

`README.MD` e `LEIA-ME.txt` indicam corretamente `mgpeb.py` como programa atual. `main.py` é um experimento de descida separado e não deve ser apresentado como o sistema integrado. `ROADMAP.MD` reúne anotações e ideias que incluem recursos não implementados; é recomendável separar futuramente decisões vigentes de propostas antigas.

O `LEIA-ME.txt` cita capítulos e páginas do curso. Os PDFs correspondentes não estão nesta cópia local; a revisão não verificou essa correspondência página a página. O teste AST aplica restrições adicionais de sintaxe que não estão expressas no enunciado fornecido; tratam-se de convenções herdadas do projeto, não de exigências confirmadas da FIAP.

## Validação realizada

- `python -m unittest -v`: oito testes aprovados.
- `python mgpeb.py`: execução padrão concluída; cinco módulos operacionais, 25 minutos e 20 kg restantes por módulo.
- `python exemplos.py`: onze cenários executados.
- Conferência adicional da autorização nas 32 combinações booleanas: resultados coerentes com `C AND S AND E AND A AND D`.
- Conferência dos limites no cenário de massa de 1.000 kg: 11,999 kg bloqueado; 12 e 15 kg aptos e urgentes; 15,001 kg apto e não urgente.
- Casos malformados e falha pós-pouso: reproduziram os achados 1 e 2.
- PDF: 10 páginas; inspeção visual das páginas renderizadas e conferência das quatro URLs nas anotações de links.

Validação executada com Python 3.12. Dependências documentais verificadas: ReportLab 4.4.9 e svglib 2.3.0. O simulador usa apenas recursos da linguagem e não depende desses pacotes.

## Ajustes técnicos incluídos nesta integração

O gerador de PDF tinha uma expressão regular que truncava URLs em caracteres como `t`, `l` e `g`, pois entidades HTML haviam sido usadas dentro de uma classe de caracteres. A expressão foi corrigida e os links do PDF foram conferidos. Também foi mantido o gráfico junto à legenda.

A instalação anterior de `svglib>=1.5,<2` selecionou a versão 1.6.0 e tentou compilar Cairo, falhando neste Mac por ausência de dependências nativas. O intervalo foi atualizado para `svglib>=2.3,<3`; a versão 2.3.0 instalou e gerou o PDF neste ambiente. Isso confirma a combinação testada, não todos os sistemas ou versões de Python.
