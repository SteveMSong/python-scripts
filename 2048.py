'''
2048 is a simple game where you combine tiles by sliding them up, down, left, or
right with the arrow keys. You can actually get a farily high score by repeatedly
sliding in an up, right, down, and left pattern over and over again. Write a
program that will open the game at https://gabrielecirulli.github.io/2048/and
keep sending up, right, down, and left keystrokes to automatically play the
game.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('https://gabrielecirulli.github.io/2048/')
elem = browser.find_element_by_css_selector('.restart-button')
elem.click()
elem = browser.find_element_by_css_selector('html')

for i in range(0, 200):
        elem.send_keys(Keys.UP)
        elem.send_keys(Keys.RIGHT)
        elem.send_keys(Keys.DOWN)
        elem.send_keys(Keys.LEFT)
            
print('The game is over!')
browser.quit()
