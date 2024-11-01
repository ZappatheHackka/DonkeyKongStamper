from tkinter import *
from tkinter.filedialog import askopenfilename
from wand.image import Image as ig
from PIL import Image, ImageTk, UnidentifiedImageError
from tkinter import Tk, Label, Button, Canvas, messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

# Global variable to keep the image reference-garbage collection
# is why the image would not appear on the canvas(check explanation)
img = None
filename = None


def pathgrabber():
    global img
    global filename  # Declare img as global to keep a reference to it
    filename = askopenfilename()
    image = Image.open(filename)
    img_width, img_height = image.size

    # Resizing if the image is too large
    if img_height > 450 or img_width > 450:
        while img_width > 450 or img_height > 450:
            img_width *= 0.99
            img_height *= 0.99
    elif img_height < 450 or img_width < 450:
        while img_width < 450 or img_height < 450:
            img_width *= 1.005
            img_height *= 1.005

    # Resize the image and prepare it for Tkinter
    im = image.resize((int(img_width), int(img_height)))
    img = ImageTk.PhotoImage(im)

    # Add image to canvas at position (225, 225)
    canvas.create_image(225, 300, image=img)
    window.update()


def stamper():
    global img
    global filename

    # Open the background image
    with ig(filename=filename) as background:
        bg_width, bg_height = background.width, background.height  # Get background image size

        # Open the watermark image
        with ig(filename="DK_approve-removebg.png") as watermark:
            wm_width, wm_height = watermark.width, watermark.height  # Get watermark size

            # Scale the watermark to be 1/6th of the background image width
            scale_factor = 1 / 4  # Ensure the watermark is always 1/6th of the background width
            new_wm_width = int(bg_width * scale_factor)
            new_wm_height = int((new_wm_width / wm_width) * wm_height)  # Maintain aspect ratio

            # Resize the watermark
            watermark.resize(new_wm_width, new_wm_height)

            # Calculate position based on percentage (5% margin from right and bottom)
            left = bg_width * 0.95 - new_wm_width  # 5% margin from the right
            top = bg_height * 0.95 - new_wm_height  # 5% margin from the bottom

            # Apply the watermark with transparency and calculated position
            background.watermark(image=watermark, transparency=.45, left=int(left), top=int(top))

        # Save the stamped image
        background.save(filename="approved.png")

        # Using Pillow to resize the stamped image and print to Tkinter window. Same code as above.
        image = Image.open("approved.png")

        img_height, img_width = image.height, image.width

        if img_height > 450 or img_width > 450:
            while img_width > 450 or img_height > 450:
                img_width *= 0.99
                img_height *= 0.99
        elif img_height < 450 or img_width < 450:
            while img_width < 450 or img_height < 450:
                img_width *= 1.005
                img_height *= 1.005

        im = image.resize((int(img_width), int(img_height)))
        img = ImageTk.PhotoImage(im)

        # Add image to canvas at position (225, 225)
        canvas.create_image(225, 300, image=img)
        window.update()

    # show messagebox telling user their image has been approved
    messagebox.showinfo(title="Dong Approved", message="Your image has received the Donkey Kong stamp of approval!\n"
                                                       "Please check your working directory for a file named"
                                                       "\"approved.png\".")


# Initializing window
window = Tk()
window.title('Donkey Kong Approval Generator')
window.geometry("800x745")
window.config(pady=8)

# Text above the image to be watermarked
label = Label(text='Donkey Kong Approval Stamper', font=('Comic Sans', 18))
label.pack()

# Canvas to hold the image
canvas = Canvas(width=450, height=600, bg='white',)
canvas.pack(pady=3)

# Button to select background image
search = Button(text='Select Image', command=pathgrabber, pady=7)
search.pack(pady=3)

# Button that adds Donkey Kong Watermark
stamper = Button(text='Give Donkey Kong\'s Approval', command=stamper, pady=5)
stamper.pack(pady=3)

window.mainloop()
