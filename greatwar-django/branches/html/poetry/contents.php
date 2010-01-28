<?php
chdir("..");	// behave as if we were in the root directory, because all paths are relative to it (xsl, etc.)
include("config.php");	

include_once("lib/xmlDbConnection.class.php");
include_once("lib/mybreadcrumb.php");

$id = $_GET['id'];

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['poetry'],
       	      'basedir' => $basedir,
      	      'debug' => false,
	      );
$tamino = new xmlDbConnection($args);
$query = 'declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction"
declare namespace xf="http://www.w3.org/2002/08/xquery-functions"
for $a in input()/TEI.2
let $docname := tf:getDocname(xf:root($a))
let $titlestmt := $a/teiHeader/fileDesc/titleStmt
let $fileDesc := $a/teiHeader/fileDesc
let $bibl := $a/teiHeader/fileDesc/sourceDesc/bibl
where $docname = ' . "'$id'" . '
return <div>
<teiHeader>
{$fileDesc}
</teiHeader>
{ for $fdiv in $a/:text/front/div1
return <front><div1> {$fdiv/@id} {$fdiv/@n} {$fdiv/@type} {$fdiv/head} </div1></front> }
{ for $div1 in $a/:text/body/div1 
   return <div1> {$div1/@id} {$div1/@n} {$div1/@type}
{$div1/head} {$div1/p[1]}
    {for $div2 in $div1/div2 
      return <div2> {$div2/@id} {$div2/@n} {$div2/@type} 
           {$div2/docAuthor}
        { for $div3 in $div2/div3 return <div3>{$div3/@id} {$div3/@n} {$div3/@type}</div3> }
        </div2> }
   </div1> }
</div>';

$xsl_file = "poetry.xsl";
$xsl_params = array("mode" => "contents");
$tamino->xquery($query, $pos, $maxdisplay);  
$title = $tamino->findNode("title");
$t = explode(":", $title, 2);
$title = $t[0];
$subtitle = $t[1];

// metadata information for cataloging
$header_xsl1 = "teiheader-dc.xsl";
$header_xsl2 = "dc-htmldc.xsl";
// copy xsl_result to xml object for a second xsl transform

print "<html>
  <head>
    $csslink
    <title>The Great War : Poetry : Contents - $title</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>"; 
$tamino->xslTransform($header_xsl1);
$tamino->xslTransformResult($header_xsl2);
$tamino->printResult();
//restore tamino xml
print "<base href='$base_url'> 
  </head> 
<body>
";

/* Contents for a single volume of poetry */


include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb();
print " - <i>$title : $subtitle</i>";
print "</p>";

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
