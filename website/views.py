from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Item, Cart
from . import db


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        size = request.form.get('size')
        price = float(request.form.get('price'))

        new_item = Item(name=name, description=description, size=size, price=price)
        db.session.add(new_item)
        db.session.commit()

        flash('Przedmiot został dodany!', category='success')

    return render_template('home.html')


@views.route('/show_items')
def show_items():
    items = Item.query.all()  # Pobieramy wszystkie przedmioty z bazy danych
    return render_template('show_items.html', items=items)  # Przekazujemy je do szablonu


@views.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item_to_delete = Item.query.get_or_404(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    flash('Przedmiot został usunięty!', category='success')
    return render_template('show_items.html')


@views.route('/show_users')
def show_users():
    users = User.query.all()
    return render_template('show_users.html', users=users)


@views.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    items = Item.query.all()  # Pobieramy wszystkie przedmioty z bazy danych

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        quantity = request.form.get('quantity', type=int)
        existing_item = Cart.query.filter_by(user_id=current_user.id, item_id=item_id).first()

        if existing_item:
            existing_item.quantity += quantity
        else:
            new_cart_item = Cart(user_id=current_user.id, item_id=item_id, quantity=quantity)
            db.session.add(new_cart_item)

        db.session.commit()
        flash('Item updated in cart', category='success')

    cart_items_in_cart = Cart.query.filter_by(user_id=current_user.id).all()  # Pobieramy elementy, które są już w koszyku

    cart_items = []
    for cart_item in cart_items_in_cart:
        item = Item.query.get(cart_item.item_id)  # Zauważ zmienioną linię. Zamiast 'id', teraz jest 'item_id'.
        cart_items.append({
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'size': item.size,
            'quantity': cart_item.quantity
        })

    return render_template('cart.html', cart_items=cart_items, items=items, current_user=current_user)  # Przekazujemy 'cart_items', a nie 'cart_items_in_cart'.

