<?php

/* Note: assumes that base_path is set, presumably by config.php */

include_once("lib/breadcrumb.class.php");

// set up a breadcrumb object to be used by all wwi pages

$breadcrumb = new breadcrumb;
$breadcrumb->homepage = '';         //don't display webserver root as home
$breadcrumb->dirformat = 'ucwords'; // Show the names in this style (first letter of each word upper case)
$breadcrumb->showfile = true;       // show the file name in the path
$breadcrumb->hideFileExt = true;    // don't show filename extension

// development version:
$breadcrumb->changeName = array('wwiweb'=>'Home');
// production version:
//$breadcrumb->changeName = array('greatwar'=>'Home');
$breadcrumb->changeFileName = array("$base_path/searchall.php" => "Keyword Search",
				    "$base_path/postcards/searchform.php" => "Advanced Search",
  				    "$base_path/postcards/search.php" => "Search Results",
  				    "$base_path/poetry/searchform.php" => "Advanced Search",
 				    "$base_path/poetry/search.php" => "Search Results",
     				    "$base_path/poetry/front.php" => "Front Matter",
      				    "$base_path/links/searchform.php" => "Search",
       				    "$base_path/links/do_add.php" => "Process New Link",
      				    "$base_path/admin/links/do_add.php" => "Process New Link",
       				    "$base_path/admin/links/do_approve.php" => "Process Approval",
       				    "$base_path/admin/links/do_modify.php" => "Process Modification",
       				    "$base_path/admin/links/test.php" => "Test Links",
       				    "$base_path/admin/links/do_modify.php" => "Process Modification",
				  );

$breadcrumb->changeDirLink = array("$base_path/postcards/" => "index.php",
				   "$base_path/poetry/" => "browse.php",
				   "$base_path/links/" => "browse.php",
				   "$base_path/admin/links/" => "view.php",
   				   "$base_path/admin/" => "login.php",
				   );

/* TEMPORARY:
  This mapping will change when the site moves to a more permanent home
*/
$breadcrumb->removeDirs = array('rebecca');

?>