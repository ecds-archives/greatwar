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

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['links']);
$subjects = new subjectList($args);


print '<div class="content">';
print '<h3>Manage Subjects</h3>';

print "<hr>";

print "<h3>Current subject headings</h3>";
$subjects->printHTMLList();

print "<hr>";

print '<h3>Add a new subject</h3>
<form action="modify_subject.php" method="get"> 
<input type="hidden" name="mode" value="add">
<table>
 <tr>
  <th>Subject:</th>
  <td><input type="text" size="50" name="subj"></td></tr>
</table>
  <input type="submit" value="Submit">
  <input type="reset">
</form>
';

print "<hr>";
print "<h3>Remove an existing subject</h3>";
$subjects->printRemovalForm("modify_subject.php");


print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>








?>