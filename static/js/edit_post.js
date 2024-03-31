
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
}