from PIL import Image, ImageTk
import tkinter as tk


# Module Functions
def create_window(title, size, resizable=True):
    """
    Create a window with optional resizable property.

    Parameters:
        title (str): Title of the window.
        size (str): Size of the window in 'WidthxHeight' format.
        resizable (bool): Whether the window is resizable.

    Returns:
        Tk: The root window object.
    """
    window = tk.Tk()
    window.title(title)
    window.geometry(size)
    window.resizable(resizable, resizable)
    return window


class EditableButton:
    """A wrapper class for a tkinter Button with resizable image functionality."""

    def __init__(self, parent, text=None, command=None, image_path=None, **kwargs):
        self.button = tk.Button(parent, text=text, command=command, **kwargs)
        self.image_path = image_path
        self.image = None
        if image_path:
            self.load_image(image_path, self.button.winfo_reqwidth(), self.button.winfo_reqheight())
            self.button.config(image=self.image)
        self.button.pack()

    def load_image(self, image_path, width, height):
        """Load and resize the image maintaining the aspect ratio."""
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)

    def resize(self, width, height):
        """Resize the button and its image."""
        self.button.config(width=width, height=height)
        if self.image_path:
            self.load_image(self.image_path, width, height)
            self.button.config(image=self.image)


class EditableLabel:
    """A wrapper class for a tkinter Label with resizable image functionality."""

    def __init__(self, parent, text=None, image_path=None, **kwargs):
        self.label = tk.Label(parent, text=text, **kwargs)
        self.image_path = image_path
        self.image = None
        if image_path:
            self.load_image(image_path, self.label.winfo_reqwidth(), self.label.winfo_reqheight())
            self.label.config(image=self.image)
        self.label.pack()

    def load_image(self, image_path, width, height):
        """Load and resize the image maintaining the aspect ratio."""
        original_image = Image.open(image_path)
        resized_image = original_image.resize((width, height), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)

    def resize(self, width, height):
        """Resize the label and its image."""
        self.label.config(width=width, height=height)
        if self.image_path:
            self.load_image(self.image_path, width, height)
            self.label.config(image=self.image)


# Utility Functions
def add_button(parent, text, command=None, image_path=None, **kwargs):
    """Add a button with optional image."""
    button = EditableButton(parent, text=text, command=command, image_path=image_path, **kwargs)
    return button


def add_label(parent, text, image_path=None, **kwargs):
    """Add a label with optional image."""
    label = EditableLabel(parent, text=text, image_path=image_path, **kwargs)
    return label


# Example Usage
if __name__ == "__main__":
    # Create the main window
    window = create_window("Resizable GUI Example", "500x500")

    # Add a resizable button with an image
    button = add_button(window, text="Click Me", image_path="example.png")
    button.resize(200, 200)

    # Add a resizable label with an image
    label = add_label(window, text="Hello World", image_path="example.png")
    label.resize(300, 300)

    # Run the Tkinter main loop
    window.mainloop()