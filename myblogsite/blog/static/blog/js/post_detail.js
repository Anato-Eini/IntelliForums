$(document).ready(() => {

    /**
     * Initialization of votes in comments
     */
    $('#comment-section').children().each(function () {
        let grandchild = $(this).children().first()
        let comment_id = grandchild.data('value');
        let children_last_child = grandchild.children().last()

        let upvote_element = children_last_child.children().first()
        let downvote_element = children_last_child.children().last()

        ajax_comment_vote(1, comment_id, "GET", upvote_element, downvote_element)

        upvote_element.on('click', () => {
            ajax_comment_vote(1, comment_id, "POST", upvote_element, downvote_element);
        })

        downvote_element.on('click', () => {
            ajax_comment_vote(0, comment_id, "POST", upvote_element, downvote_element);
        })

    })


    /**
     * Handles post_vote ajax requests
     * @param type - Vote type 1-Upvote 2-Downvote
     * @param pk - PostUser id
     * @param url - Url for ajax
     */
    function ajax_post_vote(type, pk, url){
        $.ajax({
            url: url,
            method: "POST",
            data: {
                type: type,
                pk: pk
            },
            headers: {
                'X-CSRFToken' : csrf_token
            },
            success: (data) => {
                let upvote_div = $('#post_upvote')
                let downvote_div = $('#post_downvote')
                upvote_div.text("Upvote: ".concat(data.upvote))
                downvote_div.text("Downvote: ".concat(data.downvote))
            }
        })
    }

    /**
     *
     * @param type - 1-Upvote 2-Downvote
     * @param pk - Comment.id
     * @param method - "POST" or "GET"
     * @param upvote_h5 - Upvote div to modify the text
     * @param downvote_h5 - Downvote div to modify the text
     */
    function ajax_comment_vote(type, pk, method, upvote_h5, downvote_h5){
        $.ajax({
            url: comment_vote_url,
            method: method,
            data: {
                pk: pk,
                type: type
            },
            headers: {
                'X-CSRFToken' : csrf_token
            },
            success: (data) => {
                upvote_h5.text("Upvote: ".concat(data.upvote))
                downvote_h5.text("Downvote: ".concat(data.downvote))
            }
        })
    }

    $('#post_upvote').on('click', () => {
        ajax_post_vote(1, user_post_pk, post_vote_url)
        let upvote_div = $('#post_upvote')
        if(upvote_div.hasClass('upvoted'))
            upvote_div.removeClass('upvoted')
        else
            upvote_div.addClass('upvoted')
    })

    $('#post_downvote').on('click', () => {
        ajax_post_vote(0, user_post_pk, post_vote_url)
        let downvote_div = $('#post_downvote')
        if(downvote_div.hasClass('downvoted'))
            downvote_div.removeClass('downvoted')
        else
            downvote_div.addClass('downvoted')
    })
})
