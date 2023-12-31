#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, abort, jsonify, make_response, redirect, request
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
def login():
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


@app.route('/sessions', methods=['DELETE'])
def logout():
    try:
        session_id = request.cookies.get('session_id')

        user = AUTH.get_user_from_session_id(session_id)

        if user:
            AUTH.destroy_session(user.id)
            response = redirect('/')
            response.delete_cookie('session_id')
            return response, 302
        else:
            abort(403)

    except Exception as e:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    try:
        session_id = request.cookies.get('session_id')

        user = AUTH.get_user_from_session_id(session_id)

        if user:
            response = {
                "email": user.email
            }
            return jsonify(response), 200
        else:
            abort(403)

    except Exception as e:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        email = request.form.get('email')

        reset_token = AUTH.get_reset_password_token(email)

        response = {
            "email": email,
            "reset_token": reset_token
        }
        return jsonify(response), 200
    except ValueError as e:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
        AUTH.update_password(reset_token, new_password)

        response = {
            "email": email,
            "message": "Password updated"
        }
        return jsonify(response), 200
    except ValueError as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
