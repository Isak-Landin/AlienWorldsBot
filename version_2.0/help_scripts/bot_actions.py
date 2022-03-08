import pyautogui
import cv2
from selenium import webdriver
import traceback
import time


class VisualActions:

    @staticmethod
    def find_image(image, region, confidence):
        region_return = None
        try:
            region_return = pyautogui.locateOnScreen(image,
                                                     region=region,
                                                     confidence=confidence
                                                     )
        except:
            print(traceback.print_exc())
        finally:
            return region_return

    @staticmethod
    def find_images(image, region, confidence):
        region_list_return = None
        try:
            region_list_return = pyautogui.locateAllOnScreen(image,
                                                             region=region,
                                                             confidence=confidence
                                                             )
        except:
            print(traceback.print_exc())
        finally:
            return region_list_return

    @staticmethod
    def move_to_click(coordinates, duration, click=True):
        pyautogui.moveTo(coordinates, duration=duration)
        time.sleep(0.2)
        if click is True:
            pyautogui.click()

    @staticmethod
    def get_center(region, offset_y=None, offset_x=None):
        print(region)
        center = None
        try:
            if offset_y is not None and offset_x is not None:
                center = pyautogui.center(region)
                center = (center[0] + offset_x, center[1] + offset_y)

            else:
                center = pyautogui.center(region)
        except:
            print(traceback.print_exc())
        finally:
            return center


class BotIntervention:
    def __init__(self):
        self.placeholder = None

    @staticmethod
    def farm_flowers(region, confidence):
        all_flower_region_list = []
        try:
            all_flowers_images = ['daisy.png',
                                  'sunflower.png',
                                  'gerbera.png',
                                  'artichoke.png']

            for image in all_flower_region_list:
                all_flowers_for_type = VisualActions.find_images(image,
                                                                 region=region,
                                                                 confidence=confidence
                                                                 )
                for flower_region in all_flowers_for_type:
                    all_flower_region_list.append(flower_region)

        except:
            print(traceback.print_exc())
        finally:
            return all_flower_region_list

    @staticmethod
    def all_items_in_inventory():
        pass

    @staticmethod
    def switch_pages():
        pass

