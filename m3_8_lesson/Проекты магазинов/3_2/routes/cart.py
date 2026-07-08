from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash)
from decorators import login_required, get_current_user
from services.cart_service import CartService
from models.cart import CartModel

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add(product_id: int):
    user = get_current_user()
    qty  = int(request.form.get("quantity", 1))
    CartService.add_product(user["id"], product_id, qty)
    flash("Товар добавлен в корзину!", "success")
    return redirect(url_for("shop.index"))


@cart_bp.route("/")
@login_required
def view():
    user = get_current_user()
    data = CartService.get_cart_data(user["id"])
    return render_template("cart.html", user=user, **data)


@cart_bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove(item_id: int):
    user = get_current_user()
    CartModel.remove_item(item_id, user["id"])
    flash("Товар удалён из корзины", "info")
    return redirect(url_for("cart.view"))


@cart_bp.route("/update/<int:item_id>", methods=["POST"])
@login_required
def update(item_id: int):
    user = get_current_user()
    qty  = int(request.form.get("quantity", 1))
    if qty <= 0:
        CartModel.remove_item(item_id, user["id"])
    else:
        CartModel.update_item(item_id, qty, user["id"])
    return redirect(url_for("cart.view"))
