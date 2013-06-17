#!/usr/bin/env python
"""
Test syllabus parsing.
"""

import os
import os.path
import unittest

from coursera import coursera_dl

FIREFOX_COOKIES = \
    os.path.join(os.path.dirname(__file__), "fixtures", "firefox_cookies.txt")

CHROME_COOKIES = \
    os.path.join(os.path.dirname(__file__), "fixtures", "chrome_cookies.txt")

FIREFOX_COOKIES_WITHOUT_COURSERA = \
    os.path.join(os.path.dirname(__file__), "fixtures", "firefox_cookies_without_coursera.txt")


class CookiesFileTestCase(unittest.TestCase):

	def test_get_cookiejar_from_firefox_cookies(self):
		from cookielib import MozillaCookieJar
		cj = coursera_dl.get_cookie_jar(FIREFOX_COOKIES)
		self.assertTrue(isinstance(cj, MozillaCookieJar))


	def test_get_cookiejar_from_chrome_cookies(self):
		from cookielib import MozillaCookieJar
		cj = coursera_dl.get_cookie_jar(CHROME_COOKIES)
		self.assertTrue(isinstance(cj, MozillaCookieJar))


	def test_find_cookies_for_class(self):
		import requests
		cj = coursera_dl.find_cookies_for_class(FIREFOX_COOKIES, 'class-001')
		self.assertTrue(isinstance(cj, requests.cookies.RequestsCookieJar))

		self.assertEquals(len(cj), 7)

		domains = cj.list_domains()
		self.assertEquals(len(domains), 2)
		self.assertTrue('www.coursera.org' in domains)
		self.assertTrue('class.coursera.org' in domains)

		paths = cj.list_paths()
		self.assertEquals(len(paths), 2)
		self.assertTrue('/' in paths)
		self.assertTrue('/class-001' in paths)


	def test_did_not_find_cookies_for_class(self):
		import requests
		cj = coursera_dl.find_cookies_for_class(FIREFOX_COOKIES_WITHOUT_COURSERA, 'class-001')
		self.assertTrue(isinstance(cj, requests.cookies.RequestsCookieJar))

		self.assertEquals(len(cj), 0)


	def test_we_have_enough_cookies(self):
		cj = coursera_dl.find_cookies_for_class(FIREFOX_COOKIES, 'class-001')

		self.assertTrue(coursera_dl.do_we_have_enough_cookies(cj, 'class-001'))


	def test_we_dont_have_enough_cookies(self):
		cj = coursera_dl.find_cookies_for_class(FIREFOX_COOKIES_WITHOUT_COURSERA, 'class-001')

		self.assertFalse(coursera_dl.do_we_have_enough_cookies(cj, 'class-001'))

