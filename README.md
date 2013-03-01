pubchem-reader
==============

access NCBI PubChem database via the PubChem Power User Gateway (PUG) with python


This project is intended to provide tools for accessing and parsing information from the NCBI PubChem database via the PubChem Power User Gateway (PUG)

http://pubchem.ncbi.nlm.nih.gov/pug/pughelp.html

A python interface is generated for the PUG SOAP interface using the very wonderful **ZSI** tools and the PUG DTD and XML schema.

- PUG_services_types.py
- PUG_services.py

**cid2input.py** uses this interface and provides; 

DownloadCIDs(CID_list) which sets up the database request and then downloads the requested data for the given Compound ID(s) (CID)

ParseMolFile(pubchem_XMLdata_file, CID) Is used to parses the downloaded XML file with **openbabel** to generate an XYZ format input file for use with computational chemistry packages.  

Example usage is given at the bottom of cid2input.py

Needs: python-ZSI, pyXML, python-openbabel

best of luck
-dbk
