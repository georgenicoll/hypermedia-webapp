from flask import Blueprint, abort, request, Response
from flask import render_template

from contacts_model import Contact, Archiver


# Create a blueprint for Hyperview HXML routes
hxml_api = Blueprint('hxml_api', __name__, url_prefix='/hv')


@hxml_api.route("/contacts")
def hxml_contacts():
    """List all contacts with search capability"""
    search = request.args.get("q")
    page = int(request.args.get("page", 1))

    if search:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all(page)

    return Response(
        render_template("hxml/contacts.xml", contacts=contacts_set, page=page, search=search or ''),
        mimetype='application/xml'
    )


@hxml_api.route("/contacts/<contact_id>")
def hxml_contacts_view(contact_id):
    """View a single contact"""
    contact = Contact.find(contact_id)
    if not contact:
        return abort(404)

    return Response(
        render_template("hxml/show.xml", contact=contact),
        mimetype='application/xml'
    )


@hxml_api.route("/contacts/new", methods=['GET'])
def hxml_contacts_new_get():
    """Show form to create a new contact"""
    return Response(
        render_template("hxml/new.xml", contact=Contact()),
        mimetype='application/xml'
    )


@hxml_api.route("/contacts/new", methods=['POST'])
def hxml_contacts_new_post():
    """Create a new contact"""
    c = Contact(
        None,
        request.form['first_name'],
        request.form['last_name'],
        request.form['phone'],
        request.form['email']
    )

    if c.save():
        # Return success screen that auto-navigates back
        return Response(
            render_template("hxml/created.xml", contact=c),
            mimetype='application/xml'
        )
    else:
        # Return form with errors
        return Response(
            render_template("hxml/new.xml", contact=c),
            mimetype='application/xml'
        )


@hxml_api.route("/contacts/<contact_id>/edit", methods=["GET"])
def hxml_contacts_edit_get(contact_id):
    """Show form to edit an existing contact"""
    contact = Contact.find(contact_id)
    if not contact:
        return abort(404)

    return Response(
        render_template("hxml/edit.xml", contact=contact),
        mimetype='application/xml'
    )


@hxml_api.route("/contacts/<contact_id>/edit", methods=["POST"])
def hxml_contacts_edit_post(contact_id):
    """Update an existing contact"""
    c = Contact.find(contact_id)
    if not c:
        return abort(404)

    c.update(
        request.form['first_name'],
        request.form['last_name'],
        request.form['phone'],
        request.form['email']
    )

    if c.save():
        # Return success screen that shows the updated contact
        return Response(
            render_template("hxml/show.xml", contact=c),
            mimetype='application/xml'
        )
    else:
        # Return form with errors
        return Response(
            render_template("hxml/edit.xml", contact=c),
            mimetype='application/xml'
        )


@hxml_api.route("/contacts/<contact_id>/email/validate", methods=["GET"])
def hxml_contacts_email_validate(contact_id):
    """Validate email field (returns error text or empty)"""
    c = Contact.find(contact_id)
    if not c:
        return abort(404)

    c.email = request.args.get('email')
    c.validate()

    error = c.errors.get('email') or ""
    return Response(
        f'<text xmlns="https://hyperview.org/hyperview" style="error">{error}</text>',
        mimetype='application/xml'
    )


@hxml_api.route("/contacts/<contact_id>", methods=["DELETE"])
def hxml_contacts_delete(contact_id):
    """Delete a contact"""
    contact = Contact.find(contact_id)
    if not contact:
        return abort(404)

    contact.delete()

    # Return screen that auto-navigates back to list
    return Response(
        render_template("hxml/deleted.xml"),
        mimetype='application/xml'
    )


@hxml_api.route("/contacts/count")
def hxml_contacts_count():
    """Get total contact count"""
    count = Contact.count()
    return Response(
        f'<text xmlns="https://hyperview.org/hyperview" style="count-text">({count} total Contacts)</text>',
        mimetype='application/xml'
    )
