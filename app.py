from flask import Flask,jsonify,request,session
from flask_bcrypt import Bcrypt
from models import db, user,coupon,coupon_user
from flask_cors import CORS,cross_origin
from flask_jwt_extended import create_access_token,JWTManager,get_jwt,get_jwt_identity,unset_jwt_cookies,jwt_required
from datetime import timedelta,datetime,timezone
from flask_mail import Mail,Message
import random




app=Flask(__name__)
aws_rds_endpoint = 'fintech-dev.cbnt8xhvtzh0.ap-southeast-1.rds.amazonaws.com'
username = 'admin'
password = 'CknvMh74qeFv'
aws_rds_uri = f'mysql+pymysql://{username}:{password}@{aws_rds_endpoint}:3306/fintech_dev'
app.config['SECRET_KEY']='shivam_1101'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456789@localhost/demo'
app.config['SQLALCHEMY_DATABASE_URI']=aws_rds_uri
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'btech.mshivam@gmail.com '
app.config['MAIL_PASSWORD'] = 'ajsshrnhcygyscch'
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)
verification_otp = {}
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(hours=1)
jwt=JWTManager(app)
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO=True

bcrypt=Bcrypt(app)
CORS(app,supports_credentials=True)
db.init_app(app)


with app.app_context():
    db.create_all()

@app.route("/logintoken",methods=["POST"])
def create_token():
    email=request.json.get("email",None)
    password=request.json.get("password",None)

    users=user.query.filter_by(email=email).first()

    if users is None:
        return jsonify({"error":"Unauthorised Access"}),401
    
    if not bcrypt.check_password_hash(users.password,password):
        return jsonify({"error":"Unauthorised"}),401
    
    acces_token=create_access_token(identity=email)
    # response={"access_token":acces_token}

    return jsonify({
        "email":email,
        "access_token":acces_token
    })



@app.route("/signup",methods=["POST"])
def signup():
    email=request.json["email"]
    password=request.json["password"]
    name=request.json["name"]
    phone_number=request.json["phone_number"]
    gender=request.json["gender"]

    user_exist=user.query.filter_by(email=email).first() is not None
    if user_exist:
        return jsonify({"Email Already Exist"}),409
    
    hashed_password=bcrypt.generate_password_hash(password)
    new_user=user(email=email,password=hashed_password,name=name,gender=gender,phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()

    session["user_id"]=new_user.id


    return jsonify({
        "id":new_user.id,
        "email": new_user.email,
        "name":new_user.name,
        "phone_number":new_user.phone_number,
        "gender":new_user.gender
    })
@app.route("/send-otp", methods=["POST"])
def send_verification_otp():
    email = request.json.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Generate a 4-digit OTP
    otp = str(random.randint(1000, 9999))

    # Send the OTP to the user's email
    msg = Message('Email Verification OTP', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Your verification OTP is: {otp}'
    mail.send(msg)

    # Set an expiration time for the OTP (5 minutes)
    otp_expiration_time = datetime.now() + timedelta(minutes=5)
    verification_otp[otp] = {'email': email, 'expiration_time': otp_expiration_time}

    return jsonify({"message": "OTP sent successfully"})

@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    received_otp = request.json.get("otp")

    if received_otp in verification_otp:
        # Check if the OTP is still valid (not expired)
        if datetime.now() <= verification_otp[received_otp]['expiration_time']:
            # Mark the user's email as verified in your database (You should implement this part)
            email = verification_otp[received_otp]['email']

            # Remove the OTP from the verification_otp dictionary
            del verification_otp[received_otp]

            return jsonify({"message": "Email verification successful"})
    
    # Log the received OTP and expiration time to help with debugging
    app.logger.debug(f"Received OTP: {received_otp}")
    if received_otp in verification_otp:
        app.logger.debug(f"Expiration Time: {verification_otp[received_otp]['expiration_time']}")

    return jsonify({"error": "Email verification failed"}), 400


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp=get_jwt()["exp"]
        now=datetime.now(timezone.utc)
        target_timestamp=datetime.timestamp(now+timedelta(minutes=30))
        if target_timestamp>exp_timestamp:
            access_token=create_access_token(get_jwt_identity())
            data=response.get_json()
            if type(data) is dict:
                data["access_token"]=access_token
                response.data=json.dumps(data)
        return response
    except (RuntimeError,KeyError):
        return response
@app.route("/logout",methods=["POST"])
def logout():
    response=jsonify({"message":"Logout Successfully"})
    unset_jwt_cookies(response)
    return response

@app.route("/profile/<email>", methods=["GET", "POST"])
def my_profile(email):
    if request.method == "GET":
        users = user.query.filter_by(email=email).first()
        if users:
            user_data = {
                "name": users.name,
                "email": users.email,
                "phone_number": users.phone_number
            }
            return jsonify(user_data), 200
        return jsonify({"error": "user details not found"}), 400

    if request.method == "POST":
        data = request.json
        users = user.query.first()
        if users:
            users.name = data.get("name")
            users.email = data.get("email")
            users.phone_number = data.get("phone_number")
            db.session.commit()
            return jsonify({"message": "user data updated"}), 200
        return jsonify({"error": "error updating data"}), 400


        




@app.route("/coupons",methods=["GET"])
def Coupon():
    country=request.args.get('country',default="All")
    print("recieved request for country",country)


    db_session=db.session    
    if country=="All":
        coupons=db_session.query(coupon).all()
    else:
         coupons = db_session.query(coupon).filter_by(region=country).all()
    
    # coupons=db_session.query(coupon).filter_by(region="India").all()
    # coupons=db.session.execute(db.select(coupon).filter_by(region="India")).scalars().all()
    data=[]
    for coup in coupons:
        
        data.append({"index":coup.index,
            "merchant_title":coup.merchant_title, 
            "offer_title":coup.offer_title,
            "description":coup.description,
            "coupon_code":coup.coupon_code,
            "verified":coup.verified,
            "region":coup.region,
            "title_logo":coup.title_logo,
            "type_of_voucher":coup.type_of_voucher})
    
    return jsonify(data)
@app.route('/coupon_user', methods=["GET", "POST"])
def coupon_users():
    if request.method == "GET":
        email = request.args.get("email")
        print("Received Email:", email)
        # coupon_code = request.args.get("coupon_code")  # Remove this line

        if email is None:
            return jsonify({"error": "Missing required parameters"})

        # Check if the coupon code has been used by the user
        used_coupons = db.session.query(coupon_user).filter_by(email=email).all()

        used_coupons_data = [
            {
                "offer_title": coupon.offer_title,
                "coupon_code": coupon.coupon_code,
                "points_earned":coupon.points_earned
            }
            for coupon in used_coupons
        ]

        return jsonify(used_coupons_data)

        # if coupon_used:
        #     return jsonify({"used": True})
        # else:
        #     return jsonify({"used": False})

    elif request.method == "POST":
        data = request.json
        print("Received JSON Data:", data)
        email = data.get('email')
        offer_title = data.get('offer_title')
        coupon_code = data.get('coupon_code')
        category = data.get('category')  
        points_earned = data.get('points_earned')

        print("Received Data (POST):")
        print("Email:", email)
        print("Offer Title:", offer_title)
        print("Coupon Code:", coupon_code)
        print("Category:", category)
        print("Points Earned:", points_earned)

        if email is None or offer_title is None or coupon_code is None:
            return jsonify({"error": "Missing required parameters"})

        new_coup = coupon_user(email=email, offer_title=offer_title, coupon_code=coupon_code,category=category,points_earned=points_earned)
        db.session.add(new_coup)
        db.session.commit()
        session["coupon_user_id"] = new_coup.id

        return jsonify({
            "id": new_coup.id,
            "email": new_coup.email,
            "offer_title": new_coup.offer_title,
            "coupon_code": new_coup.coupon_code,
            "category":new_coup.category,
            "points_earned":new_coup.points_earned
        })







            



if __name__=="__main__":
    app.run(debug=True)


