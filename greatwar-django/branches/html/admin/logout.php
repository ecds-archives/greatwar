<?php

include("../config.php");	


session_start();

// Unset all of the session variables.
$_SESSION = array();

// If it's desired to kill the session, also delete the session cookie.
// Note: This will destroy the session, and not just the session data!
if (isset($_COOKIE[session_name()])) {
   setcookie(session_name(), '', time()-42000, '/');
}
// Finally, destroy the session.
session_destroy();

print " 
<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'>
<html>
  <head> 
    <title>The Great War : Administration : Logout</title>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <base href='$base_url'>
    $csslink
  </head> 
<body> 
"; 

include_once("lib/taminoConnection.class.php");
include_once("lib/mybreadcrumb.php");


include("header.php");
print "<p class='breadcrumbs'>" . $breadcrumb->show_breadcrumb() . "</p>";


print "<p>You are now logged out.</p>";
print "<p>You must close your browser window to log out completely.</p>";

?>