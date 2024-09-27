$(document).ready(() => {

    /**
     * Initialization of votes in comments
     */
    $('#comment-section').children().each(child => {
        let grandchild = $(this).firstChild.firstChild
        let comment_id = grandchild.data('value');
        let children_last_child = grandchild.children().lastChild

        let upvote_element = children_last_child.firstChild
        let downvote_element = children_last_child.firstChild

        upvote_element.on('click', () => {

        })

    })


    /**
     * Handles post_vote ajax requests
     * @param type - Vote type 1-Upvote 2-Downvote
     * @param pk - PostUser id
     * @param url - Url for ajax
     */
    function post_vote(type, pk, url){
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

    function get_comment_votes(pk, url){

    }

    /**
     * Handles comment_vote ajax requests
     * @param type - Vote type 1-Upvote 2-Downvote
     * @param pk - Primary key of comment
     * @param comment_element - Comment element
     * @param url - Url to send requests
     */
    function post_comment(type, pk, comment_element, url){
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
                let vote_div = comment_element.children().lastChild()
                vote_div.firstChild.textContent = "Upvote: ".concat(data.upvote)
                vote_div.lastChild.textContent = "Downvote: ".concat(data.downvote)
            }
        })
    }

    $('#post_upvote').on('click', () => {
        post_vote(1, user_post_pk, post_vote_url)
        let upvote_div = $('#post_upvote')
        if(upvote_div.hasClass('upvoted'))
            upvote_div.removeClass('upvoted')
        else
            upvote_div.addClass('upvoted')
    })

    $('#post_downvote').on('click', () => {
        post_vote(0, user_post_pk, post_vote_url)
        let downvote_div = $('#post_downvote')
        if(downvote_div.hasClass('downvoted'))
            downvote_div.removeClass('downvoted')
        else
            downvote_div.addClass('downvoted')
    })
})
