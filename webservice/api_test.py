from webservice.api import scrape_url

url = 'https://www.amazon.es/dp/B006CZ0LGA'

response, status = scrape_url(url)


def test_scrape_url():
    assert scrape_url(url)