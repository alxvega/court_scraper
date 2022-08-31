import requests
import logging
from scraping.client import Client
from urllib.parse import urlparse, parse_qs

config = logging.basicConfig(filename='test.log', level=logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class CourtFetcher(Client):
    Client.headers['host'] = 'courtconnect.courts.delaware.gov'
    url = 'https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_judg.cp_judgment_srch_rslt'
    results_url = "https://courtconnect.courts.delaware.gov//cc//cconnect//ck_public_qry_judg.cp_judgment_dtl_rslt"
    case_url = "https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_doct.cp_dktrpt_docket_report"

    def query_catalogue(self,  first_name="", middle_name="", last_name="Smith", begin_date='02-AUG-2010', end_date='02-JAN-2020', soundex_ind='', partial_ind='checked',
                        sat_ind="All", PageNo='', backto='P'):
        data = {
            'backto': backto,
            'soundex_ind': soundex_ind,
            'partial_ind': partial_ind,
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
            'begin_date': begin_date,
            'end_date': end_date,
            'sat_ind': sat_ind,
            'PageNo': PageNo,
        }
        response = requests.get(
            self.url, headers=self.headers, params=(data), proxies=self.proxies)
        self.headers['Referer'] = response.url[:-1] + str(PageNo-1)
        return response

    def decode_url(self, url):
        if url:
            params = parse_qs(urlparse(url).query)
            data = {k: i for k, v in params.items() for i in v}
            return data
        logging.warning(f'{url} query could not be resolved.')

    def query_results(self, record_url, query_type, data=None):
        if query_type == 'records':
            wanted_url = self.results_url
        elif query_type == 'cases':
            wanted_url = self.case_url

        url = record_url
        headers = self.headers
        headers['Referer'] = wanted_url

        if wanted_url != '' and wanted_url != None:
            if data:
                response = requests.get(
                    wanted_url, headers=headers, params=data, proxies=self.proxies)
                return response
            else:
                data = self.decode_url(url)
                response = requests.get(
                    wanted_url, headers=headers, params=(data), proxies=self.proxies)
                return response
