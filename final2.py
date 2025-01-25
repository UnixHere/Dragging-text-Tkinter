import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageFont, ImageDraw, ImageTk
import ast
import logging

logging.basicConfig(level=logging.INFO)

class ImageTextApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Image Text Generator')
        self.root.geometry('350x200')
        
        # Variables
        self.seat_var = tk.StringVar(value="Seat")
        self.name_var = tk.StringVar(value="Name")
        self.save_var = tk.StringVar(value="output.jpg")
        self.chosen_img_var = tk.StringVar(value='Selected: None')
        self.chosen_preset_var = tk.StringVar(value='Selected: None')
        self.chosen_db_var = tk.StringVar(value='Selected: None')
        self.path = ''
        
        self.create_ui()

    def create_ui(self):
        # Seat Label and Entry
        tk.Label(self.root, text='Enter Seat:').grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.seat_var).grid(row=0, column=1)
        
        # Name Label and Entry
        tk.Label(self.root, text='Enter Name:').grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.name_var).grid(row=1, column=1)
        
        # Image Selection
        tk.Button(self.root, text='Select Image', 
                  command=lambda: self.open_file('Image')).grid(row=2, column=0)
        tk.Label(self.root, textvariable=self.chosen_img_var).grid(row=2, column=1)
        
        # Edit and Create Buttons
        tk.Button(self.root, text='Open Editor', 
                  command=self.open_image_editor).grid(row=3, column=0)
        tk.Button(self.root, text='Open Creator', 
                  command=self.open_image_creator).grid(row=3, column=1)

    def open_file(self, file_type):
        try:
            filetypes = {
                'Image': [("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")],
                'DataBase': [("Text Files", "*.txt")],
                'Preset': [("Text Files", "*.txt")]
            }
            
            filename = filedialog.askopenfilename(filetypes=filetypes[file_type])
            
            if not filename:
                return None
            
            if file_type == 'Image':
                self.path = filename
                self.chosen_img_var.set(f'Selected: {os.path.basename(filename)}')
            
            return filename
        except Exception as e:
            logging.error(f"Error opening file: {e}")
            return None

    def open_image_editor(self):
        if not self.path:
            logging.warning("No image selected!")
            return
        
        ImageEditor(self.path, self.seat_var, self.name_var, self.save_var)

    def open_image_creator(self):
        if not self.path:
            logging.warning("No image selected!")
            return
        
        ImageCreator(self.path, 
                     self.chosen_preset_var, 
                     self.chosen_db_var)

    def run(self):
        self.root.mainloop()

class ImageEditor:
    def __init__(self, image_path, seat_var, name_var, save_var):
        self.img_window = tk.Toplevel()
        self.img_window.title("Image Editor")
        self.img_window.grab_set()
        
        self.photo = Image.open(image_path)
        self.wi, self.hi = self.photo.size
        self.fonty = ImageFont.truetype('arial.ttf', 18)
        
        self.seat_var = seat_var
        self.name_var = name_var
        self.save_var = save_var
        
        self.seat_pos = [50, 50]
        self.name_pos = [50, 100]
        
        self.setup_ui()

    def setup_ui(self):
        # Position labels
        self.lbl_pos_seat = tk.Label(self.img_window, 
                                     text="Seat Position: x=0 y=0")
        self.lbl_pos_seat.pack()
        self.lbl_pos_name = tk.Label(self.img_window, 
                                     text="Name Position: x=0 y=0")
        self.lbl_pos_name.pack()
        
        # Canvas
        self.canvas = tk.Canvas(self.img_window, 
                                height=self.hi, width=self.wi)
        self.canvas.pack()
        
        self.can_photo = ImageTk.PhotoImage(self.photo)
        self.img_item = self.canvas.create_image(
            self.wi/2, self.hi/2, image=self.can_photo, anchor='center'
        )
        
        # Bind mouse events
        self.img_window.bind('<B1-Motion>', self.move_seat)
        self.img_window.bind('<B3-Motion>', self.move_name)
        
        # Text variable trace
        self.seat_var.trace_add('write', self.update_text)
        self.name_var.trace_add('write', self.update_text)
        
        # Save widgets
        self.save_entry = tk.Entry(self.img_window, textvariable=self.save_var)
        self.save_entry.pack()
        tk.Button(self.img_window, text='Save Image', 
                  command=self.save_image).pack()

    def move_seat(self, event):
        self.seat_pos[0], self.seat_pos[1] = event.x, event.y
        self.lbl_pos_seat.config(
            text=f"Seat Position: x={self.seat_pos[0]} y={self.seat_pos[1]}"
        )
        self.update_image()

    def move_name(self, event):
        self.name_pos[0], self.name_pos[1] = event.x, event.y
        self.lbl_pos_name.config(
            text=f"Name Position: x={self.name_pos[0]} y={self.name_pos[1]}"
        )
        self.update_image()

    def update_text(self, *args):
        self.update_image()

    def update_image(self):
        updated_photo = self.photo.copy()
        updated_draw = ImageDraw.Draw(updated_photo)
        
        updated_draw.text(self.seat_pos, 
                          text=self.seat_var.get(), 
                          fill='red', font=self.fonty)
        updated_draw.text(self.name_pos, 
                          text=self.name_var.get(), 
                          fill='blue', font=self.fonty)
        try:
            self.can_photo = ImageTk.PhotoImage(updated_photo)
            self.canvas.itemconfig(self.img_item, image=self.can_photo)
        except Exception as e:
            logging.error(f"Error reading preset: {e}") #something happens when you remove this error handling on line 169 dont remove this error handling
            

    def save_image(self):
        final_image = self.photo.copy()
        final_draw = ImageDraw.Draw(final_image)
        
        final_draw.text(self.seat_pos, 
                        text=self.seat_var.get(), 
                        fill='red', font=self.fonty)
        final_draw.text(self.name_pos, 
                        text=self.name_var.get(), 
                        fill='blue', font=self.fonty)
        
        filename = self.save_var.get()
        final_image.save(filename)
        
        # Save positions
        with open(f"{filename}_positions.txt", "w") as f:
            f.write(f"{self.seat_pos}\n{self.name_pos}")
        
        logging.info(f"Image saved as {filename}")

class ImageCreator:
    def __init__(self, image_path, chosen_preset_var, chosen_db_var):
        self.img_window = tk.Toplevel()
        self.img_window.title("Image Creator")
        self.img_window.grab_set()
        
        self.photo = Image.open(image_path)
        self.wi, self.hi = self.photo.size
        self.fonty = ImageFont.truetype('arial.ttf', 18)
        
        self.chosen_preset_var = chosen_preset_var
        self.chosen_db_var = chosen_db_var
        
        self.setup_ui()

    def setup_ui(self):
        # Preset and Database selection
        preset_btn = tk.Button(self.img_window, text='Select Preset', 
                  command=self.select_preset)
        preset_btn.grid(row=0, column=0)
        
        # Preset label
        preset_label = tk.Label(self.img_window, 
                                textvariable=self.chosen_preset_var)
        preset_label.grid(row=0, column=1)
        
        # Database button and label
        db_btn = tk.Button(self.img_window, text='Select Database', 
                  command=self.select_database)
        db_btn.grid(row=1, column=0)
        
        db_label = tk.Label(self.img_window, 
                            textvariable=self.chosen_db_var)
        db_label.grid(row=1, column=1)
        
        # Position labels
        self.lbl_pos_seat = tk.Label(self.img_window, 
                                     text="Seat Position: x=0 y=0")
        self.lbl_pos_seat.grid(row=2, column=0, columnspan=2)
        
        self.lbl_pos_name = tk.Label(self.img_window, 
                                     text="Name Position: x=0 y=0")
        self.lbl_pos_name.grid(row=3, column=0, columnspan=2)
        
        # Canvas
        self.canvas = tk.Canvas(self.img_window, height=self.hi, width=self.wi)
        self.canvas.grid(row=4, column=0, columnspan=2)
        
        self.can_photo = ImageTk.PhotoImage(self.photo)
        self.canvas.create_image(self.wi/2, self.hi/2, 
                                 image=self.can_photo, anchor='center')

    def select_preset(self):
        preset_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if preset_path:
            try:
                with open(preset_path, "r") as f:
                    positions = f.read().splitlines()
                    pos_list = [ast.literal_eval(pos) for pos in positions]
                    
                    self.lbl_pos_seat.config(
                        text=f"Seat Position: x={pos_list[0][0]} y={pos_list[0][1]}"
                    )
                    self.lbl_pos_name.config(
                        text=f"Name Position: x={pos_list[1][0]} y={pos_list[1][1]}"
                    )
                    self.preset_positions = pos_list
                    
                    # Update the preset file label
                    self.chosen_preset_var.set(f'Selected: {os.path.basename(preset_path)}')
            except Exception as e:
                logging.error(f"Error reading preset: {e}")

    def select_database(self):
        db_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if db_path:
            try:
                with open(db_path, "r") as f:
                    data = [line.strip().split(",") for line in f]
                    
                    # Update the database file label
                    self.chosen_db_var.set(f'Selected: {os.path.basename(db_path)}')
                    
                    self.create_images(data)
            except Exception as e:
                logging.error(f"Error reading database: {e}")

    def create_images(self, data):
        try:
            for name, seat in data:
                final_image = self.photo.copy()
                final_draw = ImageDraw.Draw(final_image)
                
                final_draw.text(self.preset_positions[0], 
                                text=seat, fill='red', font=self.fonty)
                final_draw.text(self.preset_positions[1], 
                                text=name, fill='blue', font=self.fonty)
                
                final_image.save(f'{name}_{seat}.jpg')
            
            logging.info(f"Created {len(data)} images")
        except Exception as e:
            logging.error(f"Error creating images: {e}")

def main():
    app = ImageTextApp()
    app.run()

if __name__ == "__main__":
    main()
