<h1>Ecommerce</h1>

### 📝 About <br>
<p>
This project is a comprehensive e-commerce platform that caters to both buyers and sellers.This project aims to create a fully functional online store where users can browse products, add them to their shopping cart, and make secure payments via Razorpay. Sellers can list products for sale. The platform employs advanced features like personalized recommendations and NLP-enhanced search for a seamless user experience.
</p>

### 📚 Features <br>

#### Buyer Features:

* **Product Catalog**: Users can view a list of products available for purchase. Each product is displayed with details like name, price and an image.

+ **Product Search**: Enhanced search functionality using NLP and fuzzy matching for accurate results.
 
+ **Personalized Recommendations**: Suggests products based on shopping behavior and search history.

* **Shopping Cart**: Users can add products to their shopping cart while browsing. They can also review and remove them during checkout.

- **Checkout**: Users can proceed to the checkout page to review their order and make a payment.

- **Secure Payments**: Complete payments via Razorpay.

#### Seller Features:

+ **Product Upload**: Add new products with name, price, and image.

#### General Features:

- **User Authentication**: Register and log in as either a buyer or a seller.

- **Role Differentiation**: Separate functionalities for buyers and sellers.

- **Seamless Navigation**: Clean interface for accessing features.

<!--IMGs-->

### 🔧 Technologies<br>

#### Frontend:
- **HTML5**: Structuring web pages.
- **CSS3**: Styling and layout.
- **JavaScript**: Interactivity and dynamic content.

#### Backend:
- **Python**: Server-side programming.
- **Flask**: Web framework for routing and logic.
- **SQLite**: Lightweight database for data persistence.

#### Payment Integration:
- **Razorpay**: Secure payment processing.

#### Natural Language Processing (NLP):
- **NLTK**: Tokenization and stopword removal.
- **FuzzyWuzzy**: Fuzzy string matching for search enhancement.

---

### 📂 Database Schema

#### `user` Table:
| Column         | Type    | Description                              |
|----------------|---------|------------------------------------------|
| `id`           | INTEGER | Primary key, auto-incremented.           |
| `username`     | TEXT    | Unique name of the user.                 |
| `email`        | TEXT    | Unique email of the user.                |
| `userType`     | INTEGER | 1 for Buyer, 2 for Seller.               |
| `password`     | TEXT    | Password for authentication.             |
| `shopping_list`| JSON    | List of product IDs for buyers.          |

#### `offer` Table:
| Column       | Type    | Description                              |
|--------------|---------|------------------------------------------|
| `id`         | INTEGER | Primary key, auto-incremented.           |
| `username`   | TEXT    | Seller's username.                       |
| `price`      | FLOAT   | Price of the product.                    |
| `offername`  | TEXT    | Name of the product.                     |
| `image`      | TEXT    | Path to the product image.               |

#### `search_history` Table:
| Column         | Type    | Description                              |
|----------------|---------|------------------------------------------|
| `id`           | INTEGER | Primary key, auto-incremented.           |
| `user_id`      | INTEGER | ID of the user performing the search.    |
| `search_query` | TEXT    | The entered search query.                |
| `timestamp`    | DATETIME| Time of the search (auto-generated).     |

---

### 🔥 Advanced Features 

1. **Razorpay Payment Integration**:
   - Create orders and process secure payments.
   - Handle success and failure scenarios with user-friendly redirection.

2. **Personalized Recommendations**:
   - Suggests products not already in the user's cart, based on shopping lists and search history.

3. **NLP-Enhanced Search**:
   - Processes queries using tokenization, stopword removal, and fuzzy matching.
   - Handles both textual and numeric search queries for relevant results.

---

### 🛠️ Workflow

#### Initial Landing Page:
- Displays navigation options: "Home," "Seller," "Cart," and "Profile."
- Redirects unauthenticated users to login or register pages.

#### Buyer Workflow:
- Add products to a shopping cart, review and during checkout, and complete purchases.
- View personalized recommendations based on shopping behavior and search queries.

#### Seller Workflow:
- Upload products with name, price, and image for buyers to purchase.

---

### 🤝 Collaborators <br>
Hari Khamala S ([GitHub](https://github.com/HariKhamala)) <br>

### 🎯 Project status <br>
Finished

### [See project](https://github.com/HariKhamala/ecommerce-flask.git)
