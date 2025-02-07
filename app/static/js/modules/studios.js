// static/js/modules/studios.js
import { DataTableFactory } from '../common/data-table-factory.js';
import { ApiService } from '../common/api-service.js';
import translations from '../l18n/en.js';

export default class Studios {
    constructor() {
        this.table = null;
    }

    init() {
        this.initializeDataTable();
    }

    initializeDataTable() {
        const config = {
            ajax: '/api/studio',
            columns: [
                DataTableFactory.createLinkColumn('id', translations.tableHeaders.studioDetails.id, '/studios/'),
                { data: 'name', title: translations.tableHeaders.studioDetails.name, visible: true },
                { 
                    data: 'telegram',
                    title: translations.tableHeaders.studioDetails.telegram,
                    render: (data) => `<a href="${data}">${data}</a>`,
                    visible: true 
                }
            ],
            order: [[2, 'asc']],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };
        
        this.table = DataTableFactory.initializeTable('#studiosTable', config);
    }
}