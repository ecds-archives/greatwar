<?xml version="1.0" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	 version="1.1">


<xsl:output method="xml" encoding="utf-8"/>  

<xsl:template match="/">
  <xsl:apply-templates/>
</xsl:template>

<xsl:key name="figure" match="figure" use="@ana"/>

<!-- count how many postcards are in each interp category, and store
count in the n attribute -->
<xsl:template match="interp">
<xsl:variable name="id"><xsl:value-of select="@id"/></xsl:variable>
  <xsl:element name="interp">
    <xsl:apply-templates select="@*"/>
   <xsl:attribute name="n"><xsl:value-of select="count(/TEI.2/text/body/p/figure[contains(@ana, $id)])"/></xsl:attribute>
  </xsl:element>
</xsl:template>

<!-- default action: copy node as is -->
<xsl:template match="@*|node()">
	<xsl:copy>
	<xsl:apply-templates select="@*|node()"/>
	</xsl:copy>
</xsl:template>

</xsl:stylesheet>