$(document).ready(function () {

    //initialization of view counts of posts
    $('.inner-main-body').children().each(function () {
        let first_children = $(this).children();
        let user_post_pk = first_children.first().val()

        let target_parent = first_children.eq(1).children().first().children().eq(2).children()

        get_views(user_post_pk).then(view_count => {
            target_parent.first().append(view_count)
        }).catch(error => {
            console.error("Error fetching view count ", error)
        })

        get_comments_count(user_post_pk).then(count => {
            target_parent.last().append(count)
        }).catch(error => {
            console.error("Error fetching comments count", error)
        })
    })

})

function get_views(user_post_id){
    return new Promise((resolve, reject) => {
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
                resolve(data.view_count)
            },
            error: (error) => {
                reject(error)
            }
        })
    })
}

function get_comments_count(user_post_id){
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url_comment_num,
            method: "GET",
            data:{
                'pk': user_post_id
            },
            headers: {
                'X-CSRFToken' : csrf_token
            },
            success: (data) => {
                resolve(data.comment_count)
            },
            error: (error) => {
                reject(error)
            }
        })
    })
}