<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Postcards : Approve Comments</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

include_once ("lib/figureComment.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$comment_id = $_GET["id"];
$action = array();
foreach ($comment_id as $c) {
  $action[$c] = $_GET[$c];
  print "DEBUG: id=$c, action = $action[$c]<br>\n";
}

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
	      'imgpath' => 'http://beck.library.emory.edu/greatwar/postcard-images/thumbnail/',
	      'name' => $_SESSION['name'],
	      'debug' => true);

foreach ($comment_id as $c) {
  $args['id'] = $c;
  $fc = new figureComment($args);
  switch ($action[$c]):
 case 'approve': $fc->approveComment();
    break;
 case 'delete': $fc->deleteComment("user");
   break;
 case 'null':
 default:     // do nothing
   endswitch;
}



print '<div class="content">'; 


print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");


?>

</body>
</html>

