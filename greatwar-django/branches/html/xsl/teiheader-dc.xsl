<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
		xmlns:dc="http://purl.org/dc/elements/1.1/"
                version="1.0">

  <xsl:output method="xml"/>

  <xsl:template match="/">
    <dc>
    <xsl:apply-templates select="//teiHeader"/>
    <dc:type>Text</dc:type>
    <dc:format>text/xml</dc:format>
    </dc>
  </xsl:template>

  <xsl:template match="titleStmt/title">
    <xsl:element name="dc:title">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="titleStmt/author">
    <xsl:element name="dc:creator">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="titleStmt/editor">
    <xsl:element name="dc:contributor">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="publicationStmt/publisher">
    <xsl:element name="dc:publisher">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <!-- electronic publication date: is this the right date to use? -->
  <xsl:template match="publicationStmt/date">
    <xsl:element name="dc:date">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>


  <!-- ignore for now; do these fit anywhere? -->
  <xsl:template match="publicationStmt/address"/>
  <xsl:template match="publicationStmt/pubPlace"/>
  <xsl:template match="respStmt"/>

  <xsl:template match="availability">
    <xsl:element name="dc:rights">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="seriesStmt/title">
    <xsl:element name="dc:relation">
      <!-- fixme: should we specify isPartOf? -->
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="sourceDesc/bibl">
    <xsl:element name="dc:source">
      <!-- process all elements, in this order. -->
      <xsl:apply-templates select="author"/>
      <xsl:apply-templates select="title"/>
      <xsl:apply-templates select="editor"/>
      <xsl:apply-templates select="pubPlace"/>
      <xsl:apply-templates select="publisher"/>
      <xsl:apply-templates select="date"/>
      <!-- in case source is in plain text, without tags -->
      <xsl:apply-templates select="text()"/>
    </xsl:element>
  </xsl:template>

  <!-- formatting for bibl elements, to generate a nice citation. -->
  <xsl:template match="bibl/author"><xsl:apply-templates/>. </xsl:template>
  <xsl:template match="bibl/title"><xsl:apply-templates/>. </xsl:template>
  <xsl:template match="bibl/editor">
    <xsl:text>Ed. </xsl:text><xsl:apply-templates/><xsl:text>. </xsl:text>
  </xsl:template>
  <xsl:template match="bibl/pubPlace">
	<xsl:if test=". != ''">
          <xsl:apply-templates/>:
        </xsl:if>
  </xsl:template>
  <xsl:template match="bibl/publisher">
    <xsl:if test=". != ''">
      <xsl:apply-templates/>, 
    </xsl:if>
  </xsl:template>
  <xsl:template match="bibl/date"><xsl:apply-templates/>.</xsl:template>


  <xsl:template match="encodingDesc/projectDesc">
    <xsl:element name="dc:description">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="profileDesc/creation/date">
    <xsl:element name="dc:coverage">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="profileDesc/creation/rs[@type='geography']">
    <xsl:element name="dc:coverage">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <!-- ignore other rs types for now -->
  <xsl:template match="profileDesc/creation/rs[@type!='geography']"/>

  <!-- ignore these: encoding specific information -->
  <xsl:template match="encodingDesc/tagsDecl"/>
  <xsl:template match="encodingDesc/refsDecl"/>
  <xsl:template match="encodingDesc/editorialDecl"/>
  <xsl:template match="revisionDesc"/>

  <!-- normalize space for all text nodes -->
  <xsl:template match="text()">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

</xsl:stylesheet>
