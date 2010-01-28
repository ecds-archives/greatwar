<?php

/* Note: the variable $siteurl must be set (by config.php) before including this file */


print "<p><img src='$base_url/images/topbanner.jpg' width='800' height='90' alt='The Great War 1914-1918'></p>";

if (isset($_SESSION["name"])) {
  // if logged in, display that fact
  print "<p class='login'>\n";
  print "Logged in as " . $_SESSION["name"];
  print "<br><a href='${base_url}admin/logout.php'>Logout</a>\n";
  print "</p>";

}

print "<table width='700' border='0' cellpadding='0' cellspacing='0' >
     <tr>
    	  <td><a href='${base_url}index.html'>Home</a></td>
          <td>&bull;</td>
	  <td><a href='${base_url}about.php'>About the Site</a></td> ";
print "   <td>&bull;</td>
	  <td><a href='${base_url}postcards/index.php'>Postcards</a></td>
          <td>&bull;</td>
	  <td><a href='${base_url}poetry/browse.php'>Poetry</a></td>
          <td>&bull;</td>
	  <td><a href='${base_url}links/browse.php'>Links</a></td>
          <td>&bull;</td>
	  <td><a href='${base_url}credits.php'>Credits</a></td> 
       </tr>
	  </table>
        <hr align='left'>
";
?>

