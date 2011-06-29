<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0"
		xmlns:tei="http://www.tei-c.org/ns/1.0">

<xsl:include href="teipoetry.xsl"/>

  <xsl:output method="xml"/>

  <xsl:template match="/">
    <div>    <!-- need div wrapper to make well-formed xml for eulcore -->
    <xsl:apply-templates/>
    <xsl:call-template name="endnotes"/> <!-- need to specifically call endnotes template -->
    </div>
  </xsl:template>

  <xsl:template match="tei:div[@type='poem']">
    <div class="poem">
      <div class="poem-body">
      <!-- ignore docAuthor in poem mode -->
      <xsl:apply-templates select="*[not(self::tei:docAuthor)]"/>
      </div>
    </div>
  </xsl:template>


</xsl:stylesheet>
