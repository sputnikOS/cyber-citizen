# Import required modules
import pyautogui
import time
  
# FAILSAFE to FALSE feature is enabled by default 
# so that you can easily stop execution of 
# your pyautogui program by manually moving the 
# mouse to the upper left corner of the screen. 
# Once the mouse is in this location,
# pyautogui will throw an exception and exit.
pyautogui.FAILSAFE = False
  
# We want to run this code for infinite 
# time till we stop it so we use infinite loop now
while True:
    
    # time.sleep(t) is used to give a break of 
    # specified time t seconds so that its not 
    # too frequent
    time.sleep(15)
  
    # This for loop is used to move the mouse 
    # pointer to 500 pixels in this case(5*100)
    for i in range(0, 100):
        pyautogui.moveTo(0, i * 5)
          
    # This for loop is used to press keyboard keys,
    # in this case the harmless key shift key is 
    # used. You can change it according to your 
    # requirement. This works with all keys.
    for i in range(0, 3):
        pyautogui.press('shift')