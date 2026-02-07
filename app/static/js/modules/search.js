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
            ajax: {
                url: `/api/toloka?query=${query}`,
                dataSrc: (json) => {
                    if (json && json.error) {
                        const message = json.message || 'Please repeat the search.';
                        UiManager.showToast(
                            translations.labels?.tolokaSearchErrorTitle ?? 'Toloka search',
                            message
                        );
                        return [];
                    }
                    if (Array.isArray(json)) return json;
                    if (json && Array.isArray(json.results)) return json.results;
                    if (json && Array.isArray(json.data)) return json.data;
                    return [];
                }
            },
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
                    render: () => Utils.renderActionButton(
                        "action-expand",
                        "btn-outline-secondary btn-sm",
                        "",
                        "bi-arrows-angle-expand",
                        translations.buttons.expandButton
                    ),
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
        this.tolokaTable.on('draw', () => {
            Utils.activeTooltips();
        });
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
        this.multiTable.on('draw', () => {
            Utils.activeTooltips();
        });
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
                    render: () => Utils.renderActionButton(
                        "action-expand-stream",
                        "btn-outline-secondary btn-sm",
                        "",
                        "bi-arrows-angle-expand",
                        translations.buttons.expandButton
                    ),
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
                {
                    data: 'link',
                    title: translations.tableHeaders.stream.link,
                    render: (data) => data ? `<a href="${this.normalizeUrl(data)}" target="_blank" rel="noopener">${this.normalizeUrl(data)}</a>` : '',
                    visible: true
                }
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
        this.streamTable.on('draw', () => {
            Utils.activeTooltips();
        });
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
            Utils.activeTooltips();
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
            Utils.activeTooltips();
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
                <button class="btn btn-sm btn-outline-primary action-show btn-wide" type="button" data-show-more="false" data-bs-toggle="tooltip" data-bs-title="${translations.labels.showMoreFiles}" title="${translations.labels.showMoreFiles}" aria-label="${translations.labels.showMoreFiles}">
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
                                    <button type="button" class="btn btn-primary position-relative btn-wide" disabled>
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

    /**
     * Format description text for Stream expand: linkify URLs and optional markdown.
     * @param {string} text - Raw description
     * @returns {string} Safe HTML
     */
    formatStreamDescription(text) {
        if (!text) return '';
        // Turn raw URLs into markdown links so they render as clickable
        const linkified = String(text).replace(
            /(https?:\/\/[^\s)\]'"]+)/g,
            '[$1]($1)'
        );
        if (typeof marked !== 'undefined' && typeof DOMPurify !== 'undefined') {
            const html = marked.parse(linkified);
            return DOMPurify.sanitize(html, { ADD_ATTR: ['target', 'rel'] });
        }
        // Fallback: plain linkify
        return linkified.replace(
            /(https?:\/\/[^\s)\]'"]+)/g,
            '<a href="$1" target="_blank" rel="noopener">$1</a>'
        );
    }

    /**
     * Build optional metadata HTML for Stream expand (year, rating, type, etc.) when available.
     * @param {Object} parentData - Row data from stream search
     * @param {Object} detail - Response from stream/details
     * @returns {string} HTML fragment or empty string
     */
    formatStreamMetadata(parentData, detail) {
        const meta = [];
        const add = (label, value) => {
            if (value != null && value !== '') meta.push({ label, value });
        };
        add(translations.tableHeaders?.multi?.releaseDate || 'Year', parentData.year ?? parentData.releaseDate ?? detail?.year);
        add(translations.labels?.rating || 'Rating', parentData.rating ?? detail?.rating);
        add(translations.tableHeaders?.anime?.type || 'Type', parentData.type ?? detail?.type);
        add(translations.tableHeaders?.multi?.status || 'Status', parentData.status ?? detail?.status);
        if (!meta.length) return '';
        return `
            <ul class="list-unstyled small text-body-secondary mb-2">
                ${meta.map(({ label, value }) => `<li><strong>${label}:</strong> ${value}</li>`).join('')}
            </ul>
        `;
    }

    /**
     * Generate a safe, unique HTML id prefix for one expanded stream row (so accordions don't clash).
     * @param {Object} parentData - Row data (provider, link, title, etc.)
     * @returns {string} Safe string for use in id attributes
     */
    getStreamRowId(parentData) {
        const provider = (parentData.provider || 'p').replace(/[^a-zA-Z0-9]/g, '');
        const link = parentData.link || parentData.url || '';
        let hash = 0;
        for (let i = 0; i < link.length; i++) {
            hash = ((hash << 5) - hash) + link.charCodeAt(i) | 0;
        }
        const linkPart = (hash >>> 0).toString(36);
        return `stream_${provider}_${linkPart}`.slice(0, 60);
    }

    formatStreamDetail(detail, parentData) {
        const descriptionHtml = this.formatStreamDescription(parentData.description || '');
        const metadataHtml = this.formatStreamMetadata(parentData, detail);
        const rowId = this.getStreamRowId(parentData);
        return `
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="row g-0">
                            <div class="col-md-2">
                                <img src="image/?url=${parentData.image_url || ''}" class="card-img-top" alt="">
                            </div>
                            <div class="col-md-4">
                                <div class="card-body">
                                    <h5 class="card-title">${parentData.title || ''}</h5>
                                    <p class="card-text">${parentData.title_eng || ''}</p>
                                    ${metadataHtml}
                                    <div class="card-text stream-description">${descriptionHtml}</div>
                                    <p class="card-text mt-2"><small class="text-body-secondary">${parentData.provider || ''}</small></p>
                                </div>
                            </div>
                            <div class="col-md-6">
                                ${this.generateSeriesExpandHTML(detail, rowId)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Group episodes by series name within a studio's episodes array.
     * Handles various formats: array of episodes, array of URLs, or mixed.
     * @param {Array} episodes - Array of episode objects or URLs
     * @returns {Object} Object with series names as keys and arrays of episodes as values
     */
    groupEpisodesBySeries(episodes) {
        if (!Array.isArray(episodes)) {
            console.log('[Stream Details] groupEpisodesBySeries: not an array:', episodes);
            return {};
        }

        console.log('[Stream Details] groupEpisodesBySeries input:', episodes);

        return episodes.reduce((acc, ep, idx) => {
            // Handle case where episode is just a string (URL)
            if (typeof ep === 'string') {
                const seriesName = translations.labels?.episode || 'Episode';
                if (!acc[seriesName]) {
                    acc[seriesName] = [];
                }
                acc[seriesName].push({
                    series: `${seriesName} ${idx + 1}`,
                    url: ep
                });
                return acc;
            }

            // Normal object case
            const seriesName = ep.series || ep.name || ep.title || `${translations.labels?.episode || 'Episode'} ${idx + 1}`;
            if (!acc[seriesName]) {
                acc[seriesName] = [];
            }
            acc[seriesName].push(ep);
            return acc;
        }, {});
    }

    /**
     * Normalize the API response to a consistent array of studio groups format.
     * Handles various response structures from different providers.
     * @param {any} data - Raw API response
     * @returns {Array} Normalized array of studio groups
     */
    normalizeStreamResponse(data) {
        console.log('[Stream Details] Normalizing response, input type:', typeof data);

        // If already an array of groups with episodes, return as-is
        if (Array.isArray(data)) {
            // Check if it's an array of groups (has studio_name/studio_id and episodes)
            if (data.length > 0 && (data[0].episodes || data[0].studio_name || data[0].studio_id)) {
                console.log('[Stream Details] Response is already in group format');
                return data;
            }
            // It might be a flat array of episodes - wrap in a single group
            console.log('[Stream Details] Response is flat array, wrapping in group');
            return [{
                studio_id: 0,
                studio_name: translations.labels?.episodes || 'Episodes',
                episodes: data
            }];
        }

        // If it's an object, try to extract the data
        if (data && typeof data === 'object') {
            // Check for common wrapper properties
            const possibleArrayProps = ['groups', 'studios', 'data', 'episodes', 'series', 'items', 'results'];
            for (const prop of possibleArrayProps) {
                if (Array.isArray(data[prop])) {
                    console.log(`[Stream Details] Found array in property '${prop}'`);
                    return this.normalizeStreamResponse(data[prop]);
                }
            }

            // Check if it's an object with studio names as keys
            // e.g., { "UAFlix": [...], "UAFlix Сезон 2": [...] }
            const keys = Object.keys(data);
            if (keys.length > 0 && !keys.includes('error')) {
                const firstValue = data[keys[0]];
                if (Array.isArray(firstValue)) {
                    console.log('[Stream Details] Response is object with studio keys, converting to groups');
                    return keys.map((key, idx) => ({
                        studio_id: idx,
                        studio_name: key,
                        episodes: data[key]
                    }));
                }
            }
        }

        console.log('[Stream Details] Could not normalize response, returning empty array');
        return [];
    }

    /**
     * Generate HTML for stream details accordion.
     * Handles the new grouped response format where data is an array of studio groups.
     * Each group: { studio_id, studio_name, episodes: [...] }
     * @param {any} data - Response from API (will be normalized)
     * @param {string} rowId - Unique prefix for this expanded row (from getStreamRowId) so IDs don't clash
     * @returns {string} HTML string for the accordion
     */
    generateSeriesExpandHTML(data, rowId) {
        const prefix = rowId || 'stream';
        const normalizedData = this.normalizeStreamResponse(data);

        console.log('[Stream Details] Normalized data:', normalizedData);

        if (!Array.isArray(normalizedData) || normalizedData.length === 0) {
            return `<div class="alert alert-info">${translations.labels?.noEpisodesFound || 'No episodes found'}</div>`;
        }

        return normalizedData.map((group, idx) => {
            const studioPrefix = `${prefix}_st${idx}`;
            const seriesByName = this.groupEpisodesBySeries(group.episodes || []);
            const episodeCount = (group.episodes || []).length;
            const studioName = group.studio_name || `${translations.labels?.studio || 'Studio'} ${group.studio_id || idx + 1}`;

            return `
            <div class="accordion mb-2" id="accordionStudio_${studioPrefix}">
                <div class="accordion-item">
                    <h2 class="accordion-header" id="heading_${studioPrefix}">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" 
                                data-bs-target="#collapse_${studioPrefix}" aria-expanded="false" 
                                aria-controls="collapse_${studioPrefix}">
                            <span class="me-2">${studioName}</span>
                            <span class="badge bg-secondary">${episodeCount} ${translations.labels?.episodes || 'episodes'}</span>
                        </button>
                    </h2>
                    <div id="collapse_${studioPrefix}" class="accordion-collapse collapse" 
                         aria-labelledby="heading_${studioPrefix}" data-bs-parent="#accordionStudio_${studioPrefix}">
                        <div class="accordion-body">
                            ${this.generateSeriesHTML(seriesByName, studioPrefix)}
                        </div>
                    </div>
                </div>
            </div>
        `;
        }).join('');
    }

    generateSeriesHTML(series, studioPrefix) {
        const seriesEntries = Object.entries(series);

        if (seriesEntries.length === 1) {
            const [seriesName, items] = seriesEntries[0];
            return `
                <div class="series-episodes">
                    <h6 class="mb-3">${seriesName}</h6>
                    ${this.generateEpisodesList(items)}
                </div>
            `;
        }

        return `
            <div class="accordion" id="accordionSeries_${studioPrefix}">
                ${seriesEntries.map(([seriesName, items], idx) => {
            const seriesId = `${studioPrefix}_s${idx}`;
            return `
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="seriesHeading_${seriesId}">
                            <button class="accordion-button collapsed" type="button" 
                                    data-bs-toggle="collapse" 
                                    data-bs-target="#seriesCollapse_${seriesId}" 
                                    aria-expanded="false" 
                                    aria-controls="seriesCollapse_${seriesId}">
                                <span class="me-2">${seriesName}</span>
                                <span class="badge bg-primary">${items.length}</span>
                            </button>
                        </h2>
                        <div id="seriesCollapse_${seriesId}" 
                             class="accordion-collapse collapse" 
                             aria-labelledby="seriesHeading_${seriesId}" 
                             data-bs-parent="#accordionSeries_${studioPrefix}">
                            <div class="accordion-body">
                                ${this.generateEpisodesList(items)}
                            </div>
                        </div>
                    </div>
                `;
        }).join('')}
            </div>
        `;
    }

    /**
     * Normalize URL to fix common issues like duplicate protocols and transform API URLs.
     * @param {string} url - The URL to normalize
     * @returns {string} Normalized URL
     */
    normalizeUrl(url) {
        if (!url) return '#';

        // Remove duplicate protocols (e.g., "https:https://..." -> "https://...")
        let normalized = url.replace(/^(https?:)+(https?:\/\/)/, '$2');

        // Also handle cases like "https:http://..." 
        normalized = normalized.replace(/^https?:(https?:\/\/)/, '$1');

        // Ensure URL starts with a protocol
        if (!normalized.startsWith('http://') && !normalized.startsWith('https://')) {
            // If it starts with "//", add https:
            if (normalized.startsWith('//')) {
                normalized = 'https:' + normalized;
            } else if (!normalized.startsWith('#')) {
                // Assume https for bare domains
                normalized = 'https://' + normalized;
            }
        }

        // Transform animeon.club API URLs to user-facing URLs
        // e.g., https://animeon.club/api/anime/176 -> https://animeon.club/anime/176
        normalized = normalized.replace(/animeon\.club\/api\//, 'animeon.club/');

        return normalized;
    }

    /**
     * Extract provider name from URL for display purposes.
     * @param {string} url - The URL to extract provider from
     * @returns {string} Provider name or empty string
     */
    extractProviderFromUrl(url) {
        if (!url) return '';

        try {
            const hostname = new URL(url).hostname.toLowerCase();

            // Map hostnames to friendly provider names
            const providerMap = {
                'animeon.club': 'AnimeON',
                'uakino.club': 'UAKino',
                'uakino.me': 'UAKino',
                'ashdi.vip': 'Ashdi',
                'uaflix.net': 'UAFlix',
                'uaserials.pro': 'UASerials',
                'uafilms.tv': 'UAFilms',
                'eneyida.tv': 'Eneyida'
            };

            // Check for exact match first
            if (providerMap[hostname]) {
                return providerMap[hostname];
            }

            // Check for partial matches
            for (const [domain, name] of Object.entries(providerMap)) {
                if (hostname.includes(domain.split('.')[0])) {
                    return name;
                }
            }

            // Return hostname without www and TLD as fallback
            return hostname.replace(/^www\./, '').split('.')[0];
        } catch {
            return '';
        }
    }

    /**
     * Generate HTML for a list of episodes within a series.
     * Handles both old format (episode.url) and new format (episode.urls array).
     * @param {Array} episodes - Array of episode objects
     * @returns {string} HTML string for the episodes list
     */
    generateEpisodesList(episodes) {
        console.log('[Stream Details] generateEpisodesList input:', episodes);

        if (!episodes || episodes.length === 0) {
            return `<div class="text-muted">${translations.labels?.noEpisodesAvailable || 'No episodes available'}</div>`;
        }

        return `
            <div class="list-group list-group-flush">
                ${episodes.map((ep, idx) => {
            const episodeTitle = ep.title || ep.name || ep.series || `${translations.labels?.episode || 'Episode'} ${idx + 1}`;

            // Handle new format: series has urls array
            if (ep.urls && Array.isArray(ep.urls) && ep.urls.length > 0) {
                return this.generateMultiUrlEpisode(episodeTitle, ep.urls, ep.provider);
            }

            // Handle old format: single url
            const provider = ep.provider || this.extractProviderFromUrl(ep.url);
            const providerBadge = provider ? `<span class="badge bg-info text-dark">${provider}</span>` : '';
            const normalizedUrl = this.normalizeUrl(ep.url);

            return `
                        <a href="${normalizedUrl}" target="_blank" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                            <span>${episodeTitle}</span>
                            <span>
                                ${providerBadge}
                                <i class="bi bi-box-arrow-up-right ms-2"></i>
                            </span>
                        </a>
                    `;
        }).join('')}
            </div>
        `;
    }

    /**
     * Generate HTML for an episode with multiple URL options.
     * @param {string} title - Episode title
     * @param {Array} urls - Array of URL strings
     * @param {string} defaultProvider - Default provider name if any
     * @returns {string} HTML string for the episode with multiple links
     */
    generateMultiUrlEpisode(title, urls, defaultProvider) {
        const urlLinks = urls.map(url => {
            const normalizedUrl = this.normalizeUrl(url);
            const provider = this.extractProviderFromUrl(normalizedUrl) || defaultProvider || '';
            const providerBadge = provider ? `<span class="badge bg-info text-dark me-1">${provider}</span>` : '';

            return `<a href="${normalizedUrl}" target="_blank" class="btn btn-sm btn-outline-primary me-1 mb-1" title="${normalizedUrl}">
                ${providerBadge}<i class="bi bi-box-arrow-up-right"></i>
            </a>`;
        }).join('');

        return `
            <div class="list-group-item d-flex justify-content-between align-items-center flex-wrap">
                <span class="me-2 mb-1">${title}</span>
                <div class="episode-urls">
                    ${urlLinks}
                </div>
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
            button.setAttribute('data-bs-title', translations.labels.showMoreFiles);
            button.setAttribute('title', translations.labels.showMoreFiles);
            button.setAttribute('aria-label', translations.labels.showMoreFiles);
        } else {
            remainingFiles.style.display = 'block';
            button.innerHTML = `<i class="bi bi-chevron-up"></i> Show Less`;
            button.dataset.showMore = 'true';
            button.setAttribute('data-bs-title', translations.labels.showLessFiles);
            button.setAttribute('title', translations.labels.showLessFiles);
            button.setAttribute('aria-label', translations.labels.showLessFiles);
        }
        Utils.activeTooltips();
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
