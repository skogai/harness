# Projeto 08. Desenhe Seu Fluxo de Trabalho como um Grafo

> Aula relacionada: [L14. Do Loop Único à Engenharia de Grafos](./../../lectures/lecture-14-graph-engineering/index.md)

## O Que Você Vai Fazer

Este é o projeto de transição de "Loop" para "Graph". Na aula anterior você montou um maker-checker loop — implementar, verificar, feedback, implementar de novo — e todas as decisões acontecem dentro da janela de contexto do mesmo agente. O que você vai fazer nesta aula é **desenhar explicitamente a estrutura escondida dentro do loop**: nós, arestas, estado compartilhado e regras de roteamento, escritos com clareza, palavra por palavra.

Você fará três experimentos progressivos: primeiro, desenhar o maker-checker loop do P07 como um grafo explícito; depois, adicionar um nó paralelo de fan-out/fan-in; e, por fim, adicionar uma aresta de rollback condicional e um nó de aprovação humana. Ao terminar, você vai sentir na prática uma coisa: **o grafo não é uma invenção nova — é o que o seu loop vira sozinho quando fica complexo o suficiente.**

## Quais Ferramentas Usar

- Claude Code ou Codex
- Git
- O maker-checker loop que você montou no P07 (ou qualquer fluxo de trabalho de agente que você consiga rodar repetidamente)
- Um editor de texto ou ferramenta de desenho (desenhar não é para ficar bonito, é para escrever a estrutura com clareza; `mermaid` ou `graph.md` escrito à mão servem)

## Passos Concretos

### Preparação

1. Comece do repositório que você terminou no P07, ou use diretamente qualquer fluxo de trabalho de agente que esteja rodando.
2. Crie três branches: `p08-explicit-graph`, `p08-parallel` e `p08-human-in-the-loop`.
3. Prepare um `state.md` como arquivo de estado compartilhado: requisitos, progresso e resultados de verificação são escritos aqui. Essa é a "mesa de trabalho pública" do grafo.

### Experimento 1: Desenhe o Loop como um Grafo Explícito

Mude para a branch `p08-explicit-graph`.

1. **Liste todos os nós**: escreva cada passo do maker-checker loop do P07 como um nó. Para cada nó, escreva com clareza: sua responsabilidade, sua entrada, sua saída e se é um agente ou código determinístico.
2. **Desenhe todas as arestas**: liste cada aresta entre os nós. Destaque duas arestas especiais:
   - Aresta condicional: verificação passa/falha, para onde vai
   - Aresta de rollback: para qual nó a falha volta
3. **Escreva o estado compartilhado**: liste explicitamente quais campos há no estado (requisitos, código, resultados de teste, conclusões de revisão) e quem lê e quem escreve cada um.
4. **Escreva as regras de roteamento**: usando a linguagem if-then mais simples, escreva as regras de "para onde ir em seguida", por exemplo:
   ```
   if a verificação passa → nó de merge
   if a verificação falha → nó de implementação
   if o nó de implementação tem informação insuficiente → nó de pesquisa
   ```
5. **Escreva em `graph.md`**: organize o conteúdo acima em um documento. Use mermaid para desenhar um grafo, anexando a tabela de nós e as regras de roteamento.
6. **Responda a esta pergunta**: depois de desenhar, encontre pelo menos uma **aresta que era implícita** — um caminho de decisão que antes estava escondido no contexto do agente e cuja existência você nem conhecia.

### Experimento 2: Adicione um Nó de Fan-out / Fan-in Paralelo

Mude para a branch `p08-parallel`.

1. **Escolha um ponto que possa ser paralelizado**: encontre um lugar na tarefa que possa ser dividido em duas partes independentes. Por exemplo:
   - Implementação dividida em dois módulos independentes, dois agentes escrevendo em paralelo
   - Verificação dividida em duas revisões independentes: uma roda testes e lint, outra faz revisão de código (instruções diferentes, focos diferentes)
   - Pesquisa dividida em duas direções, cada agente investigando um caminho
2. **Escreva as regras de fan-out**: registre no estado compartilhado que "esta tarefa foi dividida em N subtarefas paralelas", cada uma com um context independente e um nó independente.
3. **Escreva as regras de fan-in**: quando todas as subtarefas terminarem, quem mescla os resultados? Qual é o critério de mesclagem (por exemplo: só mesclamos se as duas revisões passarem, ou basta uma passar)?
4. **Use worktree para isolar**: cada subtarefa paralela roda em um git worktree independente, evitando fisicamente colisões de arquivos (reveja a primitiva Worktree da aula 13).
5. **Rode uma vez e registre**: registre o tempo de wall-clock, o consumo de tokens e a qualidade dos resultados antes e depois do paralelismo. O paralelismo realmente foi mais rápido? Ou o custo de coordenação comeu o tempo economizado?

### Experimento 3: Adicione uma Aresta de Rollback e um Nó de Aprovação Humana

Mude para a branch `p08-human-in-the-loop`.

Este é o mais importante dos três experimentos. Você vai adicionar dois tipos de nó ao grafo:

1. **Aresta de rollback condicional**: adicione ao nó de verificação um caminho de "aprovação parcial" — em vez de devolver tudo para o nó de implementação, volte com feedback específico para o **nó que causou o problema**. Por exemplo: se todos os testes passam, mas a revisão de código descobriu que a compreensão dos requisitos estava errada, volte para o nó de pesquisa, não para o de implementação. Isso exige que seu estado compartilhado registre "em qual camada está o problema".
2. **Nó de aprovação humana (Human-in-the-loop)**: adicione um nó humano antes do nó de merge. Ao chegar aqui, o grafo **para**, e espera você escrever "aprovar" ou "rejeitar" no `state.md`. O nó de aprovação pode ter uma regra de timeout: se não houver resposta em N horas, rejeita ou promove automaticamente.
3. **Escreva o formato do interrupt**: como escrever com clareza a solicitação de aprovação — o que aconteceu, o que foi alterado, por que é necessária uma pessoa e quais são as consequências de aprovar/rejeitar.
4. **Rode pelo menos 2 ciclos completos**: em cada ciclo, chegue ao nó de aprovação humana e você mesmo aprova ou rejeita uma vez. Registre: sua decisão de aprovação foi consistente com o julgamento do nó de verificação? O nó de aprovação bloqueou algo que o nó de verificação não bloqueou?

## Como Medir os Resultados

| Métrica | Experimento 1 (grafo explícito) | Experimento 2 (paralelo) | Experimento 3 (humano no loop) |
|------|----------------|--------------|------------------|
| Visibilidade da estrutura | Quantas arestas implícitas você encontrou? | O estado compartilhado consegue suportar as subtarefas paralelas? | A aresta de rollback consegue localizar com precisão a camada do problema? |
| Localização de falhas | Quando algo falha, você consegue apontar diretamente qual aresta errou? | Quando uma subtarefa paralela falha, você consegue localizar qual delas? | Quando a aprovação rejeita, você consegue apontar de qual camada é o problema? |
| Custo de colaboração | Quanto tempo demorou para escrever o grafo? | Tempo economizado pelo paralelismo vs. custo de coordenação | Tempo de espera da aprovação vs. valor do problema bloqueado |
| Observabilidade | O que acontece em cada passo, agora fica visível? | O status de cada subtarefa paralela fica visível? | A solicitação de aprovação está escrita com clareza o suficiente? |
| Confiabilidade | A descrição do grafo condiz com a execução real? | O critério de mesclagem do fan-in é confiável? | As regras de timeout/promoção realmente disparam? |

## O Que Entregar

- `graph.md` (a descrição completa do grafo do experimento 1: diagrama mermaid + tabela de nós + tabela de arestas + campos do estado compartilhado + regras de roteamento)
- A lista de arestas implícitas encontradas no experimento 1 (pelo menos uma)
- As regras de fan-out/fan-in do experimento 2 e o registro de uma execução paralela (comparação de tempo/custo/qualidade)
- As regras de aresta de rollback do experimento 3, o formato do nó de aprovação e o registro de 2 ciclos de colaboração humano-agente
- O balanço final: do loop ao grafo, o que mudou na sua forma de trabalhar? Quais tarefas valem a pena desenhar como grafo e quais não?

## Aulas Relacionadas

- [Lecture 14 — Do Loop Único à Engenharia de Grafos](../../lectures/lecture-14-graph-engineering/index.md)
- [Lecture 13 — Do Prompting Manual aos Loops Autônomos](../../lectures/lecture-13-loop-engineering/index.md) (seu loop é um nó dentro do grafo; este projeto é para abrir a estrutura interna do nó)
- [Lecture 09 — Por Que os Agentes Declaram Vitória Cedo Demais](../../lectures/lecture-09-why-agents-declare-victory-too-early/index.md) (por que o nó de verificação deve ser independente do nó de implementação; no grafo, é um problema estrutural)
- [Lecture 11 — Por Que a Observabilidade Pertence ao Harness](../../lectures/lecture-11-why-observability-belongs-inside-the-harness/index.md) (quanto mais complexo o grafo, mais você precisa ver o que cada nó está fazendo)