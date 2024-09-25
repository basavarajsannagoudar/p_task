from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import func
from flask_cors import CORS,cross_origin
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "preqin.db")


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

db = SQLAlchemy(app)
Session(app)

cors = CORS(app, resources={r"/": {"origins": "*"}})




class Investors_Details(db.Model):
    __tablename__ = 'Investors_Details'
    Investor_Id = db.Column(db.Integer, primary_key=True )
    Investor_Name = db.Column(db.String(50))
    Investory_Type = db.Column(db.String(50))
    Investor_Country = db.Column(db.String(50))
    Investor_Date_Added = db.Column(db.Date())
    Investor_Last_Updated = db.Column(db.Date())
    Investor_Address = db.Column(db.String(250))


class Commitment_Asset_Class(db.Model):
    __tablename__ = 'Commitment_Asset_Class'
    Commitment_Asset_Class_Id = db.Column(db.Integer, primary_key=True )
    Commitment_Asset_Class_Name = db.Column(db.String(50))
    Commitment_Currency =  db.Column(db.String(10))



class Investment_Details(db.Model):
    __tablename__ = 'Investment_Details'
    Investment_Details_Id = db.Column(db.Integer, primary_key=True )
    Investment_Amount = db.Column(db.Integer)

    Commitment_Asset_Class_Id =  db.Column(db.Integer, db.ForeignKey('Commitment_Asset_Class.Commitment_Asset_Class_Id'), nullable=False,index=True)
    Commitment_Asset_Class = db.relationship("Commitment_Asset_Class", backref=db.backref("Commitment_Asset_Class", uselist=False))

    Investor_Id =  db.Column(db.Integer, db.ForeignKey('Investors_Details.Investor_Id'), nullable=False,index=True)
    Investors_Details = db.relationship("Investors_Details", backref=db.backref("Investors_Details", uselist=False))


	


@app.route("/data/investors_details_all",methods = ["GET"])
@cross_origin(origin='127.0.0.1',headers=['Content- Type','Authorization'])
def get_investors_details():
    ret_val = {"DATA": [], "status": "INIT"}
    try:

        ip_data = (db.session.query(
            Investors_Details.Investor_Id,
            func.max(Investors_Details.Investor_Name).label('Investor_Name'),
            func.max(Investors_Details.Investory_Type).label('Investory_Type'),
            func.max(Investors_Details.Investor_Date_Added).label('Investor_Date_Added'),
            func.max(Investors_Details.Investor_Address).label('Investor_Address'),
            func.sum(Investment_Details.Investment_Amount).label('Total_Investment_Amount'),
            )
            .join(Investment_Details,Investment_Details.Investor_Id == Investors_Details.Investor_Id)
            .group_by(Investors_Details.Investor_Id)
            .all()
            )


        for each_data in ip_data:
            ret_val["DATA"].append(
                    {
                    "Investor_Id":each_data.Investor_Id,
                    "Investor_Name":each_data.Investor_Name,
                    "Investory_Type":each_data.Investory_Type,
                    "Investor_Date_Added":each_data.Investor_Date_Added,
                    "Investor_Address":each_data.Investor_Address,
                    "Total_Investment_Amount":each_data.Total_Investment_Amount
                    }
                )
                

    except Exception as e:
        print("SOME ISSUE HAPPENED",str(e))
    else:
        pass
    finally:
        return jsonify(ret_val)


@app.route("/data/investors_details",methods = ["GET"])
@cross_origin(origin='127.0.0.1',headers=['Content- Type','Authorization'])
def get_investors_details_ind():
    ret_val = {"DATA": [], "status": "INIT"}
    investorId = request.args.get("investorId")
    try:

        ip_data = (db.session
            .query(
                Investment_Details.Investment_Details_Id,
                Commitment_Asset_Class.Commitment_Asset_Class_Name,
                Commitment_Asset_Class.Commitment_Currency,
                Investment_Details.Investment_Amount

                )
            .join(Investors_Details,Investors_Details.Investor_Id == Investment_Details.Investor_Id)
            .join(Commitment_Asset_Class,Commitment_Asset_Class.Commitment_Asset_Class_Id == Investment_Details.Commitment_Asset_Class_Id)
            .filter(Investors_Details.Investor_Id == investorId)
            .all()
            )




        for each_data in ip_data:
            ret_val["DATA"].append(
                    {
                    "Investment_Details_Id":each_data.Investment_Details_Id,
                    "Commitment_Asset_Class_Name":each_data.Commitment_Asset_Class_Name,
                    "Commitment_Currency":each_data.Commitment_Currency,
                    "Investment_Amount":each_data.Investment_Amount
                    }
                )
                

    except Exception as e:
        print("SOME ISSUE HAPPENED",str(e))
    else:
        pass
    finally:
        return ret_val


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5500,debug=True)