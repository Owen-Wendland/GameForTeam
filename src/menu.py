import tkinter as tk
from tkinter import Label, filedialog, messagebox
import subprocess
import shutil
import os
import sys
cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')
import constants

def choose_jigsaw_image():
    # Path to the images folder
    images_folder = "images"
    
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not image_files:
        messagebox.showinfo("No Images", "No images found in the 'images' folder.")
        return

    # Create a new window for selecting the image
    selection_window = tk.Toplevel(root)
    selection_window.title("Choose Jigsaw Image")

    # Create a listbox to display the images
    listbox = tk.Listbox(selection_window, selectmode=tk.SINGLE)
    listbox.pack(padx=10, pady=10)

    # Populate the listbox with image file names
    for image_file in image_files:
        listbox.insert(tk.END, image_file)

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
    confirm_button = tk.Button(selection_window, text="Select", command=on_select, padx=10, pady=5)
    confirm_button.pack(pady=10)

# ... (rest of the code remains unchanged)
def run_quiz():
    subprocess.run(["python", cwd + "\\src\\main.py"])

def exit_program():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Menu")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

bgimg = cwd + "\\images\\backMenu.png"
bgimg= tk.PhotoImage(master=root,file = bgimg, width= screen_width, height= screen_height)
bgimg.width = screen_width
bgimg.height = screen_height
label1 = Label(root, image = bgimg) 
label1.place(x = 0, y = 0) 

# Set the size of the menu window to the size of the screen
root.geometry(f"{screen_width}x{screen_height}")
root.attributes('-fullscreen',True)

# Configure button styles
qbutton_style = {'padx': screen_width//10, 'pady': screen_height//12}
jbutton_style = {'padx': screen_width//10, 'pady': screen_height//12}
ebutton_style = {'padx': screen_width//10, 'pady': screen_height//12}

# Add buttons to the window with the configured style
quiz_button = tk.Button(root, text="Quiz", command=run_quiz, **qbutton_style)
quiz_button.place(x=screen_width//4 - screen_width//10,y=screen_width//3)

jigsaw_button = tk.Button(root, text="Jigsaw", command=choose_jigsaw_image, **jbutton_style)
jigsaw_button.place(x=screen_width//4*3 - screen_width//10,y=screen_width//3)

exit_button = tk.Button(root, text="Exit", command=exit_program, **ebutton_style)
exit_button.place(x=10, y=10)

# Run the main loop
root.mainloop()
