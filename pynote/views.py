from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user, login_user
from .models import Note
from .models import User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Заметка слишком кароткая', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Заметка добавлена', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        first_name = request.form.get('firstName')

        user = User.query.filter_by(first_name=first_name).first()
        if user:
            return render_template("blog.html", user=user)
        else:
            flash('Такого пользователя не существует', category='error')

    return render_template("search.html", user=current_user)