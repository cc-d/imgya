import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .db import *
from .functions import *

bp = Blueprint('pages', __name__)

@bp.route('/')
def index():
	return render_template('base.html')