from flask import request, jsonify

from db import db
from models.warranty import Warranties

def add_warranty():
    post_data = request.form if request.form else request.json 

    fields = ['product_id', 'warranty_months']
    required_fields = ['product_id', 'warranty_months']

    values = {} 

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify ({"message": f"{field} is required"}), 404

        values[field] = field_data
    
    new_warranty = Warranties(values['product_id'], values['warranty_months'])

    try:
        db.session.add(new_warranty)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    query = db.session.query(Warranties).filter(Warranties.product_id == values['product_id']).first()

    warranty = {
        "warranty_id": query.warranty_id,
        "product_id" : query.product_id,
        "warranty_months": query.warranty_months
    }

    return jsonify ({"message":"warranty created", "result": warranty}), 201



def get_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not query:
        return jsonify({"message": "warranty has not found"}), 404
    
    warranty = {
        "warranty_id": query.warranty_id,
        "product_id" : query.product_id,
        "warranty_months": query.warranty_months}

    return jsonify({"message":"category found", "result": warranty}), 200



def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.get_json()

    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not query:
        return jsonify({"message": "warranty not found"}), 404

    query.warranty_months = post_data.get("warranty_months", query.warranty_months)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    updated_warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    warranty_dict = {
        "warranty_id": updated_warranty_query.warranty_id,
        "product_id": updated_warranty_query.product_id,
        "warranty_months": updated_warranty_query.warranty_months
    }

    return jsonify({"message": "warranty updated successfully", "result": warranty_dict}), 200


def delete_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": "warranty not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to delete warranty"}), 400

    return jsonify({"message":"warranty deleted"}), 200
