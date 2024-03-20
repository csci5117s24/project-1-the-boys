let submitSearch = document.getElementById("searchButton")
submitSearch.addEventListener("click", searchPosts)

async function searchPosts(){
    let input = document.getElementById("searchContent")
    console.log(input)
    let searchResults  = await fetch("/api/searchPosts", {
        method:"GET",
        headers:{
            "content-type":"application/json"
        }
    })


}
<script src="../static/js/stock_api.js"></script>