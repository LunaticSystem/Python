#!/bin/python
'''
TITLE: PatchCheck.py
AUTHOR: Brendan Vandercar
DESCRIPTION: Script logins into netx sites via /saml/netx and verifies that the dashboard comes up.
This was built in order to test sites after the meltdown/spectre patches.

REQUIRED MODULES:
Selenium
Requests
'''

import time
import requests
import logging
import os
from selenium import webdriver
from getpass import getpass
from selenium.webdriver.firefox.options import Options

def log(code, site, logger):
	if code == '0':
		logger.info(site.strip('\n') + ' is up...')
	else:
		logger.error(site.strip('\n') + ' is not accessable...')


def login_saml(url, creds):
	options = Options()
	options.add_argument("--headless")
	driver = webdriver.Firefox(firefox_options=options)
	driver.get(url)
	username = driver.find_element_by_name('UserName')
	password = driver.find_element_by_name('Password')
	username.send_keys('brendan@netx.net')
	#gets credentials passed to it from the creds variable. Hopefully this is a safer method
	password.send_keys(creds)
	driver.find_element_by_id('submitButton').submit()
	time.sleep(10)
	try:
		status = driver.find_element_by_id('dashboard-header')
		print(status)
		#print("Success")
		err = "0"
		return err
	except:
		#print("Unable to access" + site + "/app after login...")
		err = "1"
		return err
	#print(err)
	 

def login_app(url, creds):
	options = Options()
	options.add_argument("--headless")
	driver = webdriver.Firefox(firefox_options=options)
	driver.get(url)
	username = driver.find_element_by_name('UserName')
	password = driver.find_element_by_name('Password')
	username.send_keys('netxsupport')
	#gets credentials passed to it from the creds variable. Hopefully this is a safer method
	password.send_keys(creds)
	driver.find_element_by_id('submitButton').submit()
	time.sleep(10)
	#Try Except statment to verify whether /app loads after initial login via saml
	try:
		status = driver.find_element_by_id('dashboard-header')
		#print("Success")
		err = "1"
		return err
	except:
		#print("Unable to access" + site + "/app after login...")
		err = "1"
		return err
	#print(err)

def main():
	os.environ['USER_SAML'] = getpass('SAML password?')
	os.environ['USER_APP'] = getpass('NetX Support password?')
	log_file = "/tmp/PatchOutput.out"
	f = open('/tmp/sites.txt', 'r')
	if os.path.exists(log_file) == True:
		os.remove(log_file)

	logger = logging.getLogger()
	handler = logging.FileHandler(log_file)
	formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)
	#creds = getpass('What is your saml password > ')
	#options = Options()
	#options.add_argument("--headless")
	#driver = webdriver.Firefox(firefox_options=options)
	#driver = webdriver.Firefox()
	for site in f:
		#site.strip('\n') strips out the newline chars as it was reading a new line
		#at the end of the sites url name.
		url = "https://"+site.strip('\n')+"/saml/netx"
		print(url)
		request = requests.get(url)
		print(request.status_code)
		if request.status_code == 200:
			creds = os.environ['USER_SAML']
			x = login_saml(url, creds)
			log(x, site, logger)
		else:
			url = "https://"+site.strip('\n')+"/app"
			creds = os.environ['USER_APP']
			x = login_app(url, creds)
			log(x, site, logger)
	del os.environ['USER_SAML']
	del os.environ['USER_APP']

if __name__ == "__main__":
	main()
	
		


	




