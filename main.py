import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

# store characters in a dictionary
characters = {}

# colors and theme
BG = "#2e1e42"         # deep violet
FG = "#f8f0ff"         # soft white
BTN = "#8f6bbf"        # lavender
ACCENT = "#ffb6d9"     # dreamy pink
FONT = ("Helvetica", 11)

# resize image for preview
def resize_image(path, size=(100, 100)):
    try:
        img = Image.open(path)
        img.thumbnail(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# character logic
def add_character():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Missing Name", "Please enter a character name.")
        return

    if name in characters:
        messagebox.showerror("Duplicate", f"Character '{name}' already exists.")
        return

    image_path = image_path_var.get()
    img_preview = resize_image(image_path) if image_path else None

    characters[name] = {
        "name": name,
        "image_path": image_path,
        "thumbnail": img_preview,
    }

    update_character_list()
    name_entry.delete(0, tk.END)
    image_path_var.set("")
    image_preview_label.config(image="")
    image_preview_label.image = None

# upload image
def browse_image():
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
    )
    if file_path:
        image_path_var.set(file_path)
        img = resize_image(file_path)
        if img:
            image_preview_label.config(image=img)
            image_preview_label.image = img

# update character display list
def update_character_list():
    listbox.delete(0, tk.END)
    for char in characters:
        listbox.insert(tk.END, char)

# main window
root = tk.Tk()
root.title("Synapse in the Void — Character Creator")
root.configure(bg=BG)
root.state('zoomed')  # Windows only — maximizes window

# ttk theme customization
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background=BG)
style.configure("TLabel", background=BG, foreground=FG, font=FONT)
style.configure("TButton", background=BTN, foreground=FG, font=FONT, padding=6)
style.map("TButton",
          background=[('active', ACCENT)],
          foreground=[('active', "#000")])

# layout frame
frame = ttk.Frame(root, padding=20, style="TFrame")
frame.pack()

# character name
ttk.Label(frame, text="Character Name:").grid(row=0, column=0, sticky="e")
name_entry = ttk.Entry(frame, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

# image input
ttk.Label(frame, text="Character Image:").grid(row=1, column=0, sticky="e")
image_path_var = tk.StringVar()
image_entry = ttk.Entry(frame, textvariable=image_path_var, width=30)
image_entry.grid(row=1, column=1, padx=5, pady=5)
browse_btn = ttk.Button(frame, text="Browse", command=browse_image)
browse_btn.grid(row=1, column=2, padx=5)

# preview image
image_preview_label = tk.Label(frame, bg=BG)
image_preview_label.grid(row=2, column=1, pady=10)

# add character button
add_btn = ttk.Button(frame, text="Add Character", command=add_character)
add_btn.grid(row=3, column=1, pady=10)

# character list
ttk.Label(frame, text="Characters:").grid(row=4, column=0, sticky="ne", pady=(10, 0))
listbox = tk.Listbox(frame, width=30, height=8, bg=BTN, fg=FG, font=("Helvetica", 10))
listbox.grid(row=4, column=1, pady=(10, 0))

root.mainloop()
