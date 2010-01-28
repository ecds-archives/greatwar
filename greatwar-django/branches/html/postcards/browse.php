<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print " 
<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'>
<html>
  <head> 
    <title>The Great War : Postcards : Thumbnails</title>
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

include("header.php");

print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb();
print " (Thumbnails";
if ($desc == "yes") { print " with descriptions"; }
print ")</p>";


$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
              'basedir' => $basedir,
	      'debug' => false,
	      );
$tamino = new xmlDbConnection($args);

$cat = $_GET["cat"];		// optionally limit postcards by category
$desc = $_GET["desc"];
$pos = $_GET["position"];
$maxdisplay = $_GET["max"];
if (isset($pos)) {} else {$pos = 1;}
if (isset($maxdisplay)) {}
else if ($desc == "yes") { $maxdisplay = 25; }
else { $maxdisplay = 50; }

($desc == "yes") ? $mode = "thumbdesc" : $mode = "thumbnail";
$xsl_params = array("mode" => $mode, "authlevel" => $_SESSION['authlevel']);
$cat_params = array("desc" => $desc, "max" => $maxdisplay);

/*
$query ='declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction"
for $a in input()/TEI.2/:text/body/p/figure '; 
if ($cat) { $query .= "where tf:containsText(\$a/@ana, '$cat') "; } 
$query .= 'return $a';
*/

// FIXME: this query won't allow for using the cursor to limit # of figures displayed
/* $query ='declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction"';
$query .= '<div> { for $a in input()/TEI.2/:text/body/p/figure ';   
if ($cat) { $query .= "where tf:containsText(\$a/@ana, '$cat') "; }    
$query .= 'return  $a } ';
$query .= '{ for $b in input()/TEI.2/:text/back/:div//interpGrp return $b }</div>';
*/ 

$declare ='declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction" ';
$for = 'for $a in input()/TEI.2/:text/body/p/figure ';
$let = 'let $b := input()/TEI.2/:text/back/:div//interpGrp ';
if ($cat) { $where = "where tf:containsText(\$a/@ana, '$cat') "; }
else { $where = ""; }
$return = "return <div> { \$a } <total>{ count($for $where return \$a) }</total> {\$b} </div>";
$sort = "sort by (figure/head)";
//$query = "$declare $for $let $where $return $sort";
$query = "$declare $for $let $where $return";

$xsl_file = "figures.xsl";

$tamino->xquery($query, $pos, $maxdisplay); 

// xquery & xsl for category labels 
$cat_query = 'for $a in input()/TEI.2/:text/back/:div//interpGrp 
return $a'; 
$cat_xsl = "interp.xsl"; 



// display options : show/hide descriptions
print "<p>";
if ($tamino->count) {		// only display navigation information if there are results (query succeeded)
  if ($desc == 'yes') {
    print "<a href='postcards/browse.php?desc=no&cat=$cat&max=$maxdisplay'>Hide descriptions</a>";
  } else {
    print "<a href='postcards/browse.php?desc=yes&cat=$cat&max=$maxdisplay'>Show descriptions</a>";
  }
  // if a category is selected, give option to revert to all
  if ($cat) { print " | <a href='postcards/browse.php?desc=$desc&max=$maxdisplay'>View all</a>";
  }
  print "</p>";
}


// FIXME: add a special case for count = 1 ?
// FIXME: add a case for count = 0 -> no matches
if ($tamino->count > 0) {

  print '<div class="content">'; 

  print "<table class='postcardnav'><tr><td>";
print "<p>Displaying postcards " . $tamino->position . " - " . ($tamino->quantity + $tamino->position - 1) . " of " . $tamino->count;
if ($cat) {
  $args["id"] = $cat;
 $ig = new interpGrp($args);
 print " for <b>" . $ig->group($cat) . " - " . $ig->name($cat) . "</b>";
} 
print "</p>";

// links to more results
if ($tamino->count > $maxdisplay) {
  $result_links .= 'More postcards:';
  $first = true;
  $maxlinks = 7;	// number of result sets to link to
  for ($i = 1; $i <= $tamino->count; $i += $maxdisplay) {
    //    if ($i > ($maxlinks * $maxdisplay))  { next; }
    // give some indication of skipping, link to last two or three?

      // construct the url, maintaining all parameters
      $url = "postcards/browse.php?max=$maxdisplay";
      if ($desc) { $url .= "&desc=$desc"; }
      if ($cat) { $url .= "&cat=$cat"; }
      // now add the key piece: the new position
      $url .= "&position=$i";
      $li = "<li class='horiz' ";
      if ($first) { $li .= "id='first'"; $first = false;}
      $li .= ">";
      $result_links .= "$li";
      if ($i != $pos) { $result_links .= "<a href='$url'>"; }	// link all but current set
      $j = min($tamino->count, ($i + $maxdisplay - 1));
      // special case-- last set only has one result
      if ($i == $j) { $result_links .= "$i"; }
      else { $result_links .= "$i - $j"; }
      if ($i != $pos) { $result_links .= "</a>"; }
      $result_links .= "</li>";

  }
}

 
print $result_links;

 print "</td><td class='maxdisplay'>"; 
 //print "<table class='maxdisplay'><tr><td>";
print " Postcards per page:
<form action='postcards/browse.php'>
<select name='max'>";
foreach (array(5,10,15,20,25,50) as $i) {
  ($i == $maxdisplay) ? $status = " selected" : $status = "";
  print "<option value='$i'$status>$i</option> ";
}
print "</select>
<input type='hidden' name='desc' value='$desc'>
<input type='hidden' name='cat' value='$cat'>
<input type='submit' value='Go'>
</form>";
//print "</td></tr></table>";
// table maxdisplay 

 print "</td></tr></table>";
 


$tamino->xslTransform($xsl_file, $xsl_params); 
//$tamino->xslTransform($xsl_file);
$tamino->printResult();

}  // end if tamino->count > 0


// print result links again at bottom
print "<p><table class='postcardnav'><tr><td>";
print $result_links;
print "</td></tr></table></p>";

print '</div>';

print '<div class="sidebar">';
include("postcards/nav.html");
include("searchbox.php");

print '<div class="categories">';
$tamino->xquery($cat_query);
$tamino->xslTransform($cat_xsl, $cat_params);
$tamino->printResult();

print '</div>';

print '</div>';

include("footer.html");


?>

</body>
</html>
