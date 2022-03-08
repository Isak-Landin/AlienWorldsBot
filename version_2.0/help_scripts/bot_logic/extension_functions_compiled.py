from selenium import webdriver
import time
import random
import json
from help_scripts import selenium_operator as sop
import traceback
from help_scripts import bot_actions
from help_scripts import get_proxies
from pathlib import Path
from selenium.webdriver.common.keys import Keys


def setup_extension(driver, window_id):
    driver = driver
    region = (window_id.topleft[0], window_id.topleft[1], window_id.width, window_id.height)
    parent_handle = driver.window_handles[0]
    driver = download_extension(driver=driver, window_id=window_id, region=region, parent_handle=parent_handle)
    configure_extension(driver=driver, window_id=window_id)
    driver = activate_profile(driver=driver)

    return driver


def download_extension(driver, window_id, region, parent_handle):
    driver.get('https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif')
    accept_cookies, succeeded = sop.find_object_XPATH(
        driver=driver,
        time_to_wait=25,
        _xpath='/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div/div/button'
    )

    if succeeded is False:
        print('Failed to find accept_cookies')
        print(traceback.print_exc())
        exit()

    accept_cookies.click()

    add_extension, succeeded = sop.find_object_XPATH(
        driver=driver,
        time_to_wait=7,
        _xpath='/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div'
    )

    time.sleep(2)
    if succeeded is False:
        add_extension, succeeded = sop.find_object_XPATH(
            driver=driver,
            time_to_wait=7,
            _xpath='/html/body/div[5]/div[2]/div/div/div[2]/div[2]/div'
        )
        #           /html/body/div[5]/div[2]/div/div/div[2]/div[2]/div

    if succeeded is False:
        print('Failed to find add_extension')
        print(traceback.print_exc())
        exit()

    add_extension.click()

    window_id.minimize()
    time.sleep(0.2)
    window_id.restore()

    add_extension_region = bot_actions.VisualActions.find_image(
        image=str(Path().resolve()) + r'\alienworlds_program_data\images\add_extension.png',
        region=region,
        confidence=0.85
    )
    start_time = time.time()
    while add_extension_region is None:
        add_extension_region = bot_actions.VisualActions.find_image(
            image=str(Path().resolve()) + r'\alienworlds_program_data\images\add_extension.png',
            region=region,
            confidence=0.85
        )

        if time.time() - start_time > 12:
            exit('SHUTDOWN due to waiting too long for add_extension.png')

    add_extension_region_center = bot_actions.VisualActions.get_center(add_extension_region)
    bot_actions.VisualActions.move_to_click(coordinates=add_extension_region_center, duration=0.15)

    while len(driver.window_handles) < 2:
        time.sleep(0.2)
        print('Looking for new handle')

    for handle in driver.window_handles:
        if handle != parent_handle:
            driver.close()
            parent_handle = handle
            driver.switch_to.window(parent_handle)

    return driver


def configure_extension(driver, window_id):
    skip_guide, succeeded = sop.find_object_XPATH(
        driver=driver,
        time_to_wait=15,
        _xpath='/html/body/div[4]/div/div/div[3]/button[1]'
    )

    if succeeded is False:
        print('Failed to find skip_guide')
        exit('Failed to find skip_guide')

    sop.click_object(skip_guide)

    proxy_profile, succeeded = sop.find_object_XPATH(
        driver=driver,
        time_to_wait=15,
        _xpath='/html/body/div[1]/header/nav/li[7]/a'
    )

    if succeeded is False:
        print('Failed to find proxy_profile')
        exit('Failed to find proxy_profile')

    sop.click_object(proxy_profile)

    server_ip, succeeded = sop.find_object_XPATH(
        driver=driver,
        time_to_wait=10,
        _xpath='/html/body/div[1]/main/div[2]/div/section[1]/div/table/tbody[1]/tr[1]/td[3]/input'
    )

    if succeeded is False:
        print('Failed to find server_ip')
        exit('Failed to find server_ip')

    server_port, succeeded = sop.find_object_XPATH(
        driver=driver,
        time_to_wait=15,
        _xpath='/html/body/div[1]/main/div[2]/div/section[1]/div/table/tbody[1]/tr[1]/td[4]/input'
    )

    if succeeded is False:
        print('Failed to find server_port')
        exit('Failed to find server_port')

    proxies = get_proxies.get_ten_and_check_online()
    random_index = random.randint(0, len(proxies) - 1)
    proxy_port = proxies.pop(random_index)[0]
    proxy = proxy_port.split(':')[0]
    port = proxy_port.split(':')[1]

    server_ip.clear()
    server_port.clear()
    server_ip.send_keys(proxy)
    server_port.send_keys(port)

    time.sleep(2)

    apply_changes, succeeded = sop.find_object_XPATH(
        driver=driver,
        time_to_wait=10,
        _xpath='/html/body/div[1]/header/nav/li[12]/a'
    )

    if succeeded is False:
        print('Failed to find apply_changes')
        exit('Failed to find apply_changes')

    sop.click_object(apply_changes)


def activate_profile(driver):
    time.sleep(3)
    driver.get('chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html')

    old_handle = driver.window_handles[0]
    time.sleep(0.15)
    driver.execute_script('''window.open("http://www.blankwebsite.com/", "_blank");''')
    time.sleep(1)
    new_handle = None
    for handle in driver.window_handles:
        if handle != old_handle:
            new_handle = handle
            break

    time.sleep(2)

    proxy_profile, succeeded = sop.find_object_XPATH(
        driver=driver,
        time_to_wait=10,
        _xpath='//*[@id="js-profile-1"]'
    )

    if succeeded is False:
        print('Failed to find your proxy_profile, please contact us or try again')
        exit('Failed to find your proxy_profile, please contact us or try again')

    sop.click_object(proxy_profile)
    time.sleep(2)

    driver.switch_to.window(new_handle)

    return driver

