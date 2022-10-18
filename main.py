import pyautogui
import time
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import sys

# Insert information into lines 10-22
HORSE1 = "INSERT HORSE NAME"  # Exact spelling/capitalization required
PREFERRED_DISTANCE1 = 'INSERT PREFERRED DISTANCE'  # Add "m" to the end of distance
PREFERRED_GATE1 = 'INSERT FIRST GATE PREFERENCE'
PREFERRED_GATE2 = 'INSERT SECOND GATE PREFERENCE'
MIN_BUY_IN1 = 0.0  # Insert $ Value buy-in must be over
MAX_BUY_IN1 = 50.0  # Insert $ Value buy-in must be under
METAMASK_PASSWORD = "INSERT PASSWORD HERE"
sys.setrecursionlimit(10**3)   # Total Repetitions of Program
options = webdriver.ChromeOptions()
# Create new user profile, Change settings with minimal aesthetic changes, Use profile name for line 12
options.add_argument(r"--user-data-dir=INSERT FILEPATH OF CHROME USER DATA COPY")
options.add_argument(r'--profile-directory=INSERT CHROME PROFILE NAME')
driver = webdriver.Chrome(executable_path=r"INSERT FILEPATH OF CHROME DRIVER", options=options)


def hover(browser, element):
    element_to_hover_over = element
    hovering = ActionChains(browser).move_to_element(element_to_hover_over)
    hovering.perform()


def prepare_web_browser():  # Sign in to Metamaska and Connect ZED Run
    metamask_sign_in()
    time.sleep(3)
    zed_and_metamask_login()


def metamask_sign_in():
    driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#unlock")  # Metamask extension link
    time.sleep(2)
    driver.maximize_window()
    pyautogui.typewrite(["enter"])  # Switches typing location from search bar to password input
    time.sleep(2)
    pyautogui.typewrite(METAMASK_PASSWORD)
    pyautogui.typewrite(["enter"])


def sign_zed_to_metamask():
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/popup.html'.format('nkbihfbeogaeaoehlefnkodbefgpgknn'))  # Metamask extension ID
    time.sleep(3)
    driver.find_element_by_xpath("//button[@class='button btn-secondary btn--large request-signature__footer__sign-butt"
                                 "on']").click()


def zed_and_metamask_login():
    driver.get("https://zed.run/home")
    time.sleep(3)
    try:
        driver.find_element_by_xpath('//button[text()="START"]').click()
        driver.find_element_by_css_selector('.login-modal .login-options .metamask-login').click()
        time.sleep(2)
        driver.execute_script("window.open('');")
        sign_zed_to_metamask()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
    except NoSuchElementException:  # If Metamask and Zed are already logged in
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])
        pass


def sign_race_metamask():
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/popup.html'.format('nkbihfbeogaeaoehlefnkodbefgpgknn'))
    time.sleep(1.5)
    driver.find_element_by_xpath("//button[@class='button btn-primary btn--large']").click()


def open_class_1_races():
    driver.get("https://zed.run/racing/events?class=1")


def open_class_2_races():
    driver.get("https://zed.run/racing/events?class=2")


def open_class_3_races():
    driver.get("https://zed.run/racing/events?class=3")


def open_class_4_races():
    driver.get("https://zed.run/racing/events?class=4")


def open_class_5_races():
    driver.get("https://zed.run/racing/events?class=5")


def no_races_found():  # If no races are found, loop again after 15 seconds
    time.sleep(15)
    print()
    enter_races(PREFERRED_DISTANCE1, MIN_BUY_IN1, MAX_BUY_IN1, PREFERRED_GATE1, PREFERRED_GATE2,
                HORSE1)


def check_number_of_available_races(race_list):
    if len(race_list) == 0:
        no_races_found()


def create_race_list():  # Create a list of races to loop over to find race that meets criteria
    try:
        try:
            race_list = (driver.find_elements_by_xpath(".//div[@class='panel']"))
            print(len(race_list), "races available")
            return race_list
        except NoSuchElementException:
            no_races_found()
    except exceptions.StaleElementReferenceException:
        create_race_list()


def check_class(race_list):
    try:
        wrong_class_list = []
        for i in race_list:
            element_container = i.find_element_by_xpath(".//div[@class='race-class']")
            element_text = element_container.find_element_by_xpath(".//div[@class='primary-text helpful']")
            try:
                # Determine racing class tag
                element_text.find_element_by_xpath(".//span[@class='racing-tag racing-tag--4 racing-tag--class']").text
            except NoSuchElementException:
                wrong_class_list.append(i)
        for element in wrong_class_list:
            if element in race_list:
                race_list.remove(element)
        print(len(race_list), 'after class')
        check_number_of_available_races(race_list)
        return race_list
    except exceptions.StaleElementReferenceException:
        print("redone")
        check_class(race_list)


def check_registered(race_list):
    try:
        full_races_list = []
        for i in race_list:
            element_container = i.find_element_by_xpath(".//div[@class='registered']")
            element_text = element_container.find_element_by_xpath(".//div[@class='primary-text bold']").text
            registered_players = int(element_text[:-3])
            if registered_players < 12:
                pass
            else:
                full_races_list.append(i)
        for element in full_races_list:
            if element in race_list:
                race_list.remove(element)
        print(len(race_list), 'after registered')
        check_number_of_available_races(race_list)
        return race_list
    except exceptions.StaleElementReferenceException:
        print("redone")
        check_registered(race_list)


def check_distance(race_list, distance):
    try:
        wrong_distance_list = []
        for i in race_list:
            element_container = i.find_element_by_xpath(".//div[@class='distance']")
            element_text = element_container.find_element_by_xpath(".//div[@class='primary-text helpful']").text
            if element_text == distance:
                pass
            else:
                wrong_distance_list.append(i)
        for element in wrong_distance_list:
            if element in race_list:
                race_list.remove(element)
        print(len(race_list), 'after distance')
        check_number_of_available_races(race_list)
        return race_list
    except exceptions.StaleElementReferenceException:
        print("redone")
        check_distance(race_list, distance)


def check_buy_in(race_list, min_buy_in, max_buy_in):
    try:
        wrong_buy_in_list = []
        for i in race_list:
            element_container = i.find_element_by_xpath(".//div[@class='buy-in']")
            try:
                element_text = element_container.find_element_by_xpath(".//div[@class='primary-text bold nomination']")\
                    .text
                cost = element_text.replace('$', '').replace('U', '').replace('S', '').replace('D', '').replace(' ', '')
                if min_buy_in < float(cost) < max_buy_in:
                    i.click()
                    print(cost)
                    time.sleep(1.5)
                else:
                    wrong_buy_in_list.append(i)
            except NoSuchElementException:  # Free race
                pass
        for element in wrong_buy_in_list:
            if element in race_list:
                race_list.remove(element)
        print(len(race_list), 'after buy-in')
        check_number_of_available_races(race_list)
        return race_list
    except exceptions.StaleElementReferenceException:
        print("redone")
        check_buy_in(race_list, min_buy_in, max_buy_in)


def choose_gate(gate, gate2):
    try:
        panel = driver.find_element_by_xpath(".//div[@class='panel open']")
        button_list = panel.find_elements_by_xpath(".//div[@class='gate-btn']")
        length = len(button_list)
        for x in range(length):
            gate_num = button_list[x].find_element_by_xpath(".//div[@class='primary-text secondary bold gate']").text
            print("gate", gate_num)
            if gate_num == gate or gate_num == gate2:
                button_list[x].click()
                return
            else:
                pass
    except NoSuchElementException or exceptions.StaleElementReferenceException:
        print("redone")
        choose_gate(gate, gate2)
    # Go back to races and choose next race with correct criteria


def choose_horse(horse):
    available_horses = driver.find_elements_by_xpath(".//div[@class='horse-infos']")
    for i in available_horses:
        if i.find_element_by_xpath(".//div[@class='primary-text bold mr-3']").text == horse:
            hover(driver, i)
            time.sleep(1)
            print(i.find_element_by_xpath(".//div[@class='primary-text bold mr-3']").text)
            i.find_element_by_xpath(".//button[text()='Enter']").click()
            time.sleep(2)
            driver.find_element_by_xpath(".//button[text()='Confirm']").click()
            return
        else:
            pass
        time.sleep(20)
        no_races_found()


def enter_races(distance, min_buy_in, max_buy_in, gate, gate2, horse):
    open_class_4_races()
    time.sleep(1)
    race_list = create_race_list()
    race_list1 = check_class(race_list)
    race_list2 = check_registered(race_list1)
    race_list3 = check_distance(race_list2, distance)
    race_list4 = check_buy_in(race_list3, min_buy_in, max_buy_in)
    time.sleep(2)
    choose_gate(gate, gate2)
    time.sleep(2)
    choose_horse(horse)
    sign_race_metamask()
    print('waiting 1000s ')
    time.sleep(1500)  # Choose new horse to do by returning


prepare_web_browser()
time.sleep(3)
enter_races(PREFERRED_DISTANCE1, MIN_BUY_IN1, MAX_BUY_IN1, PREFERRED_GATE1, PREFERRED_GATE2, HORSE1)
