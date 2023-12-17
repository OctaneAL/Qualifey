import requests
from bs4 import BeautifulSoup as bs

def scrape_software_developer():
    cookies = {
        'csrftoken': '8gkDiOx0X0dRCiLiEmyVEKWr1vKRQM2oJNNM5Z4jAXIrDChZdQvDlDORsGQ8EewL',
        'intercom-id-cg6zpunb': '588438ce-9f99-4672-8edc-71f3230b662a',
        'intercom-session-cg6zpunb': '',
        'intercom-device-id-cg6zpunb': '4f561be8-6a35-4345-a111-b307b515ac2e',
        '_hjSessionUser_3704742': 'eyJpZCI6ImYyOGI3OGI2LWM0ZmMtNWM1MS1iNDE2LTFhZTliMTVlYTc4OSIsImNyZWF0ZWQiOjE3MDI0MDc5MzA5NzgsImV4aXN0aW5nIjp0cnVlfQ==',
        '_hjIncludedInSessionSample_3704742': '0',
        '_hjSession_3704742': 'eyJpZCI6IjIzNmZkNWFmLWIxZDUtNDZmOC1hODFhLTdkNTg0MjFlNGI2MCIsImMiOjE3MDI4MjUyMzUzMTYsInMiOjAsInIiOjAsInNiIjoxfQ==',
        '_hjAbsoluteSessionInProgress': '0',
        'sessionid': '.eJwVzN0KgzAMBeB36e027Z-j9hV2N7ZriTV2AzVSKzLEd1-EwMmBL9lFoHXK6dcE6lB48X48xVUstKZw1k_O8-LLctu2IhLFAYtAY8kEJpqE38W3Y9Y6Wyl7172rtdUIgEZXPdZBAULrDPuQEDKeWEttbkrzvFTtpfTWFHdlnHUXLlIy7geIC38_Dt4TjXzFMeUZIjYhA5NIuUnrgMxyWvH4A4cUPaI:1rEsec:PwIehLPlbVUv3i9cwa2NyUz7bloF3otoeG7KLuGdiXE',
    }

    headers = {
        'authority': 'djinni.co',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,ru;q=0.7,pl;q=0.6',
        # 'cookie': 'csrftoken=8gkDiOx0X0dRCiLiEmyVEKWr1vKRQM2oJNNM5Z4jAXIrDChZdQvDlDORsGQ8EewL; intercom-id-cg6zpunb=588438ce-9f99-4672-8edc-71f3230b662a; intercom-session-cg6zpunb=; intercom-device-id-cg6zpunb=4f561be8-6a35-4345-a111-b307b515ac2e; _hjSessionUser_3704742=eyJpZCI6ImYyOGI3OGI2LWM0ZmMtNWM1MS1iNDE2LTFhZTliMTVlYTc4OSIsImNyZWF0ZWQiOjE3MDI0MDc5MzA5NzgsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample_3704742=0; _hjSession_3704742=eyJpZCI6IjIzNmZkNWFmLWIxZDUtNDZmOC1hODFhLTdkNTg0MjFlNGI2MCIsImMiOjE3MDI4MjUyMzUzMTYsInMiOjAsInIiOjAsInNiIjoxfQ==; _hjAbsoluteSessionInProgress=0; sessionid=.eJwVzN0KgzAMBeB36e027Z-j9hV2N7ZriTV2AzVSKzLEd1-EwMmBL9lFoHXK6dcE6lB48X48xVUstKZw1k_O8-LLctu2IhLFAYtAY8kEJpqE38W3Y9Y6Wyl7172rtdUIgEZXPdZBAULrDPuQEDKeWEttbkrzvFTtpfTWFHdlnHUXLlIy7geIC38_Dt4TjXzFMeUZIjYhA5NIuUnrgMxyWvH4A4cUPaI:1rEsec:PwIehLPlbVUv3i9cwa2NyUz7bloF3otoeG7KLuGdiXE',
        'referer': 'https://djinni.co/jobs/?all-keywords=developer+-enginee&primary_keyword=JavaScript&primary_keyword=Fullstack&primary_keyword=React+Native&primary_keyword=Java&primary_keyword=.NET&primary_keyword=Python&primary_keyword=PHP&primary_keyword=Node.js&primary_keyword=iOS&primary_keyword=Android&primary_keyword=C%2B%2B&primary_keyword=Flutter&primary_keyword=Golang&primary_keyword=Ruby&primary_keyword=Scala&primary_keyword=Salesforce&primary_keyword=Rust&primary_keyword=ERP&region=UKR&keywords=developer+-enginee',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'all-keywords': 'developer -engineer',
        'primary_keyword': [
            'JavaScript',
            'Fullstack',
            'React Native',
            'Java',
            '.NET',
            'Python',
            'PHP',
            'Node.js',
            'iOS',
            'Android',
            'C++',
            'Flutter',
            'Golang',
            'Ruby',
            'Scala',
            'Salesforce',
            'Rust',
            'ERP',
        ],
        'region': 'UKR',
        'keywords': 'developer -engineer',
    }

    response = requests.get('https://djinni.co/jobs/', params=params, cookies=cookies, headers=headers)

    return get_amount(response)

def scrape_data_analyst():
    cookies = {
        'csrftoken': '8gkDiOx0X0dRCiLiEmyVEKWr1vKRQM2oJNNM5Z4jAXIrDChZdQvDlDORsGQ8EewL',
        'intercom-id-cg6zpunb': '588438ce-9f99-4672-8edc-71f3230b662a',
        'intercom-session-cg6zpunb': '',
        'intercom-device-id-cg6zpunb': '4f561be8-6a35-4345-a111-b307b515ac2e',
        '_hjSessionUser_3704742': 'eyJpZCI6ImYyOGI3OGI2LWM0ZmMtNWM1MS1iNDE2LTFhZTliMTVlYTc4OSIsImNyZWF0ZWQiOjE3MDI0MDc5MzA5NzgsImV4aXN0aW5nIjp0cnVlfQ==',
        '_hjIncludedInSessionSample_3704742': '0',
        '_hjSession_3704742': 'eyJpZCI6IjIzNmZkNWFmLWIxZDUtNDZmOC1hODFhLTdkNTg0MjFlNGI2MCIsImMiOjE3MDI4MjUyMzUzMTYsInMiOjAsInIiOjAsInNiIjoxfQ==',
        '_hjAbsoluteSessionInProgress': '0',
        'sessionid': '.eJwVzN0KgzAMBeB36e027Z-j9hV2N7ZriTV2AzVSKzLEd1-EwMmBL9lFoHXK6dcE6lB48X48xVUstKZw1k_O8-LLctu2IhLFAYtAY8kEJpqE38W3Y9Y6Wyl7172rtdUIgEZXPdZBAULrDPuQEDKeWEttbkrzvFTtpfTWFHdlnHUXLlIy7geIC38_Dt4TjXzFMeUZIjYhA5NIuUnrgMxyWvH4A4cUPaI:1rEsfj:9IB7WSG2FMrkMLJp78sexxkEygschrvmgL_svO5vWAc',
    }

    headers = {
        'authority': 'djinni.co',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,ru;q=0.7,pl;q=0.6',
        # 'cookie': 'csrftoken=8gkDiOx0X0dRCiLiEmyVEKWr1vKRQM2oJNNM5Z4jAXIrDChZdQvDlDORsGQ8EewL; intercom-id-cg6zpunb=588438ce-9f99-4672-8edc-71f3230b662a; intercom-session-cg6zpunb=; intercom-device-id-cg6zpunb=4f561be8-6a35-4345-a111-b307b515ac2e; _hjSessionUser_3704742=eyJpZCI6ImYyOGI3OGI2LWM0ZmMtNWM1MS1iNDE2LTFhZTliMTVlYTc4OSIsImNyZWF0ZWQiOjE3MDI0MDc5MzA5NzgsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample_3704742=0; _hjSession_3704742=eyJpZCI6IjIzNmZkNWFmLWIxZDUtNDZmOC1hODFhLTdkNTg0MjFlNGI2MCIsImMiOjE3MDI4MjUyMzUzMTYsInMiOjAsInIiOjAsInNiIjoxfQ==; _hjAbsoluteSessionInProgress=0; sessionid=.eJwVzN0KgzAMBeB36e027Z-j9hV2N7ZriTV2AzVSKzLEd1-EwMmBL9lFoHXK6dcE6lB48X48xVUstKZw1k_O8-LLctu2IhLFAYtAY8kEJpqE38W3Y9Y6Wyl7172rtdUIgEZXPdZBAULrDPuQEDKeWEttbkrzvFTtpfTWFHdlnHUXLlIy7geIC38_Dt4TjXzFMeUZIjYhA5NIuUnrgMxyWvH4A4cUPaI:1rEsfj:9IB7WSG2FMrkMLJp78sexxkEygschrvmgL_svO5vWAc',
        'referer': 'https://djinni.co/jobs/?primary_keyword=Business+Analyst&primary_keyword=Data+Analyst&region=UKR',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'primary_keyword': [
            'Business Analyst',
            'Data Science',
            'Data Analyst',
        ],
        'region': 'UKR',
    }

    response = requests.get('https://djinni.co/jobs/', params=params, cookies=cookies, headers=headers)

    return get_amount(response)

def scrape_engineer():
    cookies = {
        'csrftoken': '8gkDiOx0X0dRCiLiEmyVEKWr1vKRQM2oJNNM5Z4jAXIrDChZdQvDlDORsGQ8EewL',
        'intercom-id-cg6zpunb': '588438ce-9f99-4672-8edc-71f3230b662a',
        'intercom-session-cg6zpunb': '',
        'intercom-device-id-cg6zpunb': '4f561be8-6a35-4345-a111-b307b515ac2e',
        '_hjSessionUser_3704742': 'eyJpZCI6ImYyOGI3OGI2LWM0ZmMtNWM1MS1iNDE2LTFhZTliMTVlYTc4OSIsImNyZWF0ZWQiOjE3MDI0MDc5MzA5NzgsImV4aXN0aW5nIjp0cnVlfQ==',
        '_hjIncludedInSessionSample_3704742': '0',
        '_hjSession_3704742': 'eyJpZCI6IjIzNmZkNWFmLWIxZDUtNDZmOC1hODFhLTdkNTg0MjFlNGI2MCIsImMiOjE3MDI4MjUyMzUzMTYsInMiOjAsInIiOjAsInNiIjoxfQ==',
        '_hjAbsoluteSessionInProgress': '0',
        'sessionid': '.eJwVzN0KgzAMBeB36e027Z-j9hV2N7ZriTV2AzVSKzLEd1-EwMmBL9lFoHXK6dcE6lB48X48xVUstKZw1k_O8-LLctu2IhLFAYtAY8kEJpqE38W3Y9Y6Wyl7172rtdUIgEZXPdZBAULrDPuQEDKeWEttbkrzvFTtpfTWFHdlnHUXLlIy7geIC38_Dt4TjXzFMeUZIjYhA5NIuUnrgMxyWvH4A4cUPaI:1rEsiO:kGyz1DocRgpc5eJ-EYoNMpiaxe-vGrdhFoRhfBFFjXI',
    }

    headers = {
        'authority': 'djinni.co',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,ru;q=0.7,pl;q=0.6',
        # 'cookie': 'csrftoken=8gkDiOx0X0dRCiLiEmyVEKWr1vKRQM2oJNNM5Z4jAXIrDChZdQvDlDORsGQ8EewL; intercom-id-cg6zpunb=588438ce-9f99-4672-8edc-71f3230b662a; intercom-session-cg6zpunb=; intercom-device-id-cg6zpunb=4f561be8-6a35-4345-a111-b307b515ac2e; _hjSessionUser_3704742=eyJpZCI6ImYyOGI3OGI2LWM0ZmMtNWM1MS1iNDE2LTFhZTliMTVlYTc4OSIsImNyZWF0ZWQiOjE3MDI0MDc5MzA5NzgsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample_3704742=0; _hjSession_3704742=eyJpZCI6IjIzNmZkNWFmLWIxZDUtNDZmOC1hODFhLTdkNTg0MjFlNGI2MCIsImMiOjE3MDI4MjUyMzUzMTYsInMiOjAsInIiOjAsInNiIjoxfQ==; _hjAbsoluteSessionInProgress=0; sessionid=.eJwVzN0KgzAMBeB36e027Z-j9hV2N7ZriTV2AzVSKzLEd1-EwMmBL9lFoHXK6dcE6lB48X48xVUstKZw1k_O8-LLctu2IhLFAYtAY8kEJpqE38W3Y9Y6Wyl7172rtdUIgEZXPdZBAULrDPuQEDKeWEttbkrzvFTtpfTWFHdlnHUXLlIy7geIC38_Dt4TjXzFMeUZIjYhA5NIuUnrgMxyWvH4A4cUPaI:1rEsiO:kGyz1DocRgpc5eJ-EYoNMpiaxe-vGrdhFoRhfBFFjXI',
        'referer': 'https://djinni.co/jobs/?all-keywords=engineer&region=UKR&keywords=engineer&page=53',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'all-keywords': 'engineer',
        'region': 'UKR',
        'keywords': 'engineer',
    }

    response = requests.get('https://djinni.co/jobs/', params=params, cookies=cookies, headers=headers)

    return get_amount(response)

def validate_response(response):
    return response.status_code == 200

def get_amount(response):
    if not validate_response(response):
        return None
    

    soup = bs(response.content, 'html.parser')

    return int(soup.find('header', class_ = 'page-header').find('h1').find('span').text)

def scrape_djinni_count():
    vacancies = {
        'Data Analyst': scrape_data_analyst(),
        'Software Developer': scrape_software_developer(),
        'Software Engineer/Architect': scrape_engineer(),
    }

    return vacancies