from amazon.scraper import AmazonScraper

url = 'https://www.amazon.es/gp/product/B06XFHQGB9?pf_rd_p=44ae21af-cb43-440e-bcab-82e6a5324e39&pf_rd_r=8QV60VAX6GCJHW92RKH9'
url = 'https://www.amazon.es/Auriculares-Microfono-Cancelacion-Acolchada-Unidireccional/dp/B078MJ4VND?ref_=Oct_DLandingS_PC_a5587a61_0&tag=hey'
scraper = AmazonScraper()
result = scraper.scrape(url)
result.to_dict()


def test_scrape_amazon_product_url():
    url = 'https://www.amazon.es/gp/product/B06XFHQGB9?pf_rd_p=44ae21af-cb43-440e-bcab-82e6a5324e39&pf_rd_r=8QV60VAX6GCJHW92RKH9'
    scraper = AmazonScraper()
    result = scraper.scrape(url)
    result.to_dict()
    assert False