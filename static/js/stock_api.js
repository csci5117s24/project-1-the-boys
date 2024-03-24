let submitSearch = document.getElementById("searchButton")
submitSearch.addEventListener("click", searchPosts)
let searchForm = document.getElementById("searchForm").addEventListener("submit", function(event){
    event.preventDefault()
})
let stockForm = document.getElementById("stockForm").addEventListener("submit", function(event){
    event.preventDefault()
})


async function searchPosts(){
    
    let input = document.getElementById("searchContent")
    
    let searchResults  = await fetch("/api/searchPosts", {
        method:"GET",
        headers:{
            "content-type":"application/json"
        }
    })


}
<script src="../static/js/stock_api.js"></script>