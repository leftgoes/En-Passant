import cv2
import numpy as np
import pyautogui
import time


class GIF:
    __slots__ = ('folder', 'region')

    def __init__(self, folder: str, region: tuple[int, int, int, int] = (460, 60, 975, 975)):
        self.folder = folder
        self.region = region

    def test(self):
        cv2.imshow('chess', cv2.cvtColor(np.array(pyautogui.screenshot(region=self.region)), cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)

    def get(self, n: int = 60, delay: float = 2):
        time.sleep(delay)
        print('starting capture')
        for i in range(n):
            s = cv2.cvtColor(np.array(pyautogui.screenshot(region=self.region)), cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'{self.folder}\\frm{n - i - 1}.png', s)
        print('end capture')


if __name__ == '__main__':
    gif = GIF(FOLDER)
    gif.get()
