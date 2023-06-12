from flask import Blueprint
from helper import NestableBlueprint
# 一级蓝图
stock = NestableBlueprint('stock', __name__, url_prefix='/stock')
# 二级蓝图
from app.blue.stock.get_data import get_data as get_data
stock.register_blueprint(get_data, url_prefix="/get_data")



