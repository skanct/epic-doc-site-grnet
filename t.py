#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from lxml.objectify import parse
import urllib2
request = urllib2.Request
urlopen = urllib2.urlopen
 
xpath_ns = {'ds': 'http://www.w3.org/2000/09/xmldsig#',
            'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
            'mdrpi': 'urn:oasis:names:tc:SAML:metadata:rpi',
            'mdui': 'urn:oasis:names:tc:SAML:metadata:ui',
            'shibmd': 'urn:mace:shibboleth:metadata:1.0',
            'xi': 'http://www.w3.org/2001/XInclude',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
 
edugain_dataset = {
    'ACOnet (AT)': 'http://eduid.at',
    'Belnet (BE)': 'http://federation.belnet.be/',
    'CaFe (BR)': 'http://cafe.rnp.br',
    'CAF (CA)': 'http://www.canarie.ca',
    'COFRe (CL)': 'http://cofre.reuna.cl',
    'AAI@EduHr (HR)': 'http://www.aaiedu.hr',
    'eduID.cz (CZ)': 'http://www.eduid.cz/',
    'WAYF (DK)': 'https://www.wayf.dk',
    'HAKA (FI)': 'http://www.csc.fi/haka',
    'FER (FR)': 'https://federation.renater.fr/',
    'DFN (DE)': 'https://www.aai.dfn.de',
    'GRNET (GR)': 'http://aai.grnet.gr/',
    'eduId.hu (HU)': 'http://eduid.hu',
    'IDEM (IT)': 'http://www.idem.garr.it/',
    'LAIFE (LV)': 'http://laife.lanet.lv/',
    'FEIDE (NO)': 'http://feide.no/',
    'SIR (ES)': 'http://www.rediris.es/',
    'SWAMID (SE)': 'http://www.swamid.se/',
    'SWITCHaai (CH)': 'http://rr.aai.switch.ch/',
    'SURFfederatie (NL)': 'http://www.surfconext.nl/',
    'UK federation (UK)': 'http://ukfederation.org.uk'
}
 
national_dataset = {
    'ACOnet (AT)': 'http://wayf.aco.net/aconet-metadata.xml',
    'Belnet (BE)': 'https://federation.belnet.be/federation-metadata.xml',
    'CaFe (BR)': 'https://ds.cafe.rnp.br/metadata/cafe-metadata.xml',
    'CAF (CA)': 'https://caf-shib2ops.ca/CoreServices/caf_metadata_signed.xml',
    'COFRe (CL)': 3,
    'AAI@EduHr (HR)': 223,
    'eduID.cz (CZ)': 'https://metadata.eduid.cz/entities/eduid',
    'WAYF (DK)': 'https://wayf.wayf.dk/saml2/idp/metadata.php',
    'HAKA (FI)': 'https://haka.funet.fi/metadata/haka-metadata.xml',
    'FER (FR)': 'https://services-federation.renater.fr/metadata/renater-metadata.xml',
    'DFN (DE)': 'http://www.aai.dfn.de/fileadmin/metadata/DFN-AAI-metadata.xml',
    'GRNET (GR)': 'http://aai.grnet.gr/grnet-metadata.xml',
    'eduId.hu (HU)': 'http://metadata.eduid.hu/current/href.xml',
    'IDEM (IT)': 'https://www.idem.garr.it/docs/conf/signed-metadata.xml',
    'LAIFE (LV)': 'https://laife.lanet.lv/metadata/laife-metadata.xml',
    'FEIDE (NO)': 'https://idp.feide.no/simplesaml/saml2/idp/metadata.php',
    'SIR (ES)': 'https://www.rediris.es/sir/shib1metadata.xml',
    'SWAMID (SE)': 'http://md.swamid.se/md/swamid-2.0.xml',
    'SWITCHaai (CH)': 'http://metadata.aai.switch.ch/metadata.switchaai.xml',
    'SURFfederatie (NL)': 'http://federatie.surfnet.nl/metadata-sfs-idp-saml20-signed.xml',
    'UK federation (UK)': 'http://metadata.ukfederation.org.uk/ukfederation-metadata.xml'
}
 
md_edugain = urlopen(request('http://mds.edugain.org/'))
md_edugain = parse(md_edugain).getroot()
 
for fed in edugain_dataset:
    fed_edugain_idps = md_edugain.xpath(
        """//md:EntityDescriptor[md:IDPSSODescriptor and 
md:Extensions/mdrpi:RegistrationInfo/@registrationAuthority and 
(md:Extensions/mdrpi:RegistrationInfo/@registrationAuthority='%s')]""" %
        edugain_dataset[fed],
        namespaces=xpath_ns)
    fed_edugain_idps_count = len(fed_edugain_idps)
 
    if isinstance(national_dataset[fed], int):
        fed_national_idps_count = national_dataset[fed]
    else:
        try:
            md_national = urlopen(request(national_dataset[fed]))
        except AttributeError:
            print md_national
        md_national = parse(md_national).getroot()
        fed_national_idps = md_national.xpath(
            "//md:EntityDescriptor[md:IDPSSODescriptor]",
            namespaces=xpath_ns)
        fed_national_idps_count = len(fed_national_idps)
 
    try:
        fed_idps_percent = (fed_edugain_idps_count * 100) / \
            fed_national_idps_count
    except ZeroDivisionError:
        print "ZeroDivisionError"
        fed_idps_percent = 0
 
    print "%-24s %3d %3d %3d%%" % (fed, fed_edugain_idps_count,
                                   fed_national_idps_count, fed_idps_percent)
