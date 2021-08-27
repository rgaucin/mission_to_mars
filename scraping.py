# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # intitiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # run all scraping functions and store results in dict
    data = {'news_title' : news_title,
            'news_paragraph' : news_paragraph,
            'featured_image' : featured_image(browser),
            'facts' : mars_facts(),
            'last_modified' : dt.datetime.now(),
            'hemispheres' : hemispheres(browser)}
    
    # stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# JPL Space Images Featured Image
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# Mars Facts
def mars_facts():

    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # convert dataframe to html formate, add bootstrap
    return df.to_html(classes='table table-striped')

def hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # create a list to hold the images and titles.
    hemisphere_image_urls = []

    # retrieve the image urls and titles for each hemisphere.
    hemispheres_html = browser.html
    hemispheres_soup = soup(hemispheres_html, 'html.parser')

    hemisphere_results = hemispheres_soup.select('div.item > a')
    try:
        for result in hemisphere_results:
            item_url = url + result.get('href')
            browser.visit(item_url)
            item_soup = soup(browser.html, 'html.parser')
            image_url = item_soup.select('li > a')[0].get('href')
            image_title = item_soup.select('h2.title')[0].get_text()
            hemisphere_image_urls.append({'img_url':url+image_url, 'title':image_title})
    except AttributeError:
        return None

    # return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == '__main__':
    # if running as script, print scraped data
    print(scrape_all())