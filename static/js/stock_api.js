
let searchForm = document.getElementById("searchForm").addEventListener("submit", async function(event){
    // event.preventDefault()
    // url = window.location.origin
    // const form = event.currentTarget;
    // const sendData = new FormData(form)
    // let data = Object.fromEntries(sendData)
    // const formStuff = JSON.stringify(data)
    // console.log(formStuff)
    // searchResults = await fetch(url+"/api/searchPosts",{
    //     method:"POST",
    //     headers:{
    //         "Content-Type":"application/json"
    //     },
    //     body:formStuff

    // }
    // )
})
// let stockForm = document.getElementById("stockForm").addEventListener("submit", function(event){
//      event.preventDefault()
//     url = window.location.origin
//     const form = event.currentTarget;
//     const sendData = new FormData(form)
//     let data = Object.fromEntries(sendData)
//     const formStuff = JSON.stringify(data)
//     console.log(formStuff)
//     searchResults = await fetch(url+"/api/searchPosts",{
//         method:"POST",
//         headers:{
//             "Content-Type":"application/json"
//         },
//         body:formStuff

//     }
//     )
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

// let postHidden=true
// let postDiv = document.getElementById("create-post-div")
// let postPopup = document.getElementById("post-button").addEventListener("click", function(event){
    
//     postDiv.toggleAttribute('hidden')
//     postHidden = !postHidden
//     console.log(postHidden)
    
// })
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