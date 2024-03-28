// let submitSearch = document.getElementById("searchButton")
// submitSearch.addEventListener("click", searchPosts)
// let searchForm = document.getElementById("searchForm").addEventListener("submit", function(event){
//     event.preventDefault()
// })
// let stockForm = document.getElementById("stockForm").addEventListener("submit", function(event){
//     event.preventDefault()
// })


// async function searchPosts(){
//     console.log(submitSearch)
//     let input = document.getElementById("searchContent")
    
//     let searchResults  = await fetch("/api/searchPosts", {
//         method:"GET",
//         headers:{
//             "content-type":"application/json"
//         }
//     })


// }


let postPopup = document.getElementById("post-button").addEventListener("click", ()=>{
    let postDiv = document.getElementById("create-post-div")
    postDiv.toggleAttribute("hidden")
    console.log("ye it works lol")
})

