# Projeto 02: Workspace Legível por Agentes

Demonstre como a legibilidade do repositório e artefatos explícitos de continuidade reduzem a perda de contexto durante o desenvolvimento em múltiplas sessões.

## Guia de Diretórios

| Diretório | Significado |
|------|------|
| `starter/` | **Ponto de partida**: baseado na solução do P1, com importação de documentos, visualização de detalhes e persistência ainda pendentes de implementação. O harness é fraco: o `AGENTS.md` é mínimo e não existe um handoff de sessão. |
| `solution/` | **Implementação de referência**: todos os novos recursos estão implementados, com documentação completa do workspace (`ARCHITECTURE.md`, `PRODUCT.md`, `session-handoff.md`). |

## Como Usar

```sh
# Requer pelo menos 2 sessões de agente para concluir
cd starter
npm install
# Sessão A: implemente a importação de documentos e a visualização de detalhes
# Sessão B: implemente a persistência (observe se o agente recupera rapidamente o contexto)

cd ../solution
npm install
# Execute novamente com o harness completo e compare a velocidade de recuperação da sessão
```

## Contrato Exato da Tarefa

Comece a partir de `starter/`. O starter já contém o shell do Projeto 01 e um
harness mínimo. O trabalho é adicionar o recorte de produto do Projeto 02 e a
documentação do workspace que permite que uma segunda sessão recupere o contexto rapidamente.

| Funcionalidade / artefato | Estado no Starter | Evidência da Solution |
|------|------|------|
| Importação de documentos | O fluxo de importação está incompleto entre renderer, preload, IPC e `DocumentService` | `src/renderer/components/ImportPanel.tsx`, `src/main/ipc-handlers.ts`, `src/services/document-service.ts` |
| Detalhes do documento | O painel de detalhes não carrega nem renderiza o conteúdo completo do arquivo via IPC | `src/renderer/components/DocumentDetail.tsx`, `IPC_CHANNELS.GET_DOCUMENT_CONTENT` |
| Persistência básica | Documentos importados não são totalmente restaurados após reinicialização | `src/services/persistence-service.ts`, tratamento de `documents-meta.json` |
| Estado legível pelo agente | Não existe arquivo final de handoff no starter | `session-handoff.md`, `docs/ARCHITECTURE.md` expandido, `docs/PRODUCT.md` expandido |

Execute isso como um exercício de duas sessões. Encerre a Sessão A antes que as três
funcionalidades do produto estejam completas e, em seguida, inicie a Sessão B usando
apenas o estado atual do repositório. A principal comparação é o quanto mais rápido
a Sessão B consegue retomar quando `session-handoff.md` e a documentação existem.

## Funcionalidades Cobertas

- Fluxo de importação de documentos (seletor de arquivos mais transferência via IPC)
- Visualização de detalhes do documento (metadados mais exibição do conteúdo)
- Persistência básica (documentos importados permanecem após reinicialização)

## Aulas Relacionadas

- [Aula 03: Por Que o Repositório Deve se Tornar a Fonte Oficial da Verdade](../../docs/pt-BR/lectures/lecture-03-why-the-repository-must-become-the-system-of-record/index.md)
- [Aula 04: Por Que Um Único Arquivo Gigante de Instruções Falha](../../docs/pt-BR/lectures/lecture-04-why-one-giant-instruction-file-fails/index.md)