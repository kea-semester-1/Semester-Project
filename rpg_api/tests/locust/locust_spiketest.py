from locust import FastHttpUser, tag, task, between, events
from locust.runners import MasterRunner, WorkerRunner
import gevent
from typing import Any
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


def change_load(
    environment: Any, user_count: int, spawn_rate: int, length_in_seconds: int
) -> None:
    """Change the load (number for users) during execution of the test."""

    environment.runner.start(user_count, spawn_rate, wait=False)
    gevent.sleep(length_in_seconds)


@events.test_start.add_listener
def on_test_start(environment: Any, **kwargs: dict[Any, Any]) -> None:
    """
    Add event listener, this allows us to control the execution of the test,
    allowing us to spike users during the test.
    """

    # Do not execute this on master or worker nodes, if we want to run test distributed
    if isinstance(environment.runner, (MasterRunner, WorkerRunner)):
        return

    # Schedule the stages of the test

    # Normal load phase 50 users for 300 seconds
    gevent.spawn(
        change_load, environment, user_count=50, spawn_rate=1, length_in_seconds=300
    )

    # Spike phase - after 300 seconds we go 150 users for 120 seconds
    gevent.spawn_later(
        300,
        change_load,
        environment,
        user_count=150,
        spawn_rate=1,
        length_in_seconds=120,
    )

    # Back to normal phase - back to 50 users for 300 seconds
    gevent.spawn_later(
        420,
        change_load,
        environment,
        user_count=50,
        spawn_rate=1,
        length_in_seconds=300,
    )
    gevent.spawn_later(720, environment.runner.quit)
