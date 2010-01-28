<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Links : Modify Link</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

include_once ("lib/alinkCollection.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$id = $_GET["id"];

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['links'],
     	      'ed_contributor' => $_SESSION['name'],
	      'id' => $id);
$link = new aLinkRecord($args);
$link->taminoGetRecord();

print '<div class="content">
<h3>Modify an existing record</h3>';

$link->printHTMLForm("modify");

print '</div>';

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");

?>

</body>
</html>

