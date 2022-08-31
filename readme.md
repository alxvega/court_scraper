# Delaware Court 
## Web Scraping Challenge

## Getting started:

This is a web scrapping tool that can help us retrieve records from https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_main.cp_main_idx

## Libraries used:

- BeautifulSoup
- Requests
- Pymongo
- Fake_useragent
- Python Virtual Env
- Scraperapi_sdk

## Running commands:

- Create env: python3 -m venv env
- Activate env source/env/bin/activate
- Install libraries: pip install -r requirements.txt
- Build Docker environment: docker-compose -f docker-compose.yml up
- Execute scraping: python3 main.py

## Architecture:
The project is divided in three core files.
#### 1. fetcher.py takes care of sending requests to the website and return responses that will be processed later
#### 2. parser.py processes the information inside the response and returns catalogue results / records information
#### 3. main.py functions as a sort of task manager where we iterate over search results, pages and such.
#### 4. client.py that specifies headers information and sets the scrape_api proxy for future requests

The order is the following:
1. Info is sended as parameter inside the body of the GET request to the website specifying info such as:
    - First name
    - Last name
    - Phonetic search
    - Case beginning date
    - Case finishing date
    - Page of records retrieved
    - etc.

2. We get the response with the results, where different people's records appear and iterate over them visiting each case and retrieving every case record.

Put simply: this scraper follows the browsing routine of a normal person. There could be some discussion as to whether making all requests first and then parse all the data could be useful but I find to be riskier and more suspicious for the server to receive concurrent requests rapidly. I opted to add some concurrency with 2-4 workers that walk all the path described.

### More resources:
1. test.log -> all logging information is processed here.
2. json file is a sample of 10 pages with about 200 documents.

### Notes:
I chose bs4 and requests as libraries since I needed a lot of freedom to parse the html and process the information. Scrapy xpath functions were not consistent with data results (website html was not very friendly to being scraped). I implemented proxy rotation with the scraper_api sdk and the whole process is records itself logs file.

This scraper can work for example with a txt file that has a list of people whose info will be needed as parameters for the query builder in main.py.

### Json output sample:

```json
{
    "_id" : ObjectId("63052bd98e6576ebd363b307"),
    "platform" : "delaware_court",
    "url" : "https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_judg.cp_judgment_rel_rslt_idx?in_seq_no=668491&in_pidm=4132363&in_name=SMITH (LECATES), KAREN",
    "address" : "3923 Layfield Road Salisbury Md 21804-1596",
    "amount" : 3996.05,
    "case_info" : [
        {
            "title" : "JP16-18-004316\n - DHSS VS. KAREN SMITH (LECATES) ET AL-NON JURY TRIAL",
            "case_id" : " JP16-18-004316",
            "type" : "60 - JP DEBT ACTION",
            "filing_date" : "Thursday , June      28th, 2018",
            "parties" : [
                {
                    "name" : "PAYNE, KATRINA ",
                    "involvement" : "AGENT",
                    "address" : "DHSS DMS/ARMS\nBIGGS BLDG #4\n1901 N. DUPONT HWY\nNEW CASTLE DE 19720\n(302)255-9465"
                },
                {
                    "name" : "WHITE, SHERRY ",
                    "involvement" : "AGENT",
                    "address" : "DHSS DMS/ARMS\nBIGGS BLDG #4\n1901 N. DUPONT HWY\nNEW CASTLE DE 19720\n(302)255-9465"
                },
                {
                    "name" : "MURRAY, LEITH ",
                    "involvement" : "AGENT",
                    "address" : "DHSS DMS/ARMS\n1901 N. DUPONT HWY\nBIGGS BLDG #4\nNEW CASTLE DE 19720"
                },
                {
                    "name" : "MCINTOSH, RACQUEL ",
                    "involvement" : "AGENT",
                    "address" : "DHSS DMS/ARMS\n1901 N. DUPONT HWY\nBIGGS BLDG #4\nNEW CASTLE DE 19720"
                },
                {
                    "name" : "CUNNINGHAM, ALESSANDRA ",
                    "involvement" : "AGENT",
                    "address" : "DHSS DMS/ARMS\nBIGGS BLDG ENTRANCE #4\n1901 N. DUPONT HWY\nNEW CASTLE DE 19720"
                },
                {
                    "name" : "DELAWARE HEALTH AND SOCIAL SERVICES ",
                    "involvement" : "CUNNINGHAM, SANDY",
                    "address" : "DHSS DMS/ARMS\nBIGGS BLDG ENTRANCE #4\n1901 N. DUPONT HWY\nNEW CASTLE DE 19720"
                },
                {
                    "name" : "SMITH (LECATES), KAREN ",
                    "involvement" : "PLAINTIFF",
                    "address" : "DHSS/ARMS\nBIGGS BLDG 4\n1901 N DUPONT HWY\nNEW CASTLE DE 19720"
                },
                {
                    "name" : "LECATES, KELSEY M.",
                    "involvement" : "DEPARTMENT OF HEALTH AND SOCIAL SERVICES\n\nDE HEALTH & SOCIAL SERVICES\n\nDE HEALTH & SOC. SERVICES\n\nDELAWARE HEALTH &SOCIAL SVCS\n\nDE HEALTH & SOCIAL SRV.\n\nDEL HEALTH & SOCIAL SERVICES\n\nDE HEALTH & SOCIAL SERVICES",
                    "address" : "DHSS/ARMS\nBIGGS BLDG 4\n1901 N DUPONT HWY\nNEW CASTLE DE 19720"
                },
                {
                    "name" : "GENESIS HEALTH CARE LLC ",
                    "involvement" : "DEFENDANT",
                    "address" : "DHSS DMS/ARMS\nBIGGS BLDG ENTANCE #4\n1901 N. DUPONT HIGHWAY\nNEW CASTLE DE 19720"
                },
                {
                    "name" : "GENISIS HEALTHCARE ",
                    "involvement" : "DEFENDANT",
                    "address" : "DHSS DMS/ARMS\nBIGGS BLDG ENTANCE #4\n1901 N. DUPONT HIGHWAY\nNEW CASTLE DE 19720"
                }
            ]
        }
    ],
    "created_at" : "2022-08-23",
    "currency" : "USD",
    "joint_and_several" : false,
    "judgment_date" : "28-DEC-2018",
    "judgment_finished" : true,
    "name_or_company" : "Smith (lecates), Karen",
    "party_end_date" : null,
    "person_id" : "@3114027"
}
```

---

### All information collected is only for educational purposes only. All rights go to their respective owners.
