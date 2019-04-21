import aiohttp
import asyncio
import json
import re
import time
import urllib.request

from bs4 import BeautifulSoup
from flask import render_template, request

from app import app, redis


async def download_all_sites(parsing_list):
    """ Open aiohttp session
        Multiple calls to download_site
        Return result, close session
     """
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(download_site(session, url)) for url in parsing_list[:10]]
        res = await asyncio.gather(*tasks, return_exceptions=True)

    return res


async def download_site(session, url):
    """Get the url content and scrape information
    :param session - aiohttp.ClientSession()
    :param url - a url link to a page
    :return dict
    """

    async with session.get(url) as response:

        page_content = await response.text()
        if not page_content:
            return dict()

        soup = BeautifulSoup(page_content, "html.parser")
        tmp = dict(telephone='', website='', typical_cost='')

        try:  # trying to find all info in the script
            script = soup.find('script', {'type': "application/ld+json"})
            script_text = script.text
            s = f'"my_object" : {script_text}'
            ss = '{' + s + '}'

            new_json_object = json.loads(ss, strict=False)
            contacts = new_json_object.get('my_object')[0]
            tmp['name'] = contacts.get('name')
            tmp['telephone'] = contacts.get('telephone')
            tmp['location'] = ', '.join([v for k, v in contacts.get('address').items() if v and not k.startswith('@')])
            tmp['website'] = contacts.get('website', '')

        except:  # couldn't parse the script / broken json etc
            tmp['name'] = soup.find('h1', {'class': 'hz-profile-header__name'}).string

        # contact name
        contact_container = soup.find('div', {'class': 'container-fluid'})
        if contact_container:
            for span in contact_container.find_all('span', {'class': 'profile-meta__val'}):
                previous_span = span.previous_sibling
                if not previous_span:
                    continue
                if re.search('Contact', str(previous_span)):
                    tmp['contact_name'] = span.string
                elif re.search('Typical Job Costs', str(previous_span.string)):
                    tmp['typical_cost'] = span.string
                elif re.search('Location:', str(previous_span)):
                    if 'location' not in tmp:
                        tmp['location'] = span.text

        if not tmp.get('website'):
            website_acncor = soup.find('a', {'class': 'hz-profile-header__contact-info-item'})
            if website_acncor:
                tmp['website'] = website_acncor.get('href')

        return tmp


@app.route('/project_three', methods=['GET', 'POST'])
def project_three():
    """ Go through the architect portal, collect links to individual pages
    Asynchronously load and scrape each page, return an object, append to a result list
    Keep track of the time spent, present result list as a table
    """

    if request.method == 'GET':
        return render_template('project_three.html')

    start_time = time.time()

    # collect a list of pages to scrape
    url = 'https://www.houzz.com/professionals/architect/c/Woodbridge--ON'
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    parsing_list = []
    for contact_block in soup.find_all('div', {'class': 'hz-pro-search-result__profile-desc'}):
        ancor = contact_block.find('a')
        parsing_list.append(ancor.get('href'))

    html.close()

    # set the event loop for asynchronous calls to download_all_sites method
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(download_all_sites(parsing_list))
    loop.close()

    # return the statistics - TODO make stats in React
    duration = time.time() - start_time
    stats = f'Processed {len(res)} pages in {round(duration, 2)} seconds'

    # save results to redis - try except in case redis server wasn't started
    # try:
    #     i = 1
    #     for tmp in res:
    #         for k, v in tmp.items():
    #             if isinstance(v, type(None)):
    #                 tmp[k] = 'None'  # redis can't have None values
    #         redis.hmset(str(i), tmp, )
    #         i += 1
    # except:
    #     pass

    return render_template('project_three.html', entries=res, stats=stats)

