<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Links : Search</title> 
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

include_once ("lib/alinkCollection.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

print '<div class="content">'; 
$subject = $_GET['subj'];
$kw = $_GET['keyword'];

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['links'],
      	      'limit_subject' => $subject[0],
	      'keyword' => $kw,
	      'sort' => $sort,
	      'debug' => false);

$linkset = new aLinkCollection($args);

print "<p align='center'>" .  $linkset->count . " match";
if ($linkset->count != 1) { print "es"; }
print "</p>";

$linkset->printSummary();


print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>

