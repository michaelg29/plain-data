ipcRenderer.on('board:load', function (e, id) {
    loadBoard(id);
});

function loadBoard(id) {
    board.retrieve(id);
}

ipcRenderer.on('board:loaded', function(e, values) {
    board_loaded(values);
});

function board_loaded(values) {
    try {
        jQuery('#title').html(values['title']);
        jQuery('#creator').html(values['creator']);
        jQuery('#date').html(values['date']);
        jQuery('#category').html(values['category']);
        jQuery('#tags').html(values['tags'].replace(/,/g, ', '));
        jQuery('#content').html(values['content']);

        jQuery('#post-comment-btn').on('click', function() {
            comment(values['id']);
        });

        let commentsHtml = "<ul>";

        for (var i = 0; i < values['comments'].length; i++) {
            let comment = values['comments'][i];

            commentsHtml += `
                <li class="blurb" style="list-style-type: none">
                    <p class="blurb-title">${comment['subject']}</p>
                    <p style="font-style:italic;" class="text-muted">${comment['name']} on ${comment['date']}</p>
                    <hr/>
                    <div class="blurb-content">
                        ${comment['content']}
                    </div>
                </li>
            `;
        }

        commentsHtml += "</ul>";

        document.querySelector('#comments').innerHTML = commentsHtml;

        renderer.updateLinks();
    } catch (error) {
        console.log(error);
    }
}

function openCommentPrompt() {
    document.querySelector('#comment-form').classList.toggle('hidden');
}

function comment(id) {
    var subject = document.querySelector('#subject').value;
    var comment_content = document.querySelector('#comment-content').value;

    board.comment(id, subject, comment_content);
}