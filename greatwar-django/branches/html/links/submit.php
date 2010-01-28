<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print "
<html>
  <head>
    $csslink
    <title>The Great War : Links : Submit a New Link</title> 
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
	      'debug' => false);
$link = new aLinkRecord($args);

print "<h2>Submit a new link</h2>";

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

