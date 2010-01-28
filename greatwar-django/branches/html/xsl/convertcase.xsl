<?xml version="1.0" encoding="ISO-8859-1"?>  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:html="http://www.w3.org/TR/REC-html40" 
	xmlns:ino="http://namespaces.softwareag.com/tamino/response2" 
	xmlns:xql="http://metalab.unc.edu/xql/">

<!-- two named templates for converting words to upper case, lower
     case, or first letter of every word capitalized -->


<!-- convert all letters to either upper or lower case -->
<xsl:template name="convertcase">
  <xsl:param name="str"/>
  <xsl:param name="conversion"/>  <!-- upper/lower -->

  <xsl:variable name="lcletters">abcdefghijklmnopqrstuvwxyz</xsl:variable>
  <xsl:variable name="ucletters">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>

  <xsl:choose>
    <xsl:when test="$conversion='upper'">
      <xsl:value-of select="translate($str,$lcletters,$ucletters)"/>
    </xsl:when>
    <xsl:when test="$conversion='lower'">
      <xsl:value-of select="translate($str,$ucletters,$lcletters)"/>
    </xsl:when>
  </xsl:choose>

</xsl:template>

<!-- convert first letter of each word to upper case -->
<xsl:template name="convertpropercase">
<xsl:param name="str" />

<xsl:if test="string-length($str) > 0">
	<xsl:variable name='f' select='substring($str, 1, 1)' />
	<xsl:variable name='s' select='substring($str, 2)' />
	
	<xsl:call-template name='convertcase'>
	  <xsl:with-param name='str' select='$f'/>
	  <xsl:with-param name='conversion'>upper</xsl:with-param>
	</xsl:call-template> 

<xsl:choose>
	<xsl:when test="contains($s,' ')">
         <xsl:call-template name="convertcase">
            <xsl:with-param name="str" select='substring-before($s," ")'/>
            <xsl:with-param name="conversion">lower</xsl:with-param>
         </xsl:call-template>
		<xsl:text> </xsl:text>
		<xsl:call-template name='convertpropercase'>
		<xsl:with-param name='str' select='substring-after($s," ")' />
		</xsl:call-template>
	</xsl:when>
<!-- special case: initials without spaces -->
        <xsl:when test="contains($s, '.')">
         <xsl:call-template name="convertcase">
            <xsl:with-param name="str" select='substring-before($s,".")'/>
            <xsl:with-param name="conversion">lower</xsl:with-param>
         </xsl:call-template>
		<xsl:text>.</xsl:text>
		<xsl:call-template name='convertpropercase'>
		<xsl:with-param name='str' select='substring-after($s,".")' />
		</xsl:call-template>
        </xsl:when>
	<xsl:otherwise>
         <xsl:call-template name="convertcase">
	    <xsl:with-param name="str"><xsl:value-of select='$s'/></xsl:with-param>
            <xsl:with-param name="conversion">lower</xsl:with-param>
         </xsl:call-template>
	</xsl:otherwise>
</xsl:choose>
</xsl:if>
</xsl:template>


</xsl:stylesheet>