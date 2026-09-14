[中文版本 →](../../../zh/projects/project-02-agent-readable-workspace/)

> Пов'язані лекції: [Лекція 03. Зробіть репозиторій єдиним джерелом правди](./../../lectures/lecture-03-why-the-repository-must-become-the-system-of-record/index.md) · [Лекція 04. Розподіляйте інструкції між файлами](./../../lectures/lecture-04-why-one-giant-instruction-file-fails/index.md)
> Файли шаблонів: [templates/](https://github.com/walkinglabs/learn-harness-engineering/blob/main/docs/uk/resources/templates/)

# Проєкт 02. Зробіть проєкт зрозумілим і відновлюйте роботу з місця зупинки

## Що ви робите

Додайте «зрозумілість» до репозиторію, щоб новий агент міг швидко зрозуміти структуру проєкту, дізнатися поточний прогрес і продовжити роботу. Конкретно: реалізуйте імпорт документів, деталізований перегляд документа та локальну персистентність — протягом двох сесій.

Ви запускаєте завдання двічі з зафіксованих у репозиторії директорій: спочатку з тоншим стартовим простором роботи без `session-handoff.md`, потім з варіантом рішення, який має розширені `ARCHITECTURE.md`, `PRODUCT.md` та `session-handoff.md`.

## Інструменти

- Claude Code або Codex
- Git
- Node.js + Electron

## Механізм harness

Простір роботи, зрозумілий агенту, + файли постійного стану

## Використовуйте зафіксований у репозиторії проєкт

Шлях у репозиторії: [`projects/project-02/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-02)

| Директорія | Що містить | Що порівнювати |
|------|------|------|
| [`starter/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-02/starter) | Код проєкту 01 плюс незавершені імпорт документів, деталізований перегляд і персистентність. Документи існують, але навмисно є тоншими, і відсутній `session-handoff.md`. | Скільки повторного ознайомлення виконує друга сесія агента. |
| [`solution/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-02/solution) | Той самий зріз у завершеному вигляді, з розширеними документами в [`projects/project-02/solution/`](https://github.com/walkinglabs/learn-harness-engineering/tree/main/projects/project-02/solution) (плюс [`feature_list.json`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-02/solution/feature_list.json) та [`session-handoff.md`](https://github.com/walkinglabs/learn-harness-engineering/blob/main/projects/project-02/solution/session-handoff.md)). | Чи може нова сесія відновити роботу зі стану репозиторію без усного контексту. |

Продуктові функції: імпорт документів, повне завантаження деталей/вмісту документа та персистентність між перезапусками. Функція harness — простір роботи, зрозумілий для передачі між сесіями.
