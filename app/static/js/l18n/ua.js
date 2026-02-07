// ua.js - Ukrainian language resource file

const translations = {
    tableHeaders: {
        studioDetails:
        {
            id: 'ID',
            name: 'Назва',
            telegram: 'Телеграм',
        },
        anime:
        {
            id: 'ID',
            titleUa: 'UA',
            titleEn: 'EN',
            season: 'Сезон',
            type: 'Тип',
            status: 'Статус',
            releaseDate: 'Дата випуску',
        },
        releases:
        {
            codename: "Кодове ім'я",
            torrent_name: 'Назва торренту',
            season_number: 'Номер сезону',
            episode_index: 'Індекс епізоду',
            adjusted_episode_number: 'Скоригований номер епізоду',
            publish_date: 'Дата публікації',
            release_group: 'Група випуску',
            download_dir: 'Директорія завантаження',
            guid: 'Toloka ID',
            hash: 'Хеш',
            meta: 'Мета',
            ongoing: 'Онгоїнг',
            actions: 'Дії'
        },
        toloka:
        {
            forum: 'Форум',
            name: 'Назва',
            author: 'Автор',
            date: 'Дата',
            answers: 'Відповіді',
            forum_url: 'URL форуму',
            leechers: 'Лічери',
            seeders: 'Сідери',
            size: 'Розмір',
            status: 'Статус',
            torrent_url: 'URL торренту',
            url: 'URL',
            verify: 'Перевірка',
            actions: 'Дії'
        },
        multi:
        {
            source: 'Джерело',
            image: 'Зображення',
            title: 'Назва',
            alternative: 'Альтернатива',
            id: 'ID',
            status: 'Статус',
            mediaType: 'Тип медіа',
            description: 'Опис',
            releaseDate: 'Дата випуску'
        },
        stream:
        {
            provider: 'Провайдер',
            image: 'Зображення',
            title: 'Назва',
            title_eng: 'Назва ENG',
            link: 'Посилання',
        },
        settings:
        {
            id: 'ID',
            section: 'Секція',
            key: 'Ключ',
            value: 'Значення',
        },
        users:
        {
            id: 'ID',
            username: "Ім'я користувача",
            roles: 'Ролі',
            actions: 'Дії'
        },
    },
    buttons: {
        dataTableRefreshButton: 'Оновити',
        dataTableColumnVisibilityhButton: 'Видимість стовпців',
        releaseAddSubmit: 'Підтвердити',
        releaseAddButton: 'Додати',
        releaseUpdateAllButton: 'Оновити все',
        releaseEditButton: 'Редагувати',
        releaseDeleteButton: 'Видалити',
        releaseUpdateButton: 'Оновити',
        releaseForceUpdateButton: 'Оновити примусово',
        expandButton: 'Розгорнути',
        tolokaDownloadButton: "Пряме завантаження",
        tolokaAddButton: "Додати до клієнта",
        tolokaCopyButton: "Копіювати значення",
        settingSaveButton: "Зберегти",
        settingsAdd: "Додати",
        settingsSyncTo: "Синхронізувати до app.ini",
        settingsSyncFrom: "Синхронізувати з app.ini",
        settingsUpdateButton: "Оновити",
        closeButton: "Закрити",
        signInButton: "Увійти",
        registerButton: "Зареєструватися",
        parseButton: "Розібрати бінарний",
        cancelButton: "Скасувати",
        saveChanges: "Зберегти зміни",
        editButton: "Редагувати",
        deleteButton: "Видалити"
    },
    labels: {
        dataTableSearchInput: "Фільтрувати записи",
        dataTablesYearText: "роки",
        dataTablesDaysText: "дні",
        dataTablesHrsText: "год тому",
        dataTablesLoadingText: "Завантаження...",
        newVersionToastTitle: "Новий реліз: ",
        operationStatusGithub: "Створіть issue на github, якщо щось не так.",
        buttonsLoadingText: "Завантаження...",
        releaseAddIndex: 'Індекс',
        releaseAddNumber: 'Номер',
        noImageAvailable: 'Зображення недоступне',
        checkVersions: 'Встановлені пакети',
        settingsNotification: 'Сторінка показує останні збережені налаштування в БД. Будь ласка, використовуйте Синхронізацію для оновлення.',
        toggleTheme: 'Перемкнути тему',
        toggleLanguage: 'Перемкнути мову',
        createAccount: 'Створити обліковий запис',
        pleaseSignIn: 'Будь ласка, увійдіть',
        systemActions: 'Системні дії',
        showVersions: 'Показати версії',
        syncTitlesFromDb: 'Синхронізувати titles.ini з БД',
        syncTitlesToDb: 'Синхронізувати titles.ini до БД',
        profileSettings: 'Налаштування профілю',
        userManagement: 'Керування користувачами',
        editRelease: 'Редагувати реліз',
        addRelease: 'Додати реліз',
        addedTitles: 'Додані тайтли',
        indexExtractor: 'Екстрактор індексу',
        provideValidFilename: 'Будь ласка, вкажіть правильну назву файлу.',
        newSuggestions: 'Нові пропозиції',
        newStreams: 'Нові стріми',
        seed: 'сід',
        notFound: 'Не знайдено',
        system: 'Система',
        profile: 'Профіль',
        configuration: 'Конфігурація',
        users: 'Користувачі',
        light: 'Світла',
        dark: 'Темна',
        auto: 'Авто',
        ongoing: 'Онгоїнг',
        ongoingDescription: 'Використовувати діапазон епізодів (S01E01-E02) замість паку сезону (S01)',
        releaseGroup: 'Група',
        meta: 'Мета',
        releaseGroupMeta: 'Теги',
        releasePreview: 'Попередній перегляд',
        tolokaSearchErrorTitle: 'Пошук Toloka',
        showMoreFiles: 'Показати більше файлів',
        showLessFiles: 'Показати менше файлів',
        noEpisodesFound: 'Епізоди не знайдено',
        studio: 'Студія',
        episodes: 'епізодів',
        unknownSeries: 'Невідома серія',
        noEpisodesAvailable: 'Епізоди недоступні',
        episode: 'Епізод',
        // Navigation
        home: 'Головна',
        studios: 'Студії',
        anime: 'Аніме',
        settings: 'Налаштування',
        logout: 'Вийти',
        search: 'Пошук',
        // Search results
        searchResults: 'Результати пошуку',
        toloka: 'Toloka',
        searchSuggestions: 'Пропозиції пошуку',
        stream: 'Стрім',
        operationResults: 'Результати операції',
        // Page titles
        voiceoverStudios: 'Студії озвучення',
        titles: 'Назви',
        animeTitles: 'Назви аніме',
        relatedAnimes: 'Пов\'язані аніме',
        animeTitle: 'Назва аніме',
        description: 'Опис',
        studioName: 'Назва студії',
        // Form labels
        tolokaUrl: 'URL Toloka',
        title: 'Назва',
        season: 'Сезон',
        episodeIndex: 'Індекс епізоду',
        indexCorrection: 'Корекція індексу',
        username: "Ім'я користувача",
        password: 'Пароль',
        roles: 'Ролі',
        role: 'Роль',
        newPassword: 'Новий пароль',
        confirmPassword: 'Підтвердити пароль',
        changePassword: 'Змінити пароль',
        rememberMe: "Запам'ятати мене",
        // User roles
        user: 'Користувач',
        admin: 'Адміністратор',
        // Modal titles
        editUser: 'Редагувати користувача',
        deleteUser: 'Видалити користувача',
        // Confirmation messages
        deleteUserConfirm: 'Ви впевнені, що хочете видалити цього користувача? Цю дію неможливо скасувати.',
        // Toast messages
        profileUpdated: 'Профіль успішно оновлено',
        userUpdated: 'Користувача успішно оновлено',
        userDeleted: 'Користувача успішно видалено',
        failedLoadProfile: 'Не вдалося завантажити дані профілю',
        failedLoadUsers: 'Не вдалося завантажити користувачів',
        failedUpdateProfile: 'Не вдалося оновити профіль',
        failedUpdateUser: 'Не вдалося оновити користувача',
        failedDeleteUser: 'Не вдалося видалити користувача',
        // Info messages
        publicApiBackup: 'Надана інформація є резервною копією публічного API з сайту AnimeOn.',
        settingsDevNotice: 'Сторінка в розробці і в поточному стані може лише відображати дані, вже збережені в базі даних. Ви можете змінити open_registration. Інші властивості не матимуть ефекту, оскільки немає синхронізації з app.ini',
        passwordRequirement: 'Пароль повинен містити щонайменше 8 символів.',
        passwordKeepBlank: 'Залиште порожнім, щоб зберегти поточний пароль. Новий пароль повинен містити щонайменше 8 символів.',
        // Form validation
        provideValidUrl: 'Будь ласка, вкажіть дійсну URL-адресу.',
        provideTitle: 'Будь ласка, вкажіть назву.',
        provideValidSeason: 'Будь ласка, вкажіть дійсний номер сезону (мін: 0).',
        provideValidEpisodeIndex: 'Будь ласка, вкажіть дійсний індекс епізоду (мін: 1).',
        // Button labels with icons
        cutTitle: 'Обрізати назву'
    },
    validation: {
        invalidTitle: 'Назва містить недопустимі символи, які можуть порушити шляхи або JSON (/, \\, :, *, ?, ", <, >, |)',
        invalidNumber: 'Будь ласка, введіть дійсне число',
        invalidUrl: 'Будь ласка, введіть дійсну URL-адресу Toloka (має починатися з https://toloka.to/)'
    },
    pages: {
        titles: {
            base: 'Toloka2Web'
        }
    }
};

export default translations;
