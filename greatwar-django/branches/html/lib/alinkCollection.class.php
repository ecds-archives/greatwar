<?php

include_once("linkCollection.class.php");
include_once("alinkRecord.class.php");

// a linkCollection to use alinkRecord (approval)
class aLinkCollection extends linkCollection {


  function aLinkCollection ($argArray) {
    $this->pretty_sort_opts['approve'] = "Approved";
    $this->sortfield["approve"] = '@approved';

    parent::linkCollection($argArray);	   // call parent constructor
    // this array is defined in parent constructor overridden by 
    array_push($this->sort_opts, "approve");

    // then override linkRecords with alinkRecords
    $this->link = array();	// over-write as empty array
    foreach ($this->ids as $i) {
      $linkargs = $argArray;
      $linkargs["id"] = $i;
      $this->link[$i] = new alinkRecord($linkargs);
      $this->link[$i]->taminoGetRecord();
    }
  }

  //print summary info ONLY if approved=yes
  function printSummary () {
    foreach ($this->ids as $i) {
      if ($this->link[$i]->approved == "yes") {
        $this->link[$i]->printSummary();
      }
    }
   }

  // return the number of links needing approval
  function approveCount () {
    $count = 0;
    foreach ($this->ids as $i) {
      if ($this->link[$i]->approved == "no") {
	$count++;
      }
    }
    return $count;
  }
  
  // print out an approval form to approve submitted links
  function printApprovalForm ($url) {
    $count = 0;
    print "<form action='$url'>";
    print "<table class='linkRecord'>";
    print "<tr><th colspan='2'>Select the records you approve.</th></tr>";
    print "<tr><th class='input'>Approve</th><th class='link'>Record summary</th></tr>";
    //foreach linkRecord that is not approved, print out a table row with checkbox
    foreach ($this->ids as $i) {
      if ($this->link[$i]->approved == "no") {
	$count++;
	print "<tr><td class='input'>";
	print "<input type='checkbox' name='$i' checked='yes'></td>";
	print "<td class='link'>";
        $this->link[$i]->printSummary();
	print "</td></tr>";
      }
    }
    if ($count == 0) {
      print "<tr><td></td><td>There are no link records to approve.</td></tr>";
    } else {
      print "<tr><td colspan='2'><input type='submit' value='Approve Selected Links'></td></tr>";
    }
    print "</table>";
    print "</form>";

  }

}
