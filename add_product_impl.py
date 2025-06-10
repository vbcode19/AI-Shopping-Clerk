from termcolor import colored
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time
import random
from driver import SeleniumDriverSingleton
    
class AddProductImpl():
    def __init__(self):
        self._driver = SeleniumDriverSingleton().get_driver()
        self._wait = SeleniumDriverSingleton().get_wait()
        SeleniumDriverSingleton().access_web_page("https://www.delhaize.be/")

    def try_click(self, element):
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            body = self._driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ESCAPE)
            print(colored("Click intercepted, escaped.", "yellow"))
            time.sleep(2)
            return False
        except Exception:
            return False
        
    def search(self, item: str):
        buttons = self._driver.find_elements(By.XPATH, '//button[@data-testid="search-bar-clear"]')
        if buttons:
            self._wait.until(lambda d: self.try_click(buttons[0]))
            time.sleep(2)

        search_input = self._driver.find_element(By.XPATH, '//input[@placeholder="Cherchez des produits ou des recettes"]')
        search_input.clear()
        search_input.send_keys(item)
        time.sleep(random.uniform(1, 2))
        button = self._driver.find_element(By.XPATH, '//button[@aria-label="Lancer la recherche"]')
        self._wait.until(lambda d: self.try_click(button))

    def add_product_to_cart(self, product):
        product_name_span = product.find_element(By.XPATH, './/span[@data-testid="product-name"]')
        product_name = product_name_span.text
        add_button = product.find_element(By.XPATH, './/button[@data-testid="product-block-add"]')
        self._driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_button)
        self._wait.until(lambda d: self.try_click(add_button))
        print(colored(f"Clicked Add button for: {product_name}", "green"))

    def add_product_condition(self, product_name, product_name_to_search):
        if product_name == product_name_to_search:
            return True
        return False

    def add_product_by_name(self, product_name_to_search: str):
        time.sleep(1)
        self.search(product_name_to_search)
        time.sleep(1)
        parent_div = self._driver.find_element(By.XPATH, '//div[@data-testid="search-results-list-wrapper"]')
        list_items = parent_div.find_elements(By.XPATH, './/li[contains(@class, "product-item")]')
        time.sleep(1)
        for i in range(len(list_items)):
            while(True):
                try:
                    # Refetch the parent and all items every loop iteration to avoid stale references
                    parent_div = self._driver.find_element(By.XPATH, '//div[@data-testid="search-results-list-wrapper"]')
                    items = parent_div.find_elements(By.XPATH, './/li[contains(@class, "product-item")]')

                    li = items[i]  # get fresh li reference
                    product_name_span = li.find_element(By.XPATH, './/span[@data-testid="product-name"]')
                    product_name = product_name_span.text
                    if self.add_product_condition(product_name, product_name_to_search):
                        self.add_product_to_cart(li)
                        return True
                    break
                except StaleElementReferenceException:
                    print(colored(f"Stale element at index {i}, retrying.", "red"))
                    time.sleep(2)
                except Exception as e:
                    print(colored(f"Exception at index {i}, retrying. {e}", "red"))
                    time.sleep(2)

        return False


if __name__ == "__main__":
    add_product_impl = AddProductImpl()
    add_product_impl.add_product_by_name("Jonagold | 6PC")
    input("Press Enter to close browser and end script...")
else:
    print(f"Importing module: {__name__}...")

