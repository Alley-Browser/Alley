"""Tests for setting cookies in CustomWebEnginePage.

The tests verify that:

- setCookie adds a cookie with the expected name and value
- setCookie replaces existing cookies with the same name 
- setCookie sets the expected cookie attributes
"""
import pytest
from PyQt5.QtNetwork import QNetworkCookie
from src.CustomWebEnginePage import CustomWebEnginePage

@pytest.fixture
def custom_page():
    return CustomWebEnginePage()

def test_set_cookie(custom_page):
    filename = "test.txt"
    custom_page.setCookie(filename)
    
    cookies = custom_page.profile().cookieStore().getAllCookies()
    assert len(cookies) == 1
    assert cookies[0].name() == b"download_warning"
    assert b"filename*=UTF-8''{}".format(filename.encode()) in cookies[0].value()

def test_set_cookie_replace(custom_page):
    custom_page.setCookie("test1.txt")
    custom_page.setCookie("test2.txt")
    
    cookies = custom_page.profile().cookieStore().getAllCookies()
    assert len(cookies) == 1
    assert cookies[0].name() == b"download_warning"
    assert b"test2.txt" in cookies[0].value()
    
def test_set_cookie_attributes(custom_page):
    custom_page.setCookie("test.txt")
    cookie = custom_page.profile().cookieStore().getAllCookies()[0]

    assert cookie.isHttpOnly() == False
    assert cookie.isSecure() == False
    assert cookie.path() == b"/"
    assert cookie.sameSite() == QNetworkCookie.SameSiteLax
