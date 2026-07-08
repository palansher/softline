from flask import Blueprint, render_template
from models.product import ProductModel
from decorators import get_current_user

shop_bp = Blueprint("shop", __name__)


@shop_bp.route("/")
def index():
    products = ProductModel.all()
    user     = get_current_user()
    return render_template("index.html", products=products, user=user)
