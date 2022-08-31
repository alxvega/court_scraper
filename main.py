import logging
from utils.mongo import insert_bulk
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from scraping.fetcher import CourtFetcher
from scraping.parser import CourtCatalogueParser

logger = logging.basicConfig(filename='test.log', level=logging.INFO)

MAX_WORKERS = 3  # it can be set to a max of 4 to do it safely


class CourtScraper:
    scraped_data = []

    def start_scraper(self, page):
        print(f'Currently scraping page {page}')
        court_fetcher = CourtFetcher()
        court_parser = CourtCatalogueParser()
        response = court_fetcher.query_catalogue(
            first_name='', last_name='Smith', begin_date='02-AUG-2010', end_date='02-AUG-2022', PageNo=page)
        json_data = []
        catalogue = court_parser.parse(response, page)
        for record in catalogue:
            cases = court_fetcher.query_results(
                record['url'], query_type='records')
            results = court_parser.parse_results(cases)
            if results:
                results_dict = [court_fetcher.decode_url(
                    case) for case in results]
                cases_responses = (court_fetcher.query_results(
                    record['url'], 'cases', data=case) for case in results_dict)
                for record_url in cases_responses:
                    case_info = court_parser.parse_records(record_url, record)
                    json_data.append(case_info)
        
        if len(json_data) > 0:
            self.scraped_data.extend(json_data)
            logging.info(f'Results from page {page} have been scraped.')

    def db_insert(self):
        insert_bulk(self.scraped_data, 'delaware_records')
        # logging.info(f'Inserted {len(self.scraped_data)} records to DB.')

    # Changeable. I set it to 15 because I know that the default document has at least 15 pages.
    def concurrent_scraping(self, pages=15):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            scraping = [executor.submit(self.start_scraper, i)
                        for i in range(1, pages+1)]
            wait(scraping, return_when=ALL_COMPLETED)

        self.db_insert()


if __name__ == '__main__':
    court_scraper = CourtScraper()
    court_scraper.concurrent_scraping(pages=15)
    print('Finished scraping.')
