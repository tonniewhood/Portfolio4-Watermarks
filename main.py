import os

import tkinter as tk

from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WaterMarker(tk.Tk):

    def __init__(self, root):

        # Create image canvas
        self.image_canvas = tk.Canvas(root, width=400, height=400, bg="gray", highlightthickness=1, highlightbackground="black")
        self.image_canvas.pack(anchor=tk.CENTER, padx=10, pady=10)

        # Create information Frame
        self.options_frame = tk.Frame(root, width=400, height=200)
        self.options_frame.pack(anchor=tk.CENTER, padx=10, pady=10)

        # Image selection label
        self.image_label = tk.Label(self.options_frame, text="Select Image: ")
        self.image_label.grid(row=0, column=0)

        # Image path entry
        self.image_entry = tk.Entry(self.options_frame)
        self.image_entry.grid(row=0, column=1, pady=10)

        # Image selection button
        self.image_button = tk.Button(self.options_frame, text="Browse", command=self.browse_for_image)
        self.image_button.grid(row=0, column=2, pady=10)


    def render_options(self):

        # Create watermark text label
        self.watermark_label = tk.Label(self.options_frame, text="Watermark: ")
        self.watermark_label.grid(row=1, column=0)

        # Create watermark text entry
        self.sv = tk.StringVar()
        self.sv.trace_add("write", self.show_watermark)
        self.watermark_entry = tk.Entry(self.options_frame, textvariable=self.sv)
        self.watermark_entry.grid(row=1, column=1, pady=10)
        self.img_watermark = self.image_canvas.create_text(200, 200, text="", font=("Arial", 15), fill="black", anchor=tk.CENTER)

        # Create button labels
        self.loc_label = tk.Label(self.options_frame, text="Location: ")
        self.loc_label.grid(row=3, column=0)

        # Create location radio buttons
        self.active_loc = tk.IntVar()
        self.loc_left = tk.Radiobutton(self.options_frame, text="Left", value=0, variable=self.active_loc, command=self.show_watermark)
        self.loc_left.grid(row=4, column=0)
        self.loc_center = tk.Radiobutton(self.options_frame, text="Center", value=1, variable=self.active_loc, command=self.show_watermark)
        self.loc_center.grid(row=4, column=1)
        self.loc_right = tk.Radiobutton(self.options_frame, text="Right", value=2, variable=self.active_loc, command=self.show_watermark)
        self.loc_right.grid(row=4, column=2)

        # Create save button
        self.save_button = tk.Button(self.options_frame, text="Save", command=self.save_image)
        self.save_button.grid(row=6, column=0)


    def browse_for_image(self):
        current_dir = os.path.dirname(__file__)
        filename = filedialog.askopenfilename(initialdir=current_dir, title="Select Image", filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png")))

        self.image = Image.open(filename)

        long_side = max(self.image.width, self.image.height)
        short_side = min(self.image.width, self.image.height)

        self.new_long_side = 400
        self.new_short_side = int(short_side * (400 / long_side))

        x = self.new_long_side if self.image.width > self.image.height else self.new_short_side
        y = self.new_long_side if self.image.width <= self.image.height else self.new_short_side

        self.image = self.image.resize((x, y))
        self.image_tk = ImageTk.PhotoImage(self.image)


        self.canvas_x = (400 - x) / 2
        self.canvas_y = (400 - y) / 2

        self.image_canvas.create_image(self.canvas_x, self.canvas_y, image=self.image_tk, anchor=tk.NW)

        self.image_entry.insert(0, filename)
        self.render_options()


    def show_watermark(self, *args):

        contents = self.sv.get()
        location = self.active_loc.get()

        location_anchor = tk.SW
        location_x = self.canvas_x + 5
        location_y = self.canvas_y + self.image.height - 5
        if location == 1:
            location_anchor = tk.S
            location_x = 200
        elif location == 2:
            location_anchor = tk.SE
            location_x = self.canvas_x + self.image.width - 5


        self.image_canvas.delete(self.img_watermark)
        self.img_watermark = self.image_canvas.create_text(location_x, location_y, text=contents, font=("Arial", 15), fill="black", anchor=location_anchor)


    def save_image(self):

        filename = filedialog.asksaveasfilename(initialdir=os.path.dirname(__file__), defaultextension=".png", filetypes=(("png files", "*.png"), 
                                                                                                                                    ("jpeg files", "*.jpeg"), 
                                                                                                                                    ("jpg files", "*.jpg")))
        
        edit_image = ImageDraw.Draw(self.image)

        contents = self.sv.get()
        location = self.active_loc.get()
        bounds = self.image_canvas.bbox(self.img_watermark)

        location_x = 5
        location_y = self.image.height - 20
        if location == 1:
            location_x = self.image.width / 2 - (bounds[2] - bounds[0]) / 2
        elif location == 2:
            location_x = self.image.width - (5 + (bounds[2] - bounds[0]))

        edit_image.text((location_x, location_y), contents, fill="black", font=ImageFont.truetype("arial.ttf", 15))

        self.image.save(filename)



def main():
    # Create Root
    root = tk.Tk()
    root.title("Water-marker")
    root.geometry("860x700")

    # Create WaterMarker object
    wm = WaterMarker(root)

    root.mainloop()

if __name__ == "__main__":
    main()
