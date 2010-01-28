<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Links : Process Approval</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

include_once ("lib/alinkRecord.class.php");
include_once("lib/mybreadcrumb.php");

$myargs = array('host' => $tamino_server,
		'db' => $tamino_db,
		'coll' => $tamino_coll['links'],
		'debug' => false);

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

print '<div class="content">'; 

print '<h3>Processing link record approval</h3>'; 

// each id is a record to approve, if val=on
foreach ($_GET as $id => $val) {
  if ($val != "on") {
    next; //probably should not happen
  }
  // spaces in the ids are getting converted to underscores
  $id = str_replace("_", " ", $id);
  $myargs[id] = $id;
  $newlink[$id] = new alinkRecord($myargs);
  $newlink[$id]->taminoGetRecord();	// initialize link
  $newlink[$id]->approve();
}


print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>

