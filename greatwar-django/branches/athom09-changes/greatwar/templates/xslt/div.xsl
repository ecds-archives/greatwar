<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0"
		xmlns:tei="http://www.tei-c.org/ns/1.0">

<xsl:include href="teipoetry.xsl"/>

  <xsl:output method="xml"/>

  <xsl:template match="/">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="tei:div[@type='poem']">
    <div class="poem">
      <!-- ignore docAuthor in poem mode -->
      <xsl:apply-templates select="*[not(self::tei:docAuthor)]"/>
    </div>
  </xsl:template>


</xsl:stylesheet>
