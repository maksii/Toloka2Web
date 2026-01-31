import { DataTableFactory } from '../common/data-table-factory.js';
import { ApiService } from '../common/api-service.js';
import { UiManager } from '../common/ui-manager.js';
import { Utils, translations } from '../common/utils.js';

export default class ReleasesDetails {
    constructor() {
        this.table = null;
        this.releaseId = null;
        this.releaseForm = document.querySelector('#releaseForm');
        this.submitButton = document.querySelector('#submitButton');
    }

    async init() {
        this.releaseId = this.getReleaseIdFromUrl();
        await this.loadReleaseDetails();
        this.initializeDataTable();
        this.addEventListeners();
    }

    getReleaseIdFromUrl() {
        return Utils.getIdFromUrl();
    }

    async loadReleaseDetails() {
        try {
            const data = await ApiService.get(`../api/releases/${this.releaseId}`);
            if (data && data[0]) {
                document.querySelector('#releaseTitle').textContent = data[0].title;
                document.querySelector('#releaseStatus').textContent = data[0].status.name;
                document.querySelector('#releaseType').textContent = data[0].type.name;
            }
        } catch (error) {
            console.error('Error loading release details:', error);
        }
    }

    initializeDataTable() {
        const config = {
            ajax: `../api/releases/${this.releaseId}/files`,
            columns: [
                DataTableFactory.createLinkColumn('id', translations.tableHeaders.releaseDetails.id, '/files/'),
                { data: 'name', title: translations.tableHeaders.releaseDetails.name, visible: true },
                { data: 'size', title: translations.tableHeaders.releaseDetails.size, visible: true },
                { data: 'status', title: translations.tableHeaders.releaseDetails.status, visible: true },
                { data: 'type', title: translations.tableHeaders.releaseDetails.type, visible: true },
                DataTableFactory.createDateColumn('created', translations.tableHeaders.releaseDetails.created),
                DataTableFactory.createActionColumn(() => this.renderActionButtons())
            ],
            order: [[5, 'desc']],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };
        
        this.table = DataTableFactory.initializeTable('#filesTable', config);
        this.table.on('draw', () => {
            Utils.activeTooltips();
        });
    }

    addEventListeners() {
        if (this.releaseForm) {
            this.releaseForm.addEventListener('submit', async (e) => this.handleFormSubmit(e));
        }
    }

    renderActionButtons() {
        return `
            ${Utils.renderActionButton("action-update", "btn-outline-primary", "", "bi-pencil-square", translations.buttons.releaseDetailsUpdateButton)}
            ${Utils.renderActionButton("action-delete", "btn-outline-danger", "", "bi-trash", translations.buttons.releaseDetailsDeleteButton)}
        `;
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        try {
            UiManager.setButtonLoading(this.submitButton);
            
            const formData = new FormData(this.releaseForm);
            const result = await ApiService.post('/api/files', formData);

            // Show operation results
            UiManager.showOperationResults(result);
            
            // Close modal and refresh table
            UiManager.hideModal('addFileModal');
            if (this.table) {
                this.table.ajax.reload();
            }

        } catch (error) {
            console.error('Error submitting form:', error);
        } finally {
            UiManager.resetButton(this.submitButton, translations.buttons.releaseDetailsSubmit);
        }
    }

    async handleAction(actionName, element) {
        const tr = element.closest('tr');
        const row = this.table.row(tr);
        const data = row.data();

        const actions = {
            update: () => this.updateFile(data),
            delete: () => this.deleteFile(data)
        };

        const action = actions[actionName];
        if (action) {
            await action();
        } else {
            console.error(`No handler defined for action: ${actionName}`);
        }
    }

    async updateFile(data) {
        try {
            const result = await ApiService.put(`/api/files/${data.id}`, data);
            UiManager.showOperationResults(result);
            this.table.ajax.reload();
        } catch (error) {
            console.error('Error updating file:', error);
        }
    }

    async deleteFile(data) {
        try {
            if (await UiManager.showConfirmDialog(translations.messages.releaseDetailsDeleteConfirm)) {
                const result = await ApiService.delete(`/api/files/${data.id}`);
                UiManager.showOperationResults(result);
                this.table.ajax.reload();
            }
        } catch (error) {
            console.error('Error deleting file:', error);
        }
    }
} 
