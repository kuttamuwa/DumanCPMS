// AJAX for posting
function create_checkaccount() {
    console.log("create post is working!")  // sanity check
    console.log($('#post-text').val())
};

// Submit post on submit
$('#checkaccount-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});
