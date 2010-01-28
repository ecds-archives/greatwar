<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print "<html>
  <head> 
    $csslink
    <title>The Great War : Postcards : Search Results</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
    <base href='$base_url'>
  </head> 
<body> 
"; 

include_once("lib/xmlDbConnection.class.php");
include_once("lib/interpGrp.class.php");
include_once("lib/mybreadcrumb.php");

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => 'postcards',
	      'basedir' => $basedir,
	      'debug' => false,
	      );
$tamino = new xmlDbConnection($args);
$ig = new interpGrp($args);

// search terms
$kw = $_GET["keyword"];

$title = $_GET["title"];
$figdesc = $_GET["figdesc"];
// categories (how not to hard code this?)
$nat = $_GET["nationality"];
$mil = $_GET["military"];
$hf = $_GET["homefront"];
$con = $_GET["content"];
$time = $_GET["time-period"];		// FIXME: errors with the space
$category = array($nat, $mil, $hf, $con);
// clean up input so explode will work properly
if ($kw) {
  $kw = preg_replace("/\s+/", " ", $kw);  // multiple white spaces become one space
  $kw = preg_replace("/\s$/", "", $kw);	// ending white space is removed
  $kwterms = explode(" ", $kw);    // multiple search terms, divided by spaces
} else { $kwterms = array(); }
$terms = array();
if ($title) { array_push($terms, $title); }
if ($figdesc) { array_push($terms, $figdesc); }
if ($kw) { array_push($terms, $kwterms); }
$pos = $_GET["position"];
if (isset($pos)) {} else {$pos = 1;}

$desc = "yes";		// for now - default to showing descriptions

($desc == "yes") ? $mode = "thumbdesc" : $mode = "thumbnail";
$xsl_params = array("mode" => $mode);
$cat_params = array("desc" => $desc);

$firstcond = false;  // false =  this is the first condition; true = print 'and'

$declare ='declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction" ';
$for = 'for $a in input()/TEI.2/:text/body/p/figure ';
$let = 'let $b := input()/TEI.2/:text/back/:div//interpGrp ';
$where = 'where ';
if ($title) {
  $where .= " tf:containsText(\$a/head, '$title') ";
  ($desc == "yes") ? $mode = "thumbdesc" : $mode = "thumbnail";
  $firstcond = true;
}
if ($figdesc) {
  if ($firstcond) { $where .= " and "; }
  $where .= " tf:containsText(\$a/figDesc, '$figdesc') ";
  $firstcond = true;
}
// keyword search
foreach ($kwterms as $t) {
  if ($t != '') {
    if ($firstcond) { $where .= " and "; }
    $where .= " tf:containsText(\$a, '$t') ";
    $firstcond = true;
  }
}
foreach ($category as $c) {
  if (($c != "null") && ($c != '')) {  	// if null, skip selection
    if ($firstcond) { $where .= " and "; }
    $where .= "tf:containsText(\$a/@ana, '$c') ";
    $firstcond = true;
  }
}
$return .= 'return <div> { $a } {$b} ' . "<total>{ count($for $where return \$a) }</total> </div>";
$query = "$declare $for $let $where $return";


$xsl_file = "figures.xsl";


$maxdisplay = 10;
$tamino->xquery($query, $pos, $maxdisplay); 

include("header.php");

print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";


print '<div class="content">'; 

$searchterms = array();

print "<p class='postcardnav'>Search results for ";
// FIXME: maybe put this in an unordered list?  might be cleaner...
// also make text smaller, as it is in browse.php...  highlight search terms to match text?
if ($title) { array_push($searchterms, "'$title' in title"); }
if ($figdesc) { array_push($searchterms, "'$figdesc' in figure description"); }
foreach ($category as $c) {
  if (($c != "null") && ($c != '')) {  	// if null, skip
       array_push($searchterms, $ig->group($c) . " = " . $ig->name($c));
  }
}

if ($kw) {
  $kwstring = "keyword"; 
  if(count($kwterms) > 1) { $kwstring .= "s"; }
  $kwstring .= ": " . implode($kwterms, ", ");
  array_push($searchterms, "$kwstring"); 
} 


// print out search terms with comma and space between
print implode($searchterms, ", ");

print "</p>";
print "<p>Displaying postcard";
($tamino->quantity > 1) ? print "s " : print " ";
print $tamino->position;
if ($tamino->position != $tamino->quantity) { print " - " . ($tamino->quantity + $tamino->position - 1); }
print " of " . $tamino->count . "</p>"; 

// links to more results
if ($tamino->count > $maxdisplay) {
  $result_links .= 'More postcards:';
  $first = true;
  for ($i = 1; $i <= $tamino->count; $i += $maxdisplay) {
    if ($i == $pos) { next; }	// skip current set of results
    else {
      // construct the url, maintaining all parameters
      $url = "postcards/browse.php?";
      if ($desc) { $url .= "&desc=$desc"; }
      if ($cat) { $url .= "&cat=$cat"; }
      // now add the key piece: the new position
      $url .= "&position=$i";
      $li = "<li class='horiz' ";
      if ($first) { $li .= "id='first'"; $first = false;}
      $li .= ">";
      $result_links .= "$li";
      $result_links .= " <a href='$url'>";
      $j = min($tamino->count, ($i + $maxdisplay - 1));
      // special case-- last set only has one result
      if ($i == $j) { $result_links .= "$i"; }
      else { $result_links .= "$i - $j"; }
      $result_links .= "</a> ";
      $result_links .= "</li>";
    }
  }
}

print $result_links;


$tamino->xslTransform($xsl_file, $xsl_params);
//$tamino->xslTransform($xsl_file);

// FIXME: why is highlighting not working properly?
$tamino->printResult($terms);

print '</div>';

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print '</div>';

include("footer.html");

?>

</body>
</html>
