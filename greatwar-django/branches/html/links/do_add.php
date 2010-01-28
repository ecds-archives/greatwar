<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print "
<html>
  <head>
    $csslink
    <title>The Great War : Links : Process New Link</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
  </head>
<body>
";

include_once ("lib/alinkRecord.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

print '<div class="content">'; 

print '<h2>Processing new link</h2>'; 


$url = htmlentities($_GET["url"]);
$title = htmlentities($_GET["title"]);
$description = htmlentities($_GET["desc"]);
$subject = $_GET["subj"];
$date = htmlentities($_GET["date"]);
$contributor = htmlentities($_GET["contrib"]);


// check that variables are set (all fields should be set)
if (!(isset($url))||(!(isset($title)))||(!(isset($description)))
    ||(!isset($subject))||(!isset($date))||(!isset($contributor))) {
  print "<p class='error'>Error! One or more required fields were not defined.</p>";
  print "Please <a href='javascript:back()'>go back</a> and fill in those fields.";
  exit();
}


$myargs = array('host' => $tamino_server,
		'db' => $tamino_db,
		'coll' => $tamino_coll['links'],
		'url' => $url,
		'title' => $title,
		'description' => $description,
		'date' => $date,
		'contributor' => $contributor,
		'debug' => false);
$newlink = new alinkRecord($myargs, $subject);
$newlink->taminoAdd();
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

