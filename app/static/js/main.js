import Releases from './modules/releases.js';
import Search from './modules/search.js';
import Anime from './modules/anime.js';
import AnimeDetails from './modules/anime-details.js';
import Studios from './modules/studios.js';
import StudiosDetails from './modules/studios-details.js';
import Settings from './modules/settings.js';
import { DataTableManager } from './common/datatable.js';

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
    }

    init() {
        DataTableManager.disableAlertErrors();
        DataTableManager.handleBootstrapTabs();

        const searchModule = new Search();
        searchModule.init();

        // Get the page identifier from the body's ID
        const pageId = document.body.id;

        // Initialize the module corresponding to the current page
        if (this.modules[pageId]) {
            const moduleInstance = new this.modules[pageId]();
            moduleInstance.init();
        } else {
            console.log('No specific module for this page or page identifier missing.');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const app = new AppController();
    app.init();
});