<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print "
<html>
  <head>
    $csslink
    <title>The Great War : Poetry : Search Results</title> 
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
    <base href='$base_url'> 
  </head> 
<body>
";

include_once("lib/xmlDbConnection.class.php");
include_once("lib/mybreadcrumb.php");

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['poetry'],
      	      'basedir' => $basedir,
	      'debug' => false,
	     );
$tamino = new xmlDbConnection($args);

// search terms
$kw = $_GET["keyword"];
$title = $_GET["title"];
$author = $_GET["author"];
$date = $_GET["date"];
$maxdisplay = $_GET["max"];
$position = $_GET["pos"];  // position (i.e, cursor)

// set a default maxdisplay
if ($maxdisplay == '') $maxdisplay = 25;
// if no position is specified, start at 1
if ($position == '') $position = 1;

// clean up input so explode will work properly
$kw = preg_replace("/\s+/", " ", $kw);  // multiple white spaces become one space
$kw = preg_replace("/\s$/", "", $kw);	// ending white space is removed
$terms = explode(" ", $kw);    // multiple search terms, divided by spaces

// construct the query, based on which terms are set
$declare ='declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction" ';
$for = ' for $a in input()/TEI.2/:text/body/div1/div2 ';
$where = 'where $a/@type="poem" ';
if ($terms[0]) {
  foreach ($terms as $t) {  $where .= " and tf:containsText(\$a, '$t') "; }
}
if ($title) { $where .= " and tf:containsText(\$a/head, '$title') "; }
// note: for now, must look for author field in two different places
if ($author) { $where .= " and (tf:containsText(\$a//docAuthor, '$author') or tf:containsText(\$a/../docAuthor, '$author')) " ; }
if ($date) { $where .= " and \$a/../docDate = '$date' "; }
$return = ' return <div2> {$a/@type} {$a/@id} {$a/@n} {$a/docAuthor} {$a/../docAuthor} ';
// if using keyword search, retrieve matching lines also
if ($terms[0]) {
   $return .= " {for \$l in \$a//l where ";
   foreach ($terms as $t) {
     if ($t != $terms[0]) { $return .= " or "; }
     $return .= " tf:containsText(\$l, '$t') ";
   }
   $return .= " return \$l }  ";
}
  //foreach ($terms as $t) {  $query .= " {for \$l in \$a//l where tf:containsText(\$l, '$t') return \$l }  "; }
//if ($kw) { $query .= " {for \$l in \$a//l where tf:containsText(\$l, '$kw') return \$l } "; }
$return .= ' <linecount> { count($a//l) } </linecount> </div2> sort by (@n)'; 
$total = "<total>{count($for $where return \$a)}</total>";

$end = $position + $maxdisplay - 1;	// end of current segment: start + max - 1 (e.g., display 1 - 20)
$query = "$declare <result> { ($for $let $where $return)[position() >= $position and position() <= $end] } $total </result>";
//$query = "$declare <result> { $for $where $return } $total </result>";

$xsl_params = array("mode" => "search");
$xsl_file = "poetry.xsl";

$tamino->xquery($query); 

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

print '<div class="content">'; 
print "<p align='center'>Found " . $tamino->count . " match";
if ($tamino->count != 1) { print "es"; }
print " </p>";

// if there are further pages of search results, link to them.
if ($tamino->count > $maxdisplay) {
  $result_links .= '<ul class="horiz">More results:';
  for ($i = 1; $i <= $tamino->count; $i += $maxdisplay) {
    if ($i == 1) {
      $result_links .= '<li class="horiz" id="first">'; 
    } else { 
      $result_links .= '<li class="horiz">';
    }
    // reconstruct the url and search terms
    $url = "poetry/search.php?keyword=$kw&title=$title&author=$author&date=$date&maxdisplay=$maxdisplay";
    // now add the key piece: the new position
    $url .= "&pos=$i";
    if ($i != $position) {
      $result_links .= "<a href='$url'>";
      // url should be based on current search url, with new position defined
    }
    $j = min($tamino->count, ($i + $maxdisplay - 1));
    // special case-- last set only has one result
    if ($i == $j) {
      $result_links .= "$i";
    } else {
      $result_links .= "$i - $j";
    }
    if ($i != $position) {
      $result_links .= "</a>";
    }
    $result_links .= "</li>";
  }
    $result_links .= "</ul>";
}

print "$result_links<p>";


$tamino->xslTransform($xsl_file, $xsl_params);
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
