<?php

include_once("xmlDbConnection.class.php");
include_once("phpDOM/classes/include.php");

class interpGrp {

  var $tamino;

  var $groups;
  var $groupnames;
  var $names;
  
  var $id;	// optionally get information for only one interp id

  var $xquery;
  
  
  // Constructor 
  function interpGrp($argArray) {
    // pass host/db/collection settings to tamino object
    $this->tamino = new xmlDbConnection($argArray);

    $this->groups = array();
    $this->groupnames = array();
    $this->names = array();
    $this->id = $argArray["id"];
    if (isset($this->id)) {
      // return only the interpGrp and interp we are interested in, if id is set
      $this->xquery["getRecord"] = 'for $b in input()/TEI.2/:text/back/:div//interpGrp
	let $i := $b/interp[@id = "' . $this->id . '"]
	where $b/interp/@id = "' . $this->id . '" 
	return <interpGrp type="{$b/@type}"> {$i} </interpGrp>';
    } else {
      $this->xquery["getRecord"] = 'for $b in input()/TEI.2/:text/back/:div//interpGrp return $b';
    }

    // initialize values from tamino
    $this->taminoGetRecord();
  } 


  // retrieve interpGrps from tamino & initialize object values
  function taminoGetRecord() {
   $rval = $this->tamino->xquery($this->xquery["getRecord"]);
    if ($rval) {
    } else {            // xquery succeeded

      //convert xml tree to simple xml object
      $sx = simplexml_import_dom($this->tamino->xml);

      foreach ($sx->xpath("//interpGrp") as $g) {
   	$grp = $g["type"];
	  // add group name to list of interp groups
	array_push($this->groupnames, $grp);
	  // create an array for ids belonging to this group
	$this->groups["$grp"] = array();
	foreach ($g->interp as $i) {
	  $id = $i["id"];
	  $val = $i["value"];
	    // add id to group array
 	  array_push($this->groups["$grp"], $id);
	    // add index to pretty name array
	  $this->names["$id"] = $val;
	}
      }

      //      $xmlgroup = $this->tamino->xml->getBranches("ino:response/xq:result");
      //      $children = $result->childNodes;

      /*      if ($children) {
	// Cycle through all of the branches (order doesn't matter)
	foreach ($children as $c) {
	  //	  print "DEBUG: XMLString is" . $g->getXMLString() . "<br>\n";
 	  $grp = $c->getTagAttribute("type");
	  // add group name to list
    	  array_push($this->groupnames, $grp);
	  // create an array for ids belonging to this group
	  $this->groups[$grp] = array();

	  $xmlinterp = $g->getBranches();
	  foreach ($xmlinterp as $i) {
      	    $id = $i->getTagAttribute("id");
       	    $val = $i->getTagAttribute("value");
	    // add id to group array
	    array_push($this->groups[$grp], $id);
	    // add index to pretty name
	    $this->names[$id] = $val;
	  } // foreach interp
	} // foreach interpGrp
      }  */
    }
  } 

  function printSummary () {
    foreach ($this->groupnames as $g) {
      print "$g<br>\n<ul>\n";
      foreach ($this->groups["$g"] as $i) {
	print "<li>" . $this->names["$i"] . "  ($i)</li>\n";
      }
      print "</ul>\n";
    }
  }

  // return an interp name (value) for an interp id
  function name ($id) {
    $val = $this->names["$id"];
    return $val;
  }

  // return which group an id belongs to
  function group ($id) {
    foreach ($this->groupnames as $g) {
      if (in_array($id, $this->groups["$g"])) {
	return $g;
      }
    }
  }

  
}
