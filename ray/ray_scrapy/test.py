
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_product_name_by_url(url):
    from bs4 import BeautifulSoup
    import requests
    r  = requests.get(url, headers=headers)
    #print(data)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find("meta", {"name": "keywords"})
    product_name = s.get("content").split(',')[0]
    print(product_name)

    # for tag in soup.find_all("meta"):
    #     if tag.get("name", None) == "keywords":
    #         print(tag.get("content", None))

    #print("YAHOOOooo {}".format(span))

get_product_name_by_url('https://www.amazon.com/Sony-Cancelling-Behind-Neck-Headphones-International/dp/B075XF9VN9')