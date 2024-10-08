(function (window, document) {

    // we fetch the elements each time because docusaurus removes the previous
    // element references on page navigation
    function getElements() {
        return {
            layout: document.getElementById('layout'),
            menu: document.getElementById('menu'),
            menuLink: document.getElementById('menuLink')
        };
    }

    function toggleClass(element, className) {
        var classes = element.className.split(/\s+/);
        var length = classes.length;
        var i = 0;

        for (; i < length; i++) {
            if (classes[i] === className) {
                classes.splice(i, 1);
                break;
            }
        }
        // The className is not found
        if (length === classes.length) {
            classes.push(className);
        }

        element.className = classes.join(' ');
    }
    
    function toggleAll() {
        var active = 'active';
        var elements = getElements();

        toggleClass(elements.layout, active);
        toggleClass(elements.menu, active);
        toggleClass(elements.menuLink, active);
    }
    
    function handleEvent(e) {
        var elements = getElements();
        
        if (e.target.id === elements.menuLink.id) {
            toggleAll();
            e.preventDefault();
        } else if (elements.menu.className.indexOf('active') !== -1) {
            toggleAll();
        }
    }
    
    document.addEventListener('click', handleEvent);

}(this, this.document));

let postHidden=true
let postDiv = document.getElementById("create-post-div")
let editDiv = document.getElementById("profileUpdate")

let postPopup = document.getElementById("post-button").addEventListener("click", function(event){
    console.log("toggle post")
    postDiv.toggleAttribute('hidden')
    if(!editDiv.hasAttribute('hidden')){
        editDiv.toggleAttribute('hidden')
        console.log("edit profile hidden due to post popup")
    }
    postHidden = !postHidden
    console.log(postHidden)
    
})



let closePost = document.getElementById("close-post").addEventListener("click", ()=>{
    if(!postDiv.hasAttribute('hidden')){
        postDiv.toggleAttribute('hidden')
        console.log("post hidden due to X")
    }
    
})






// let menu = document.getElementById("menu")

// let items = menu.getElementsByTagName("li")
// for(item of items){
//     item.addEventListener("click",()=>{
//         console.log(item.toggleClass("pure-menu-selected"))
//     });
// }


