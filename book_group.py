import requests
import re
from lxml import etree

isbns = ['9780241242377', '9781250054265', '9781501125799', '9781786074102', '9781478970392', '9780143131144']
with open('books.txt', 'w') as f:
    for isbn in isbns:
        isbn = re.sub('\D', '', isbn)
        item_info = {}
        result = {}
        #DC
        session = requests.session()
        base_url = 'https://catalog.dclibrary.org/'
        search_url = 'client/en_US/dcpl/search/results?qu='
        req = session.get(base_url + search_url + isbn)
        root = etree.HTML(req.content)
        if not root.xpath('.//div[contains(@class, "searchResults_wrapper")]/div[contains(@id, "no_results_wrapper")]'):
            for element in root.xpath('.//div[contains(@class, "displayElementText")]'):
                if 'class' in element.attrib.keys():
                    item_info[element.attrib['class'].split()[1]] = element.text
            if 'DCPL_245' in item_info.keys():
                f.write('{}\n'.format(item_info['DCPL_245']))
                f.write('{}\n\n'.format(item_info['ABSTRACT']))
            else:
                f.write('{}\n'.format(item_info['TITLE']))
                f.write('{}\n\n'.format(item_info['DESCRIPTION']))
            f.write('\tAvailability\n')
            try:
                service_url = re.findall('\'(.*lookupavailability.*?)\'', req.text)[0]
                req = session.get(base_url + service_url)
                result['copies'] = re.findall('"copyCount"\s+:\s+"(\d+)",', req.text)
                result['available'] = re.findall('"availableCount"\s+:\s+"(\d+)",', req.text)
                result['holds'] = re.findall('"holdCount"\s+:\s+"(\d+)",', req.text)
            except:
                pass
            f.write('\tDC {}\n'.format(str(result)))
            print(item_info)
    
        #MoCo
        result = {}
        base_url = 'https://mdpl.ent.sirsi.net/'
        search_url = 'client/en_US/catalog/search/results?qu='
        req = session.get(base_url + search_url + isbn)
        try:
            text = re.findall('parseDetailAvailabilityJSON\(\{.*?\}\);', req.text, re.DOTALL)[0]
            text = re.sub('\s+', '', text)
            result['copies'] = re.findall('"copies":\["\d+,(\d+)"\],', text)
            result['available'] = re.findall('"totalAvailable":(\d+),', text)
            result['holds'] = re.findall('"holdCounts":\["\d+,(\d+)"\],', text)
        except:
            pass
        if len(item_info):
            f.write('\tMoCo {}\n\n'.format(str(result)))
    
