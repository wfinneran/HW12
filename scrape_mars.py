from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint

def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    first_title, first_paragraph = mars_news(browser)

    results = {
        "title": first_title,
        "paragraph": first_paragraph,
        "image_URL": mars_image(browser),
        "weather": mars_weather(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemis(browser),
    }

    browser.quit()
    return results


def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')


    first_title = mars_soup.find('div', class_='content_title').text
    first_paragraph = mars_soup.find('div', class_='article_teaser_body').text
    return first_title, first_paragraph

def mars_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    html = browser.html
    images_soup = BeautifulSoup(html, 'html.parser')

    featured_img_url = images_soup.find('figure', class_='lede').a['href']
    featured_img_full_url = f'https://www.jpl.nasa.gov{featured_img_url}'
    return featured_img_full_url

def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    twitter_soup = BeautifulSoup(html, 'html.parser')
    
    first_tweet = twitter_soup.find('p', class_='TweetTextSize').text
    return first_tweet

def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Property', 'Value']
    df.set_index('Property', inplace=True)
    
    return df.to_html()


def mars_hemis(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    html = browser.html
    hemisphere_soup = BeautifulSoup(html, 'html.parser')

    hemisphere_string = []
    links = hemisphere_soup.find_all('h3')
    
    for hemi in links:
        hemisphere_string.append(hemi.text)
    
    hemisphere_image_urls = []

    for hemi in hemisphere_string:
        
        hemisphere_dict = {}
        browser.click_link_by_partial_text(hemi)
        
        hemisphere_dict["img_url"] = browser.find_by_text('Sample')['href']
        hemisphere_dict["title"] = hemi
        
        hemisphere_image_urls.append(hemisphere_dict)
        
        pprint(hemisphere_image_urls)
        
        browser.back()
    
        return hemisphere_image_urls





