// static/js/modules/anime-details.js
import { DataTableFactory } from '../common/data-table-factory.js';
import { ApiService } from '../common/api-service.js';
import translations from '../l18n/en.js';

export default class AnimeDetails {
    constructor() {
        this.relatedAnimeTable = null;
        this.studiosTable = null;
        this.animeId = null;
        this.elements = {
            title: document.querySelector('#animeTitle'),
            description: document.querySelector('#animeDescription'),
            malLink: document.querySelector('#linkMal'),
            imdbLink: document.querySelector('#linkImdb')
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
        try {
            const url = new URL(window.location.href);
            const segments = url.pathname.split('/');
            return segments.pop() || null;
        } catch (error) {
            console.error('Error getting anime ID from URL:', error);
            return null;
        }
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
            this.elements.title.textContent = data.titleEn || 'No title available';
        }

        // Update description
        if (this.elements.description) {
            this.elements.description.textContent = data.description || 'No description available';
        }

        // Update MAL link
        if (this.elements.malLink && data.malId) {
            this.elements.malLink.href = `https://myanimelist.net/anime/${data.malId}`;
        }

        // Update IMDB link
        if (this.elements.imdbLink && data.ashdiId) {
            this.elements.imdbLink.href = `https://www.imdb.com/title/${data.ashdiId}`;
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
                    render: (data) => data ? `<a href="${data}">${data}</a>` : '',
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
}