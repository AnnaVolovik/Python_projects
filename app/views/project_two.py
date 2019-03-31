import traceback

from bs4 import BeautifulSoup
from flask import render_template, request
import openpyxl
from openpyxl.styles import Font
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from app import app, db
from app.models import DentistContacts


@app.route('/project_two', methods=['GET', 'POST'])
def parse_with_selenium():
    """ Iterate over pages and scrape the information needed """
    if request.method == 'GET':
        return render_template('project_two.html')

    url = "https://www.103.ua/list/stomatologii/kiev/"
    page_limit = 2  # by default for demonstration purposes we only go through first two pages

    # selenium part
    res = []

    def parse_block(contact_block):
        """ local helper function to parse contact blocks"""
        ancor_div = contact_block.find('div', {'class': 'Place__mainTitle'})
        ancor = ancor_div.find('a')

        website = ancor.get('href')
        name = ancor.text
        address = contact_block.find('span', {'class': 'Place__addressText'}).text
        phone_div = contact_block.find('div', {'class': 'Place__phoneNumber '})
        try:
            ancor_phone = phone_div.find('a')
            phone = ancor_phone.get('href').replace('tel:', '')
        except:
            phone = None

        return dict(
            name=name,
            address=address,
            phone=phone,
            website=website
            )

    try:
        driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        driver.get(url)

        for page in driver.find_elements_by_class_name('Pagination__page'):

            WebDriverWait(driver, 15).until(page)
            page.click()

            html = driver.page_source
            soup = BeautifulSoup(html)

            # find all contact information blocks
            for contact_block in soup.find_all('div', {'class': 'Place__wrap'}):
                res.append(parse_block(contact_block))

        driver.close()
        driver.quit()

    # backup part written on requests & beautiful soup if selenium fails
    except:
        try:
            # close the driver if it was open
            driver.close()
            driver.quit()
        except:
            pass

    for page_number in range(page_limit):
        page_url = f'{url}?page={page_number}'

        r = requests.get(page_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        # find all contact information blocks
        for contact_block in soup.find_all('div', {'class': 'Place__wrap'}):
            res.append(parse_block(contact_block))

    # sort results by company name
    res.sort(key=lambda x: x['name'])

    # export results to database
    for tmp in res:

        if not db.session.query(DentistContacts).filter(
                DentistContacts.name == tmp['name'],
                DentistContacts.address == tmp['address']).count():

            entry = DentistContacts(**tmp)
            db.session.add(entry)
    try:
        db.session.flush()
        db.session.commit()
    except:
        print(traceback.format_exc())
        db.session.rollback()
        return render_template('project_two.html', error='Произошла ошибка Базы Данных')

    # # write elements into ms excel file
    # # set output file and its styles
    # wb = openpyxl.Workbook()
    # ws = wb.active  # grab the active worksheet
    # bold = Font(bold=True)
    #
    # # add and style the header
    # ws['A1'].value = 'Company name'
    # ws['B1'].value = 'Address'
    # ws['C1'].value = 'Website'
    # ws['D1'].value = 'Phone number'
    #
    # for cell in ws['A1':'D1']:
    #     cell.font = bold
    #
    # row = 2
    # for tmp in res:
    #     ws.cell(row=row, column=0).value = tmp['company']
    #     ws.cell(row=row, column=1).value = tmp['address']
    #     ws.cell(row=row, column=2).value = tmp['website']
    #     ws.cell(row=row, column=3).value = tmp['phone']
    #
    # # add borders style
    #
    # wb.save("output.xlsx")

    return render_template('project_two.html', entries=res)
