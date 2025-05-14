from flask import render_template, redirect, url_for, flash, request, session
import re


@app.route("/phone", methods=['GET', 'POST'])
def phone():
    global USER_NOW
    number = request.form.get('number')
    if not re.match(r'^\+7\d{10}$', number):
        flash('Некорректный формат номера')