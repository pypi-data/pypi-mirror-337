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
            return dict(get_flashy_messages=get_flashy_messages)


class FlashyMessage:
    def __init__(self, message: str, category: str = "message", **kwargs) -> None:
        self.message = message
        self.category = category
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"{self.message}"


def flash(message: str, category: str = "message", **kwargs) -> None:
    """Flashes a message to the next request. In order to remove the flashed message from the session and display it to the user, the template has to call :func:`get_flashy_messages`.

    Args:
        message (str): Text of the message to be displayed.
        category (str, optional): Category of the message for styling purposes. Defaults to "message".
        **kwargs: Optional additional attributes to be added to the message object, such as url, title, timestamp, etc.
    """
    flashes = session.get("_flashy", [])
    flash = FlashyMessage(message, category, **kwargs)
    flashes.append(flash)
    session["_flashy"] = flashes


def get_flashy_messages() -> list:
    """Pulls all flashed messages from the session, removes them, and returns them.

    Returns:
        list: List of flashed messages.
    """
    flashes = session.get("_flashy", None)
    if flashes is None:
        return []
    flashes = session.pop("_flashy")
    return flashes
