from tkinter import *
import subprocess
import shutil
import os
import sys
from tkinter import messagebox
from PIL import Image, ImageTk

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
background_image = Image.open(cwd + "\\images\\menu2.png")
 
# Resize the image using resize() method
background_image = background_image.resize((screen_width, screen_height))
 
background_image = ImageTk.PhotoImage(master=root,image=background_image)


# Create a label to display the background image
background_label = Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

class variables():
    def __init__(self):
        self.background_label = False
        
Variables = variables()

def choose_jigsaw_image():
    # Path to the images folder
    images_folder = "images"
    
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
    listbox.pack(padx=10, pady=10)

    # Populate the listbox with image file names
    for image_file in image_files:
        listbox.insert(END, image_file)

    def on_select():
        # Get the selected image file
        selected_index = listbox.curselection()
        if selected_index:
            selected_image = image_files[selected_index[0]]

            # Copy the selected image to replace the existing one used in jigsaw.py
            selected_image_path = os.path.join(images_folder, selected_image)
            shutil.copy(selected_image_path, "images\\large.png")

            # Close the selection window
            selection_window.destroy()
            subprocess.run(["python", "src\\jigsaw.py"])

    # Create a button to confirm the selection
    confirm_button = Button(selection_window, text="Select", command=on_select, padx=10, pady=5)
    confirm_button.pack(pady=10)

def run_quiz():
    subprocess.run(["python", cwd + "\\src\\main.py"])

def exit_program():
    root.destroy()

def leaderboard():
    Variables.background_label = True
    # Read the Image
    background_image = Image.open(cwd + "\\images\\menu3.png")
    
    # Resize the image using resize() method
    background_image = background_image.resize((screen_width, screen_height))
    
    background_image = ImageTk.PhotoImage(master=root,image=background_image)
    
    background_label.configure(image=background_image)
    background_label.image = background_image
    
    
def runButton(event):
    x = event.x
    y = event.y
    if(not(Variables.background_label)):
        if(screen_width//12 < x and x < screen_width // 2):
            if(screen_height//3 < y and y < screen_height//2):
                run_quiz()
                
            if(int(screen_height * (2/3)) < y and y < int(screen_height * (5/6))):
                leaderboard()
                
        elif(screen_width//2 < x and x < screen_width * 11//12):
            if(screen_height//3 < y and y < screen_height//2):
                choose_jigsaw_image()
                
            if(int(screen_height * (2/3)) < y and y < int(screen_height * (5/6))):
                exit_program()
                
                #fix ratios
    elif(Variables.background_label):
        if(int(screen_height * (14/27)) < y and y < int(screen_height * (13/18))):
            if(int(screen_width* (9/160)) < x and x < int(screen_width * (15/32))):
                print('quiz')
                
            if(int(screen_width* (9/160)) < x and x < int(screen_width * (5/6))):
                print('Jigsaw')
                
        elif(int(screen_height * (2/3)) < y and y < int(screen_height * (5/6))):
            print('back')
            
# Set the size of the menu window to the size of the screen
root.geometry(f"{screen_width}x{screen_height}")
root.attributes('-fullscreen',True)

root.bind("<Button-1>",runButton)

# Run the main loop
root.mainloop()
