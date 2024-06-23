// static/js/modules/search.js
import { DataTableManager, EventDelegator } from '../common/datatable.js';
import { Utils } from '../common/utils.js';
import translations from '../l18n/en.js';

export default class Search {
    constructor() {
        this.tolokaTable = null;
        this.multiTable = null;
        this.streamTable = null;
    }

    searchForm = document.querySelector('#searchForm');
    searchOffcanvas = new bootstrap.Offcanvas('#offcanvasTopSearchResults');  
    searchOffcanvasClose = document.querySelector('#offcanvasTopSearchResults > div.offcanvas-header > button');
    tolokaTableBody = document.querySelector('#torrentTable tbody');
    multiTableBody = document.querySelector('#suggested-search tbody');
    streamTableBody = document.querySelector('#tableStream tbody');


    init() {
        this.addEventListeners();
    }

    initiateOffCanvas(e)
    {
        e.preventDefault();
        const formData = new FormData(this.searchForm);
        var query = formData.get('query');
        document.querySelector("#searchResultsQuery").textContent = query;
        this.searchOffcanvas = new bootstrap.Offcanvas('#offcanvasTopSearchResults');
        this.searchOffcanvasClose = document.querySelector('#offcanvasTopSearchResults > div.offcanvas-header > button');
        
        if(this.tolokaTable == null)
            {
                this.initializeDataTable(query);
                this.addDataTablesEvents();
            }
        else
        {
            this.refreshDataTable(query);
        }

        this.searchOffcanvas.toggle()

    }

    initializeDataTable(query) {
        this.initializeTolokaDataTable(query);
        this.initializeMultiDataTable(query);
        this.initializeStreamDataTable(query);
    }

    refreshDataTable(query)
    {
        this.tolokaTable.ajax.url('/api/toloka?query=' + query).load()
        this.multiTable.ajax.url('/api/search?query=' + query).load()
        this.streamTable.ajax.url('/api/stream?query=' + query).load()
    }

    initializeTolokaDataTable(query)
    {
        const config = {
            ajax: {
                url: "/api/toloka?query=" + query,        
                dataSrc: function(json) {
                    if (json.error) {
                        return [];  // Return an empty array to DataTables
                    }
                    var result = json;
                    return result;
                },
                error: function(xhr, error, thrown) {
                    console.log(xhr.responseJSON.error)
                }
            },
            responsive: true,
            columns: [
                {   // Responsive control column
                    className: 'control',
                    orderable: false,
                    data: null,
                    defaultContent: '',
                    responsivePriority: 1
                },
                {
                    className: 'details-control',
                    title: translations.buttons.expandButton,
                    orderable: false,
                    data: null,
                    defaultContent: '',
                    render: function () {
                        return ' <i class="bi bi-arrows-angle-expand action-expand" aria-hidden="true"></i>';
                    },
                    width: "15px",
                    responsivePriority: 2
                },
                { data: "forum", title: translations.tableHeaders.toloka.forum, visible: true },
                { data: "name", type: 'html', title: translations.tableHeaders.toloka.name, render: (data, type, row) => { return this.renderTorrentTitle(data, type, row)}, visible: true },
                { data: "author", title: translations.tableHeaders.toloka.author, visible: true },
                { data: "date", type: 'date',  title: translations.tableHeaders.toloka.date, render: function(data, type, row) { return DataTableManager.customDateRenderer(data, type, row)}, visible: true },
                { data: "answers", title: translations.tableHeaders.toloka.answers, visible: false },
                { data: "forum_url", title: translations.tableHeaders.toloka.forum_url, visible: false },
                { data: "leechers", title: translations.tableHeaders.toloka.leechers, visible: false },
                { data: "seeders", title: translations.tableHeaders.toloka.seeders, visible: false },
                { data: "size", title: translations.tableHeaders.toloka.size, visible: false },
                { data: "status", title: translations.tableHeaders.toloka.status, visible: false },
                { data: "torrent_url", title: translations.tableHeaders.toloka.torrent_url, visible: false },
                { data: "url", title: translations.tableHeaders.toloka.url, render: function(data, type, row) { return DataTableManager.dataTableRenderAsUrl("https://toloka.to/", data, data);}, visible: false },
                { data: "verify", title: translations.tableHeaders.toloka.verify, visible: false },
                { data: null, title: translations.tableHeaders.toloka.actions, orderable: false, render: (data, type, row) =>  { return this.tolokaDataTableRenderActionButtons();}, visible: true }
            ],
            order: [[5, 'des']],
            columnDefs: [
                {
                    searchPanes: {
                        show: true
                    },
                    targets: [2, 4]
                }
            ],
            layout: {
                topStart: DataTableManager.returnDefaultLayout()
            },
            language: DataTableManager.returnDefaultLanguage()
        };
        this.tolokaTable = DataTableManager.initializeDataTable('#torrentTable', config);
        
        this.tolokaTableBody = document.querySelector('#torrentTable tbody');
    }

    renderTorrentTitle(data, type, row)
    {
        if (type === 'sort') {
            return data;
        } else if (type === 'display') 
            {
                return DataTableManager.dataTableRenderAsUrl("https://toloka.to/", row.url, data)
            }
    }

    handleAction(actionName, element) {
        const tr = element.closest('tr');
        const row = this.tolokaTable.row(tr);
        const data = row.data();
        const childData = tr.dataset.childData;

        const actionHandlers = {
          expand: () => this.performDetailsExpandAction(tr),
          download: () => this.performDownloadAction(data, childData),
          copy: () => this.performCopyAction(data, childData),
          add: () => this.performAddAction(data, childData),
        };
    
        const actionFunction = actionHandlers[actionName];
        if (actionFunction) {
          actionFunction();
        } else {
          console.error(`No handler defined for action: ${actionName}`);
        }
      }

    initializeMultiDataTable(query)
    {
        const config = {
            ajax: {
                url: "/api/search?query=" + query,        
                dataSrc: function(json) {
                    if (json.error) {
                        return [];  // Return an empty array to DataTables
                    }
                    var result = json;
                    return result;
                },
                error: function(xhr, error, thrown) {
                    console.log(xhr.responseJSON.error)
                }
            },
            responsive: true,
            columns: [
                { data: 'source', title: translations.tableHeaders.multi.source },
                { data: 'image', title: translations.tableHeaders.multi.image, render: function(data, type, row) {
                    return data ? `<img src="image/?url=${data}" alt="Image" height="100">` : `${translations.labels.noImageAvailable}`;
                }},
                { data: 'title', title: translations.tableHeaders.multi.title },
                { data: 'alternative', title: translations.tableHeaders.multi.alternative },
                {
                    data: 'id',
                    title: translations.tableHeaders.multi.id,
                    type: 'html',
                    render: function(data, type, row) {
                        let url;
                        switch (row.source) {
                            case 'MAL':
                                url = `https://myanimelist.net/anime/${data}`;
                                break;
                            case 'TMDB':
                                if (row.mediaType === 'tv') {
                                    url = `https://www.themoviedb.org/tv/${data}`;
                                } else if (row.mediaType === 'movie') {
                                    url = `https://www.themoviedb.org/movie/${data}`;
                                }
                                break;
                            case 'localdb':
                                url = `/anime/${data}`;
                                break;
                            default:
                                return data; // Return the ID as plain text if no source matches
                        }
                        return DataTableManager.dataTableRenderAsUrl(url,"",data);
                    }
                },
                { data: 'status', title: translations.tableHeaders.multi.status },
                { data: 'mediaType', title: translations.tableHeaders.multi.mediaType},
                { data: 'description', title: translations.tableHeaders.multi.description, visible: false  },
                { data: 'releaseDate', type: 'date', title: translations.tableHeaders.multi.releaseDate },
            ],
            order: [[8, 'des']],
            columnDefs: [
                {
                    searchPanes: {
                        show: true
                    },
                    targets: [0, 2, 5]
                }
            ],
            layout: {
                topStart: DataTableManager.returnDefaultLayout()
            },
            language: DataTableManager.returnDefaultLanguage()
        };
        this.multiTable = DataTableManager.initializeDataTable('#suggested-search', config);
    }

    tolokaDataTableRenderActionButtons(data, type, row) {
        let downloadButton = Utils.renderActionButton("action-download","btn-outline-warning", "", "bi-download", translations.buttons.tolokaDownloadButton);
        let addButton = Utils.renderActionButton("action-add","btn-outline-warning", "", "bi-cloud-download", translations.buttons.tolokaAddButton);
        let copyButton = Utils.renderActionButton("action-copy","btn-outline-primary", "", "bi-chevron-double-left", translations.buttons.tolokaCopyButton);
        return `${downloadButton}
        ${addButton}
        ${copyButton}`;
    }

    initializeStreamDataTable(query)
    {
        const config = {
            ajax: {
                url: "/api/stream?query=" + query,        
                dataSrc: function(json) {
                    if (json.error) {
                        return [];  // Return an empty array to DataTables
                    }
                    var result = json;
                    return result;
                },
                error: function(xhr, error, thrown) {
                    console.log(xhr.responseJSON.error)
                }
            },
            responsive: true,
            columns: [
                {   // Responsive control column
                    className: 'control',
                    orderable: false,
                    data: null,
                    defaultContent: '',
                    responsivePriority: 1
                },
                {
                    className: 'details-control',
                    title: translations.buttons.expandButton,
                    orderable: false,
                    data: null,
                    defaultContent: '',
                    render: function () {
                        return ' <i class="bi bi-arrows-angle-expand" aria-hidden="true"></i>';
                    },
                    width: "15px",
                    responsivePriority: 2
                },
                { data: "provider", title: translations.tableHeaders.stream.provider, visible: true },
                { data: 'image_url', title:  translations.tableHeaders.stream.image_url, render: function(data, type, row) {
                    return data ? `<img src="image/?url=${data}" alt="Image" height="100">` : 'No image available';
                }},
                { data: "title", title:  translations.tableHeaders.stream.title, visible: true },
                { data: "title_eng", title:  translations.tableHeaders.stream.title_eng, visible: true },
                { data: "link", title:  translations.tableHeaders.stream.link, render: function(data, type, row) {
                    return DataTableManager.dataTableRenderAsUrl(data,"",data);
                }, visible: true },
            ],
            order: [[2, 'des']],
            columnDefs: [
                {
                    searchPanes: {
                        show: true
                    },
                    targets: [2, 4]
                }
            ],
            layout: {
                topStart: DataTableManager.returnDefaultLayout()
            },
            language: DataTableManager.returnDefaultLanguage()
        };
        this.streamTable = DataTableManager.initializeDataTable('#tableStream', config);
    }

    addEventListeners()
    {   
        if(this.searchForm)
        {
                this.searchForm.addEventListener('submit', (e) => { this.initiateOffCanvas(e) });
        }
    }

    addDataTablesEvents()
    {
        new EventDelegator('#torrentTable tbody', this.handleAction.bind(this));
    }


    formatDetail(detail, parentData) {
        let fileItems = detail.files.map(file => `
            <li class="list-group-item d-flex justify-content-between align-items-start">
                <div class="ms-2 me-auto">
                    <div class="fw-bold">${file.folder_name}</div>
                    ${file.file_name}
                </div>
                <span class="badge text-bg-primary rounded-pill">${file.size}</span>
            </li>
        `).join('');
    
        return `
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="row g-0">
                            <div class="col-md-2">
                                <img src="image/?url=${detail.img}" class="card-img-top" alt="...">
                                <div class="d-grid gap-2">
                                    <button type="button" class="btn btn-primary position-relative" disabled>
                                        ${detail.size}
                                        <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-success">
                                            ${parentData.leechers}
                                            <span class="visually-hidden">leach</span>
                                        </span>
                                        <span class="position-absolute top-0 start-0 translate-middle badge rounded-pill bg-danger">
                                            ${parentData.seeders}
                                            <span class="visually-hidden">sead</span>
                                        </span>
                                    </button>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card-body">
                                    <h5 class="card-title">${detail.author}</h5>
                                    <p class="card-text">${detail.name}</p>
                                    <p class="card-text">${detail.description}</p>
                                    <p class="card-text"><small class="text-body-secondary">Last updated ${detail.date}</small></p>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <ol class="list-group list-group-numbered">${fileItems}</ol>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    performDetailsExpandAction(tr)
    {
        var row = this.tolokaTable.row(tr);

        if (row.child.isShown()) {
            row.child.hide();
            tr.classList.remove('shown');
        } else {
            var data = row.data();
            row.child(DataTableManager.formatLoading()).show();
            tr.classList.add('shown');

            fetch(`/api/toloka/${data.url}`)
            .then(response => response.json())
            .then(detail => {
                const childData = this.formatDetail(detail, data);
                row.child(childData).show();
                tr.dataset.childData = JSON.stringify(detail);
            });
        }
    }

    performAddAction(rowData, childData) {
        fetch("/api/toloka/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(rowData) 
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

    }
    
    performCopyAction(rowData, childData) {
        Utils.addRelease();
        document.querySelector('#releaseTitle').value = rowData.name;
        document.querySelector('#tolokaUrl').value  = `https://toloka.to/${rowData.url}`;
        if(childData != null)
        {
            childData = JSON.parse(childData);
            var filePath = `${childData.files[0].folder_name}/${childData.files[0].file_name}`
            var input = document.querySelector('#filenameIndex');
            document.querySelector('#filenameIndexGroup').classList.toggle("d-none");
            input.value = filePath
            const event = new Event('input', {
                bubbles: true,
                cancelable: true,
            });
            input.dispatchEvent(event);
        }
        this.searchOffcanvas.hide()
    }
    
    performDownloadAction(rowData, childData) {
        console.log('Download action triggered', rowData, childData);
        var url = `https://toloka.to/${rowData.torrent_url}`

        Utils.downloadFile(url);
    }
}