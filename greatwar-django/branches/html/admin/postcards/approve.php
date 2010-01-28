<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Postcards : Approve Comments</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

include_once ("lib/figureComment.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
	      'entity' => $entity,
	      'imgpath' => 'http://beck.library.emory.edu/greatwar/postcard-images/thumbnail/',
	      'name' => $_SESSION['name'],
	      'debug' => true);
$fc = new figureComment($args);


print '<div class="content">'; 

$fc->getUserComments();
$fc->approvalForm("do_approve.php");

print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>

