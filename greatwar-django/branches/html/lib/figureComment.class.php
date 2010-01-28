<?php

include_once("taminoConnection.class.php");

class figureComment {

  var $tamino;
  var $imgpath;

  // relevant figure components
  var $entity;
  var $title;

  var $comment;
  var $date;

  // comment components
  /*  var $id;
  var $comment;  // (actual text of the comment)
  var $name;
  */

  // Constructor 
  function figureComment($argArray) {
    // pass host/db/collection settings to tamino object
    $this->tamino = new taminoConnection($argArray);
    $this->imgpath = $argArray['imgpath'];
    
    $this->entity = $argArray['entity'];
    $this->title = $argArray['title'];

    $this->comment = array();
    if (isset($argArray['comment']) || isset($argArray['id'])) {
      // also could be ... date, name, [entity]
      $mycom = new comment($argArray);
      array_push($this->comment, $mycom);
    }

    /* If date is not set, initialize date value to today.  
       Format is: 2004-04-09 4:13:00 PM */
    if (!($this->date)) {
      $this->date = date("Y-m-d g:i:s A");
    }

    $this->cleanInput();
  }


   // generate an xquery for the specified mode, based on current variable settings
  function xquery ($mode, $auth = 'admin') {	// auth = user or admin
    $declare = 'declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction"
		declare namespace xf="http://www.w3.org/2002/08/xquery-functions"';
    $for['admin'] = 'for $a in input()/TEI.2/:text/body/p/figure ';
    $for['user'] = 'for $a in input()/TEI.2/:text/body/div1';
    // user add query must be relative to containing node; all others are not
    if ($mode != 'add') { $for['user'] .= "/p"; }
    $let['admin'] = '';
    $let['user'] = 'let $docname := tf:getDocname(xf:root($a))';
    $condition['admin'] = '$a/@entity = "' . $this->entity . '"';  
    $condition['id'] = '$a/@id = "' . $this->comment[0]->id . '" ';  
    $condition['user'] = '$docname = "postcard-comments.xml"';
    //    $return['admin'] = 'return <figure>{$a/head}</figure>';
    $return['admin'] = 'return <comment> {$a/p} <figure>{$a/head} {$a/@entity}</figure></comment>';
    $return['user'] = 'return $a';
    $insert['admin'] = 'do insert ' . $this->XMLstring($auth) . ' preceding $a/figDesc';
    $insert['user'] = 'do insert ' . $this->XMLstring($auth) .  ' following $a/p[last()]';
    $replace['admin'] = 'do replace $a/p with ' . $this->XMLstring($auth);
    $delete['admin'] = 'do delete $a/p';
    $delete['user'] = 'do delete $a';
 
    switch ($mode):
  case 'getRecord': 
    // xquery to retrieve a record by figure entity
    $query = "$declare $for[$auth] $let[$auth] where $condition[$auth] and " . $condition['id'] . "$return[$auth]"; 
    break;
  case 'add':
    // xquery to add a new comment to a figure
    $query = "$declare update $for[$auth] $let[$auth] where $condition[$auth] $insert[$auth]";
    break;
  case 'modify':
    // xquery to update an existing comment (admin only)
    $query = "update $for[$auth] $let[$auth] where " . $condition['id'] . " $replace[$auth]";
  case 'delete':
    // xquery to delete an existing comment 
    $query = "$declare update $for[$auth] $let[$auth] where $condition[$auth] and " . $condition['id'] . " $delete[$auth]";
    break;
  case 'figureInfo':
    // xquery to retrieve figure title (e.g., for a new comment)
    $query = 'for $a in input()/TEI.2/:text/body/p/figure
	      where $a/@entity = "' . $this->entity . '"
	      return <figure>{$a/head}</figure>';
    break;
  case 'UserComments':
    // xquery to retrieve all user-submitted comments for approval
    $query = "$declare $for[$auth][@n='comment'] $let[$auth] where $condition[$auth] return \$a";
    break;
   endswitch;

   /*
This xquery works for submitting a user comment to the holding-area file!
(FIXME: maybe get rid of the div1 in the skeleton file? is it necessary?)

declare namespace tf="http://namespaces.softwareag.com/tamino/TaminoFunction"
declare namespace xf="http://www.w3.org/2002/08/xquery-functions"
update for $a in input()/TEI.2/:text/body/div1
let $docname   := tf:getDocname(xf:root($a))
where $docname = 'postcard-comments.xml'
do insert <p id='rlsktest'><date>10-01-2004</date><name>rlsk</name>testing xquery for user submission</p> following $a/p[position() = last()]
   */

   return $query;
  }

  // retrieve a comment from tamino by entity value
  function taminoGetComment($auth = "user") {	// auth = user, admin
    $path['user'] = "ino:response/xq:result";
    $path['admin'] = "ino:response/xq:result/comment/p";
    $rval = $this->tamino->xquery($this->xquery('getRecord', $auth));
    if ($rval) {
      print "<p>figureComment Error: failed to retrieve comment details from Tamino.<br>";
      print "(Tamino error code $rval)</p>";
      $this->description = "";		// load failed; set to null string
    } else {            // xquery succeeded 	
      $xmlRecord = $this->tamino->xml->getBranches($path[$auth]);
      if ($xmlRecord) {
	// process all of the branches
	$this->CommentInit($xmlRecord);
      }
    }
  }

  // retrieve figure information from tamino by entity - for a new comment
  function getFigureInfo() {
    $rval = $this->tamino->xquery($this->xquery('figureInfo'));
    if ($rval) {
      print "<p>figureComment Error: failed to retrieve figure details from Tamino.<br>";
      print "(Tamino error code $rval)</p>";
      $this->description = "";		// load failed; set to null string
    } else {            // xquery succeeded
      $val = $this->tamino->xml->getTagContent("ino:response/xq:result/figure/head");
      if ($val) { $this->title = $val; }
    }
  }

  function display () {
    print "<table class='figDesc'>";
    print "<tr><th colspan='2'>$this->title</th></tr>";
    foreach ($this->comment as $c) {
      print "<tr><td>";
      if ($this->imgpath) {
        print "<img src='" . $this->imgpath . $c->entity . ".jpg' alt='postcard thumbnail'>";
      }
      print "</td><td>";
      $c->printSummary();
      print "</td></tr>";
    }
    print "</td></table>";
  }

  function printform ($action) {
    print "<form action='$action' method='post'>\n";
    print "<input type='hidden' name='title' value='$this->title'>";
    print "<input type='hidden' name='entity' value='$this->entity'>";
    print "<table  class='figDesc'>";
    print "<tr><th colspan='2'>$this->title</th></tr>";
    print "<tr><td valign='middle'>";
    if ($this->imgpath) { print "<img src='" . $this->imgpath . $this->entity . ".jpg'>";  }
    print "</td>";
    if (count($this->comment) > 0) {
      foreach ($this->comment as $c) {
        print "<td>Comments:<br>\n";
        print "<textarea cols='80' rows='15' name='comment'>" . $c->text . "</textarea>\n";
        print "<tr><td>Name:</td>\n";
        print "<td><input type='text' name='name' size='80' value='$c->name'></td></tr>\n";
        print "<tr><td>Date:</td>\n";
        print "<td><input type='text' name='date' size='80' value='$c->date'></td></tr>\n";
      }
    } else {
      /* new comment - no default values except date : use today's date */
        print "<td>Comments:<br>\n";
        print "<textarea cols='80' rows='15' name='comment'></textarea>\n";
        print "<tr><td>Name:</td>\n";
        print "<td><input type='text' name='name' size='80'></td></tr>\n";
        print "<tr><td>Date:</td>\n";
        print "<td><input type='text' name='date' size='80' value='$this->date'></td></tr>\n";
    }
    print "</table>";
    print "<input type='reset'>";
    print "<input type='submit' name='preview' value='Preview'>";
    print "<input type='submit' name='submit' value='Submit'>";
    print "</form>\n";
  }


  // add a comment to a figure in tamino
  function taminoAdd ($auth = "user") {  // user or admin
    $rval = $this->tamino->xquery($this->xquery('add', $auth));
    if ($rval) {       // tamino error
      if ($auth == "admin") {			// different feedback for user/admin
        print "<p>Failed to add comment to figure.</p>";
      } else if ($auth == "user") {
        print "<p>Comment submission failed.</p>";
      }
    } else {
      if ($auth == "admin") {
        print "<p>Successfully added comment to figure.</p>";
      } else if ($auth == "user") {
	print "<p>Succesfully submitted comment.</p>";
      }
    }
  }

  function getUserComments () {
    $rval = $this->tamino->xquery($this->xquery('UserComments', 'user'));
    if ($rval) {
      print "<p>figureComment Error: failed to retrieve user comments from Tamino.<br>";
      print "(Tamino error code $rval)</p>";
    } else {            // xquery succeeded
      $xmlRecord = $this->tamino->xml->getBranches("ino:response/xq:result");
      // process all of the branches
      $this->CommentInit($xmlRecord);
    }
  }

  function countUserComments() {
    if (!(isset($this->comment))) {
      // initialize if necessary
      $this->getUserComments();
    }
    return count($this->comment);
  }

  // print out an approval form to approve user-submitted comments
  function approvalForm ($url) {
    print "<form action='$url'>";
    print "<table class='figDesc'>";
    print "<tr><th colspan='3'>Select the appropriate action for each comment.</th></tr>";
    print "<tr><th class='input'>Action</th><th>Comment summary</th><th>Postcard</th></tr>";
    //foreach unapproved comment, print out a table row with checkbox
    foreach ($this->comment as $c) {
      print "<tr><td class='input'>";
      // pass id in array, so action can be picked up
      print "<input type='hidden' name='id[]' value='$c->id'>";
      print "<input type='radio' name='" . $c->id . "' checked='yes' value='approve'><br>Approve<br>";
      print "<input type='radio' name='" . $c->id . "' value='delete'><br>Delete<br>";
      print "<input type='radio' name='" . $c->id . "' value='null'><br>No Action<br>";
      print "</td>";
      print "<td>";
      $c->printSummary();
      if ($this->imgpath) {
        print "<td><img src='" . $this->imgpath . $c->entity . ".jpg' alt='postcard thumbnail'></td>";
      }
      print "</td></tr>";
    }
    if (count($this->comment) == 0) {
      print "<tr><td></td><td>There are no comments to approve.</td></tr>";
    } else {
      print "<tr><td colspan='3'><input type='submit' value='Submit'></td></tr>";
    }
    print "</table>";
    print "</form>";

  }

  function approveComment() {
    //    print "DEBUG: comment id is " . $this->comment[0]->id ."<br>\n";
    $this->taminoGetComment("user");
    $this->display();
    //    $this->comment[0]->printSummary();
    // delete user comment
    // TESTING: don't actually delete until the add is working
    //    $this->deleteComment("user");
    // add admin-style comment
    //    print "DEBUG: comment entity is " . $this->comment[0]->entity ."<br>\n";
    //    print "DEBUG: comment id is " . $this->comment[0]->id ."<br>\n";
    $this->entity = $this->comment[0]->entity;
    $this->taminoAdd("admin");
  }

  function deleteComment($mode) {	// mode = admin, user
    $rval = $this->tamino->xquery($this->xquery('delete', $mode));
    if ($rval) {
      print "<p>figureComment Error: failed to delete $mode comments from Tamino.<br>";
      print "(Tamino error code $rval)</p>";
    } else {            // xquery succeeded
      print "<p>Successfully deleted $mode comment.</p>";
    }
  }
  

  function CommentInit ($xmlRecord) {	// array of phpDom XML branches
    //    print "DEBUG: in function CommentInit<br>\n";
    foreach ($xmlRecord as $branch) {
      //          print "DEBUG: in foreach loop CommentInit<br>\n";
       	  $val = $branch->getTagAttribute("id", "p");
	  if ($val) {
	    if ($this->comment[0]->id = $val) {
	      // if this comment id already exists (e.g., approving user comment),
	      // then don't create a new comment object; modify existing object      
	      $myc =& $this->comment[0];	
	    } else {
	       $myc = new comment();
	    }
	    $myc->id = $val; //print "DEBUG: id=$val<br>\n";
	  }
	  $val = $branch->getTagContent("p/name");
	  if ($val) { $myc->name = $val; /* print "DEBUG: name=$val<br>\n"; */}
	  $val = $branch->getTagContent("p/date");
	  if ($val) { $myc->date = $val; /* print "DEBUG: date=$val<br>\n"; */}
       	  $val = $branch->getTagAttribute("id", "p");
	  if ($val) { $myc->id = $val; /* print "DEBUG: id=$val<br>\n"; */}
       	  $val = $branch->getTagAttribute("n", "p/xptr");
	  if ($val) { $myc->entity = $val; /* print "DEBUG: entity=$val<br>\n";*/}
	  // do this last: remove all branches so we get text content only
	  $branch->removeAllBranches();
    	  $val = $branch->getTagContent("p");
       	  if ($val) { $myc->text = $val; }
	  /*          if ($auth == "admin") {
            $val = $this->tamino->xml->getTagContent("figure/head");
            if ($val) { $this->title = $val; }
            $val = $this->tamino->xml->getTagAttribute("entity", "figure");
            if ($val) { $this->entity = $val; }
	  }
	  */
	  // add the newly initialize comment object to the comment array
	  if ($myc->id != $this->comment[0]->id) {  // (if it doesn't exist already)
            array_push($this->comment, $myc);
	  }
        }
  }

  

  // clean up description input
  function cleanInput () {
    // quotes are getting commented by a backslash in submission process; undo this
    foreach ($this->comment as $c) {
      $c->text = preg_replace ('/\\\"/', '"', $c->text);	// replace \" with "
      $c->text = preg_replace ("/\\\'/", "'", $c->text);      // replace \' with '
    }
  }

  function XMLstring ($auth) {
    $xmlstring = "";
    foreach ($this->comment as $c) {
      $myid = $c->name . "-" . $c->date;
      $myid = preg_replace ('/ /', '_', $myid);	// replace space with underscore
      $myid = preg_replace ('/:/', '', $myid);	// remove colons

      // Note: the TEIform attribute is used to circumvent strange behavior from tamino  
      $xmlstring .= "<p TEIform='p' id='$myid' n='comment'>";
      if ($auth == "user") {	// if user mode, record which figure comment belongs to
        $xmlstring .= "<xptr n='$c->entity'/>";
      }
      $xmlstring .= "   <name TEIform='name'>$c->name</name>
        <date TEIform='date'>$c->date</date>
        $c->text
        </p>";
    }
    return $xmlstring;
  }

}


// simple class to keep track of figure comments
class comment {
  // comment components
  var $id;
  var $text;  	 // (actual text of the comment)
  var $name;
  var $date;
  var $entity;   // figure entity the comment belongs to

  function comment ($argArray) {
    $this->id = $argArray['id'];
    $this->text = $argArray['comment'];
    $this->name = $argArray['name'];
    $this->date = $argArray['date'];
    $this->entity = $argArray['entity'];
  }

  function printSummary () {
    print "<table class='comment'>";
    print "<tr><th>comments:</th><td> " . htmlentities($this->text) . "</td></tr>\n";
    print "<tr><th>name:</th><td> " . $this->name . "</td></tr>\n";
    print "<tr><th>date:</th><td> " . $this->date . "</td></tr>\n";
    if (isset($this->entity)) {
      print "<tr><th>figure:</th><td> " . $this->entity . "</td></tr>\n";
    }
    print "</table>";
  }
}
