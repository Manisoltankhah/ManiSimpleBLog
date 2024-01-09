function sendArticleComment(articleId) {
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();
    console.log(parentId);
    $.get('/article/add-article-comment', {
        article_comment: comment,
        article_id: articleId,
    }).then(res => {
        console.log(res);
    });
}






















