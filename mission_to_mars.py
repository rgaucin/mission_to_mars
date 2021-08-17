#!/usr/bin/env python
# coding: utf-8

# In[31]:


# import splinter and beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[18]:


executable_path = {"executable_path": ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path, headless=False)


# In[10]:


url = "https://redplanetscience.com"
browser.visit(url)
# optional delay for loading page
browser.is_element_present_by_css("div.list_text", wait_time=1)


# In[11]:


html = browser.html
news_soup = soup(html, "html.parser")
slide_elem = news_soup.select_one("div.list_text")


# In[13]:


news_title = slide_elem.select_one("div.content_title").get_text()
news_title


# In[15]:


news_p = slide_elem.select_one("div.article_teaser_body").get_text()
news_p


# In[16]:


browser.quit()


# ### Featured Images

# In[19]:


url = "https://spaceimages-mars.com"
browser.visit(url)


# In[20]:


# find and click the full image button
full_image_elem = browser.find_by_tag("button")[1]
full_image_elem.click()


# In[25]:


html = browser.html
img_soup = soup(html, "html.parser")


# In[29]:


# get relative img url
img_url_rel = img_soup.select_one("img.fancybox-image").get("src")
img_url_rel


# In[30]:


img_url = f"https://spaceimages-mars.com/{img_url_rel}"
img_url


# In[39]:


df = pd.read_html("https://galaxyfacts-mars.com")[0]
df.columns=["description", "mars", "earth"]
df.set_index("description", inplace=True)
df


# In[40]:


df.to_html()


# In[ ]:




