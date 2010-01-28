<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

print "<html>
  <head> 
    $csslink
    <title>The Great War : Poetry : Poets</title> 
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
    <base href='$base_url'>
  </head> 
<body>
";

include_once("lib/xmlDbConnection.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$self = "poetry/poet.php";
$pos = $_GET["position"];
$maxdisplay = $_GET["max"];
if (isset($pos)) {} else {$pos = 1;}
if (isset($maxdisplay)) {} else { $maxdisplay = 75; }

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['poetry'],
      	      'basedir' => $basedir,
     	      'debug' => false,
	       );
$tamino = new xmlDbConnection($args);

$query = 'declare namespace xf="http://www.w3.org/2002/08/xquery-functions"
declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction"
for $a in input()/TEI.2/:text/body//docAuthor
let $div := $a/..
let $docname := tf:getDocname(xf:root($a))
where $div/docAuthor/@n
return <div docname="{$docname}">
{$div/@n}
{$div/@id}
{$div/@type}
{$a}
{for $div2 in $div/div2
   return <div2> {$div2/@id} {$div2/@n} {$div2/@type} {$div2/docAuthor} </div2> }
</div> sort by (docAuthor/@n, @n)';  


$xsl_file = "poetry.xsl";
$xsl_params = array("mode" => "poetbrowse", "selflink" => $self, "max" => $maxdisplay, "position" => $pos);

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
