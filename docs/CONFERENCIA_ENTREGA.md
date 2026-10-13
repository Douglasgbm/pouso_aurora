# Conferência da entrega obrigatória — 13 de outubro de 2026

Referência: documento “PBL Aurora 2.docx” fornecido pela equipe. A conferência trata o HTML como extra, conforme orientação de Marcelo.

## Resultado

Código, exemplos e PDF da equipe conferidos. RELATORIO_FINAL_EQUIPE.pdf tem 10 páginas e inclui o anexo na página 3. A revisão por página está em REVISAO_PDF_FINAL.md. RELATORIO_TECNICO.pdf permanece como apoio. O envio no portal cabe à equipe.

| Exigência | Evidência no projeto | Situação |
|---|---|---|
| Cenário, módulos e atributos | Cinco tipos e cadastro de 12 campos em mgpeb.py; seção 1 do relatório | Atendido |
| Fila e listas auxiliares | fila, espera, pousados e alertas; seção 2 | Atendido |
| Portas e decisões booleanas | autorizar, AND/OR/NOT em docs/portas_logicas.svg; seção 3 | Atendido |
| Protótipo Python simples e comentado | mgpeb.py, sem importações; funções de busca, ordenação e simulação | Atendido |
| Exemplos executáveis | exemplos.py e exemplos_saida.txt, 14 cenários | Atendido |
| Função matemática e análise | C(t)=k*m*t; F(t)=C(t)+R; unidades, parâmetros, gráfico e autorização na seção 4 | Atendido no PDF final |
| Evolução da computação e hardware | Seção 5 e 5.1, com consequências para programação e estruturas | Atendido no PDF final |
| ESG e governança | Seção 6: pouso, recursos, resíduos, energia e participação | Atendido no PDF final |
| Anexo com exemplos concretos | Seção 2, cenário urgente: fila/espera, aptos, pousados e pilha | Atendido no PDF final, página 3 |
| PDF de 5 a 10 páginas | RELATORIO_FINAL_EQUIPE.pdf tem 10 páginas | Atendido |

## Validação nesta conferência

- 46 testes aprovados (22 do simulador, 11 do exportador, 4 da transmissão e 9 do roteiro).
- 13 verificações da auditoria aprovadas.
- JavaScript conferido nos 15 cenários em ambos os modos, com DOM simulado; teste pontual de visualização e navegação também realizado no site publicado.
- PDF de apoio de 10 páginas e guia de estudo separados, renderizados para inspeção.
- Programa principal executado sem dependências externas.
- Os 14 exemplos reproduzem exatamente exemplos_saida.txt em UTF-8.
- Código obrigatório também verificado isoladamente, sem HTML, exportador, testes ou geradores de documentos.

## Conteúdo preservado no PDF final

1. Descrição do cenário e dos módulos.
2. Diagramas e expressão correta: NOT(NOT S OR NOT E) = S AND E.
3. Modelagem matemática, unidades, parâmetros, análise gráfica e relação com a autorização. Consumo linear; mínimo com reserva afim.
4. Contextualização histórica e limitações de hardware.
5. ESG e governança, identificando propostas que o simulador não implementa.
6. Anexo da seção 2 com exemplos concretos de listas, fila e pilha.
7. Limite total de 5 a 10 páginas, incluindo o anexo quando integrado, e identificação da equipe conforme o portal.

O documento recebido não exige HTML, NumPy ou Matplotlib. O núcleo acadêmico não depende deles. O código de apresentação usa recursos adicionais e está identificado como complemento.

Esta conferência não promete nota máxima nem substitui a avaliação docente. Não há pendência conhecida de implementação nos requisitos obrigatórios verificados.
