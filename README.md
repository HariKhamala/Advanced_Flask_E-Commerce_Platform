# 🛒 Advanced E-Commerce Website (Flask)

This repository contains a **full-featured E-Commerce Platform** developed using **Flask** with secure authentication, payment integration, and advanced search capabilities.  

---

## 🚀 Features

### 👤 User Roles
- **Buyers**  
  - Register/Login with secure session management  
  - Browse products, add to cart, view cart, and checkout  
  - Secure payment via **Razorpay Gateway** (order creation, payment verification, success/failure handling)  
  - Personalized product recommendations (based on cart & recent searches)  

- **Sellers**  
  - Register/Login as seller  
  - Upload products with image, name, price, and description  
  - Manage product listings  

---

### 🔐 Security
- User authentication & session management  
- Secure cart persistence  
- Payment verification with Razorpay  

---

### 🛠️ Advanced Functionalities
- **Product Recommendations**: Smart suggestions based on user activity  
- **NLP-Based Search** (Powered by NLTK + FuzzyWuzzy)  
  - Tokenization & stopword removal for better matching  
  - Fuzzy string matching for similar terms  
  - Numeric queries (e.g., price filters) handled directly  

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)  
- **Database**: SQLite  
- **Frontend**: HTML5, CSS3, JavaScript  
- **Payment**: Razorpay Integration  
- **NLP**: NLTK (tokenization, stopwords), FuzzyWuzzy (string similarity)  

---
