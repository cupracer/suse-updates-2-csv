#!/usr/bin/python

import sys
import getopt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests


def run_query(date_from, date_to, offset, limit):
    url = 'https://www.suse.com/support/ajax/?fields[node--support_update_item]=field_announcement_id,' \
            'field_category,field_release_date,' \
            'field_severity,path,title,field_content_formatted_long.value&sort=-field_release_date&filter[' \
            'date-filter][condition][path]=field_release_date&filter[date-filter][condition][' \
            'operator]=BETWEEN&filter[date-filter][condition][value][]=' + date_from + '&filter[date-filter]' \
            '[condition][value][]=' + date_to + \
            '&filter%5Bstatus%5D%5Bvalue%5D=1&page%5Boffset%5D=' + str(offset) + '&page%5Blimit%5D=' + str(limit)

    resp = requests.get(url=url)
    result = resp.json()

    if not result['data']:
        return True

    for row in result['data']:
        attr = row['attributes']
        title = attr['title']
        announcement_id = attr['field_announcement_id']
        category = attr['field_category']
        release_date = attr['field_release_date']
        severity = attr['field_severity']
        print(category + ';' + severity + ';' + announcement_id + ';' + title + ';' + release_date)

    run_query(date_from, date_to, offset + limit, limit)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('requires month to fetch in format: MM-YYYY')
        exit(1)

    date_str = str(sys.argv[1])
    date_obj = datetime.strptime(date_str, '%m-%Y')

    start_date = date_obj.replace(day=1)
    end_date = start_date + relativedelta(months=1) - timedelta(days=1)

    run_query(datetime.strftime(start_date, '%Y-%m-%d'), datetime.strftime(end_date, '%Y-%m-%d'), 0, 50)
