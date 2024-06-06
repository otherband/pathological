from flask import Flask, make_response

from pathological.exceptions.user_input_exception import UserInputException


def register_error_handlers(app: Flask):
    @app.errorhandler(UserInputException)
    def handle_user_input_exception(e: UserInputException):
        print(f"Exception occurred: {e}")
        return {
            "errorMessage": e.args[0]
        }, 400
