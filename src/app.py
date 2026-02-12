from time import sleep
import uuid
from flask import Flask, abort, flash, redirect, request, send_file

from contacts_model import Contact, Archiver
from flask import render_template


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.route("/")
def index():
    return redirect("/contacts")


@app.route("/contacts")
def contacts():
    search = request.args.get("q")
    page = int(request.args.get("page", 1))
    if search:
        contacts_set = Contact.search(search)
        if request.headers.get('HX-Trigger') == 'search':
            return render_template("rows.html", contacts=contacts_set)
    else:
        contacts_set = Contact.all(page)
    if request.headers.get('HX-Trigger') == 'search':
        return render_template("rows_and_lazy_load.html", contacts=contacts_set, page=page)
    return render_template("index.html", contacts=contacts_set, page=page, archiver=Archiver.get())


@app.route("/contacts/count")
def contacts_count():
    count = Contact.count()
    return "(" + str(count) + " total Contacts)"


@app.route("/contacts/new", methods=['GET'])
def contacts_new_get():
    return render_template("new.html", contact=Contact())


@app.route("/contacts/new", methods=['POST'])
def contacts_new():
    c = Contact(
      None,
      request.form['first_name'],
      request.form['last_name'],
      request.form['phone'],
      request.form['email'])
    if c.save():
        flash("Created New Contact!")
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=c)


@app.route("/contacts/<contact_id>")
def contacts_view(contact_id):
    contact = Contact.find(contact_id)
    if not contact:
        return abort(404)
    return render_template("show.html", contact=contact)


@app.route("/contacts/<contact_id>/edit", methods=["GET"])
def contacts_edit_get(contact_id):
    contact = Contact.find(contact_id)
    if not contact:
        return abort(404)
    return render_template("edit.html", contact=contact)


@app.route("/contacts/<contact_id>/edit", methods=["POST"])
def contacts_edit_post(contact_id):
    c = Contact.find(contact_id)
    if not c:
        return abort(404)
    c.update(
      request.form['first_name'],
      request.form['last_name'],
      request.form['phone'],
      request.form['email'])
    if c.save():
        flash("Updated Contact!")
        return redirect("/contacts/" + str(contact_id))
    else:
        return render_template("edit.html", contact=c)


@app.route("/contacts/<contact_id>/email", methods=["GET"])
def contacts_email_get(contact_id):
    c = Contact.find(contact_id)
    if not c:
        return abort(404)
    c.email = request.args.get('email')
    c.validate()
    return c.errors.get('email') or ""


@app.route("/contacts/<contact_id>", methods=["DELETE"])
def contacts_delete(contact_id):
    contact = Contact.find(contact_id)
    if not contact:
        return abort(404)
    contact.delete()
    if request.headers.get('HX-Trigger') == 'delete-btn':
        flash("Deleted Contact!")
        return redirect("/contacts", 303)
    else:
        return ""


@app.route("/contacts", methods=["DELETE"])
def contacts_delete_all():
    page = int(request.args.get("page", 1))
    contact_ids = [
        int(id)
        for id in request.args.getlist("selected_contact_ids")
    ]
    for contact_id in contact_ids:
        contact = Contact.find(contact_id)
        if not contact:
            return abort(404)
        contact.delete()
    flash("Deleted Contact!")
    contacts_set = Contact.all(page)
    return render_template("index.html", contacts=contacts_set, page=page, archiver=Archiver.get())


@app.route("/contacts/archive", methods=["POST"])
def start_archive():
    archiver = Archiver.get()
    archiver.run()
    return render_template("archive_ui.html", archiver=archiver)


@app.route("/contacts/archive", methods=["GET"])
def archive_status():
    return render_template("archive_ui.html", archiver=Archiver.get())


@app.route("/contacts/archive/file", methods=["GET"])
def archive_content():
    archiver = Archiver.get()
    return send_file(
        archiver.archive_file(), "archive.json", as_attachment=True
    )


@app.route("/contacts/archive", methods=["DELETE"])
def reset_archive():
    archiver = Archiver.get()
    archiver.reset()
    return render_template("archive_ui.html", archiver=archiver)


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()

