// static/js/modules/studio-details.js
import { DataTableManager } from '../common/datatable.js';
import { Utils } from '../common/utils.js';

export default class StudiosDetails {
    constructor() {
        this.table = null;
    }

    init() {
        const url = new URL(window.location.href);
        const segments = url.pathname.split('/');
        const studioId = segments.pop();
    
        // Fetch and display studio details
        $.getJSON(`../api/studio//${studioId}`, function(data) {
            $('#studioName').text(data[0].name);
            $('#studioTelegram').text(data[0].telegram);
        });
        this.initializeDataTable(studioId);
    }

    initializeDataTable(studioId) {
        const config = {
            ajax: {
                url:  `../api/studio/${studioId}/anime`,
                dataSrc: function(json) {
                    var result = [];
                    Object.keys(json).forEach(function(key) {
                        var item = json[key];
                        item.codename = key;
                        result.push(item);
                    });
                    return result;
                }
            },
            responsive: true,
            columns: [
                { data: "id", title: 'ID', render: function(data, type, row) {
                    return `<a href="/anime/${data}">${data}</a>`;
                }, visible: true },
                { data: 'titleUa', title: 'UA', visible: true },
                { data: 'titleEn', title: 'EN', visible: true },
                { data: 'releaseDate', title: 'releaseDate', visible: true },
            ],
            order: [[3, 'des']],
            layout: {
                topStart: DataTableManager.returnDefaultLayout()
            },
            language: DataTableManager.returnDefaultLanguage()
        };
        this.table = DataTableManager.initializeDataTable('#titlesTable', config);
    }
}