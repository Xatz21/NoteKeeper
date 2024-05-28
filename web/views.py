from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Notes
from . import db
import json


views = Blueprint("views", __name__)

@views.route("/", methods=["POST", "GET"])
@login_required
def home_page():
    if request.method == "POST":
        notes = request.form.get("notes")
        
        if len(notes) < 1:
            flash("Empty note", category="error")
        else:
            new_notes = Notes(data=notes, user_id=current_user.id)
            db.session.add(new_notes)
            db.session.commit()
            flash("Note added", category="success")
                
            
    return render_template("home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    notes = json.loads(request.data)
    noteId = notes["noteId"]
    note = Notes.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        
    return jsonify({})
        