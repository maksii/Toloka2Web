let searchDataTable;

// Listen for Bootstrap tab change
document.querySelectorAll('button[data-bs-toggle="tab"]').forEach((el) => {
    el.addEventListener('shown.bs.tab', () => {
        DataTable.tables({ visible: true, api: true }).columns.adjust();
    });
});

function fetchData(url) {
    return $.ajax({
        url: url,
        dataType: 'json'
    });
}

function loadMultiSearchData(query) {
    return Promise.all([
        fetchData(`/api/mal/search?query=${query}`),
        fetchData(`/api/tmdb/search?query=${query}`),
        fetchData(`/api/anime?query=${query}`)
    ]);
}

function initializeMultiSearchTable(data) {
    searchDataTable = $('#suggested-search').DataTable({
        data: data,
        columns: [
            { data: 'source', title: 'source' },
            { data: 'title', title: 'title' },
            { data: 'id', title: 'id' },
            { data: 'status', title: 'status' },
            { data: 'mediaType', title: 'mediaType' },
            { data: 'image', title: 'image', render: function(data, type, row) {
                return data ? '<img src="'+ data +'" alt="Image" height="100">' : 'No image available';
            }},
            { data: 'description', title: 'description' },
            { data: 'releaseDate', title: 'releaseDate' },
            { data: 'alternative', title: 'alternative' }
        ]
    });
}

function refreshMultiSearchTable(query) {
    document.querySelector('#resultsInMulti').classList.toggle('d-none');
    searchDataTable.clear().draw();
    searchDataTable.destroy();
    $('#suggested-search').empty();
    loadMultiSearchData(query).then(processMultiSearchData).then(initializeMultiSearchTable);
}

function processMultiSearchData(responses) {
    let combinedData = [];

    // Process MAL data
    responses[0].data.forEach(item => {
        let alternatives = item.node.alternative_titles.en + ' | ' + item.node.alternative_titles.ja;
        alternatives += ' | ' + item.node.alternative_titles.synonyms.join(' | ');
        combinedData.push({
            source: 'MAL',
            title: item.node.title,
            id: item.node.id,
            status: item.node.status,
            mediaType: item.node.media_type,
            image: item.node.main_picture.medium,
            description: item.node.title,
            releaseDate: item.node.start_date,
            alternative: alternatives
        });
    });

    // Process TMDB data
    responses[1].results.forEach(item => {
        combinedData.push({
            source: 'TMDB',
            title: item.name || item.title,
            id: item.id,
            status: item.media_type === 'tv' ? 'TV Show' : 'Movie',
            mediaType: item.media_type,
            image: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
            description: item.overview,
            releaseDate: item.first_air_date || item.release_date,
            alternative: item.original_name || ''
        });
    });

    // Process custom API data
    responses[2].forEach(item => {
        combinedData.push({
            source: 'localdb',
            title: item.titleEn,
            id: item.id,
            status: item.status_id === 2 ? 'Currently Airing' : 'Finished Airing',
            mediaType: 'Anime',
            image: '', 
            description: item.description,
            releaseDate: item.releaseDate,
            alternative: item.titleUa
        });
    });

    if (combinedData.length > 0)
        document.querySelector('#resultsInMulti').classList.toggle('d-none');
    
    return combinedData
}

function generateSuggestionsSearch(query)
{
    loadMultiSearchData(query).then(processMultiSearchData).then(initializeMultiSearchTable);
}
