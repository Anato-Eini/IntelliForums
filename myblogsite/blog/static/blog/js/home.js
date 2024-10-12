$(document).ready(function () {


    //initialization of view counts of posts
    $('.inner-main-body').children().forEach(function (element) {
        let user_post_pk = element.children().first().val()

    })
})

function get_views(user_post_id){
    let view_count

    $.ajax({
        url: url_view_num,
        method: "GET",
        data: {
            'pk': user_post_id,
        },
        headers: {
            'X-CSRFToken' : csrf_token
        },
        success: (data) => {
            view_count = data
        }
    })

    return view_count
}

function get_comments_count(user_post_pk){
    //TODO implement ajax that fetch number of comments of a particular post
}