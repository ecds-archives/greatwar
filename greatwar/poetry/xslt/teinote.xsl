<?xml version="1.0" encoding="utf-8"?>  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:html="http://www.w3.org/TR/REC-html40" 
	xmlns:tei="http://www.tei-c.org/ns/1.0" >

<!-- handle footnotes -->

<xsl:template match="tei:ref">
  <xsl:variable name="target"><xsl:value-of select="substring-after(@target,'#')"/></xsl:variable>
  <a>
  <xsl:attribute name="name"><xsl:value-of select="concat($target,'-link')"/></xsl:attribute>
  <xsl:attribute name="href"><xsl:value-of select="@target"/></xsl:attribute>
  <xsl:attribute name="class">footnote</xsl:attribute>
  <xsl:apply-templates/>
  </a>
</xsl:template>

<!-- handle inline note  -->
<xsl:template match="tei:note[@place='inline']">
  <p class="inline-note">
   <xsl:apply-templates/>
  </p>
</xsl:template>

<!-- in normal mode, do nothing : only process at end -->
<xsl:template match="tei:note"/>

<!-- generate text of actual notes -->
<!-- Note: this template MUST be explicitly called, after the main text is
     processed -->
<xsl:template name="endnotes">
<!-- only display endnote div if there actually are notes -->
  <xsl:if test="count(//tei:note) > 0">
    <div class="endnote">
      <h2>Notes</h2>
      <xsl:apply-templates select="//tei:note" mode="end"/>
    </div>
 </xsl:if>    
</xsl:template>

<!-- note, endnote mode : display number and content of note; 
     link back to ref in the text 
     (do not handle inline notes here)
-->
<xsl:template match="tei:note[@place!='inline']" mode="end">
  <xsl:element name="p">
    <xsl:attribute name="class">footnote</xsl:attribute>
    <xsl:element name="a">
      <xsl:attribute name="name"><xsl:value-of select="@xml:id"/></xsl:attribute>
      <xsl:attribute name="href"><xsl:value-of select="concat('#',@xml:id,'-link')"/></xsl:attribute>
      <xsl:attribute name="title">Return to text</xsl:attribute>
        <xsl:value-of select="@n"/> 
    </xsl:element>. <!-- a -->
 
  <xsl:apply-templates mode="endnote"/>

  <!-- special case: properly display poetry within a note -->
  <xsl:if test="count(.//tei:l) > 0">
   <table border="0">
      <tr><td>
        <xsl:apply-templates select="tei:l"/>
      </td></tr>
    </table>
  </xsl:if>    
  </xsl:element> <!-- p -->

</xsl:template>

<xsl:template match="tei:note/tei:p" mode="endnote">
   <xsl:apply-templates/><br/>
</xsl:template>

<!-- handle poetry lines within a note separately -->
<xsl:template match="tei:note/tei:l" mode="endnote">
</xsl:template>


</xsl:stylesheet>