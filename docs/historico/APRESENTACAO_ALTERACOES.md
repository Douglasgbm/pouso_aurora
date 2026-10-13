# Aurora Siger — apresentação das alterações e revisão

Apresentação histórica da integração documental, anterior às correções 1.1. Revisão de 6 de outubro de 2026. As pendências abaixo foram tratadas depois; consultar `GUIA_DETALHADO.md` e a atualização de `REVISAO_PROJETO.md` para o estado atual.

## Slide 1 — Objetivo desta entrega

**O que foi feito:** incorporação dos itens 5 e 6 do enunciado ao relatório técnico, atualização do PDF e revisão do projeto completo.

**Por quê:** o trabalho precisa explicar tanto as decisões computacionais quanto as consequências ambientais, sociais e de governança da base.

**Escopo:** documentação e geração do relatório. A lógica do simulador continua na versão 1.0; os problemas encontrados nela foram registrados para uma próxima correção.

## Slide 2 — Parte 5: evolução da computação

- O texto relaciona o ENIAC, a miniaturização e o uso de computadores embarcados nas missões Apollo.
- O MGPEB aparece como aplicação didática: recebe dados, avalia condições e organiza decisões.
- O exemplo concreto é um módulo prioritário que continua bloqueado quando os sensores falham.

**Por quê:** o requisito pede uma conexão com o sistema projetado, e não apenas uma cronologia de computadores. Fontes históricas e da NASA estão identificadas no relatório.

## Slide 3 — Parte 5: hardware e algoritmos

- Foram discutidos memória, processamento, energia, temperatura e radiação.
- O Perseverance ilustra um caso real; suas especificações não são impostas à base fictícia.
- Listas, busca linear e ordenação por inserção foram relacionadas ao cenário pequeno e ao aprendizado.
- O texto reconhece cópias de listas, contagens por laço e crescimento do histórico.

**Por quê:** clareza didática não demonstra eficiência para voo espacial. O relatório precisa justificar escolhas e admitir seus custos. Booleanos que representam sensores não implementam proteção física contra radiação.

## Slide 4 — Parte 6: ambiente e recursos

- A área de pouso considera segurança, dispersão de poeira, proteção de instalações e preservação de regiões científicas.
- A proposta energética considera geração, armazenamento e reserva para serviços essenciais.
- Água, resíduos e produção local recebem critérios de controle, recuperação e avaliação de impactos.

**Por quê:** sustentabilidade precisa aparecer em decisões concretas. Utilizar recursos locais não é suficiente para garantir baixo impacto.

## Slide 5 — Parte 6: pessoas e governança

- Prioridades devem considerar necessidades essenciais e consequências da perda de cargas.
- Propõem-se treinamento, canais de relato sem retaliação e participação de diferentes áreas.
- Mudanças nas regras precisam de justificativa e revisão; emergências devem seguir procedimentos acordados.
- Os registros futuros devem conter horário, módulo, motivo e versão da regra, com proteção de dados pessoais.

**Por quê:** o algoritmo distribui oportunidades de pouso e influencia a organização da base. Seus critérios devem ser compreensíveis e passíveis de revisão. O histórico atual em memória ainda não é uma auditoria persistente.

## Slide 6 — Integração documental

| Arquivo | Alteração | Motivo |
|---|---|---|
| `RELATORIO_TECNICO.md` | Parte 5 reúne história e hardware; parte 6 desenvolve ESG; conclusão passa a ser seção 7 | Alinhar a numeração ao enunciado e evitar duplicações |
| `RELATORIO_TECNICO.pdf` | Regenerado com 10 páginas | Entregar a mesma versão do texto editável, respeitando o limite |
| `gerar_relatorio_pdf.py` | Corrigidos os links e a manutenção do gráfico junto à legenda | Referências utilizáveis e melhor leitura |
| `requirements-relatorio.txt` | Atualizado o intervalo do svglib para a versão 2.3 testada | A instalação anterior tentou compilar Cairo e falhou neste ambiente |
| `docs/partes_5_e_6_rascunho.md` | Preservado como rascunho histórico, com aviso da integração | Manter a origem do texto sem confundir a versão de entrega |
| `README.MD` | Links para apresentação, revisão e instrução para gerar o PDF | Facilitar a consulta da equipe |

A seção 2 foi identificada como anexo integrado de estruturas de dados. As referências das novas partes foram consolidadas em quatro fontes citadas no corpo. A autoria histórica do repositório foi preservada.

## Slide 7 — Evidências da revisão

- Os oito testes existentes passaram.
- A demonstração padrão e os onze cenários executaram.
- Foram conferidas as 32 combinações das cinco condições de autorização.
- Foram verificados os limites de combustível de 11,999; 12; 15 e 15,001 kg no cenário padrão.
- O PDF final tem 10 páginas; as páginas foram renderizadas para inspeção visual e os quatro links das referências foram verificados no arquivo.

Esses resultados sustentam o comportamento dos casos conferidos. Não representam validação aeroespacial nem garantia de ausência de falhas.

## Slide 8 — Considerações e próximos ajustes

**Avaliação:** o projeto reúne os conteúdos centrais da atividade e possui uma base funcional para a apresentação acadêmica. As partes 5 e 6 agora explicam escolhas e propostas com relação explícita ao MGPEB.

**Pendências prioritárias:** definir o tratamento de falhas após o pouso, melhorar a validação de entradas malformadas, atualizar a saída salva dos exemplos, apresentar as portas lógicas com símbolos gráficos e preencher os integrantes da equipe.

**Decisões de escopo:** a descida é atômica; não há consumo em órbita; a pilha serve para consulta; o histórico não é permanente. Essas escolhas devem ser explicadas na defesa do projeto. Não é necessário transformar este protótipo em um sistema de voo para atender à atividade.

Detalhes e reproduções: [revisão do projeto](REVISAO_PROJETO.md).
