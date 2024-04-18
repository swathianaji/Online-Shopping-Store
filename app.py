# app.py
from flask import Flask, jsonify, render_template, url_for, redirect, flash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

products = [
    {"id": 1, "name": "Nike Air VaporMax 2021", "price": 100, "availability": 4, "description": "Embrace sustainability with the Nike Air VaporMax 2021, featuring at least 50% recycled content by weight. Its airy, cushioned feel delivers a gravity-defying sensation, perfect for the eco-conscious runner seeking comfort and performance.", "image": "../static/images/products/product-1.jpg"},
    {"id": 2, "name": "Nike ZoomX Vaporfly", "price": 200, "availability": 6, "description": "Experience unmatched speed and responsiveness with the Nike ZoomX Vaporfly. Engineered for record-breaking speed, this elite race shoe features revolutionary ZoomX foam and a carbon fiber plate to propel you towards the finish line faster than ever.", "image": "../static/images/products/product-2.jpg"},
    {"id": 3, "name": "Nike Blazer Mid '77", "price": 300, "availability": 3, "description": "Retro meets modern in the Nike Blazer Mid '77. This classic silhouette blends a vintage mid-cut with lush suede and a timeless design. Perfect for those looking to add a stylish yet comfortable touch to their everyday wear.", "image": "../static/images/products/product-3.jpg"},
    {"id": 4, "name": "Nike Air Force 1", "price": 400, "availability": 5, "description": "A streetwear staple since 1982, the Nike Air Force 1 remains an icon of style and comfort. With its durable foam midsole and pivot point outsole, it's designed to provide premium all-day comfort and agile movement.", "image": "../static/images/products/product-4.jpg"},
    {"id": 5, "name": "Nike Air Max 90", "price": 500, "availability": 10, "description": "The Nike Air Max 90 stays true to its roots with the iconic Waffle sole, stitched overlays, and classic TPU accents. Known for its outstanding cushioning, it's designed to keep you looking and feeling great on your feet.", "image": "../static/images/products/product-5.jpg"},
    {"id": 6, "name": "Nike Glide FlyEase", "price": 600, "availability": 12,"description": "Nike Glide FlyEase offers a seamless blend of comfort and accessibility with its innovative lace-free design. Engineered for easy on and off, it's ideal for athletes of all abilities who don't want to compromise on performance or style.", "image": "../static/images/products/product-6.jpg"},
    {"id": 7, "name": "Nike Zoom Freak", "price": 700,"availability": 1, "description": "Unleash your inner Giannis Antetokounmpo with the Nike Zoom Freak. Designed with two Zoom Air units for explosive movements, this shoe offers a snug fit and multidirectional traction to dominate the court just like the MVP himself.", "image": "../static/images/products/product-7.jpg"},
    {"id": 8, "name": "Nike Air Pegasus", "price": 800, "availability": 2,"description": "The Nike Air Pegasus continues its legacy as a runner's best friend with added comfort and durability. This all-time favorite is designed for every runner, providing long-lasting stability and breathable comfort for extended training.", "image": "../static/images/products/product-8.jpg"},
    {"id": 9, "name": "Nike Air Jordans", "price": 900,"availability": 0, "description": "Step into a legacy of quality and cool with the Nike Air Jordans. These sneakers offer more than just style; they're equipped with state-of-the-art cushioning technology to deliver performance that matches their iconic status.", "image": "../static/images/products/product-1.jpg"},
    # Add more products as needed
]

cart = {
    "items": [],
    "num_items": 0,
    "total_price": 0
}

@app.route('/products', methods=['GET'])
def get_products():
    for i in range(len(products)):
        products[i]["url"] = url_for('get_product', product_id=products[i]["id"])
    return jsonify(products)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', cart=cart)

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((item for item in products if item['id'] == product_id), None)
    return render_template('product.html', product=product, cart=cart)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = next((item for item in products if item['id'] == product_id), None)
    cart["items"].append(product)
    cart["num_items"] += 1
    cart["total_price"] += product["price"]
    return redirect(url_for('get_product', product_id=product_id))


@app.route('/checkout/', methods=['GET'])
def checkout():
    global cart
    unique_items = {}
    orderCanBePlaced = True
    for item in cart["items"]:
        unique_items[item["id"]] = unique_items.get(item["id"], 0) + 1
        if unique_items[item["id"]] > item["availability"]:
            orderCanBePlaced = False

    if not orderCanBePlaced:
        flash("Unable to place order!", category="warning")
        return redirect(url_for('home'))

    for item_id, count in unique_items.items():
        ind = products.index(next((item for item in products if item['id'] == item_id), None))
        products[ind]["availability"] -= count
    
    cart = {
        "items": [],
        "num_items": 0,
        "total_price": 0
    }

    flash("Order placed successfully!", category="success")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
