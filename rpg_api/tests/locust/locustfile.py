from locust import FastHttpUser, tag, task, between
from rpg_api.tests.locust import utils
import random

from uuid import uuid4

PREFIX = "/api/postgres"


class WebUser(FastHttpUser):
    """Default user for load testing."""

    wait_time = between(1, 2)

    def on_start(self) -> None:
        """
        Runs before each user is created.

        This will create a user, log the user in and attach data to that user,
        that will later be used e.g. header and id.
        """

        self.user_id, self.token_header = utils.setup_user(self)

    def on_stop(self) -> None:
        with self.client.delete(
            url=f"{PREFIX}/base-users",
            headers=self.token_header,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                utils.handle_error(response)

    @task(1)
    @tag("create_char")
    def create_character(self) -> None:
        """Create character endpoint."""

        with self.client.get(
            url=f"{PREFIX}/base-classes",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                utils.handle_error(response)

            response_data = utils.get_data(response=response)
            classes = [data["id"] for data in response_data]

        with self.client.post(
            url=f"{PREFIX}/characters",
            headers=self.token_header,
            json={
                "base_class_id": random.choice(classes),
                "gender": "male",
                "character_name": f"string{uuid4()}",
            },
            catch_response=True,
        ) as response:
            if response.status_code != 201:
                utils.handle_error(response)

    @task(5)
    @tag("get_chars")
    def get_all_characters(self) -> None:
        """Get all characters for logged in user."""

        with self.client.get(
            url=f"{PREFIX}/characters",
            headers=self.token_header,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                utils.handle_error(response)

    @task(10)
    @tag("get_char_place")
    def get_character_place_details(self) -> None:
        """Get the place details for specific character."""

        # T
        with self.client.get(
            url=f"{PREFIX}/characters",
            headers=self.token_header,
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                utils.handle_error(response)
            response_data = utils.get_data(response=response)
            character_ids = [data["id"] for data in response_data]

        if character_ids:
            random_character_id = random.choice(character_ids)

            with self.client.get(
                url=f"{PREFIX}/characters/place/{random_character_id}",
                headers=self.token_header,
                name=f"{PREFIX}/characters/place/:character_id",
                catch_response=True,
            ) as response_data:
                if response.status != 200:
                    utils.handle_error(response=response)

    @task(20)
    @tag("move_char")
    def move_character(self) -> None:
        """Move specific character in the world."""

        with self.client.get(
            url=f"{PREFIX}/characters", headers=self.token_header, catch_response=True
        ) as response:
            if response.status_code != 200:
                utils.handle_error(response)
            response_data = utils.get_data(response=response)
            character_ids = [data["id"] for data in response_data]

        if character_ids:
            random_character_id = random.choice(character_ids)

            with self.client.patch(
                url=f"{PREFIX}/character-locations/{random_character_id}",
                headers=self.token_header,
                name=f"{PREFIX}/character-locations/:random_character_id",
                json={"x": 0, "y": 0},
                catch_response=True,
            ) as response:
                if response.status_code != 200:
                    utils.handle_error(response=response)
