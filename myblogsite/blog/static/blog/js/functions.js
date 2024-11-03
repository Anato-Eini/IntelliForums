export function get_views(user_post_id){
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/view_num/',
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

export function get_comments_count(user_post_id){
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
