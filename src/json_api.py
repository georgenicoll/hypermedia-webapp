from flask import Blueprint, jsonify, request
from contacts_model import Contact, Archiver


# Create a blueprint for API v1 routes
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@api_v1.route("/contacts", methods=["GET"])
def json_v1_contacts():
    contacts_set = Contact.all()
    contacts_dict = [c.__dict__ for c in contacts_set]
    return {'contacts': contacts_dict}

@api_v1.route("/contacts", methods=["POST"])
def json_v1_contacts_new():
    data = request.json
    c = Contact(None,
      data.get('first'),
      data.get('last'),
      data.get('phone'),
      data.get('email'))
    if c.save():
        return c.__dict__
    else:
        return {"errors": c.errors}

@api_v1.route("/contacts/<contact_id>", methods=["GET"])
def json_contact_view(contact_id=0):
    contact = Contact.find(contact_id)
    return contact.__dict__

@api_v1.route("/contacts/<contact_id>", methods=["PUT"])
def json_contact_edit(contact_id):
    c = Contact.find(contact_id)
    assert c is not None
    data = request.json
    c.update(
        data['first'],
        data['last'],
        data['phone'],
        data['email'])
    if c.save():
        return c.__dict__
    else:
        return {"errors": c.errors}

@api_v1.route("/contacts/<contact_id>", methods=["DELETE"])
def json_contacts_delete(contact_id=0):
    contact = Contact.find(contact_id)
    assert contact is not None
    contact.delete()
    return jsonify({"success": True})
