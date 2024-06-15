$(document).ready(function() {
    var table = $('#settingsTable').DataTable({
        ajax: {
            url: '/api/settings',
            dataSrc: function(json) {
                return json;
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

    $('#settingsTable tbody').on('click', 'button.save', function(event) {
        var row = table.row($(this).parents('tr'));
        var rowData = row.data();

        console.log('Original data', rowData);

        var inputs = $('input', row.node());
        var updatedData = {};
        updatedData.section = inputs[0].value;
        updatedData.key = inputs[1].value;
        updatedData.value = inputs[2].value;

        let target = event.target;
            target.disabled = true;
            target.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';

            let formData = new FormData();
            formData.append('id', rowData.id);
            formData.append('section', updatedData.section);
            formData.append('key', updatedData.key);
            formData.append('value', updatedData.value);
    
            fetch(`/api/settings/${rowData.id}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(detail => {
                target.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Update';
                target.disabled = false;
                table.ajax.reload();
            })
            .catch(error => {
                console.error('Error:', error);
                target.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Update';
                target.disabled = false;
            });
        



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


