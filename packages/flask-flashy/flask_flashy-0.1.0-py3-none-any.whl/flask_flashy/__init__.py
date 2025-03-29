from flask import Flask, session


class Flashy:
    def __init__(self, app: Flask = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        self.app = app

        @app.context_processor
        def flashy_context_processor():
            """Injects the get_flashy_messages function into the template context."""

            def get_flashy_messages():
                """Returns the flashy messages from the session and clears them."""
                return self.get_flashy_messages()

            return dict(get_flashy_messages=get_flashy_messages)

    def flash(self, message: str, category: str = "message", **kwargs) -> None:
        """_summary_

        Args:
            message (str): Text of the message to be displayed.
            category (str, optional): Category of the message for styling purposes. Defaults to "message".
            **kwargs: Optional additional attributes to be added to the message object, such as url, title, timestamp, etc.
        """
        flashes = session.get("_flashy", [])
        flash = FlashyMessage(message, category, **kwargs)
        flashes.append(flash)
        session["_flashy"] = flashes

    def get_flashy_messages(self) -> list | None:
        """Returns the flashy messages from the session and clears them."""
        flashes = session.pop("_flashy")
        return flashes


class FlashyMessage:
    def __init__(self, message: str, category: str = "message", **kwargs) -> None:
        self.message = message
        self.category = category
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"{self.message}"
