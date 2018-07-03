<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns="http://www.w3.org/TR/REC-html40">
<xsl:template match="/">
  <xsl:text disable-output-escaping="yes">
<!DOCTYPE rdf:RDF [
    <!ENTITY ebi "http://www.ebi.ac.uk/" >
    <!ENTITY swo "http://www.ebi.ac.uk/swo/" >
    <!ENTITY owl "http://www.w3.org/2002/07/owl#" >
    <!ENTITY obo "http://purl.obolibrary.org/obo/" >
    <!ENTITY dc "http://purl.org/dc/elements/1.1/" >
    <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >
    <!ENTITY owl2xml "http://www.w3.org/2006/12/owl2-xml#" >
    <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >
    <!ENTITY organization "http://www.ebi.ac.uk/swo/organization/" >
    <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >
  ]>

  <rdf:RDF xmlns="viscat_software/"
       xml:base=""
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:obo="http://purl.obolibrary.org/obo/"
       xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
       xmlns:organization="&ebi;swo/organization/"
       xmlns:owl2xml="http://www.w3.org/2006/12/owl2-xml#"
       xmlns:swo="&ebi;swo/"
       xmlns:owl="http://www.w3.org/2002/07/owl#"
       xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
       xmlns:ebi="http://www.ebi.ac.uk/">
    <owl:Ontology rdf:about="viscat_software/">
      <owl:versionInfo>0.4</owl:versionInfo>
    </owl:Ontology>
    </xsl:text>
<xsl:for-each select="catalogue/software">
<xsl:value-of select="title"/>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>

