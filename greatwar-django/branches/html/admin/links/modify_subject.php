<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Links : Manage Subjects</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

include_once ("lib/subjectList.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$myargs = array('host' => $tamino_server,
		'db' => $tamino_db,
		'coll' => $tamino_coll['links']);
$subject_list = new subjectList($myargs);

print '<div class="content">
<h3>Modifying Subjects</h3>';

print "<hr>";


$subject = $_GET["subj"];
if (count($subject) > 1) {
  // only if there are multiple subjects (i.e., when removing several)
  foreach ($subject as $s) {
    $s = htmlentities($s);
 }
}
$mode = $_GET["mode"];  // add or del

switch ($mode):
  case 'add':  
  // Only add the subject if it is not already in the list
    if ( $subject_list->isSubject($subject)) {
      print "<p>Error: Subject <b>$subject</b> is already in the list.  Not adding.</p>";
    } else {
      $subject_list->taminoAdd($subject); 
    }
    break;
  case 'del':  
   // it is possible to have multiple subjects selected for deletion
    foreach ($subject as $s) {
      $subject_list->taminoDelete($s); 
    }
    break;
endswitch;

// update subject list from Tamino
$subject_list->taminoGetSubjects();
print "<hr><h3>Newly updated subject heading list</h3>\n";
$subject_list->printHTMLList();


print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>

