<p align="center">
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/English-d9d9d9"></a>
  <a href="README-CN.md"><img alt="简体中文" src="https://img.shields.io/badge/简体中文-d9d9d9"></a>
  <a href="README-ZH-TW.md"><img alt="繁體中文" src="https://img.shields.io/badge/繁體中文-d9d9d9"></a>
  <a href="README-JA.md"><img alt="日本語" src="https://img.shields.io/badge/日本語-d9d9d9"></a>
  <a href="README-ES.md"><img alt="Español" src="https://img.shields.io/badge/Español-d9d9d9"></a>
  <a href="README-FR.md"><img alt="Français" src="https://img.shields.io/badge/Français-d9d9d9"></a>
  <a href="README-KO.md"><img alt="한국어" src="https://img.shields.io/badge/한국어-d9d9d9"></a>
  <a href="README-AR.md"><img alt="العربية" src="https://img.shields.io/badge/العربية-d9d9d9"></a>
  <a href="README-VI.md"><img alt="Tiếng_Việt" src="https://img.shields.io/badge/Tiếng_Việt-d9d9d9"></a>
  <a href="README-DE.md"><img alt="Deutsch" src="https://img.shields.io/badge/Deutsch-d9d9d9"></a>
  <a href="README-TR.md"><img alt="Türkçe" src="https://img.shields.io/badge/Türkçe-d9d9d9"></a>
  <a href="README-PT-BR.md"><img alt="Português (Brasil)" src="https://img.shields.io/badge/Português (Brasil)-d9d9d9"></a>
  <a href="README-UK.md"><img alt="Українська" src="https://img.shields.io/badge/Українська-d9d9d9"></a>
</p>

# Skills

Цей каталог містить багаторазові навички (skills) для AI-агентів проєкту Learn Harness Engineering. Кожна навичка — це самодостатній шаблон промту, який AI-агенти для написання коду (Claude Code, Codex, Cursor, Windsurf тощо) можуть завантажити для виконання спеціалізованих задач.

## Доступні навички

### harness-creator

Навичка для інженерії harness виробничого рівня для AI-агентів написання коду. Допомагає створювати, оцінювати та покращувати файли harness агента (AGENTS.md, списки функціональності, процеси верифікації, механізми безперервності сесій).

- **7 еталонних патернів**: Memory Persistence, Skill Runtime, Context Engineering, Tool Registry, Multi-Agent Coordination, Lifecycle & Bootstrap, Gotchas
- **Шаблони**: AGENTS.md/CLAUDE.md, feature-list.json, init.sh, progress.md, session-handoff.md
- **Скрипти**: скафолдинг, валідація, рендеринг HTML-оцінювання, запуск структурного бенчмарку
- **10 вбудованих тестових кейсів для оцінювання (eval)**

Повну документацію див. у [harness-creator/README.md](harness-creator/README.md).

## Як було створено harness-creator

Навичку `harness-creator` було розроблено за методологією **skill-creator** — офіційної мета-навички Anthropic для створення, тестування та ітеративного вдосконалення навичок агентів. skill-creator надає структурований процес (чернетка → тестування → оцінювання → ітерація) із вбудованими запускачами eval, оцінювачами та переглядачем бенчмарків.

- **Джерело skill-creator**: [anthropics/skills — skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
- **Документація Anthropic щодо навичок Claude Code**: [anthropics/claude-code — plugin-dev/skills](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills)

## Структура каталогу

```
skills/
├── README.md                    # Цей файл
├── README-CN.md                 # Китайська версія
├── README-ZH-TW.md              # Традиційна китайська версія
├── README-JA.md                 # Японська версія
├── README-ES.md                 # Іспанська версія
├── README-FR.md                 # Французька версія
├── README-AR.md                 # Арабська версія
├── README-VI.md                 # В'єтнамська версія
├── README-DE.md                 # Німецька версія
├── README-TR.md                 # Турецька версія
├── README-PT-BR.md              # Версія португальською (Бразилія)
├── README-UK.md                 # Українська версія
└── harness-creator/             # Навичка для інженерії harness
    ├── SKILL.md                 # Основне визначення навички
    ├── SKILL.md.en              # Версія лише англійською
    ├── README.md                # Детальна документація
    ├── metadata.json            # Метадані та тригери навички
    ├── agents/                  # Метадані UI навички
    ├── scripts/                 # Помічники: скафолдинг, валідація, бенчмарк
    ├── evals/                   # Тестові кейси
    ├── templates/               # Шаблони для скафолдингу
    └── references/              # Докладні документи з патернів
```

## Як працюють навички

Кожна навичка має стандартну структуру:

1. **SKILL.md** — точка входу. Містить YAML-фронтматер (name, description для тригерингу) та інструкції для агента у форматі Markdown.
2. **references/** — додаткові документи, що завантажуються в контекст за потреби.
3. **templates/** — початкові шаблони, які навичка може генерувати для користувачів.

Навички використовують прогресивне розкриття (progressive disclosure): агент спочатку бачить лише name + description, потім, коли спрацьовує тригер, завантажує повний вміст SKILL.md і лише за потреби читає супутні ресурси.

## Аудит безпеки

Усі файли в цьому каталозі пройшли аудит безпеки:

- Без бекдорів, прихованих URL чи закодованих корисних навантажень
- Без витоку даних чи жорстко закодованих облікових даних
- Без вразливостей до ін'єкції команд
- Скрипти використовують лише вбудовані модулі Node.js
- Згенерований `init.sh` запускає виявлені команди верифікації проєкту

## Ліцензія

MIT
