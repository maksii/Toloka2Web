// static/js/modules/studios-details.js
import { DataTableFactory } from '../common/data-table-factory.js';
import { ApiService } from '../common/api-service.js';
import { translations } from '../common/utils.js';

export default class StudiosDetails {
    constructor() {
        this.table = null;
        this.studioId = null;
    }

    async init() {
        this.studioId = this.getStudioIdFromUrl();
        await this.loadStudioDetails();
        this.initializeDataTable();
    }

    getStudioIdFromUrl() {
        const url = new URL(window.location.href);
        const segments = url.pathname.split('/');
        return segments.pop();
    }

    async loadStudioDetails() {
        try {
            const data = await ApiService.get(`../api/studio/${this.studioId}`);
            if (data && data[0]) {
                document.querySelector('#studioName').textContent = data[0].name;
                document.querySelector('#studioTelegram').textContent = data[0].telegram;
            }
        } catch (error) {
            console.error('Error loading studio details:', error);
        }
    }

    initializeDataTable() {
        const config = {
            ajax: `../api/studio/${this.studioId}/anime`,
            columns: [
                DataTableFactory.createLinkColumn('id', translations.tableHeaders.anime.id, '/anime/'),
                { data: 'titleUa', title: translations.tableHeaders.anime.titleUa, visible: true },
                { data: 'titleEn', title: translations.tableHeaders.anime.titleEn, visible: true },
                DataTableFactory.createDateColumn('releaseDate', translations.tableHeaders.anime.releaseDate)
            ],
            order: [[3, 'desc']],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };
        
        this.table = DataTableFactory.initializeTable('#titlesTable', config);
    }
}