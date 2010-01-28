<?php

/* Configuration settings for entire site */

// pick up login/authorization information
session_start();

// set level of php error reporting --  ONLY display errors
// (will hide ugly warnings if databse goes offline/is unreachable)
//error_reporting(E_ERROR);		// for production
//error_reporting(E_ERROR | E_PARSE);    // for development

// root directory and url where the website resides
// development version
$basedir = "/home/httpd/html/rebecca/greatwar";
$server = "reagan.library.emory.edu";
$base_path = "/rebecca/greatwar";
$base_url = "http://$server$base_path/";

// root directory and url where the website resides
// production version
/* $basedir = "/home/httpd/html/cti/greatwar";
$server = "cti.library.emory.edu";
$base_path = "/greatwar";
$base_url = "http://$server$base_path/";
*/

// add basedir to the php include path (for header/footer files and lib directory)
//set_include_path(get_include_path() . ":" . $basedir . ":" . "$basedir/lib" . ":" . "$basedir/content");

//shorthand for link to main css file
$cssfile = "wwi.css";
$csslink = "<link rel='stylesheet' type='text/css' href='$base_url/$cssfile'>";

/* tamino settings common to all pages
   Note: all pages use same database, but there are three different collections
 */
$tamino_server = "vip.library.emory.edu";
$tamino_db = "WW1";
/* define all these in one place so it is easy to change for testing */
$tamino_coll["poetry"] = "poetry";
$tamino_coll["links"] = "links";
$tamino_coll["postcards"] = "postcards";
//$tamino_coll["postcards"] = "postcards-test";
?>
