from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import os
import pandas as pd


def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

# Scrape Latest Title and Text

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find('div', class_='list_text')
    print(results)

    title = results.find('div', class_='content_title').text
    text = results.find('div', class_='article_teaser_body').text

# Scrape Featured Image

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # HTML object
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find('div', class_='fancybox-inner')
    print(results)

    img = results.find('img', class_='fancybox-image').get('src')

    # img = results

    # print(img)

    featured_img_url = (url+img)

    # print(featured_image_url)


# Scrape Mars Facts

    # url = 'https://galaxyfacts-mars.com'
    # tables = pd.read_html(url)[0]
    

    # # type(tables)

    # tables.columns=["Description","Mars","Earth"]
    # tables.set_index("Description", inplace=True)

    # stats_table = tables.to_html()

# Scrape Mars Hemispheres  Name & Url

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    # All Hemispheres

    hemisphere_links = soup.find_all('div',class_="item")

    type(hemisphere_links)

    # print(hemisphere_links)

    hemisphere_title_list =[]
    for hemisphere_link in hemisphere_links:
        title = hemisphere_link.find('h3').text
        title = title.strip("Enhanced")
        hemisphere_title_list.append(title)

    # print(hemisphere_title_list)

    hemisphere_url_list =[]
    for hemisphere_link in hemisphere_links:
        link=hemisphere_link.find('a',class_="product-item")['href']
        link = (url+link)
        browser.visit(link)
        browser.links.find_by_partial_text('Open').click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_url = soup.find('img',class_="wide-image").get('src')
        hemisphere_url=(url+hemisphere_url)
        hemisphere_url_list.append(hemisphere_url)

    # print(hemisphere_url_list)

    # Create List of dictionaries for each hemisphere

    hemisphere_image_urls = []
    for i in range(4):
        hemisphere_image_urls.append({"title":hemisphere_title_list[i],"img_url":hemisphere_url_list[i]})

    mars_dict = {
        "Title": title,
        "Text": text,
        "Featured_Img": featured_img_url,
        "Hemispheres_Img": hemisphere_image_urls
    }
    
    # print('-------------')
    # print(mars_dict)
    # print('-------------')

     # Quit the browser
    browser.quit()

    # print(mars_dict)

    return mars_dict
