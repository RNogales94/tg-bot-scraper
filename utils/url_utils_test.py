from utils.url_utils import capture_urls, expand_url, get_ASIN, is_aliexpress


def test_get_ASIN():
    url = "http://www.amazon.com/Kindle-Wireless-Reading-Display-Generation/dp/B0015T963C"
    assert get_ASIN(url) == 'B0015T963C'
    url = "http://www.amazon.com/dp/B0015T963C"
    assert get_ASIN(url) == 'B0015T963C'
    url = "http://www.amazon.com/gp/product/B0015T963C"
    assert get_ASIN(url) == 'B0015T963C'
    url = "http://www.amazon.com/gp/product/glance/B0015T963C"
    assert get_ASIN(url) == 'B0015T963C'
    url = "https://www.amazon.de/gp/product/B00LGAQ7NW/ref=s9u_simh_gw_i1?ie=UTF8&pd_rd_i=B00LGAQ7NW&pd_rd_r=5GP2JGPPBAXXP8935Q61&pd_rd_w=gzhaa&pd_rd_wg=HBg7f&pf_rd_m=A3JWKAKR8XB7XF&pf_rd_s=&pf_rd_r=GA7GB6X6K6WMJC6WQ9RB&pf_rd_t=36701&pf_rd_p=c210947d-c955-4398-98aa-d1dc27e614f1&pf_rd_i=desktop"
    assert get_ASIN(url) == 'B00LGAQ7NW'
    url = "https://www.amazon.de/Sawyer-Wasserfilter-Wasseraufbereitung-Outdoor-Filter/dp/B00FA2RLX2/ref=pd_sim_200_3?_encoding=UTF8&psc=1&refRID=NMR7SMXJAKC4B3MH0HTN"
    assert get_ASIN(url) == 'B00FA2RLX2'
    url = "https://www.amazon.de/Notverpflegung-Kg-Marine-wasserdicht-verpackt/dp/B01DFJTYSQ/ref=pd_sim_200_5?_encoding=UTF8&psc=1&refRID=7QM8MPC16XYBAZMJNMA4"
    assert get_ASIN(url) == 'B01DFJTYSQ'
    url = "https://www.amazon.de/dp/B01N32MQOA?psc=1"
    assert get_ASIN(url) == 'B01N32MQOA'


def test_capture_urls():
    text = "/cupon ASDASD 123€ https://www.amazon.es/gp/aw/d/B06XFWF7J4/ref=ox_sc_act_image_1?smid=A1AT7YVPFBWXBL&psc=1"
    assert isinstance(capture_urls(text), list)


def test_expand_url():
    short = 'https://amzn.to/31ftG0O'
    expanded = 'https://www.amazon.es/WOWGO-autom%C3%A1tica-Dispensador-silenciosa-Anti-mordedura/dp/B07CHKP6JW?SubscriptionId=AKIAIKPCRXSD7LRXGZWQ&tag=chollosxpress-21&linkCode=xm2&camp=2025&creative=165953&creativeASIN=B07CHKP6JW'
    assert expand_url(short) == expanded
    assert expand_url('no_url') is 'no_url'


def test_is_aliexpress():
    url = 'https://es.aliexpress.com/item/10000008027797.html?mb=zNbw7rRQY4RJmED&srcSns=Plus&tid=white_backgroup_101&tt=org.telegram.plus&image=U229e328280e24b66a06e8d1ed8f6e6bax.jpg&aff_request_id=9bc2a5b41978475583a918e1c36dcd45-1586772007439-06914-_dZdXx5S&spreadType=socialShare&aff_platform=default&sk=_dZdXx5S&aff_trace_key=9bc2a5b41978475583a918e1c36dcd45-1586772007439-06914-_dZdXx5S&businessType=ProductDetail&templateId=white_backgroup_101&title=%E2%82%AC+199%2C49++24%25de+DESCUENTO+%7C+CHUWI+HeroBook+pantalla+IPS+de+14%2C1+pulgadas+Intel+E8000+Quad+Core+Windows+10+OS+4GB+RAM+64GB+ROM+ordenador+port%C3%A1til+con+la+disposici%C3%B3n+de+teclado&platform=AE&terminal_id=d0cf318a7415401e8bd43cacb8e3fd67'
    assert is_aliexpress(url)
