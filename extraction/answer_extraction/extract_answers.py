#!/usr/bin/env python3

import gcp
from bs4 import BeautifulSoup

version = 12 # increment version to go through pages we are uncertain about again
batch_size = 20

conn, cur = gcp.connect_to_gcp()

print('Connected to DB')

def handle_featured_snippet(snippet):
    short_answer_div = snippet.find('div', attrs={'data-tts': 'answers'})
    short_answer = None
    if short_answer_div:
        short_answer = short_answer_div.get_text()
        short_answer_div.parent.decompose() # make it easier to find long answer
    long_div = snippet.find('div', attrs={'role': 'heading'})
    if long_div and long_div.span:
        long_answer = long_div.span.get_text()
        return 'feat_snip', short_answer, long_answer
    else:
        ol = snippet.find('ol')
        ul = snippet.find('ul')
        if ol and not ol.has_attr('role'): # see 6916 and 4143239
            long_list = [x.get_text() for x in ol.find_all('li')]
            return 'rich_list', short_answer, str(long_list)
        elif ul:
            long_list = [x.get_text() for x in ul.find_all('li')]
            return 'rich_set', short_answer, str(long_list)
        else:
            return 'rich_snip', short_answer, None

def get_split(question, delimiter):
    split = question.split(delimiter)
    if len(split) == 2 and len(split[1]) > 0:
        return split[1]

def handle_unit_converter(featured, question):
    equals = featured.parent.div(text='=')[0]
    count = equals.find_next('input')
    count_value = count.get('value')
    unit = count.find_next('option', {'selected': '1'})
    unit_value = ''
    if unit:
        unit_value = unit.get_text()
    else: # see 13783 and 19581
        unit_value = get_split(question, ' how many ')
        if unit_value is None:
            unit_value = get_split(question, ' equal to ')

    short_answer = count_value # sometimes it's just PEBKAC and no units available; see 20802
    if unit_value:
        short_answer = '{0} {1}'.format(count_value, unit_value)
    return 'unit_conv', short_answer, None

def handle_currency_converter(featured):
    input = featured.parent.find('select')
    count = input.find_next('input')
    count_value = count.get('value')
    unit = count.find_next('option', {'selected': '1'})
    unit_value = unit.get_text()
    short_answer = '{0} {1}'.format(count_value, unit_value)
    return 'curr_conv', short_answer, None

def handle_translation_result(featured):
    # todo: 8349104 as an example of one with another result
    short_answer = featured.parent.find('pre', {'id': 'tw-target-text'}).get_text()
    return 'tr_result', short_answer, None

def handle_local_results(featured):
    return 'local_rst', None, None

def handle_local_time_conversion(featured):
    short_answer = featured.parent.find('div', {'class': 'vk_bk'}).get_text()
    return 'time_conv', short_answer, None

def handle_local_time(featured):
    # strip because sometimes there's whitespace at the end due to div spacing
    short_answer = featured.parent.find('div', {'class': 'vk_bk'}).get_text().strip()
    return 'localtime', short_answer, None

def handle_weather(featured):
    return 'weather', None, None

def handle_kp_header(header):
    gsrt = header.find('div', {'class': 'gsrt'})
    if gsrt:
        short_answer = gsrt.div.get_text()
        return 'knowledge', short_answer, None
    else:
        return None, None, None

def handle_directions(featured):
    return 'direction', None, None

def handle_description(featured):
    return 'descript', None, None

def handle_overview(doc):
    short_ans = doc.a.get_text()
    return 'overview', short_ans, None

def handle_no_snippet(featured):
    # todo: 1119248 and 8349104 as examples of incorrect no_answer extractions
    return 'no_answer', None, None

def has_no_other_answer_markers(doc):
    return doc.find('div', {'class': 'kp-header'}) is None and \
            doc.find('div', {'class': 'answered-question'}) is None

def get_url(snippet):
    r_div = snippet.find('div', attrs={'class': 'r'})
    if r_div:
        return r_div.a['href']

def do_batch():
    cur.execute('''
        SELECT q.id, question, html
        FROM queries AS q
          LEFT JOIN extractions AS e ON q.id = e.id
        WHERE q.html IS NOT NULL
          AND q.id = 7669997
          AND e.answer IS NULL
          AND e.short_answer IS NULL
          AND e.answer_type IS NULL
          AND (e.extract_v < %s OR e.extract_v IS NULL)
        FOR UPDATE OF q SKIP LOCKED
        LIMIT %s;''',
        [version, batch_size])

    for id, question, html in cur.fetchall():
        extraction_type = None
        short_answer = None
        long_answer = None
        url = None

        doc = BeautifulSoup(html, 'html.parser')
        featured = doc.h2
        # the casing in the html is inconsistent, so just always lowercase
        featured_type = featured.get_text().lower() if featured else None

        # Examples of ones where featured snippets do not include h2
        # 1389251
        # 1389246
        # 1389247

        # Example of one where it doesn't include 'kp-header' (it does include "answered-question")
        # 41802

        try:
            if featured_type == 'featured snippet from the web':
                snippet = featured.parent.div
                url = get_url(snippet)
                extraction_type, short_answer, long_answer = handle_featured_snippet(snippet)
            elif featured_type == 'unit converter':
                extraction_type, short_answer, long_answer = handle_unit_converter(featured, question)
            elif featured_type == 'currency converter':
                extraction_type, short_answer, long_answer = handle_currency_converter(featured)
            elif featured_type == 'translation result':
                extraction_type, short_answer, long_answer = handle_translation_result(featured)
            elif featured_type == 'local results':
                extraction_type, short_answer, long_answer = handle_local_results(featured)
            elif featured_type == 'local time conversion':
                extraction_type, short_answer, long_answer = handle_local_time_conversion(featured)
            elif featured_type == 'local time':
                extraction_type, short_answer, long_answer = handle_local_time(featured)
            elif featured_type == 'weather result':
                extraction_type, short_answer, long_answer = handle_weather(featured)
            elif featured_type == 'directions':
                extraction_type, short_answer, long_answer = handle_directions(featured)
            elif featured_type == 'description':
                extraction_type, short_answer, long_answer = handle_description(featured)
            elif featured_type == 'overview':
                extraction_type, short_answer, long_answer = handle_overview(doc)
            elif has_no_other_answer_markers(doc) and ( \
                featured_type == 'web results' or
                featured_type == 'people also ask' or
                featured_type == 'web result with site links' or
                featured_type is None):
                extraction_type, short_answer, long_answer = handle_no_snippet(featured)
            else:
                answered_div = doc.find('div', {'class': 'answered-question'})
                if answered_div:
                    url = get_url(snippet)
                    extraction_type, short_answer, long_answer = handle_featured_snippet(answered_div)
                else:
                    kp_header = doc.find('div', {'class': 'kp-header'})
                    if kp_header:
                        extraction_type, short_answer, long_answer = handle_kp_header(kp_header)
                    else:
                        print('        Unknown featured display "{0}"'.format(featured_type))
        except Exception as e:
            print('Extraction for {0} failed: {1}'.format(id, e))
            continue

        long_str = long_answer
        if long_str and len(long_str) > 50:
            long_str = long_str[:24] + '...' + long_str[-23:]
        print('{0:7} {1:10} Short ans: {2}. Long ans: {3}'.format(
            id,
            str(extraction_type),
            short_answer,
            long_str))
        if short_answer and len(short_answer) > 100: # example: 80100
            print('TODO: Fix length for {0}'.format(id))
            short_answer = None
            answer = None
            answer_type = None
        cur.execute('''
            INSERT INTO extractions (id, short_answer, answer, answer_url, answer_type, extract_v)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE
              SET
                short_answer = EXCLUDED.short_answer,
                answer = EXCLUDED.answer,
                answer_url = EXCLUDED.answer_url,
                answer_type = EXCLUDED.answer_type,
                extract_v = EXCLUDED.extract_v;
        ''', [id, short_answer, long_answer, url, extraction_type, version])
    conn.commit()
    print('Extracted from {0} pages'.format(batch_size))

while True:
    do_batch()

conn.close()