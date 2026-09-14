[中文版本 →](../../../zh/projects/project-04-incremental-indexing/)

> Пов'язані лекції: [Лекція 07. Встановлюйте чіткі межі завдань для агентів](./../../lectures/lecture-07-why-agents-overreach-and-under-finish/index.md) · [Лекція 08. Використовуйте списки функцій для обмеження дій агента](./../../lectures/lecture-08-why-feature-lists-are-harness-primitives/index.md)
> Файли шаблонів: [templates/](https://github.com/walkinglabs/learn-harness-engineering/blob/main/docs/uk/resources/templates/)

# Проєкт 04. Використовуйте зворотний зв'язок у runtime для корекції поведінки агента

## Що ви робите

Додайте спостережуваність у runtime (журнали запуску, журнали імпорту/індексування, стани помилок) та архітектурні обмеження для запобігання порушенням між шарами. Посадіть помилку у runtime, яку агент має виправити.

Ви порівнюєте зафіксовані в репозиторії стартову версію та рішення: стартова версія має слабку діагностику і жодного скрипта перевірки архітектури, тоді як рішення додає структуровані журнали, перевірки меж і виправлення помилки.

## Інструменти

- Claude Code або Codex
- Git
- Node.js + Electron

## Механізм harness

Зворотний зв'язок у runtime + контроль обсягу + інкрементальне індексування

## Використовуйте зафіксований у репозиторії проєкт

Шлях у репозиторії: [`projects/project-04/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-04)

| Директорія | Що містить | Що порівнювати |
|------|------|------|
| [`starter/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-04/starter) | Код проєкту 03 зі слабкою діагностикою. Навмисно посаджений дефект індексування може спричинити збій розбиття великих файлів на частини, і відсутній скрипт перевірки архітектури. | Скільки часу агент витрачає на пошук першопричини без сигналів runtime. |
| [`solution/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-04/solution) | Структурований логер, документи та скрипт меж архітектури, виправлена логіка розбиття та [`clean-state-checklist.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-04/solution/clean-state-checklist.md). | Чи роблять журнали та перевірки меж виправлення швидшим і менш інвазивним. |

Конкретні файли для перевірки: [`projects/project-04/solution/src/services/logger.ts`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-04/solution/src/services/logger.ts),
[`projects/project-04/solution/scripts/check-architecture.sh`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-04/solution/scripts/check-architecture.sh),
[`projects/project-04/solution/docs/ARCHITECTURE.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-04/solution/docs/ARCHITECTURE.md) та
[`projects/project-04/solution/src/services/indexing-service.ts`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-04/solution/src/services/indexing-service.ts).
