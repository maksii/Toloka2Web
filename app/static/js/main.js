// static/js/main.js
import Releases from './modules/releases.js';
import ReleasesAdd from './modules/releases-add.js';
import Search from './modules/search.js';
import Anime from './modules/anime.js';
import AnimeDetails from './modules/anime-details.js';
import Studios from './modules/studios.js';
import StudiosDetails from './modules/studios-details.js';
import Settings from './modules/settings.js';
import UpdateChecker from './common/update-checker.js';
import { DataTableFactory } from './common/data-table-factory.js';
import { Backdrop } from './common/utils.js';

class AppController {
    constructor() {
        this.modules = {
            'releases-page': Releases,
            'search-page': Search,
            'anime-page': Anime,
            'anime-details-page': AnimeDetails,
            'studios-page': Studios,
            'studios-details-page': StudiosDetails,
            'settings-page': Settings
        };

        this.commonModules = {
            search: Search,
            releasesAdd: ReleasesAdd,
            updateChecker: UpdateChecker
        };
    }

    async init() {
        try {
            // Initialize DataTable global settings
            DataTableFactory.initializeGlobalSettings();

            // Initialize backdrop
            const backdrop = new Backdrop();
            await backdrop.fetchData();
            backdrop.setRandomBackdrop();

            // Initialize common modules that should be available on all pages
            await this.initializeCommonModules();

            // Initialize page-specific module
            await this.initializePageModule();

        } catch (error) {
            console.error('Error initializing application:', error);
        }
    }

    async initializeCommonModules() {
        // Initialize search functionality (available on all pages)
        const searchModule = new this.commonModules.search();
        await searchModule.init();

        // Initialize releases add functionality (available on all pages)
        const releaseAddModule = new this.commonModules.releasesAdd();
        await releaseAddModule.init();

        // Initialize update checker
        const updateCheckerModule = new this.commonModules.updateChecker();
        await updateCheckerModule.init();
    }

    async initializePageModule() {
        // Get the page identifier from the body's ID
        const pageId = document.body.id;

        // Initialize the module corresponding to the current page
        if (this.modules[pageId]) {
            try {
                const moduleInstance = new this.modules[pageId]();
                await moduleInstance.init();
            } catch (error) {
                console.error(`Error initializing module for page ${pageId}:`, error);
            }
        } else {
            console.log('No specific module for this page or page identifier missing.');
        }
    }
}

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', async () => {
    const app = new AppController();
    await app.init();
});