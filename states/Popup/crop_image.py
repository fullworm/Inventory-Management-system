from PIL import Image, ImageDraw, ImageTk
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog,Canvas, Toplevel
import ttkbootstrap as ttk
import math
import json
class CropImage:
    def __init__(self, master_toplevel, username):
        self.master = master_toplevel
        self.master.title("Circular Image Crop Tool")
        # Set a default size for the popup, can be adjusted
        self.master.geometry("800x600") 
        
        # Make the popup modal: grabs input and stays on top
        self.master.grab_set() 
        # Make it transient to the main window (iconifies/destroys with main)
        self.master.transient(self.master.master) 
        
        # Handle window closing to release the grab
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.original_image = None
        self.display_image = None # PhotoImage for displaying on canvas
        self.canvas_image_id = None

        self.circle_center = (0, 0)
        self.circle_radius = 0 
        self.circle_id = None # ID of the circle drawn on the canvas

        self.start_x = None
        self.start_y = None
        self.dragging_circle = False
        self.username = username
        self.pfpPath = ''
        self.menuPfp = ''

        # --- Widgets ---
        # Frame for controls
        self.controls_frame = ttk.Frame(self.master, padding=10)
        self.controls_frame.pack(side="top", fill="x")

        self.load_button = ttk.Button(
            self.controls_frame, text="Load Image", command=self.load_image
        )
        self.load_button.pack(side="left", padx=5)

        self.crop_button = ttk.Button(
            self.controls_frame, text="Crop Image", command=self.crop_image, state="disabled"
        )
        self.crop_button.pack(side="left", padx=5)

        self.radius_label = ttk.Label(self.controls_frame, text="Radius:")
        self.radius_label.pack(side="left", padx=5)
        self.radius_slider = ttk.Scale(
            self.controls_frame,
            from_=20, to=300, # Min/max radius
            orient="horizontal",
            command=self.update_radius_from_slider,
            length=200,
            state='disabled'
        )
        self.radius_slider.set(self.circle_radius)
        self.radius_slider.pack(side="left", padx=5)


        # Canvas for image display and drawing - use tkinter.Canvas
        self.canvas = Canvas(self.master, bg="lightgray", highlightbackground="darkgray", highlightthickness=2)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Bindings for dragging the circle
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Ensure canvas dimensions are updated before initial image load for resizing
        self.master.update_idletasks()

    def on_closing(self):
        """Releases the grab and destroys the Toplevel window when closed."""
        self.master.grab_release()
        self.master.destroy()

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Jpg", "*.jpg"), ('PNG', '*.png'), ('MP4', '*.mp4')]
        )
        if file_path:
            try:
                self.original_image = Image.open(file_path).convert("RGBA")
                self.display_image = self.resize_image_for_display(self.original_image)
                
                # Clear previous image and circle
                self.canvas.delete("all")
                
                # Center image on canvas initially
                self.canvas_image_id = self.canvas.create_image(
                    self.canvas.winfo_width() / 2, 
                    self.canvas.winfo_height() / 2,
                    image=self.display_image,
                    anchor="center"
                )


                # Set initial circle center to image center
                self.circle_center = (
                    self.canvas.winfo_width() / 2,
                    self.canvas.winfo_height() / 2
                )
                self.draw_circle()
                self.crop_button.config(state="normal")
                self.radius_slider.configure(state='normal')

            except Exception as e:
                Messagebox.show_error(
                    title="Error Loading Image", message=f"Could not load image: {e}", parent=self.master
                )
                self.original_image = None
                self.display_image = None
                self.canvas.delete("all")
                self.crop_button.config(state="disabled")

    def resize_image_for_display(self, pil_image):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # If canvas dimensions not yet available, use a reasonable default for calculation
        if not canvas_width or not canvas_height: 
            canvas_width = 700 
            canvas_height = 500

        img_width, img_height = pil_image.size

        # Determine if resizing is needed and calculate new dimensions
        if img_width > canvas_width or img_height > canvas_height:
            # Add a small buffer so image isn't right at the edge
            max_display_width = canvas_width * 0.95
            max_display_height = canvas_height * 0.95

            ratio = min(max_display_width / img_width, max_display_height / img_height)
            new_width = int(img_width * ratio) 
            new_height = int(img_height * ratio)

            # Ensure dimensions are at least 1 pixel
            new_width = max(1, new_width)
            new_height = max(1, new_height)


            resized_image = pil_image.copy().resize((new_width, new_height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
        else:
            return ImageTk.PhotoImage(pil_image.copy())

    def draw_circle(self):
        if self.circle_id:
            self.canvas.delete(self.circle_id)

        x, y = self.circle_center
        r = self.circle_radius

        self.circle_id = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            outline="red", width=3, tags="crop_circle"
        )

    def update_radius_from_slider(self, val):
        self.circle_radius = int(float(val))
        self.draw_circle()

    def on_press(self, event):
        if self.original_image and self.circle_id:
            x1, y1, x2, y2 = self.canvas.coords(self.circle_id)
            # Check if click is near the circle boundary or inside
            if (x1 - 10 <= event.x <= x2 + 10 and y1 - 10 <= event.y <= y2 + 10):
                self.dragging_circle = True
                self.start_x = event.x
                self.start_y = event.y

    def on_drag(self, event):
        if self.dragging_circle:
            dx = event.x - self.start_x
            dy = event.y - self.start_y

            self.circle_center = (self.circle_center[0] + dx, self.circle_center[1] + dy)
            self.canvas.move(self.circle_id, dx, dy)

            self.start_x = event.x
            self.start_y = event.y

    def on_release(self, event):
        self.dragging_circle = False

    def crop_image(self):
        if not self.original_image:
            Messagebox.show_warning(
                title="No Image", message="Please load an image first.", parent=self.master
            )
            return

        if not self.canvas_image_id:
            return

        # Get coordinates of the displayed image on the canvas (its center)
        img_canvas_x, img_canvas_y = self.canvas.coords(self.canvas_image_id)
        
        # Convert canvas-centered coordinates to top-left for the displayed image
        display_width, display_height = self.display_image.width(), self.display_image.height()
        img_left_on_canvas = img_canvas_x - (display_width / 2)
        img_top_on_canvas = img_canvas_y - (display_height / 2)

        # Calculate the circle's center relative to the top-left of the *displayed* image
        circle_center_on_display_x = self.circle_center[0] - img_left_on_canvas
        circle_center_on_display_y = self.circle_center[1] - img_top_on_canvas

        # Scale these coordinates and radius back to the original image's dimensions
        original_width, original_height = self.original_image.size
        
        # Calculate scaling factors
        scale_x = original_width / display_width
        scale_y = original_height / display_height

        original_circle_center_x = int(circle_center_on_display_x * scale_x)
        original_circle_center_y = int(circle_center_on_display_y * scale_y)
        
        # Use the average or min scale for radius to avoid disproportionate scaling if image aspect ratio changed
        # It's better to use the scaling factor that was applied to the image itself if it was constrained
        # For simplicity, we can assume the image was scaled proportionally, so min(scale_x, scale_y) is robust.
        original_circle_radius = int(self.circle_radius * min(scale_x, scale_y)) 

        # Ensure the circle is within the bounds of the original image (important for edge cases)
        original_circle_radius = max(1, original_circle_radius) # Minimum radius

        # Clamp circle center to prevent it from going entirely off the original image
        original_circle_center_x = max(original_circle_radius, min(original_width - original_circle_radius, original_circle_center_x))
        original_circle_center_y = max(original_circle_radius, min(original_height - original_circle_radius, original_circle_center_y))

        # Create a blank image with a transparent background
        # We create it the size of the original image first, then crop later
        cropped_image_with_alpha = Image.new("RGBA", self.original_image.size, (0, 0, 0, 0))

        # Create a circular mask image
        mask = Image.new("L", self.original_image.size, 0) # Black (0) means transparent
        draw = ImageDraw.Draw(mask)

        # Draw a white (255) circle on the mask
        x_orig, y_orig = original_circle_center_x, original_circle_center_y
        r_orig = original_circle_radius
        draw.ellipse((x_orig - r_orig, y_orig - r_orig, x_orig + r_orig, y_orig + r_orig), fill=255) # White (255) means opaque

        # Apply the mask to the original image
        # This will make areas outside the circle transparent
        cropped_image_with_alpha.paste(self.original_image, (0, 0), mask)

        # Determine the bounding box for the final crop
        # This ensures the output image is only the size of the circle's content
        final_bbox = (
            x_orig - r_orig,
            y_orig - r_orig,
            x_orig + r_orig,
            y_orig + r_orig
        )
        # Ensure bounding box coordinates are within image bounds
        final_bbox = (
            max(0, final_bbox[0]),
            max(0, final_bbox[1]),
            min(original_width, final_bbox[2]),
            min(original_height, final_bbox[3])
        )

        cropped_image = cropped_image_with_alpha.crop(final_bbox)

        usericon = cropped_image.resize((250,250), Image.Resampling.LANCZOS)

        usericon.save(f'userImages/{self.username}Icon.png')

        menuicon = cropped_image.resize((100,100), Image.Resampling.LANCZOS)
        menuicon.save(f'userImages/menu{self.username}Icon.png')
        # Save or display the cropped image
        self.pfpPath = f'userImages/{self.username}Icon.png'
        self.menuPfp = f'userImages/menu{self.username}Icon.png'
        self.set_pfp()
        self.show_cropped_image(usericon)


    def show_cropped_image(self, image_to_display):
        # Create a new Toplevel window to display the result
        top_result = Toplevel(self.master) # Make it transient to the cropping tool popup
        top_result.title("Cropped Image Result")
        top_result.transient(self.master)
        top_result.grab_set() # Make it modal to the cropping tool popup

        # Convert PIL image to PhotoImage for Tkinter
        # Keep a reference on the Toplevel window to prevent garbage collection
        top_result.tk_image = ImageTk.PhotoImage(image_to_display)

        display_canvas = Canvas(top_result, bg="white", width=image_to_display.width, height=image_to_display.height)
        display_canvas.pack(padx=10, pady=10)
        display_canvas.create_image(
            image_to_display.width / 2,
            image_to_display.height / 2,
            image=top_result.tk_image,
            anchor="center"
        )

        close_button = ttk.Button(top_result, text="Close", command=top_result.destroy)
        close_button.pack(pady=5)

        # When this result window closes, release its grab
        top_result.protocol("WM_DELETE_WINDOW", top_result.destroy)
    def set_pfp(self):
        with open('users.json', 'w+') as u:
            users = json.load(u) 
            users[self.username]['Profile Picture'] = self.pfpPath
            users[self.username]['Profile Picture Small'] = self.menuPfp
            json.dump(users, u)
            u.close()
    @classmethod
    def get_count():
        return CropImage._instance_count
