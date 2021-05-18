import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Web scrapper for infinite scrolling page
driver = webdriver.Chrome(executable_path=r"D:\chromedriver.exe")
driver.get("https://store.steampowered.com/search/?filter=topsellers")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1
scrolls = 0
game_names = []
game_urls =[]
size = 0

#Creating CSV File For Storing Data
outfile = open('game_list.csv','w', newline='',encoding="utf-8")
writer = csv.writer(outfile)
writer.writerow(["Game Name", "Game URL"])

while scrolls<500:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    scrolls = scrolls + 1
    if (screen_height) * i > scroll_height:
        break


##### Extract Steam URLS URLs #####
urls = []
soup = BeautifulSoup(driver.page_source, "html.parser")
for parent in soup.find_all(class_="col search_name ellipsis"):
    title_tag = parent.find(class_="title")
    name = title_tag.text
    game_names.append(name)

size = len(game_names)


#Finding URLS Of Games
for parent in soup.find_all(id ="search_resultsRows"):
    #"search_result_row ds_collapse_flag app_impression_tracked"
    #search_resultsRows
    for i in parent.findAll('a'):
        #print(i['href'])
        urls.append(i['href'])

for i in range(0,size):
    writer.writerow([game_names[i], urls[i]])
    print(game_names[i]," : ",urls[i])

print("Games Scraped:",size)
outfile.close()



