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

let postHidden=true
let postDiv = document.getElementById("create-post-div")
let postPopup = document.getElementById("post-button").addEventListener("click", function(event){
  
    postDiv.toggleAttribute('hidden')
    postHidden = !postHidden
    console.log(postHidden)
    
})
// let body = document.querySelector('body')

// body.addEventListener("click", function(event){
//   if(!postHidden){
//     if(event.target.closest('#html-body')) return
//     postDiv.toggleAttribute('hidden')
//     postHidden=true
//   }
// })

// const onClickOutside = (element, callback) => {
//     document.addEventListener('click', e => {
//       if (!element.contains(e.target)) callback();
//     });
    
//   };
  
//   onClickOutside(postDiv, () => 
// {
    
//     console.log(postDiv.getAttribute("hidden"))
//     postDiv.setAttribute("hidden", true)}
//     );