<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/TR/REC-html40">
<xsl:template match="/">
  <xsl:text disable-output-escaping="yes">
    &lt;!DOCTYPE rdf:RDF [
    &lt;!ENTITY ebi "http://www.ebi.ac.uk/" >
    &lt;!ENTITY swo "http://www.ebi.ac.uk/swo/" >
    &lt;!ENTITY owl "http://www.w3.org/2002/07/owl#" >
    &lt;!ENTITY obo "http://purl.obolibrary.org/obo/" >
    &lt;!ENTITY dc "http://purl.org/dc/elements/1.1/" >
    &lt;!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >
    &lt;!ENTITY owl2xml "http://www.w3.org/2006/12/owl2-xml#" >
    &lt;!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >
    &lt;!ENTITY organization "http://www.ebi.ac.uk/swo/organization/" >
    &lt;!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >
]>

  &lt;rdf:RDF xmlns="viscat_software/"
     xml:base=""
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:obo="http://purl.obolibrary.org/obo/"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
     xmlns:owl2xml="http://www.w3.org/2006/12/owl2-xml#"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:ebi="http://www.ebi.ac.uk/">
    &lt;owl:Ontology rdf:about="viscat_software/">
        &lt;owl:versionInfo>0.4&lt;/owl:versionInfo>
    &lt;/owl:Ontology>
  </xsl:text>
  <xsl:for-each select="catalogue/software">
    <!-- Software ID-->
    <xsl:text disable-output-escaping="yes">
    &lt;owl:Class rdf:about="&amp;obo</xsl:text>;SOFT_<xsl:value-of select="position()"/>"<xsl:text disable-output-escaping="yes">></xsl:text>
    
    <!-- Label -->
    <xsl:text disable-output-escaping="yes">   
        &lt;rdfs:label></xsl:text>   
    <xsl:value-of select="label"/>
    <xsl:text disable-output-escaping="yes">&lt;/rdfs:label></xsl:text>

    <!-- SubClass of Software -->
    <xsl:text disable-output-escaping="yes">
        &lt;rdfs:subClassOf rdf:resource="http://www.ebi.ac.uk/swo/SWO_0000001"/></xsl:text>
    
    <!-- Homepage -->
    <xsl:if test="homepage">
      <xsl:text disable-output-escaping="yes">
        &lt;obo:IAO_0000119 rdf:datatype="&amp;xsd;string"></xsl:text>
      <xsl:value-of select="homepage"/>
      <xsl:text disable-output-escaping="yes">&lt;/obo:IAO_0000119&gt;</xsl:text>
    </xsl:if>
    
    <!-- Software close -->
    <xsl:text disable-output-escaping="yes">
    &lt;/owl:Class>
    </xsl:text>
    
  </xsl:for-each>
  <xsl:text disable-output-escaping="yes">
&lt;/rdf:RDF>
</xsl:text>
</xsl:template>
</xsl:stylesheet>

