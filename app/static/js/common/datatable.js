// static/js/common/datatable.js
// Note: DataTableFactory (in data-table-factory.js) is the primary class for DataTable operations.
// DataTableManager provides additional utility methods and legacy compatibility.

import { DataTableFactory } from './data-table-factory.js';
import { translations } from './utils.js';

export class DataTableManager {
    /**
     * Initialize a DataTable with given config.
     * @deprecated Use DataTableFactory.initializeTable() instead
     */
    static initializeDataTable(selector, config) {
        return DataTableFactory.initializeTable(selector, config);
    }

    /**
     * Render a value as a clickable URL link.
     */
    static dataTableRenderAsUrl(host, url, text) {
        const fullPath = url ? `${host}/${url}` : host;
        return `<a href="${fullPath}" target="_blank">${text}</a>`;
    }

    /**
     * Render a value as an editable input field.
     */
    static dataTableRenderAsInput(value) {
        return `<input type="text" class="form-control" value="${value || ''}">`;
    }

    /**
     * Refresh/reload a DataTable's AJAX data.
     */
    static refreshTable(table) {
        if (table && typeof table.ajax?.reload === 'function') {
            table.ajax.reload();
        }
    }

    /**
     * Get loading spinner HTML.
     * @deprecated Use DataTableFactory.formatLoading() instead
     */
    static formatLoading() {
        return DataTableFactory.formatLoading();
    }

    /**
     * Disable DataTable's default error alerts.
     * @deprecated Use DataTableFactory.initializeGlobalSettings() instead
     */
    static disableAlertErrors() {
        $.fn.dataTable.ext.errMode = 'none';
    }

    /**
     * Handle Bootstrap tabs to properly adjust columns on tab switch.
     * @deprecated Use DataTableFactory.initializeGlobalSettings() instead
     */
    static handleBootstrapTabs() {
        document.querySelectorAll('button[data-bs-toggle="tab"]').forEach((el) => {
            el.addEventListener('shown.bs.tab', () => {
                DataTable.tables({ visible: true, api: true }).columns.adjust();
            });
        });
    }

    /**
     * Track original data from XHR responses for comparison/editing.
     * @param {DataTable} table - The DataTable instance
     * @param {Object} originalDataStore - Object to store original data by ID
     */
    static onDataTableXhr(table, originalDataStore = {}) {
        table.on('xhr', function() {
            const data = table.ajax.json();
            if (Array.isArray(data)) {
                data.forEach(function(item) {
                    if (item.id !== undefined) {
                        originalDataStore[item.id] = item;
                    }
                });
            }
        });
        return originalDataStore;
    }

    /**
     * Custom date renderer for DataTable columns.
     * @deprecated Use DataTableFactory.renderDate() instead - it handles more date formats
     */
    static customDateRenderer(data, type, row) {
        return DataTableFactory.renderDate(data, type);
    }

    /**
     * Get default layout configuration for DataTable buttons.
     * @deprecated Use DataTableFactory.returnDefaultLayout() instead
     */
    static returnDefaultLayout() {
        return DataTableFactory.returnDefaultLayout();
    }

    /**
     * Get default language configuration for DataTable.
     */
    static returnDefaultLanguage() {
        return {
            search: "_INPUT_",
            searchPlaceholder: translations.labels.dataTableSearchInput,
            loadingRecords: DataTableFactory.formatLoading()
        };
    }
}

export class EventDelegator {
    constructor(selector, actionHandler) {
      this.selector = selector;
      this.actionHandler = actionHandler;
      this.attachListener();
    }
  
    attachListener() {
      const element = document.querySelector(this.selector);
      if (!element) {
        console.error(`Element with selector "${this.selector}" not found.`);
        return;
      }
  
      element.addEventListener('click', (event) => this.handleButtonClick(event));
    }
  
    handleButtonClick(event) {
      let targetElement = event.target;
      while (targetElement && !targetElement.classList.contains('button') && !targetElement.matches("[class*='action-']")) {
        targetElement = targetElement.parentElement;
      }
  
      if (targetElement && targetElement.matches("[class*='action-']")) {
        const actionNameMatch = targetElement.className.match(/action-(\w+)/);
        if (actionNameMatch) {
          const actionName = actionNameMatch[1];
          this.actionHandler(actionName, targetElement);
        }
      }
    }
  }