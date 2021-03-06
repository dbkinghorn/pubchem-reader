#!/usr/bin/env python

# bring in the ZSI-generated interface from
# wsdl2py --complexType --url='http://pubchem.ncbi.nlm.nih.gov/pug_soap/pug_soap.cgi?wsdl'
from PUG_services import *

# other modules/functions
from time import sleep
from urllib import urlopen, urlretrieve
import sys
import openbabel


def DownloadCIDs(CID_list):
    """Download the PubChem data files for the listed CID's
    
    The PubChem SOAP interface is used to access the database  
    
    Keyword arguments:
    
    CID_list -- list of CIDS :-) as a list of one or more ints
    
    Returns: file_handle
    
    """
    
    # get a PUG SOAP port instance
    loc = PUGLocator()
    port = loc.getPUGSoap()
    
    # start with a list of CIDs
    req = InputListSoapIn()
    req.set_element_ids(req.new_ids())
    req.get_element_ids().set_element_int(CID_list)
    req.set_element_idType('eID_CID')
    listKey = port.InputList(req).get_element_ListKey()
    print 'ListKey =', listKey
    
    # request download in XML format, no compression, 3D coords
    req = DownloadSoapIn();
    req.set_element_ListKey(listKey)
    req.set_element_eFormat('eFormat_XML')
    req.set_element_eCompress('eCompress_None')
    req.set_element_Use3D('True')
    downloadKey = port.Download(req).get_element_DownloadKey()
    print 'DownloadKey =', downloadKey
    
    # call GetOperationStatus until the operation is finished
    req = GetOperationStatusSoapIn()
    req.set_element_AnyKey(downloadKey)
    status = port.GetOperationStatus(req).get_element_status()
    while (status == 'eStatus_Queued' or status == 'eStatus_Running'):
        print 'Waiting for operation to finish...'
        sleep(10)
        status = port.GetOperationStatus(req).get_element_status()
        
    # check status
    if (status == 'eStatus_Success'):
        
        # get the url of the prepared file
        req = GetDownloadUrlSoapIn()
        req.set_element_DownloadKey(downloadKey)
        url = port.GetDownloadUrl(req).get_element_url()
        print 'Success! URL =', url
        
        # download to an internal file handle 
        #fh = urlopen(url)
        (filename, headers) = urlretrieve(url, "pubchem-data.pc")
        print "Downloaded to ", filename
        
        return filename, CID_list

        
        
    else:   # status indicates error
        
        # see if there's some explanatory message
        req = GetStatusMessageSoapIn()
        req.set_element_AnyKey(downloadKey)
        print 'Error:', port.GetStatusMessage(req).get_element_message()


def ParseMolFile(pubchem_XMLdata_file, CID):
    """Use openbabel to pull the coord info from PubChem data file.
    
    Keyword arguments:
    
    pubchem_XMLdata_file -- the standard PubChem compound XML format file.
    """
    
   # pc_data = pubchem_XMLdata_file.read()
    
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("pc", "xyz")
    
    mol = openbabel.OBMol()
    obConversion.ReadFile(mol, pubchem_XMLdata_file)
    obConversion.WriteFile(mol, str(CID[0])+".xyz")
    
    

if __name__ == '__main__':
    (CID_info, CID) = DownloadCIDs([2])
    ParseMolFile(CID_info, CID)
    
