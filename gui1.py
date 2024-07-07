import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import os

class ScriptRunnerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Detection Widget")
        self.output_text = None
        self.image_label = None

        # Create the main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill="both")

        # Text area to display output
        self.create_output_area()

        # Button to run the script
        self.create_run_button()

        # Button to select an image
        self.create_image_button()

    def create_output_area(self):
        self.output_text = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=("Courier New", 12),
            state=tk.DISABLED,
        )
        self.output_text.pack(padx=10, pady=10, side=tk.TOP, expand=True, fill="both")

    def create_run_button(self):
        run_button = tk.Button(
            self.main_frame,
            text="Run Script",
            command=self.run_script,
            width=20,
            height=2,
            font=("Arial", 12, "bold"),
        )
        run_button.pack(pady=10)

    def run_script(self):
        # Replace 'your_script.py' with the name of your Python script
        script_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py")],
            initialdir=os.getcwd(),
            title="Select Script",
        )

        if script_path:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)

            # Execute the script and capture the output
            try:
                output = subprocess.check_output(
                    ["python", script_path], universal_newlines=True
                )
            except subprocess.CalledProcessError as e:
                output = f"Error: {e}\n"

            self.output_text.insert(tk.END, output)
            self.output_text.config(state=tk.DISABLED)

    def create_image_button(self):
        image_button = tk.Button(
            self.main_frame,
            text="Select Image",
            command=self.show_image,
            width=20,
            height=2,
            font=("Arial", 12, "bold"),
        )
        image_button.pack(pady=10)

    def show_image(self):
        # Replace 'your_image.jpg' with the name of your image file
        image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")],
            initialdir=os.getcwd(),
            title="Select Image",
        )

        if image_path:
            image = Image.open(image_path)
            image = image.resize((300, 300), Image.ANTIALIAS)
            image_tk = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self.main_frame, image=image_tk)
            self.image_label.image = image_tk
            self.image_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptRunnerGUI(root)
    root.mainloop()
