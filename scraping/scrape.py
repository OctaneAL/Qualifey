from scraping.utils import eures_to_db, eures_counts_to_db, djinni_count_to_db
from scraping.eures_scraping import scrap_eures, scrap_eures_counts
from scraping.djinni_scraping import scrape_djinni_count

def scrape_vacancies():
    eures = scrap_eures()
    eures_to_db(eures)
    eures_counts = scrap_eures_counts()
    eures_counts_to_db(eures_counts)

    djinni_count = scrape_djinni_count()
    djinni_count_to_db(djinni_count)
