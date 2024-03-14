import pickle
import time
from tkinter import *
import subprocess
import shutil
import os
import sys
from tkinter import messagebox
from PIL import Image, ImageTk
from threading import Thread

cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')
import constants

# Create the main window
root = Tk()
root.title("Menu")

# Get the screen width and height
screen_width = constants.screenSize[0]
screen_height = constants.screenSize[1]

# Read the Image
background_image = Image.open(cwd + "\\images\\menu8.png")

# Resize the image using resize() method
background_image = background_image.resize((screen_width, screen_height))

background_image = ImageTk.PhotoImage(master=root,image=background_image)


# Create a label to display the background image
backgroundlabel = Label(root, image=background_image)
backgroundlabel.place(relwidth=1, relheight=1)

iList = []
tList = []
pList = []

class variables():
    def __init__(self):
        self.background_label = 1
        self.activated = list((0,1))
        self.past = ''

Variables = variables()

def choose_jigsaw_image():
    # Path to the images folder
    images_folder = cwd + "\\jigmg"

    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not image_files:
        messagebox.showinfo("No Images", "No images found in the 'images' folder.")
        return

    # Create a new window for selecting the image
    selection_window = Toplevel(root)
    selection_window.title("Choose Jigsaw Image")

    # Create a listbox to display the images
    listbox = Listbox(selection_window, selectmode=SINGLE)
    listbox.pack(padx=0, pady=0)
    listbox.configure(background="#b80020", foreground="#FFFFFF", font=('Aerial 13', screen_width//64),width=screen_width//32)
    
    # Populate the listbox with image file names
    for image_file in image_files:
        listbox.insert(END, image_file)

    def on_select():
        # Get the selected image file
        selected_index = listbox.curselection()
        Variables.activated[1] = 1
        if selected_index:
            selected_image = image_files[selected_index[0]]

            # Copy the selected image to replace the existing one used in jigsaw.py
            selected_image_path = os.path.join(images_folder, selected_image)
            shutil.copy(selected_image_path, cwd + "\\images\\large.png")

            # Close the selection window
            selection_window.destroy()
            subprocess.run(["python", cwd + "\\src\\jigsaw.py"])

    # Create a button to confirm the selection
    confirm_button = Button(selection_window, text="Select", command=on_select, padx=10, pady=5)
    confirm_button.pack(pady=10)

def run_quiz():
    subprocess.run(["python", cwd + "\\src\\main.py"])

def exit_program():
    root.destroy()

#leaderboard
def switchLeaderboard():
    if(Variables.background_label == 1):
        Variables.background_label = 2
        # Read the Image
        background_image = Image.open(cwd + "\\images\\menu3.png")

        # Resize the image using resize() method
        background_image = background_image.resize((screen_width, screen_height))

        background_image = ImageTk.PhotoImage(master=root,image=background_image)

        backgroundlabel.configure(image=background_image)
        backgroundlabel.image = background_image
        backgroundlabel.update()
        for i in range(len(tList)):
            if(i < 5):
                tList[i].place(x=screen_width * 1//6,y=screen_height//8.08181818182*(i+3) - 30)
                iList[i].place(x=screen_width * 13/48,y=screen_height//8.08181818182*(i+3) - 30)
                pList[i].place(x=screen_width * 139/384,y=screen_height//8.08181818182*(i+3) - 30)
            else:
                tList[i].place(x=screen_width * 40//64,y=screen_height//8.08181818182*(i+3-5) - 30)
                iList[i].place(x=screen_width * 93/128,y=screen_height//8.08181818182*(i+3-5) - 30)
                pList[i].place(x=screen_width * 157/192,y=screen_height//8.08181818182*(i+3-5) - 30)
        
    elif(Variables.background_label == 2):
        Variables.background_label = 1
        if(Variables.activated[0] == 1 and Variables.activated[1] == 1):
            background_image = Image.open(cwd + "\\images\\menu7.png")

            # Resize the image using resize() method
            background_image = background_image.resize((screen_width, screen_height))

            background_image = ImageTk.PhotoImage(master=root,image=background_image)

            backgroundlabel.configure(image=background_image)
            backgroundlabel.image = background_image
        elif(Variables.activated[0] == 1):
            Variables.background_label = 1
            backgroundimage = Image.open(cwd + "\\images\\menu9.png")

            # Resize the image using resize() method
            background_image = background_image.resize((screen_width, screen_height))

            background_image = ImageTk.PhotoImage(master=root,image=background_image)

            backgroundlabel.configure(image=background_image)
            backgroundlabel.image = background_image
        elif(Variables.activated[1] == 1):
            Variables.background_label = 1
            background_image = Image.open(cwd + "\\images\\menu8.png")

            # Resize the image using resize() method
            background_image = background_image.resize((screen_width, screen_height))

            background_image = ImageTk.PhotoImage(master=root,image=background_image)

            backgroundlabel.configure(image=background_image)
            backgroundlabel.image = background_image
            backgroundlabel.update()
        else:
            background_image = Image.open(cwd + "\\images\\menu8.png")

            # Resize the image using resize() method
            background_image = background_image.resize((screen_width, screen_height))

            background_image = ImageTk.PhotoImage(master=root,image=background_image)

            backgroundlabel.configure(image=background_image)
            backgroundlabel.image = background_image
            backgroundlabel.update()
        for i in range(len(tList)):
            tList[i].place_forget()
            pList[i].place_forget()
            iList[i].place_forget()
    
def runButton(event):
    try:
        for i in range(10):
            tList[i].place_forget()
            pList[i].place_forget()
            iList[i].place_forget()
    except:
        print('first Go')
    tList.clear()
    pList.clear()
    iList.clear()
    with open(cwd + "\\dat\\topTen.pkl", 'rb') as f:
        z = pickle.load(f)
        for i in range(10):
            i += 1
            iz = ('initial' + str(i))
            pz = ('points' + str(i))
            tz = ('team' + str(i))
            iList.append(Label(root, text=(z[iz]), font=("Arial", 20), background='#b80020', foreground=('#FFFFFF')))
            tList.append(Label(root, text=(z[tz]), font=("Arial", 20), background='#b80020', foreground=('#FFFFFF')))
            pList.append(Label(root, text=(z[pz]), font=("Arial", 20), background='#b80020', foreground=('#FFFFFF')))
    x = event.x
    y = event.y
    print(x,y)
    #menu page 1
    if(Variables.activated[0] == 1 and Variables.activated[1] == 1):
        background_image = Image.open(cwd + "\\images\\menu7.png")

        # Resize the image using resize() method
        background_image = background_image.resize((screen_width, screen_height))

        background_image = ImageTk.PhotoImage(master=root,image=background_image)

        backgroundlabel.configure(image=background_image)
        backgroundlabel.image = background_image
    elif(Variables.activated[0] == 1):
        background_image = Image.open(cwd + "\\images\\menu9.png")

        # Resize the image using resize() method
        background_image = background_image.resize((screen_width, screen_height))

        background_image = ImageTk.PhotoImage(master=root,image=background_image)

        backgroundlabel.configure(image=background_image)
        backgroundlabel.image = background_image
    elif(Variables.activated[1] == 1):
        background_image = Image.open(cwd + "\\images\\menu8.png")

        # Resize the image using resize() method
        background_image = background_image.resize((screen_width, screen_height))

        background_image = ImageTk.PhotoImage(master=root,image=background_image)

        backgroundlabel.configure(image=background_image)
        backgroundlabel.image = background_image
        backgroundlabel.update()
    if(Variables.background_label == 1):
        if(int(screen_height * (4/9)) > y and y > int(screen_height * (3/9))):
            if(int(screen_width* (27/32)) > x and x > int(screen_width * (22/32)) and Variables.activated[0] == 0):
                Variables.activated[0] = 1
                Variables.activated[1] = 0
                run_quiz()

            if(int(screen_width* (10/32)) > x and x > int(screen_width * (5/32))and Variables.activated[1] == 0):
                choose_jigsaw_image()
                
            if(int(screen_width* (18/32)) > x and x > int(screen_width * (15/32))):
                switchLeaderboard()
                
        elif(int(screen_height * (7/9)) < y and y < int(screen_height * (31/32))):
            if(int(screen_width* (1/32)) < x and x < int(screen_width * (7/32))):
                exit_program()

    #menu page 2 (leaderboard menu)
    elif(Variables.background_label == 2):
        if(int(screen_height * (13/72)) < y and y < int(screen_height * (5/18))):
            if(int(screen_width* (25/32)) < x and x < int(screen_width * (15/16))):
                switchLeaderboard()
def resetLeader(event):
    cwd = os.getcwd()
    cwd = str(cwd)
    cwd = cwd.replace('src','')
    sys.path.append(cwd + '\\dat')

    #sets all to blank
    b = {
    "initial1": 'blank1',
    "team1": 'blank',
    "points1": 10,
    "initial2": 'blank2',
    "team2": 'blank',
    "points2": 9,
    "initial3": 'blank3',
    "team3": 'blank',
    "points3": 8,
    "initial4": 'blank4',
    "team4": 'blank',
    "points4": 7,
    "initial5": 'blank5',
    "team5": 'blank',
    "points5": 6,
    "initial6": 'blank6',
    "team6": 'blank',
    "points6": 5,
    "initial7": 'blank7',
    "team7": 'blank',
    "points7": 4,
    "initial8": 'blank8',
    "team8": 'blank',
    "points8": 3,
    "initial9": 'blank9',
    "team9": 'blank',
    "points9": 2,
    "initial10": 'blank10',
    "team10": 'blank',
    "points10": 1
    }
    with open(cwd + "\\dat\\topTen.pkl", "wb") as f:
        pickle.dump(b, f)
def change():
    if(Variables.background_label == 1):
        if(Variables.activated[0] == 1 and Variables.activated[1] == 1):
            background_image = Image.open(cwd + "\\images\\menu7.png")

            # Resize the image using resize() method
            background_image = background_image.resize((screen_width, screen_height))

            background_image = ImageTk.PhotoImage(master=root,image=background_image)

            backgroundlabel.configure(image=background_image)
            backgroundlabel.image = background_image
        elif(Variables.activated[0] == 1):
            background_image = Image.open(cwd + "\\images\\menu9.png")

            # Resize the image using resize() method
            background_image = background_image.resize((screen_width, screen_height))

            background_image = ImageTk.PhotoImage(master=root,image=background_image)

            backgroundlabel.configure(image=background_image)
            backgroundlabel.image = background_image
        elif(Variables.activated[1] == 1):
            background_image = Image.open(cwd + "\\images\\menu8.png")

            # Resize the image using resize() method
            background_image = background_image.resize((screen_width, screen_height))

            background_image = ImageTk.PhotoImage(master=root,image=background_image)

            backgroundlabel.configure(image=background_image)
            backgroundlabel.image = background_image
            backgroundlabel.update()
    elif(Variables.background_label == 2):
        Variables.background_label = 2
        # Read the Image
        background_image = Image.open(cwd + "\\images\\menu3.png")

        # Resize the image using resize() method
        background_image = background_image.resize((screen_width, screen_height))

        background_image = ImageTk.PhotoImage(master=root,image=background_image)

        backgroundlabel.configure(image=background_image)
        backgroundlabel.image = background_image
        backgroundlabel.update()
        for i in range(len(tList)):
            if(i < 5):
                tList[i].place(x=screen_width * 1//6,y=screen_height//8.08181818182*(i+3) - 30)
                iList[i].place(x=screen_width * 13/48,y=screen_height//8.08181818182*(i+3) - 30)
                pList[i].place(x=screen_width * 139/384,y=screen_height//8.08181818182*(i+3) - 30)
            else:
                tList[i].place(x=screen_width * 40//64,y=screen_height//8.08181818182*(i+3-5) - 30)
                iList[i].place(x=screen_width * 93/128,y=screen_height//8.08181818182*(i+3-5) - 30)
                pList[i].place(x=screen_width * 157/192,y=screen_height//8.08181818182*(i+3-5) - 30)
    root.after(200, change)
            
# Set the size of the menu window to the size of the screen
root.geometry(f"{screen_width}x{screen_height}")
root.attributes('-fullscreen',True)

root.bind("<Control-Insert>", resetLeader)
root.bind("<Button-1>",runButton)
root.after(500, change)
# Run the main loop
root.mainloop()