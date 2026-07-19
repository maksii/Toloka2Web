// static/js/modules/anime-details.js
import { DataTableFactory } from '../common/data-table-factory.js';
import { ApiService } from '../common/api-service.js';
import { Utils, translations } from '../common/utils.js';

export default class AnimeDetails {
    constructor() {
        this.relatedAnimeTable = null;
        this.studiosTable = null;
        this.releasesTable = null;
        this.animeId = null;
        this.elements = {
            title: document.querySelector('#animeTitle'),
            description: document.querySelector('#animeDescription'),
            malLink: document.querySelector('#linkMal'),
            hikkaLink: document.querySelector('#linkHikka')
        };
    }

    async init() {
        this.animeId = this.getAnimeIdFromUrl();
        if (!this.animeId) {
            console.error('No anime ID found in URL');
            return;
        }

        await this.loadAnimeDetails();
        this.initializeTables();
    }

    getAnimeIdFromUrl() {
        return Utils.getIdFromUrl();
    }

    async loadAnimeDetails() {
        try {
            const data = await ApiService.get(`../api/anime/${this.animeId}`);
            if (!data) {
                throw new Error('No data received from API');
            }

            this.updateAnimeDetails(data);
        } catch (error) {
            console.error('Error loading anime details:', error);
            this.showErrorMessage('Failed to load anime details');
        }
    }

    updateAnimeDetails(data) {
        // Update title
        if (this.elements.title) {
            this.elements.title.textContent = data.titleUa || data.titleEn || 'No title available';
        }

        // The catalog has no synopsis — show a compact meta line instead
        if (this.elements.description) {
            const meta = [
                data.titleEn,
                data.releaseDate,
                data.type?.name,
                data.status?.name,
                data.episodes ? `${data.episodes} ep.` : null
            ].filter(Boolean).join(' • ');
            this.elements.description.textContent = meta || 'No details available';
        }

        // Update MAL link - show only if data exists
        if (this.elements.malLink) {
            if (data.malId) {
                this.elements.malLink.href = `https://myanimelist.net/anime/${data.malId}`;
                this.elements.malLink.style.display = '';
            } else {
                this.elements.malLink.style.display = 'none';
            }
        }

        // Update Hikka link - show only if data exists
        if (this.elements.hikkaLink) {
            if (data.hikkaUrl) {
                this.elements.hikkaLink.href = data.hikkaUrl;
                this.elements.hikkaLink.style.display = '';
            } else {
                this.elements.hikkaLink.style.display = 'none';
            }
        }
    }

    showErrorMessage(message) {
        // You can implement this based on your UI requirements
        console.warn(message);
        // Example: Show error in the title element if it exists
        if (this.elements.title) {
            this.elements.title.textContent = message;
            this.elements.title.classList.add('text-danger');
        }
    }

    initializeTables() {
        this.initializeRelatedAnimeTable();
        this.initializeStudiosTable();
        this.initializeReleasesTable();
    }

    initializeRelatedAnimeTable() {
        const config = {
            ajax: `../api/anime/${this.animeId}/related`,
            columns: [
                DataTableFactory.createLinkColumn('id', translations.tableHeaders.anime.id, '/anime/'),
                { data: 'titleUa', title: translations.tableHeaders.anime.titleUa, visible: true },
                { data: 'titleEn', title: translations.tableHeaders.anime.titleEn, visible: true },
                { data: 'season', title: translations.tableHeaders.anime.season, visible: true },
                { data: 'type.name', title: translations.tableHeaders.anime.type, visible: true },
                { data: 'status.name', title: translations.tableHeaders.anime.status, visible: true },
                DataTableFactory.createDateColumn('releaseDate', translations.tableHeaders.anime.releaseDate)
            ],
            order: [[6, 'desc']],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };

        this.relatedAnimeTable = DataTableFactory.initializeTable('#relatedAnimeTable', config);
    }

    initializeStudiosTable() {
        const config = {
            ajax: `../api/anime/${this.animeId}/studios`,
            columns: [
                DataTableFactory.createLinkColumn('id', translations.tableHeaders.studioDetails.id, '/studios/'),
                { data: 'name', title: translations.tableHeaders.studioDetails.name, visible: true },
                {
                    data: 'telegram',
                    title: translations.tableHeaders.studioDetails.telegram,
                    render: (data) => DataTableFactory.safeUrl(data)
                        ? `<a href="${DataTableFactory.escapeHtml(data)}">${DataTableFactory.escapeHtml(data)}</a>`
                        : '',
                    visible: true
                }
            ],
            order: [[0, 'asc']],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };
    
        this.studiosTable = DataTableFactory.initializeTable('#studiosTable', config);
    }

    initializeReleasesTable() {
        const headers = translations.tableHeaders.animeReleases;
        const esc = DataTableFactory.escapeHtml;
        const safeUrl = DataTableFactory.safeUrl;
        const externalLink = (href, text) => {
            const url = safeUrl(href);
            return url ? `<a href="${esc(url)}" target="_blank" rel="noopener">${esc(text)}</a>` : esc(text);
        };
        const config = {
            ajax: `../api/anime/${this.animeId}/releases`,
            columns: [
                {
                    data: 'teams',
                    title: headers.teams,
                    render: (data) => (data || [])
                        .map(team => team.id
                            ? `<a href="/studios/${encodeURIComponent(team.id)}">${esc(team.name || team.id)}</a>`
                            : esc(team.name || ''))
                        .join(', '),
                    visible: true
                },
                { data: 'status', title: headers.status, visible: true },
                { data: 'episodes', title: headers.episodes, visible: true },
                {
                    data: 'dubinfo',
                    title: headers.dub,
                    render: (data) => esc((data || []).join(', ')),
                    visible: true
                },
                {
                    data: 'subinfo',
                    title: headers.sub,
                    render: (data) => esc((data || []).join(', ')),
                    visible: true
                },
                {
                    data: 'torrentLinks',
                    title: headers.links,
                    orderable: false,
                    render: (data, type, row) => {
                        const links = (data || []).map(link => externalLink(link.href, link.text || 'torrent'));
                        if (row.fexlink) links.push(externalLink(row.fexlink, 'FEX'));
                        if (row.sitelink) links.push(externalLink(row.sitelink, 'site'));
                        return links.join(' | ');
                    },
                    visible: true
                }
            ],
            order: [[1, 'asc']],
            layout: {
                topStart: DataTableFactory.returnDefaultLayout()
            }
        };

        this.releasesTable = DataTableFactory.initializeTable('#releasesTable', config);
    }
}