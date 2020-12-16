from random import randint
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def login():
    try:
        driver.get("https://steamcommunity.com/login")

        driver.find_element_by_id("input_username").send_keys(userId)
        driver.find_element_by_id("input_password").send_keys(password)
        driver.find_element_by_class_name("btn_blue_steamui").click()

        if isEmailAuth:
            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.ID, "authcode")))

            code = input("이메일 인증 번호를 입력하세요: ").upper()

            driver.find_element_by_id("authcode").send_keys(code)
            driver.find_element_by_css_selector("#auth_buttonset_entercode > div:nth-child(1)").click()

            WebDriverWait(driver, 5).until(
                ec.element_to_be_clickable((By.ID, "success_continue_btn")))

            driver.find_element_by_id("success_continue_btn").click()
        else:
            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.ID, "twofactorcode_entry")))

            code = input("스팀 가드 인증 코드를 입력하세요: ").upper()

            driver.find_element_by_id("twofactorcode_entry").send_keys(code)
            driver.find_element_by_css_selector("#login_twofactorauth_buttonset_entercode > div:nth-child(1)").click()
    except Exception as e:
        print(f"로그인하던 중 오류가 발생했습니다. 오류: {e}")


def block_profile():
    try:
        driver.get(file)
        driver.execute_script("ConfirmBlock();")
        driver.find_element_by_class_name("btn_green_steamui").click()

        waitTime = randint(5, 10)
        print(f"유저를 차단했지만 오류 방지를 위해 {waitTime}초 동안 기다리고 있습니다.")
        sleep(waitTime)
    except Exception as e:
        print(f"프로필을 차단하던 중 오류가 발생했습니다. 오류: {e}")


print("스팀 프로필 차단기\n제작자: green1052\n")
print("이메일 인증 = y 스팀 가드 인증 = n\n")
userId = input("아이디를 입력해주세요: ")
password = input("비밀번호를 입력해주세요: ")
isEmailAuth = True if input("이메일 인증을 사용하고 있습니까?: ").lower() == "y" else False

if not userId or not password:
    print("잘못된 입력")
    exit()

options = Options()
options.headless = True

profile = webdriver.FirefoxProfile()
profile.set_preference("security.enterprise_roots.enabled", True)

driver = webdriver.Firefox(options=options, firefox_profile=profile)

try:
    print("로그인을 하고 있습니다.")
    login()
    print("완료")

    for file in open("profiles.txt", encoding="utf-8").read().split('\n'):
        if file is None or "http" not in file:
            continue

        block_profile()
except Exception as e:
    print(f"메인 코드에서 오류가 발생했습니다. 오류: {e}")
finally:
    driver.quit()
