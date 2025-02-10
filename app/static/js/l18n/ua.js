// en.js - English language resource file

const translations = {
    tableHeaders: {
        studioDetails:
        {
            id:'ID',
            name:'Назва',
            telegram:'телеграм',
        },
        anime:
        {
            id:'ID',
            titleUa:'UA',
            titleEn:'EN',
            season:'Сезон',
            type:'Тип',
            status:'Статус',
            releaseDate:'дата випуску',
        },        
        releases:
        {
            codename:"Кодове ім'я",
            torrent_name:'Назва торренту', 
            season_number: 'Номер сезону',
            episode_index:'Індекс епізоду',
            adjusted_episode_number:'Скоригований номер епізоду', 
            publish_date: 'Дата публікації',
            release_group: 'Група випуску', 
            download_dir: 'Директорія завантаження',
            hash: 'Хеш', 
            meta: 'Мета', 
            actions: 'Дії'
        },
        toloka:
        {
            forum: 'Форум',
            name: 'Назва',
            author: 'Автор', 
            date: 'дата',  
            answers: 'відповіді',
            forum_url: 'URL форуму',
            leechers: 'Лічери',
            seeders: 'Сідери',
            size: 'розмір',
            status: 'статус',
            torrent_url: 'URL торренту',
            url: 'URL', 
            verify: 'перевірити',
            actions:'Дії'            
        },
        multi:
        {
            source:'Джерело',
            image:'Зображення', 
            title:'Назва',
            alternative:'альтернатива',
            id:'ID',  
            status:'Статус', 
            mediaType:'Тип медіа' ,
            description:'опис',
            releaseDate: 'Дата випуску' 
        },
        stream:
        {
            provider: 'Провайдер', 
            title: 'Зображення',
            title:'Назва',
            title_eng:'Назва ENG',
            link:'Посилання',
        },
        settings:
        {
            id: 'ID', 
            section: 'Секція',
            key:'Ключ',
            value:'Значення',
        },
    },
    buttons: {
        dataTableRefreshButton: 'Оновити',
        dataTableColumnVisibilityhButton: 'Видимість стовпців',
        releaseAddSubmit: 'Подати',
        releaseAddButton:'Додати',
        releaseUpdateAllButton:'Оновити все',
        releaseEditButton:'Редагувати',
        releaseDeleteButton:'Видалити',
        releaseUpdateButton:'Оновити',
        expandButton:'Розгорнути',
        tolokaDownloadButton:"Пряме завантаження",
        tolokaAddButton:"Додати до клієнта",
        tolokaCopyButton:"Копіювати значення",
        settingSaveButton: "Зберегти",
        settingsAdd:"Додати",
        settingsSyncTo:"Синхронізація з app.ini",
        settingsSyncFrom:"Синхронізація з app.ini",
        settingsUpdateButton:"Оновити",
        closeButton: "Закрити",
        signInButton: "Увійти",
        registerButton: "Зареєструватися",
        parseButton: "Розібрати бінарний",
        cancelButton: "Скасувати"
    },
    labels: {
        dataTableSearchInput: "Фільтрувати записи",
        dataTablesYearText:"роки",
        dataTablesDaysText:"дні",
        dataTablesHrsText:"год тому",
        dataTablesLoadingText:"Завантаження...",
        newVersionToastTitle:"Новий реліз: ",
        operationStatusGithub: "Створіть issue на github, якщо щось не так.",
        buttonsLoadingText:"Завантаження...",
        releaseAddIndex: 'Індекс',
        releaseAddNumber:'Номер',
        noImageAvailable:'Зображення недоступне',
        checkVersions: 'Встановлені пакети',
        settingsNotification: 'Сторінка показує останні збережені налаштування в БД. Будь ласка, використовуйте Синхронізацію для оновлення.',
        toggleTheme: 'Перемкнути тему',
        toggleLanguage: 'Перемкнути мову',
        createAccount: 'Створити обліковий запис',
        pleaseSignIn: 'Будь ласка, увійдіть',
        systemActions: 'Системні дії',
        showVersions: 'Показати версії',
        syncTitlesFromDb: 'Синхронізувати titles.ini з БД',
        syncTitlesToDb: 'Синхронізувати titles.ini в БД',
        profileSettings: 'Налаштування профілю скоро будуть доступні...',
        userManagement: 'Керування користувачами скоро буде доступне...',
        editRelease: 'Редагувати реліз',
        addRelease: 'Додати реліз',
        addedTitles: 'Додані назви',
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
        dark: 'Темна'
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