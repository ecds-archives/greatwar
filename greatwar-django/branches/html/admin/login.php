<?php

include("../config.php");	

session_start();
header("Cache-control: private");	//  IE 6 fix
$_SESSION['authlevel'] = 1;
$_SESSION['name'] = $_SERVER['REMOTE_USER'];

print " 
<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'>
<html>
  <head> 
    <title>The Great War : Administration</title>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <base href='$base_url'>
    $csslink
  </head> 
<body> 
"; 

include_once("lib/taminoConnection.class.php");
include_once ("lib/alinkCollection.class.php");
include_once ("lib/figureComment.class.php");
include_once("lib/mybreadcrumb.php");


include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

print "<div class='content'>\n";
print "<p>You are now logged in as : " .  $_SESSION['name'] . "</p>";
//print "Your session is : " .  session_id() . "<br>";

print "<p>To edit postcard descriptions, browse or search and find the cards
you wish to modify.  In both the single postcard view and the browse
view with descriptions, there will be a link to modify the postcard
description and categories.</p>"; 

// FIXME: add useful information
// there are currently $count links to approve and $count postcard comments to approve
$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['links'],
	      'limit_subject' => $subject[0],
	      'sort' => $sort,
	      'debug' => false);

$linkset = new aLinkCollection($args);
$appr_count = $linkset->approveCount();

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
	      'debug' => false);
$fc = new figureComment($args);
$fc->getUserComments();
$pc_count = $fc->countUserComments();


print "<p><b>Pending approvals</b><br>";
print "&nbsp;&nbsp;Link submissions: <b>$appr_count</b><br>";
print "&nbsp;&nbsp;Postcard comments: <b>$pc_count</b><br></p>";

print "</div>";
print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print '</div>';
include("footer.html");

?>

</body>
</html>
