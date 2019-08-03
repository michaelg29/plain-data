function categoryToggle() {
    jQuery('#category-list').toggleClass("dropdown-show");
}

function categorySelected(val) {
    jQuery('#category').html(val);
    categoryToggle();
}

function createBoard() {
    let atts = {
        "user": remote.getGlobal('user').atts['ID'],
        "title": jQuery('#title').val(),
        "creator": remote.getGlobal('user').atts['Username'],
        "category": document.querySelector('#category').innerHTML,
        "tags": jQuery('#tags').val(),
        "content": jQuery('#content').val()
    };

    board.create(atts);
}