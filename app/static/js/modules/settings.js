// static/js/modules/settings.js
import { DataTableFactory } from '../common/data-table-factory.js';
import { EventDelegator } from '../common/datatable.js';
import { ApiService } from '../common/api-service.js';
import { UiManager } from '../common/ui-manager.js';
import { translations } from '../common/utils.js';

export default class Settings {
    constructor() {
        this.table = null;
        this.collapsedGroups = {};
    }

    init() {
        this.initializeDataTable();
        this.addEventListeners();
        this.checkVersions();
        document.querySelector("#configuration-tab-pane > div:nth-child(1) > div > div").innerText = translations.labels.settingsNotification;
    }

    initializeDataTable() {
        const config = {
            ajax: '/api/settings',
            columns: [
                { data: "id", title: translations.tableHeaders.settings.id, visible: true },
                { 
                    data: 'section',
                    title: translations.tableHeaders.settings.section,
                    visible: true,
                    render: (data, type) => this.renderAsInput(data, type)
                },
                { 
                    data: 'key',
                    title: translations.tableHeaders.settings.key,
                    visible: true,
                    render: (data, type) => this.renderAsInput(data, type)
                },
                { 
                    data: 'value',
                    title: translations.tableHeaders.settings.value,
                    visible: true,
                    render: (data, type) => this.renderAsInput(data, type)
                },
                DataTableFactory.createActionColumn(() => this.renderActionButton())
            ],
            columnDefs: [
                { targets: [0], searchable: false, orderable: false, className: "align-middle" },
                { targets: [1, 2, 3], className: "align-middle" },
                { targets: [4], searchable: false, orderable: false, className: "align-middle text-center" }
            ],
            rowGroup: {
                dataSrc: 'section',
                startRender: (rows, group) => this.renderRowGroup(rows, group)
            },
            paging: false,
            order: [[1, 'des']],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout(),
                top1End: {
                    buttons: this.getTableButtons()
                }
            }
        };

        this.table = DataTableFactory.initializeTable('#settingsTable', config);
    }

    renderAsInput(data, type) {
        if (type === 'display') {
            return `<input type="text" class="form-control" value="${data}">`;
        }
        return data;
    }

    renderActionButton() {
        return `<button class="btn btn-outline-warning action-save">
            <i class="bi bi-pencil-square"></i>
            <span class="visually-hidden">${translations.buttons.settingSaveButton}</span>
        </button>`;
    }

    renderRowGroup(rows, group) {
        const collapsed = !!this.collapsedGroups[group];
        
        rows.nodes().each(function(r) {
            r.style.display = collapsed ? '' : 'none';
        });

        return $('<tr/>')
            .append(`<td class="action-collapse" colspan="8">${group} (${rows.count()})</td>`)
            .attr('data-name', group)
            .toggleClass('collapsed', collapsed);
    }

    getTableButtons() {
        return [
            {
                text: translations.buttons.settingsAdd,
                className: 'btn btn-primary',
                action: () => this.addNewRow()
            },
            {
                text: translations.buttons.settingsSyncTo,
                className: 'btn btn-primary',
                action: () => this.syncSettings("to", "app")
            },
            {
                text: translations.buttons.settingsSyncFrom,
                className: 'btn btn-primary',
                action: () => this.syncSettings("from", "app")
            }
        ];
    }

    addEventListeners() {
        new EventDelegator('#settingsTable tbody', this.handleAction.bind(this));
        document.querySelector('#syncTorrentReleaseTo').addEventListener('click', () => this.syncSettings('to', 'release'));
        document.querySelector('#syncTorrentReleaseFrom').addEventListener('click', () => this.syncSettings('from', 'release'));
    }

    handleAction(actionName, element) {
        const actions = {
            save: () => this.saveSettingAction(element),
            collapse: () => this.groupToggle(element)
        };

        const action = actions[actionName];
        if (action) {
            action();
        } else {
            console.error(`No handler defined for action: ${actionName}`);
        }
    }

    async syncSettings(direction, type) {
        try {
            const formData = new FormData();
            formData.append('direction', direction);
            formData.append('type', type);
            
            const result = await ApiService.post('/api/settings/sync', formData);
            this.table.ajax.reload();
            
        } catch (error) {
            console.error('Error syncing settings:', error);
        }
    }

    groupToggle(element) {
        const name = element.parentElement.getAttribute('data-name');
        this.collapsedGroups[name] = !this.collapsedGroups[name];
        this.table.draw(false);
    }

    async saveSettingAction(target) {
        try {
            UiManager.setButtonLoading(target);
            
            const row = this.table.row(target.closest('tr'));
            const rowData = row.data();
            const inputs = row.node().querySelectorAll('input');
            
            const formData = new FormData();
            formData.append('id', rowData.id);
            formData.append('section', inputs[0].value);
            formData.append('key', inputs[1].value);
            formData.append('value', inputs[2].value);

            await ApiService.post(`/api/settings/${rowData.id}`, formData);
            this.table.ajax.reload();
            
        } catch (error) {
            console.error('Error saving setting:', error);
        } finally {
            UiManager.resetButton(target);
        }
    }

    addNewRow() {
        const data = this.table.data().toArray();
        const newRowId = data.length > 0 
            ? Math.max(...data.map(o => o.id)) + 1 
            : 1;

        this.table.row.add({
            id: newRowId,
            section: '',
            key: '',
            value: ''
        }).draw(false);

        const newRow = this.table.row(':last').node();
        newRow.querySelector('input:first-child').focus();
    }

    checkVersions() {
        const showToastButton = document.getElementById('showToast');
        showToastButton.addEventListener('click', async () => {
            try {
                const data = await ApiService.get('/api/settings/versions');
                const formattedContent = this.formatVersionContent(data);
                UiManager.showToast(translations.labels.checkVersions, formattedContent);
            } catch (error) {
                console.error('Error fetching version data:', error);
            }
        });
    }

    formatVersionContent(data) {
        let contentHTML = '<ol class="list-group list-group-numbered">';
        for (const [key, value] of Object.entries(data)) {
            contentHTML += `
                <li class="list-group-item d-flex justify-content-between align-items-start">
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${key}</div>
                        ${key}
                    </div>
                    <span class="badge text-bg-primary rounded-pill">${value}</span>
                </li>
            `;
        }
        contentHTML += '</ol>';
        return contentHTML;
    }
}