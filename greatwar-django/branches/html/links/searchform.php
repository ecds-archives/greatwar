<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	
include_once("lib/mybreadcrumb.php");
include_once ("lib/alinkCollection.class.php");

print "<html>
  <head> 
    $csslink
    <title>The Great War : Links : Search</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
  </head> 
<body> 
"; 

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb();

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['links'],
	      'debug' => false);
$linkset = new aLinkCollection($args);


print '
<div class="content">
<h2>Link Search</h2>
<form name="linksearch" action="search.php" method="get">
<table class="searchform" border="0">
<tr><th>Keyword</th><td><input type="text" size="40" name="keyword"></td></tr>
<tr><th class="label">Subjects</th>';
print "<td>";
$linkset->subject->printSelectList();
print "</td></tr>";
print '</table>
<input type="submit" value="Submit"> 
<input type="reset" value="Reset">
</form>';


print '</div>';

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print '</div>';

include("footer.html");

?>

</body>
</html>
