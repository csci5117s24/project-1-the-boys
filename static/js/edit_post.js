


function display(idname)
{   
    if(document.getElementById(idname).getAttribute("hidden") === "true")
    {
        document.getElementById(idname).removeAttribute("hidden");
        console.log("setting false");
    }
    else
    {
        console.log("setting true");
        document.getElementById(idname).setAttribute("hidden","true");
    }
    if(!postDiv.hasAttribute('hidden')){
        postDiv.toggleAttribute('hidden')
        console.log("post hidden due to X")
    }
    
}
function hideEditPost(id){
    let thisPost = document.getElementById(id)
    thisPost.addEventListener("click",()=>{
        if(!thisPost.hasAttribute("hidden")){
            thisPost.toggleAttribute("hidden")
            console.log("close edit post")
        }
    })
}
