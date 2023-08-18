#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, abort, jsonify, make_response, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = AUTH.register_user(email, password)

        response = {
            "email": user.email,
            "message": "user created"
        }
        return jsonify(response), 200
    except ValueError as e:
        response = {"message": "email already registered"}
        return jsonify(response), 400


@app.route('/sessions', methods=['POST'])
def sessions():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if not AUTH.valid_login(email, password):
            abort(401)

        session_id = AUTH.create_session(email)
        response = make_response(jsonify(
            {"email": f"{email}", "message": "logged in"})
            )
        response.set_cookie("session_id", session_id)

        return response, 200
    except Exception as e:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
