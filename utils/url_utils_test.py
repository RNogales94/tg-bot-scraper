from utils.url_utils import capture_urls, expand_url


def test_capture_urls():
    text = "/cupon ASDASD 123€ https://www.amazon.es/gp/aw/d/B06XFWF7J4/ref=ox_sc_act_image_1?smid=A1AT7YVPFBWXBL&psc=1"
    assert isinstance(capture_urls(text), list)


def test_expand_url():
    short = 'https://amzn.to/31ftG0O'
    expanded = 'https://www.amazon.es/WOWGO-autom%C3%A1tica-Dispensador-silenciosa-Anti-mordedura/dp/B07CHKP6JW?SubscriptionId=AKIAIKPCRXSD7LRXGZWQ&tag=chollosxpress-21&linkCode=xm2&camp=2025&creative=165953&creativeASIN=B07CHKP6JW'
    assert expand_url(short) == expanded
    assert expand_url('no_url') is None