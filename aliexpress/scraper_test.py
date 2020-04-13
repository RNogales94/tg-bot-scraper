from aliexpress.scraper import AliexpressScraper

def test_scrape_amazon_product_url():
    url = 'https://www.amazon.es/gp/product/B06XFHQGB9?pf_rd_p=44ae21af-cb43-440e-bcab-82e6a5324e39&pf_rd_r=8QV60VAX6GCJHW92RKH9'
    scraper = AliexpressScraper()
    result = scraper.scrape(url)
    assert isinstance(result, dict)
    assert 'short_description' in result.keys()
    assert 'description' in result.keys()
    assert 'features' in result.keys()
    assert 'standard_price' in result.keys()
    assert 'end_date' in result.keys()
    assert 'price' in result.keys()
    assert 'url' in result.keys()
    assert 'image_url' in result.keys()
    assert 'size' in result.keys()
    assert 'is_captcha' in result.keys()