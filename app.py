from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Mahsulotlar ro'yxati
products = [
    {'id': 1, 'name': 'Musqaymoq', 'description': 'Yangi va mazali musqaymoq, eng yaxshi sifatda.', 'price': 5000, 'category': 'Meva va Savzavotlar', 'image_url': 'https://example.com/musqaymoq.jpg'},
    {'id': 2, 'name': 'Telefon', 'description': 'Smartphone', 'price': 500000, 'category': 'Elektronika', 'image_url': '/static/images/phone.jpg'},
    {'id': 3, 'name': 'Kurtka', 'description': 'Kiyim', 'price': 150000, 'category': 'Kiyimlar', 'image_url': '/static/images/jacket.jpg'},
    {'id': 4, 'name': 'Kompyuter', 'description': 'Elektronika', 'price': 1500000, 'category': 'Elektronika', 'image_url': '/static/images/computer.jpg'}
]

# Kategoriyalar
categories = ["Asbob-uskunalar", "Kiyimlar", "Mevalar", "Elektronika"]

# Rasmni saqlash uchun papka
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rasmning kengaytmasi tekshiruvi
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # URLdan category parametrini olish
    category = request.args.get('category')
    
    # Agar category bo'lsa, faqat shu kategoriya bo'yicha mahsulotlar ko'rsatiladi
    if category:
        filtered_products = [p for p in products if p['category'] == category]
    else:
        filtered_products = products  # Agar kategoriya tanlanmasa, barcha mahsulotlar ko'rsatiladi
    
    return render_template('index.html', products=filtered_products, categories=categories)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']  # Kategoriyani olish

        # Rasmni yuklash
        if 'image' not in request.files:
            return "No file part"
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_url = url_for('static', filename=f'images/{filename}')
        else:
            image_url = ''  # Agar rasm bo'lmasa

        new_product = {
            'id': len(products) + 1,
            'name': name,
            'description': description,
            'price': int(price),
            'category': category,  # Kategoriya qo'shildi
            'image_url': image_url  # Rasm URL qo'shildi
        }
        products.append(new_product)
        return redirect(url_for('index'))
    
    return render_template('add_product.html', categories=categories)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    
    if request.method == 'POST':
        product['name'] = request.form['name']
        product['description'] = request.form['description']
        product['price'] = request.form['price']
        product['category'] = request.form['category']  # Kategoriyani yangilash
        
        # Yangi rasmni yuklash
        if 'image' in request.files and request.files['image']:
            file = request.files['image']
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                product['image_url'] = url_for('static', filename=f'images/{filename}')
        
        return redirect(url_for('index'))
    
    return render_template('edit_product.html', product=product, categories=categories)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return redirect(url_for('index'))

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
