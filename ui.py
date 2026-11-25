from tkinter import *
from PIL import Image, ImageTk
import requests
import os
from io import BytesIO

class PosterCanvas:
    def __init__(self):
        self.window = Tk()
        self.poster_image = PhotoImage()
        self.window.title("Movies 2 Watch🍿")
        self.window.geometry("1000x600")
        bg_img = Image.open("Theatre-PNG-Pic.png")
        bg_img = bg_img.resize((1000, 600))
        photo = ImageTk.PhotoImage(bg_img)
        self.canvas = Canvas(self.window, width=1000, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=photo, anchor="nw")
# Starting image
        popcorn_img = Image.open("popcorn.jpg")
        popcorn_img = popcorn_img.resize((400, 300))
        popcorn_photo = ImageTk.PhotoImage(popcorn_img)
        self.popcorn_id = self.canvas.create_image(300, 80, image=popcorn_photo, anchor="nw", tags="intro")
# Search button
        button = Image.open("search_button.jpg")
        button = button.resize((50, 40))
        button_photo = ImageTk.PhotoImage(button)
        self.search_button = Button(image=button_photo, highlightthickness=0, command=self.show_gif)
        self.canvas.create_window(198, 460, window=self.search_button)
# Entry
        self.entry = Entry(width=25, font=("Times New Roman", 20), highlightthickness=0)
        self.add_placeholder(self.entry, "Enter the movie title.")
        self.canvas.create_window(419, 460, window=self.entry)

        self.window.mainloop()

    def add_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.config(fg="gray")

        def focus_in(event):
            if entry.get() == text:
                entry.delete(0, END)
                entry.config(fg="black")

        def focus_out(event):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg="gray")

        entry.bind("<FocusIn>", focus_in)
        entry.bind("<FocusOut>", focus_out)
# Gif animation
    def show_gif(self):

        gif = Image.open("old_movie_countdown.gif")

        frames = []

        try:
            while True:
                frame = gif.copy()
                frame = frame.resize((660, 395))
                frames.append(ImageTk.PhotoImage(frame))
                gif.seek(gif.tell() + 1)

        except EOFError:
            pass

        image_id = self.canvas.create_image(170, 34, image=frames[0], anchor="nw", tags="intro")

        def animate(frame_num=0):
            self.canvas.itemconfig(image_id, image=frames[frame_num])
            frame_num = (frame_num + 1) % len(frames)
            self.window.after(400, animate, frame_num)
        animate()

        def remove_intro():
            self.gif_running = False
            self.canvas.delete("intro")
            self.movie_finder()
        self.window.after(6560, remove_intro)

    def movie_finder(self):
# Request data from OMDB API
        api_key = os.getenv("OMDB_API_KEY")
        movie_title = self.entry.get()
        movie_parameters = {
            "apikey": api_key,
            "t": movie_title
        }

        response = requests.get("http://www.omdbapi.com/", params=movie_parameters)
        response.raise_for_status()
        movie_data = response.json()
# Show poster
        poster_url = movie_data["Poster"]
        poster_response = requests.get(poster_url)
        img = Image.open(BytesIO(poster_response.content))
        img = img.resize((250, 395))
        self.poster_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(
              170,
               34,
               image=self.poster_image,
               anchor="nw"
        )
# Show movie details
        self.canvas.create_text(450, 90, text=movie_data["Title"], fill="black", anchor="nw",
                                font=("Arial", 18, "bold"), tags="intro")
        self.canvas.create_text(450, 130, text=movie_data["Genre"], fill="black", anchor="nw",
                        font=("Arial", 16, "italic"), tags="intro")
        self.canvas.create_text(450, 170, text=f"Director: {movie_data["Director"]}", fill="black", anchor="nw",
                        font=("Arial", 16, "italic"), tags="intro")
        self.canvas.create_text(450, 210, text=f"Release Date: {movie_data["Released"]}", fill="black", anchor="nw",
                        font=("Arial", 16, "italic"), tags="intro")
        self.canvas.create_text(450, 250, width=350, text=movie_data["Plot"], fill="black", anchor="nw",
                        font=("Arial", 16, "italic"), tags="intro")
