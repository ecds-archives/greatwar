<?xml version="1.0" encoding="ISO-8859-1"?>  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:html="http://www.w3.org/TR/REC-html40" 
	xmlns:ino="http://namespaces.softwareag.com/tamino/response2" 
	xmlns:xql="http://metalab.unc.edu/xql/">

<!-- Note: all links in this stylesheet should be relative to the root
     directory of the entire site. -->

<xsl:include href="teipoetry.xsl"/>
<xsl:include href="teinote.xsl"/>
<xsl:include href="convertcase.xsl"/>

<xsl:param name="mode"/>
<xsl:param name="selflink"/>	<!-- for use with footnotes -->	
<xsl:param name="max"/>
<xsl:param name="position"/>

<!-- options:
     browse = list of titles with author/editor
     poetbrowse = browse by poet
     contents = list of poems (and any other content) in a single book 
     poem = full-text of a single poem (or poem-level item)
     frontmatter = forewords and such
     search = search results (list of poems)
-->

<xsl:output method="xml"/>  

<xsl:template match="/"> 
  <xsl:choose>
    <xsl:when test="$mode='browse'">
      <ul>
        <xsl:apply-templates select="//div" mode="browse"/>
     </ul>
    </xsl:when>
    <xsl:when test="$mode='poetbrowse'">
      <xsl:element name="script">
        <xsl:attribute name="language">Javascript</xsl:attribute>
        <xsl:attribute name="src">toggle-list.js</xsl:attribute>
      </xsl:element> <!-- script -->
	<p>Displaying poets 
	<xsl:call-template name="lastname">
   	<xsl:with-param name="author"><xsl:value-of select="//div[1]/docAuthor/@n"/></xsl:with-param>
 	</xsl:call-template>
	- 
	<xsl:call-template name="lastname">
   	<xsl:with-param name="author"><xsl:value-of select="//div[last()]/docAuthor/@n"/></xsl:with-param>
 	</xsl:call-template>
<br/>
<!-- link to next and previous -->
<xsl:call-template name="poetlinks"/>
	</p>

      <ul>
        <xsl:apply-templates select="//div" mode="poetbrowse"/>
     </ul>
<!-- also link at the bottom of the list  -->
<p><xsl:call-template name="poetlinks"/></p>

    </xsl:when>
    <xsl:when test="$mode='contents'">
      <xsl:apply-templates select="//div" mode="contents"/>
    </xsl:when>
    <xsl:when test="$mode='poem'">
      <xsl:apply-templates select="//div" mode="poem"/>
    </xsl:when>
    <xsl:when test="$mode='frontmatter'">
      <xsl:apply-templates select="//div" mode="front"/>
    </xsl:when>
    <xsl:when test="$mode='search'">
      <xsl:apply-templates select="//div2" mode="search"/>
    </xsl:when>
  </xsl:choose>
</xsl:template>



<xsl:template match="div" mode="browse">
 <li>
   <a>
   <xsl:attribute name="href">poetry/contents.php?id=<xsl:value-of select="@id"/></xsl:attribute>
     <xsl:value-of select="titleStmt/title"/></a>
       <br/><xsl:value-of select="titleStmt/author"/> 
       <xsl:apply-templates select="titleStmt/editor"/>
 </li>
</xsl:template>

<xsl:template match="editor">
  <xsl:value-of select="."/>, ed.
</xsl:template>


<xsl:key name="poetkey" match="div" use="docAuthor/@n"/>

<xsl:template match="div" mode="poetbrowse">

  <!-- only print poet name if it hasn't already been printed -->
  <xsl:choose>
    <xsl:when test="docAuthor/@n = preceding-sibling::div[1]/docAuthor/@n">
    </xsl:when>
      <!-- only print if docAuthor is actually defined -->
    <xsl:when test="docAuthor/@n">
    <div class="toggle">
	<!-- added position to lastname to ensure uniqueness -->
    <xsl:variable name="lastname">
      <xsl:value-of select="concat(substring-before(docAuthor/@n, ','), '-', position())"/>
    </xsl:variable>
      <!-- create toggle image -->
      <xsl:call-template name="toggle-image">
        <xsl:with-param name="id"><xsl:value-of select="$lastname"/></xsl:with-param>
      </xsl:call-template>
 <!--     <xsl:apply-templates select="docAuthor"/> -->
      <xsl:value-of select="docAuthor/@n"/>
      <ul>
       <xsl:attribute name="id"><xsl:value-of select="$lastname"/></xsl:attribute>
        <xsl:apply-templates select="key('poetkey', docAuthor/@n)" mode="poetbrowsetitle"/>
      </ul>
     </div>
    </xsl:when>
    <xsl:otherwise/>
  </xsl:choose>

</xsl:template>


<xsl:template name="poetlinks">
<!-- FIXME: this count still seems a bit off -->
<xsl:variable name="poetcount"><xsl:value-of select="count(//div/docAuthor/@n[not(preceding-sibling::div/docAuthor/@n = .)])"/></xsl:variable>

  <!-- links to next & previous sets of poets -->
  <xsl:if test="$position != 1"> 		<!-- if not the first set, link back -->
   <a>
   <xsl:attribute name="href"><xsl:value-of select="concat($selflink,
'?max=', $max, '&amp;position=')"/><xsl:value-of select="$position - $max"/></xsl:attribute>
   &lt; Previous</a>
   </xsl:if>
   <!-- if displaying both links, put a little divider -->
   <xsl:if test="$position != 1 and $poetcount >= $max"><xsl:text> | </xsl:text></xsl:if>
   <!-- if # of poets = maxdisplay, there are (probably) more poets -->
   <xsl:if test="$poetcount >= $max">
   <a>
   <xsl:attribute name="href"><xsl:value-of select="concat($selflink,
'?max=', $max, '&amp;position=')"/><xsl:value-of select="$position + $max"/></xsl:attribute>
   Next &gt;</a>
   </xsl:if>
</xsl:template>


<!-- poems should link to the poem page -->
<xsl:template match="div[@type='poem']" mode="poetbrowsetitle">
  <li>
    <a>
     <xsl:attribute name="href">poetry/view.php?id=<xsl:value-of select="@id"/></xsl:attribute>
     <xsl:value-of select="@n"/>
     <xsl:if test="not(@n)">[untitled]</xsl:if>
    </a> 

    <font class="type">(<xsl:value-of select="@type"/>)</font>
  </li>
</xsl:template>

<!-- any other divs should be entire volumes -->
<xsl:template match="div" mode="poetbrowsetitle">
  <xsl:variable name="myid"><xsl:value-of select="div2[1]/@id"/></xsl:variable>
  <li class="toggle">
      <!-- create toggle image -->
      <xsl:call-template name="toggle-image">
        <xsl:with-param name="id"><xsl:value-of select="$myid"/></xsl:with-param>
      </xsl:call-template>

  <a>
  <xsl:attribute name="href">poetry/contents.php?id=<xsl:value-of select="@docname"/></xsl:attribute>
  <xsl:value-of select="@n"/>
  <xsl:if test="not(@n)">
    <xsl:value-of select="head"/>
  </xsl:if>
  </a>
   <font class="type">(<xsl:value-of select="@type"/>)</font>
   
  <ul>
    <xsl:attribute name="id"><xsl:value-of select="$myid"/></xsl:attribute>
    <xsl:apply-templates select="div2" mode="contents"/>
  </ul>
</li>
</xsl:template>

<xsl:template match="div" mode="contents">
  <ul>
    <xsl:apply-templates select="//div1" mode="contents"/>
  </ul>
  <xsl:apply-templates select="teiHeader"/>
</xsl:template>


<xsl:template match="div" mode="front">
  <xsl:apply-templates select="div1"/>
  <xsl:apply-templates select="teiHeader"/>
</xsl:template>


<xsl:template match="teiHeader">
<!-- first two are redundant -->
<!--  <xsl:value-of select="fileDesc/titleStmt/title"/><br/>
  <xsl:value-of select="fileDesc/titleStmt/author"/><br/> -->
 <p class="copyright">
    <xsl:apply-templates select="fileDesc/sourceDesc/bibl"/>
 </p>
</xsl:template>

<xsl:template match="fileDesc/sourceDesc/bibl">
  <xsl:choose>
    <xsl:when test="title"> 	
<!-- if title is defined, bibl uses fields; construct the publication
     line from the components -->
      <xsl:value-of select="author"/>
      <xsl:apply-templates select="editor"/>
      <i><xsl:value-of select="title"/>. </i>
      <xsl:value-of select="pubPlace"/>: 
      <xsl:value-of select="publisher"/>,
      <xsl:value-of select="date"/>.
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="."/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="div1" mode="contents">
  <li>
  <xsl:value-of select="@n"/>
  <xsl:if test="not(@n)">
    <xsl:value-of select="head"/>
  </xsl:if>
   <font class="type">(<xsl:value-of select="@type"/>)</font>
	<br/> 
  <xsl:value-of select="docAuthor"/> <xsl:value-of select="docDate"/> <xsl:value-of select="bibl"/>
   
  <xsl:if test="count(div2) > 0">
    <ul>
      <xsl:apply-templates select="div2" mode="contents"/>
    </ul>
  </xsl:if>

</li>
</xsl:template>

<!-- front matter divs : similar to above, but with a link to content -->
<xsl:template match="front/div1" mode="contents">
 <li>
  <a>
   <xsl:attribute name="href">poetry/front.php?id=<xsl:value-of select="@id"/></xsl:attribute>
  <xsl:choose>
    <xsl:when test="@n">
      <xsl:value-of select="@n"/>
    </xsl:when>
    <xsl:when test="head">
      <xsl:value-of select="head"/>
    </xsl:when>
    <xsl:otherwise>
       <xsl:call-template name="convertpropercase">
         <xsl:with-param name="str"><xsl:value-of select="@type"/></xsl:with-param>
       </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
  </a>
   <!-- only display type if it was not used for title/link -->
   <xsl:if test="@n or head">
     <font class="type">(<xsl:value-of select="@type"/>)</font>
   </xsl:if>
 </li>
</xsl:template>


<!-- same as above, but linked to content -->
<xsl:template match="div1[@type='colophon']" mode="contents">
  <li>
    <xsl:value-of select="p"/>    
    <font class="type">(<xsl:value-of select="@type"/>)</font> 
  </li>
</xsl:template>



<xsl:template match="div2" mode="contents">
  <li>
    <a>
     <xsl:attribute name="href">poetry/view.php?id=<xsl:value-of select="@id"/></xsl:attribute>
     <xsl:value-of select="@n"/>
     <xsl:if test="not(@n)">[untitled]</xsl:if>
    </a> 
    <xsl:if test="docAuthor">
	<xsl:value-of select="concat(' - ', docAuthor)"/>
    </xsl:if>

    <font class="type">(<xsl:value-of select="@type"/>)</font>
  
    <xsl:if test="count(div3) > 0">
      <ul>
        <xsl:apply-templates select="div3" mode="contents"/>
      </ul>
    </xsl:if>


  </li>
</xsl:template>

<xsl:template match="div3[@type='poem']" mode="contents">
  <li>
    <a>
     <xsl:attribute name="href">poetry/view.php?id=<xsl:value-of select="../@id"/>#<xsl:value-of select="@id"/></xsl:attribute>
     <xsl:value-of select="@n"/>
     <xsl:if test="not(@n)">[untitled]</xsl:if>
    </a> 
    <xsl:if test="docAuthor">
	<xsl:value-of select="concat(' - ', docAuthor)"/>
    </xsl:if>

    <font class="type">(<xsl:value-of select="@type"/>)</font>
  
    <ul>
      <xsl:apply-templates select="div3" mode="contents"/>
    </ul>

  </li>
</xsl:template>



<!-- search results -->
<xsl:template match="div2" mode="search">
   <p>
    <a>
     <xsl:attribute name="href">poetry/view.php?id=<xsl:value-of select="@id"/></xsl:attribute>
     <xsl:value-of select="@n"/>
     <xsl:if test="not(@n)">[untitled]</xsl:if>
    </a> 

   <xsl:if test="docAuthor"><xsl:value-of select="concat(' - ', docAuthor)"/></xsl:if>

   <!-- search results mode: display line count and lines matching
	search term -->
    <xsl:apply-templates select="linecount" mode="search"/>
   </p>
    <p class="linematch">
      <xsl:apply-templates select="l" mode="search"/>
    </p>
</xsl:template>

<xsl:template match="linecount" mode="search">
  <font class="extent">
     <xsl:text> (</xsl:text><xsl:value-of select="."/><xsl:text> lines)</xsl:text>
  </font>
</xsl:template>

<!-- matching lines from keyword search -->
<xsl:template match="l" mode="search">
  <xsl:text>... </xsl:text>
  <xsl:apply-templates/>
  <xsl:text> ...</xsl:text>
  <br/>
</xsl:template>

<xsl:template match="div1">
  <xsl:apply-templates/>
  <xsl:call-template name="endnotes"/>
</xsl:template>

<xsl:template match="p">
  <p><xsl:apply-templates/></p>
</xsl:template>

<xsl:template match="div" mode="poem">

  <p class="source">Contents - 
  <a>
   <xsl:attribute name="href">poetry/contents.php?id=<xsl:value-of select="@id"/></xsl:attribute>
     <xsl:value-of select="//titleStmt/title"/></a>, <xsl:value-of select="//titleStmt/author"/>
	 <xsl:value-of select="//titleStmt/editor"/>
  </p>


  <xsl:apply-templates select="div2" mode="poem"/>

  <p class="source"> from 
  <a>
   <xsl:attribute name="href">poetry/contents.php?id=<xsl:value-of select="@id"/></xsl:attribute>
     <xsl:value-of select="//titleStmt/title"/></a>, <xsl:value-of select="//titleStmt/author"/>
	 <xsl:value-of select="//titleStmt/editor"/>
  </p>

  <xsl:variable name="myid"><xsl:value-of select="div2/@id"/></xsl:variable>
  <p class="next-prev">Continue browsing this volume:<br/>
   <xsl:apply-templates select="//div/siblings/div2[@id=$myid]" mode="prev"/>
   <xsl:apply-templates select="//div/siblings/div2[@id=$myid]" mode="next"/>
</p>


  <xsl:apply-templates select="teiHeader"/>
</xsl:template>

<xsl:template match="div2" mode="poem">
 <table class="poem">
  <tr><td>
   <!-- ignore docAuthor in poem mode -->
   <xsl:apply-templates select="*[not(self::docAuthor)]"/>
  </td></tr>
 </table>

  <xsl:call-template name="endnotes"/>
</xsl:template>

<!-- offset div3 poems a little, and give them a name anchor to link to -->
<xsl:template match="div3[@type='poem']">
 <table class="poem">
  <tr><td>
  <a>
   <xsl:attribute name="name"><xsl:value-of select="@id"/></xsl:attribute>
  </a>
  <xsl:apply-templates select="*[not(self::docAuthor)]"/>  
  </td></tr>
 </table>

</xsl:template>

 <!-- create toggle image -->
<xsl:template name="toggle-image">
  <xsl:param name="id"/>
   <xsl:element name="a">
     <xsl:element name="img">
       <xsl:attribute name="onclick">javascript:toggle_ul('<xsl:value-of select="$id"/>')</xsl:attribute>
       <xsl:attribute name="href">javascript:toggle_ul('<xsl:value-of select="$id"/>')</xsl:attribute>
       <xsl:attribute name="src">images/closed.gif</xsl:attribute>
       <xsl:attribute name="id"><xsl:value-of select="concat($id,'-gif')"/></xsl:attribute>
     </xsl:element> <!-- img -->
   </xsl:element> <!-- a -->
</xsl:template>


<xsl:template name="lastname">
  <xsl:param name="author"/>
  
  <xsl:choose>
    <xsl:when test="contains($author, ',')">
	<xsl:value-of select="substring-before($author, ',')"/>
    </xsl:when>
    <xsl:otherwise>
	<xsl:value-of select="$author"/>
    </xsl:otherwise>
  </xsl:choose>

</xsl:template>


<xsl:template match="siblings/div2" mode="next">
 <!-- if sibling exists, link to it -->
 <xsl:if test="following-sibling::div2">
  Next poem: 
  <a>
    <xsl:attribute name="href">poetry/view.php?id=<xsl:value-of select="following-sibling::div2/@id"/></xsl:attribute>
    <xsl:attribute name="rel">next</xsl:attribute>
    <xsl:value-of select="following-sibling::div2/@n"/>
  </a>
  <xsl:if test="following-sibling::div2/docAuthor">
    - <xsl:value-of select="following-sibling::div2/docAuthor"/>
  </xsl:if>
  <br/>
 </xsl:if>
</xsl:template>

<xsl:template match="siblings/div2" mode="prev">
 <!-- if sibling exists, link to it -->
 <xsl:if test="preceding-sibling::div2">
  Previous poem: 
  <a>
    <xsl:attribute name="href">poetry/view.php?id=<xsl:value-of select="preceding-sibling::div2[1]/@id"/></xsl:attribute>
    <xsl:attribute name="rel">prev</xsl:attribute>
    <xsl:value-of select="preceding-sibling::div2[1]/@n"/>
  </a> 
  <xsl:if test="preceding-sibling::div2/docAuthor">
    - <xsl:value-of select="preceding-sibling::div2[1]/docAuthor"/>
  </xsl:if>
  <br/>
</xsl:if>
</xsl:template>


</xsl:stylesheet>
