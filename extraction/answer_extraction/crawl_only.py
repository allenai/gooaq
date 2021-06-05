#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from gcp import connect_to_gcp
from fake_useragent import UserAgent
import psycopg2
import sys
import time
import random
import threading
import urllib.parse

task_batch_size = 10
concurrent_sessions = 3 if len(sys.argv) < 2 else int(sys.argv[1])
ua = UserAgent()

class CrawlWindow(threading.Thread):
    count = 0

    def __init__(self):
        threading.Thread.__init__(self)

        CrawlWindow.count += 1
        self.id = CrawlWindow.count

        chrome_options = Options()
        chrome_options.add_argument("--window-size=1024x768")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('log-level=3')
        agent = ua.random
        print('Window {0} using user agent {1}'.format(self.id, agent))
        chrome_options.add_argument('user-agent={0}'.format(ua.random))
        self.driver = webdriver.Chrome(options=chrome_options)

        self.conn, self.cur = connect_to_gcp()
        print('Window {0} successfully connected to DB'.format(self.id))

    def ask_google(self, query):
        # Search for query
        query = urllib.parse.quote(query)
        self.driver.get('http://www.google.com/search?q=' + query)

        # Get HTML only
        return self.driver.find_element_by_xpath('//div[@id="search"]').get_attribute("outerHTML")

    def crawl(self, i, question):
        html = self.ask_google(question)
        self.cur.execute('UPDATE queries SET html = %s WHERE id = %s;', [html, i])
        print('Window {2} retrieved HTML for question {0}: {1}'.format(i, question, self.id))

    def do_tasks(self, tasks):
        for i, question in tasks:
            self.crawl(i, question)
            time.sleep(random.randint(2, 10))

    def run(self):
        while True:
            self.cur.execute(
                    '''
                    SELECT id, question 
                    FROM queries 
                    WHERE html IS NULL 
                    FOR UPDATE SKIP LOCKED 
                    LIMIT %s;
                    ''',
                    [task_batch_size])
            self.do_tasks(self.cur.fetchmany(task_batch_size))
            # "for update skip locked" means that we shouldn't commit until all tasks
            # in a batch are done
            self.conn.commit()
            print('Window {1} finished {0} tasks'.format(task_batch_size, self.id))

for _ in range(concurrent_sessions):
    CrawlWindow().start()
