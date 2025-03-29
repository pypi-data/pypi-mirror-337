#!/usr/bin/env python3
"""
later work- DISPLAY all dissapeared pdf s from lundl and (still existing) tunl
"""
#
#  created by GPT
#
#
import cv2
import numpy as np
import pdf2image
import os
import fire
import importlib_resources
from glob import glob
import select,os,sys
import tty, termios
import threading

"""
View ISOBAR situation, also 9t4 12t6
"""

GW = 800
GH = 600

GW = 1024
GH = 768

# Initialize global variables for user input and the running state
user_input = ""
running = True



def load_img( file_path ):
    global GW,GH
    images = pdf2image.convert_from_path(file_path)
    #for i in range(len(images)):
    img = np.array(images[0])

    # here I crop it
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    x, y, w, h = cv2.boundingRect(binary)
    #print("D... ",x,y,w,h)
    crop = img[max(0, y-10):y+h+10, max(0, x-10):x+w+10]
    max_size = (1280, 960)
    max_size = (GW, GH)
    crop = cv2.resize(crop, max_size, interpolation = cv2.INTER_AREA)
    return crop


def get_finum():
    # continue
    global user_input

    file_number = user_input
    lunds,tunl,tunlone  = False, False,False
    last_input = file_number
    file_path = ""

    if file_number == 'q':
        return ""
    if file_number == '.q':
        return ""
    if len(file_number) == 0:
        return ""

    if file_number.isdigit():
        lunds = True
    elif len(file_number) > 1 and file_number[-1] == "t":
        file_number = file_number[:-1]
        if file_number.isdigit():
            tunl = True

    elif file_number.find("t")>0:
        a,z = file_number.split("t")
        if a.isdigit() and z.isdigit():
            tunlone = True
    else:
        print("Invalid input. Please enter a number between 1 and 273, evetually 4t-20t or AtZ")
        lunds = False
        tunl = False
        tunlone = False

    #aaa = importlib_resources.files("nuphy2")
    #aab = importlib_resources.files("nuphy2").joinpath("data/")
    #aac = importlib_resources.files("nuphy2").joinpath("data/pdf_summary/")
    #print(aaa, aab, aac)

    # Here I get image from pdf ************************************************************
    if lunds:
        filename = f"pdf_summary/{file_number.zfill(3)}.pdf"
        file_path = importlib_resources.files("nuphy2").joinpath("data/"+filename)
    if tunl:
        filename = f"tunl/{file_number.zfill(2)}_is_*.pdf"
        file_path = importlib_resources.files("nuphy2").joinpath("data/"+filename)
        #print( file_path)
        #file_path = "/home/ojr/02_GIT/GITLAB/nuphy2/nuphy2/data/tunl/04_is_*.pdf"
        file_path = list(glob( str(file_path) ))
        if len(file_path)>0:
            file_path = file_path[0]
        else:
            print(" ... NO SUCH FILE")
            return ""

    if tunlone:
        a,z = file_number.split("t")
        filename = f"tunl/{a.zfill(2)}_{z.zfill(2)}_*.pdf"
        file_path = importlib_resources.files("nuphy2").joinpath("data/"+filename)
        #print( file_path)
        #file_path = "/home/ojr/02_GIT/GITLAB/nuphy2/nuphy2/data/tunl/04_is_*.pdf"
        file_path = list(glob( str(file_path) ))
        if len(file_path)>0:
            file_path = file_path[0]
        else:
            print(" ... NO SUCH FILE")
            return ""

    #print( file_path)
    return file_path




# Function to handle user input
def input_thread():
    global user_input, running
    while running:
        user_input = input("Enter text: ")
        if user_input == 'q':
            running = False
            break

# Function to display the green canvas and write user input
def display_green_canvas():
    global user_input, running ,GH, GW
    # Create a green canvas image
    green_canvas = np.zeros((GH, GW, 3), dtype=np.uint8)
    green_canvas[:] = (0, 55, 0)  # Set the color to green

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_color = (255, 255, 255)  # White color
    font_thickness = 2
    position = (50, 50)  # Position of the text

    while running:
        # Make a copy of the canvas to write new text without overlapping
        canvas_copy = green_canvas.copy()
        # Put the user input text onto the canvas copy

        fipath = get_finum()
        if os.path.exists( fipath ):
            canvas_copy = load_img( fipath )
        #cv2.putText(canvas_copy, f"{fipath}", position, font, font_scale, font_color, font_thickness)

        cv2.namedWindow("sch", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("sch", GW, GH)              # Resize

        cv2.imshow('sch', canvas_copy)
        if cv2.waitKey(500) & 0xFF == ord('q'):  # Refresh every second, exit on 'q'
            running = False

    cv2.destroyAllWindows()


def run_one():
    """
    Input mass number A and view a scheme (isobars/isotope), for TUNL input 4t-20t OR AtZ (12t6)
    """
    # Start the input thread
    threading.Thread(target=input_thread, daemon=True).start()
    # Start the display loop
    display_green_canvas()



if __name__ == "__main__":
    fire.Fire(run_one)
    #fire.Fire(display_pdf_as_image)
