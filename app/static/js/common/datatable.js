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
}