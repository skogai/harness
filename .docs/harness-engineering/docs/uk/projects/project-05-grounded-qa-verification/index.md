[中文版本 →](../../../zh/projects/project-05-grounded-qa-verification/)

> Пов'язані лекції: [Лекція 09. Зупиніть агентів від передчасного оголошення перемоги](./../../lectures/lecture-09-why-agents-declare-victory-too-early/index.md) · [Лекція 10. Лише повний прогін конвеєра вважається справжньою верифікацією](./../../lectures/lecture-10-why-end-to-end-testing-changes-results/index.md)
> Файли шаблонів: [templates/](https://github.com/walkinglabs/learn-harness-engineering/blob/main/docs/uk/resources/templates/)

# Проєкт 05. Змусьте агента верифікувати власну роботу

## Що ви робите

Реалізуйте розподіл ролей — генератор, який реалізує, оцінювач, який перевіряє, та опційно планувальник. Запустіть тричі, щоб виміряти ефект кожної доданої ролі.

Оберіть суттєве покращення функціональності (багатоходова розмова, редизайн панелі цитат або фільтрація документів) і підтримуйте його незмінним у всіх запусках.

## Інструменти

- Claude Code або Codex
- Git
- Node.js + Electron

## Механізм harness

Самоверифікація + grounded Q&A + завершення на основі доказів

## Використовуйте зафіксований у репозиторії проєкт

Шлях у репозиторії: [`projects/project-05/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-05)

| Директорія | Що містить | Що порівнювати |
|------|------|------|
| [`starter/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-05/starter) | Застосунок на основі проєкту 04 до оновлення функції збереження історії розмови. | Відправна точка, якщо ви хочете самостійно перезапустити три варіанти. |
| [`solution/single-role/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-05/solution/single-role) | Один агент планує, реалізує та самостійно перевіряє. | Оцінка [`evaluator-rubric.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-05/solution/single-role/evaluator-rubric.md): 1,6/5 і перелік дефектів. |
| [`solution/gen-eval/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-05/solution/gen-eval) | Генератор плюс оцінювач із доказами ревізії. | Оцінка [`evaluator-rubric.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-05/solution/gen-eval/evaluator-rubric.md): 3,3/5 і нотатки щодо ревізій. |
| [`solution/plan-gen-eval/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-05/solution/plan-gen-eval) | Планувальник плюс генератор плюс оцінювач. | [`sprint-contract.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-05/solution/plan-gen-eval/sprint-contract.md), оцінка [`evaluator-rubric.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-05/solution/plan-gen-eval/evaluator-rubric.md): 4,9/5. |

Зафіксована в репозиторії функція — збереження історії багатоходової розмови Q&A. Підтримуйте цю функцію незмінною у всіх трьох варіантах, щоб єдиною змінною був розподіл ролей.
