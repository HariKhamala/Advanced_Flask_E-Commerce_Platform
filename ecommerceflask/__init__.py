import os
import json
from flask import Flask, session, g, render_template, request, redirect, url_for
import razorpay
import sqlite3
from dotenv import load_dotenv

UPLOAD_DIRECTORY = 'imgs'
load_dotenv()

# Razorpay keys (replace with your keys from the Razorpay dashboard)
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_SECRET_KEY = os.getenv('RAZORPAY_SECRET_KEY')
# Use these variables securely in your code

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # Change later
        DATABASE=os.path.join(app.instance_path, 'ecommerce.sqlite'),
        RAZORPAY_KEY_ID=RAZORPAY_KEY_ID,
        RAZORPAY_SECRET_KEY=RAZORPAY_SECRET_KEY
    )

    app.config['UPLOAD_DIRECTORY'] = os.path.join(app.instance_path, UPLOAD_DIRECTORY)
    app.secret_key = b'd93284ufdsaf'

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config['UPLOAD_DIRECTORY'])
    except OSError:
        pass

    # Initialize Razorpay client
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET_KEY))

    @app.before_request
    def load_logged_user():
        from .db import get_db
        user_id = session.get('user_id')
        app.logger.debug(f"user_id = {user_id}")

        if user_id is None:
            g.user = None
        else:
            user = get_db().execute(
                "SELECT * FROM user WHERE id = ?", (user_id,)
            ).fetchone()
            g.user = user['id']
            g.username = user['username']

        app.logger.debug(f"Loading {g.user} as user")

    @app.before_request
    def load_cart():
        from .db import get_db
        cart_id = list()
        db = get_db()

        if g.user is not None:
            cart_id = json.loads(db.execute(
                "SELECT * FROM user WHERE id = ?", (g.user,)
            ).fetchone()['shopping_list'])

        g.cart = list()

        for item_id in cart_id:
            item = db.execute(
                    "SELECT * FROM offer WHERE id = ?", (item_id,)
                    ).fetchone()
            g.cart.append(item)

    # Route for initiating payment
    @app.route('/create_order', methods=['POST'])
    def create_order():
        amount = int(request.form['amount']) * 100  # Amount in paisa
        receipt = f"order_rcptid_{g.user}"

        # Create Razorpay order
        order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "receipt": receipt,
            "payment_capture": 1
        })

        # Send order details to the client
        return render_template('payment.html', order_id=order['id'], amount=amount, key_id=RAZORPAY_KEY_ID)

    # Route for verifying payment
    @app.route('/verify_payment', methods=['POST'])
    def verify_payment():
        try:
            payment_id = request.form['razorpay_payment_id']
            order_id = request.form['razorpay_order_id']
            signature = request.form['razorpay_signature']

            # Verify payment signature
            razorpay_client.utility.verify_payment_signature({
                "razorpay_payment_id": payment_id,
                "razorpay_order_id": order_id,
                "razorpay_signature": signature
            })

            return render_template('success.html')
        except razorpay.errors.SignatureVerificationError:
            return render_template('cancel.html')

    from . import auth
    from . import seller
    from . import index

    app.register_blueprint(auth.bp)
    app.register_blueprint(seller.bp)
    app.register_blueprint(index.bp)

    from . import db
    db.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Load schema.sql if the database is not initialized
    if not os.path.exists('site.db'):
        with sqlite3.connect('site.db') as conn:
            with open('schema.sql', 'r') as f:
                conn.executescript(f.read())

    return app

