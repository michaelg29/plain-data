ipcRenderer.on('board:search:results', function (e, results) {
    board_search_results(results);
});

function board_search_results(results) {
    var html = `<h1>Search Results (${results.length} items):</h1><ol>`;

    results.map((res, idx, arr) => {
        var item = `<li class='blurb' onclick='open_board(${res['id']})'>
            <span class="blurb-title">${res['title']}</span><br/>
            Author: <span class='blurb-val'>${res['creator']}</span>
        </li>`;

        html += item;
    });

    html += "</ol>"

    jQuery('#search-results').html(html);
}

function open_board(id) {
    board.retrieve(id);
}