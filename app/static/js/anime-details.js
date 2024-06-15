$(document).ready(function() {
    const url = new URL(window.location.href);
    const segments = url.pathname.split('/');
    const animeId = segments.pop();

    // Fetch and display anime details
    $.getJSON(`../api/anime/${animeId}`, function(data) {
        $('#animeTitle').text(data.titleEn);
        $('#animeDescription').text(data.description);
        $('#linkMal').attr('href', `https://myanimelist.net/anime/${data.malId}`);
        $('#linkImdb').attr('href', `https://www.imdb.com/title/${data.ashdiId}`);
        // Additional links can be updated here
    });


    var table = $('#relatedAnimeTable').DataTable({
        ajax: {
            url:  `../api/anime/${animeId}/related`,
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
            { data: "id", title: 'ID', render: function(data, type, row) {
                return `<a href="/anime/${data}">${data}</a>`;
            }, visible: true },
            { data: 'titleUa', title: 'UA', visible: true },
            { data: 'titleEn', title: 'EN', visible: true },
            { data: 'season', title: 'Season', visible: true },
            { data: 'type.name', title: 'Type', visible: true },
            { data: 'status.name', title: 'Status', visible: true },
            { data: 'releaseDate', title: 'releaseDate', visible: true },
        ],
        order: [[6, 'des']],
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
                        className: 'btn btn-secondary',
                        config: {
                            cascadePanes: true
                        }
                        
                    },
                    { 
                        action: function ( e, dt, node, config ) {dt.ajax.reload();},                        
                        text: '<i class="bi bi-arrow-clockwise"></i>',
                        titleAttr: 'Refresh'
                    },
                    {
                        extend: 'pageLength',
                        className: 'btn btn-secondary'
                    }
                ]
            }
        },
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Search records"
        }
    });

    var table = $('#studiosTable').DataTable({
        ajax: {
            url:  `../api/anime/${animeId}/studios`,
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
            { data: "id", title: 'ID', render: function(data, type, row) {
                return `<a href="/studios/${data}">${data}</a>`;
            }, visible: true },
            { data: 'name', title: 'Name', visible: true },
            { data: "telegram", title: 'telegram', render: function(data, type, row) {
                return `<a href="${data}">${data}</a>`;
            }, visible: true },
        ],
        order: [[3, 'des']],
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
                        className: 'btn btn-secondary',
                        config: {
                            cascadePanes: true
                        }
                        
                    },
                    { 
                        action: function ( e, dt, node, config ) {dt.ajax.reload();},                        
                        text: '<i class="bi bi-arrow-clockwise"></i>',
                        titleAttr: 'Refresh'
                    },
                    {
                        extend: 'pageLength',
                        className: 'btn btn-secondary'
                    }
                ]
            }
        },
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Search records"
        }
    });


});


