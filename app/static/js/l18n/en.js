// en.js - English language resource file

const translations = {
    tableHeaders: {
        studioDetails:
        {
            id: 'ID',
            name: 'Name',
            telegram: 'Telegram',
        },
        anime:
        {
            id: 'ID',
            titleUa: 'UA',
            titleEn: 'EN',
            season: 'Season',
            type: 'Type',
            status: 'Status',
            releaseDate: 'Release Date',
        },
        releases:
        {
            codename: 'Codename',
            torrent_name: 'Torrent Name',
            season_number: 'Season Number',
            episode_index: 'Episode Index',
            adjusted_episode_number: 'Adjusted Episode Number',
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
            date: 'Date',
            answers: 'Answers',
            forum_url: 'Forum URL',
            leechers: 'Leechers',
            seeders: 'Seeders',
            size: 'Size',
            status: 'Status',
            torrent_url: 'Torrent URL',
            url: 'URL',
            verify: 'Verify',
            actions: 'Actions'
        },
        multi:
        {
            source: 'Source',
            image: 'Image',
            title: 'Title',
            alternative: 'Alternative',
            id: 'ID',
            status: 'Status',
            mediaType: 'Media Type',
            description: 'Description',
            releaseDate: 'Release Date'
        },
        stream:
        {
            provider: 'Provider',
            image: 'Image',
            title: 'Title',
            title_eng: 'Title ENG',
            link: 'Link',
        },
        settings:
        {
            id: 'ID',
            section: 'Section',
            key: 'Key',
            value: 'Value',
        },
        users:
        {
            id: 'ID',
            username: 'Username',
            roles: 'Roles',
            actions: 'Actions'
        },
    },
    buttons: {
        dataTableRefreshButton: 'Refresh',
        dataTableColumnVisibilityhButton: 'Column Visibility',
        releaseAddSubmit: 'Submit',
        releaseAddButton: 'Add',
        releaseUpdateAllButton: 'Update All',
        releaseEditButton: 'Edit',
        releaseDeleteButton: 'Delete',
        releaseUpdateButton: 'Update',
        releaseForceUpdateButton: 'Force Update',
        expandButton: 'Expand',
        tolokaDownloadButton: "Direct Download",
        tolokaAddButton: "Add to client",
        tolokaCopyButton: "Copy Values",
        settingSaveButton: "Save",
        settingsAdd: "Add",
        settingsSyncTo: "Sync to app.ini",
        settingsSyncFrom: "Sync from app.ini",
        settingsUpdateButton: "Update",
        closeButton: "Close",
        signInButton: "Sign in",
        registerButton: "Register",
        parseButton: "Parse Binary",
        cancelButton: "Cancel",
        saveChanges: "Save Changes",
        editButton: "Edit",
        deleteButton: "Delete"
    },
    labels: {
        dataTableSearchInput: "Filter records",
        dataTablesYearText: "years",
        dataTablesDaysText: "days",
        dataTablesHrsText: "hrs ago",
        dataTablesLoadingText: "Loading...",
        newVersionToastTitle: "New Release: ",
        operationStatusGithub: "Create an issue on github if something wrong.",
        buttonsLoadingText: "Loading...",
        releaseAddIndex: 'Index',
        releaseAddNumber: 'Number',
        noImageAvailable: 'No image available',
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
        profileSettings: 'Profile Settings',
        userManagement: 'User Management',
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
        auto: 'Auto',
        ongoing: 'Ongoing',
        ongoingDescription: 'Use episode range naming (S01E01-E02) instead of season pack (S01)',
        releaseGroup: 'Release Group',
        meta: 'Meta',
        releaseGroupMeta: 'Release group & Meta',
        releasePreview: 'Preview',
        tolokaSearchErrorTitle: 'Toloka search',
        showMoreFiles: 'Show more files',
        showLessFiles: 'Show fewer files',
        noEpisodesFound: 'No episodes found',
        studio: 'Studio',
        episodes: 'episodes',
        unknownSeries: 'Unknown Series',
        noEpisodesAvailable: 'No episodes available',
        episode: 'Episode',
        // Navigation
        home: 'Home',
        studios: 'Studios',
        anime: 'Anime',
        settings: 'Settings',
        logout: 'Logout',
        search: 'Search',
        // Search results
        searchResults: 'Search Results',
        toloka: 'Toloka',
        searchSuggestions: 'Search Suggestions',
        stream: 'Stream',
        operationResults: 'Operation Results',
        // Page titles
        voiceoverStudios: 'Voiceover Studios',
        titles: 'Titles',
        animeTitles: 'Anime Titles',
        relatedAnimes: 'Related Animes',
        animeTitle: 'Anime Title',
        description: 'Description',
        studioName: 'Studio Name',
        // Form labels
        tolokaUrl: 'Toloka URL',
        title: 'Title',
        season: 'Season',
        episodeIndex: 'Episode Index',
        indexCorrection: 'Index Correction',
        username: 'Username',
        password: 'Password',
        roles: 'Roles',
        role: 'Role',
        newPassword: 'New Password',
        confirmPassword: 'Confirm Password',
        changePassword: 'Change Password',
        rememberMe: 'Remember me',
        // User roles
        user: 'User',
        admin: 'Admin',
        // Modal titles
        editUser: 'Edit User',
        deleteUser: 'Delete User',
        // Confirmation messages
        deleteUserConfirm: 'Are you sure you want to delete this user? This action cannot be undone.',
        // Toast messages
        profileUpdated: 'Profile updated successfully',
        userUpdated: 'User updated successfully',
        userDeleted: 'User deleted successfully',
        failedLoadProfile: 'Failed to load profile data',
        failedLoadUsers: 'Failed to load users',
        failedUpdateProfile: 'Failed to update profile',
        failedUpdateUser: 'Failed to update user',
        failedDeleteUser: 'Failed to delete user',
        // Info messages
        publicApiBackup: 'The information provided is a backup of the public API from AnimeOn site.',
        settingsDevNotice: 'The page in development and in the current state is only able to display the data already saved in the database. You can change open_registration. Other properties will not make any affect, as there no sync in\\to app.ini',
        passwordRequirement: 'Password must be at least 8 characters long.',
        passwordKeepBlank: 'Leave blank to keep current password. New password must be at least 8 characters long.',
        // Form validation
        provideValidUrl: 'Please provide a valid URL.',
        provideTitle: 'Please provide a title.',
        provideValidSeason: 'Please provide a valid season number (min: 0).',
        provideValidEpisodeIndex: 'Please provide a valid episode index (min: 1).',
        // Button labels with icons
        cutTitle: 'Cut Title'
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
