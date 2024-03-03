document.getElementById("edit").addEventListener("click", display);

function display()
{
    if(document.getElementById("profileUpdate").getAttribute("hidden") === "true")
    {
        document.getElementById("profileUpdate").removeAttribute("hidden");
        console.log("setting false");
    }
    else
    {
        console.log("setting true");
        document.getElementById("profileUpdate").setAttribute("hidden","true");
    }
}