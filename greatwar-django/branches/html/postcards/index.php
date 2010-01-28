<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");

print " 
<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'>
<html>
  <head> 
    <title>The Great War : Postcards</title>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <script language='Javascript' type='text/javascript' src='../toggle-list.js'></script>
    <base href='$base_url'>
    $csslink
  </head> 
<body> 
"; 

/* NOTE: IE (6.0) seems to choke if javascript is included using any other syntax than the above. */

include_once("lib/xmlDbConnection.class.php");
include_once("lib/interpGrp.class.php");
include_once("lib/mybreadcrumb.php");

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
              'basedir' => $basedir,
	      'debug' => false,
	      );
$tamino = new xmlDbConnection($args);
// xquery & xsl for category labels 
$cat_query = 'for $a in input()/TEI.2/:text/back/:div//interpGrp 
return $a'; 
$cat_xsl = "interp.xsl";
$cat_params = array("showtitle" => 0);
// xquery for total count of postcards
$total_query = "<total>{count(input()/TEI.2/:text/body/p/figure)}</total>";
$tamino->xquery($total_query);		// get count of postcards loaded
$count = $tamino->count;
// get a random index between 1 and the total number of postcards
$rand_index = rand(1, $count);
$random_pcard = "for \$a in input()/TEI.2/:text/body/p/figure[$rand_index] return \$a";
$pcard_xsl = "figures.xsl";
$pcard_params = array("mode" => "thumbnail");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";
print '<div class="content">';
print '<p>';
// display a random postcard  
print '<div class="random_postcard">';
$tamino->xquery($random_pcard);
$tamino->xslTransform($pcard_xsl, $pcard_params);
$tamino->printResult();
print '</div>';

print '<p>For more information about the postcards, read <a href="about.php">about  this project</a>.</p> 
<p> 
There are several different ways to view the postcards: 
<ul> 
<li><a href="postcards/browse.php">Browse</a> - browse through all <b>' . $count . '</b> postcards<br>
View thumbnails with titles, or thumbnails with a brief description<br> 
(not advisable for slow connections) </li>';


print '<li>Browse by category
<div class="categories">';  
$tamino->xquery($cat_query);
$tamino->xslTransform($cat_xsl, $cat_params);
$tamino->printResult();
print '</div>
</li>
<li><a href="postcards/searchform.php">Search</a> the postcards by keyword, title, description, and category
</li>
</ul>

<p>Images of the postcards are available in three sizes:</p>
<ul>
<li>Thumbnail - browse pages & search results<br>
(may be viewed with titles only, or with brief descriptions)
</li>
<li>roughly realsize - view an individual postcard with full details</li>
<li>roughly doublesize - linked from individual postcard view</li>
</ul>
</div>';

print '<div class="sidebar">';
include("postcards/nav.html");
include("searchbox.php");
print '</div>';
include("footer.html");

?>

</body>
</html>

