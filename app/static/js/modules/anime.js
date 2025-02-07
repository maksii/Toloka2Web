// static/js/modules/anime.js
import { DataTableFactory } from '../common/data-table-factory.js';
import { ApiService } from '../common/api-service.js';
import translations from '../l18n/en.js';

export default class Anime {
    constructor() {
        this.table = null;
    }

    init() {
        this.initializeDataTable();
    }

    initializeDataTable() {
        const config = {
            ajax: '/api/anime',
            columns: [
                DataTableFactory.createLinkColumn('id', translations.tableHeaders.anime.id, '/anime/'),
                { data: 'titleUa', title: translations.tableHeaders.anime.titleUa, visible: true },
                { data: 'titleEn', title: translations.tableHeaders.anime.titleEn, visible: true },
                { data: 'season', title: translations.tableHeaders.anime.season, visible: true },
                { 
                    data: 'type.name', 
                    title: translations.tableHeaders.anime.type, 
                    visible: true 
                },
                { 
                    data: 'status.name', 
                    title: translations.tableHeaders.anime.status, 
                    visible: true 
                },
                DataTableFactory.createDateColumn('releaseDate', translations.tableHeaders.anime.releaseDate)
            ],
            order: [[6, 'desc']],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };
        
        this.table = DataTableFactory.initializeTable('#animeTable', config);
    }
}