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
            {
                data: 'id',
                title: 'ID',
                render: function(data, type, row) {
                    let url;
                    switch (row.source) {
                        case 'MAL':
                            url = `https://myanimelist.net/anime/${data}`;
                            break;
                        case 'TMDB':
                            if (row.mediaType === 'tv') {
                                url = `https://www.themoviedb.org/tv/${data}`;
                            } else if (row.mediaType === 'movie') {
                                url = `https://www.themoviedb.org/movie/${data}`;
                            }
                            break;
                        case 'localdb':
                            url = `/anime/${data}`;
                            break;
                        default:
                            return data; // Return the ID as plain text if no source matches
                    }
                    return `<a href="${url}" target="_blank">${data}</a>`;
                }
            },
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
    let slice = 4;
    let tmdbPromises = [];
    // Process MAL data
    // Check if the first response contains an error
    if (responses[0].error || responses[0].status_code) {
        console.error("Error from MAL API:", responses[0].message || responses[0].status_message);
    } else {
    responses[0].data.slice(0, slice).forEach(item => {
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
    }
    
    if (responses[1].error || responses[1].status_code) {
        console.error("Error from TMDB API:", responses[1].message || responses[1].status_message);
    } else {
    // Process TMDB data
    responses[1].results.slice(0, 4).forEach(item => {
        tmdbPromises.push(
            fetch(`/api/tmdb/detail/${item.id}?type=${item.media_type}`)
            .then(response => response.json())
            .then(details => {
                const relevantCountries = ['JP', 'US', 'UA', 'UK'];
                // First, determine the source array to use: either results or titles
                const sourceArray = details && details.alternative_titles
                    ? (Array.isArray(details.alternative_titles.results) ? details.alternative_titles.results
                        : Array.isArray(details.alternative_titles.titles) ? details.alternative_titles.titles
                        : null)
                    : null;

                // Now process the source array if it's not null
                const alternativeTitles = sourceArray
                    ? sourceArray
                        .filter(title => relevantCountries.includes(title.iso_3166_1))
                        .map(title => title.title)
                        .join(' | ')
                    : '';  // Default to an empty string if no valid array is found

                console.log(alternativeTitles);

                const alternative = item.original_name ? `${item.original_name} | ${alternativeTitles}` : alternativeTitles;

                combinedData.push({
                    source: 'TMDB',
                    title: item.name || item.title,
                    id: item.id,
                    status: details.status || (item.media_type === 'tv' ? 'TV Show' : 'Movie'),
                    mediaType: item.media_type,
                    image: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
                    description: item.overview,
                    releaseDate: item.first_air_date || item.release_date,
                    alternative: alternative
                });
            })
            .catch(error => {
                console.error('Error fetching or processing data for item:', item.id, error);
            })
        );
    });
}

    // Process custom API data
    responses[2].slice(0, slice).forEach(item => {
        combinedData.push({
            source: 'localdb',
            title: item.titleUa,
            id: item.id,
            status: item.status_id === 2 ? 'Currently Airing' : 'Finished Airing',
            mediaType: 'Anime',
            image: '', 
            description: item.description,
            releaseDate: item.releaseDate,
            alternative: item.titleEn
        });
    });

    // Wait for all TMDB fetches to complete before continuing
    return Promise.all(tmdbPromises).then(() => {
        if (combinedData.length > 0)
            document.querySelector('#resultsInMulti').classList.toggle('d-none');
        
        return combinedData;
    });
}

function generateSuggestionsSearch(query)
{
    loadMultiSearchData(query).then(processMultiSearchData).then(initializeMultiSearchTable);
}
