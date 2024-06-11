$(document).ready(function() {
    var table = $('#settingsTable').DataTable({
        ajax: {
            url: '/api/settings',
            dataSrc: function(json) {
                var result = [];
                Object.keys(json).forEach(function(key) {
                    var item = json[key];
                    item.codename = key;
                    result.push(item);
                });
                return result;
            }
        },
        responsive: true,
        columns: [
            { data: "id", title: 'ID', visible: true },
            { data: 'section', title: 'Section', visible: true, render: function(data, type, row) {
                if (type === 'display') {
                    return `<input type="text" class="form-control" value="${data}">`;
                }
                return data;
            } },
            { data: 'key', title: 'Key', visible: true, render: function(data, type, row) {
                if (type === 'display') {
                    return `<input type="text" class="form-control" value="${data}">`;
                }
                return data;
            } },
            { data: 'value', title: 'Value', visible: true, render: function(data, type, row) {
                if (type === 'display') {
                    return `<input type="text" class="form-control" value="${data}">`;
                }
                return data;
            } },
            { data: null, defaultContent: `<button class="save btn btn-success">Save</button>` }
        
        ],
        columnDefs: [
            { targets: [0], searchable: false, orderable: false, className: "align-middle" },
            { targets: [1, 2, 3], className: "align-middle" },
            { targets: [4], searchable: false, orderable: false, className: "align-middle text-center" }
        ],
        rowGroup: {
            dataSrc: 'section'
        },
        paging: false,
        order: [[1, 'des']],
        layout: {
            topStart: {
                buttons: [
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
                    }
                ]
            },
            top1End:
            {
                buttons:[
                    {
                        text: 'Add',
                        className: 'btn btn-primary',
                        action: function () {
                            var newRowId = 1;
                            var data = table.data().toArray();
                            if (data.length > 0) {
                                newRowId = Math.max.apply(Math, data.map(function(o) { return o.id; })) + 1;
                            }
                            table.row.add({
                                id: newRowId,
                                section: '',
                                key: '',
                                value: ''
                            }).draw(false);
                    
                            // Focus on the first input of the new row
                            var newRow = table.row(':last').node();
                            $('input:first', newRow).focus();
                        }
                    },
                    {
                        text: 'Sync to app.ini',
                        className: 'btn btn-primary',
                        action: function () {
                            console.log('TBD');
                        }
                    },
                    {
                        text: 'Sync from app.ini',
                        className: 'btn btn-primary',
                        action: function () {
                            console.log('TBD');
                        }
                    }
                ]
            }
        },
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Search records"
        }
    });

    table.on('xhr', function() {
        var data = table.ajax.json();
        originalData = {};
        data.forEach(function(item) {
            originalData[item.id] = item;
        });
    });

    $('#settingsTable tbody').on('click', 'button.save', function() {
        var row = table.row($(this).parents('tr'));
        var rowData = row.data();

        console.log('Saving data', rowData);
    });

    $('#settingsTable tbody').on('click', 'button.reset', function() {
        var row = table.row($(this).parents('tr'));
        var rowData = row.data();
        var originalData = { id: rowData.id, name: rowData.name, age: rowData.age, country: rowData.country }; // Assuming original data can be reconstructed or fetched

        $('input', row.node()).each(function(index) {
            this.value = originalData[$(this).attr('name')];
        });
    });

});


