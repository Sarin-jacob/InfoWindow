#!/usr/bin/env python3
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Import the new V2 driver
try:
    from driver import epd7in5b_V2
except ImportError as e:
    print(f"Import Error: {e}")
    print("Ensure 'epd7in5b_V2.py' AND 'epdconfig.py' are in the 'driver' folder.")
    exit()

def test_v2_display():
    print("\n--- Testing V2 E-Ink Display (800x480) ---")
    
    epd = epd7in5b_V2.EPD()
    print("Initializing...")
    epd.init()

    print("Clearing screen (this takes a moment)...")
    epd.Clear()

    print("Creating Black and Red image layers...")
    # The V2 driver requires TWO separate 1-bit images.
    # 255 is White (Background), 0 is Ink (Foreground)
    image_black = Image.new('1', (epd.width, epd.height), 255)
    image_red = Image.new('1', (epd.width, epd.height), 255)

    draw_black = ImageDraw.Draw(image_black)
    draw_red = ImageDraw.Draw(image_red)

    # Load fonts
    try:
        font_large = ImageFont.truetype("fonts/roboto/Roboto-Black.ttf", 60)
        font_small = ImageFont.truetype("fonts/roboto/Roboto-Regular.ttf", 32)
    except Exception:
        print("Could not load Roboto font, using default.")
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw on the BLACK layer
    draw_black.text((40, 40), "WAVESHARE V2 DRIVER TEST", font=font_large, fill=0)
    draw_black.text((40, 380), "If you can read this, the BLACK channel works!", font=font_small, fill=0)

    # Draw on the RED layer
    current_time = datetime.now().strftime("%I:%M %p IST") 
    draw_red.text((40, 160), "THIS TEXT SHOULD BE RED", font=font_large, fill=0)
    draw_red.text((40, 260), f"Test Run Time: {current_time}", font=font_small, fill=0)

    print("Generating memory buffers...")
    buf_black = epd.getbuffer(image_black)
    buf_red = epd.getbuffer(image_red)

    print("Pushing data to display (Wait 15-20 seconds for refresh)...")
    epd.display(buf_black, buf_red)

    print("Putting display to sleep...")
    epd.sleep()
    
    print("\n[SUCCESS] Test script finished. Check the physical screen!")

if __name__ == '__main__':
    test_v2_display()