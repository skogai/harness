[中文版本 →](../../../zh/projects/project-06-runtime-observability-and-debugging/)

> Пов'язані лекції: [Лекція 11. Зробіть runtime агента спостережуваним](./../../lectures/lecture-11-why-observability-belongs-inside-the-harness/index.md) · [Лекція 12. Чистий перехід наприкінці кожної сесії](./../../lectures/lecture-12-why-every-session-must-leave-a-clean-state/index.md)
> Файли шаблонів: [templates/](https://github.com/walkinglabs/learn-harness-engineering/blob/main/docs/uk/resources/templates/)

# Проєкт 06. Побудуйте повний harness агента (підсумковий проєкт)

## Що ви робите

Це підсумковий проєкт. Зберіть усе, чого ви навчилися в перших п'яти проєктах, запустіть повний бенчмарк, а потім виконайте прохід очищення, щоб переконатися, що якість підтримувана.

Використовуйте фіксований набір багатофункціональних завдань, що охоплює повний продуктовий зріз: імпорт документів, індексування, Q&A на основі цитат, спостережуваність у runtime та зрозумілий перезапускуваний стан репозиторію. Спочатку запустіть зі слабким базовим harness, потім із вашим найсильнішим harness, далі — очищення та повторний запуск. Нарешті, проведіть абляційний експеримент harness — видаляйте по одному компоненту і спостерігайте, які з них насправді мають значення.

## Інструменти

- Claude Code або Codex
- Git
- Node.js + Electron
- Шаблон якісного документа
- Рубрика оцінювача
- Усі компоненти harness, накопичені з перших п'яти проєктів

## Механізм harness

Повний harness: усі механізми + спостережуваність + абляційне дослідження

## Використовуйте зафіксований у репозиторії проєкт

Шлях у репозиторії: [`projects/project-06/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-06)

| Директорія | Що містить | Що порівнювати |
|------|------|------|
| [`starter/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-06/starter) | Здебільшого завершений продуктовий код із навмисно слабкою поверхнею harness: базовий [`AGENTS.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-06/starter/AGENTS.md), без `feature_list.json`, без `session-handoff.md`, без чеклисту чистого стану. | Ручні спостереження базового рівня зі слабким harness. Стартова версія навмисно не містить скриптів бенчмарку. |
| [`solution/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-06/solution) | Повна поверхня harness: [`AGENTS.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-06/solution/AGENTS.md), [`CLAUDE.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-06/solution/CLAUDE.md), [`feature_list.json`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-06/solution/feature_list.json), [`init.sh`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-06/solution/init.sh), [`session-handoff.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-06/solution/session-handoff.md), [`clean-state-checklist.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-06/solution/clean-state-checklist.md), документи якості/оцінювача, скрипти бенчмарку та очищення. | Запустіть [`projects/project-06/solution/scripts/benchmark.sh`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-06/solution/scripts/benchmark.sh) та [`projects/project-06/solution/scripts/cleanup-scanner.sh`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-06/solution/scripts/cleanup-scanner.sh), потім порівняйте докази з якісних документів. |

На відміну від попередніх проєктів, стартова версія підсумкового проєкту не є здебільшого неповною з точки зору продуктових функцій. Основний пробіл — у робочому harness навколо застосунку.
