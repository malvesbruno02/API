name = str(input('Search Product: ')).strip().lower().capitalize()

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=options)
driver.get(f"https://shopping.google.com.br/?pli=1")
search_bar = driver.find_element(By.ID, 'REsRA')
search_bar.send_keys(name)
search_bar.send_keys(Keys.ENTER)
time.sleep(1)
produtos = driver.find_elements(By.CLASS_NAME, 'sh-dgr__grid-result')
count = 0

product_list = []
product_dict = {}
for produto in produtos:
    link = produto.find_element(By.CLASS_NAME, 'mnIHsc')
    link = link.find_element(By.TAG_NAME, 'a')
    link = link.get_attribute('href')
    site = produto.find_element(By.CLASS_NAME, 'aULzUe')
    product = produto.find_element(By.CLASS_NAME, 'C7Lkve')
    product_atr = product.text.split('\n')
    price = produto.find_element(By.CLASS_NAME, 'XrAfOe')
    price = price.text.split('\n')[0]
    price = price.replace('R$ ', '').replace('.', '').replace(',', '.')
    if len(price.split(' ')) == 2:
        price_h = price.split(' ')
        price = float(price_h[0])
        o_price = float(price_h[1])
    elif 'Custava' in price:
        price = price.replace('· Custava ', '')
        price_h = price.split(' ')
        price = float(price_h[0])
        o_price = float(price_h[1])
    else:
        o_price = float(price)
        price = float(price)
    if len(product_atr) == 2:
        product_name = product_atr[0]
        product_info = product_atr[1]
        product_rate = 0
    elif len(product_atr) == 5:
        product_name = product_atr[0]
        product_info = product_atr[-1]
        product_rate = product_atr[1]
    else:
        product_name = product_atr[0]
        product_info = ''
        product_rate = 0
    product_dict['link'] = link
    product_dict['product_name'] = product_name
    product_dict['price'] = price
    product_dict['old_price'] = o_price
    product_dict['product_info'] = product_info
    product_dict['product_rate'] = product_rate
    product_dict['site'] = site.text
    product_list.append(product_dict.copy())
    product_dict.clear()
prices_list = []
for p in product_list:
    prices_list.append(p['price'])
prices_list.sort()
best_prices = []
for pr in prices_list:
    for p in product_list:
        if p['price'] == pr:
            best_prices.append(p.copy())
for produ in best_prices:
    print(produ)
print(len(product_list))
