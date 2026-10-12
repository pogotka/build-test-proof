# Evidence beside the claim

Use the user's language and omit empty sections. A concise Russian example, with actual values substituted from the run:

Изменена карточка товара; проверен локальный Chromium, 1280×800.

- **Карточка — проверено.** Открыта `/catalog`; новый заголовок и кнопка видны без обрезания.

  ![Карточка после изменения](/absolute/evidence/catalog-final.png)

- **Добавление — проверено после исправления.** Нажатие «Добавить» увеличило счётчик с 0 до 1; тот же ввод повторён после перезагрузки. Скриншот показывает конечное состояние; действие проверено отдельно.

  ![Счётчик после добавления](/absolute/evidence/add-fixed.png)

- **Оформление — проверено.** `/catalog` → добавление → `/details` → ввод безопасных тестовых данных → `/done`. [Видео фактического сценария](/absolute/evidence/flow.webm).
- **Сохранение — не исправлено.** Нажатие оставило ошибку «Сервис недоступен». Приложены воспроизведение и снимок. Остальные успешные проверки не закрывают эту проблему.

Предложения: добавить явное состояние повтора запроса. Не выполнено в этой задаче.
Не проверены: реальная оплата, Safari, физическое мобильное устройство.

Do not copy invented sample outcomes. Report observed facts and use absolute paths in local chat links. For a portable Markdown handoff, relative paths within the evidence bundle are appropriate; explicitly distinguish them from chat artifact paths.

## Optional Markdown

Default to chat only for a single-screen change. Add a Markdown report if asked or when a multi-artifact handoff needs durable reproduction details. Keep it with evidence outside source. Include a short scope/environment block, per-change assertions with adjacent images, long-flow video links, failure/rerun details, and unchecked behavior. Open/inspect image and video references, and verify every file exists. Local paths will not become public links automatically; when relocating a bundle use relative Markdown links and keep the directory structure intact.

The first prototype evaluation found Markdown useful for the combined failure/fix/video handoff, but redundant for one visual adjustment. Therefore it is conditional, not automatically generated after every task.
