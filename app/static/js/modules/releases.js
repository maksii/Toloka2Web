// static/js/modules/releases.js
import { DataTableManager } from '../common/datatable.js';
import { Utils } from '../common/utils.js';

export default class Releases {
    constructor() {
        this.table = null;
    }

    init() {
        this.initializeDataTable();
        this.addEventListeners();
    }

    tableBody = document.querySelector('#dataTableTitles tbody');
    urlButton = document.querySelector('#urlButton');
    filenameIndex = document.querySelector('#filenameIndex');
    filenameIndexGroup = document.querySelector('#filenameIndexGroup');
    cutButton = document.querySelector('#cutButton');
    releaseTitle = document.querySelector('#releaseTitle');
    submitButton = document.querySelector('#submitButton');
    releaseForm = document.querySelector('#releaseForm');  

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
                { data: 'codename', title: 'Codename', visible: true },
                { data: 'torrent_name', title: 'Torrent Name', visible: true },
                { data: 'adjusted_episode_number', title: 'Adjusted Episode Number', visible: false },
                { data: 'download_dir', title: 'Download Dir', visible: false },
                { data: 'episode_index', title: 'Episode Index', visible: false },
                { data: 'ext_name', title: 'Ext Name', visible: false },
                { data: 'guid', title: 'GUID', render: function(data, type, row) { return DataTableManager.dataTableRenderAsUrl("https://toloka.to", data, data)}, visible: true },
                { data: 'hash', title: 'Hash', visible: false },
                { data: 'meta', title: 'Meta', visible: false },
                { data: 'publish_date', title: 'Publish Date', visible: true  },
                { data: 'release_group', title: 'Release Group', visible: false },
                { data: 'season_number', title: 'Season Number' , visible: false},
                { data: null, title: 'Actions', orderable: false, render: (data, type, row) => { return this.dataTableRenderActionButtons(data, type, row) }, visible: true }
            ],
            order: [[9, 'des']],
            columnDefs: [
                {
                    searchPanes: {
                        show: true
                    },
                    targets: [1, 8, 10]
                }
            ],
            layout: {
                topStart: {
                    buttons: [
                        {
                            extend: 'colvis',
                            postfixButtons: ['colvisRestore'],
                            text: '<i class="bi bi-table"></i>',
                            titleAttr: 'Column Visibility'
                            
                        },
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
                        },
                        {
                            extend: 'pageLength',
                            className: 'btn btn-secondary'
                        }
                    ]
                },
                top1End:
                {
                    buttons:[
                        {
                            text: 'Add',
                            className: 'btn btn-primary',
                            action: () => { this.dataTableAddAction() }
                        },
                        {
                            text: 'Update All',
                            className: 'btn btn-primary',
                            action: ( e, dt, node, config) => { this.dataTableUpdateAllAction(e, dt, node, config)}
                        }
                    ]
                }
            },
            language: {
                search: "_INPUT_",
                searchPlaceholder: "Search records"
            }
        }
        this.table = DataTableManager.initializeDataTable('#dataTableTitles', config);
        this.tableBody = document.querySelector('#dataTableTitles tbody');
    }

    dataTableRenderActionButtons(data, type, row) {
        return `
            <button class="btn btn-outline-warning" disabled><span class="bi bi-pencil-square" aria-hidden="true"></span><span class="visually-hidden" role="status">Edit</span></button>
            <button class="btn btn-outline-danger" disabled><span class="bi bi-trash" aria-hidden="true"></span><span class="visually-hidden" role="status">Delete</span></button>
            <button class="btn btn-outline-primary action-update" ><span class="bi bi-arrow-clockwise" aria-hidden="true"></span><span class="visually-hidden" role="status">Update</span></button>
        `;
    }

    dataTableAddAction()
    {
        const leftSideAdd = document.querySelector('#leftSideAdd');
        leftSideAdd.classList.toggle('d-none');
        const rightSideTitles = document.querySelector('#rightSideTitles');
        rightSideTitles.classList.toggle('col-md-12');
        rightSideTitles.classList.toggle('col-md-8');
    }

    dataTableUpdateAllAction(e, dt, node, config)
    {
        node[0].disabled = true;
        node[0].innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';

        fetch('/api/releases/', { method: 'POST' })
        .then(response => response.json())
        .then(result => {
            node[0].innerHTML = '<i class="bi bi-arrow-clockwise"></i> Update All';
            node[0].disabled = false;

            const bsOperationOffcanvas = new bootstrap.Offcanvas('#offcanvasOperationResults');
            Utils.generateOperationResponseOffCanvas(result);  // Display operation status
            bsOperationOffcanvas.toggle();
            DataTableManager.refreshTable(this.table);
        });
    }

    addEventListeners() {
        this.tableBody.addEventListener('click', event => this.handleTableClick(event));
        this.urlButton.addEventListener('click', () => { this.filenameIndexGroup.classList.toggle("d-none"); });
        this.filenameIndex.addEventListener('input', () => this.extractNumbers());
        this.cutButton.addEventListener('click', () => this.cutTextTillSeparator());
        this.releaseForm.addEventListener('submit', async (e) => { await this.submitAddNewTitleForm(e) });
    }

    handleTableClick(event) {
        let target = event.target;
        while (target && !target.classList.contains('action-update')) {
            if (target === event.currentTarget) return;
            target = target.parentNode;
        }
        if (target && target.classList.contains('action-update')) {
            this.updateRelease(target);
        }
    }

    async updateRelease(target) {
        let tr = target.closest('tr');
        let row = this.table.row(tr).data();

        target.disabled = true;
        target.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';

        // Assuming `codename` is a property of the row data
        let formData = new FormData();
        formData.append('codename', row.codename);

        fetch('/api/releases/update', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(detail => {
            target.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Update';
            target.disabled = false;

            const bsOperationOffcanvas = new bootstrap.Offcanvas('#offcanvasOperationResults');
            Utils.generateOperationResponseOffCanvas(detail);  // Display operation status
            bsOperationOffcanvas.toggle();
            DataTableManager.refreshTable(this.table);
        })
        .catch(error => {
            console.error('Error:', error);
            target.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Update';
            target.disabled = false;
        });
    }
    

    
    //move to utils part of it?
    extractNumbers() {
        const input = this.filenameIndex.value;
        const numbers = input.split('').map((ch) => (ch >= '0' && ch <= '9') ? ch : ' ').join('').trim().split(/\s+/);
        const resultList = document.querySelector('#numberList');
        resultList.innerHTML = '';
    
        numbers.forEach((number, index) => {
            if (number !== '') {
                const item = document.createElement('div');
                item.className = 'list-group-item';
                item.textContent = `Index: ${index+1}, Number: ${number}`;
                item.addEventListener('click', () => {
                    document.querySelector('#index').value = index + 1;
                    resultList.style.display = 'none';
                });
                resultList.appendChild(item);
            }
        });
    
        resultList.style.display = numbers.join('').length === 0 ? 'none' : 'block';
    }

    cutTextTillSeparator()
    {
        const delimiterIndex = this.releaseTitle.value.search(/[\/|]/);
        if (delimiterIndex !== -1) {
            this.releaseTitle.value = this.releaseTitle.value.substring(delimiterIndex + 1);
        }
    }

    async submitAddNewTitleForm(e)
    {
        e.preventDefault();
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        submitButton.disabled = true;
        const formData = new FormData(releaseForm);
        const response = await fetch('/api/releases', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        submitButton.innerHTML = 'Submit';
        submitButton.disabled = false;

        const bsOperationOffcanvas = new bootstrap.Offcanvas('#offcanvasOperationResults')
        Utils.generateOperationResponseOffCanvas(result);  // Display operation status
        bsOperationOffcanvas.toggle()
        DataTableManager.refreshTable(this.table);
    }

}