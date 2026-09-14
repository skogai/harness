# Projeto 05: Loops de Avaliação e Evoluções com Três Papéis

Meça como a separação de papéis (um único papel, gerador mais avaliador, planejador mais gerador mais avaliador) altera a qualidade da implementação.

## Guia de Diretórios

| Diretório | Significado |
|------|------|
| `starter/` | **Ponto de partida**: baseado na solução do P4, com o histórico de conversas em múltiplas interações ainda pendente de implementação. |
| `solution/single-role/` | **Variante A**: um agente faz todo o trabalho (planejamento, implementação e autoavaliação). Qualidade de referência inicial. |
| `solution/gen-eval/` | **Variante B**: padrão de gerador mais avaliador. Maior qualidade, com evidências de revisão. |
| `solution/plan-gen-eval/` | **Variante C**: planejador mais gerador mais avaliador. Maior qualidade, com contrato de sprint e critérios de pontuação. |

## Como Usar

```sh
# Comece pelo starter se quiser executar o exercício por conta própria.
cd starter
npm install
# Implemente a mesma evolução do ConversationHistory três vezes usando a configuração de papéis abaixo.

# Inspecione as três variantes de referência independentemente
cd solution/single-role && npm install  # modo de papel único
cd solution/gen-eval && npm install     # modo gerador mais avaliador
cd solution/plan-gen-eval && npm install # modo completo com três papéis

# Compare as três variantes:
# - Qualidade do código (pontuação do evaluator-rubric.md)
# - Quantidade de defeitos encontrados
# - Quantidade de retrabalho necessário
```

## Contrato Exato da Tarefa

A evolução do produto para as soluções versionadas é fixa: implemente o histórico de
perguntas e respostas em múltiplas interações usando `ConversationHistory`. Os três
diretórios de solução não são etapas sequenciais; são três execuções independentes da
mesma funcionalidade com diferentes papéis de harness.

| Variante | O que demonstra | Evidência para inspecionar |
|------|------|------|
| `starter/` | Aplicação baseada no P4 antes da evolução de histórico de conversas | `src/renderer/components/ConversationHistory.tsx`, `App.tsx` |
| `solution/single-role/` | Um agente planeja, implementa e faz sua própria revisão | Pontuação 1.6/5 do `evaluator-rubric.md` e defeitos listados |
| `solution/gen-eval/` | Gerador e avaliador separados com evidências de revisão | Pontuação 3.3/5 do `evaluator-rubric.md` e notas de revisão |
| `solution/plan-gen-eval/` | Planejador + gerador + avaliador com um contrato de sprint | `sprint-contract.md`, pontuação 4.9/5 do `evaluator-rubric.md` |

Mantenha a funcionalidade constante ao executar novamente o projeto. Alterar a
funcionalidade entre as variantes invalida a comparação, pois a separação de papéis é
a única variável pretendida.

## Funcionalidades Cobertas

- Histórico de QA em múltiplas interações (interface conversacional)
- Contrato de sprint
- Ajuste de critérios de avaliação do avaliador

## Aulas Relacionadas

- [Aula 09: Por Que Agentes Declaram Vitória Cedo Demais](../../docs/pt-BR/lectures/lecture-09-why-agents-declare-victory-too-early/index.md)
- [Aula 10: Por Que Testes End-to-End Alteram os Resultados](../../docs/pt-BR/lectures/lecture-10-why-end-to-end-testing-changes-results/index.md)