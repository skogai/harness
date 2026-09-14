# Skills

Este diretório contém skills reutilizáveis de agentes de IA para o projeto Learn Harness Engineering. Cada skill é um template de prompt independente que pode ser carregado por agentes de programação com IA (Claude Code, Codex, Cursor, Windsurf, etc.) para executar tarefas especializadas.

## Skills Disponíveis

### harness-creator

Skill de engenharia de harness para agentes de programação com IA em ambientes de produção. Ajuda a criar, avaliar e melhorar arquivos de harness de agentes (`AGENTS.md`, listas de funcionalidades, fluxos de verificação, mecanismos de continuidade de sessão).

- **7 padrões de referência**: Persistência de Memória, Runtime de Skills, Engenharia de Contexto, Registro de Ferramentas, Coordenação Multiagente, Ciclo de Vida e Bootstrap, Armadilhas
- **Templates**: `AGENTS.md`/`CLAUDE.md`, `feature-list.json`, `init.sh`, `progress.md`, `session-handoff.md`
- **Scripts**: criação de estrutura, validação, renderização de avaliação em HTML, execução de benchmark estrutural
- **10 casos de teste de avaliação integrados**

Consulte [harness-creator/README.md](harness-creator/README.md) para a documentação completa.

## Como o harness-creator Foi Criado

A skill `harness-creator` foi desenvolvida usando a metodologia **skill-creator** — a meta-skill oficial da Anthropic para criar, testar e iterar sobre skills de agentes. O skill-creator fornece um fluxo de trabalho estruturado (rascunho → teste → avaliação → iteração) com executores de avaliação, avaliadores e um visualizador de benchmark integrados.

- **Fonte do skill-creator**: [anthropics/skills — skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
- **Documentação de skills do Claude Code da Anthropic**: [anthropics/claude-code — plugin-dev/skills](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills)

## Estrutura de Diretórios
```
skills/
├── README.md                    # Este arquivo
├── README-CN.md                 # Versão em chinês
├── README-ZH-TW.md              # Versão em chinês tradicional
├── README-JA.md                 # Versão em japonês
├── README-ES.md                 # Versão em espanhol
├── README-FR.md                 # Versão em francês
├── README-AR.md                 # Versão em árabe
├── README-VI.md                 # Versão em vietnamita
├── README-DE.md                 # Versão em alemão
├── README-TR.md                 # Versão em turco
├── README-PT-BR.md              # Versão em português (Brasil)
└── harness-creator/             # Skill de engenharia de harness
    ├── SKILL.md                 # Definição principal do skill
    ├── SKILL.md.en              # Versão apenas em inglês
    ├── README.md                # Documentação detalhada
    ├── metadata.json            # Metadados e gatilhos do skill
    ├── agents/                  # Metadados da UI do skill
    ├── scripts/                 # Auxiliares de scaffold, validação, benchmark
    ├── evals/                   # Casos de teste
    ├── templates/               # Templates de scaffold
    └── references/              # Documentos de padrões detalhados
```

## Como as Skills Funcionam

Cada skill segue uma estrutura padrão:

1. **SKILL.md** — O ponto de entrada. Contém frontmatter YAML (nome, descrição para acionamento) e instruções em Markdown para o agente.
2. **references/** — Documentos adicionais carregados no contexto conforme necessário.
3. **templates/** — Templates iniciais que a skill pode gerar para os usuários.

As skills utilizam divulgação progressiva — o agente primeiro visualiza apenas o nome + descrição, depois carrega o conteúdo completo do SKILL.md quando acionado e lê os recursos incluídos somente quando necessário.

## Auditoria de Segurança

Todos os arquivos deste diretório foram auditados para segurança:

- Sem backdoors, URLs ocultas ou payloads codificados
- Sem exfiltração de dados ou credenciais armazenadas diretamente no código
- Sem vulnerabilidades de injeção de comandos
- Os scripts utilizam apenas módulos nativos do Node.js
- O `init.sh` gerado executa comandos de verificação detectados do projeto

## Licença

MIT