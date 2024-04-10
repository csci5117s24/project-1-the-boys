
// let stockCurrent = document.getElementById('stock-ticker-viewer').innerText

// let currentStockVals = document.querySelectorAll('div.group-stock h1')
// let currentStockNums = document.querySelectorAll(".stock-nums td")
// let searchForm = document.getElementById("searchForm").addEventListener("submit", searchPosts)

// async function searchPosts(event){
    
//     url = window.location.origin
//     let form = event.currentTarget;
//     let sendData = new FormData(form)
//     let data = Object.fromEntries(sendData)
//     data["name"]=currentStockVals[0].innerText
//     data["symbol"]=currentStockVals[1].innerText
//     data["from" ]=currentStockVals[2].innertext
//     data["open"]=currentStockNums[0].innerText
//     data["close"]=currentStockNums[1].innerText
//     data["high"]=currentStockNums[2].innerText
//     data["low"]=currentStockNums[3].innerText
//     data["volume"]=currentStockNums[4].innerText
//     data["type"]="Search"
//     const formStuff = JSON.stringify(data)
//     console.log(formStuff)
//     await fetch(url+"/",{
//         method:"POST",
//         headers:{
//             "Content-Type":"application/json"
//         },
//         body:formStuff

//     }).then((response) => {
//         return response.text();
//     })
// }

// let currentPosts = document.getElementById("searchContent").innerText
// let stockForm = document.getElementById("stockForm").addEventListener("submit", searchStock)
// async function searchStock(event){
//     event.preventDefault()
//     url = window.location.origin
//     let form = event.currentTarget;
//     let sendData = new FormData(form)
//     let data = Object.fromEntries(sendData)
//     data["searchFor"]=currentPosts
//     data["type"]="Stock"
//     const formStuff = JSON.stringify(data) 
//     console.log(formStuff)
//     await fetch(url+"/",{
//         method:"POST",
//         headers:{
//             "Content-Type":"application/json"
//         },
//         body:formStuff

//     }).then((response) => {
        
//         return response.text();
//     }).then((html) => {
        
//         document.head.innerHTML=html
//         stockCurrent = document.getElementById('stock-ticker-viewer').innerText
//         currentStockVals = document.querySelectorAll('div.group-stock h1')
//         currentStockNums = document.querySelectorAll(".stock-nums td")
//         stockForm = document.getElementById("stockForm").addEventListener("submit", searchStock)
//     });
        
// }


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



