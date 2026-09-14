# Projeto 04: Feedback em Tempo de Execução e Controle Estrutural

Introduza observabilidade em tempo de execução e verificações de limites estruturais enquanto depura um defeito de execução pré-configurado.

## Guia de Diretórios

| Diretório | Significado |
|------|------|
| `starter/` | **Ponto de partida**: baseado na solução do P3, com recursos de logging e limites estruturais ainda pendentes de implementação. O `IndexingService` contém um bug oculto pré-configurado: arquivos com mais de 1000 caracteres podem gerar chunks vazios. Não existe script de verificação de arquitetura nem checklist final de estado limpo. |
| `solution/` | **Implementação de referência**: módulo de logging estruturado, script de verificação de limites de arquitetura e o bug pré-configurado corrigido. |

## Como Usar

```sh
cd starter
npm install
# 1. Observe se o agente consegue localizar o bug através dos logs
# 2. Importe um arquivo grande e verifique se o comportamento de divisão em chunks está incorreto

cd ../solution
npm install
# Compare como logs estruturados aceleram o diagnóstico
```

## Contrato Exato da Tarefa

O Projeto 04 é um exercício de depuração e criação de proteções. O starter já contém
o recorte de produto do Projeto 03, mas o ambiente de execução é mais difícil de
inspecionar e o defeito de divisão em chunks pré-configurado deve ser corrigido somente
depois que o agente conseguir visualizar evidências suficientes.

| Funcionalidade / artefato | Estado no Starter | Evidência da Solution |
|------|------|------|
| Logging estruturado | Não existe um serviço de logger compartilhado | `src/services/logger.ts`, chamadas de logging em `main.ts`, `ipc-handlers.ts` e serviços |
| Diagnósticos de importação / indexação | Falhas são difíceis de rastrear a partir da saída de execução | Entradas de log ao redor da importação, início/conclusão da indexação e caminhos de falha do QA |
| Limites de arquitetura | Não existe script que verifique desvios entre limites de renderer/main/service | `scripts/check-architecture.sh`, `docs/ARCHITECTURE.md`, regras de limites no AGENTS |
| Bug pré-configurado de divisão em chunks | Arquivos grandes podem gerar saída de chunks inválida/vazia | Lógica de parágrafos/chunks corrigida em `src/services/indexing-service.ts` |
| Handoff limpo | O Starter não possui checklist final | `clean-state-checklist.md` |

Use um documento de exemplo longo para reproduzir o bug antes e depois da correção.
Uma solução bem-sucedida deve apresentar tanto alterações no código quanto evidências
de diagnóstico, não apenas uma afirmação de que passou.

## Funcionalidades Cobertas

- Logs de inicialização
- Logs de importação e indexação
- Caminho de falha do QA visível
- Limites explícitos entre as camadas main, preload, renderer e services
- Depuração de um defeito de execução pré-configurado

## Aulas Relacionadas

- [Aula 07: Por Que Agentes Extrapolam o Escopo e Não Finalizam](../../docs/pt-BR/lectures/lecture-07-why-agents-overreach-and-under-finish/index.md)
- [Aula 08: Por Que Listas de Funcionalidades São Primitivas de Harness](../../docs/pt-BR/lectures/lecture-08-why-feature-lists-are-harness-primitives/index.md)