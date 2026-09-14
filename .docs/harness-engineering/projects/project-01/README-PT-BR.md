# Projeto 01: Baseline vs. Harness Mínimo

Compare como um harness fraco (apenas prompt) e um harness explícito (arquivos de regras mais mecanismos de verificação) afetam a taxa de conclusão de tarefas de agentes de programação com IA.

## Guia de Diretórios

| Diretório | Significado |
|------|------|
| `starter/` | **Ponto de partida**: apenas um `task-prompt.md` vago, sem `AGENTS.md` e sem `feature_list.json`. Esta é a versão de "harness fraco" que você entrega ao agente. |
| `solution/` | **Implementação de referência**: o mesmo código da aplicação, mas com arquivos completos de harness (`AGENTS.md`, `feature_list.json`, `init.sh`, `claude-progress.md`). Esta é a versão de "harness explícito". |

## Como Usar

```sh
# 1. Execute a tarefa do agente uma vez com starter (harness fraco)
cd starter
npm install
# Forneça o conteúdo de task-prompt.md como prompt para Claude Code / Codex
# Peça ao agente para concluir: inicialização da janela, lista de documentos, painel de QA, diretório de dados
# Não forneça os arquivos da solução ao agente durante esta execução.

# 2. Execute a mesma tarefa com solution (harness explícito)
cd ../solution
npm install
# Peça ao agente para ler AGENTS.md, init.sh, feature_list.json e claude-progress.md
# antes de alterar o código. O código do produto já deve satisfazer as mesmas quatro funcionalidades.

# 3. Compare os dois resultados
# - A tarefa foi concluída?
# - Quantas tentativas adicionais foram necessárias?
# - O agente afirmou "concluído" cedo demais?
```

## Contrato Exato da Tarefa

O prompt inicial é intencionalmente vago (`starter/task-prompt.md` contém apenas
"Construa uma aplicação Electron que possa exibir documentos e responder perguntas."). Use o harness da solução para tornar essa solicitação vaga concreta:

| Funcionalidade | Evidência do Starter para inspecionar | Evidência da Solution para comparar |
|------|------|------|
| Inicialização da janela | `src/main/main.ts`, `src/preload/preload.ts` | Item `window-launch` do `feature_list.json` |
| Painel de lista de documentos | `src/renderer/components/DocumentList.tsx` | Item `document-list` do `feature_list.json` |
| Painel de perguntas | `src/renderer/components/QuestionPanel.tsx` | Item `question-panel` do `feature_list.json` |
| Diretório de dados | `src/services/persistence-service.ts` | Item `data-directory` do `feature_list.json` |

Este projeto é um experimento, não uma tarefa comum de "preencher o starter até que ele seja igual à solução". O resultado de aprendizado é a diferença medida entre uma execução baseada apenas em prompt e uma execução que começa com regras explícitas do repositório e artefatos de verificação.

## Funcionalidades Cobertas

- A janela do Electron inicia com sucesso
- A interface exibe a área da lista de documentos
- A interface exibe o painel de QA
- A aplicação cria e utiliza um diretório de dados local

## Aulas Relacionadas

- [Aula 01: Por Que Agentes Capazes Ainda Falham](../../docs/pt-BR/lectures/lecture-01-why-capable-agents-still-fail/index.md)
- [Aula 02: O Que É Um Harness na Prática](../../docs/pt-BR/lectures/lecture-02-what-a-harness-actually-is/index.md)
