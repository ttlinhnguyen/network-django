document.querySelectorAll('.like-btn').forEach(btn => {
    btn.onclick = function() {
        likePost(this.dataset.postid, btn)
    }
})

document.querySelectorAll('.like-numbers').forEach(span => {
    showLikeNumbers(span.dataset.postid, span)
})

function showLikeNumbers(postid, container) {
    fetch(`/like/${postid}`)
    .then(response => response.json())
    .then(data => {
        container.innerHTML = data.like_count
    })
}

function likePost(postid, container) {
    fetch(`/like/${postid}`, {
        method: 'PUT'
    })
    showLikeNumbers(postid, container.querySelector('.like-numbers'))
}