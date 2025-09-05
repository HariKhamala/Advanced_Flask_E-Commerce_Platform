
from flask import request, flash, redirect, url_for, g, session, render_template, Blueprint, current_app, send_from_directory, current_app
import json
import razorpay
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.data.path.append('C:\\Users\\HP\\nltk_data')
nltk.download('stopwords', download_dir='C:\\Users\\HP\\nltk_data')
nltk.download('punkt', download_dir='C:\\Users\\HP\\nltk_data')
nltk.download('punkt_tab', download_dir='C:\\Users\\HP\\nltk_data')

bp = Blueprint('main', __name__)

@bp.route('/img/<name>')
def img(name:str):
    return send_from_directory(current_app.config['UPLOAD_DIRECTORY'], name)

def get_recommended_products(user_id):
    from .db import get_db
    db = get_db()

    # Example collaborative filtering logic based on shopping lists
    user_data = db.execute(
        "SELECT shopping_list FROM user WHERE id = ?", (user_id,)
    ).fetchone()

    # Deduplicate shopping list
    shopping_list = list(set(json.loads(user_data['shopping_list']))) if user_data and user_data['shopping_list'] else []

    # Fetch user's recent search queries
    recent_searches = db.execute(
        "SELECT search_query FROM search_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5", 
        (user_id,)
    ).fetchall()

    search_terms = [row['search_query'] for row in recent_searches]
    search_filter = f"%{'%'.join(search_terms)}%" if search_terms else None

    # Get all product IDs
    all_product_ids = [row['id'] for row in db.execute("SELECT id FROM offer").fetchall()]
    
    # Products not in the user's cart
    products_not_in_cart = [pid for pid in all_product_ids if pid not in shopping_list]

    if search_filter:
        # Recommend products matching recent searches and not in cart
        recommended = db.execute(
            """
            SELECT * FROM offer 
            WHERE id IN ({}) 
            AND offername LIKE ? 
            LIMIT 5
            """.format(",".join(map(str, products_not_in_cart))),
            (search_filter,)
        ).fetchall()
    else:
        # Default behavior: recommend random products not in the cart
        recommended = db.execute(
            """
            SELECT * FROM offer 
            WHERE id IN ({}) 
            ORDER BY RANDOM() 
            LIMIT 5
            """.format(",".join(map(str, products_not_in_cart)))
        ).fetchall()

    # Fallback: Show random products if no recommendations are found(if all are in cart)
    if not recommended:
        recommended = db.execute(
            "SELECT * FROM offer ORDER BY RANDOM() LIMIT 5"
        ).fetchall()

    return recommended


    

from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

@bp.route("/")
def home():
    from .db import get_db
    db = get_db()

    search = request.args.get('search')
    user_id = g.user if g.user else None

    if search:
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(search.lower())
        keywords = [word for word in tokens if word not in stop_words]

        # Advanced NLP-enhanced search
        query = "SELECT * FROM offer WHERE " + " OR ".join(["offername LIKE ?"] * len(keywords))
        params = [f"%{keyword}%" for keyword in keywords]
        offers_nlp = db.execute(query, params).fetchall()

        # Fuzzy search for numeric queries (price match)
        all_offers = db.execute("SELECT * FROM offer").fetchall()
        search_results_fuzzy = []

        if search.isdigit():  # Handle numeric queries
            search_results_fuzzy = [
                offer for offer in all_offers if int(search) == int(offer['price'])
            ]
        else:  # Handle text queries
            for offer in all_offers:
                similarity = fuzz.partial_ratio(search.lower(), offer['offername'].lower())
                if similarity > 70:  # Adjust threshold as needed
                    search_results_fuzzy.append(offer)

        # Combine results from both search methods
        offers = list({offer['id']: offer for offer in offers_nlp + search_results_fuzzy}.values())  # Remove duplicates by 'id'
    else:
        offers = db.execute("SELECT * FROM offer").fetchall()

    recommendations = get_recommended_products(user_id) if user_id else []

    return render_template(
        "index.html", offers=offers, recommendations=recommendations
    )



@bp.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if g.user is None:
        flash("You must be logged in to checkout.")
        return redirect(url_for('auth.login'))

    from .db import get_db
    db = get_db()

    # Fetch the user's shopping list
    user_data = db.execute(
        "SELECT shopping_list FROM user WHERE id = ?", (g.user,)
    ).fetchone()

    shopping_list = []
    if user_data and user_data['shopping_list']:
        shopping_list = json.loads(user_data['shopping_list'])
        # Fetch product details for each item in the shopping list
    products = []
    if shopping_list:
        for product_id in shopping_list:
            product = db.execute(
                "SELECT * FROM offer WHERE id = ?", (product_id,)
            ).fetchone()
            if product:
                products.append(product)

    # Handle POST request for payment
    if request.method == 'POST':
        if not products:
            flash("Your cart is empty.")
            return redirect(url_for('main.home'))

        amount = sum(item['price'] * 100 for item in g.cart)
        razorpay_order = razorpay.Client(
            auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_SECRET_KEY'])
        ).order.create({
            'amount': amount,
            'currency': 'INR',
            'receipt': f"order_rcptid_{g.user}",
            'payment_capture': 1
        })
        return render_template('payment.html', order_id=razorpay_order['id'], amount=amount, key_id=current_app.config['RAZORPAY_KEY_ID'])

    return render_template('checkout.html', products=products)




@bp.route('/product/<int:id>', methods=['GET', 'POST'])
def product(id):

    from .db import get_db
    db = get_db()

    if request.method == 'POST':
        user = get_db().execute(
                "SELECT * FROM user WHERE id = ?", (g.user,)
                ).fetchone()

        # Load the current shopping list without deduplication
        current_products = json.loads(user['shopping_list']) if user['shopping_list'] else []
        current_products.append(id)


        # Update user's shopping list
        db.execute(
            "UPDATE user SET shopping_list = json(?) WHERE id = ?",
            (json.dumps(current_products), g.user,)
        )
        db.commit()

        


    offer = get_db().execute(
            "SELECT * FROM offer WHERE id = ?", (id,)
            ).fetchone()

    return render_template('product.html', product=offer)

@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/search', methods=['POST'])
def search():
    search_query = request.form['bsearch']
    if g.user:
        from .db import get_db
        db = get_db()
        db.execute(
            "INSERT INTO search_history (user_id, search_query) VALUES (?, ?)",
            (g.user, search_query)
        )
        db.commit()
    return redirect(url_for('main.home', search=search_query))


@bp.route('/checkout/success')
def checkout_success():
    return render_template('success.html')

@bp.route('/checkout/cancel')
def checkout_cancel():
    return render_template('cancel.html')
@bp.route('/verify_payment', methods=['POST'])
def verify_payment():
    payment_data = request.form
    try:
        razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_SECRET_KEY'])).utility.verify_payment_signature(payment_data)
        return redirect(url_for('main.checkout_success'))
    except razorpay.errors.SignatureVerificationError:
        return redirect(url_for('main.checkout_cancel'))
@bp.route('/remove_from_cart/<int:id>', methods=['POST'])
def remove_from_cart(id):
    if g.user is None:
        flash("You must be logged in to modify your cart.")
        return redirect(url_for('auth.login'))

    from .db import get_db
    db = get_db()

    # Fetch the user's current shopping list
    user_data = db.execute(
        "SELECT shopping_list FROM user WHERE id = ?", (g.user,)
    ).fetchone()

    if user_data and user_data['shopping_list']:
        shopping_list = json.loads(user_data['shopping_list'])

        # Remove the product ID if it exists in the list
        if id in shopping_list:
            shopping_list.remove(id)

        # Update the database with the modified shopping list
        db.execute(
            "UPDATE user SET shopping_list = ? WHERE id = ?",
            (json.dumps(shopping_list), g.user)
        )
        db.commit()

        flash("Product removed from your cart.")
    else:
        flash("Your cart is empty or the product is not in your cart.")

    return redirect(url_for('main.checkout'))
 