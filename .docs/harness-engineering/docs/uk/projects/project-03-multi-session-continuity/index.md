[中文版本 →](../../../zh/projects/project-03-multi-session-continuity/)

> Пов'язані лекції: [Лекція 05. Зберігайте контекст між сесіями](./../../lectures/lecture-05-why-long-running-tasks-lose-continuity/index.md) · [Лекція 06. Ініціалізуйте перед кожною сесією агента](./../../lectures/lecture-06-why-initialization-needs-its-own-phase/index.md)
> Файли шаблонів: [templates/](https://github.com/walkinglabs/learn-harness-engineering/blob/main/docs/uk/resources/templates/)

# Проєкт 03. Підтримуйте роботу агента під час перезапуску сесій

## Що ви робите

Додайте контроль обсягу та перевірочні шлюзи до агента. Реалізуйте розбиття документів на частини, вилучення метаданих, відображення прогресу індексування та потік запитань і відповідей на основі цитат. Використовуйте `feature_list.json` для відстеження статусу функцій — по одній функції за раз, без позначення як «пройдено» без доказів верифікації.

Ви порівнюєте зафіксовані в репозиторії стартову версію та рішення: стартова версія має лише початкову поверхню відстеження, тоді як рішення додає більш суворі артефакти перезапуску та передачі роботи навколо того самого списку функцій.

## Інструменти

- Claude Code або Codex
- Git
- Node.js + Electron

## Механізм harness

Журнал прогресу + передача сесії + безперервність між сесіями + верифікація по одній функції за раз

## Використовуйте зафіксований у репозиторії проєкт

Шлях у репозиторії: [`projects/project-03/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-03)

| Директорія | Що містить | Що порівнювати |
|------|------|------|
| [`starter/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-03/starter) | Код проєкту 02 з незавершеними індексуванням і grounded QA. Містить початковий [`feature_list.json`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-03/starter/feature_list.json), але бракує фінальних артефактів перезапуску/передачі. | Чи відхиляється агент між кількома функціями або чи втрачає стан після перезапуску. |
| [`solution/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-03/solution) | Завершене розбиття на частини, метадані, статус індексу та QA на основі цитат, плюс [`init.sh`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-03/solution/init.sh), [`session-handoff.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-03/solution/session-handoff.md), [`claude-progress.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-03/solution/claude-progress.md) та [`clean-state-checklist.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-03/solution/clean-state-checklist.md). | Чи є конкретні докази верифікації для кожної функції до того, як вона позначається як пройдена. |

Цей проєкт — не загальна вправа з «кількох сесій». Зафіксоване в репозиторії рішення відповідає чотирьом конкретним продуктовим функціям: розбиття документів на частини, вилучення метаданих, інтерфейс статусу індексування та grounded Q&A з цитатами.
