// static/js/modules/releases.js
import { DataTableManager } from '../common/datatable.js';
import { Utils } from '../common/utils.js';

export default class Settings {
    constructor() {
        this.table = null;
    }

    init() {
        this.initializeDataTable();
        this.addEventListeners();
        //DataTableManager.onDataTableXhr(this.table);
    }
    settingsTableBody = document.querySelector('#settingsTable tbody');

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
                        return `<input type="text" class="form-control" value="${data}">`;
                    }
                    return data;
                } },
                { data: 'key', title: 'Key', visible: true, render: function(data, type, row) {
                    if (type === 'display') {
                        return `<input type="text" class="form-control" value="${data}">`;
                    }
                    return data;
                } },
                { data: 'value', title: 'Value', visible: true, render: function(data, type, row) {
                    if (type === 'display') {
                        return `<input type="text" class="form-control" value="${data}">`;
                    }
                    return data;
                } },
                { data: null, defaultContent: `<button class="save btn btn-success">Save</button>` }
            
            ],
            columnDefs: [
                { targets: [0], searchable: false, orderable: false, className: "align-middle" },
                { targets: [1, 2, 3], className: "align-middle" },
                { targets: [4], searchable: false, orderable: false, className: "align-middle text-center" }
            ],
            rowGroup: {
                dataSrc: 'section'
            },
            paging: false,
            order: [[1, 'des']],
            layout: {
                topStart: {
                    buttons: [
                        {
                            extend: 'searchPanes',
                            className: 'btn btn-secondary',
                            config: {
                                cascadePanes: true
                            }
                            
                        },
                        { 
                            action: function ( e, dt, node, config ) {dt.ajax.reload();},                        
                            text: '<i class="bi bi-arrow-clockwise"></i>',
                            titleAttr: 'Refresh'
                        }
                    ]
                },
                top1End:
                {
                    buttons:[
                        {
                            text: 'Add',
                            className: 'btn btn-primary',
                            action: function () {
                                var newRowId = 1;
                                var data = table.data().toArray();
                                if (data.length > 0) {
                                    newRowId = Math.max.apply(Math, data.map(function(o) { return o.id; })) + 1;
                                }
                                table.row.add({
                                    id: newRowId,
                                    section: '',
                                    key: '',
                                    value: ''
                                }).draw(false);
                        
                                // Focus on the first input of the new row
                                var newRow = table.row(':last').node();
                                $('input:first', newRow).focus();
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
            language: {
                search: "_INPUT_",
                searchPlaceholder: "Search records"
            }
        };
        this.table = DataTableManager.initializeDataTable('#settingsTable', config);
        this.settingsTableBody = document.querySelector('#settingsTable tbody');
    }

    addEventListeners() {
        this.settingsTableBody.addEventListener('click', event => this.handleTableClick(event));
        // Additional event listeners...
    }

    handleTableClick(event) {
        //'button.save'
        let target = event.target;
        while (target && !target.classList.contains('button.save')) {
            if (target === event.currentTarget) return;
            target = target.parentNode;
        }
        if (target && target.classList.contains('button.save')) {
            this.updateRelease(target);
        }

        //reset 
        var row = table.row($(this).parents('tr'));
        var rowData = row.data();
        var originalData = { id: rowData.id, name: rowData.name, age: rowData.age, country: rowData.country }; // Assuming original data can be reconstructed or fetched

        $('input', row.node()).each(function(index) {
            this.value = originalData[$(this).attr('name')];
        });
    }

    saveSettingAction(targe)
    {
        var row = table.row($(this).parents('tr'));
        var rowData = row.data();

        console.log('Original data', rowData);

        var inputs = $('input', row.node());
        var updatedData = {};
        updatedData.section = inputs[0].value;
        updatedData.key = inputs[1].value;
        updatedData.value = inputs[2].value;

        let target = event.target;
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
                table.ajax.reload();
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
    
                toastContainer.lastElementChild.addEventListener('hidden.bs.toast', function () {
                    localStorage.setItem('lastCheckedVersion', currentVersion);
                });
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