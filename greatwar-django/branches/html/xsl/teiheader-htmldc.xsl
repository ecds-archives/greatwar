<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

  <xsl:output method="html"/>

  <xsl:template match="/">
    <link rel="schema.DC" href="http://purl.org/dc/elements/1.1/" />
    <link rel="schema.DCTERMS" href="http://purl.org/dc/terms/" />
    <xsl:apply-templates select="//teiHeader"/>
  </xsl:template>

  <xsl:template match="titleStmt/title">
    <xsl:element name="meta">
      <xsl:attribute name="name">DC.title</xsl:attribute>
      <xsl:attribute name="content"><xsl:value-of select="."/></xsl:attribute>
    </xsl:element>
  </xsl:template>

  <xsl:template match="titleStmt/author">
    <xsl:element name="meta">
      <xsl:attribute name="name">DC.creator</xsl:attribute>
      <xsl:attribute name="content"><xsl:apply-templates/></xsl:attribute>
    </xsl:element>
  </xsl:template>

  <xsl:template match="titleStmt/editor">
    <xsl:element name="meta">
      <xsl:attribute name="name">DC.contributor</xsl:attribute>
      <xsl:attribute name="content"><xsl:apply-templates/></xsl:attribute>
    </xsl:element>
  </xsl:template>

  <xsl:template match="publicationStmt/publisher">
    <xsl:element name="meta">
      <xsl:attribute name="name">DC.publisher</xsl:attribute>
      <xsl:attribute name="content"><xsl:apply-templates/></xsl:attribute>
    </xsl:element>
  </xsl:template>

  <!-- ignore for now; do these fit anywhere? -->
  <xsl:template match="publicationStmt/address"/>
  <xsl:template match="publicationStmt/pubPlace"/>
  <xsl:template match="publicationStmt/date"/>
  <xsl:template match="respStmt"/>


  <xsl:template match="availability">
    <xsl:element name="meta">
      <xsl:attribute name="name">DC.rights</xsl:attribute>
      <xsl:attribute name="content"><xsl:apply-templates/></xsl:attribute>
    </xsl:element>
  </xsl:template>

  <xsl:template match="seriesStmt/title">
    <xsl:element name="meta">
      <!-- fixme: should we specify isPartOf? -->
      <xsl:attribute name="name">DC.relation</xsl:attribute>
      <xsl:attribute name="content"><xsl:apply-templates/></xsl:attribute>
    </xsl:element>
  </xsl:template>

  <xsl:template match="sourceDesc/bibl">
    <xsl:element name="meta">
      <xsl:attribute name="name">DC.source</xsl:attribute>
      <xsl:attribute name="content"><xsl:apply-templates/></xsl:attribute>
    </xsl:element>
  </xsl:template>

  <xsl:template match="bibl/author"><xsl:apply-templates/>. </xsl:template>
  <xsl:template match="bibl/title"><xsl:apply-templates/>. </xsl:template>
  <xsl:template match="bibl/editor">
    <xsl:text>Ed. </xsl:text><xsl:apply-templates/><xsl:text>. </xsl:text>
  </xsl:template>
  <xsl:template match="bibl/pubPlace"><xsl:apply-templates/>: </xsl:template>
  <xsl:template match="bibl/publisher"><xsl:apply-templates/>, </xsl:template>
  <xsl:template match="bibl/date"><xsl:apply-templates/>.</xsl:template>

  <xsl:template match="text()">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

</xsl:stylesheet>
