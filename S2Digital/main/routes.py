import re
from flask import Blueprint, render_template, request, jsonify, current_app
from ..extensions import db
from ..models import Contact
from datetime import datetime

bp = Blueprint("main", __name__, template_folder="templates")

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
MAX_NAME = 120
MAX_EMAIL = 200
MAX_MESSAGE = 2000
MAX_MOBILE = 40
MOBILE_RE = re.compile(r'^[+\d().\-\s]{7,40}$')

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/products")
def products():
    return render_template("products.html")

@bp.route("/services")
def services():
    return render_template("services.html")

@bp.route("/contact")
def contact():
    return render_template("contact.html")

@bp.route("/contact/submit", methods=["POST"])
def contact_submit():
    try:
        # accept JSON or form POST
        data = request.get_json() if request.is_json else request.form
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        mobile = (data.get("mobile") or "").strip()
        message = (data.get("message") or "").strip()

        # Basic validations
        if not name or not email or not message:
            return jsonify({"ok": False, "error": "name, email and message required"}), 400
        if len(name) > MAX_NAME:
            return jsonify({"ok": False, "error": "name too long"}), 400
        if len(email) > MAX_EMAIL or not EMAIL_RE.match(email):
            return jsonify({"ok": False, "error": "invalid email"}), 400
        if len(message) > MAX_MESSAGE:
            return jsonify({"ok": False, "error": "message too long"}), 400

        # mobile (optional) validation
        if mobile:
            if len(mobile) > MAX_MOBILE:
                return jsonify({"ok": False, "error": "mobile number too long"}), 400
            if not MOBILE_RE.match(mobile):
                return jsonify({"ok": False, "error": "invalid mobile number"}), 400
            # basic XSS guard
            if '<' in mobile or '>' in mobile:
                return jsonify({"ok": False, "error": "invalid characters in mobile"}), 400

        # Save
        c = Contact(name=name, email=email, mobile=mobile or None, message=message, created_at=datetime.utcnow())
        db.session.add(c)
        db.session.commit()
        return jsonify({"ok": True}), 201

    except Exception as exc:
        # log full exception to server console / logs
        current_app.logger.exception("contact_submit failed")
        # return safe JSON error (expose details only when DEBUG)
        if current_app.config.get("DEBUG"):
            return jsonify({"ok": False, "error": str(exc)}), 500
        return jsonify({"ok": False, "error": "internal server error"}), 500

# --- Simple admin view to list contact inquiries ---
@bp.route("/admin")
def admin():
    """List saved contact inquiries. Protect with a simple key:
       /admin?key=YOUR_KEY
    """
    key = request.args.get("key", "")
    if key != current_app.config.get("ADMIN_KEY"):
        return "Forbidden", 403

    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template("admin.html", contacts=contacts)

@bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@bp.route("/compliance")
def compliance():
    return render_template("compliance.html")

@bp.route("/cookies")
def cookies():
    return render_template("cookies.html")

@bp.route("/security")
def security():
    return render_template("security.html")

# --- New informational pages for footer links ---
@bp.route("/our-story")
def our_story():
    return render_template("our_story.html")

@bp.route("/life-at")
def life_at():
    return render_template("life_at.html")

@bp.route("/careers")
def careers():
    return render_template("careers.html")

@bp.route("/contact-us")
def contact_us():
    # reuse existing contact page
    return render_template("contact.html")

@bp.route("/blog")
def blog():
    return render_template("blog.html")

@bp.route("/resources")
def resources():
    return render_template("resources.html")

@bp.route("/industry/financial-services")
def industry_financial():
    return render_template("industry_financial.html")

@bp.route("/industry/banking-insurance")
def industry_banking():
    return render_template("industry_banking.html")

@bp.route("/industry/telecommunication")
def industry_telecom():
    return render_template("industry_telecom.html")

@bp.route("/industry/technology")
def industry_technology():
    return render_template("industry_technology.html")