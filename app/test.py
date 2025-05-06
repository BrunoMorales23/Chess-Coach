from flask import Flask, render_template, request, session
from playwright.sync_api import sync_playwright
import time

url = "https://www.youtube.com"
p = sync_playwright().start()
browser = p.chromium.launch(headless=False)
page = browser.new_page()
print(page)
page.goto(url)
print(page)
time.sleep(10)
url = "https://www.google.com"
page.goto(url)
time.sleep(10)
