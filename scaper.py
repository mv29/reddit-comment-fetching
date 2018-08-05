import urllib.request
import json
from bs4 import BeautifulSoup as bs

all_comment=[]
def comments(url):
    # print(url)
    #headers adding the user agent for avoiding the blocking error
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'})
    html = urllib.request.urlopen(request).read()
    soup = bs(html, 'html.parser')

    mainpost = soup.find('div', attrs={'id': 'siteTable'})

    title =   mainpost.find('a', attrs={'class': 'title'}).text
    upvotes = mainpost.find('div', attrs={'class': 'score unvoted'}).text
    poster =  mainpost.find('a', attrs={'class': 'author'}).text

    comment_area = soup.find('div', attrs={'class': 'commentarea'})
    #finding the all the upvoted comments
    comments = comment_area.find_all('div', attrs={'class': 'entry unvoted'})

    extracted_comments = []
    for c in comments:
        if c.find('form'):
            commenter = c.find('a', attrs={'class': 'author'}).text
            comment_text = c.find('div', attrs={'class': 'md'}).text
            permalink = c.find('a', attrs={'class': 'bylink'})['href']
            extracted_comments.append({'commenter': commenter, 'comment_text': comment_text, 'permalink': permalink})

    all_comment.append({'url':url,'title':title,'upvotes':upvotes,'poster':poster,'comments':extracted_comments})


url="https://old.reddit.com/top/"
#making request to the reqiured url
request = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'})
html = urllib.request.urlopen(request).read()

# creating the parser
soup=bs(html,'html.parser')

#finding the div element with id siteTable
table=soup.find("div",attrs={'id': 'siteTable'})
#finding  all the  tags with the reqiured class which will give the url to the comments page of a particular post
comment=table.find_all('a',attrs={'class': 'bylink comments may-blank'})

urls=[]
#creating a list allthe urls for traversing the different pages
for i in comment:
    url=i['href']
    if not url.startswith('http'):
        url='https://reddit.com'+url
    urls.append(url)

for i in urls:
    comments(i)


with open('data.json', 'w') as outfile:
    json.dump(all_comment, outfile)






