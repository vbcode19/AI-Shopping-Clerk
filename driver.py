from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import threading
from termcolor import colored

class SeleniumDriverSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SeleniumDriverSingleton, cls).__new__(cls)
                cls._instance._init_driver()
            return cls._instance

    def _init_driver(self):
        self.accessed = False
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=0.1)
        self.driver.maximize_window()

    def get_driver(self):
        return self.driver

    def get_wait(self):
        return self.wait

    def close_cookies(self):
        driver = self.driver
        button = driver.find_element(By.XPATH, '//button//div[@data-testid="button-text" and text()="Français"]')
        time.sleep(random.uniform(1, 2))
        button.click()

        button = driver.find_element(By.XPATH, '//button//div[@data-testid="button-text" and text()="Accepter"]')
        time.sleep(random.uniform(1, 2))
        button.click()

    def access_web_page(self, url: str):
        if not self.accessed:
            self.driver.get(url)
            print(colored(f"Access {self.driver.title}", 'green'))
            self.driver.implicitly_wait(2)
            self.close_cookies()
        self.accessed = True

    def show_popup_and_get_result(self) -> str:
        
        # Inject custom modal
        self.driver.execute_script("""
        const existing = document.getElementById('customPromptModal');
        if (existing) existing.remove();

        const modal = document.createElement('div');
        modal.id = 'customPromptModal';
        modal.innerHTML = `
            <div style="
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background: rgba(0, 0, 0, 0.6);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                font-family: Arial, sans-serif;
            ">
                <div style="
                    background: #fff;
                    padding: 30px 25px;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                    width: 90%;
                    max-width: 400px;
                    box-sizing: border-box;
                    text-align: center;
                ">
                    <h2 style="margin-top: 0; font-size: 24px; color: #333;">How may I help you?</h2>
                    <input
                        type="text"
                        id="recipeInput"
                        placeholder="Type your request here..."
                        style="
                            width: 100%;
                            box-sizing: border-box;
                            padding: 12px 15px;
                            font-size: 16px;
                            border: 1px solid #ccc;
                            border-radius: 8px;
                            outline: none;
                            margin-top: 10px;
                            margin-bottom: 20px;
                        "
                    />
                    <br/>
                    <button
                        onclick="
                            window._customInputValue = document.getElementById('recipeInput').value;
                            document.getElementById('customPromptModal').remove();
                        "
                        style="
                            padding: 10px 20px;
                            font-size: 16px;
                            background-color: #007BFF;
                            color: white;
                            border: none;
                            border-radius: 8px;
                            cursor: pointer;
                        "
                    >Submit</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        """)

        # Wait for user to input
        print("Waiting for user input in browser...")
        while True:
            value = self.driver.execute_script("return window._customInputValue || null;")
            if value:
                break
            time.sleep(0.5)

        return value
