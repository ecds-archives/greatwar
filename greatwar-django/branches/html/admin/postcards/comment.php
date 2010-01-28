<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Postcards : Add Comments</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

// name of the current file (for links that display same content with different options)
$self = "comment.php";

include_once ("lib/figureComment.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$entity = $_GET["id"]; 

print '<div class="content"> 
          <h3>Add Comments to Postcard</h3>';

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
	      'entity' => $entity,
	      'imgpath' => 'http://beck.library.emory.edu/greatwar/postcard-images/thumbnail/',
	      'name' => $_SESSION['name'],
	      'debug' => false);
$fc = new figureComment($args);

//$fc->taminoGetRecord();
$fc->getFigureInfo();
$fc->printform("add_comment.php");


print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");
print "</body>
</html>";

?>
