// en.js - English language resource file

const translations = {
    tableHeaders: {
        studioDetails:
        {
            id:'ID',
            name:'Name',
            telegram:'telegram',
        },
        anime:
        {
            id:'ID',
            titleUa:'UA',
            titleEn:'EN',
            season:'Season',
            type:'Type',
            status:'Status',
            releaseDate:'releaseDate',
        },        
        releases:
        {
            codename:'Codename',
            torrent_name:'Torrent Name', 
            season_number: 'Season Number',
            episode_index:'Episode Index',
            adjusted_episode_number:'Adjusted Episode Number', 
            publish_date: 'Publish Date',
            release_group: 'Release Group', 
            download_dir: 'Download Dir',
            guid: 'Toloka ID', 
            hash: 'Hash', 
            meta: 'Meta', 
            ongoing: 'Ongoing',
            actions: 'Actions'
        },
        toloka:
        {
            forum: 'Forum',
            name: 'Title',
            author: 'Author', 
            date: 'date',  
            answers: 'answers',
            forum_url: 'forum_url',
            leechers: 'Leechers',
            seeders: 'Seeders',
            size: 'size',
            status: 'status',
            torrent_url: 'torrent_url',
            url: 'url', 
            verify: 'verify',
            actions:'Actions'            
        },
        multi:
        {
            source:'Source',
            image:'Image', 
            title:'Title',
            alternative:'alternative',
            id:'ID',  
            status:'Status', 
            mediaType:'Media Type' ,
            description:'description',
            releaseDate: 'Release Date' 
        },
        stream:
        {
            provider: 'Provider', 
            title: 'Image',
            title:'Title',
            title_eng:'Title ENG',
            link:'Link',
        },
        settings:
        {
            id: 'ID', 
            section: 'Section',
            key:'Key',
            value:'Value',
        },
    },
    buttons: {
        dataTableRefreshButton: 'Refresh',
        dataTableColumnVisibilityhButton: 'Column Visibility',
        releaseAddSubmit: 'Submit',
        releaseAddButton:'Add',
        releaseUpdateAllButton:'Update All',
        releaseEditButton:'Edit',
        releaseDeleteButton:'Delete',
        releaseUpdateButton:'Update',
        expandButton:'Expand',
        tolokaDownloadButton:"Direct Download",
        tolokaAddButton:"Add to client",
        tolokaCopyButton:"Copy Values",
        settingSaveButton: "Save",
        settingsAdd:"Add",
        settingsSyncTo:"Sync to app.ini",
        settingsSyncFrom:"Sync from app.ini",
        settingsUpdateButton:"Update",
        closeButton: "Close",
        signInButton: "Sign in",
        registerButton: "Register",
        parseButton: "Parse Binary",
        cancelButton: "Cancel"
    },
    labels: {
        dataTableSearchInput: "Filter records",
        dataTablesYearText:"years",
        dataTablesDaysText:"days",
        dataTablesHrsText:"hrs ago",
        dataTablesLoadingText:"Loading...",
        newVersionToastTitle:"New Release: ",
        operationStatusGithub: "Create an issue on github if something wrong.",
        buttonsLoadingText:"Loading...",
        releaseAddIndex: 'Index',
        releaseAddNumber:'Number',
        noImageAvailable:'No image available',
        checkVersions: 'Installed Packages',
        settingsNotification: 'Page shows last saved settings in DB. Please use Sync to and Sync from to keep them up to date state.',
        toggleTheme: 'Toggle theme',
        toggleLanguage: 'Toggle language',
        createAccount: 'Create Account',
        pleaseSignIn: 'Please sign in',
        systemActions: 'System Actions',
        showVersions: 'Show Versions',
        syncTitlesFromDb: 'Sync titles.ini from DB',
        syncTitlesToDb: 'Sync titles.ini to DB',
        profileSettings: 'Profile settings coming soon...',
        userManagement: 'User management coming soon...',
        editRelease: 'Edit Release',
        addRelease: 'Add Release',
        addedTitles: 'Added Titles',
        indexExtractor: 'Index Extractor',
        provideValidFilename: 'Please provide a valid filename.',
        newSuggestions: 'New suggestions',
        newStreams: 'New streams',
        seed: 'seed',
        notFound: 'Not Found',
        system: 'System',
        profile: 'Profile',
        configuration: 'Configuration',
        users: 'Users',
        light: 'Light',
        dark: 'Dark',
        ongoing: 'Ongoing',
        ongoingDescription: 'Use episode range naming (S01E01-E02) instead of season pack (S01)',
        releaseGroup: 'Release Group',
        meta: 'Meta',
        releaseGroupMeta: 'Release group & Meta',
        releasePreview: 'Preview'
    },
    validation: {
        invalidTitle: 'Title contains invalid characters that could break paths or JSON (/, \\, :, *, ?, ", <, >, |)',
        invalidNumber: 'Please enter a valid number',
        invalidUrl: 'Please enter a valid Toloka URL (should start with https://toloka.to/)'
    },
    pages: {
        titles: {
            base: 'Toloka2Web'
        }
    }
};

export default translations;