console.log(document.getElementsByClassName("close-popup"))
let closePopup = document.getElementsByClassName("close-popup")

for(let close of closePopup){
    
    close.addEventListener("click", function(event){
        console.log(closePopup)
        if(!postDiv.hasAttribute('hidden')){
            postDiv.toggleAttribute('hidden')
            console.log("closed edit")
        }
        else if(!editDiv.hasAttribute('hidden')){
            editDiv.toggleAttribute('hidden')
            console.log("closed edit")
        }
    })
}
let editPopup = document.getElementById("edit").addEventListener("click", function(event){
    console.log("toggle edit")
    editDiv.toggleAttribute('hidden')
    if(!postDiv.hasAttribute('hidden')){
        postDiv.toggleAttribute('hidden')
        console.log("post hidden due to edit popup")
    }
    
    console.log(postHidden)
    
})