
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    # Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Browser
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(.1)

    # Beautiful Soup
    nasa_html = browser.html
    soup = bs(nasa_html, "html.parser")

    # Find title and paragraph
    nasa_headline = soup.find('div', class_='content_title').get_text()
    nasa_teaser = soup.find('div', class_='article_teaser_body').get_text()

    # JPL Mars Space Images
    url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    time.sleep(.1)
    browser.click_link_by_partial_text('FULL IMAGE')
    soup = bs(browser.html, 'html.parser')

    image_src = soup.find_all('img')[1]["src"]
    featured_image_url = jpl_url + image_src

    # Mars Facts
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(mars_facts_url)
    time.sleep(.1)
    mars_facts_soup = bs(browser.html, 'html.parser')

    mars_df = pd.read_html(browser.html)[1]
    mars_facts_html = mars_df.to_html()

    # Mars Hemispheres
    mars_hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemisphere_url)
    time.sleep(.1)
    soup = bs(browser.html, 'html.parser')

    links = soup.find_all('a', class_='itemLink')

    image_data = []
    for l in links:
        try:
            browser.visit(url + l['href'])
            time.sleep(.1)
            soup = bs(browser.html, 'html.parser')
            hemi_title = soup.find('h2', class_='title')
            hemi_link = soup.find('img', class_='wide-image')['src']
            my_dict = {'title': hemi_title.get_text(),
                       'img_url': url + hemi_link}
            image_data.append(my_dict)
        except TypeError:
            pass

    hemisphere_image_urls = []

    for element in image_data:
        if element not in hemisphere_image_urls:
            hemisphere_image_urls.append(element)

    hemisphere_image_urls

    data_scrape = {}
    data_scrape['title'] = title
    data_scrape['paragraph'] = paragraph
    data_scrape['featured_image_url'] = featured_image_url
    data_scrape['mars_facts_html'] = mars_facts_html
    data_scrape['hemisphere_image_urls'] = hemisphere_image_urls

    return data_scrape
