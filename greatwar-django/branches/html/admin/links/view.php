<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Links : View Links</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

// name of the current file (for links that display same content with different options)
$self = "view.php";

include_once ("lib/alinkCollection.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$sort = $_GET["sort"]; // options: title|contrib|date
if ($sort == '') { $sort = 'title'; }	// default sort
$show_edits = $_GET["show_edits"];   // options : 1 | 0
$subject = $_GET['subj'];

print '<div class="content"> 
          <h3>All Links - Full Listing</h3>';

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => 'links',
	      'limit_subject' => $subject[0],
	      'sort' => $sort,
	      'debug' => false);
$linkset = new aLinkCollection($args);


print "<p align='center'>Sorting by <b>$sort</b>, edits are <b>" . ($show_edits ? "visible" : "hidden") . "</b>";
if ($subject[0]) {
  print ", and subject is <b>$subject[0]</b>";
} 
print ".</p>";

print "<p><table class='sortopts'><tr><td>";
$linkset->printSortOptions($self, "admin");
print "</td><td>";
if ($show_edits) {
  print "<a href='$self?sort=$sort&show_edits=0&subj[]=$subject[0]'>Hide Edits</a>";
} else {
  $show_edits = 0;
  print "<a href='$self?sort=$sort&show_edits=1&subj[]=$subject[0]'>Show Edits</a>";
}
print "</td><tr>";
print "<tr><td colspan='2'>";
$linkset->printSubjectOptions("$self?sort=$sort&show_edits=$show_edits", $subject);
print "</td></tr></table></p>";

$linkset->printRecords($show_edits);

print "</div>"; 

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>

