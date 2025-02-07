import { DataTableManager } from './datatable.js';
import translations from '../l18n/en.js';

export class DataTableFactory {
    static initializeGlobalSettings() {
        // Disable default error alerts
        $.fn.dataTable.ext.errMode = 'none';

        // Handle bootstrap tabs
        document.querySelectorAll('button[data-bs-toggle="tab"]').forEach((el) => {
            el.addEventListener('shown.bs.tab', () => {
                DataTable.tables({ visible: true, api: true }).columns.adjust();
            });
        });
    }

    static formatLoading() {
        return `
            <div class="d-flex justify-content-center">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">${translations.labels.dataTablesLoadingText}</span>
                </div>
            </div>
        `;
    }

    static initializeTable(selector, config) {
        const defaultConfig = {
            responsive: true,
            language: {
                search: "_INPUT_",
                searchPlaceholder: translations.labels.dataTableSearchInput,
                loadingRecords: this.formatLoading()
            }
        };

        // Handle AJAX configuration
        if (config.ajax) {
            if (typeof config.ajax === 'string') {
                config.ajax = {
                    url: config.ajax,
                    dataSrc: (json) => {
                        if (json.error) return [];
                        if (Array.isArray(json)) return json;
                        
                        // Handle object responses
                        const result = [];
                        Object.entries(json).forEach(([key, item]) => {
                            if (typeof item === 'object') {
                                item.codename = key;
                                result.push(item);
                            }
                        });
                        return result;
                    }
                };
            } else if (typeof config.ajax === 'object' && !config.ajax.dataSrc) {
                config.ajax.dataSrc = (json) => {
                    if (json.error) return [];
                    return Array.isArray(json) ? json : [];
                };
            }
        }

        const finalConfig = { ...defaultConfig, ...config };
        return $(selector).DataTable(finalConfig);
    }

    static returnDefaultLayout() {
        return {
            buttons: [
                {
                    extend: 'colvis',
                    postfixButtons: ['colvisRestore'],
                    text: '<i class="bi bi-table"></i>',
                    titleAttr: translations.buttons.dataTableColumnVisibilityhButton
                },
                {
                    extend: 'searchPanes',
                    className: 'btn btn-secondary',
                    config: {
                        cascadePanes: true
                    }
                },
                { 
                    action: (e, dt) => dt.ajax.reload(),
                    text: '<i class="bi bi-arrow-clockwise"></i>',
                    titleAttr: translations.buttons.dataTableRefreshButton
                },
                {
                    extend: 'pageLength',
                    className: 'btn btn-secondary'
                }
            ]
        };
    }

    static createLinkColumn(field, title, baseUrl) {
        return {
            data: field,
            title: title,
            render: (data) => `<a href="${baseUrl}${data}">${data}</a>`,
            visible: true
        };
    }

    static createDateColumn(field, title) {
        return {
            data: field,
            title: title,
            type: 'date',
            render: this.renderDate,
            visible: true
        };
    }

    static createActionColumn(renderFunction) {
        return {
            data: null,
            title: 'Actions',
            orderable: false,
            render: renderFunction,
            visible: true
        };
    }

    static renderDate(data, type) {
        if (!data) return '';

        // Function to parse various date formats
        function parseDate(dateStr) {
            // Handle invalid or malformed dates
            if (!dateStr || dateStr === 'NaN/NaN/NaN' || dateStr.includes('undefined')) {
                return null;
            }

            // Try different date formats
            let parsed = null;

            // Try standard format (YY-MM-DD HH:mm or YY-MM-DD)
            if (dateStr.includes('-')) {
                const [datePart, timePart] = dateStr.split(' ');
                const [year, month, day] = datePart.split('-').map(n => parseInt(n, 10));
                parsed = {
                    year: year < 100 ? 2000 + year : year,
                    month: month || null,
                    day: day || null,
                    time: timePart || null
                };
            }
            // Try NaN/NaN/YYYY format (partial dates)
            else if (dateStr.includes('/')) {
                const parts = dateStr.split('/');
                const yearPart = parts[parts.length - 1];
                // Extract just the year if it's embedded with other numbers
                const yearMatch = yearPart.match(/\d{4}/);
                if (yearMatch) {
                    parsed = {
                        year: parseInt(yearMatch[0], 10),
                        month: parts[1] !== 'NaN' ? parseInt(parts[1], 10) : null,
                        day: parts[0] !== 'NaN' ? parseInt(parts[0], 10) : null,
                        time: null
                    };
                }
            }
            // Try just year format
            else if (/^\d{4}$/.test(dateStr)) {
                parsed = {
                    year: parseInt(dateStr, 10),
                    month: null,
                    day: null,
                    time: null
                };
            }

            return parsed;
        }

        // Function to format the date based on available parts
        function formatDate(dateParts) {
            if (!dateParts) return 'Invalid date';
            
            // If only year is available
            if (!dateParts.month && !dateParts.day) {
                return `${dateParts.year}`;
            }
            
            // If only year and month are available
            if (!dateParts.day) {
                return `${dateParts.month}/${dateParts.year}`;
            }
            
            // Full date
            let formattedDate = `${dateParts.day}/${dateParts.month}/${dateParts.year}`;
            if (dateParts.time && dateParts.time !== '00:00') {
                formattedDate += ` ${dateParts.time}`;
            }
            return formattedDate;
        }

        // Function to calculate time difference
        function timeSince(dateParts) {
            if (!dateParts || !dateParts.year) return '';

            const now = new Date();
            const past = new Date(
                dateParts.year,
                (dateParts.month ? dateParts.month - 1 : 0),
                dateParts.day || 1,
                ...(dateParts.time ? dateParts.time.split(':').map(Number) : [0, 0])
            );

            // If only year is available, just show the year
            if (!dateParts.month) {
                return `${dateParts.year}`;
            }

            const diff = now - past;
            const daysTotal = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const years = Math.floor(daysTotal / 365);
            const days = daysTotal % 365;

            if (years > 0) {
                return `${years} ${translations.labels.dataTablesYearText} ${days} ${translations.labels.dataTablesDaysText} ${hours} ${translations.labels.dataTablesHrsText}`;
            } else {
                return `${days} ${translations.labels.dataTablesDaysText} ${hours} ${translations.labels.dataTablesHrsText}`;
            }
        }

        const parsedDate = parseDate(data);
        if (!parsedDate) return 'Invalid date';

        // Return different data based on the type of data request
        if (type === 'sort') {
            // Return an ISO format date for correct sorting
            const isoDate = `${parsedDate.year}${
                parsedDate.month ? `-${parsedDate.month.toString().padStart(2, '0')}` : '-01'}${
                parsedDate.day ? `-${parsedDate.day.toString().padStart(2, '0')}` : '-01'}`;
            return parsedDate.time ? isoDate + 'T' + parsedDate.time : isoDate;
        } else if (type === 'display') {
            // For display, show relative time only for full dates with time
            if (parsedDate.time && parsedDate.day && parsedDate.month) {
                if (parsedDate.time === '00:00') {
                    return formatDate(parsedDate);
                } else {
                    const since = timeSince(parsedDate);
                    const fullDate = formatDate(parsedDate);
                    return `<span title="${fullDate}">${since}</span>`;
                }
            } else {
                return formatDate(parsedDate);
            }
        }
        // For filtering and type detection, return the formatted date
        return formatDate(parsedDate);
    }
} 