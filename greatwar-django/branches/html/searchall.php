<?php
include("config.php");	

print "<html>
  <head> 
    $csslink
    <title>The Great War : Keyword Search</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
    <base href='$base_url'>
  </head> 
<body> 
"; 

include_once("lib/xmlDbConnection.class.php");
include_once("lib/alinkCollection.class.php");
include_once("lib/mybreadcrumb.php");

$kw = $_GET["keyword"];			        // term to search for
$dosearch["poetry"] = $_GET["poetry"];		// which searches to do
$dosearch["postcards"] = $_GET["postcards"];
$dosearch["links"] = $_GET["links"];

$position = 1; $maxdisplay = 10;	// don't display too many results on search all page

// clean up input so explode will work properly
$kw = preg_replace("/\s+/", " ", $kw);  // multiple white spaces become one space
$kw = preg_replace("/\s$/", "", $kw);	// ending white space is removed
$terms = explode(" ", $kw);    // multiple search terms, divided by spaces

// base settings used by all three searches
$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'debug' => false);
$search = array("postcards", "poetry", "links");
foreach ($search as $s) {
  $args["coll"] = $tamino_coll[$s];	// tamino collection
  if ($s == "links") {		// links needs a different arg & is a different object type
    $args["keyword"] = $kw;
    $db[$s] = new aLinkCollection($args);    
  } else {
    $db[$s] =  new xmlDbConnection($args);
  }
}

// name of this page, and link back to current instance
$self = "searchall.php";
$selflink = "$self?keyword=$kw&poetry=" . $dosearch['poetry']. "&postcards=" . $dosearch['postcards'] . "&links=" . $dosearch['links'];

// xqueries for postcards & poetry (links works differently)
$query = $for = $return = $xsl_file =  $xsl_params = array();
$declare = 'declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction" ';
$for["postcards"] = 'for $a in input()/TEI.2/:text/body/p/figure ';
$for["poetry"] = 'for $a in input()/TEI.2/:text/body/div1/div2[@type="poem"] ';
//$where = "where tf:containsText(\$a, '$kw') ";
$where = "where";
if ($terms[0]) {
  foreach ($terms as $t) {
    if ($t != $terms[0]) { $where .= " and "; }
    $where .= " tf:containsText(\$a, '$t') ";
  }
}

$return["postcards"] = "return \$a";
$total["postcards"] = "<total> {count(" . $for["postcards"] . " $where return \$a)}</total> ";
$return["poetry"] = ' return <div2> {$a/@type} {$a/@id} {$a/@n} {$a/docAuthor} {$a/../docAuthor} ';
/* if ($terms[0]) {
   $return["poetry"] .= " {for \$l in \$a//l where "; 
   foreach ($terms as $t) { 
     if ($t != $terms[0]) { $return["poetry"] .= " or "; } 
     $return["poetry"] .= " tf:containsText(\$l, '$t') "; 
   } 
   $return["poetry"] .= " return \$l }  "; 
} */
// {for $l in $a//l where tf:containsText($l, ' . "'$kw'" . ') return $l }
$return["poetry"] .= '<linecount> { count($a//l) } </linecount> </div2> sort by (@n)';  
$total["poetry"] = "<total> {count(" . $for["poetry"] . " $where return \$a)}</total>"; 

foreach ($search as $s) {
  if ($s == "links") next;
  $query[$s] ="$declare <div>{(" . $for[$s]  . " $where " . $return[$s] . ")[position() >= 1 and position() <= 10] } " . $total[$s] . "</div>";  
}

$xsl_file["postcards"] = "figures.xsl";
$xsl_params["postcards"] = array("mode" => "thumbnail");
$xsl_file["poetry"] = "poetry.xsl";
$xsl_params["poetry"] = array("mode" => "search");

include("header.php");  
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>"; 

print '<div class="content">'; 

print "<p align='center'>Results for keyword <span class='term1'>$kw</span><ul class='horiz'>";

$first = true;
foreach ($search as $s) {
  if ($dosearch[$s] == "on") {
    if ($s != "links" ) { $db[$s]->xquery($query[$s], $position, $maxdisplay); }
    $li = "<li class='horiz'";
    if ($first) { $li .= " id='first' "; $first = false; }
    $li .= ">";
    print "$li<a href='$selflink#$s'>" . ucfirst($s) . "</a>: " . $db[$s]->count . "</a> match";
    if ($db[$s]->count != 1) { print "es"; }
    print "</li>";
  }
}
print "</ul></p>";

foreach ($search as $s) {
  if (($dosearch[$s] == "on") && ($db[$s]->count > 0)) {
    //    print "<hr class='floatright'><p><a name='$s'>" . ucfirst($s) . "</a></p>";
    print "<p class='searchdiv'><a name='$s'>" . ucfirst($s) . "</a></p>";
    if ($s == "links") {
      $db[$s]->printSummary();
    } else {
      if ($db[$s]->count > 10) {
	print "<p>Displaying results 1-10 of " . $db[$s]->count . ". ";
	print "See <a href='" . $s . "/search.php?keyword=$kw'>more results</a>.</p>";
      }
      $db[$s]->xslTransform($xsl_file[$s], $xsl_params[$s]); 
      //      $db[$s]->printResult(array($kw));
      $db[$s]->printResult($terms);
    }
  }
} 

print '</div>';

print '<div class="sidebar">';
include("searchbox.php");
print '</div>';
include("footer.html");

?>

</body>
</html>
