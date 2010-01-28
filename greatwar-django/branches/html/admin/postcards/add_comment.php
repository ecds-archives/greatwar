<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Postcards : Process Comment</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

// name of the current file (for links that display same content with different options)
$self = "add_comment.php";

include_once ("lib/figureComment.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$entity = $_POST["entity"];
$title = $_POST["title"];
$comment = $_POST["comment"];
$name = $_POST["name"];
$date = $_POST["date"];
$pre = $_POST["preview"];
$post = $_POST["submit"];

if ($pre) { $mode = "preview"; }
else if ($post) { $mode = "submit"; }

print "<div class='content'>\n";
if ($mode == "preview") {
  print "<h3>Preview Postcard Comment</h3>";
} else if ($mode == "submit") {
  print "<h3>Process Postcard Comment</h3>";
}

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
	      'entity' => $entity,
      	      'title' => $title,
              'comment' => $comment,
              'name' => $name,
	      'date' => $date,
	      'imgpath' => 'http://beck.library.emory.edu/greatwar/postcard-images/thumbnail/',
	      'debug' => false);
$fc = new figureComment($args);

if ($mode == "preview") {
  print "<p>Preview</p>";
  $fc->display();
  print "<hr>";
  print "<p>Continue Editing</p>";
  $fc->printform("add_comment.php");

} else if ($mode == "submit") {
  $fc->display();
  $fc->taminoAdd("admin");	// add comment in admin mode

  // link to the postcard detailed view
  print "<a href='${base_url}postcards/view.php?id=$entity'>View Postcard</a><br>\n";
}


print "</div>";

print '<div class="sidebar">'; 
include("nav.html"); 
include("searchbox.php"); 
print '</div>'; 
include("footer.html"); 

print "</body>
</html>";

?>
