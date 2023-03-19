import os
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlencode
import time
import json
import csv
import pickle
from collections import namedtuple
import argparse
import logging

logger = logging.getLogger("whatsapp")


def encode_string(string):
    return urlencode({"text": string}).replace("text=", "")


def convert_phone(n):
    try:
        return str(int(n))
    except ValueError:
        return n


def type_shift_enter(action_chain):
    action_chain = action_chain.key_down(Keys.SHIFT)
    action_chain = action_chain.key_down(Keys.ENTER)
    action_chain = action_chain.key_up(Keys.SHIFT)
    action_chain = action_chain.key_up(Keys.ENTER)
    action_chain = action_chain.perform()

class Whatsapper:
    def __init__(self):
        self.driver = None

    def open_chrome(self):
        options = webdriver.ChromeOptions()

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        self.driver.get("https://web.whatsapp.com")
        # input("Press ENTER after login into Whatsapp Web and your chats are visiable.")

    def clear_message(self):
        input_box = self.get_input_box()
        actions = ActionChains(self.driver)
        actions = actions.move_to_element(input_box)
        actions = actions.click()
        actions = actions.key_down(Keys.CONTROL)
        actions = actions.send_keys("a")
        actions = actions.key_up(Keys.CONTROL)
        actions = actions.key_down(Keys.BACK_SPACE)
        actions = actions.key_up(Keys.BACK_SPACE)
        actions = actions.perform()

    def load_number(self, phone, message: str = "", verbose: bool = False):
        message = encode_string(message)
        message = f"https://web.whatsapp.com/send/?phone=972{phone}&text={message}&type=phone_number&app_absent=0"
        if verbose is True:
            print(message)
        self.driver.get(message)
        input_box = self.get_input_box()
        successfully_loaded = input_box is not None
        return successfully_loaded

    def get_input_box(self):
        xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            message_input = self.driver.find_element(by=By.XPATH, value=xpath)
            message_input.click()
            return message_input
        except Exception as exc:
            logger.exception(f"Error getting input box", exc_info=exc)

    def write_message(self, message):
        input_box = self.get_input_box()
        self.clear_message()
        message_parts = message.split('\n')
        for i, part in enumerate(message_parts):
            input_box.send_keys(part)
            if i < len(message_parts) - 1:
                type_shift_enter(ActionChains(self.driver))
        return True

    def send(self):
        input_box = self.get_input_box()
        input_box.send_keys("\n")
        return True

    def click_send(self):
        xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.find_element(by=By.XPATH, value=xpath).click()
            return True
        except Exception as exc:
            logger.exception(f"No phone number available!", exc_info=exc)
            return False

    def close(self):
        self.driver.quit()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("messages")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--run-live", action="store_true")
    parser.add_argument("--test-number", default="0587922790")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    is_test = args.run_live is False
    main(args.messages, test=is_test, test_number=args.test_number, no_browser=args.no_browser)
