// Rebecca Sutton Koeser, August 26 2003
// Collapsible list functions 


// base url for closed/open images
var base_url = "images/";


function toggle_ul (id) {
  if(document.getElementById){
   a = document.getElementById(id);
   //   alert("current style is " + a.style.display);
   if (a.style.display == '') {
     a.style.display = "none";
   }
   a.style.display = (a.style.display != "none") ? "none":"block";
  }
  toggle_gif(id+'-gif');  
}

function toggle_gif (id) {
  if(document.getElementById) {
    a=document.getElementById(id);
   if (a.style.display == '') {
     a.style.display = "closed";
   }
   a.status = (a.status == "open") ? "closed":"open";
   a.src = base_url + a.status + ".gif";
  }
}

// store current display properties in cookies
function store_status (max, name) {
  var crumb = new Cookie(document, name);		

  // Note: only lists that are open/visible will be stored here, 
  // in an attempt to keep cookie size minimal
  for (i = 1; i <= max; i++) { 
    if(document.getElementById) { 
      var list = document.getElementById('list' + i); 
      // only set cookie if list is being displayed (otherwise default)
      if (list.style.display == "block") {	// only set cookie if = 1
	crumb["L" + i] = 1; 
      }
    }
  }
  crumb.store();
}

// store current display properties in cookies
function load_status (max, name) {
  var crumb = new Cookie(document, name);
  crumb.load();
  // for each list & each graphic, load current setting from cookie 
  for (i = 1; i <= max; i++) { 
    if(document.getElementById) { 
      var list = document.getElementById('list' + i); 
      // list:  1 = block, 0 or undefined = none
      list.style.display = (crumb["L" + i]) ? "block" : "none";

      var gif = document.getElementById('gif_list'+i); 
      // gif must correspond to list in being open/closed
      // list icon : 1 = open, 0 = closed
      gif.status = (crumb["L" + i]) ? "open" : "closed";
      // default image is closed; change image if necessary
      if (gif.status == 'open')  gif.src = base_url + "open.gif";
    } 
  } 
}


