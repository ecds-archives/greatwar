<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");

include_once("lib/xmlDbConnection.class.php");
include_once("lib/mybreadcrumb.php");

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
	      'basedir' => $basedir,
	      'debug' => false,
	      );
$tamino = new xmlDbConnection($args);

$id = $_GET["id"];
$zoom = $_GET["zoom"];

($zoom == "2") ? $mode = "zoom" : $mode = "full";
$xsl_params = array("mode" => $mode);


$query = '<div> { for $a in input()/TEI.2/:text/body/p/figure
where $a/@entity = "';
$query .= "$id";
$query .= '" return $a }"';
$query .= '{ for $b in input()/TEI.2/:text/back/:div//interpGrp return $b }</div>';
// need to retrieve interpGrps to display categories nicely
$xsl_file = "figures.xsl";
$tamino->xquery($query);
$title = $tamino->findNode("head");

// FIXME: titles with tags in them will display a little strangely

print "<html>
  <head> 
    $csslink
    <title>The Great War : Postcards : $title ";
($zoom == "2") ? print "(Double size)" : print "(Full Details)";
print "</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
    <base href='$base_url'>
  </head> 
<body> 
"; 


include("header.php");   

print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . " ";
($zoom == "2") ? print "(Double size)" : print "(Full Details)";
print "</p>";

/*
print '<p class="breadcrumbs">  
<a href="index.html">Home</a> &gt; <a href="postcards/">Postcards</a>  
	  &gt; Browse &gt; Detail  
</p>';
*/

print '<div class="content">'; 


$tamino->xslTransform($xsl_file, $xsl_params); 
$tamino->printResult();

// if logged in / have permissions
if ($_SESSION['authlevel']) { 	
  print "<p class='admin'>\n";
  print "Admin<br>\n";
  print "<a href='admin/postcards/modify.php?id=$id'>Modify description</a><br>\n";
  // are admin comments completely functional?
  print "<a href='admin/postcards/comment.php?id=$id'>Add a Comment</a><br>\n";
  // modify/delete comments -- only display if there are comments ?
  //print "<a href='admin/postcards/comment.php?id=$id'>Modify Comments</a><br>\n";
  print "</p>\n";
} else {
  // user comments not yet completely functional
  //  print "<a class='comment' href='postcards/comment.php?id=$id'>Add a Comment</a><br>\n";
}


print '</div>';

print '<div class="sidebar">';
include("postcards/nav.html");
include("searchbox.php");

print '</div>';

include("footer.html");

?>

</body>
</html>

