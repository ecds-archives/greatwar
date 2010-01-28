<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Postcards : Process Description Change</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

// name of the current file (for links that display same content with different options)
$self = "do_modify.php";

include_once ("lib/figDesc.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$entity = $_POST["entity"];
$title = $_POST["title"];
$description = $_POST["desc"];
// categories (how not to hard code this?)
// FIXME: these should at least be in one place (config file?)
$interpGrp["nat"] = $_POST["nationality"];
$interpGrp["mil"] = $_POST["military"];
$interpGrp["hf"] = $_POST["homefront"];
$interpGrp["con"] = $_POST["content"];
$interpGrp["img"] = $_POST["image"];
$interpGrp["time"] = $_POST["time-period"];		// FIXME: errors with the space ?

$ana = "";
 foreach ($interpGrp as $ig) {
  for ($i = 0; $ig[$i]; $i++) {
     $ana .= "$ig[$i] ";
  }
}

print '<div class="content"> 
          <h3>Modify Postcard Description</h3>';

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
	      'entity' => $entity,
      	      'title' => $title,
	      'ana' => $ana,
              'description' => $description,
	      'imgpath' => 'http://beck.library.emory.edu/greatwar/postcard-images/thumbnail/',
	      'debug' => false);
$desc = new figDesc($args);

$desc->printDesc();
$desc->taminoModify();

print "<p class='admin'>\n";
print "<a href='${base_url}postcards/view.php?id=$entity'>View postcard</a><br>\n";
print "<a href='modify.php?id=$entity'>Modify description</a><br>\n";
print "<a href='comment.php?id=$entity'>Add a Comment</a><br>\n";
// modify/delete comments -- only display if there are comments ?
//print "<a href='admin/postcards/comment.php?id=$id'>Modify Comments</a><br>\n";
print "</p>\n";

print "</div>";
print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

print "</body>
</html>";

?>
