import logging
import datetime
from bs4 import BeautifulSoup
from pymongo import UpdateOne

logger = logging.basicConfig(filename='test.log', level=logging.INFO)
BASE_URL = "https://courtconnect.courts.delaware.gov/cc/cconnect/"


class CourtCatalogueParser:
    now = datetime.datetime.now()
    created_at = now.strftime("%Y-%m-%d")
    platform = 'delaware_court'

    @classmethod
    def parse(self, response, num):
        """This function recieves a page response and returns parsed data if successful."""
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', attrs={'border': True})
            if not table:
                num = str(num)
                logging.warning(
                    f'Page {num} no longer has items. {response.url}')
                return None

            records = table.select('tr[align*="left"]')
            information = []
            for record in records[1:]:
                person_id = record.select('td[nowrap*="nowrap"]')[0].text
                party_end_date = record.select(
                    'td')[1].text.strip()
                name_or_company = record.select(
                    'td[nowrap*="nowrap"]')[1].text
                address = record.select('td')[3].text
                joint_and_several = record.select(
                    'td[align*="center"]')[0].text
                judgment_finished = record.select(
                    'td[align*="center"]')[1].text
                judgment_date = record.select(
                    'td[align*="center"]')[2].text
                url = record.select_one('a')
                try:
                    url = url['href']
                except Exception:
                    url = None
                # cleanse
                try:
                    amount = float(record.select_one(
                        'a').text.replace('$', '').replace(',', ''))
                except Exception:
                    amount = 0

                if name_or_company:
                    name_or_company = " ".join(
                        map(lambda x: x.capitalize(), name_or_company.lower().split()))

                if address and address != 'unknown':
                    address = " ".join(
                        map(lambda x: x.capitalize(), address.lower().split()))
                else:
                    address = None

                record = {
                    "person_id": person_id,
                    "party_end_date": None if not party_end_date else party_end_date,
                    "name_or_company": name_or_company,
                    "address": address,
                    "joint_and_several":  False if joint_and_several == 'No' else True,
                    "amount": amount,
                    "created_at": self.created_at,
                    "platform": self.platform,
                    "judgment_finished":  False if judgment_finished in [
                        'SATISFIED' 'unknown'] else True,
                    "judgment_date": None if 'unknown' in judgment_date else judgment_date,
                    "currency": 'USD',
                    "url": BASE_URL + url if url else None}
                information.append(record)
            logging.info(f'Parsed info correctly from page {num}')
            return information
        except Exception:
            logging.warning(
                f'Current page ({num}) could not be read. status_code: {response.status_code} | {response.url}\n')

    @classmethod
    def parse_results(self, response):
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', attrs={'border': True})
            if not table:
                num = str(num)
                logging.warning(
                    f'Page {num} has no items. {response.url}')
                return None
            i_tag = table.select_one('i').select('a')
            urls = [BASE_URL + tag['href'] for tag in i_tag]
            return urls

        except Exception:
            logging.warning(
                f'No cases available. status_code: {response.status_code} | {response.url}\n')

    @classmethod
    def parse_records(self, response, record):
        query = {
            "platform": self.platform,
            "url":      record['url'],
        }
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        try:
            case_info = tables[1].select(
                'tr[valign*="top"]')[0].find('td').get_text(strip=True).split(':')
            case_info = [{i: case_info[i]} for i in range(0, len(case_info))]
            case_title = case_info[1][1].replace('Filing Date', '')
            case_id = tables[0].find_all('tr')[0].find_all('td')[
                2].get_text().split('\n')[0]
            case_type = tables[1].find_all('tr')[2].find_all(
                'td')[1].get_text().split('\n')[1].strip()
            filing_date = tables[1].find_all('tr')[0].find_all(
                'td')[3].get_text().split('\n')[0].replace('Filing Date:', '').strip()
            """GOT CASE DESCRIPTION: case_type, case_id, case_title"""

            clean_names = []
            case_parties = tables[2].find_all('tr')
            for tr in case_parties:
                try:
                    name = tr.find_all('td')[5].find('b').get_text()
                    clean_names.append(name)
                except Exception:
                    pass
            """GOT PARTIES NAMES (clean_names)"""

            party_types = []
            s = tables[2].find_all('tr')
            for tr in s:
                try:
                    type_x = tr.find_all('td')[3].get_text().strip('\n')
                    if type_x != 'none':
                        party_types.append(type_x)
                except Exception:
                    pass
            """GOT PARTIES NAMES (party_types)"""

            addresses = []
            s = tables[2].find_all('tr')
            for tr in s:
                try:
                    address = tr.select('td[colspan="2"]')[
                        0].get_text().strip('\n')
                    if address:
                        addresses.append(address)
                except Exception:
                    pass

            item = {
                'title': case_title,
                'case_id': case_id,
                'type': case_type,
                'filing_date': filing_date,
                'parties': []
            }
            for name, involvement, address in zip(clean_names, party_types, addresses):
                person = {
                    'name': name,
                    'involvement': involvement,
                    'address': address if address != 'unavailable' else None,
                }
                item['parties'].append(person)

            record['case_info'] = []
            record['case_info'].append(item)
            logging.info(f'Parsed correctly records from {response.url}')
        except Exception:
            logging.error(
                f'Something happened with {response.url}. It could not be parsed, most likely absense of items. Status code {response.status_code}')
        return UpdateOne(query, {"$set": record}, upsert=True)
