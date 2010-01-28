<?xml version="1.0" encoding="ISO-8859-1"?>  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:html="http://www.w3.org/TR/REC-html40" 
	xmlns:ino="http://namespaces.softwareag.com/tamino/response2" 
	xmlns:xql="http://metalab.unc.edu/xql/">


<xsl:param name="desc"/>
<xsl:param name="max"/>
<xsl:param name="mode"/>   
<!-- default mode: output pretty linked list; form mode: select box -->
<xsl:param name="showtitle">1</xsl:param> <!-- by default, display -->

<xsl:output method="xml" omit-xml-declaration="yes"/>  

<xsl:template match="/"> 

  <xsl:choose>
   <xsl:when test="$mode = 'form'">
      <xsl:apply-templates select="//interpGrp" mode="form"/>
   </xsl:when> 
   <xsl:otherwise>
  <!-- NOTE: putting the javascript NOT in the header kills any content after this for Internet Explorer.  
	Any page that uses this *MUST* have the toggle-list.js included for functionality. --> 
     <!--      <xsl:element name="script">
        <xsl:attribute name="type">text/javascript</xsl:attribute>
        <xsl:attribute name="language">Javascript</xsl:attribute>
        <xsl:attribute name="src">toggle-list.js</xsl:attribute>
      </xsl:element>  --> <!-- script -->

     <xsl:if test="$showtitle = 1">
      <h3>Categories</h3>
     </xsl:if>
      <xsl:apply-templates select="//interpGrp" />
   </xsl:otherwise>
  </xsl:choose>

</xsl:template> 


<xsl:template match="interpGrp">

<h4>
   <!-- create toggle image -->
   <xsl:element name="a">
       <xsl:attribute name="onclick">javascript:toggle_ul('<xsl:value-of select="@type"/>')</xsl:attribute>
<!--      <xsl:attribute name="onclick">toggle_ul('list<xsl:value-of select="$num"/>')</xsl:attribute> -->
     <xsl:element name="img">
       <xsl:attribute name="alt">.</xsl:attribute>
       <xsl:attribute name="href">javascript:toggle_ul('<xsl:value-of select="@type"/>')</xsl:attribute>
       <xsl:attribute name="src">images/closed.gif</xsl:attribute>
       <xsl:attribute name="id"><xsl:value-of select="concat(@type,'-gif')"/></xsl:attribute>
     </xsl:element> <!-- img -->

     <xsl:value-of select="@type"/>
   </xsl:element> <!-- a -->

</h4>

  <ul>
    <xsl:attribute name="id"><xsl:value-of select="@type"/></xsl:attribute>
    <xsl:apply-templates select="interp"/>
  </ul>
</xsl:template>

<xsl:template match="interp">
  <li>
   <xsl:element name="a">
     <xsl:attribute name="href">postcards/browse.php?cat=<xsl:value-of
select="@id"/><xsl:if test="$desc">&amp;desc=<xsl:value-of select="$desc"/></xsl:if><xsl:if test="$max">&amp;max=<xsl:value-of select="$max"/></xsl:if></xsl:attribute>
<!-- only pass along display-description setting and max display if defined -->
     <xsl:value-of select="@value"/>
   </xsl:element>
   <xsl:if test="@n != ''">	 <!-- display nothing if there is no count value -->
    <font class="count">(<xsl:value-of select="@n"/>)</font>
   </xsl:if>
  </li>
</xsl:template>

<xsl:template match="interpGrp" mode="form">
  <!-- translate any spaces to dashes for easier passing as http variables -->
  <xsl:variable name="space"> </xsl:variable>
  <xsl:variable name="dash">-</xsl:variable>
  <tr><th><xsl:value-of select="@type"/></th>
  <td>
  <select>
    <xsl:attribute name="name"><xsl:value-of select="translate(@type,$space,$dash)"/></xsl:attribute>
    <option selected="true" value="null">--</option>
    <xsl:apply-templates mode="form"/>
  </select>
  </td></tr>
</xsl:template>

<xsl:template match="interp" mode="form">
  <option>
   <xsl:attribute name="value"><xsl:value-of select="@id"/></xsl:attribute>
    <xsl:value-of select="@value"/>
  </option>
</xsl:template>


</xsl:stylesheet>
