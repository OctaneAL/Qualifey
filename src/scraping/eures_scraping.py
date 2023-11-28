import requests, json, pytz
from datetime import datetime
from scraping.models import Country, JobTitle, OccupationUri

def scrap_eures_keyword(keyword):
    json_data['occupationUris'] = occupationUris[keyword]

    vacancies = {}
    for country_code in country_codes:
        print(country_code.upper())
        vacancies[country_code] = []

        json_data['locationCodes'] = [country_code]

        json_obj = response_text_to_json(get_response_text(send_search_request(cookies=cookies, headers=headers, json_data=json_data)))
        
        if json_obj == None:
            print('Error')
            continue

        cur = 0
        print('Count of vacancies -', json_obj['numberRecords'])

        for page in range(1, 200+1):
            json_data['page'] = page

            json_obj = response_text_to_json(get_response_text(send_search_request(cookies=cookies, headers=headers, json_data=json_data)))

            if json_obj == None:
                print('Error')
                break

            cur += len(json_obj['jvs'])

            print(cur, '/', json_obj['numberRecords'])

            arr = parse_vacancies(json_obj)

            if arr == []:
                break

            vacancies[country_code] += arr
    
    return vacancies

def response_text_to_json(text):
    if text:
        return json.loads(text)
    return None

def get_response_text(response):
    if response == None or response.status_code != 200:
        return None
    return response.text

def parse_vacancies(json_obj):
    arr = []

    # ???
    # if not 'jvs' in json_obj:
    #     return arr

    for obj in json_obj['jvs']:
        arr.append(
            {
                'id': obj['id'],
                'timestamp': datetime.fromtimestamp(obj['lastModificationDate'] // 1000, tz=timezone), # Creation Date
                'schedule': obj['positionScheduleCodes'], # Full-Time, ...
            }
        )

    return arr

def send_search_request(cookies, headers, json_data):
    try:
        response = requests.post(
            'https://europa.eu/eures/eures-apps/searchengine/page/jv-search/search',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )
    except ConnectionError:
        response = None

    return response

def scrap_eures_keyword_count(keyword):
    json_data['occupationUris'] = occupationUris[keyword]

    vacancies = {}
    for country_code in country_codes:
        print(country_code.upper())
        vacancies[country_code] = None

        json_data['locationCodes'] = [country_code]

        json_obj = response_text_to_json(get_response_text(send_search_request(cookies=cookies, headers=headers, json_data=json_data)))
        
        if json_obj == None:
            print('Error')
            continue

        vacancies[country_code] = json_obj['numberRecords']
    
    return vacancies

def scrap_eures():
    json_data['publicationPeriod'] = 'LAST_WEEK'
    vacancies = {}
    for keyword in keywords:
        vacancies[keyword] = scrap_eures_keyword(keyword)

    return vacancies

def scrap_eures_counts():
    json_data['publicationPeriod'] = None
    vacancies = {}
    for keyword in keywords:
        vacancies[keyword] = scrap_eures_keyword_count(keyword)
    
    return vacancies

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,ru;q=0.7,pl;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://europa.eu',
    'Referer': 'https://europa.eu/eures/portal/jv-se/search?page=1&resultsPerPage=10&orderBy=MOST_RECENT&locationCodes=be&keywordsEverywhere=data%20analyst&publicationPeriod=LAST_DAY&escoIsco=C25&lang=en',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'X-XSRF-TOKEN': '6d7256c5-c485-4a5a-a839-1f57c2fc86a5',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'keywords': [
        {
            'keyword': '',
            'specificSearchCode': 'EVERYWHERE',
        },
    ],
    'publicationPeriod': 'LAST_WEEK', # LAST_DAY / LAST_WEEK / None
    'occupationUris': [
        'http://data.europa.eu/esco/isco/C25',
    ],
    'skillUris': [],
    'requiredExperienceCodes': [],
    'positionScheduleCodes': [],
    'sectorCodes': [],
    'educationLevelCodes': [],
    'positionOfferingCodes': [],
    'locationCodes': [],
    'euresFlagCodes': [],
    'otherBenefitsCodes': [],
    'requiredLanguages': [],
    'resultsPerPage': 50,
    'sortSearch': 'MOST_RECENT',
    'page': 1,
    'minNumberPost': None,
    'sessionId': '', # not necessary
}

cookies = {
    'EURES_JVSE_SESSIONID': '82A6077C467A850381157C245CC1F130',
    'XSRF-TOKEN': '6d7256c5-c485-4a5a-a839-1f57c2fc86a5',
    'cck1': '%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Atrue%7D',
}

# occupationUris = {
#     'Software Developer': [
#         'http://data.europa.eu/esco/occupation/866c7813-2c03-47d7-9bdc-192cfbace57c',
#         'http://data.europa.eu/esco/occupation/9ebaf3f0-0be0-47b7-b2b1-b3b04130fa81',
#         'http://data.europa.eu/esco/occupation/bb6198c4-1d3e-40b9-9cc4-ad2dd9d7c74b',
#         'http://data.europa.eu/esco/occupation/bd272aee-adc9-4a06-a15c-a73b4b4a46a7',
#         'http://data.europa.eu/esco/occupation/f2b15a0e-e65a-438a-affb-29b9d50b77d1',
#     ],
#     'Data Analyst': [
#         'http://data.europa.eu/esco/occupation/04ba4d6c-957d-417f-bf63-5b9e015a9f86',
#         'http://data.europa.eu/esco/occupation/0ab5c12c-c1c1-4772-8345-aa287d0e391d',
#         'http://data.europa.eu/esco/occupation/102e75c8-3b47-4964-9b47-30a980aed25c',
#         'http://data.europa.eu/esco/occupation/258e46f9-0075-4a2e-adae-1ff0477e0f30',
#         'http://data.europa.eu/esco/occupation/a6a0b60f-08da-4faa-bf54-942987efb471',
#         'http://data.europa.eu/esco/occupation/d3edb8f8-3a06-47a0-8fb9-9b212c006aa2',
#         'http://data.europa.eu/esco/occupation/e3229e40-f571-4b26-baca-29edc8fe313e',
#         'http://data.europa.eu/esco/occupation/faed411a-f920-4100-86a8-b877928b429c',
#         'http://data.europa.eu/esco/occupation/fe0fa514-b48d-4a53-9757-a283c0baacf0',
#     ],
#     'Software Engineer/Architect': [
#         'http://data.europa.eu/esco/occupation/07e60525-1aad-4099-aaf3-2c7014c92212',
#         'http://data.europa.eu/esco/occupation/10469d70-78a3-4650-9e29-d04de13c62c1',
#         'http://data.europa.eu/esco/occupation/1562c7a3-c7d9-419d-b9b6-db26610bcf84',
#         'http://data.europa.eu/esco/occupation/2bef94db-0088-4507-982a-2ca717529adb',
#         'http://data.europa.eu/esco/occupation/35553663-deab-4d9a-bf22-15c1625d28e8',
#         'http://data.europa.eu/esco/occupation/812c217d-32b7-4f6a-9faf-993d3577ac7f',
#         'http://data.europa.eu/esco/occupation/8d9ec84d-cf2d-4179-87bc-335cda54a427',
#         'http://data.europa.eu/esco/occupation/cf2b03cd-feb7-4f47-90f6-ff1ed6016d3d',
#         'http://data.europa.eu/esco/occupation/d0aa0792-4345-474b-9365-686cf4869d2e',
#         'http://data.europa.eu/esco/occupation/e0b544dd-b621-4126-a55e-054af25c6ea0',
#         'http://data.europa.eu/esco/occupation/e1c72b5f-4c5c-487c-a6df-e84b64a51dae',
#     ],
# }

# country_codes = ['be', 'de', 'se', 'nl', 'li', 'ro', 'pl', 'fr']
timezone = pytz.timezone("Europe/Sofia")
country_codes = [obj.abbreviation for obj in Country.objects.all()]
country_codes.remove('US')
# keywords = ['Data Analyst', 'Software Developer', 'Software Engineer/Architect']
keywords = [obj.name for obj in JobTitle.objects.all()]

occupationUris = {
    keyword.name: [occupationUri.link for occupationUri in OccupationUri.objects.filter(jobtitle_id = keyword.id)] for keyword in JobTitle.objects.all()
}

# eures_vacancies = scrap_eures()