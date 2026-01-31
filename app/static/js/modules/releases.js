// static/js/modules/releases.js
import { DataTableFactory } from '../common/data-table-factory.js';
import { EventDelegator } from '../common/datatable.js';
import { ApiService } from '../common/api-service.js';
import { UiManager } from '../common/ui-manager.js';
import { Utils, translations } from '../common/utils.js';

export default class Releases {
    constructor() {
        this.table = null;
        this.tableBody = null;
    }

    init() {
        this.initializeDataTable();
        this.addEventListeners();
        this.setupTableCallbacks();
    }

    setupTableCallbacks() {
        this.table.on('draw', () => {
            Utils.activeTooltips();
        });
    }

    initializeDataTable() {
        const config = {
            ajax: '/api/releases',
            columns: [
                { data: 'codename', title: translations.tableHeaders.releases.codename, visible: true },
                { 
                    data: 'torrent_name',
                    type: 'html',
                    title: translations.tableHeaders.releases.torrent_name,
                    render: (data, type, row) => this.renderTorrentInfo(data, type, row),
                    visible: true 
                },
                { data: 'season_number', title: translations.tableHeaders.releases.season_number, visible: false },
                { data: 'episode_index', title: translations.tableHeaders.releases.episode_index, visible: false },
                { data: 'adjusted_episode_number', title: translations.tableHeaders.releases.adjusted_episode_number, visible: false },
                DataTableFactory.createDateColumn('publish_date', translations.tableHeaders.releases.publish_date),
                { data: 'release_group', title: translations.tableHeaders.releases.release_group, visible: false },
                { data: 'download_dir', title: translations.tableHeaders.releases.download_dir, visible: false },
                DataTableFactory.createLinkColumn('guid', translations.tableHeaders.releases.guid, 'https://toloka.to/'),
                { data: 'hash', title: translations.tableHeaders.releases.hash, visible: false },
                { data: 'meta', title: translations.tableHeaders.releases.meta, visible: false },
                { 
                    data: 'is_partial_season', 
                    title: translations.tableHeaders.releases.ongoing, 
                    visible: true,
                    render: (data, type, row) => {
                        if (type === 'display') {
                            const isOngoing = data === 'true' || data === true || data === 'True';
                            return isOngoing 
                                ? '<i class="bi bi-check-circle-fill text-success" title="Ongoing"></i>'
                                : '<i class="bi bi-x-circle-fill text-secondary" title="Completed"></i>';
                        }
                        return data;
                    }
                },
                DataTableFactory.createActionColumn(() => this.renderActionButtons())
            ],
            order: [[5, 'desc']],
            columnDefs: [
                {
                    searchPanes: {
                        show: true
                    },
                    targets: [1, 6, 8]
                }
            ],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout(),
                top1End: {
                    buttons: this.getTableButtons()
                }
            }
        };

        this.table = DataTableFactory.initializeTable('#dataTableTitles', config);
        this.tableBody = document.querySelector('#dataTableTitles tbody');
        
        // Listen for release added events to refresh the table
        window.addEventListener('releaseAdded', () => {
            this.table.ajax.reload();
        });
    }

    getTableButtons() {
        return [
            {
                text: translations.buttons.releaseAddButton,
                className: 'btn btn-primary',
                action: () => Utils.addRelease()
            },
            {
                text: translations.buttons.releaseUpdateAllButton,
                className: 'btn btn-primary',
                action: (e, dt, node) => this.updateAllReleases(node)
            }
        ];
    }

    renderTorrentInfo(data, type, row) {
        let cleanedValue = data.replace(/^"|"$/g, '');
        if (type === 'display') {
            const torrentInfo = row.torrent_info || {
                progress: 0,
                name: "Not Found",
                state: "Not Found"
            };

            const progress = Utils.progressPercentage(torrentInfo.progress);
            const progressColor = Utils.getColorForProgress(progress);

            return `<span style="color: ${progressColor};"
                data-bs-toggle="tooltip" 
                data-bs-placement="top"
                data-bs-custom-class="custom-tooltip"
                data-bs-title="${torrentInfo.state} | ${progress} | ${torrentInfo.name}">${cleanedValue}</span>`;
        }
        return cleanedValue;
    }

    renderActionButtons() {
        return `
            ${Utils.renderActionButton("action-edit", "btn-outline-warning", "", "bi-pencil-square", translations.buttons.releaseEditButton)}
            ${Utils.renderActionButton("action-delete", "btn-outline-danger", "", "bi-trash", translations.buttons.releaseDeleteButton)}
            ${Utils.renderActionButton("action-update", "btn-outline-primary", "", "bi-arrow-clockwise", translations.buttons.releaseUpdateButton)}
            ${Utils.renderActionButton("action-forceupdate", "btn-outline-info", "", "bi-arrow-repeat", translations.buttons.releaseForceUpdateButton)}
        `;
    }

    addEventListeners() {
        new EventDelegator('#dataTableTitles tbody', this.handleAction.bind(this));
        document.querySelector('#editReleaseSubmitForm').addEventListener('click', () => this.submitEditForm());
    }

    handleAction(actionName, element) {
        const tr = element.closest('tr');
        const row = this.table.row(tr).data();

        const actions = {
            edit: () => this.populateEditForm(row),
            delete: () => this.deleteRelease(element, row),
            update: () => this.updateRelease(element, row),
            forceupdate: () => this.forceUpdateRelease(element, row)
        };

        const action = actions[actionName];
        if (action) {
            action();
        } else {
            console.error(`No handler defined for action: ${actionName}`);
        }
    }

    async deleteRelease(target, row) {
        try {
            UiManager.setButtonLoading(target);

            const formData = new FormData();
            formData.append('codename', row.codename);

            await ApiService.delete('/api/releases', formData);
            this.table.ajax.reload();

        } catch (error) {
            console.error('Error deleting release:', error);
        } finally {
            UiManager.resetButton(target);
        }
    }

    populateEditForm(formData) {
        const form = document.getElementById('dataForm');
        form.innerHTML = '<div class="row">';

        const createColumn = () => {
            const col = document.createElement('div');
            col.className = 'col-md-4';
            return col;
        };

        let currentColumn = createColumn();
        let fieldCount = 0;

        // Fields to exclude from the text inputs (handled separately or not needed)
        const excludedFields = ['torrent_info', 'ongoing', 'is_partial_season'];

        // Sort keys to ensure 'codename' is first
        const keys = Object.keys(formData)
            .filter(key => !excludedFields.includes(key))
            .sort((a, b) => {
                if (a === 'codename') return -1;
                if (b === 'codename') return 1;
                return 0;
            });

        keys.forEach(key => {
            if (fieldCount % 5 === 0 && fieldCount !== 0) {
                form.firstChild.appendChild(currentColumn);
                currentColumn = createColumn();
            }

            const value = String(formData[key] || '').replace(/"/g, '&quot;');
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            const div = document.createElement('div');
            div.className = 'form-floating mb-3';
            div.innerHTML = `
                <input type="text" class="form-control" id="${key}" name="${key}" placeholder="${label}" value="${value}">
                <label for="${key}">${label}</label>
            `;
            currentColumn.appendChild(div);
            fieldCount++;
        });

        form.firstChild.appendChild(currentColumn);
        form.innerHTML += '</div>';

        // Add Ongoing checkbox at the end - check is_partial_season field from API
        const isPartialValue = formData.is_partial_season;
        const ongoingChecked = isPartialValue === 'true' || isPartialValue === true || isPartialValue === 'True';
        const ongoingDiv = document.createElement('div');
        ongoingDiv.className = 'form-check form-switch mb-3 mt-3';
        ongoingDiv.innerHTML = `
            <input class="form-check-input" type="checkbox" role="switch" name="ongoing" id="editOngoing" ${ongoingChecked ? 'checked' : ''}>
            <label class="form-check-label" for="editOngoing">
                <i class="bi bi-arrow-repeat me-1"></i>${translations.labels.ongoing || 'Ongoing'}
                <small class="text-muted d-block">${translations.labels.ongoingDescription || 'Use episode range naming (S01E01-E02) instead of season pack (S01)'}</small>
            </label>
        `;
        form.appendChild(ongoingDiv);

        UiManager.showModal('editRelease');
    }

    async submitEditForm() {
        try {
            const formData = new FormData(document.getElementById('dataForm'));
            
            // Handle ongoing checkbox - ensure it's sent as a proper boolean value
            const ongoingCheckbox = document.querySelector('#editOngoing');
            formData.set('ongoing', ongoingCheckbox && ongoingCheckbox.checked ? 'true' : 'false');
            
            await ApiService.put('/api/releases', formData);
            this.table.ajax.reload();
            UiManager.hideModal('editRelease');
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    }

    async updateRelease(target, row) {
        try {
            UiManager.setButtonLoading(target);

            const formData = new FormData();
            formData.append('codename', row.codename);

            const result = await ApiService.post('/api/releases/update', formData);
            UiManager.showOperationResults(result);
            this.table.ajax.reload();

        } catch (error) {
            console.error('Error updating release:', error);
        } finally {
            UiManager.resetButton(target);
        }
    }

    async forceUpdateRelease(target, row) {
        try {
            UiManager.setButtonLoading(target);

            const formData = new FormData();
            formData.append('codename', row.codename);
            formData.append('force', 'true');

            const result = await ApiService.post('/api/releases/update', formData);
            UiManager.showOperationResults(result);
            this.table.ajax.reload();

        } catch (error) {
            console.error('Error force updating release:', error);
        } finally {
            UiManager.resetButton(target);
        }
    }

    async updateAllReleases(node) {
        try {
            UiManager.setButtonLoading(node[0], translations.buttons.releaseUpdateAllButton);
            
            const result = await ApiService.post('/api/releases/update', {});
            UiManager.showOperationResults(result);
            this.table.ajax.reload();

        } catch (error) {
            console.error('Error updating all releases:', error);
        } finally {
            UiManager.resetButton(node[0]);
        }
    }
}
