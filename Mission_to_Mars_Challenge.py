# Import Splinter, BeautifulSoup, ChromeDriver, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_all():
    
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemi_list,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            "div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image


def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"

    return img_url

# ## Mars Facts


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# ### Mars Weather

def hemispheres(browser):

    # Visit the weather website
    url = 'https://mars.nasa.gov/insight/weather/'
    browser.visit(url)

    # Parse the data
    html = browser.html
    weather_soup = soup(html, 'html.parser')

    # Scrape the Daily Weather Report table
    weather_table = weather_soup.find('table', class_='mb_table')
    print(weather_table.prettify())

    # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

    # ### Hemispheres

    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    hemi_title = hemi_soup.find_all("h3")
    hemi_titles = []
    rel_urls =[]
    for title in hemi_title:
        hemi_title = title.text
        hemi_titles.append(hemi_title)
        for title in hemi_titles:
            browser.visit(url)
            html = browser.html
            hemi_soup = soup(html, 'html.parser')
            
            link_element = browser.links.find_by_partial_text(title)
            link_element.click()
                
            hypertext = browser.html
            img_soup = soup(hypertext, 'html.parser')
                
            rel_url =  img_soup.select_one("img.wide-image").get('src')
            if rel_url not in rel_urls:
                rel_urls.append(rel_url)
            
    for url in rel_urls:
        full_img_url = f'https://astrogeology.usgs.gov{url}'
        hemisphere_image_urls.append(full_img_url)
        
    hemi_zip = zip(hemisphere_image_urls, hemi_titles)
    hemi_list = []
    for img_url, title in hemi_zip:
        hemispheres = {}
        
        hemispheres['img_url'] = img_url
        
        hemispheres['title'] = title
        
        hemi_list.append(hemispheres)

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemi_list

    # 5. Quit the browser
    browser.quit()
