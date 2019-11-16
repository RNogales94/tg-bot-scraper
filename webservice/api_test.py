from webservice.api import scrape_url
import json


def test_scrape_url_format():
    catan_url = 'https://www.amazon.es/dp/B006CZ0LGA'
    response, status = scrape_url(catan_url)
    response = json.loads(response)

    assert status == 200
    assert isinstance(response, dict)
    assert 'is_captcha' in response.keys()
    assert "short_description" in response.keys()
    assert "description" in response.keys()
    assert "features" in response.keys()
    assert "standard_price" in response.keys()
    assert "end_date" in response.keys()
    assert "price" in response.keys()
    assert "url" in response.keys()
    assert "image_url" in response.keys()
    assert "size" in response.keys()
    assert response['url'] == catan_url
    if response['is_captcha']:
        print(f'Is captcha {response["url"]}')
    else:
        print(f'Is not captcha {response["url"]}')
        assert "catan" in str.lower(response['short_description'])
        assert "catan" in str.lower(response['description'])


def test_scrape_bad_url():
    url = 'https://www.google.com'
    response, status = scrape_url(url)
    assert status == 412
    assert isinstance(json.loads(response), dict)
    assert "Error" in json.loads(response).keys()
