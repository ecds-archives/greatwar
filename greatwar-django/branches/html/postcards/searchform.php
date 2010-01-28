<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print "<html>
  <head> 
    $csslink
    <title>The Great War : Postcards : Advanced Search</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
    <base href='$base_url'>
  </head> 
<body> 
"; 

include_once("lib/mybreadcrumb.php");
include_once("lib/xmlDbConnection.class.php");

include("header.php");

print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb();


$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
      	      'coll' => $tamino_coll['postcards'],
	      'basedir' => $basedir,
	      'debug' => false,
	      );
$tamino = new xmlDbConnection($args);

$cat_query = 'for $a in input()/TEI.2/:text/back/:div//interpGrp 
return $a'; 
$cat_xsl = "interp.xsl";
$cat_params = array("mode" => "form");
$tamino->xquery($cat_query);
$tamino->xslTransform($cat_xsl, $cat_params);


print '
<div class="content">
<h2>Postcard Search</h2>
<form name="postcardquery" action="postcards/search.php" method="get">
<table class="searchform" border="0">
<tr><th>Keyword</th><td><input type="text" size="40" name="keyword"></td></tr>
<tr><th>Title</th><td><input type="text" size="40" name="title"></td></tr>
<tr><th>Description</th><td><input type="text" size="40" name="figdesc"></td></tr>
<tr><th colspan="2" class="label">Categories</th></tr>';
$tamino->printResult();
print '
</tr></td>
</table>
<input type="submit" value="Submit"> 
<input type="reset" value="Reset">
</form>';


print '</div>';

print '<div class="sidebar">';
include("postcards/nav.html");
include("searchbox.php");
print '</div>';

include("footer.html");

?>

</body>
</html>
