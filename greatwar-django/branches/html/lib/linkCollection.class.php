<?php

include_once("lib/xmlDbConnection.class.php");
include_once("subjectList.class.php");
include_once("linkRecord.class.php");

class linkCollection {
  var $tamino;
  var $subject;
  var $link;
  var $ids;
  var $sort;         // sort linkRecords by: title|contrib|date 
  var $sort_opts;
  var $user_sort_opts;
  var $pretty_sort_opts;
  var $sortfield;

  var $count;

  // limit by subject or keyword
  var $limit_subject;
  var $search;

  var $dcns;
  var $xquery;
  
  function linkCollection ($argArray) {
    // pass host/db/collection settings to member objects
    $this->tamino = new xmlDbConnection($argArray);
    $this->subject = new subjectList($argArray);

    $this->sort_opts = array("title", "date","contrib");
    $this->user_sort_opts = $this->sort_opts;
    $this->pretty_sort_opts['date'] = "Date Submitted";
    $this->pretty_sort_opts['title'] = "Title";
    $this->pretty_sort_opts['contrib'] = "Contributor";

    $this->sortfield["date"] = "dc:date";
    $this->sortfield["title"] = "dc:title";
    $this->sortfield["contrib"] = "dc:contributor";
    $this->sort = $argArray['sort'];
    $this->limit_subject = $argArray['limit_subject'];

    // keyword search term
    $this->search["keyword"] = $argArray['keyword'];

    if ($this->sort == '') { $this->sort = "title"; }  // default

    // Dublin Core namespace
    $this->dcns = "dc='http://purl.org/dc/elements/1.1/'";
    // xquery to retrieve all linkRecord identifiers from tamino
    $declare = "declare namespace $this->dcns 
	declare namespace tf='http://namespaces.softwareag.com/tamino/TaminoFunction'"; 
    $for =  'for $b in input()/linkCollection/linkRecord';
    $cond_i = 0;	// condition index/count
    if (isset($this->limit_subject) && ($this->limit_subject != '') 
	&& ($this->limit_subject != 'all')) {
      $cond[$cond_i] = " \$b/dc:subject = '$this->limit_subject' ";
      $cond_i++;
    }
    if (isset($this->search["keyword"]) && ($this->search["keyword"] != '')) {
      $cond[$cond_i] = ' tf:containsText($b//*, "' . $this->search["keyword"] . '") ';
      $cond_i++;
    }
    if ($cond_i > 0) {		// there is at least one condition set
      $where = "where $cond[0]";
      for ($i = 1; $i < $cond_i; $i++) {	// add any more conditions
        $where .= " and $cond[$i]";
      }
    } else { $where = ""; }
    $return = 'return $b/@id';
    $sort = " sort by (" . $this->sortfield[$this->sort] . ")";
    $this->xquery = "$declare $for $where $return $sort";

    // initialize id list from Tamino  
    $this->taminoGetIds(); 
    // for each id, create and initialize a linkRecord object
    foreach ($this->ids as $i) {
      $linkargs = $argArray;
      $linkargs["id"] = $i;
      $this->link[$i] = new linkRecord($linkargs);
      $this->link[$i]->taminoGetRecord();
    }
    $this->count = count($this->link);
  }

  // retrieve all the linkRecord ids
  function taminoGetIds() {
    $rval = $this->tamino->xquery($this->xquery);
    if ($rval) {       // tamino Error
      print "<p>LinkCollection Error: failed to retrieve linkRecord id list.<br>";
      if ($this->tamino->debug) { print "(Tamino error code $rval)"; }
      print "</p>";
    } else {       
      // convert xml ids into a php array 
      $this->ids = array();
      $this->tamino->xpath->registerNamespace("xq","http://namespaces.softwareag.com/tamino/XQuery/result");
      $id_list = $this->tamino->xpath->query("//xq:attribute");	// should return nodelist
      for ($j=0; $j < $id_list->length; $j++) {
      	array_push($this->ids, $id_list->item($j)->getAttribute("id"));
      }

      //      $this->xml_result = $this->tamino->xml->getBranches("ino:response/xq:result");
      //      if ($this->xml_result) {
	// Cycle through all of the branches 
      //	foreach ($this->xml_result as $branch) {
      //	  if ($att = $branch->getTagAttribute("id", "xq:attribute")) {
      //	    array_push($this->ids, $att);
      //	  }
      //	}    /* end foreach */
      //      } 
    }

  }     /* end taminoGetIds() */

  // print full details of all linkRecords in a nice table
  function printRecords ($show_edits = 1) {
    print "<table class='linkCollection'>";
    foreach ($this->ids as $i) {
      print "<tr><td>";
      $this->link[$i]->printHTML($show_edits);
      print "</td>";
      print "<td class='delmod'><p><a href='delete.php?id=$i'>Delete</a></p>";
      print "<p><a href='modify.php?id=$i'>Modify</a></p>";
      print "<p><a href='test.php?id=$i'>Test</a></p>";
      print "</td></tr>"; 
    }
    print "</table>";
  }

  //print summary info for all linkRecords
  function printSummary () {
    foreach ($this->ids as $i) {
      $this->link[$i]->printSummary();
    }
   }


  // print sort options linked to the url passed in
  // mode-- user vs. admin ?
  function printSortOptions ($url, $mode = "user") {
    if ($this->tamino->xml) {		// only display if we have content
      print "<p align='center'><b>Sort by:</b> ";
      if ($mode == "user") {
        $sort = $this->user_sort_opts;
      } else if ($mode == "admin") {
        $sort = $this->sort_opts;
      }

      foreach ($sort as $s) {
        if ($s != $sort[0]) {
  	 // print a separator between terms
  	 print " | ";
        }
        if ($s == $this->sort) {
 	  print "&nbsp;" . $this->pretty_sort_opts[$s] . "&nbsp;";
        } else {
  	  print "&nbsp;<a href='$url?sort=$s'>" . 
	  $this->pretty_sort_opts[$s] . "</a>&nbsp;";
        }
      }
      print "</p>";
    } else if ($this->tamino->debug) {
	print "<p><b>Warning:</b> in linkCollection::printSortOptions; XML is undefined, not printing sort options.</p>\n";
    }
  }

  // drop-down box to limit links by subject
  // optionally specify the current selection (by default, none)
  function printSubjectOptions ($url, $selected = NULL) {
    if ($this->tamino->xml) {		// only display if we have content
      print "Limit by Subject:<br>\n";
      print "<form action='$url' method='get'>\n";
      $this->subject->printSelectList($selected, 1, 'no', true);
      print '<input type="submit" value="Go">';
      print "</form>\n";
    } else if ($this->tamino->debug) {
      print "<p><b>Warning:</b> in linkCollection::printSubjectOptions; XML is undefined, not printing subject options.</p>\n";
    }
  }


  // print url status for all linkrecords
  function printUrlStatus ($id = NULL) {
    //if an id is specified, only display the status of the requested url
    print "<table class='linkStatus'>";
    if (isset($id)) {
      $this->link[$id]->printUrlStatus(false);
    } else {
      foreach ($this->ids  as $i) {
	 // display each link as a table row, not a full table
         $this->link[$i]->printUrlStatus(false);		
      }
    print "</table>";
    }
  }

}
