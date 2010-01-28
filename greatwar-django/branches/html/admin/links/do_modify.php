<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Links : Process  Link Modification</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

include_once ("lib/alinkCollection.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";


print '<div class="content">
<h3>Processing link modification</h3>'; 

$url = htmlentities($_GET["url"]);
$id = htmlentities($_GET["id"]);
$title = htmlentities($_GET["title"]);
$description = htmlentities($_GET["desc"]);
$subject = $_GET["subj"];
$date = htmlentities($_GET["date"]);
$contributor = htmlentities($_GET["contrib"]);
$edit_date = htmlentities($_GET["mod_date"]);
$edit_contributor = htmlentities($_GET["mod_contrib"]);
$edit_desc = htmlentities($_GET["mod_desc"]);

$myargs = array('host' => $tamino_server,
		'db' => $tamino_db,
		'coll' => $tamino_coll['links'],
		'url' => $url,
		'id' => $id,
		'title' => $title,
		'description' => $description,
		'date' => $date,
		'debug' => false,
		'contributor' => $contributor);
$newlink = new aLinkRecord($myargs, $subject);


// editing information is submitted via hidden inputs
// get any old edits & add to linkRecord so they are not lost
$edit_count = count($_GET['prev_date']);
$prev_date = $_GET['prev_date'];
$prev_contrib = $_GET['prev_contrib'];
$prev_desc = $_GET['prev_desc'];
for ($i = 0; $i < $edit_count; $i++) {
  $prev_edit = array( "date" => $prev_date[$i], 
	 	      "contributor" => $prev_contrib[$i], 
		      "description" => $prev_desc[$i]); 
  $newlink->addEdit($prev_edit); 
}

$edit_array = array( "date" => $edit_date,
		     "contributor" => $edit_contributor,
		     "description" => $edit_desc);


$newlink->addEdit($edit_array);
$newlink->taminoModify();
$newlink->printHTML();

print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>
