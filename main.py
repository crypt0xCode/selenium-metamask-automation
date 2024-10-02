from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging
from logging import FileHandler, Formatter
import time
import config
import json

'''
This demo script connect MetaMask wallet and add new Mainnet Scroll into MetaMask.
'''

# Setting up logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = FileHandler(filename='logs.txt')
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

logger.info("Starting application.")

msg = ''
exception_msg = ''

# Create webdriver options.
options = Options()
options.add_argument(f'user-agent: {UserAgent.random}')
options.add_extension(config.MTM_PATH)

# Install Chrome webdriver automatically.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                          options=options)
driver.implicitly_wait(10)


if __name__ == "__main__":
    driver.get('https://google.com')
    time.sleep(5)
    
    logger.debug("Opening Chrome browser + MetaMask extension.")
    msg = "Opening Chrome browser + MetaMask extension."
    print(msg)

    general_handler = driver.window_handles[0]
    mtm_handler = driver.window_handles[2]    
    driver.switch_to.window(mtm_handler)
    
    #region MetaMask automation.
    logger.debug("Starting MetaMask login stage automation")
    msg = "Starting MetaMask login stage automation"
    print(msg)

    # Press on agreement flag.
    driver.find_element(by=By.XPATH, value='//*[@id="onboarding__terms-checkbox"]').click()
    
    # Press on login in wallet.
    driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[3]/button').click()
    # Press on Continue.
    driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button[2]').click()

    # Load secret phrase from json.
    wallet_data = dict()
    with open(config.JSON_WALLET_PATH, 'r') as f:
        wallet_data = json.load(f)
    
    # Insert secret phrase.
    phrase = wallet_data['secret phrase']
    for i in range(len(phrase)):
        # MTM word frame id.
        driver.find_element(by=By.XPATH, value=f'//*[@id="import-srp__srp-word-{i}"]').send_keys(phrase[i])
        
    driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/button').click()
    
    # Insert password.
    password = wallet_data['password']
    for i in range(1,3):
        driver.find_element(by=By.XPATH, value=f'//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[{i}]/label/input').send_keys(password)
    driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/span[1]/input').click()
    driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button').click()

    logger.debug("Login into MetaMask is done")
    msg = "Login into MetaMask is done"
    print(msg)
    # Start using MTM.
    for i in range(0,3):
        driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button').click()
    
    # Pause for MetaMask page correctly update.
    time.sleep(5)

    logger.debug("Starting adding Scroll Mainnet.")
    msg = "Starting adding Scroll Mainnet."
    print(msg)
    # Add new net.
    driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[2]/div/div[1]/button/span[1]').click()
    driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[3]/div/section/div[3]/button').click()
    driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[3]/a/h6').click()    
    
    net_data = dict()
    with open(config.JSON_NET_PATH, 'r') as f:
        net_data = json.load(f)
    
    # Insert net data in MTM.
    driver.find_element(by=By.XPATH, value=f'//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/input').send_keys(net_data['net-name'])
    driver.find_element(by=By.XPATH, value=f'//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/label/input').send_keys(net_data['url-rpc'])
    driver.find_element(by=By.XPATH, value=f'//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div/input').send_keys(net_data['blockchain-id'])
    driver.find_element(by=By.XPATH, value=f'//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[4]/div/input').send_keys(net_data['currency'])
    
    # Complete net inserting.
    driver.find_element(by=By.XPATH, value='//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/button[2]').click()    
    #endregion

    time.sleep(5)

    logger.debug("Adding Scroll Mainnet is done.")
    msg = "Adding Scroll Mainnet is done."
    print(msg)
    # If MetaMask show notice after adding Mainnet.
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="popover-content"]/div/div/section/div[1]/div/button').click()    
    except Exception as exc:
        exception_msg = exc.__traceback__.__str__
        logger.warning(exception_msg)
    finally:    
        input("Press Enter to continue . . .")
        logger.info("Exiting from application.")
        driver.close()
        driver.quit()
    