// static/js/common/datatable.js
export class DataTableManager {
    static initializeDataTable(selector, config) {
        return $(selector).DataTable(config);
    }

    static dataTableRenderAsUrl(host, url, text) {
        return `<a href="${host}/${url}">${text}</a>`;
    }

    static refreshTable(table) {
        table.ajax.reload();
    }

    static formatLoading() {
        return '<div class="d-flex justify-content-center">' +
               '<div class="spinner-border" role="status">' +
               '<span class="visually-hidden">Loading...</span>' +
               '</div>' +
               '</div>';
    }

    static disableAlertErrors()
    {
        $.fn.dataTable.ext.errMode = 'none';
    }

    static handleBootstrapTabs()
    {
        document.querySelectorAll('button[data-bs-toggle="tab"]').forEach((el) => {
            el.addEventListener('shown.bs.tab', () => {
                DataTable.tables({ visible: true, api: true }).columns.adjust();
            });
        });
    }

    static onDataTableXhr(table)
    {
        table.on('xhr', function() {
            var data = table.ajax.json();
            originalData = {};
            data.forEach(function(item) {
                originalData[item.id] = item;
            });
        });
    }

}