import uuid
from flask import Flask, abort, flash, redirect, request

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
    if search is not None:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()
    return render_template("index.html", contacts=contacts_set, archiver=Archiver.get())


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


@app.route("/contacts/<contact_id>/delete", methods=["POST"])
def contacts_delete(contact_id=0):
    contact = Contact.find(contact_id)
    if not contact:
        return abort(404)
    contact.delete()
    flash("Deleted Contact!")
    return redirect("/contacts")


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()

