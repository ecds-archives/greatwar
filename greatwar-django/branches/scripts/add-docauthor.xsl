<?xml version="1.0" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	 version="1.1">

<!-- This xsl adds a docAuthor tag at the div2 level.
     It takes the docAuthor value from the byline field within the
     div2, and does some additional cleaning up of that data.
     It is intended for use with anthologies, which do not have
     the same author for the entire document. 

     Note: any author bylines that are only initials will most likely
     need to be handled manually. 
-->

<xsl:template match="/">

  <xsl:apply-templates/>

</xsl:template>

<xsl:template match="div2">
  <xsl:element name="div2">
     <!-- grab all the attributes -->
    <xsl:apply-templates select="@*"/>
<!--    <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
    <xsl:attribute name="n"><xsl:value-of select="@n"/></xsl:attribute>
    <xsl:attribute name="type"><xsl:value-of
select="@type"/></xsl:attribute>
-->

   <xsl:if test="byline">
    <xsl:variable name="author">
      <xsl:call-template name="fix-author">
	<xsl:with-param name="author"><xsl:value-of select="./byline"/></xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:element name="docAuthor">
      <xsl:attribute name="n">
        <xsl:call-template name="name-invert">
	  <xsl:with-param name="name"><xsl:value-of select="$author"/></xsl:with-param>
        </xsl:call-template>
      </xsl:attribute>
      <xsl:value-of select="$author"/>
    </xsl:element>  <!-- docAuthor -->
  </xsl:if>

    <xsl:apply-templates/>
  </xsl:element>
</xsl:template>


<!-- default action: copy node as is -->
<xsl:template match="@*|node()">
	<xsl:copy>
	<xsl:apply-templates select="@*|node()"/>
	</xsl:copy>
</xsl:template>


<xsl:template name="name-invert">
 <xsl:param name="name"/>

 <xsl:variable name="name1">
  <xsl:choose>
   <xsl:when test="contains($name, ' ')">
     <xsl:value-of select="substring-after($name, ' ')"/>
   </xsl:when> 
   <xsl:otherwise>
     <xsl:value-of select="$name"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:variable>

 <xsl:variable name="lastname">
  <xsl:choose>
   <xsl:when test="contains($name1, ' ')">
     <xsl:value-of select="substring-after($name1, ' ')"/>
   </xsl:when> 
   <xsl:otherwise>
     <xsl:value-of select="$name1"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:variable>

 <xsl:variable name="firstname">
   <xsl:value-of select="substring($name, 1, (string-length($name) - string-length($lastname) - 1))"/>
 </xsl:variable>

 <xsl:value-of select="concat($lastname, ', ', $firstname)"/>

</xsl:template>

<!-- clean up author names from byline tag -->
<xsl:template name="fix-author">
 <xsl:param name="author"/>

<!-- first pass: remove comma and any following description of author -->
 <xsl:variable name="auth1">
    <xsl:choose>
     <xsl:when test="contains($author, ',')">
       <xsl:value-of select="substring-before($author, ',')"/>
     </xsl:when>
     <xsl:otherwise>
       <xsl:value-of select="$author"/>
     </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

<!-- second pass: fix case of letters -->
 <xsl:variable name="auth2">
   <xsl:call-template name="convertpropercase">
     <xsl:with-param name="str"><xsl:value-of select="normalize-space($auth1)"/></xsl:with-param>
    </xsl:call-template>
 </xsl:variable>

 <!-- third pass: remove final period -->
 <xsl:variable name="len"><xsl:value-of select="string-length($auth2)"/></xsl:variable>
 <xsl:variable name="lastlet">
   <xsl:value-of select="substring($auth2,($len - 1))"/>
 </xsl:variable>

 <xsl:choose>
   <!-- no spaces = all initials; leave final period as is -->
   <xsl:when test="not(contains($auth2,' '))">	
      <xsl:value-of select="$auth2"/>
   </xsl:when>
   <!-- remove final period -->
   <xsl:when test="contains($lastlet,'.')">
     <xsl:value-of select="substring($auth2,1,($len -1))"/>
   </xsl:when>
   <xsl:otherwise>
      <xsl:value-of select="$auth2"/>
   </xsl:otherwise>
 </xsl:choose>

</xsl:template>

<!-- templates to convert case -->

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