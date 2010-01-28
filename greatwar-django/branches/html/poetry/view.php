<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

include_once("lib/xmlDbConnection.class.php");
include_once("lib/mybreadcrumb.php");

$id = $_GET['id'];
$self = "view.php";
$selflink = "$base_url" . "poetry/" . $self . "?id=$id";

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
      	      'coll' => $tamino_coll['poetry'],
      	      'basedir' => $basedir,
	      'debug' => false,
	     );
$tamino = new xmlDbConnection($args);
$query = 'declare namespace xf="http://www.w3.org/2002/08/xquery-functions"
declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction"
for $a in input()/TEI.2/:text/body/div1/div2
let $root := xf:root($a)
let $docname := tf:getDocname($root)
let $titlestmt := $root/TEI.2/teiHeader/fileDesc/titleStmt
let $bibl := $root/TEI.2/teiHeader/fileDesc/sourceDesc/bibl
where $a/@id = ' . "'$id'" . '
return <div id="{$docname}">
<teiHeader>
<fileDesc> {$titlestmt}
<sourceDesc>
  {$bibl}
</sourceDesc>
</fileDesc>
</teiHeader>
{$a}
<siblings>
{ for $s in $root/TEI.2/:text/body/div1/div2
return <div2> {$s/@id} {$s/@n} {$s/docAuthor} </div2> }
</siblings>
</div>';

$xsl_file = "poetry.xsl";
$xsl_params = array("mode" => "poem", "selflink" => $selflink);
$tamino->xquery($query, $pos, $maxdisplay); 
$title = $tamino->findNode("head");
$title = preg_replace("/<hi TEIform=\"hi\" rend=\"\w*\">/", "", $title);
$title = str_replace("</hi>", "", $title);

print "<html>
  <head> 
    $csslink
    <title>The Great War : Poetry : Poem - $title</title> 
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
    <base href='$base_url'> 
  </head> 
<body> 
";


include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . " - \"$title\"</p>";


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
