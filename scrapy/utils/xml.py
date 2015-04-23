import os
from lxml import etree
from scrapy import log

def read_xml(path):
    """
    Parses the xml file from path
    """
    if os.path.exists(path):
        try:
            return etree.parse(path)
        except IOError as error:
            log.err('The file %s cannot be read'%path)
            log.err(str(error))
            return None
        except etree.XMLSyntaxError as e:
            log.err('lxml: The file %s does not contain valid XML.\n %s'%(path, e))
            return None
        except:
            log.err('lxml: Unknown parsing error %s'%path)
            return None
    else:
        log.err('File %s not found'%path)
        return None

def get_xslt(path):
    """
    Returns etree xslt transform
    
    @param path: The path to the template to use for the transform
    """
    try:
        xsl = read_xml(path)
        xslt = etree.XSLT(xsl)
    except etree.XSLTParseError as error:
        log.err('lxml: Invalid XSL in the file %s\n%s'%(path, error))
        return None
    except Exception as e:
        log.err('lxml: Unknown XSL parsing error in file %s.'%path)
        log.err(e)
        return None
    return xslt

def apply_xslt(path, xslt):
    """
    Processes XML file from path with xslt and return the result.

    @param path: path to XML file
    @xslt xsl transform used
    @return: the transformed XML text as elementTree object, or None if an error occured
    """
    xml = read_xml(path)
    try:
        result = xslt(xml)
        log.msg('XSLT of %s was successful.\n%s'%(os.path.basename(path), xslt.error_log))
    except Exception as excp:
        log.err('lxml: Error during XSLT of file %s'%path)
        log.err(xslt.error_log) 
        return None
    return result