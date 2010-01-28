<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Links : Delete Link</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

include_once ("lib/alinkCollection.class.php");
include_once("lib/mybreadcrumb.php");

$id = $_GET["id"];

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

print '<div class="content">
<h3>Delete an existing link</h3>';

$myargs = array('host' => $tamino_server,
		  'db' => $tamino_db,
		  'coll' => $tamino_coll['links'],
		  'id' => $id);
$link = new aLinkRecord($myargs);
// get the record so we can display useful feedback-- i.e., what was deleted
$link->taminoGetRecord();
$link->taminoDelete();

print 'Return to <a href="view.php">full listing</a> of all links records.'; 

print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>
