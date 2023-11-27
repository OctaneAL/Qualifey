import json, requests, time, threading, datetime, re, hashlib, os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from queue import Queue
from art import text2art
from progress.bar import FillingSquaresBar
from collections import Counter
from itertools import permutations
from visualization.utils import visualize_graph
from scraping.eures_scraping import scrap_eures

from scraping.models import (
    Skill, Skill_phrase,
    Graph, Vacancy, Company,
    State, Country,
)

ua = UserAgent()

job_detail_link = 'https://www.dice.com/job-detail/%s'

input_path = os.path.join(os.getcwd(), 'scraping', 'data')
output_path = os.path.join(os.getcwd(), 'static', 'graphs_data')
memo = {} # id: {skills: list, company: str}

memo_graph = {}

memo_vacancy = {}

memo_skill = {}

memo_vacancy_skill = {}

memo_company = {}

memo_city = {} # city : id

memo_state = {} # abbreviation: id

memo_country = {} # abbreviation : id

skill_to_id = {}

global EditExistingFlag
EditExistingFlag = False

def load_memo_company():
    companies = Company.objects.all()
    for company in companies:
        memo_company[company.name] = company.id

def load_memo_graph():
    graphs = Graph.objects.all()
    for graph in graphs:
        memo_graph[graph.skill_id] = graph

def load_memo_vacancy():
    vacancies = Vacancy.objects.all()
    for vacancy in vacancies:
        memo_vacancy[vacancy.job_id] = vacancy

def load_memo_skill():
    skills = Skill.objects.all()
    for skill in skills:
        memo_skill[skill.id] = skill

def load_skill_to_id():
    skills = Skill.objects.all()
    for skill in skills:
        skill_to_id[skill.skill] = skill.id

def load_memo_vacancy_skill():
    vacancy_skills = Vacancy_skill.objects.all()
    for vacancy_skill in vacancy_skills:
        if vacancy_skill.vacancy_id in memo_vacancy_skill:
            memo_vacancy_skill[vacancy_skill.vacancy_id].append(vacancy_skill.skill_id)
        else:
            memo_vacancy_skill[vacancy_skill.vacancy_id] = [vacancy_skill.skill_id]

def load_memo_city():
    cities = City.objects.all()
    for city in cities:
        memo_city[city.name.lower()] = city.id

def load_memo_state():
    states = State.objects.all()
    for state in states:
        memo_state[state.abbreviation] = state.id

def load_memo_country():
    countries = Country.objects.all()
    for country in countries:
        memo_country[country.abbreviation] = country.id

# good
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

    # graph_id = Graph.objects.get(skill_id = Skill.objects.get(skill = keyword).id).id # skill_to_id
    skill_id = skill_to_id[keyword]
    obj = memo_graph[skill_id]
    graph_id = obj.id
    data = obj.data

    items = data['items']
    # subskills_name = 'subskills.json'
    # subskills = read_json(subskills_name)
    # subskills = {}

    node_sizes = {}
    edge_weights = {}

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

    obj.data = graph
    obj.save()

    # Graph.objects.filter(id = graph_id).update(data = graph)

# good
def convert_json_graphs(keywords):
    for keyword in keywords:
        convert_json_graph(keyword)

# useless
def write_json(_json, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(_json, f, indent = 4)

# useless
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

# good
def is_word_in(word, s):
    if re.search(r"\b" + re.escape(word) + r"\b", s):
        return True
    return False

def parse_city(s: str) -> str or None:
    s = s.lower()

    s = s.replace('remote or ', '')
    if s.split(',')[0].strip() in memo_city:
        return memo_city[s.split(',')[0].strip()]

def parse_state(s: str) -> str or None:
    s = [i.strip() for i in s.split(',')]
    
    for word in s:
        if word in memo_state:
            return memo_state[word]
    
    return None

def parse_country(s: str) -> str or None:
    s = [i.strip() for i in s.split(',')]
    
    for word in s:
        if word in memo_country:
            return memo_country[word]
    
    return None

def is_remote(s: str) -> bool:
    return 'remote' in s.lower()

# good ??? to review
def get_skills_from_description(task, skills):
    global graph_bar, skills_list, cur_id, EditExistingFlag

    # print('EditExistingFlag =', EditExistingFlag)

    def find_skills(_skills):
        _skills_list = skills_list.copy()
        for id in _skills_list:
            if _skills_list[id]['links'] == _skills:
                return id
        return -1

    id = task.get()

    # if Vacancy.objects.filter(job_id = id).exists():
    if id in memo_vacancy and memo_vacancy[id].id in memo_vacancy_skill:
        # vacancy_id = Vacancy.objects.get(job_id = id).id
        vacancy_id = memo_vacancy[id].id
        
        # _skills = [Skill.objects.get(id = i.skill_id).skill for i in Vacancy_skill.objects.filter(vacancy_id = vacancy_id)] # memo_skill
        _skills = [memo_skill[skill_id].skill for skill_id in memo_vacancy_skill[vacancy_id]]
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

    company_name = None
    try:
        el = soup.find('a', {'data-cy': 'companyNameLink'})
        company_name = el.text
    except:
        pass

    if not company_name in memo_company and company_name != None:
        obj = Company(name = company_name)
        obj.save()
        memo_company[obj.name] = obj.id

    # description = ' ' + description + ' '

    for skill_name in skills:
        for skill in skills[skill_name]:
            if is_word_in(skill, description):
                _skills.append(skill_name)
                break
    
    # id - job_id 
    # _skills - skill_ids
    _skills.sort()

    salary = soup.find('div', {'data-cy': 'payDetails'})
    nums = []
    
    if salary != None:
        salary = salary.findChild().text
        salary = clear_salary_string(salary)

        nums = salary.split('-')

    has_salary = yearly = True
    salary_min = salary_max = None



    # ---------
    # WARNING
    # GOVNO-KOD
    # ---------
    
    # ---------
    # WARNING
    # GOVNO-KOD
    # ---------
    
    # ---------
    # WARNING
    # GOVNO-KOD
    # ---------
    
    # ---------
    # WARNING
    # GOVNO-KOD
    # ---------

    # print(id, '| nums =', nums)
    if len(nums) < 1 or len(nums) > 2:
        has_salary = False
    elif len(nums) == 1: 
        try:
            nums[0] = int(nums[0])

            if 5 < nums[0] < 400_000:
                salary_min = salary_max = nums[0]

                if salary_min < 500:
                    yearly = False
            else:
                has_salary = False
        except:
            has_salary = False
            
    elif len(nums) == 2:
        try:
            nums[0] = int(nums[0])
            nums[1] = int(nums[1])

            if nums[1] > nums[0] and nums[0] > 5:
                salary_min = salary_max = nums[0]

                if salary_min < 500:
                    yearly = False
            else:
                has_salary = False
        except:
            has_salary = False

    # ---------
    # WARNING
    # GOVNO-KOD
    # ---------
    
    # ---------
    # WARNING
    # GOVNO-KOD
    # ---------
    
    # ---------
    # WARNING
    # GOVNO-KOD
    # ---------
    
    # ---------
    # WARNING
    # GOVNO-KOD
    # ---------



    if not id in memo_vacancy:
        obj = Vacancy(job_id = id, has_salary = has_salary, salary_min = salary_min, salary_max = salary_max, yearly_salary = yearly)
        obj.save()
        memo_vacancy[id] = obj
    elif EditExistingFlag: # elif EditExisting !!!!!!!!!!!!!!!!!!!!!!!!!!
        obj = memo_vacancy[id]
        obj.has_salary = has_salary
        obj.salary_min = salary_min
        obj.salary_max = salary_max
        obj.yearly_salary = yearly
        obj.save()

    vacancy_id = memo_vacancy[id].id

    if not vacancy_id in memo_vacancy_skill:
        for skill_id in [skill_to_id[i] for i in _skills]:
            obj = Vacancy_skill(vacancy_id = vacancy_id, skill_id = skill_id)
            obj.save()

            if not vacancy_id in memo_vacancy_skill:
                memo_vacancy_skill[vacancy_id] = [skill_id]
            else:
                memo_vacancy_skill[vacancy_id].append(skill_id)
    elif False: # elif EditExisting ??????
        pass

            
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

# good
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

# useless
def write_to_file(_json, name):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(_json, f, indent = 4)

# good
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

# bad, but we wont use it
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

# bad, but we wont use it
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

def clear_salary_string(salary: str) -> str:
    res = ''

    salary = salary.replace('.00 ', '')
    if salary.endswith('.00'):
        salary = salary[:-3]

    for i in salary:
        if '0' <= i <= '9' or i == '-':
            res += i
    
    return res

# useless
def hash_code(s: str) -> str:
    return str(hashlib.sha512(s.encode('utf-8')).hexdigest())

# good 70/30, i need to convert JSON
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

    while ids:
        for _ in range(min(len(ids), 50)):
            threading.Thread(target=get_skills_from_description, args=(task, skills)).start()
            ids.pop(0)

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
    
    # !!!
    # CONVERT GRAPH
    # !!!

    # write to db | If exists - replace
    skill_id = skill_to_id[search_keyword] # skill_to_id {}

    # if Graph.objects.filter(skill_id = skill_id).exists():
    if skill_id in memo_graph:
        memo_graph[skill_id].data = res
        memo_graph[skill_id].save()
        # Graph.objects.filter(skill_id = skill_id).update(data = res)
    else:
        obj = Graph(skill_id = skill_id, data = res)
        obj.save()
        memo_graph[skill_id] = obj
    # write_to_file(res, name = os.path.join(output_path, f'{hash_code(search_keyword)}.json'))

# good
def scrape_graphs(ids) -> None:
    skills = get_all_keywords()

    
    for keyword in ids:
        scrape_graph(ids[keyword], keyword, skills)

    art = text2art(f'ALL GRAPHS DONE')
    print(art)

# good
def get_all_keywords_keys() -> list[str]:
    return [memo_skill[i].skill for i in memo_skill]
    return [obj.skill for obj in Skill.objects.all()]

# good
def get_all_keywords() -> list[str]:
    return {
        i: [j.phrase for j in Skill_phrase.objects.filter(skill = Skill.objects.get(skill = i).id)] for i in get_all_keywords_keys() # skill_to_id {}
    }

# good
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

# to review
def main(scrapeGraph: bool = False, scrapeAllDescriptionSkills: bool = False, EditExisting: bool = False) -> None:
    global EditExistingFlag
    
    if not scrapeGraph and not scrapeAllDescriptionSkills:
        return
    
    load_memo_company()
    load_memo_graph()
    load_memo_skill()
    load_memo_vacancy()
    load_memo_vacancy_skill()
    load_memo_city()
    load_memo_state()
    load_memo_country()
    load_skill_to_id()

    EditExistingFlag = EditExisting

    # print(skill_to_id.keys())
    # print(memo_vacancy_skill.keys())
    # print(memo_vacancy_skill[1223])

    search_keywords = get_all_keywords_keys() # [-7:-6]
    
    print(search_keywords)

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
        ids[keyword] = keyword_ids

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

def scrape_vacancies():
    eures = scrap_eures()
    eures_to_db(eures)

def eures_to_db(vacancies):
    for country_code in vacancies:
        country_id = Country.objects.get(abbreviation = country_code).id
        for vacancy in vacancies[country_code]:
            if Vacancy.objects.filter(job_id = vacancy['id'], country_id = country_id, timestamp = vacancy['timestamp']).exists():
                continue
            obj = Vacancy(job_id = vacancy['id'], country_id = country_id, timestamp = vacancy['timestamp']) # maybe more
            obj.save()
            
# if __name__ == '__main__':
#     scrapeGraph = True
#     scrapeAllDescriptionSkills = False

#     main(scrapeGraph = scrapeGraph, scrapeAllDescriptionSkills = scrapeAllDescriptionSkills)