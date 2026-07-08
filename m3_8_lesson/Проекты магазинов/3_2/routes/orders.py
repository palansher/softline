from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash)
from decorators import login_required, get_current_user
from services.order_service import OrderService
from models.order import OrderModel

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/create", methods=["POST"])
@login_required
def create():
    user  = get_current_user()
    phone = request.form.get("phone", user.get("phone", ""))
    try:
        order_id = OrderService.create_from_cart(user["id"], phone)
        flash(f"Заказ #{order_id} оформлен!", "success")
    except ValueError as exc:
        flash(str(exc), "warning")
        return redirect(url_for("cart.view"))
    except Exception as exc:
        flash(f"Ошибка: {exc}", "danger")
    return redirect(url_for("orders.my_orders"))


@orders_bp.route("/")
@login_required
def my_orders():
    user   = get_current_user()
    orders = OrderModel.for_user(user["id"])
    return render_template("orders.html", orders=orders, user=user)
