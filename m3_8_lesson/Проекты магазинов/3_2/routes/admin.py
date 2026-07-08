from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash)
from decorators import admin_required, get_current_user
from models.order import OrderModel
from models.user import UserModel

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def dashboard():
    user   = get_current_user()
    orders = OrderModel.all_with_users()
    stats  = OrderModel.stats()
    return render_template(
        "admin/dashboard.html",
        orders=orders, stats=stats, user=user,
    )


@admin_bp.route("/order/<int:order_id>")
@admin_required
def order_detail(order_id: int):
    user  = get_current_user()
    order = OrderModel.find_by_id_with_user(order_id)
    if not order:
        flash("Заказ не найден", "danger")
        return redirect(url_for("admin.dashboard"))
    items = OrderModel.items_for_order(order_id)
    return render_template(
        "admin/order_detail.html",
        order=order, items=items, user=user,
    )


@admin_bp.route("/order/<int:order_id>/status", methods=["POST"])
@admin_required
def update_status(order_id: int):
    new_status = request.form["status"]
    OrderModel.update_status(order_id, new_status)
    flash(f"Статус заказа #{order_id} → \"{new_status}\"", "success")
    return redirect(url_for("admin.order_detail", order_id=order_id))


@admin_bp.route("/users")
@admin_required
def users():
    user       = get_current_user()
    users_list = UserModel.all_with_stats()
    return render_template(
        "admin/users.html",
        users_list=users_list, user=user,
    )
