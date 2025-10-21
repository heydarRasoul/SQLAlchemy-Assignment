from flask import jsonify, request

from db import db
from models.company import Companies

def add_company():
    post_data = request.form if request.form else request.get_json()

    fields = ['company_name']
    required_fields =['company_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_company = Companies(values['company_name']) 

    try:
        db.session.add(new_company)
        db.session.commit()
    except: 
        db.session.rollback()
        return jsonify({"message": "unable to create record."}), 400 

    query = db.session.query(Companies).filter(Companies.company_name== values['company_name']).first()

    company = {
        "company_id" : query.company_id,
        "company_name": query.company_name
    }

    return jsonify({"message":"company created", "result":company}), 201


def get_all_companies():
    query= db.session.query(Companies).all()

    company_list = []

    for company in query:
        company_dict = {
            "company_id":company.company_id,
            "company_name":company.company_name
        }
        company_list.append(company_dict)

    return jsonify({"message": "companies founded.", "results": company_list}), 200


def get_company_by_id(company_id):
    query= db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if not query:
        return jsonify({"message": "company has not found"}), 404
    
    company={
        "company_id":query.company_id,
        "company_name":query.company_name
    }

    return jsonify({"message":"company found", "resukt": company}), 200


def update_company_by_id(company_id):
    post_data = request.form if request.form else request.get_json()
    query = db.session.query(Companies).filter(Companies.company_id==company_id).first()

    query.company_name = post_data.get("company_name", query.company_name)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}),400

    
    update_company_query = db.session.query(Companies).filter(Companies.company_id==company_id).first()

    company={
        "company_id": update_company_query.company_id,
        "company_name": update_company_query.company_name
    }

    return jsonify ({"message": "record updated.", "result": company}), 200


def delete_company_by_id(company_id):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not query:
        return jsonify({"message": "company not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to delete company"}), 400

    return jsonify({"message":"company deleted"}), 200