# Imports
import requests
from datetime import datetime
import os
import sys


# "multireddit" function
def multireddit(subreddits, user, limit=5, orderby='score'):

    # Header information - Reddit username
    headers = {'user-agent': 'reddit-{}'.format(user)}


    ''' Displays an HTML listing of the top `limit` articles from the
    various `subreddits` specified by the user.  These articles will be
    sorted by the field specified by `orderby`

      - `subreddits` is a comma-separated list of subreddits (ie.
        `linux,linuxmasterrace`)

      - `orderby` is any field in the Reddit JSON data for a particular
        article (ie. `score`, `title`, `created_utc`, etc.)
    '''

    # Process function arguments
    subreddits = [subreddit.strip() for subreddit in subreddits.split(',')]

    urls = []
    articles = []
    for item in subreddits:
        URL = 'https://www.reddit.com/r/' + item + '/.json'
        urls.append(URL)
        #print(URL)

    # Fetch subreddit data
    for url in urls:
        response = requests.get(url, params=item, headers=headers)
        print(url)
        data = response.json()
        subdata = data['data']
        children = subdata['children']
        #       print(type(children))
        for child in children:
            #            print('\n')
            childData = child['data']
            articles.append(child['data'])

    # Sort and limit data, and construct HTML results
    index = 0  # keep track of article number
    html = '<table><tbody>'
    for article in sorted(articles, reverse=True, key=lambda a: a[orderby])[:limit]:
        index += 1
        LN = article['url']  # link to article
        cmLN = 'https://www.reddit.com/' + article['permalink']  # link to comments
        html += f'''
        <tr>
            <td>{str(index) + '.'}</td>
            <td style="text-align: left"><a href="{LN}">{article['title']}</td>
            <td style="text-align: right">Score: {article['score']}</td>
            <td><a href="{cmLN}">Comments</td>
        </tr>'''
    return html


if __name__ == '__main__':
    # DEFINE PROGRAM PARAMETERS
    NEW_PAGE_NAME = 'reddit_' + ('_'.join(item for item in str(datetime.now()).split(' '))).replace(':', '_').replace('.', '_') + '.html'
    USER = 'AcademyNEXT2020'
    ORDERBY = 'score'
    SUBREDDITS = 'Python, MachineLearning'

    # CALL "MULTIREDDIT" AND RETURN HTML-FORMATTED DATA
    generated_html = multireddit(SUBREDDITS, USER, limit=100, orderby=ORDERBY)

    # SAVE HTML WEB PAGE (default is current working directory based on user's operating system parameters)
    with open(os.path.join(sys.path[0], NEW_PAGE_NAME), "w+") as f:
        if f.write(generated_html):
            print('\nSuccessfully wrote ' + NEW_PAGE_NAME + ' to ' + sys.path[0])
        else:
            print('Error: could not write file to ' + sys.path[0])


