
    let tableStream;

    function initStreamTable(query){
            // Initialize DataTable
            tableStream = $('#tableStream').DataTable({
                ajax: {
                    url: "/api/stream?query=" + query,        
                    dataSrc: function(json) {
                        if (json.error) {
                            return [];  // Return an empty array to DataTables
                        }
                        var result = json;
                        return result;
                    },
                    error: function(xhr, error, thrown) {
                        console.log(xhr.responseJSON.error)
                    }
                },
                responsive: true,
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
                        title: 'Expand',
                        orderable: false,
                        data: null,
                        defaultContent: '',
                        render: function () {
                            return ' <i class="bi bi-arrows-angle-expand" aria-hidden="true"></i>';
                        },
                        width: "15px",
                        responsivePriority: 2
                    },
                    { data: "title", title: 'Title', visible: true },
                    { data: "title_eng", title: 'title_eng', visible: true },
                    { data: "link", title: 'link', render: function(data, type, row) {
                        return `<a href="${data}" target="_blank">${data}</a>`;
                    }, visible: true },
                    { data: 'image_url', title: 'image_url', render: function(data, type, row) {
                        return data ? `<img src="image/?url=${data}" alt="Image" height="100">` : 'No image available';
                    }},{ data: "provider", title: 'provider', visible: true },
                ],
                order: [[0, 'des']],
                columnDefs: [
                    {
                        searchPanes: {
                            show: true
                        },
                        targets: [1, 3]
                    }
                ],
                layout: {
                    topStart: {
                        buttons: [
                            {
                                extend: 'colvis',
                                postfixButtons: ['colvisRestore'],
                                text: '<i class="bi bi-table"></i>',
                                titleAttr: 'Column Visibility'
                                
                            },
                            {
                                extend: 'searchPanes',
                                config: {
                                    cascadePanes: true
                                }
                            }
                        ]
                    }
                }
            });

        }

    function refreshStream(query)
    {
        tableStream.ajax.url('/api/stream?query=' + query).load(); 
    }    
