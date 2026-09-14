[中文版本 →](../../../zh/projects/project-01-baseline-vs-minimal-harness/)

> Пов'язані лекції: [Лекція 01. Потужні моделі не гарантують надійне виконання](./../../lectures/lecture-01-why-capable-agents-still-fail/index.md) · [Лекція 02. Що насправді означає harness](./../../lectures/lecture-02-what-a-harness-actually-is/index.md)
> Файли шаблонів: [templates/](https://github.com/walkinglabs/learn-harness-engineering/blob/main/docs/uk/resources/templates/)

# Проєкт 01. Тільки промпт vs. правила спочатку: наскільки велика різниця

## Що ви робите

Побудуйте мінімальну оболонку Electron-застосунку для бази знань — вікно зі списком документів ліворуч, панель запитань і відповідей праворуч та локальна директорія даних. Саме завдання не є складним. Складність — у тому, як змусити агента виконати його.

Ви запускаєте завдання двічі. Перший раз: лише промпт, без підготовки. Другий раз: `AGENTS.md`, `init.sh`, `feature_list.json` заздалегідь розміщені в репозиторії. Потім порівнюєте результати.

Цей сценарій курсу використовує короткий інтервал повторного ознайомлення/підготовки як приклад, а не як фіксований вимірюваний результат.

## Інструменти

- Claude Code або Codex (оберіть один, використовуйте для обох запусків)
- Git (керування гілками та порівняння)
- Node.js + Electron (стек проєкту)
- Таймер (фіксуйте тривалість кожного запуску)

## Механізм harness

Мінімальний harness: `AGENTS.md` + `init.sh` + `feature_list.json`

## Використовуйте зафіксований у репозиторії проєкт

Шлях у репозиторії: [`projects/project-01/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-01)

| Директорія | Що містить | Як використовувати |
|------|------|------|
| [`starter/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-01/starter) | Запуск зі слабким harness. Містить лише [`task-prompt.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-01/starter/task-prompt.md) як опис завдання та не містить `AGENTS.md` або `feature_list.json`. | Передайте промпт вашому AI-агенту для написання коду та виміряйте, що він виконає без додаткової структури. |
| [`solution/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-01/solution) | Той самий продуктовий зріз з явними артефактами harness: [`AGENTS.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-01/solution/AGENTS.md), [`CLAUDE.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-01/solution/CLAUDE.md), [`init.sh`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-01/solution/init.sh), [`feature_list.json`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-01/solution/feature_list.json) та [`claude-progress.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-01/solution/claude-progress.md). | Порівняйте, як те саме завдання конкретизується через правила та докази верифікації. |

Чотири конкретні функції: запуск вікна, список документів, панель запитань та створення локальної директорії даних. Перегляньте `solution/feature_list.json`, щоб дізнатися про очікувані докази для кожної функції.
