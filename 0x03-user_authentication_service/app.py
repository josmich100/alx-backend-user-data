#!/usr/bin/env python3
"""
Main module
"""


from flask import Flask, jsonify
from flask import request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def home() -> str:
    """Home endpoint
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """Users endpoint
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """Login endpoint
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        return jsonify({"message": "wrong password"}), 401


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Logout endpoint
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return jsonify({"message": "Unauthorized"}), 403
    AUTH.destroy_session(user.id)
    return jsonify({"message": "Bienvenue"})


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """Profile endpoint
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return jsonify({"message": "Unauthorized"}), 403
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """Reset password endpoint
    """
    email = request.form.get('email')
    try:
        user = AUTH.get_reset_password_token(email)
        return jsonify({"email": user.email, "reset_token": user.reset_token})
    except ValueError:
        return jsonify({"message": "email not registered"}), 403


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """Update password endpoint
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        return jsonify({"message": "Invalid reset token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
