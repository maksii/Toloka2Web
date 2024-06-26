// static/js/modules/setttings.js
import { DataTableManager, EventDelegator } from '../common/datatable.js';
import { Utils } from '../common/utils.js';

export default class Settings {
    constructor() {
        this.table = null;
    }

    init() {
        this.initializeDataTable();
        this.addEventListeners();
        this.checkVersions();
        //DataTableManager.onDataTableXhr(this.table);
    }
    settingsTableBody = document.querySelector('#settingsTable tbody');
    collapsedGroups = {};

    initializeDataTable() {
        const config = {
            ajax: {
                url: '/api/settings',
                dataSrc: function(json) {
                    return json;
                }
            },
            responsive: true,
            columns: [
                { data: "id", title: 'ID', visible: true },
                { data: 'section', title: 'Section', visible: true, render: function(data, type, row) {
                    if (type === 'display') {
                        return DataTableManager.dataTableRenderAsInput(data);
                    }
                    return data;
                } },
                { data: 'key', title: 'Key', visible: true, render: function(data, type, row) {
                    if (type === 'display') {
                        return DataTableManager.dataTableRenderAsInput(data);
                    }
                    return data;
                } },
                { data: 'value', title: 'Value', visible: true, render: function(data, type, row) {
                    if (type === 'display') {
                        return DataTableManager.dataTableRenderAsInput(data);
                    }
                    return data;
                } },
                { data: null, defaultContent: Utils.renderActionButton("action-save","btn-outline-warning", "", "bi-pencil-square", "Save") }
            
            ],
            columnDefs: [
                { targets: [0], searchable: false, orderable: false, className: "align-middle" },
                { targets: [1, 2, 3], className: "align-middle" },
                { targets: [4], searchable: false, orderable: false, className: "align-middle text-center" }
            ],
            rowGroup: {
                dataSrc: 'section',
                startRender: (rows, group, level) => {
                    var collapsed = !!this.collapsedGroups[group];
            
                    rows.nodes().each(function (r) {
                      r.style.display = 'none';
                      if (collapsed) {
                        r.style.display = '';
                      }});
            
                    // Add category name to the <tr>. NOTE: Hardcoded colspan
                    return $('<tr/>')
                      .append('<td class="action-collapse" colspan="8">' + group + ' (' + rows.count() + ')</td>')
                      .attr('data-name', group)
                      .toggleClass('collapsed', collapsed);
                  }
            },
            paging: false,
            order: [[1, 'des']],
            layout: {
                topStart: DataTableManager.returnDefaultLayout(),
                top1End:
                {
                    buttons:[
                        {
                            text: 'Add',
                            className: 'btn btn-primary',
                            action: () => {
                                var newRowId = 1;
                                var data = this.table.data().toArray();
                                if (data.length > 0) {
                                    newRowId = Math.max.apply(Math, data.map(function(o) { return o.id; })) + 1;
                                }
                                this.table.row.add({
                                    id: newRowId,
                                    section: '',
                                    key: '',
                                    value: ''
                                }).draw(false);
                        
                                // Focus on the first input of the new row
                                var newRow = this.table.row(':last').node();
                                newRow.querySelector('input:first-child').focus();
                            }
                        },
                        {
                            text: 'Sync to app.ini',
                            className: 'btn btn-primary',
                            action: function () {
                                console.log('TBD');
                            }
                        },
                        {
                            text: 'Sync from app.ini',
                            className: 'btn btn-primary',
                            action: function () {
                                console.log('TBD');
                            }
                        }
                    ]
                }
            },
            language: DataTableManager.returnDefaultLanguage()
        };
        this.table = DataTableManager.initializeDataTable('#settingsTable', config);
        this.settingsTableBody = document.querySelector('#settingsTable tbody');
    }

    addEventListeners() {
        new EventDelegator('#settingsTable tbody', this.handleAction.bind(this));
    }

    handleAction(actionName, element) {
        const actionHandlers = {
          save: () => this.saveSettingAction(element),
          collapse: () => this.groupToggle(element),
        };
    
        const actionFunction = actionHandlers[actionName];
        if (actionFunction) {
          actionFunction();
        } else {
          console.error(`No handler defined for action: ${actionName}`);
        }
      }

    groupToggle(element)
    {
        var name = element.parentElement.getAttribute('data-name');
        this.collapsedGroups[name] = !this.collapsedGroups[name];
        this.table.draw(false);
    }

    saveSettingAction(target)
    {
        const row = this.table.row(target.closest('tr'));
        var rowData = row.data();

        console.log('Original data', rowData);

        const inputs = row.node().querySelectorAll('input');
        var updatedData = {};
        updatedData.section = inputs[0].value;
        updatedData.key = inputs[1].value;
        updatedData.value = inputs[2].value;

        target.disabled = true;
        target.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';

        let formData = new FormData();
        formData.append('id', rowData.id);
        formData.append('section', updatedData.section);
        formData.append('key', updatedData.key);
        formData.append('value', updatedData.value);
    
        fetch(`/api/settings/${rowData.id}`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(detail => {
            target.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Update';
            target.disabled = false;
            this.table.ajax.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            target.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Update';
            target.disabled = false;
        });
        
    }

    checkVersions()
    {
        const showToastButton = document.getElementById('showToast');

        showToastButton.addEventListener('click', () => {
            fetch('/api/settings/versions')
            .then(response => response.json())
            .then(data => {
                const formattedContent = formatContent(data);
                showVersionToast("Installed Packages", formattedContent);
            })
            .catch(error => console.error('Error fetching version data:', error));
            });
    
            function showVersionToast(title, content) {
                const toastContainer = document.querySelector('.toast-container');
                const toastHTML = `
                    <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
                        <div class="toast-header">
                            <strong class="me-auto">${title}</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                        <div class="toast-body">
                            ${content}
                        </div>
                    </div>
                `;
                toastContainer.insertAdjacentHTML('beforeend', toastHTML);
                const toastElement = new bootstrap.Toast(toastContainer.lastElementChild);
                toastElement.show();
            }
    
            function formatContent(data) {
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
}