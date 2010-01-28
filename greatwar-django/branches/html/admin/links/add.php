<?php
include("../../config.php");	


print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Links : Add a New Link</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

include_once ("lib/alinkRecord.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

print '<div class="content">'; 

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['links'],
       	      'contributor' => $_SESSION['name'],
	      'debug' => false);
$link = new aLinkRecord($args);

print "<h3>Submit a new link</h3>";

$link->printHTMLForm("add");

print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>

