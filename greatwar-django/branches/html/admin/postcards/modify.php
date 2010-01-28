<?php
include("../../config.php");	

print "<html>
  <head>
    $csslink
    <title>The Great War : Admin : Postcards : Modify Description</title>
    <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'> 
  </head>
<body>
";

// name of the current file (for links that display same content with different options)
$self = "modify.php";

include_once ("lib/figDesc.class.php");
include_once("lib/mybreadcrumb.php");

include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";

$entity = $_GET["id"]; 


print '<div class="content"> 
          <h3>Modify Postcard Description</h3>';

if (isset($entity)) {

$args = array('host' => $tamino_server,
	      'db' => $tamino_db,
	      'coll' => $tamino_coll['postcards'],
	      'entity' => $entity,
	      'imgpath' => 'http://beck.library.emory.edu/greatwar/postcard-images/thumbnail/',
	      'debug' => false);
$desc = new figDesc($args);
$desc->taminoGetRecord();
$desc->printform("do_modify.php");

/* NOTE: weird tamino/TEIform attribute problem still in play
  ...  possible solution: allow limited html input, convert to tei & set
  TEIform attributes */
/* print '<hr><p><b>Allowed tags for formatting:</b><br>
&lt;lb/&gt; : line break<br>
&lt;hi rend="mode"&gt;text&lt;/hi&gt; where mode is one of: italic, bold, underline, smallcaps
</p>';
 print "<p><i>Note: for other formatting needs, please contact Rebecca.</i></p>";
*/

print '<hr><p><b>Allowed tags for formatting:</b><br> <i>Note: at this time,
due to technical issues, no formatting tags are allowed.  Hopefully, this
feature will be available soon.</i></p>';
 
 
}  else {
  print "<p>Error! No postcard was specified.</p>\n";
}

print "</div>";
print '<div class="sidebar">'; 
include("nav.html"); 
include("searchbox.php"); 
print '</div>'; 
include("footer.html"); 

print "</body>
</html>";

?>
