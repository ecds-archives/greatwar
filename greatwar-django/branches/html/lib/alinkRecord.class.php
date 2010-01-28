<?php

include_once("linkRecord.class.php");

// linkRecord with approval value
class alinkRecord extends linkRecord {
  var $approved;

  function alinkRecord($argArray, $subjArray = NULL) {
    $this->approved = "no";		// by default, approval is false for a new linkRecord
    // pass paramters to base class constructor
    $this->linkRecord($argArray, $subjArray);
  }

  function taminoGetRecord() {
    parent::taminoGetRecord();	// call base class function first, fill in all values
    $rec = $this->tamino->xpath->query("//linkRecord");
    $this->approved = $rec->item(0)->getAttribute("approved"); 
  }

  // overload the parent class (there must be a better way to do this!)
  function XMLstring () {
    $xmlstring .= "<linkRecord id='$this->id' approved='$this->approved'>
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

  function printHTML ($show_edits = 1) {
    print "<p class='alinkRecord'>";
    parent::printHTML($show_edits);	// call base class function first
    $astatus = ($this->approved == "yes") ? "Yes" : "Pending";
    print "Approved: $astatus</p>";
  }

  //mark a record as approved
  function approve () {
    $this->approved = "yes";
    // xquery to set approved attribute to yes
    $xquery = "update for \$b in input()/linkCollection/linkRecord
	      let \$a := \$b/@approved
              where \$b/@id = '$this->id'
              do replace \$a with attribute approved { 'yes' }";
    $rval = $this->tamino->xquery($xquery);
    if ($rval) {       // tamino error
      print "<p>Error: Approval failed for:</p>";
      $this->printSummary();
    } else {
      print "<p>Approval succeeded for:</p>";
      $this->printSummary();
    }
  }
		     
  
}
