import os
import random
import requests
import smtplib
from email.message import EmailMessage

class MovieRecommendation:
    def __init__(self, m_list):
        self.api_key = os.getenv("OMDB_API_KEY")
        self.user_email = os.getenv("EMAIL_ADDRESS")
        self.user_password = os.getenv("EMAIL_PASSWORD")
        self.movie_title = ""
        self.movie_list = m_list
        self.movie_parameters = {}
        self.recommend_movie()

# Movie recommendations feature
    def recommend_movie(self):
        self.movie_title = random.choice(self.movie_list)
        self.movie_parameters = {
            "apikey": self.api_key,
            "t": self.movie_title
        }
        response = requests.get("http://www.omdbapi.com/", params=self.movie_parameters)
        response.raise_for_status()
        movie_data = response.json()
        msg = EmailMessage()

        msg["Subject"] = "What to watch"
        msg["From"] = self.user_email
        msg["To"] = "primefire0.3@gmail.com"

        msg.set_content(f"Recommendation of the week: {movie_data["Title"]}\n\n{movie_data["Plot"]}")

        poster_url = movie_data["Poster"]
        image_data = requests.get(poster_url).content
        msg.add_attachment(
            image_data,
            maintype="image",
            subtype="jpeg",
            filename=f"{movie_data["Title"]}.jpg"
        )

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(self.user_email, self.user_password)
            connection.send_message(msg)