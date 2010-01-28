<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print "
<html>
  <head> 
    $csslink
    <title>The Great War : Poetry : Advanced Search</title> 
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
    <base href='$base_url'>
  </head> 
<body>
";

include_once("lib/mybreadcrumb.php");

include("header.php");

print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb();

print '
<div class="content">
<h2>Poetry Search</h2>
<form name="poetryquery" action="poetry/search.php" method="get">
<table class="searchform" border="0">
<tr><th>Keyword</th><td><input type="text" size="40" name="keyword"></td></tr>
<tr><th>Title</th><td><input type="text" size="40" name="title"></td></tr>
<tr><th>Author</th><td><input type="text" size="40" name="author"></td></tr>
<tr><th>Date</th><td><input type="text" size="40" name="date"></td></tr>
</tr></td>
</table>
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
