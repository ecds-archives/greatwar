<?php

include_once("lib/xmlDbConnection.class.php");
include_once("subjectList.class.php");
include_once("lib/HTTP/Request.php");	// for testing urls

class linkRecord {

  var $tamino;

  var $id;
  var $title;
  var $url;
  var $subject;  
  var $description;
  var $contributor;
  var $ed_contributor;
  var $date;
  var $lastModified;
  var $edit;
  var $all_subjects;
  var $httpResponse;
  /* original date / date last modified ? */


  // Constructor 
  function linkRecord($argArray, $subjArray = NULL) {
    // pass host/db/collection settings to tamino object
    $this->tamino = new xmlDbConnection($argArray);

    $this->id = $argArray['id'];
    $this->url = $argArray['url'];

    /* These fields may or may not be set-- 
       They may also be defined by setting id (was url) & using getRecord() */
    $this->title = $argArray['title'];
    $this->description = $argArray['description'];
    $this->contributor = $argArray['contributor'];
    $this->ed_contributor = $argArray['ed_contributor'];
    $this->date = $argArray['date'];
    // initialize lastModified to same as date, at first
    $this->lastModified = $argArray['date'];

    // define subjects for this record, if set
    if ($subjArray) {
      $this->subject = $subjArray;
    } else {
      $this->subject = array();
    }
    
    // pass in tamino settings to subject list
    $this->all_subjects = new subjectList($argArray);

    // FIXME: edits?
    $this->edit = array();

  }  // end linkRecord constructor

  // generate an xquery using current settings, depending on the mode
  function xquery ($mode) {
    // Dublin Core namespace
    $dcns = 'dc="http://purl.org/dc/elements/1.1/"';

    switch ($mode):
  case 'getRecord': 
    // xquery to retrieve a record by id
    $query = "declare namespace $dcns
                  for \$b in input()/linkCollection/linkRecord 
                  where \$b/@id = '$this->id' 
                 return \$b"; 
    break;
  case 'delete':
    // xquery to delete record by url
    $query = "declare namespace $dcns 
              update for \$b in input()/linkCollection/linkRecord
              where \$b/@id = '$this->id'
              do delete \$b";
    break;
  case 'add':
    // xquery to add a new record
    $query = "declare namespace $dcns
              update for \$b in input()/linkCollection 
              do insert " . $this->XMLstring() . ' into $b'; 
    break; 
  case 'modify':  
    // xquery to modify an existing record 
   $query = "declare namespace $dcns  
              update for \$b in input()/linkCollection/linkRecord  
              where \$b/@id = '$this->id'   
              do replace \$b with " . $this->XMLstring(); 
   break;
   endswitch;

   return $query;
  }

  // create an id (for a new record)
  function generateId() {
    $this->id = "$this->date $this->contributor";
  }


  // retrieve a record from tamino by url & initialize object values
  function taminoGetRecord() {
    $rval = $this->tamino->xquery($this->xquery('getRecord'));
    if ($rval) {
      print "<p>LinkRecord Error: failed to retrieve linkRecord from Tamino.<br>";
      print "(Tamino error code $rval)</p>";
    } else {            // xquery succeeded
      $this->tamino->xpath->registerNamespace("xq","http://namespaces.softwareag.com/tamino/XQuery/result");
      $dc_list = $this->tamino->xpath->query("//linkRecord/*");	// should return nodelist
      for ($j=0; $j < $dc_list->length; $j++) {
	switch ($dc_list->item($j)->localName) {
  	case "identifier"  : $this->url = $dc_list->item($j)->textContent; break;
  	case "title"       : $this->title = $dc_list->item($j)->textContent; break;
	case "description" : $this->description = $dc_list->item($j)->textContent; break;
	case "date"        : $this->date = $dc_list->item($j)->textContent; break;
	case "contributor" : $this->contributor = $dc_list->item($j)->textContent; break;
	case "subject"     : array_push($this->subject, $dc_list->item($j)->textContent); break;
	}
      }
      $edits = $this->tamino->xpath->query("//linkRecord/edit");
      if ($edits) {
	  // arrays to store values temporarily, to get into linkEdit objects
	  $mydate = array();
	  $mycontrib = array();
	  $mydesc = array();
        for ($j=0; $j < $edits->length; $j++) {
  	  switch ($edits->item($j)->localName) {
    	  case "date" : array_push($mydate, $edits->item($j)->textContent); break;
    	  case "description" : array_push($mydesc, $edits->item($j)->textContent); break;
    	  case "contributor" : array_push($mycontrib, $edits->item($j)->textContent); break;
	  }
	}
	
        for ($i=0; $i < count($mydate); $i++) {
	  $edit_args = array('date' => $mydate[$i], 
			       'contributor' => $mycontrib[$i],
			       'description' => $mydesc[$i]);
	  $this->addEdit($edit_args);
	}
      }
    }
  }

  // Delete record from tamino
  function taminoDelete (){
    $rval = $this->tamino->xquery($this->xquery('delete'));
    if ($rval) {
      print "<p>Failed to delete linkRecord for <b>$this->title</b>.</p>";
    } else {
      print "<p>Successfully deleted record for <b>$this->title</b>.</p>";
    }
  }

  // add a record to tamino
  function taminoAdd () {
    if (($this->id == '')||(!(isset($this->id)))) {
      $this->generateId();
    }
    /* 
    print "DEBGU taminoAdd: xquery  is " . $this->xquery('add') . "<br>";
    */

    $rval = $this->tamino->xquery($this->xquery('add'));
    if ($rval) {          // tamino error
      print "<p>Failed to add new record for <b>$this->url</b>.</p>";
    } else {          // success
      print "<p>Successfully added new record for <b>$this->url</b>.</p>";
    }
  }

  // update a record in tamino
  function taminoModify () {
    $rval = $this->tamino->xquery($this->xquery('modify'));
    if ($rval) {       // tamino error
      print "<p>Failed to update record for <b>$this->url</b>.</p>";
    } else {
      print "<p>Successfully updated record for <b>$this->url</b>.</p>";
    }
  }

  function XMLstring () {
    $xmlstring .= "<linkRecord id='$this->id'>
                 <dc:title>$this->title</dc:title> 
                 <dc:identifier>$this->url</dc:identifier> 
                 <dc:description>$this->description</dc:description> 
                 <dc:date>$this->date</dc:date> 
                 <dc:contributor>$this->contributor</dc:contributor>";  
    foreach ($this->subject as $s) {
      $xmlstring .= "<dc:subject>$s</dc:subject>\n";
    }
    foreach ($this->edit as $e) {
     $xmlstring .= "<edit>
                  <dc:date>$e->date</dc:date> 
                  <dc:description>$e->description</dc:description> 
                  <dc:contributor>$e->contributor</dc:contributor> 
               </edit>"; 
    }
    $xmlstring .= "</linkRecord>";
    return $xmlstring;
  }
  
  // print a brief listing of the record
  function printSummary () {
    print "<p><a href='$this->url'>$this->title</a><br>";
    print "<font size='-1'>$this->url</font><br>";
    print "$this->description<br>";
    print "<font size='-2'>Contributed by: $this->contributor</font><br>";
    print "</p>";
  }


  // print all the values in a nice HTML table
  function printHTML ($show_edits = 1) {
    print "<table class='fullLinkRecord'>";
    print "<tr><th width='20%'>Title:</th><td>$this->title</td></tr>";
    print "<tr><th>ID:</th><td>$this->id</td></tr>";    
    print "<tr><th>URL:</th><td><a href='$this->url'>$this->url</a></td></tr>";
    print "<tr><th>Subject(s):</th><td>";
    foreach ($this->subject as $s) { print "$s<br>"; }
    print "</td></tr>";
    print "<tr><th>Description:</th><td>$this->description</td></tr>";
    print "<tr><th>Contributor:</th><td>$this->contributor</td></tr>";
    print "<tr><th>Submitted:</th><td>$this->date</td></tr>";
    if ($this->date != $this->lastModified) {
      // only print last modified if it is different than submitted
      print "<tr><th>Last Modified:</th><td>$this->lastModified</td></tr>";
    }
    if ($show_edits && (count($this->edit) > 0)) {
      print "<tr><th>Modifications</th><td>";
      foreach ($this->edit as $e) { 
	$e->printEdit(); 
      }
      print "</td></tr>";
    }
    print "</table>";
  }

  // create an HTML form, with initial values set (if defined)
  // mode should be either add or modify
  function printHTMLForm ($mode) {
    $textinput  = "input type='text' size='50'";
    $hiddeninput = "input type='hidden'";
    $readonlyinput = "input type='text' readonly='yes' size='50'";
    print "<table class='fullLinkRecord' border='1' align='center'>\n";
    print "<form action='do_$mode.php' method='get'>\n";
    print "<tr><th>Title:</th><td><$textinput name='title' value='$this->title'></td></tr>\n";
    print "<tr><th>URL:</th><td>\n";
    if (isset($this->url)) {
      print "<$textinput name='url' value='$this->url'>";
    } else {
      print "<$textinput name='url' value='http://'>";
    }
    print "</td></tr>\n";
    print "<tr><th>Description</th><td><textarea cols='50' rows='4' name='desc'>$this->description</textarea></td></tr>\n";
    print "<tr><th>Subject(s):</th>\n";
    print "<td>";
    $this->all_subjects->printSelectList($this->subject);
    print "<br><i>Note: use control or shift keys to select multiple subjects.</i>\n";
    print "</td></tr>\n";
    print "<tr><th>Submitted by:</th><td>\n";
    // if already defined, don't allow user to modify
    if (isset($this->contributor)) {
      //      print "<$hiddeninput name='contrib' value='$this->contributor'>$this->contributor";
      print "<$readonlyinput name='contrib' value='$this->contributor'>\n";
    } else {
      print "<$textinput name='contrib'>\n";
    }
    print "</td></tr>";
    print "<tr><th>Date Submitted:</th><td>\n";
    // if already defined, don't allow user to modify
    if (isset($this->date)) {
      print "<$readonlyinput name='date' value='$this->date'>\n";
    } else {
      /* If unset, initialize date value to today.  
         Format is: 2004-04-09 4:13:00 PM */
      print "<$textinput name='date' value='" . date("Y-m-d g:i:s A") . "'>\n";
    }
    print "</td></tr>";
    if (isset($this->id)) {
      print "<tr><th>Record ID:</th><td><$readonlyinput name='id' value='$this->id'></td></tr>\n";
    }

    // Fields to keep track of changes to a record
    if ($mode == 'modify') {

      print "<tr><th class='label' colspan='2'>Modification Data</th></tr>\n";

      if (count($this->edit) > 0) {
	print "<tr><th>Previous edits:</th><td>\n";
	foreach ($this->edit as $e) { 
	  $e->printEdit(); 
	  print "<$hiddeninput name='prev_date[]' value='" . $e->date . "'>\n";
	  print "<$hiddeninput name='prev_contrib[]' value='" . $e->contributor . "'>\n";
	  print "<$hiddeninput name='prev_desc[]' value='" . $e->description . "'>\n";
	}
	print "</td></tr>";
      }

      print "<tr><th class='label' colspan='2'>Current Edit</th></tr>\n";

      print "<tr><th>Edited by:</th><td>";
      if (isset($this->contributor)) {
        print "<$textinput name='mod_contrib' value='$this->ed_contributor'>\n";
      } else {
        print "<$textinput name='mod_contrib'>\n";
      }
      print "</td></tr>\n";
      print "<tr><th>Description of change:</th>\n";
      print "<td><textarea cols='50' rows='4' name='mod_desc'></textarea></td></tr>\n";
      print "<tr><th>Date Modified:</th><td><$textinput name='mod_date' value='" . date("Y-m-d g:i A") . "'></td></tr>\n";
    }
    print "<tr><td colspan='2' align='center'>\n";
    print "<input type='submit' value='Submit'>\n";
    print "<input type='reset'>\n";
    print "</td></tr></form></table>\n";
  }

  function addEdit ($argArray) {
    // create a new linkEdit with specified settings
    $myedit = new linkEdit($argArray);
    // add to array of edits for this linkRecord
    array_push($this->edit, $myedit);
  }

  // check if a url is still valid 
  function testUrl () {
    $req = & new HTTP_Request("");
    $req->setURL($this->url);
    $req->sendRequest();
    $this->httpResponse = $req->getResponseCode();
  }

  // print out a readable version of the url status
  // by default, each link will be in its own table, unless requested otherwise
  function printUrlStatus ($show_table = true) {
    if (!(isset($this->httpResponse))) {
      $this->testUrl();		// if response is not set, test the url first
    }
    
    $code = array("404" => "Not Found",
	       	  "403" => "Forbidden",
	          "401" => "Unauthorized",
	          "301" => "Moved Permanently",
	          "302" => "Redirected",
	          "200" => "OK");

    if ($show_table) { print "<table class='linkStatus'>"; }
    print "<tr>";
    print "<td class='url'><a href='$this->url'>$this->title</a><br>";
    print "<font size='-1'>$this->url</font></td>"; 
    print "<td class='response_code'>";
    switch ($this->httpResponse) {
    case 404:		/* 400s - errors */ 
    case 403:
    case 401:
        print "<font class='error'>" . $code[$this->httpResponse] . "</font><br>\n";
        break;
    case 301:		/* 300s - warnings */
    case 302:
        print "<font class='warning'>" . $code[$this->httpResponse] . "</font><br>\n";
        break;
    case 200:		/* 200 - OK */
      print "<font class='ok'>" . $code[$this->httpResponse] . "</font><br>\n";
        break;
    default:
      print "Response code: $this->httpResponse <br>\n";
    }
    print "</td></tr>";
    if ($show_table) print "</table>";
    
  }
		     

}



// simple class to keep track of edits to a record
class linkEdit {
  var $date;
  var $contributor;
  var $description;

  function linkEdit ($argArray) {
    $this->date = $argArray['date'];
    $this->contributor = $argArray['contributor'];
    $this->description = $argArray['description'];
  }
  
  // print edit information in a nice table
  function printEdit () {
    print "<table class='linkEdit'>";
    print "<tr><th width='20%'>Editor:</th><td>$this->contributor</td></tr>";
     print "<tr><th>Description:</th><td>$this->description</td></tr>";
    print "<tr><th>Date:</th><td>$this->date</td></tr>";
   print "</table>";
  }
   
}
