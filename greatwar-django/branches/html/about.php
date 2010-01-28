<?php
include("config.php");

print " 
<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'>
<html>
  <head> 
    <title>The Great War : About the Site</title>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <base href='$base_url'>
    $csslink
  </head> 
<body> 
"; 

include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

// actual content: introductory essay (in content directory)
include("about.xml");


print '<div class="sidebar">';
include("searchbox.php");
print '</div>';
include("footer.html");

?>

</body>
</html>

