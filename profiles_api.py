from customer_api import *
from datetime import datetime
from run import db, app, bcrypt
from flask import jsonify, abort, make_response, request

class Profiles(db.Model):
    __tablename__ ='profiles'
    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column('fname',db.String)
    lname = db.Column('lname',db.String)
    age = db.Column('age',db.Integer)
    mobile = db.Column('mobile',db.String)
    created_date = db.Column('created_date',db.String)
    modified_date = db.Column('modified_date',db.String)
    user_id = db.Column('user_id',db.Integer)


@app.route('/profiles', methods=['GET'])
@token_required
def all_profiles(user):

    profiles = Profiles.query.all()

    output = []
    print(profiles)
    
    for profile in profiles:

        profiles_data = {}
        profiles_data['id'] = profile.id
        profiles_data['fname'] = profile.fname
        profiles_data['lname'] = profile.lname
        profiles_data['age'] = profile.age
        profiles_data['mobile'] = profile.mobile
        profiles_data['created_date'] = profile.created_date
        profiles_data['modified_date'] = profile.modified_date
        output.append(profiles_data)
    return jsonify({'profiles': output})

@app.route('/get_profiles', methods=['GET'])
@token_required
def get_profiles(user):
    profiles = Profiles.query.filter_by(user_id=user.id)
    
    if profiles.count() == 0:
        return jsonify({'message': 'No profiles found the current user'})
    output = []
    for profile in profiles:

        profiles_data = {}
        profiles_data['id'] = profile.id
        profiles_data['fname'] = profile.fname
        profiles_data['lname'] = profile.lname
        profiles_data['age'] = profile.age
        profiles_data['mobile'] = profile.mobile
        profiles_data['created_date'] = datetime.utcnow()
        profiles_data['modified_date'] = datetime.utcnow()
        output.append(profiles_data)
    return jsonify({'profiles': output})
        

@app.route('/create_profiles', methods=['POST'])
@token_required
def create_profiles(user):
    data = request.get_json()

    new_profile = Profiles(fname=data['fname'],lname=data['lname'],age=data['age'],mobile=data['mobile'],created_date=datetime.utcnow(), modified_date=datetime.utcnow(),user_id=user.id)

    db.session.add(new_profile)
    db.session.commit()

    return jsonify({'message': 'The New Profile has been created'})

@app.route('/profiles/<int:id>', methods=['PUT'])
@token_required
def update_profiles(user,id):

    profile = Profiles.query.filter_by(id=id,user_id=user.id).first()

    if not profile:
        return jsonify({'Message': 'No profiles to update'})
 
    data = request.get_json()
    profile.fname = data['fname']
    profile.lname = data['lname']
    profile.age = data['age']
    profile.mobile = data['mobile']
    profile.modified_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'Message': 'The profile has been updated'})

@app.route('/profiles/<int:id>', methods=['DELETE'])
@token_required
def delete_profiles(user,id):
    profile = Profiles.query.filter_by(id=id,user_id=user.id).first()

    if not profile:
        return jsonify({'Message': 'No profile to delete'})

    db.session.delete(profile)
    db.session.commit()

    return jsonify({'Message': 'Profile has been deleted successfully'})