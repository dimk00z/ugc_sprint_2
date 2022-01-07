import json

from locust import HttpUser, between, task


def get_votes_uuids():
    with open("votes.json") as file:
        votes = json.load(file)
    for vote in votes:
        yield vote


def get_reviews_uuids():
    with open("reviews.json") as file:
        reviews = json.load(file)
    for review in reviews:
        yield review


def get_bookmark_uuids():
    with open("bookmarks.json") as file:
        bookmarks = json.load(file)
    for bookmark in bookmarks:
        yield bookmark


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_likes(self):
        for vote in get_votes_uuids():
            self.client.get(f"/api/v1/film/{vote['movie_id']}/likes")

    @task
    def get_reviews(self):
        for review in get_reviews_uuids():
            self.client.post(
                "/api/v1/film/review/info",
                json={"user_id": review["user_id"], "movie_id": review["movie_id"]},
            )

    @task
    def get_bookmarks(self):
        for bookmark in get_bookmark_uuids():
            self.client.get(f"/api/v1/user/{bookmark['user_id']}/bookmarks")
