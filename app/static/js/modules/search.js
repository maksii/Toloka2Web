// static/js/modules/search.js
import { DataTableFactory } from '../common/data-table-factory.js';
import { EventDelegator } from '../common/datatable.js';
import { ApiService } from '../common/api-service.js';
import { UiManager } from '../common/ui-manager.js';
import { Utils, translations } from '../common/utils.js';

export default class Search {
    constructor() {
        this.tolokaTable = null;
        this.multiTable = null;
        this.streamTable = null;
        this.searchForm = document.querySelector('#searchForm');
        this.searchOffcanvas = null;
    }

    init() {
        this.addEventListeners();
        // Add offcanvas close event listener
        const searchOffcanvasElement = document.querySelector('#offcanvasTopSearchResults');
        if (searchOffcanvasElement) {
            searchOffcanvasElement.addEventListener('hidden.bs.offcanvas', () => this.clearTables());
        }
    }

    addEventListeners() {
        if (this.searchForm) {
            this.searchForm.addEventListener('submit', (e) => {
                e.preventDefault(); // Prevent form submission
                this.handleSearch();
            });
        }
    }

    async handleSearch() {
        const formData = new FormData(this.searchForm);
        const query = formData.get('query');
        
        document.querySelector("#searchResultsQuery").textContent = query;
        
        // Initialize or clear tables
        if (this.tolokaTable) {
            this.refreshTables(query);
        } else {
            this.initializeTables(query);
            this.addDataTablesEvents();
        }

        // Clear search input and show results
        this.searchForm.reset();
        this.showSearchResults();
    }

    showSearchResults() {
        this.searchOffcanvas = new bootstrap.Offcanvas('#offcanvasTopSearchResults');
        this.searchOffcanvas.show();
    }

    refreshTables(query) {
        this.tolokaTable.ajax.url('/api/toloka?query=' + query).load();
        this.multiTable.ajax.url('/api/search?query=' + query).load();
        this.streamTable.ajax.url('/api/stream?query=' + query).load();
    }

    initializeTables(query) {
        this.initializeTolokaTable(query);
        this.initializeMultiTable(query);
        this.initializeStreamTable(query);
    }

    initializeTolokaTable(query) {
        const config = {
            ajax: `/api/toloka?query=${query}`,
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
                    render: () => '<i class="bi bi-arrows-angle-expand action-expand" aria-hidden="true"></i>',
                    width: "15px",
                    responsivePriority: 2
                },
                { data: "forum", title: translations.tableHeaders.toloka.forum, visible: true },
                { 
                    data: "name", 
                    type: 'html', 
                    title: translations.tableHeaders.toloka.name, 
                    render: (data, type, row) => this.renderTorrentTitle(data, type, row), 
                    visible: true 
                },
                { data: "author", title: translations.tableHeaders.toloka.author, visible: true },
                DataTableFactory.createDateColumn('date', translations.tableHeaders.toloka.date),
                { data: "answers", title: translations.tableHeaders.toloka.answers, visible: false },
                { data: "forum_url", title: translations.tableHeaders.toloka.forum_url, visible: false },
                { data: "leechers", title: translations.tableHeaders.toloka.leechers, visible: false },
                { data: "seeders", title: translations.tableHeaders.toloka.seeders, visible: false },
                { data: "size", title: translations.tableHeaders.toloka.size, visible: false },
                { data: "status", title: translations.tableHeaders.toloka.status, visible: false },
                { data: "torrent_url", title: translations.tableHeaders.toloka.torrent_url, visible: false },
                { data: "url", title: translations.tableHeaders.toloka.url, visible: false },
                { data: "verify", title: translations.tableHeaders.toloka.verify, visible: false },
                DataTableFactory.createActionColumn(() => this.renderTolokaActionButtons())
            ],
            order: [[5, 'desc']],
            columnDefs: [
                {
                    searchPanes: { show: true },
                    targets: [2, 4]
                }
            ],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };

        this.tolokaTable = DataTableFactory.initializeTable('#torrentTable', config);
    }

    initializeMultiTable(query) {
        const config = {
            ajax: `/api/search?query=${query}`,
            columns: [
                { data: 'source', title: translations.tableHeaders.multi.source },
                { 
                    data: 'image', 
                    title: translations.tableHeaders.multi.image,
                    render: (data) => data ? 
                        `<img src="image/?url=${data}" alt="Image" height="100">` : 
                        translations.labels.noImageAvailable
                },
                { data: 'title', title: translations.tableHeaders.multi.title },
                { data: 'alternative', title: translations.tableHeaders.multi.alternative },
                { 
                    data: 'id',
                    title: translations.tableHeaders.multi.id,
                    type: 'html',
                    render: (data, type, row) => this.renderMultiSourceLink(data, row)
                },
                { data: 'status', title: translations.tableHeaders.multi.status },
                { data: 'mediaType', title: translations.tableHeaders.multi.mediaType },
                { data: 'description', title: translations.tableHeaders.multi.description, visible: false },
                DataTableFactory.createDateColumn('releaseDate', translations.tableHeaders.multi.releaseDate)
            ],
            order: [[8, 'desc']],
            columnDefs: [
                {
                    searchPanes: { show: true },
                    targets: [0, 2, 5]
                }
            ],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };

        this.multiTable = DataTableFactory.initializeTable('#suggested-search', config);
    }

    initializeStreamTable(query) {
        const config = {
            ajax: `/api/stream?query=${query}`,
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
                    render: () => '<i class="bi bi-arrows-angle-expand action-expand-stream" aria-hidden="true"></i>',
                    width: "15px",
                    responsivePriority: 2
                },
                { data: "provider", title: translations.tableHeaders.stream.provider, visible: true },
                { 
                    data: 'image_url',
                    title: translations.tableHeaders.stream.image_url,
                    render: (data) => data ? 
                        `<img src="image/?url=${data}" alt="Image" height="100">` : 
                        translations.labels.noImageAvailable
                },
                { data: "title", title: translations.tableHeaders.stream.title, visible: true },
                { data: "title_eng", title: translations.tableHeaders.stream.title_eng, visible: true },
                DataTableFactory.createLinkColumn('link', translations.tableHeaders.stream.link, '')
            ],
            order: [[2, 'desc']],
            columnDefs: [
                {
                    searchPanes: { show: true },
                    targets: [2, 4]
                }
            ],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };

        this.streamTable = DataTableFactory.initializeTable('#tableStream', config);
    }

    addDataTablesEvents() {
        new EventDelegator('#torrentTable tbody', this.handleTolokaAction.bind(this));
        new EventDelegator('#tableStream tbody', this.handleStreamAction.bind(this));
    }

    renderTorrentTitle(data, type, row) {
        if (type === 'sort' || type === 'filter' || type === 'search') {
            return data;
        }
        return type === 'display' ? 
            `<a href="https://toloka.to/${row.url}" target="_blank">${data}</a>` : 
            data;
    }

    renderMultiSourceLink(data, row) {
        const sourceUrls = {
            'MAL': `https://myanimelist.net/anime/${data}`,
            'TMDB': row.mediaType === 'tv' ? 
                `https://www.themoviedb.org/tv/${data}` : 
                `https://www.themoviedb.org/movie/${data}`,
            'localdb': `/anime/${data}`
        };

        const url = sourceUrls[row.source];
        return url ? `<a href="${url}">${data}</a>` : data;
    }

    renderTolokaActionButtons() {
        return `
            ${Utils.renderActionButton("action-download", "btn-outline-warning", "", "bi-download", translations.buttons.tolokaDownloadButton)}
            ${Utils.renderActionButton("action-add", "btn-outline-warning", "", "bi-cloud-download", translations.buttons.tolokaAddButton)}
            ${Utils.renderActionButton("action-copy", "btn-outline-primary", "", "bi-chevron-double-left", translations.buttons.tolokaCopyButton)}
        `;
    }

    handleTolokaAction(actionName, element) {
        const tr = element.closest('tr');
        const row = this.tolokaTable.row(tr);
        const data = row.data();
        const childData = tr.dataset.childData;

        const actions = {
            expand: () => this.expandTolokaDetails(tr),
            download: () => this.downloadTorrent(data),
            copy: () => this.copyToReleaseForm(data, childData, tr),
            add: () => this.addToClient(data),
            show: () => this.toggleRemainingFiles(element)
        };

        const action = actions[actionName];
        if (action) {
            action();
        } else {
            console.error(`No handler defined for action: ${actionName}`);
        }
    }

    handleStreamAction(actionName, element) {
        const tr = element.closest('tr');
        const row = this.streamTable.row(tr);
        const data = row.data();

        const actions = {
            expand: () => this.expandStreamDetails(tr, data)
        };

        const action = actions[actionName];
        if (action) {
            action();
        } else {
            console.error(`No handler defined for action: ${actionName}`);
        }
    }

    async expandTolokaDetails(tr) {
        const row = this.tolokaTable.row(tr);
        
        if (row.child.isShown()) {
            row.child.hide();
            tr.classList.remove('shown');
            return;
        }

        try {
            row.child(DataTableFactory.formatLoading()).show();
            tr.classList.add('shown');

            const data = row.data();
            const detail = await ApiService.get(`/api/toloka/${data.url}`);
            const childData = this.formatTolokaDetail(detail, data);
            
            row.child(childData).show();
            tr.dataset.childData = JSON.stringify(detail);
        } catch (error) {
            console.error('Error expanding torrent details:', error);
            row.child('Error loading details').show();
        }
    }

    async expandStreamDetails(tr, data) {
        const row = this.streamTable.row(tr);
        
        if (row.child.isShown()) {
            row.child.hide();
            tr.classList.remove('shown');
            return;
        }

        try {
            row.child(DataTableFactory.formatLoading()).show();
            tr.classList.add('shown');

            const detail = await ApiService.post('/api/stream/details', data);
            const childData = this.formatStreamDetail(detail, data);
            
            row.child(childData).show();
            tr.dataset.childData = JSON.stringify(detail);
        } catch (error) {
            console.error('Error expanding stream details:', error);
            row.child('Error loading details').show();
        }
    }

    async addToClient(data) {
        try {
            await ApiService.post("/api/toloka/", data);
        } catch (error) {
            console.error('Error adding to client:', error);
        }
    }

    downloadTorrent(data) {
        Utils.downloadFile(`https://toloka.to/${data.torrent_url}`);
    }

    async copyToReleaseForm(data, childData, tr) {
        const handleCopy = (childDataToUse) => {
            Utils.addRelease();
            
            // Set the title and URL
            document.querySelector('#releaseTitle').value = data.name;
            document.querySelector('#tolokaUrl').value = `https://toloka.to/${data.url}`;
            // Set release group from Toloka search author
            const releaseGroupInput = document.querySelector('#releaseGroup');
            if (releaseGroupInput) releaseGroupInput.value = data.author != null ? data.author : '';
            
            // Handle file name extraction from child data
            if (childDataToUse) {
                try {
                    const parsedData = typeof childDataToUse === 'string' ? JSON.parse(childDataToUse) : childDataToUse;
                    if (parsedData.files && parsedData.files.length > 0) {
                        const file = parsedData.files[0];
                        const filePath = file.folder_name ? `${file.folder_name}/${file.file_name}` : file.file_name;
                        
                        // Show the filename index group and set the value
                        const indexGroup = document.querySelector('#filenameIndexGroup');
                        const input = document.querySelector('#filenameIndex');
                        
                        indexGroup.classList.remove('d-none');
                        input.value = filePath;
                        
                        // Trigger the input event to process the filename
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                } catch (error) {
                    console.error('Error parsing child data:', error);
                }
            }
            
            // Hide the search results
            this.searchOffcanvas.hide();
        };

        // If we don't have child data yet, expand the details first
        if (!childData) {
            const copyButton = tr.querySelector('.action-copy');
            UiManager.setButtonLoading(copyButton);

            await this.expandTolokaDetails(tr);

            // Wait for child data to be available
            const checkInterval = setInterval(() => {
                if (tr.dataset.childData) {
                    clearInterval(checkInterval);
                    UiManager.resetButton(copyButton);
                    handleCopy(tr.dataset.childData); // Pass the child data from dataset
                }
            }, 100);
        } else {
            handleCopy(childData);
        }
    }

    formatTolokaDetail(detail, parentData) {
        const generateFileItem = (file) => `
            <li class="list-group-item d-flex justify-content-between align-items-start">
                <div class="ms-2 me-auto">
                    <div class="fw-bold">${file.folder_name}</div>
                    ${file.file_name}
                </div>
                <span class="badge text-bg-primary rounded-pill">${file.size}</span>
            </li>
        `;

        const initialFiles = detail.files.slice(0, 4).map(generateFileItem).join('');
        const remainingFiles = detail.files.length > 4 ? 
            detail.files.slice(4).map(generateFileItem).join('') : '';

        // Format the date to match parent table format
        const dateParts = detail.date.split(' ')[0].split('-');
        const timeParts = detail.date.split(' ')[1].split(':');
        const date = new Date(
            parseInt('20' + dateParts[2]), // Year
            parseInt(dateParts[1]) - 1,    // Month (0-based)
            parseInt(dateParts[0]),        // Day
            parseInt(timeParts[0]),        // Hours
            parseInt(timeParts[1])         // Minutes
        );
        const formattedDate = date.toLocaleDateString('en-GB') + ' ' + date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });

        const showMoreButton = detail.files.length > 4 ? `
            <div class="text-center mt-2">
                <button class="btn btn-sm btn-outline-primary action-show" type="button" data-show-more="false">
                    <i class="bi bi-chevron-down"></i> Show More (${detail.files.length - 4} more files)
                </button>
            </div>` : '';

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
                                            <span class="visually-hidden">seed</span>
                                        </span>
                                    </button>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card-body">
                                    <h5 class="card-title">${detail.author}</h5>
                                    <p class="card-text">${detail.name}</p>
                                    <p class="card-text">${detail.description}</p>
                                    <p class="card-text"><small class="text-body-secondary">${formattedDate}</small></p>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <ol class="list-group list-group-numbered">
                                    ${initialFiles}
                                    <div class="remaining-files" style="display: none;">
                                        ${remainingFiles}
                                    </div>
                                </ol>
                                ${showMoreButton}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    formatStreamDetail(detail, parentData) {
        return `
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="row g-0">
                            <div class="col-md-2">
                                <img src="image/?url=${parentData.image_url}" class="card-img-top" alt="...">
                            </div>
                            <div class="col-md-4">
                                <div class="card-body">
                                    <h5 class="card-title">${parentData.title}</h5>
                                    <p class="card-text">${parentData.title_eng}</p>
                                    <p class="card-text">${parentData.description}</p>
                                    <p class="card-text"><small class="text-body-secondary">${parentData.provider}</small></p>
                                </div>
                            </div>
                            <div class="col-md-6">
                                ${this.generateSeriesExpandHTML(detail)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    groupByStudio(data) {
        return data.reduce((acc, item) => {
            if (!acc[item.studio_id]) {
                acc[item.studio_id] = {
                    studio_name: item.studio_name,
                    series: {}
                };
            }
            if (!acc[item.studio_id].series[item.series]) {
                acc[item.studio_id].series[item.series] = [];
            }
            acc[item.studio_id].series[item.series].push(item);
            return acc;
        }, {});
    }

    generateSeriesExpandHTML(data) {
        const groupedData = this.groupByStudio(data);
        return Object.entries(groupedData).map(([studioId, studio], idx) => `
            <div class="accordion" id="accordionStudio${idx}">
                <div class="accordion-item">
                    <h2 class="accordion-header" id="heading${idx}">
                        <button class="accordion-button" type="button" data-bs-toggle="collapse" 
                                data-bs-target="#collapse${idx}" aria-expanded="true" 
                                aria-controls="collapse${idx}">
                            ${studio.studio_name}
                        </button>
                    </h2>
                    <div id="collapse${idx}" class="accordion-collapse collapse show" 
                         aria-labelledby="heading${idx}" data-bs-parent="#accordionStudio${idx}">
                        <div class="accordion-body">
                            ${this.generateSeriesHTML(studio.series, idx)}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    generateSeriesHTML(series, studioIdx) {
        return `
            <div class="accordion" id="accordionSeries${studioIdx}">
                ${Object.entries(series).map(([seriesName, items], idx) => `
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="seriesHeading${studioIdx}_${idx}">
                            <button class="accordion-button collapsed" type="button" 
                                    data-bs-toggle="collapse" 
                                    data-bs-target="#seriesCollapse${studioIdx}_${idx}" 
                                    aria-expanded="false" 
                                    aria-controls="seriesCollapse${studioIdx}_${idx}">
                                ${seriesName}
                            </button>
                        </h2>
                        <div id="seriesCollapse${studioIdx}_${idx}" 
                             class="accordion-collapse collapse" 
                             aria-labelledby="seriesHeading${studioIdx}_${idx}" 
                             data-bs-parent="#accordionSeries${studioIdx}">
                            <div class="accordion-body">
                                ${items.map(item => 
                                    `<a href="${item.url}" target="_blank">${item.url}</a><br>`
                                ).join('')}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    toggleRemainingFiles(button) {
        const isShowing = button.dataset.showMore === 'true';
        const remainingFiles = button.closest('.col-md-6').querySelector('.remaining-files');
        
        if (isShowing) {
            remainingFiles.style.display = 'none';
            button.innerHTML = `<i class="bi bi-chevron-down"></i> Show More (${remainingFiles.children.length} more files)`;
            button.dataset.showMore = 'false';
        } else {
            remainingFiles.style.display = 'block';
            button.innerHTML = `<i class="bi bi-chevron-up"></i> Show Less`;
            button.dataset.showMore = 'true';
        }
    }

    clearTables() {
        if (this.tolokaTable) {
            this.tolokaTable.clear().draw();
        }
        if (this.multiTable) {
            this.multiTable.clear().draw();
        }
        if (this.streamTable) {
            this.streamTable.clear().draw();
        }
    }
}