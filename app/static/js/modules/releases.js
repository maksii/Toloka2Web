// static/js/modules/releases.js
import { DataTableManager, EventDelegator } from '../common/datatable.js';
import { Utils } from '../common/utils.js';
import translations from '../l18n/en.js';

export default class Releases {
    constructor() {
        this.table = null;
    }

    init() {
        this.initializeDataTable();
        new EventDelegator('#dataTableTitles tbody', this.handleAction.bind(this));
        this.addEventListeners();
    }

    tableBody = document.querySelector('#dataTableTitles tbody');

    initializeDataTable() {
        const config = {
            ajax: {
                url: 'api/releases',
                dataSrc: function(json) {
                    if (json.error) {
                        return [];  // Return an empty array to DataTables
                    }
                    var result = [];
                    Object.keys(json).forEach(function(key) {
                        var item = json[key];
                        item.codename = key;
                        result.push(item);
                    });
                    return result;
                },
                error: function(xhr, error, thrown) {
                    console.log(xhr.responseJSON.error)
                }
            },
            responsive: true,
            columns: [
                { data: 'codename', title: translations.tableHeaders.releases.codename, visible: true },
                { data: 'torrent_name', title: translations.tableHeaders.releases.torrent_name, render: function(data, type, row) { return data.replace(/^"|"$/g, '');}, visible: true },
                { data: 'season_number', title: translations.tableHeaders.releases.season_number , visible: false},
                { data: 'episode_index', title: translations.tableHeaders.releases.episode_index, visible: false },
                { data: 'adjusted_episode_number', title: translations.tableHeaders.releases.adjusted_episode_number, visible: false },
                { data: 'publish_date', title: translations.tableHeaders.releases.publish_date, render: function(data, type, row) { return DataTableManager.customDateRenderer(data, type, row)}, visible: true  },
                { data: 'release_group', title: translations.tableHeaders.releases.release_group, visible: false },
                { data: 'download_dir', title: translations.tableHeaders.releases.download_dir, visible: false },
                { data: 'ext_name', title: translations.tableHeaders.releases.ext_name, visible: false },
                { data: 'guid', title: translations.tableHeaders.releases.guid, render: function(data, type, row) { return DataTableManager.dataTableRenderAsUrl("https://toloka.to", data, data)}, visible: true },
                { data: 'hash', title: translations.tableHeaders.releases.hash, visible: false },
                { data: 'meta', title: translations.tableHeaders.releases.meta, visible: false },
                { data: null, title: translations.tableHeaders.releases.actions, orderable: false, render: (data, type, row) => { return this.dataTableRenderActionButtons(data, type, row) }, visible: true }
            ],
            order: [[5, 'des']],
            columnDefs: [
                {
                    searchPanes: {
                        show: true
                    },
                    targets: [1, 6, 8]
                }
            ],
            layout: {
                topStart: DataTableManager.returnDefaultLayout(),
                top1End:
                {
                    buttons:[
                        {
                            text: translations.buttons.releaseAddButton,
                            className: 'btn btn-primary',
                            action: () => { Utils.addRelease(); }
                        },
                        {
                            text: translations.buttons.releaseUpdateAllButton,
                            className: 'btn btn-primary',
                            action: ( e, dt, node, config) => { this.dataTableUpdateAllAction(e, dt, node, config)}
                        }
                    ]
                }
            },
            language: DataTableManager.returnDefaultLanguage()
        }
        this.table = DataTableManager.initializeDataTable('#dataTableTitles', config);
        this.tableBody = document.querySelector('#dataTableTitles tbody');
    }

    dataTableRenderActionButtons(data, type, row) {
        let editButton = Utils.renderActionButton("action-edit","btn-outline-warning", "disabled", "bi-pencil-square", translations.buttons.releaseEditButton);
        let deleteButton = Utils.renderActionButton("action-delete","btn-outline-danger", "disabled", "bi-trash", translations.buttons.releaseDeleteButton);
        let updateButton = Utils.renderActionButton("action-update","btn-outline-primary", "", "bi-arrow-clockwise", translations.buttons.releaseUpdateButton);
        return `${editButton}
        ${deleteButton}
        ${updateButton}`;
    }

    dataTableUpdateAllAction(e, dt, node, config)
    {
        node[0].disabled = true;
        node[0].innerHTML = Utils.renderButtonSpinner();

        fetch('/api/releases/', { method: 'POST' })
        .then(response => response.json())
        .then(result => {
            node[0].innerHTML = `<i class="bi bi-arrow-clockwise"></i> ${translations.buttons.releaseUpdateAllButton}`;
            node[0].disabled = false;

            const bsOperationOffcanvas = new bootstrap.Offcanvas('#offcanvasOperationResults');
            Utils.generateOperationResponseOffCanvas(result);  // Display operation status
            bsOperationOffcanvas.toggle();
            DataTableManager.refreshTable(this.table);
        });
    }

    addEventListeners() {
    }

    handleAction(actionName, element) {
        const actionHandlers = {
          edit: () => console.log(`Editing release associated with ${element}`),
          delete: () => console.log(`Deleting release associated with ${element}`),
          update: () => this.updateRelease(element),
        };
    
        const actionFunction = actionHandlers[actionName];
        if (actionFunction) {
          actionFunction();
        } else {
          console.error(`No handler defined for action: ${actionName}`);
        }
      }

    async updateRelease(target) {
        let tr = target.closest('tr');
        let row = this.table.row(tr).data();

        target.disabled = true;
        target.innerHTML = Utils.renderButtonSpinner();

        // Assuming `codename` is a property of the row data
        let formData = new FormData();
        formData.append('codename', row.codename);

        fetch('/api/releases/update', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(detail => {
            target.innerHTML = `<i class="bi bi-arrow-clockwise"></i> ${translations.buttons.releaseUpdateButton}`;
            target.disabled = false;

            const bsOperationOffcanvas = new bootstrap.Offcanvas('#offcanvasOperationResults');
            Utils.generateOperationResponseOffCanvas(detail);  // Display operation status
            bsOperationOffcanvas.toggle();
            DataTableManager.refreshTable(this.table);
        })
        .catch(error => {
            console.error('Error:', error);
            target.innerHTML = `<i class="bi bi-arrow-clockwise"></i> ${translations.buttons.releaseUpdateButton}`;
            target.disabled = false;
        });
    }
}