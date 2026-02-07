// datatables-ua.js - Ukrainian DataTables language resource file
// Based on official DataTables i18n: https://cdn.datatables.net/plug-ins/2.3.7/i18n/uk.json

const datatablesTranslations = {
    "emptyTable": "Ця таблиця не містить даних",
    "info": "Показано від _START_ по _END_ з _TOTAL_ записів",
    "infoEmpty": "Показано від 0 по 0 з 0 записів",
    "infoFiltered": "(відфільтровано з _MAX_ записів)",
    "infoPostFix": "",
    "infoThousands": ",",
    "lengthMenu": "Показати _MENU_ записів",
    "loadingRecords": "Завантаження...",
    "processing": "Опрацювання...",
    "search": "Пошук:",
    "zeroRecords": "Не знайдено жодних записів",
    "thousands": ",",
    "paginate": {
        "first": "Перша",
        "last": "Остання",
        "next": "Наступна",
        "previous": "Попередня"
    },
    "aria": {
        "orderable": ": активувати для сортування",
        "orderableReverse": ": активувати для зворотного сортування"
    },
    "select": {
        "rows": {
            "_": "Вибрано %d рядків",
            "0": "",
            "1": "Вибрано 1 рядок"
        },
        "columns": {
            "_": "%d колонок вибрано",
            "0": "",
            "1": "1 колонку вибрано"
        },
        "cells": {
            "_": "%d клітинок вибрано",
            "0": "",
            "1": "1 клітинку вибрано"
        }
    },
    "buttons": {
        "copy": "Копіювати",
        "copyTitle": "Копіювати в буфер обміну",
        "copySuccess": {
            "_": "Скопійовано %d рядків в буфер обміну",
            "1": "Скопійовано 1 рядок в буфер обміну"
        },
        "print": "Друк",
        "colvis": "Видимість стовпців",
        "colvisRestore": "Відновити видимість",
        "pageLength": {
            "_": "Показати %d рядків",
            "-1": "Показати всі рядки"
        },
        "collection": "Колекція"
    },
    "searchBuilder": {
        "add": "Додати умову",
        "button": {
            "_": "Розширений пошук (%d)",
            "0": "Розширений пошук"
        },
        "clearAll": "Очистити все",
        "condition": "Умова",
        "conditions": {
            "array": {
                "contains": "Містить",
                "empty": "Пустий",
                "equals": "Дорівнює",
                "not": "Не",
                "notEmpty": "Не пусто",
                "without": "Без"
            },
            "date": {
                "after": "Після",
                "before": "До",
                "between": "Між",
                "empty": "Пусто",
                "equals": "Дорівнює",
                "not": "Не",
                "notBetween": "Не між",
                "notEmpty": "Не пусто"
            },
            "number": {
                "between": "Між",
                "empty": "Пусто",
                "equals": "Дорівнює",
                "gt": "Більше ніж",
                "gte": "Більше або дорівнює",
                "lt": "Менше ніж",
                "lte": "Менше або дорівнює",
                "not": "Не",
                "notBetween": "Не між",
                "notEmpty": "Не пусто"
            },
            "string": {
                "contains": "Містить",
                "empty": "Пусто",
                "endsWith": "Закінчується на",
                "equals": "Дорівнює",
                "not": "Не",
                "notContains": "Не містить",
                "notEmpty": "Не пусто",
                "notEndsWith": "Не закінчується на",
                "notStartsWith": "Не починається з",
                "startsWith": "Починається з"
            }
        },
        "data": "Дані",
        "deleteTitle": "Видалити правило фільтрування",
        "leftTitle": "Зняти відступ критерію",
        "logicAnd": "ТА",
        "logicOr": "АБО",
        "rightTitle": "Зробити відступ критерію",
        "title": {
            "_": "Розширений пошук (%d)",
            "0": "Розширений пошук"
        },
        "value": "Значення"
    },
    "searchPanes": {
        "clearMessage": "Очистити все",
        "collapse": {
            "_": "Панелі пошуку (%d)",
            "0": "Панель пошуку"
        },
        "collapseMessage": "Приховати всі",
        "count": "{total}",
        "countFiltered": "{shown} ({total})",
        "emptyMessage": "Немає даних",
        "emptyPanes": "Немає панелей пошуку",
        "loadMessage": "Завантаження панелей пошуку",
        "showMessage": "Показати всі",
        "title": "Активні фільтри - %d"
    },
    "stateRestore": {
        "creationModal": {
            "button": "Створити",
            "columns": {
                "search": "Пошук у стовпці",
                "visible": "Видимість стовпця"
            },
            "name": "Ім'я:",
            "order": "Сортування",
            "paging": "Пейджинг",
            "scroller": "Прокручування",
            "search": "Пошук",
            "searchBuilder": "Конструктор запитів",
            "select": "Вибір",
            "title": "Створити новий стан",
            "toggleLabel": "Включає:"
        },
        "duplicateError": "Стан з такою назвою вже існує.",
        "emptyError": "Назва не може бути порожньою.",
        "emptyStates": "Немає збереженого стану.",
        "removeConfirm": "Ви впевнені, що хочете видалити %s?",
        "removeError": "Не вдалося видалити стан.",
        "removeJoiner": "і",
        "removeSubmit": "Видалити",
        "removeTitle": "Видалити стан",
        "renameButton": "Перейменувати",
        "renameLabel": "Нова назва для %s:",
        "renameTitle": "Перейменувати стан"
    },
    "editor": {
        "close": "Закрити",
        "create": {
            "button": "Новий",
            "submit": "Створити",
            "title": "Створити новий запис"
        },
        "edit": {
            "button": "Редагувати",
            "submit": "Оновити",
            "title": "Редагування запису"
        },
        "error": {
            "system": "Виникла помилка системи (<a target=\"\\\" rel=\"nofollow\" href=\"\\\">Додаткова інформація</a>)."
        },
        "multi": {
            "info": "Вибране поле містить кілька елементів з різними значеннями. Щоб змінити їх значення, клацніть на них; інакше будуть збережені їхні значення за замовчуванням.",
            "noMulti": "Це значення можна редагувати окремо – незалежно від групи.",
            "restore": "Скасувати зміни",
            "title": "Поле з кількома значеннями"
        },
        "remove": {
            "button": "Видалити",
            "confirm": {
                "_": "Ви впевнені, що хочете видалити %d рядків?",
                "1": "Ви впевнені, що хочете видалити 1 рядок?"
            },
            "submit": "Видалити",
            "title": "Видалити"
        }
    }
};

export default datatablesTranslations;
