<?php
$mydir = getcwd();
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print "<html>
  <head> 
    $csslink
    <title>The Great War : Poetry : Browse</title> 
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
    <base href='$base_url'>
  </head> 
<body>
";

include_once("lib/xmlDbConnection.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['poetry'],
      	      'basedir' => $basedir,
     	      'debug' => false,
	       );
$tamino = new xmlDbConnection($args);
$query = 'declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction"
declare namespace xf="http://www.w3.org/2002/08/xquery-functions"
for $a in input()/TEI.2/teiHeader/fileDesc/titleStmt
let $docname := tf:getDocname(xf:root($a))
return <div id="{$docname}"> {$a} </div> sort by (titleStmt/title)'; 

$xsl_file = "poetry.xsl";
$xsl_params = array("mode" => "browse");

$tamino->xquery($query, $pos, $maxdisplay); 

print '<div class="content">';
$tamino->xslTransform($xsl_file, $xsl_params);
$tamino->printResult();
print "</div>";

print '<div class="sidebar">';
include("nav.html");
include("searchbox.php");
print "</div>";

include("footer.html");

?>
</body>
</html>
