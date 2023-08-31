import json, requests, time, threading, datetime, re, hashlib, os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from queue import Queue
from art import text2art
from progress.bar import FillingSquaresBar
from collections import Counter
from itertools import permutations
from visualization.utils import visualize_graph

ua = UserAgent()

job_detail_link = 'https://www.dice.com/job-detail/%s'

memo = {} # id: [skills]

input_path = os.path.join(os.getcwd(), 'scraping', 'data')
output_path = os.path.join(os.getcwd(), 'static', 'graphs_data')

def convert_json_graph(keyword):
    def add_weight(source, target, weight):
        if not source in edge_weights:
            edge_weights[source] = {}
        if not target in edge_weights[source]:
            edge_weights[source][target] = 0
        edge_weights[source][target] += weight

    def add_size(node, weight):
        if not node in node_sizes:
            node_sizes[node] = 0
        node_sizes[node] += weight

    path = os.path.join(os.getcwd(), 'static', 'graphs_data', f'{hash_code(keyword)}.json')

    # if exists...
    data = read_json(path)
    items = data['items']
    # subskills_name = 'subskills.json'
    # subskills = read_json(subskills_name)
    # subskills = {}

    node_sizes = {}
    edge_weights = {}

    # memoization???
    for id in items.keys():
        weight = items[id]['count']

        # items[id]['links'] = clear_items(items[id]['links'])

        for i, source in enumerate(items[id]['links']):
            add_size(source, weight)
            # if source in subskills:
            #     source = subskills[source]

            for target in items[id]['links'][i+1:]:
                # if target in subskills:
                #     target = subskills[target]
                add_size(target, weight)
                add_weight(source, target, weight)
                add_weight(target, source, weight)

    # for source in edge_weights:
    #     for target in edge_weights[source]:
    #         edge_weights[source][target] /= 2

    graph = {
        'phrase': data['phrases'],
        'parse_date': data['parse_date'], 
        'node_sizes': node_sizes,
        'edge_weights': edge_weights,
    }

    write_json(graph, path)

def convert_json_graphs(keywords):
    for keyword in keywords:
        convert_json_graph(keyword)

def write_json(_json, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(_json, f, indent = 4)

def read_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def get_job_ids(search: str, page_size: int, radius: int, page: int):
    headers = {
        'authority': 'job-search-api.svc.dhigroupinc.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,ru;q=0.7',
        'origin': 'https://www.dice.com',
        'referer': 'https://www.dice.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-api-key': '1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8',
    }

    params = {
        'q': search,
        'countryCode2': 'US',
        'radius': str(radius),
        'radiusUnit': 'mi',
        'page': str(page),
        'pageSize': str(page_size),
        'facets': 'employmentType|postedDate|workFromHomeAvailability|employerType|easyApply|isRemote',
        'fields': 'id|jobId|summary|title|jobLocation.displayName|detailsPageUrl|salary|clientBrandId|companyPageUrl|companyLogoUrl|positionId|companyName|employmentType|isHighlighted|score|easyApply|employerType',
        'culture': 'en',
        'recommendations': 'true',
        'interactionId': '0',
        'fj': 'true',
        'includeRemote': 'true',
        'eid': 'a6zd7NUgR0Wy8Tzf36TS2Q_|Tb30SliOSoWcjf4RBdhGSg_1',
    }

    try:
        response = requests.get('https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search', params=params, headers=headers).json()
    except:
        raise ValueError('Page number out of range')

    ids = []
    for vacancy in response['data']:
        ids.append(vacancy['id'])

    return ids

def is_word_in(word, s):
    if re.search(r"\b" + re.escape(word) + r"\b", s):
        return True
    return False

def get_skills_from_description(task, skills):
    global graph_bar, skills_list, cur_id

    def find_skills(_skills):
        _skills_list = skills_list.copy()
        for id in _skills_list:
            if _skills_list[id]['links'] == _skills:
                return id
        return -1

    id = task.get()

    if id in memo:
        _skills = memo[id]
        if _skills:
            id = find_skills(_skills)
            if id == -1:
                cur_id += 1
                skills_list[cur_id] = {
                    'links': _skills[:],
                    'count': 1
                }
            else:
                skills_list[id]['count'] += 1
        graph_bar.next()
        return

    headers = {
        'User-Agent': ua.random,
    }

    link = job_detail_link % id
    description = ''
    _skills = []

    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser") 
    try:
        for el in soup.find('div', {'data-testid': 'jobDescriptionHtml'}).findChildren():
            description += el.text.lower() + ' '
    except:
        # print(link) # write into logs
        pass

    # description = ' ' + description + ' '

    for skill_name in skills:
        for skill in skills[skill_name]:
            if is_word_in(skill, description):
                _skills.append(skill_name)
                break
    
    _skills.sort()
    memo[id] = _skills[:]

    if _skills:
        
        id = find_skills(_skills)
        if id == -1:
            cur_id += 1
            skills_list[cur_id] = {
                'links': _skills[:],
                'count': 1
            }
        else:
            skills_list[id]['count'] += 1

        # skills_list.append(_skills[:])
    graph_bar.next()

def get_skills(task):
    global skills, skills_bar

    id = task.get()

    headers = {
        'User-Agent': ua.random,
    }

    link = job_detail_link % id
    _skills = []
    
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser") 
    try:
        for el in soup.find('ul', {'data-cy': 'skillsList'}).findChildren():
            _skills.append(el.text.strip().lower())
    except Exception as e:
        # print(link) # write into logs
        pass

    for skill in _skills:
        skills.add(skill)

    skills_bar.next()

def write_to_file(_json, name):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(_json, f, indent = 4)

def get_all_description_skills(task):
    global temp_bar, skills_dict

    id = task.get()

    headers = {
        'User-Agent': ua.random,
    }

    link = job_detail_link % id
    words = []

    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser") 
    try:
        for el in soup.find('ul', {'data-cy': 'skillsList'}).findChildren():
            words.append(el.text.lower())
    except:
        # print(link) # write into logs
        pass

    for word in words:
        if not word in skills_dict:
            skills_dict[word] = 1
        else:
            skills_dict[word] += 1

    temp_bar.next()

def scrape_all_description_skills(ids):
    global skills_dict, temp_bar

    ids_set = set()
    for keyword in ids:
        for id in ids[keyword]:
            ids_set.add(id)
    ids = list(ids_set)

    print()
    print('Count of raw vacancies:', len(ids))
    print()

    art = text2art('ALL SKILLS')
    print(art)

    start = time.time()

    task = Queue(maxsize=10**9)
    skills_dict = {}

    for id in ids:
        task.put(id)
    
    temp_bar = FillingSquaresBar('Vacancies scraped', max = len(ids))
    
    for _ in range(len(ids)):
        threading.Thread(target=get_all_description_skills, args=(task,)).start()

    while True:
        if threading.active_count() == 1:
            break
    
    skills_dict = dict(sorted(skills_dict.items(), key = lambda x: x[1], reverse = True))

    write_to_file(skills_dict, name = os.path.join(input_path, 'all_skills.json'))

    print(f'\nScraping All Skills done in {time.time() - start} seconds\n')

def scrape_skills(ids):
    global skills, skills_bar

    art = text2art('SKILLS')
    print(art)

    start = time.time()

    task = Queue(maxsize=10**9)
    skills = set()

    for id in ids:
        task.put(id)
    
    skills_bar = FillingSquaresBar('Vacancies scraped', max = len(ids))

    for _ in range(len(ids)):
        threading.Thread(target=get_skills, args=(task,)).start()

    while True:
        if threading.active_count() == 1:
            break

    skills = list(skills)
    write_to_file(skills, name = os.path.join(input_path, 'keywords.json'))

    print(f'\nScraping Skills done in {time.time() - start} seconds\n')

def hash_code(s: str) -> str:
    return str(hashlib.sha512(s.encode('utf-8')).hexdigest())

def scrape_graph(ids, search_keyword, skills):
    global graph_bar, skills_list, cur_id

    art = text2art(f'GRAPH  {search_keyword}')
    print(art)
    print(f'Count of vacancies - {len(ids)}')

    start = time.time()

    skills_list = {}

    task = Queue(maxsize=10**9)

    for id in ids:
        task.put(id)
    
    cur_id = 0
    graph_bar = FillingSquaresBar('Vacancies scraped', max = len(ids))

    for _ in range(len(ids)):
        threading.Thread(target=get_skills_from_description, args=(task, skills)).start()

    while True:
        if threading.active_count() == 1:
            break

    print(f'\nScraping graph done in {time.time() - start} seconds\n')

    res = {
        'parse_date': str(datetime.datetime.now()),
        'phrases': search_keyword,
        'items_number': sum([skills_list[id]['count'] for id in skills_list]),
        'items': skills_list,
    }
    
    write_to_file(res, name = os.path.join(output_path, f'{hash_code(search_keyword)}.json'))

def scrape_graphs(ids):
    skills = get_all_keywords()

    
    for keyword in ids:
        scrape_graph(ids[keyword], keyword, skills)

    art = text2art(f'ALL GRAPHS DONE')
    print(art)

def get_all_keywords_keys(path: str = os.path.join(os.getcwd(), 'scraping', 'data', 'keywords.json')) -> list[str]:
    data = read_json(path)

    return list(data.keys())

def get_all_keywords(path: str = os.path.join(os.getcwd(), 'scraping', 'data', 'keywords.json')) -> list[str]:
    data = read_json(path)

    return data

def visualize_graphs(keywords):
    art = text2art(f'VISUALIZATION')
    print(art)

    visualization_bar = FillingSquaresBar('Vacancies scraped', max = len(keywords))

    start = time.time()

    for keyword in keywords:
        try:
            visualize_graph(keyword)
        except:
            print('BAD:', keyword)
        visualization_bar.next()
    
    print(f'\nVisualization done in {time.time() - start} seconds\n')

def main(scrapeGraph: bool = False, scrapeAllDescriptionSkills: bool = False) -> None:
    if not scrapeGraph and not scrapeAllDescriptionSkills:
        return

    search_keywords = get_all_keywords_keys()

    ids = {}
    for keyword in search_keywords:
        art = text2art(keyword)
        print(art)

        keyword_ids = []
        page = 1
        while True:
            try:
                keyword_ids += get_job_ids(keyword, 1000, 100, page)
                print(page, end = ' ')
                page += 1
            except:
                print()
                break
        ids[keyword] = keyword_ids[:]

    t = 0
    for i in ids:
        t += len(i)
    print()
    print('Count of raw vacancies:', t)
    print()

    if scrapeGraph:
        scrape_graphs(ids)
        convert_json_graphs(ids)
        visualize_graphs(ids.keys())
    if scrapeAllDescriptionSkills:
        scrape_all_description_skills(ids)

# if __name__ == '__main__':
#     scrapeGraph = True
#     scrapeAllDescriptionSkills = False

#     main(scrapeGraph = scrapeGraph, scrapeAllDescriptionSkills = scrapeAllDescriptionSkills)