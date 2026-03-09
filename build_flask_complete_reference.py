from __future__ import annotations

from collections import defaultdict
from html import escape
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
OUTFILE = ROOT / "flask_complete_reference.html"

TITLE = "Flask Complete Reference"
SUBTITLE = "Flask 3.x from HTTP and WSGI first principles to testing, extensions, and production deployment"

LAYER_NAMES = {
    0: "Web & Flask Foundations",
    1: "Routing",
    2: "Request & Response",
    3: "Templates",
    4: "Data & Persistence",
    5: "Forms & Validation",
    6: "Sessions & Authentication",
    7: "REST APIs",
    8: "Async Flask",
    9: "Extensions Deep-Dive",
    10: "Testing",
    11: "Performance, Security & Production",
    12: "Advanced Patterns",
}

NAV_LABELS = {
    0: "Layer 0: Web & Flask Foundations",
    1: "Layer 1: Routing",
    2: "Layer 2: Request & Response",
    3: "Layer 3: Templates",
    4: "Layer 4: Data & Persistence",
    5: "Layer 5: Forms & Validation",
    6: "Layer 6: Sessions & Authentication",
    7: "Layer 7: REST APIs",
    8: "Layer 8: Async Flask",
    9: "Layer 9: Extensions Deep-Dive",
    10: "Layer 10: Testing",
    11: "Layer 11: Performance, Security & Production",
    12: "Layer 12: Advanced Patterns",
}

REFERENCE_SECTIONS = [
    ("dependency-table", "Concept DAG & Dependency Table"),
    ("wsgi-flow", "WSGI Request Flow"),
    ("context-stack", "Application & Request Context Stack"),
    ("ecosystem-map", "Flask Extension Ecosystem"),
    ("quick-reference", "Quick Reference"),
]

CLUSTER_CLASS = {
    "foundation": "cluster-foundation",
    "routing": "cluster-routing",
    "request": "cluster-request",
    "templates": "cluster-templates",
    "data": "cluster-data",
    "forms": "cluster-forms",
    "auth": "cluster-auth",
    "rest": "cluster-rest",
    "async": "cluster-async",
    "extensions": "cluster-extensions",
    "testing": "cluster-testing",
    "production": "cluster-production",
    "architecture": "cluster-architecture",
}

OTHER_LABELS = {
    "foundation": "Django / FastAPI",
    "routing": "Django",
    "request": "Django",
    "templates": "Django",
    "data": "Django",
    "forms": "Django",
    "auth": "Django",
    "rest": "FastAPI",
    "async": "Quart / FastAPI",
    "extensions": "Django",
    "testing": "Django",
    "production": "Django",
    "architecture": "Django",
}

CLUSTER_COMPARISON = {
    "foundation": (
        "You handle sockets, request parsing, and response bytes directly, so every bug starts at the transport boundary.",
        "Flask keeps HTTP visible but replaces protocol plumbing with request, response, and routing primitives.",
        "Django starts higher with more structure; FastAPI starts API-first with type-driven request validation.",
    ),
    "routing": (
        "Routing is a chain of if/elif checks against PATH_INFO and REQUEST_METHOD.",
        "Flask stores URL rules in Werkzeug's URL map and dispatches named endpoints cleanly.",
        "Django centralizes routes in URLconf and names them for reverse resolution.",
    ),
    "request": (
        "You read values from the WSGI environ and build headers/status manually.",
        "Flask exposes context-local proxies backed by Werkzeug Request and Response objects.",
        "Django gives comparable request and response objects but with more framework conventions around them.",
    ),
    "templates": (
        "HTML is assembled with string concatenation or a manually configured template engine.",
        "Flask ships with Jinja2 and leaves the template architecture mostly to you.",
        "Django ships its own template language and stronger defaults around project layout.",
    ),
    "data": (
        "You open connections, manage transactions, map rows, and clean up resources yourself.",
        "Flask lets you choose raw SQL, SQLAlchemy, or other stores and wire them into the app factory.",
        "Django includes an integrated ORM, migrations, and admin assumptions from the start.",
    ),
    "forms": (
        "Validation, coercion, redisplay, and CSRF checks are all hand-rolled.",
        "Flask-WTF and WTForms package form state, validation, and CSRF into reusable classes.",
        "Django forms and ModelForms are built-in and more tightly integrated with models and templates.",
    ),
    "auth": (
        "You invent password hashing, cookie signing, login state, and access control from scratch.",
        "Flask composes focused auth extensions so you can pick sessions, JWT, or OAuth per system.",
        "Django bundles auth, permissions, and session-backed login in one integrated stack.",
    ),
    "rest": (
        "You parse JSON, validate payloads, serialize responses, and document the API by hand.",
        "Flask can stay minimal with pure routes or grow into Flask-Smorest / RESTX for schemas and docs.",
        "FastAPI makes validation and OpenAPI generation core features rather than add-ons.",
    ),
    "async": (
        "You control the event loop and concurrency model directly, including cancellation and backpressure.",
        "Flask allows async views but still centers the WSGI request model unless you change the serving stack.",
        "Quart and FastAPI are ASGI-native, so long-lived async I/O fits them more naturally.",
    ),
    "extensions": (
        "Cross-cutting features become ad-hoc globals and hand-wired helpers quickly.",
        "Flask standardizes extension wiring around the init_app pattern and application state.",
        "Django often ships similar capabilities in core or within a more opinionated app registry.",
    ),
    "testing": (
        "You create raw environ dictionaries or hit a live server with external HTTP clients.",
        "Flask ships an in-process test client and integrates cleanly with pytest fixtures.",
        "Django also has a strong in-process test stack, but its defaults are more preassembled.",
    ),
    "production": (
        "You manually assemble process supervision, logging, TLS termination, health checks, and caching.",
        "Flask keeps deployment explicit: pick Gunicorn, nginx, Docker, Redis, and observability tools yourself.",
        "Django deployment solves many of the same problems but from a fuller default app shape.",
    ),
    "architecture": (
        "Code organization follows whatever import graph you happen to grow into.",
        "Flask rewards explicit boundaries like service layers, repositories, and factories because nothing enforces them for you.",
        "Django's app conventions give more architectural pressure even when teams choose different patterns.",
    ),
}

CLUSTER_SECURITY = {
    "foundation": "Treat raw socket and WSGI demos as teaching tools only. Production safety depends on hardened HTTP parsers, timeouts, TLS termination, and reverse proxies.",
    "routing": "Named routes reduce broken redirects and open redirect mistakes. Restrict methods intentionally so unsafe actions do not leak onto GET endpoints.",
    "request": "Trust boundaries live here: content type, cookies, headers, and body parsing. Validate early and fail with explicit status codes.",
    "templates": "Jinja2's autoescaping blocks many reflected XSS bugs, but the `safe` filter removes that protection instantly.",
    "data": "Use parameterized queries or SQLAlchemy expressions. String-built SQL, open transactions, and leaked connections become security and reliability failures quickly.",
    "forms": "CSRF tokens, filename sanitization, and server-side validation are mandatory because browsers and clients cannot be trusted to police input.",
    "auth": "Weak secrets, plaintext passwords, insecure cookies, and confused token/session boundaries are the fastest ways to lose user accounts.",
    "rest": "APIs need strict schema validation, authentication, authorization, and error discipline. Silent coercion or overly helpful error bodies leak too much.",
    "async": "Background concurrency does not remove auth, context, or secret-handling rules. It only makes mistakes harder to observe.",
    "extensions": "Every extension expands the trusted computing base. Pin versions, initialize them explicitly, and understand what state they store.",
    "testing": "Security bugs survive when tests assert only happy paths. Include malformed inputs, auth failures, CSRF checks, and rollback behavior.",
    "production": "Production hardening means HTTPS, secure cookies, strong secrets, sane worker counts, logging, alerting, and no debug surfaces.",
    "architecture": "Architecture choices affect security because confused boundaries create duplicated auth checks, hidden side effects, and untestable code paths.",
}

CLUSTER_MISTAKES = {
    "foundation": [
        ("Treating Flask as if it replaces HTTP", "The framework only wraps the protocol. Status codes, methods, headers, and cookies still define browser behavior.", "Debug the raw request and response shape before changing application logic."),
        ("Using the development server as a deployment strategy", "Werkzeug's dev server prioritizes debugging ergonomics, not process management or hardening.", "Put Flask behind Gunicorn and a reverse proxy in production."),
    ],
    "routing": [
        ("Hardcoding URLs in templates or redirects", "A path string spreads through the codebase and breaks when routes change.", "Reverse endpoints with `url_for()` everywhere."),
        ("Letting GET mutate state", "Safe methods are cacheable and replayable, so side effects on GET create bugs and security surprises.", "Reserve state changes for POST, PUT, PATCH, or DELETE."),
    ],
    "request": [
        ("Reading `request.json` without checking content type", "A form or text request yields `None`, and code fails later with misleading errors.", "Enforce JSON with `request.is_json` and return 415/422 explicitly."),
        ("Accessing `request` or `g` outside context", "Those objects are proxies, not globals, and Flask can only resolve them inside an active context.", "Push a request or app context explicitly when running scripts and tests."),
    ],
    "templates": [
        ("Using `|safe` on user input", "The template engine stops escaping and your page becomes an XSS sink.", "Escape by default and only mark content safe after sanitization or trusted generation."),
        ("Putting business logic in templates", "Presentation code becomes impossible to test and reuse cleanly.", "Move heavy branching and data shaping into view or service code."),
    ],
    "data": [
        ("Calling `db.create_all()` in production", "It cannot express careful schema evolution and does not replace reviewed migrations.", "Use Alembic / Flask-Migrate for every production schema change."),
        ("Ignoring lazy-loading behavior", "N+1 queries often look fine in development and fall over under real data volume.", "Choose eager loading strategies intentionally and measure query counts."),
    ],
    "forms": [
        ("Trusting browser validation alone", "Clients can bypass HTML constraints instantly.", "Repeat all validation on the server and display errors clearly."),
        ("Saving uploaded files with the original name blindly", "Path traversal and executable payloads become trivial.", "Use `secure_filename`, allowlists, and content inspection."),
    ],
    "auth": [
        ("Storing plaintext passwords or reversible encryption", "A database leak becomes immediate account compromise.", "Use slow password hashes and compare secrets in constant time."),
        ("Using the same cookie and token rules for every client", "Browsers and mobile/API clients have different trust and storage boundaries.", "Choose sessions for browser apps and JWT only when stateless distribution is worth the trade-off."),
    ],
    "rest": [
        ("Returning ad-hoc JSON shapes for errors", "Clients cannot build reliable error handling and debugging becomes inconsistent.", "Standardize error envelopes and status codes."),
        ("Writing API handlers before defining schemas", "Invalid payloads hit business logic and the database too early.", "Validate at the boundary and reject malformed data immediately."),
    ],
    "async": [
        ("Calling blocking libraries inside async views", "The event loop or worker thread is still blocked, so there is no concurrency win.", "Use truly async clients or move the work into a task queue."),
        ("Spawning background threads without context handling", "Tasks lose app config, DB handles, and request-local state silently.", "Copy context deliberately or redesign the task boundary."),
    ],
    "extensions": [
        ("Binding extensions to the app at import time only", "That pattern fights testing and multi-config setups.", "Create extension objects once and call `init_app()` inside the factory."),
        ("Assuming extensions explain themselves", "Opaque storage, signals, or proxy behavior can leak state across requests.", "Read the extension's lifecycle and verify cleanup hooks."),
    ],
    "testing": [
        ("Asserting only status codes", "A 200 response can still contain the wrong JSON, cookie, redirect, or DB side effect.", "Assert payload shape, headers, and persisted state too."),
        ("Reusing a dirty database between tests", "State leakage turns failures into order-dependent noise.", "Use fixtures that isolate or roll back state per test."),
    ],
    "production": [
        ("Leaving `debug=True` or weak secrets in production", "The interactive debugger can become remote code execution and leaked secrets invalidate every other control.", "Use environment-based config, rotate secrets, and keep debug disabled."),
        ("Deploying without health checks or logs", "Incidents become guesswork and orchestrators cannot tell healthy from wedged workers.", "Expose `/health`, log to stdout, and instrument the request path."),
    ],
    "architecture": [
        ("Letting views talk to every dependency directly", "Transaction handling, validation, and auth rules scatter across endpoints.", "Push orchestration into services and keep views thin."),
        ("Using the global app object everywhere", "Circular imports and test pain follow quickly.", "Use the app factory and import from extension modules instead."),
    ],
}

CLUSTER_WRONG_FIX = {
    "foundation": (
        """app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
""",
        """# app.py
from flask import Flask

app = Flask(__name__)

# production:
# gunicorn -w 4 "app:app"
""",
    ),
    "routing": (
        """from flask import redirect

def go_to_user(user_id: int):
    return redirect("/users/" + str(user_id))
""",
        """from flask import redirect, url_for

def go_to_user(user_id: int):
    return redirect(url_for("users.detail", user_id=user_id))
""",
    ),
    "request": (
        """@app.post("/login")
def login():
    email = request.json["email"]
    return {"email": email}
""",
        """@app.post("/login")
def login():
    if not request.is_json:
        abort(415, description="application/json required")
    payload = request.get_json()
    return {"email": payload["email"]}
""",
    ),
    "templates": (
        """@app.get("/preview")
def preview():
    return render_template("preview.html", body=request.args["body"])

# preview.html
{{ body|safe }}
""",
        """@app.get("/preview")
def preview():
    return render_template("preview.html", body=request.args.get("body", ""))

# preview.html
{{ body }}
""",
    ),
    "data": (
        """# wrong for production startup
with app.app_context():
    db.create_all()
""",
        """# migrations belong in deploy scripts
# flask db upgrade
with app.app_context():
    db.session.execute(select(Product).limit(20))
""",
    ),
    "forms": (
        """file = request.files["image"]
file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
""",
        """file = request.files["image"]
name = secure_filename(file.filename)
path = os.path.join(app.config["UPLOAD_FOLDER"], name)
file.save(path)
""",
    ),
    "auth": (
        """if submitted_password == user.password:
    session["user_id"] = user.id
""",
        """if check_password_hash(user.password_hash, submitted_password):
    session["user_id"] = user.id
""",
    ),
    "rest": (
        """@app.post("/api/products")
def create_product():
    data = request.get_json()
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify(data)
""",
        """@app.post("/api/products")
def create_product():
    payload = product_schema.load(request.get_json())
    product = Product(**payload)
    db.session.add(product)
    db.session.commit()
    return product_schema.dump(product), 201
""",
    ),
    "async": (
        """@app.get("/report")
async def report():
    time.sleep(5)
    return {"status": "done"}
""",
        """@app.get("/report")
async def report():
    result = await external_client.get("/report")
    return {"status": result.json()["status"]}
""",
    ),
    "extensions": (
        """db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)
""",
        """db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    return app
""",
    ),
    "testing": (
        """def test_products():
    response = client.get("/api/products")
    assert response.status_code == 200
""",
        """def test_products(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert response.json["items"][0]["name"] == "Desk Lamp"
""",
    ),
    "production": (
        """app.config["SECRET_KEY"] = "dev"
app.config["SESSION_COOKIE_SECURE"] = False
app.run(debug=True)
""",
        """app.config.from_prefixed_env()
app.config["SESSION_COOKIE_SECURE"] = True
# gunicorn -w 4 --bind 0.0.0.0:8000 "wsgi:app"
""",
    ),
    "architecture": (
        """@app.post("/orders")
def create_order():
    user = User.query.get(session["user_id"])
    product = Product.query.get(request.json["product_id"])
    order = Order(user=user)
    db.session.add(order)
    db.session.commit()
    return {"id": order.id}
""",
        """@app.post("/orders")
def create_order():
    result = order_service.create_order(user_id=session["user_id"], payload=request.get_json())
    return order_schema.dump(result), 201
""",
    ),
}

RAW_HTTP_LOGIN = """POST /login HTTP/1.1
Host: shop.example.com
Content-Type: application/json
Content-Length: 41
Cookie: session=eyJ1c2VyX2lkIjoyfQ.sig

{"email":"ana@example.com","password":"secret"}
"""

RAW_HTTP_RESPONSE = """HTTP/1.1 302 FOUND
Content-Type: text/html; charset=utf-8
Location: /dashboard
Set-Cookie: session=...; HttpOnly; Secure; SameSite=Lax

<!doctype html><title>Redirecting...</title>
"""

RAW_SOCKET_SERVER = """import socket

server = socket.socket()
server.bind(("127.0.0.1", 8080))
server.listen(1)

conn, _ = server.accept()
request_bytes = conn.recv(4096)
print(request_bytes.decode("utf-8"))

response = b"HTTP/1.1 200 OK\\r\\nContent-Type: text/plain\\r\\n\\r\\nhello"
conn.sendall(response)
conn.close()
server.close()
"""

MINIMAL_WSGI_APP = """from wsgiref.simple_server import make_server

def application(environ, start_response):
    body = f"hello {environ['PATH_INFO']}".encode("utf-8")
    headers = [("Content-Type", "text/plain; charset=utf-8"), ("Content-Length", str(len(body)))]
    start_response("200 OK", headers)
    return [body]

with make_server("127.0.0.1", 8000, application) as server:
    server.serve_forever()
"""

ECOMMERCE_MODELS = """from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    orders: Mapped[list["Order"]] = relationship(back_populates="user")

class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    inventory: Mapped[int]

class Order(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    created_at: Mapped[str] = mapped_column(server_default=func.now())
    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItem(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    quantity: Mapped[int]
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2))
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
"""

CORE_REQUIREMENTS = """Flask==3.1.0
Werkzeug==3.1.3
Jinja2==3.1.4
itsdangerous==2.2.0
click==8.1.8
blinker==1.8.2
"""

DATA_REQUIREMENTS = """Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.36
Flask-Migrate==4.0.7
Alembic==1.14.0
marshmallow==3.23.1
Flask-Marshmallow==1.2.1
"""

AUTH_REQUIREMENTS = """Flask-Login==0.6.3
Flask-JWT-Extended==4.7.1
Authlib==1.4.0
Flask-Session==0.8.0
Redis==5.2.1
"""

REST_REQUIREMENTS = """Flask-Smorest==0.45.0
apispec==6.8.0
marshmallow==3.23.1
"""

EXTENSION_REQUIREMENTS = """Flask-Caching==2.3.0
Flask-Mail==0.10.0
Flask-Admin==1.6.1
Flask-CORS==5.0.0
celery==5.4.0
"""

TESTING_REQUIREMENTS = """pytest==8.3.4
pytest-flask==1.3.0
responses==0.25.3
factory-boy==3.3.1
pytest-cov==6.0.0
"""

OBSERVABILITY_REQUIREMENTS = """sentry-sdk[flask]==2.19.0
prometheus-flask-exporter==0.23.0
python-json-logger==2.0.7
"""


def ex(title, why, *, code=None, lang="python", note="", kind="code", tabs=None):
    return {
        "title": title,
        "why": why,
        "code": code,
        "lang": lang,
        "note": note,
        "kind": kind,
        "tabs": tabs or [],
    }


def c(
    id,
    layer,
    cluster,
    title,
    prereqs,
    summary,
    problem,
    solution,
    under_hood,
    sample,
    *,
    sample_lang="python",
    sample_kind="code",
    security=None,
    comparison=None,
    other_label=None,
    wsgi_code=None,
    wsgi_lang="python",
    before_code=None,
    before_lang=None,
    after_code=None,
    after_lang=None,
    wrong_code=None,
    fix_code=None,
    mistakes=None,
    version=None,
    extra_examples=None,
):
    return {
        "id": id,
        "layer": layer,
        "cluster": cluster,
        "title": title,
        "prereqs": prereqs,
        "summary": summary,
        "problem": problem,
        "solution": solution,
        "under_hood": under_hood,
        "sample": sample,
        "sample_lang": sample_lang,
        "sample_kind": sample_kind,
        "security": security or CLUSTER_SECURITY[cluster],
        "comparison": comparison or CLUSTER_COMPARISON[cluster],
        "other_label": other_label or OTHER_LABELS[cluster],
        "wsgi_code": wsgi_code,
        "wsgi_lang": wsgi_lang,
        "before_code": before_code,
        "before_lang": before_lang,
        "after_code": after_code,
        "after_lang": after_lang,
        "wrong_code": wrong_code,
        "fix_code": fix_code,
        "mistakes": mistakes or CLUSTER_MISTAKES[cluster],
        "version": version,
        "extra_examples": extra_examples or [],
    }


def default_wsgi(item):
    snippets = {
        "foundation": MINIMAL_WSGI_APP,
        "routing": """def application(environ, start_response):
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]
    if path == "/products" and method == "GET":
        body = b"list products"
        start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
        return [body]
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"not found"]
""",
        "request": """from urllib.parse import parse_qs

def application(environ, start_response):
    query = parse_qs(environ["QUERY_STRING"])
    body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH") or 0))
    payload = str({"query": query, "body": body.decode("utf-8")}).encode("utf-8")
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(payload)))])
    return [payload]
""",
        "templates": """import html

def application(environ, start_response):
    name = html.escape(environ.get("QUERY_STRING", "guest"))
    payload = f"<h1>Hello {name}</h1>".encode("utf-8")
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(payload)))])
    return [payload]
""",
        "data": """import sqlite3

def application(environ, start_response):
    conn = sqlite3.connect("shop.db")
    rows = conn.execute("SELECT id, name FROM product ORDER BY id LIMIT 5").fetchall()
    conn.close()
    payload = str(rows).encode("utf-8")
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(payload)))])
    return [payload]
""",
        "forms": """from urllib.parse import parse_qs

def application(environ, start_response):
    raw = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH") or 0)).decode("utf-8")
    payload = str(parse_qs(raw)).encode("utf-8")
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(payload)))])
    return [payload]
""",
        "auth": """from http.cookies import SimpleCookie

def application(environ, start_response):
    cookies = SimpleCookie(environ.get("HTTP_COOKIE", ""))
    payload = f"session={cookies.get('session')}".encode("utf-8")
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(payload)))])
    return [payload]
""",
        "rest": """import json

def application(environ, start_response):
    raw = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH") or 0) or 0)
    data = json.loads(raw or b"{}")
    payload = json.dumps({"received": data}).encode("utf-8")
    start_response("200 OK", [("Content-Type", "application/json"), ("Content-Length", str(len(payload)))])
    return [payload]
""",
        "async": """def application(environ, start_response):
    payload = b"WSGI itself is synchronous"
    start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(payload)))])
    return [payload]
""",
        "extensions": """class TimingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
""",
        "testing": """from werkzeug.test import EnvironBuilder

builder = EnvironBuilder(path="/products", method="GET")
environ = builder.get_environ()
response = app.wsgi_app(environ, lambda status, headers: None)
print(b"".join(response))
""",
        "production": """from myapp import create_app

app = create_app()
""",
        "architecture": """def create_order_service(repo, inventory, payload):
    order = repo.create_order(payload["user_id"])
    inventory.reserve(order.id, payload["items"])
    return order
""",
    }
    return snippets[item["cluster"]], "This is the lower-level boundary Flask wraps for this concept."


def default_wrong_fix(item):
    return CLUSTER_WRONG_FIX[item["cluster"]]


def build_examples(item):
    raw_code, raw_note = (
        (item["wsgi_code"], "This raw WSGI version shows the boundary Flask removes.")
        if item.get("wsgi_code")
        else default_wsgi(item)
    )
    wrong_code, fix_code = item.get("wrong_code"), item.get("fix_code")
    if not wrong_code or not fix_code:
        default_wrong, default_fix = default_wrong_fix(item)
        wrong_code = wrong_code or default_wrong
        fix_code = fix_code or default_fix
    examples = [
        ex("Minimal Working Shape", item["solution"], code=item["sample"], lang=item["sample_lang"], note=item["under_hood"], kind=item["sample_kind"]),
        ex(
            "Before Flask / After Flask",
            "Seeing the same idea before and after Flask makes the abstraction boundary concrete.",
            kind="tabs",
            tabs=[
                ("Before Flask", item.get("before_lang") or item.get("wsgi_lang") or "python", item.get("before_code") or raw_code),
                ("After Flask", item.get("after_lang") or item.get("sample_lang") or "python", item.get("after_code") or item["sample"]),
            ],
            note=raw_note,
        ),
        ex(
            "Common Mistake / Fix",
            "Production bugs usually come from boundary mistakes rather than syntax.",
            kind="tabs",
            tabs=[("Wrong", "python", wrong_code), ("Fix", "python", fix_code)],
            note=item["mistakes"][0][1] if item["mistakes"] else "",
        ),
    ]
    examples.extend(item["extra_examples"])
    return examples


def render_pre(code, label="python", extra_class=""):
    lines = dedent(code).strip("\n").splitlines() or [""]
    classes = ["has-lines"]
    if extra_class:
        classes.append(extra_class)
    body = "".join(
        f"<span class='code-line'><span class='line-no'>{i}</span><span class='line-text'>{escape(line) or '&nbsp;'}</span></span>"
        for i, line in enumerate(lines, 1)
    )
    return f"<pre data-lang='{escape(label)}' class='{' '.join(classes)}'><code class='language-{escape(label)}'>{body}</code></pre>"


def render_http(code):
    return f"<div class='http-display'>{render_pre(code, 'http', 'http-block')}</div>"


def render_tabs(section_id, example_index, tabs):
    buttons = []
    panels = []
    for idx, (label, lang, code) in enumerate(tabs):
        active = " is-active" if idx == 0 else ""
        panel_id = f"{section_id}-ex{example_index}-tab{idx}"
        buttons.append(
            f"<button class='tab-btn{active}' type='button' data-panel='{panel_id}' aria-pressed='{'true' if idx == 0 else 'false'}'>{escape(label)}</button>"
        )
        panels.append(f"<div class='tab-panel{active}' id='{panel_id}'>{render_pre(code, lang)}</div>")
    return f"<div class='tabbed-code'><div class='tab-buttons'>{''.join(buttons)}</div><div class='tab-panels'>{''.join(panels)}</div></div>"


def render_example(example, section_id, index):
    body = [
        "<article class='example-card'>",
        f"<h4>Example {index}. {escape(example['title'])}</h4>",
        f"<p><strong>Why it matters:</strong> {escape(example['why'])}</p>",
    ]
    if example["kind"] == "tabs":
        body.append(render_tabs(section_id, index, example["tabs"]))
    elif example["kind"] == "http":
        body.append(render_http(example["code"]))
    else:
        body.append(render_pre(example["code"], example["lang"]))
    if example.get("note"):
        body.append(f"<p><strong>What to observe:</strong> {escape(example['note'])}</p>")
    body.append("</article>")
    return "".join(body)


def render_comparison(item):
    raw_text, flask_text, other_text = item["comparison"]
    return (
        "<div class='comparison-box'>"
        "<table><thead><tr>"
        "<th>Raw Python / WSGI</th>"
        "<th>Flask</th>"
        f"<th>{escape(item['other_label'])}</th>"
        "</tr></thead><tbody><tr>"
        f"<td>{escape(raw_text)}</td>"
        f"<td>{escape(flask_text)}</td>"
        f"<td>{escape(other_text)}</td>"
        "</tr></tbody></table></div>"
    )


def render_mistakes(items):
    cards = []
    for wrong, cause, fix in items:
        cards.append(
            "<article class='gotcha-box'>"
            f"<h4>{escape(wrong)}</h4>"
            f"<p><strong>Root cause:</strong> {escape(cause)}</p>"
            f"<p><strong>Fix:</strong> {escape(fix)}</p>"
            "</article>"
        )
    return f"<div class='mistake-grid'>{''.join(cards)}</div>"


def render_badges(ids):
    if not ids:
        return "<span class='badge subtle'>None</span>"
    return "".join(f"<a class='badge' href='#{escape(i)}'>{escape(i)}</a>" for i in ids)


def build_dependents():
    deps = defaultdict(list)
    for item in CONCEPTS:
        for prereq in item["prereqs"]:
            deps[prereq].append(item["id"])
    return deps


def render_section(item, dependents, index):
    next_id = CONCEPTS[index + 1]["id"] if index + 1 < len(CONCEPTS) else "quick-reference"
    used_later = dependents.get(item["id"], [])
    raw_code, raw_note = (
        (item["wsgi_code"], "This raw WSGI version shows the boundary Flask removes.")
        if item.get("wsgi_code")
        else default_wsgi(item)
    )
    version_html = ""
    if item.get("version"):
        version_html = f"<aside class='callout version-box'><strong>Flask 2.x vs 3.x:</strong> {escape(item['version'])}</aside>"
    checks = [
        ("What problem does this solve?", item["problem"]),
        ("What is Flask doing under the hood?", item["under_hood"]),
        ("What security or reliability risk matters most here?", item["security"]),
    ]
    examples = "".join(render_example(example, item["id"], idx) for idx, example in enumerate(build_examples(item), 1))
    used_html = "".join(f"<a class='badge subtle' href='#{escape(cid)}'>{escape(cid)}</a>" for cid in used_later[:10]) or "<span class='badge subtle'>No direct dependents listed</span>"
    return f"""
<section id="{item['id']}" class="concept-section" data-layer="{item['layer']}" data-title="{escape(item['title'])}">
  <div class="section-kicker">{item['id']} &middot; Layer {item['layer']} &middot; {escape(LAYER_NAMES[item['layer']])}</div>
  <h2>{escape(item['title'])}</h2>
  <div class="section-meta">
    <span class="cluster-pill {CLUSTER_CLASS[item['cluster']]}">{escape(item['cluster'].title())}</span>
    <span class="badge subtle">Anchor {item['id']}</span>
  </div>
  <p class="lead">{escape(item['summary'])}</p>
  {version_html}
  <div class="forward-links">
    <div><span class="meta-label">Read first</span>{render_badges(item['prereqs'])}</div>
    <div><span class="meta-label">Used in</span>{used_html}</div>
  </div>
  <h3>The Problem</h3>
  <aside class="callout why-box">{escape(item['problem'])}</aside>
  <h3>Flask's Solution</h3>
  <p>{escape(item['solution'])}</p>
  <h3>Under The Hood</h3>
  <p>{escape(item['under_hood'])}</p>
  <aside class="callout wsgi-box" hidden>
    <div class="wsgi-title">Raw WSGI Equivalent</div>
    <p>{escape(raw_note)}</p>
    {render_pre(raw_code, item.get('wsgi_lang') or 'python')}
  </aside>
  <h3>Code Examples</h3>
  <div class="example-grid">{examples}</div>
  <h3>Comparison</h3>
  {render_comparison(item)}
  <h3>Common Mistakes</h3>
  {render_mistakes(item['mistakes'])}
  <h3>Security Implications</h3>
  <aside class="callout security-box">{escape(item['security'])}</aside>
  <h3>Self-Check</h3>
  {''.join(f"<details class='self-check'><summary>{escape(q)}</summary><div>{escape(a)}</div></details>" for q, a in checks)}
  <h3>Forward Links</h3>
  <p>This concept is used in: {used_html}</p>
  <div class="section-footer"><a class="prev-link" href="#dependency-table">Back to references</a><a class="next-link" href="#{next_id}">Next concept &rarr; {next_id}</a></div>
</section>
"""


def render_dag():
    nodes = []
    edges = []
    for item in CONCEPTS:
        nodes.append(f'    {item["id"]}["{item["id"]} {item["title"]}"]:::{item["cluster"]}')
        for prereq in item["prereqs"]:
            edges.append(f"    {prereq} --> {item['id']}")
    class_defs = """
    classDef foundation fill:#2a1216,stroke:#e04646,color:#f5ebe4;
    classDef routing fill:#331517,stroke:#ff6f61,color:#f5ebe4;
    classDef request fill:#2e1a1c,stroke:#ff8a65,color:#f5ebe4;
    classDef templates fill:#1b2b2a,stroke:#7fffd4,color:#f5ebe4;
    classDef data fill:#202321,stroke:#d8c77a,color:#f5ebe4;
    classDef forms fill:#3a2418,stroke:#ffb347,color:#f5ebe4;
    classDef auth fill:#1f2432,stroke:#89a6ff,color:#f5ebe4;
    classDef rest fill:#192730,stroke:#56d6ff,color:#f5ebe4;
    classDef async fill:#25203a,stroke:#b590ff,color:#f5ebe4;
    classDef extensions fill:#2a2323,stroke:#ff9f80,color:#f5ebe4;
    classDef testing fill:#1f2d2a,stroke:#8ce6c1,color:#f5ebe4;
    classDef production fill:#2a2520,stroke:#f2d28b,color:#f5ebe4;
    classDef architecture fill:#222128,stroke:#b6b2ff,color:#f5ebe4;
"""
    return "graph TD\n" + "\n".join(nodes + edges) + class_defs


def render_dependency_table(dependents):
    rows = "".join(
        "<tr>"
        f"<td><a href='#{item['id']}'>{item['id']}</a></td>"
        f"<td>{escape(item['title'])}</td>"
        f"<td>{item['layer']}</td>"
        f"<td>{', '.join(item['prereqs']) or 'None'}</td>"
        f"<td>{', '.join(dependents.get(item['id'], [])) or 'None'}</td>"
        "</tr>"
        for item in CONCEPTS
    )
    return f"""
<section class='concept-section' id='dependency-table' data-title='Concept DAG & Dependency Table'>
  <div class='section-kicker'>Task 2 &middot; Concept DAG</div>
  <h2>Flask Concept DAG</h2>
  <p>The order of the document follows this dependency graph exactly, so each section appears after the ideas it depends on.</p>
  <div class='mermaid-wrap'><div class='mermaid'>{escape(render_dag())}</div></div>
  <h3>All 59 Concepts</h3>
  <div class='table-wrap'><table><thead><tr><th>ID</th><th>Concept</th><th>Layer</th><th>Prerequisites</th><th>Dependents</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
"""


def render_wsgi_flow():
    flow = """
flowchart LR
    A[Raw HTTP Request] --> B[Socket Accept]
    B --> C[WSGI Server<br/>Gunicorn / Werkzeug]
    C --> D[Flask WSGI App]
    D --> E[Push App Context]
    E --> F[Push Request Context]
    F --> G[URL Match via Werkzeug Map]
    G --> H[before_request Hooks]
    H --> I[View Function]
    I --> J[after_request Hooks]
    J --> K[Pop Request Context]
    K --> L[Pop App Context]
    L --> M[WSGI Response Iterable]
    M --> N[Server Writes HTTP Response]
"""
    return f"""
<section class='concept-section' id='wsgi-flow' data-title='WSGI Request Flow'>
  <div class='section-kicker'>Task 2 &middot; WSGI Flow</div>
  <h2>Flask WSGI Request Flow</h2>
  <p>Every request still starts as bytes on a socket. Flask's value is how it structures the steps after a server has parsed those bytes into WSGI state.</p>
  <div class='mermaid-wrap'><div class='mermaid'>{escape(flow)}</div></div>
</section>
"""


def render_context_stack():
    diagram = """
flowchart LR
    A[No active context] --> B[Push app context]
    B --> C[current_app available]
    C --> D[Push request context]
    D --> E[request, session, and g available]
    E --> F[View logic runs]
    F --> G[Run teardown_request]
    G --> H[Pop request context]
    H --> I[Run teardown_appcontext]
    I --> J[Pop app context]
"""
    return f"""
<section class='concept-section' id='context-stack' data-title='Application & Request Context Stack'>
  <div class='section-kicker'>Task 2 &middot; Contexts</div>
  <h2>Application And Request Context Stack</h2>
  <p>Flask's globals are proxies into the current stack frame. Push the wrong context, or none at all, and those proxies have nowhere safe to resolve.</p>
  <div class='mermaid-wrap'><div class='mermaid'>{escape(diagram)}</div></div>
</section>
"""


def render_ecosystem_map():
    cards = [
        ("Database", "Flask-SQLAlchemy", "App-factory friendly SQLAlchemy integration."),
        ("Database", "Flask-MongoEngine", "MongoDB document mapping if your workload fits it."),
        ("Auth", "Flask-Login", "Session-backed browser authentication."),
        ("Auth", "Flask-JWT-Extended", "JWT access and refresh token workflows."),
        ("Auth", "Flask-Dance / Authlib", "OAuth and social login flows."),
        ("Forms", "Flask-WTF", "WTForms integration and CSRF support."),
        ("Forms", "Flask-Rebar", "Schema-heavy request validation patterns."),
        ("REST", "Flask-RESTX", "Resource classes and Swagger generation."),
        ("REST", "Flask-Smorest", "Marshmallow-first REST APIs with OpenAPI."),
        ("Tasks", "Celery", "Retries, scheduling, and background task queues."),
        ("Tasks", "RQ / APScheduler", "Lighter task or scheduling options."),
        ("Testing", "pytest-flask", "pytest helpers around app and client fixtures."),
        ("Testing", "responses", "Mock outbound HTTP calls deterministically."),
        ("Testing", "factory-boy", "Factories for expressive test data."),
        ("Admin", "Flask-Admin", "Metadata-driven admin surface."),
        ("Admin", "Flask-AdminLTE", "Bootstrap-oriented admin skin."),
        ("Caching", "Flask-Caching", "Memoization and backend cache integration."),
        ("Email", "Flask-Mail", "SMTP helpers for app email flows."),
    ]
    rendered = "".join(
        f"<article class='extension-card'><div class='extension-type'>{escape(cat)}</div><h3>{escape(name)}</h3><p>{escape(desc)}</p></article>"
        for cat, name, desc in cards
    )
    return f"""
<section class='concept-section' id='ecosystem-map' data-title='Flask Extension Ecosystem'>
  <div class='section-kicker'>Task 11 &middot; Ecosystem</div>
  <h2>Flask Extension Ecosystem</h2>
  <p>Flask stays small by design. The ecosystem fills in batteries as needed, which is power and responsibility at the same time.</p>
  <div class='extension-grid'>{rendered}</div>
</section>
"""


def render_quick_reference():
    rows = "".join(
        "<tr>"
        f"<td><a href='#{item['id']}'>{item['id']}</a></td>"
        f"<td>{item['layer']}</td>"
        f"<td>{escape(item['title'])}</td>"
        f"<td>{escape(item['summary'])}</td>"
        "</tr>"
        for item in CONCEPTS
    )
    return f"""
<section class='concept-section quick-reference' id='quick-reference' data-title='Quick Reference'>
  <div class='section-kicker'>Task 11 &middot; Quick Reference</div>
  <h2>FL01-FL59 At A Glance</h2>
  <div class='table-wrap'><table><thead><tr><th>ID</th><th>Layer</th><th>Concept</th><th>One-line Summary</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
"""


def render_nav():
    by_layer = defaultdict(list)
    for item in CONCEPTS:
        by_layer[item["layer"]].append(item)
    parts = [
        "<section class='nav-group' data-layer='ref'>"
        "<button class='group-toggle' type='button' data-layer='R' aria-expanded='true'><span>References</span><span>▾</span></button>"
        "<div class='group-links'>"
        + "".join(
            f"<a href='#{target}' data-id='{target}' data-label='{escape(label.lower())}'><span class='nav-dot'>R</span><span>{escape(label)}</span></a>"
            for target, label in REFERENCE_SECTIONS
        )
        + "</div></section>"
    ]
    for layer in sorted(LAYER_NAMES):
        links = "".join(
            f"<a href='#{item['id']}' data-id='{item['id']}' data-label='{escape((item['id'] + ' ' + item['title']).lower())}'><span class='nav-dot'>{layer}</span><span>{escape(item['id'] + ' · ' + item['title'])}</span></a>"
            for item in by_layer[layer]
        )
        parts.append(
            f"<section class='nav-group' data-layer='{layer}'>"
            f"<button class='group-toggle' type='button' data-layer='{layer}' aria-expanded='true'><span>{escape(NAV_LABELS[layer])}</span><span>▾</span></button>"
            f"<div class='group-links'>{links}</div></section>"
        )
    return "".join(parts)


def render_shell(dependents):
    return f"""<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>{TITLE}</title>
<link rel='preconnect' href='https://fonts.googleapis.com'>
<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>
<link href='https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Fira+Code:wght@400;500;600&family=Nunito:wght@400;600;700;800&display=swap' rel='stylesheet'>
<style>
:root {{
  --bg:#0a0a0f;
  --panel:#111119;
  --panel-2:#161622;
  --panel-3:#1f1f30;
  --ink:#f4efe7;
  --muted:#c7bfb5;
  --accent:#e04646;
  --mint:#7fffd4;
  --gold:#e2c275;
  --blue:#89a6ff;
  --border:rgba(255,255,255,.09);
  --shadow:0 18px 50px rgba(0,0,0,.45);
  --sidebar-w:280px;
  --font-head:'DM Serif Display', serif;
  --font-body:'Nunito', sans-serif;
  --font-code:'Fira Code', monospace;
}}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; background:var(--bg); }}
body {{
  margin:0;
  min-height:100vh;
  background:
    radial-gradient(circle at 12% 8%, rgba(224,70,70,.16), transparent 28%),
    radial-gradient(circle at 88% 18%, rgba(127,255,212,.06), transparent 22%),
    radial-gradient(circle at 78% 86%, rgba(140,29,34,.18), transparent 28%),
    linear-gradient(180deg, #0b0b10 0%, #09090d 100%);
  color:var(--ink);
  font-family:var(--font-body);
  line-height:1.7;
}}
a {{ color:var(--mint); text-decoration:none; }}
a:hover {{ color:#cffff2; }}
h1,h2,h3,h4,h5 {{ font-family:var(--font-head); line-height:1.15; margin:0; }}
h1 {{ font-size:clamp(2.6rem, 4.5vw, 4.6rem); letter-spacing:-.03em; }}
h2 {{ font-size:clamp(1.6rem, 2.7vw, 2.7rem); margin-bottom:.75rem; }}
h3 {{ font-size:1.25rem; margin:1.9rem 0 .75rem; color:#fff3ee; }}
h4 {{ font-size:1.05rem; margin-bottom:.4rem; color:#fff0ea; }}
p, li, td, th, summary {{ font-size:1rem; color:var(--muted); }}
strong {{ color:var(--ink); }}
code, pre, .meta-label, .badge, .section-kicker, .theme-note, .nav-dot, .extension-type {{ font-family:var(--font-code); }}
p code, li code, td code {{
  background:rgba(127,255,212,.08);
  border:1px solid rgba(127,255,212,.16);
  color:var(--mint);
  border-radius:8px;
  padding:.14em .42em;
  font-size:.88em;
}}
.kw {{ color:#ff6f61; }}
.str {{ color:var(--mint); }}
.cmt {{ color:#8d8b94; }}
.fn {{ color:#ff9c7f; }}
.cls {{ color:var(--gold); }}
.app-shell {{ display:flex; min-height:100vh; }}
.sidebar {{
  position:fixed;
  inset:0 auto 0 0;
  width:var(--sidebar-w);
  background:rgba(10,10,15,.96);
  border-right:1px solid var(--border);
  padding:1.1rem .9rem 1.3rem;
  overflow:hidden;
  z-index:40;
  box-shadow:var(--shadow);
}}
.sidebar-top {{
  position:sticky;
  top:0;
  background:linear-gradient(180deg, rgba(10,10,15,.98), rgba(10,10,15,.88));
  padding-bottom:.9rem;
  margin-bottom:.9rem;
  z-index:3;
}}
.brand {{
  border:1px solid var(--border);
  border-radius:18px;
  padding:1rem;
  background:linear-gradient(180deg, rgba(224,70,70,.12), rgba(255,255,255,.02));
  margin-bottom:.8rem;
}}
.brand h2 {{ font-size:1.4rem; margin-bottom:.2rem; }}
.theme-note {{ font-size:.75rem; color:#ffd4cc; text-transform:uppercase; letter-spacing:.12em; }}
.legend {{ display:flex; flex-wrap:wrap; gap:.45rem; margin-top:.75rem; }}
.legend span {{
  padding:.28rem .52rem;
  border-radius:999px;
  background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.08);
  font-size:.72rem;
}}
.sidebar-controls {{ display:grid; gap:.55rem; margin-bottom:.8rem; }}
.nav-search {{
  width:100%;
  border-radius:12px;
  border:1px solid var(--border);
  background:rgba(255,255,255,.04);
  color:var(--ink);
  padding:.78rem .85rem;
  font:600 .92rem var(--font-body);
}}
.nav-search::placeholder {{ color:#9a9390; }}
.control-row {{ display:grid; grid-template-columns:1fr 1fr; gap:.5rem; }}
.sidebar button, .back-to-top {{
  appearance:none;
  border:1px solid var(--border);
  background:rgba(255,255,255,.04);
  color:var(--ink);
  border-radius:12px;
  padding:.68rem .8rem;
  cursor:pointer;
  font:600 .82rem var(--font-code);
}}
.sidebar button:hover, .back-to-top:hover {{ background:rgba(224,70,70,.12); border-color:rgba(224,70,70,.4); }}
.progress-shell {{ border:1px solid var(--border); border-radius:16px; padding:.8rem; background:rgba(255,255,255,.03); }}
.progress-meta {{ display:flex; justify-content:space-between; gap:.6rem; margin-bottom:.55rem; font-size:.82rem; color:#f0d4cb; }}
.progress-track {{ height:10px; border-radius:999px; overflow:hidden; background:rgba(255,255,255,.06); }}
.progress-fill {{ width:0%; height:100%; background:linear-gradient(90deg, var(--accent), #ff8a65); }}
.sidebar-nav {{ overflow-y:auto; height:calc(100vh - 300px); padding-right:.1rem; }}
.nav-group {{ margin:0 0 .7rem; border:1px solid var(--border); border-radius:16px; background:rgba(255,255,255,.02); overflow:hidden; }}
.group-toggle {{
  width:100%;
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:.6rem;
  background:transparent;
  border:none;
  padding:.82rem .9rem;
  font:600 .78rem var(--font-code);
  text-transform:uppercase;
  letter-spacing:.08em;
  color:#f2dad4;
}}
.group-links {{ padding:.15rem .35rem .45rem; }}
.nav-group.collapsed .group-links {{ display:none; }}
.nav-group.collapsed .group-toggle span:last-child {{ transform:rotate(-90deg); }}
.group-links a {{
  display:grid;
  grid-template-columns:auto 1fr;
  gap:.6rem;
  align-items:start;
  border-radius:10px;
  padding:.46rem .56rem;
  color:var(--muted);
  border-left:2px solid transparent;
}}
.group-links a:hover, .group-links a.active {{ background:rgba(224,70,70,.12); border-left-color:var(--accent); color:#fff3ee; }}
.group-links a[hidden] {{ display:none !important; }}
.nav-dot {{
  display:inline-flex;
  justify-content:center;
  align-items:center;
  min-width:1.55rem;
  height:1.55rem;
  border-radius:999px;
  background:rgba(127,255,212,.08);
  color:var(--mint);
  border:1px solid rgba(127,255,212,.16);
  font-size:.68rem;
}}
main {{ margin-left:var(--sidebar-w); width:calc(100% - var(--sidebar-w)); padding:2rem clamp(1rem, 2.2vw, 2rem) 3rem; }}
.hero {{
  position:relative;
  overflow:hidden;
  border:1px solid var(--border);
  border-radius:28px;
  padding:2.2rem;
  background:linear-gradient(135deg, rgba(224,70,70,.17), rgba(255,255,255,.02)), rgba(255,255,255,.02);
  box-shadow:var(--shadow);
}}
.hero-grid {{ display:grid; grid-template-columns:1.3fr .9fr; gap:1.2rem; align-items:start; }}
.hero-card {{ border:1px solid var(--border); border-radius:20px; padding:1rem; background:rgba(0,0,0,.18); }}
.concept-section {{
  margin-top:1.4rem;
  border:1px solid var(--border);
  border-radius:24px;
  padding:1.7rem;
  background:linear-gradient(180deg, rgba(255,255,255,.025), rgba(255,255,255,.018));
  box-shadow:var(--shadow);
  scroll-margin-top:1rem;
}}
.section-kicker {{ color:#ffb2a3; text-transform:uppercase; letter-spacing:.12em; font-size:.74rem; margin-bottom:.7rem; }}
.lead {{ color:#f0e1d7; font-size:1.04rem; }}
.section-meta, .forward-links {{ display:flex; flex-wrap:wrap; gap:.7rem 1rem; align-items:center; margin:.75rem 0 1rem; }}
.forward-links > div {{ display:flex; flex-wrap:wrap; gap:.5rem; align-items:center; }}
.meta-label {{ font-size:.73rem; letter-spacing:.08em; text-transform:uppercase; color:#eac6bd; }}
.badge {{ display:inline-flex; align-items:center; justify-content:center; padding:.24rem .56rem; border-radius:999px; background:rgba(224,70,70,.12); border:1px solid rgba(224,70,70,.24); color:#ffd7cf; font-size:.72rem; }}
.badge.subtle {{ background:rgba(127,255,212,.08); border-color:rgba(127,255,212,.16); color:var(--mint); }}
.cluster-pill {{ display:inline-flex; align-items:center; border-radius:999px; padding:.22rem .62rem; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; }}
.cluster-foundation {{ background:rgba(224,70,70,.14); color:#ffd1c7; }}
.cluster-routing {{ background:rgba(255,111,97,.14); color:#ffd9d0; }}
.cluster-request {{ background:rgba(255,138,101,.14); color:#ffe0d3; }}
.cluster-templates {{ background:rgba(127,255,212,.12); color:#caffef; }}
.cluster-data {{ background:rgba(226,194,117,.14); color:#ffefc3; }}
.cluster-forms {{ background:rgba(255,179,71,.14); color:#ffe0b3; }}
.cluster-auth {{ background:rgba(137,166,255,.14); color:#dde6ff; }}
.cluster-rest {{ background:rgba(86,214,255,.14); color:#d5f6ff; }}
.cluster-async {{ background:rgba(181,144,255,.14); color:#eadcff; }}
.cluster-extensions {{ background:rgba(255,159,128,.14); color:#ffe0d6; }}
.cluster-testing {{ background:rgba(140,230,193,.14); color:#ddfff0; }}
.cluster-production {{ background:rgba(242,210,139,.14); color:#fff2cf; }}
.cluster-architecture {{ background:rgba(182,178,255,.14); color:#eeedff; }}
.callout {{ border-radius:18px; padding:1rem 1.05rem; border:1px solid var(--border); }}
.why-box {{ background:rgba(224,70,70,.11); border-left:4px solid var(--accent); color:#ffe4dd; }}
.wsgi-box {{ background:rgba(127,255,212,.08); border-left:4px solid var(--mint); }}
.security-box {{ background:rgba(255,179,71,.09); border-left:4px solid var(--gold); color:#fff0cf; }}
.version-box {{ background:rgba(137,166,255,.08); border-left:4px solid var(--blue); color:#dde6ff; }}
.wsgi-title {{ font:600 .82rem var(--font-code); letter-spacing:.08em; text-transform:uppercase; color:#1d3e34; }}
body.show-wsgi .wsgi-box[hidden] {{ display:block; }}
.comparison-box {{ border:1px solid var(--border); border-radius:18px; overflow:hidden; background:rgba(255,255,255,.02); }}
.table-wrap {{ overflow:auto; }}
table {{ width:100%; border-collapse:collapse; min-width:720px; }}
th, td {{ padding:.85rem .9rem; border-bottom:1px solid rgba(255,255,255,.08); text-align:left; vertical-align:top; }}
th {{ color:#fff0ea; font-family:var(--font-code); font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; }}
.example-grid {{ display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:1rem; }}
.example-card, .gotcha-box, .mermaid-wrap, .extension-card {{ border:1px solid var(--border); border-radius:18px; padding:1rem; background:rgba(255,255,255,.025); }}
pre[data-lang] {{ position:relative; overflow:auto; margin:.85rem 0 0; border:1px solid rgba(127,255,212,.1); border-radius:16px; background:#090910; padding:2.4rem 0 0; }}
pre[data-lang]::before {{ content:attr(data-lang); position:absolute; top:.7rem; left:.9rem; font:600 .72rem var(--font-code); text-transform:uppercase; letter-spacing:.08em; color:#ffb2a3; }}
.copy-btn {{ position:absolute; top:.55rem; right:.65rem; border-radius:10px; border:1px solid rgba(255,255,255,.12); background:rgba(255,255,255,.04); color:var(--ink); padding:.35rem .55rem; font:600 .72rem var(--font-code); cursor:pointer; }}
.code-line {{ display:grid; grid-template-columns:3rem 1fr; gap:.8rem; padding:0 .95rem; }}
.code-line:last-child {{ padding-bottom:.9rem; }}
.line-no {{ color:#746d6a; text-align:right; user-select:none; }}
.line-text {{ color:#eae4db; white-space:pre; }}
.http-display {{ border:1px solid rgba(224,70,70,.2); border-radius:18px; background:rgba(224,70,70,.05); padding:.2rem; }}
.tab-buttons {{ display:flex; flex-wrap:wrap; gap:.45rem; margin-top:.8rem; }}
.tab-btn {{ appearance:none; border:1px solid var(--border); background:rgba(255,255,255,.03); color:var(--muted); border-radius:999px; padding:.45rem .7rem; cursor:pointer; font:600 .74rem var(--font-code); }}
.tab-btn.is-active {{ background:rgba(224,70,70,.14); color:#fff0ea; border-color:rgba(224,70,70,.34); }}
.tab-panel {{ display:none; }}
.tab-panel.is-active {{ display:block; }}
.mistake-grid {{ display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:1rem; }}
.self-check {{ border:1px solid var(--border); border-radius:14px; padding:.7rem .9rem; background:rgba(255,255,255,.02); margin-bottom:.7rem; }}
.self-check summary {{ cursor:pointer; color:#ffe9e2; font-weight:700; }}
.self-check div {{ margin-top:.55rem; }}
.section-footer {{ display:flex; justify-content:space-between; gap:.8rem; margin-top:1.4rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,.08); }}
.prev-link, .next-link {{ display:inline-flex; align-items:center; gap:.35rem; padding:.62rem .82rem; border-radius:12px; background:rgba(255,255,255,.03); border:1px solid var(--border); }}
.extension-grid {{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:1rem; }}
.extension-type {{ color:#ffb2a3; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; }}
.mermaid-wrap {{ overflow:auto; }}
.back-to-top {{ position:fixed; right:1rem; bottom:1rem; z-index:30; display:none; }}
.back-to-top.visible {{ display:inline-flex; }}
.mobile-toggle {{ display:none; position:fixed; left:1rem; top:1rem; z-index:45; width:46px; height:46px; border-radius:14px; font-size:1.1rem; }}
@media (max-width: 1100px) {{ .hero-grid, .example-grid, .mistake-grid, .extension-grid {{ grid-template-columns:1fr; }} }}
@media (max-width: 900px) {{
  .mobile-toggle {{ display:inline-flex; align-items:center; justify-content:center; }}
  .sidebar {{ transform:translateX(-110%); transition:transform .22s ease; width:min(88vw, 320px); }}
  .sidebar.open {{ transform:translateX(0); }}
  main {{ margin-left:0; width:100%; padding-top:4.5rem; }}
}}
</style>
</head>
<body>
<button class='mobile-toggle' id='mobileToggle' aria-label='Toggle navigation'>☰</button>
<div class='app-shell'>
<aside class='sidebar' id='sidebar'>
  <div class='sidebar-top'>
    <div class='brand'>
      <div class='theme-note'>Flask 3.x Reference</div>
      <h2>{TITLE}</h2>
      <p>HTTP, WSGI, Jinja2, SQLAlchemy, auth, APIs, async, testing, and deployment in one dependency-ordered document.</p>
      <div class='legend'><span class='kw'>keywords</span><span class='str'>strings</span><span class='cmt'>comments</span><span class='fn'>functions</span><span class='cls'>classes</span></div>
    </div>
    <div class='sidebar-controls'>
      <input class='nav-search' id='navSearch' type='search' placeholder='Press / to filter FL sections'>
      <div class='control-row'><button id='collapseAll' type='button'>Collapse</button><button id='expandAll' type='button'>Expand</button></div>
      <button id='wsgiToggle' type='button'>Show WSGI equivalents</button>
      <div class='progress-shell'><div class='progress-meta'><span>Reading progress</span><span id='progressText'>0%</span></div><div class='progress-track'><div class='progress-fill' id='progressFill'></div></div></div>
    </div>
  </div>
  <nav class='sidebar-nav' aria-label='Flask concept navigation'>{render_nav()}</nav>
</aside>
<main>
<!-- TASK-1 START -->
<section class='hero' id='top'>
  <div class='section-kicker'>Flask Complete Reference</div>
  <div class='hero-grid'>
    <div>
      <h1>{SUBTITLE}</h1>
      <p>This document assumes Python fundamentals but no prior framework knowledge. It starts from raw HTTP, sockets, and WSGI, then climbs through routing, request handling, templates, persistence, sessions, auth, REST APIs, async trade-offs, testing, and production deployment.</p>
      <p>The running product is a small e-commerce system with <code>User</code>, <code>Product</code>, <code>Order</code>, and <code>OrderItem</code>. The same domain appears through SQLAlchemy, forms, login flows, APIs, background work, and tests so the examples stay coherent.</p>
    </div>
    <div class='hero-card'>
      <h3>Baseline Core Packages</h3>
      {render_pre(CORE_REQUIREMENTS, "text")}
    </div>
  </div>
</section>
<!-- TASK-1 END -->
<!-- TASK-2 START -->
{render_dependency_table(dependents)}
{render_wsgi_flow()}
{render_context_stack()}
<!-- TASK-2 END -->
"""


def tail_script():
    return r"""
</main>
</div>
<script defer src='https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  const navLinks = [...document.querySelectorAll('.group-links a')];
  const sections = [...document.querySelectorAll('main .concept-section[id]')];
  const conceptSections = sections.filter((section) => /^FL\d+$/.test(section.id));
  const sidebar = document.getElementById('sidebar');
  const mobileToggle = document.getElementById('mobileToggle');
  const collapseAll = document.getElementById('collapseAll');
  const expandAll = document.getElementById('expandAll');
  const searchInput = document.getElementById('navSearch');
  const wsgiToggle = document.getElementById('wsgiToggle');
  const backToTop = document.getElementById('backToTop');
  const progressFill = document.getElementById('progressFill');
  const progressText = document.getElementById('progressText');
  let wsgiVisible = false;
  document.querySelectorAll('pre[data-lang]').forEach((pre) => {
    let button = pre.querySelector('.copy-btn');
    if (!button) {
      button = document.createElement('button');
      button.className = 'copy-btn';
      button.type = 'button';
      button.textContent = 'Copy';
      pre.appendChild(button);
    }
    if (button.dataset.bound === 'true') return;
    button.dataset.bound = 'true';
    button.addEventListener('click', async () => {
      const text = [...pre.querySelectorAll('.line-text')].map((line) => line.textContent || '').join('\n');
      await navigator.clipboard.writeText(text);
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = 'Copy'; }, 1200);
    });
  });
  document.querySelectorAll('.tabbed-code').forEach((root) => {
    const buttons = [...root.querySelectorAll('.tab-btn')];
    buttons.forEach((button) => {
      if (button.dataset.bound === 'true') return;
      button.dataset.bound = 'true';
      button.addEventListener('click', () => {
        const panelId = button.dataset.panel;
        buttons.forEach((candidate) => {
          const active = candidate === button;
          candidate.classList.toggle('is-active', active);
          candidate.setAttribute('aria-pressed', String(active));
        });
        root.querySelectorAll('.tab-panel').forEach((panel) => {
          panel.classList.toggle('is-active', panel.id === panelId);
        });
      });
    });
  });
  function setProgress(activeId) {
    const index = Math.max(0, conceptSections.findIndex((section) => section.id === activeId));
    const total = conceptSections.length || 1;
    const pct = activeId && /^FL\d+$/.test(activeId) ? Math.round(((index + 1) / total) * 100) : 0;
    progressFill.style.width = `${pct}%`;
    progressText.textContent = `${pct}%`;
  }
  function setActiveLink(id) {
    navLinks.forEach((link) => {
      const active = link.dataset.id === id;
      link.classList.toggle('active', active);
      link.setAttribute('aria-current', active ? 'location' : 'false');
      if (active) {
        const group = link.closest('.nav-group');
        group?.classList.remove('collapsed');
        group?.querySelector('.group-toggle')?.setAttribute('aria-expanded', 'true');
      }
    });
    setProgress(id);
  }
  const observer = new IntersectionObserver((entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
    if (!visible.length) return;
    setActiveLink(visible[0].target.id);
  }, { rootMargin: '-18% 0px -58% 0px', threshold: [0.2, 0.45, 0.7] });
  sections.forEach((section) => observer.observe(section));
  document.querySelectorAll('.group-toggle').forEach((button) => {
    button.addEventListener('click', () => {
      const group = button.closest('.nav-group');
      const collapsed = group.classList.toggle('collapsed');
      button.setAttribute('aria-expanded', String(!collapsed));
    });
  });
  collapseAll.addEventListener('click', () => {
    document.querySelectorAll('.nav-group').forEach((group) => {
      group.classList.add('collapsed');
      group.querySelector('.group-toggle')?.setAttribute('aria-expanded', 'false');
    });
  });
  expandAll.addEventListener('click', () => {
    document.querySelectorAll('.nav-group').forEach((group) => {
      group.classList.remove('collapsed');
      group.querySelector('.group-toggle')?.setAttribute('aria-expanded', 'true');
    });
  });
  function filterNav(value) {
    const term = value.trim().toLowerCase();
    document.querySelectorAll('.nav-group').forEach((group) => {
      const links = [...group.querySelectorAll('.group-links a')];
      let visibleCount = 0;
      links.forEach((link) => {
        const text = `${link.dataset.id} ${link.dataset.label || ''}`.toLowerCase();
        const visible = !term || text.includes(term);
        link.hidden = !visible;
        if (visible) visibleCount += 1;
      });
      group.hidden = visibleCount === 0;
    });
  }
  searchInput.addEventListener('input', (event) => filterNav(event.target.value));
  document.addEventListener('keydown', (event) => {
    if (event.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName || '')) {
      event.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });
  wsgiToggle.addEventListener('click', () => {
    wsgiVisible = !wsgiVisible;
    document.body.classList.toggle('show-wsgi', wsgiVisible);
    document.querySelectorAll('.wsgi-box').forEach((box) => {
      box.hidden = !wsgiVisible;
    });
    wsgiToggle.textContent = wsgiVisible ? 'Hide WSGI equivalents' : 'Show WSGI equivalents';
  });
  mobileToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
  function updateScrollState() { backToTop.classList.toggle('visible', window.scrollY > 700); }
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  window.addEventListener('scroll', updateScrollState, { passive: true });
  updateScrollState();
  if (window.mermaid && typeof window.mermaid.initialize === 'function') {
    window.mermaid.initialize({ startOnLoad: true, securityLevel: 'loose', theme: 'dark' });
  }
  const initial = window.location.hash.slice(1);
  if (initial) setActiveLink(initial);
  else if (sections[0]) setActiveLink(sections[0].id);
});
</script>
</body>
</html>
"""


CONCEPTS = []

CONCEPTS.extend(
    [
        c(
            "FL01",
            0,
            "foundation",
            "How the Web Works for Flask",
            [],
            "HTTP is the request/response contract Flask lives on top of, not a detail hidden below the framework.",
            "If you only know decorators, debugging headers, redirects, cookies, caching, or proxy behavior feels like random framework magic.",
            "Flask lets you think in terms of requests and responses while a WSGI server handles socket I/O and HTTP parsing.",
            "A server accepts bytes, parses HTTP, produces a WSGI environ, and only then does Flask dispatch your view and build a response iterable.",
            RAW_SOCKET_SERVER,
            wsgi_code=MINIMAL_WSGI_APP,
            before_code=RAW_SOCKET_SERVER,
            after_code="""from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
    return "hello"
""",
            extra_examples=[
                ex(
                    "Raw HTTP Request / Response",
                    "Flask never changes the protocol contract itself; it just gives you better objects for working with it.",
                    code=RAW_HTTP_LOGIN + "\n" + RAW_HTTP_RESPONSE,
                    kind="http",
                    note="Read the method, path, headers, cookies, and body as separate pieces because Flask maps each one into a request attribute later.",
                )
            ],
        ),
        c(
            "FL02",
            0,
            "foundation",
            "WSGI - The Contract",
            [],
            "WSGI is the narrow Python callable contract between a web server and a synchronous Python web application.",
            "Without WSGI, every server would expose a different API and Flask could not run consistently behind Werkzeug, Gunicorn, or uWSGI.",
            "Flask is itself a WSGI app: the server calls it with `environ` and `start_response`, and Flask returns an iterable of response bytes.",
            "Werkzeug wraps the low-level WSGI objects into Request and Response helpers, but Flask's `app.wsgi_app` still speaks plain WSGI.",
            MINIMAL_WSGI_APP,
            before_code=MINIMAL_WSGI_APP,
            after_code="""from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
    return "hello from Flask"

print(callable(app))
print(callable(app.wsgi_app))
""",
            extra_examples=[
                ex(
                    "What `environ` looks like",
                    "These keys are the raw material Flask turns into `request`.",
                    code="""{
    "REQUEST_METHOD": "GET",
    "PATH_INFO": "/products/42",
    "QUERY_STRING": "preview=1",
    "SERVER_NAME": "127.0.0.1",
    "SERVER_PORT": "8000",
    "wsgi.url_scheme": "http",
    "CONTENT_TYPE": "",
    "HTTP_HOST": "127.0.0.1:8000"
}""",
                    lang="text",
                    note="The WSGI server normalizes transport details into a dictionary so frameworks can stay portable.",
                )
            ],
            version="Flask 2.x and 3.x are both WSGI-first. Async views arrived in 2.0, but the primary callable exposed by Flask is still a WSGI application in 3.x.",
        ),
        c(
            "FL03",
            0,
            "foundation",
            "Flask's Philosophy",
            [],
            "Flask is a microframework: routing, request/response handling, and Jinja2 templating are core; almost everything else is opt-in.",
            "Teams expecting Django-style batteries can accidentally build a pile of ad-hoc globals because Flask intentionally leaves many choices to you.",
            "Flask stays small so you can assemble the exact stack an API, microservice, or prototype needs instead of inheriting a full application framework up front.",
            "Werkzeug provides the HTTP and routing layer, Jinja2 provides templating, and extensions follow `init_app()` so the core stays tiny.",
            """from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    login_manager.init_app(app)
    return app
""",
            other_label="Django / FastAPI",
            comparison=(
                "You choose every layer yourself, including routing, persistence, auth, docs, and deployment.",
                "Flask gives you a thin, explicit core and lets you add exactly the extensions your application shape needs.",
                "Django is stronger for admin-heavy full-stack apps; FastAPI is stronger when typed API contracts and ASGI-native behavior are central.",
            ),
            extra_examples=[
                ex(
                    "Opinionated stack snapshot",
                    "Pinning extension versions keeps a Flask app reproducible because your batteries are external packages.",
                    code=CORE_REQUIREMENTS + "\n" + DATA_REQUIREMENTS + "\n" + AUTH_REQUIREMENTS,
                    lang="text",
                    note="Flask's flexibility is only an advantage if the chosen stack is explicit and versioned.",
                )
            ],
        ),
        c(
            "FL04",
            0,
            "foundation",
            "Flask Application Object",
            [],
            "`Flask(__name__)` creates the central application object that stores config, URL rules, Jinja setup, and extension state.",
            "A hidden or globally mutated app object makes imports brittle, testing awkward, and configuration precedence hard to reason about.",
            "Flask centralizes shared application state in the app object and exposes `current_app` inside an application context when direct imports are the wrong tool.",
            "`__name__` tells Flask where the package lives so templates and static files can be discovered relative to the module path.",
            """from flask import Flask, current_app

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DefaultConfig")
    app.config.from_pyfile("local_settings.py", silent=True)

    @app.get("/config-check")
    def config_check():
        return {"debug": current_app.config["DEBUG"]}

    return app
""",
            extra_examples=[
                ex(
                    "Configuration precedence",
                    "Flask applies later config loaders on top of earlier ones.",
                    code="""class DefaultConfig:
    DEBUG = False
    SITE_NAME = "Shop"

app.config.from_object(DefaultConfig)
app.config.from_envvar("SHOP_SETTINGS", silent=True)
app.config.from_mapping(SITE_NAME="Shop DEV")
""",
                    note="A factory can swap config objects per environment or test case without mutating a module-level singleton.",
                )
            ],
        ),
        c(
            "FL05",
            0,
            "foundation",
            "Flask Development Server",
            [],
            "The built-in development server is for local feedback loops only: reloader, debugger, and interactive tracebacks.",
            "If you deploy the dev server, you lose robust worker management, hardened request handling, and safe failure modes.",
            "Flask gives fast iteration locally with `--debug`, but production should run the WSGI app under Gunicorn or a comparable process manager.",
            "The reloader runs a parent watcher plus a child process; the debugger can execute code in-process, which is why leaving it exposed is dangerous.",
            """flask --app shop run --debug
""",
            sample_lang="bash",
            before_code="""python app.py
""",
            before_lang="bash",
            after_code="""flask --app shop run --debug
""",
            after_lang="bash",
            extra_examples=[
                ex(
                    "Production handoff",
                    "The correct deployment target is the Flask app object or factory, not `app.run()`.",
                    code="""gunicorn -w 4 "shop:create_app()"
""",
                    lang="bash",
                    note="Keep the debugger and auto-reloader for local development only.",
                )
            ],
            version="Flask 3.x removed the old `FLASK_ENV=development` workflow. Prefer `flask --app shop run --debug` or CLI flags instead of environment tricks from older tutorials.",
        ),
        c(
            "FL06",
            1,
            "routing",
            "Route Registration",
            ["FL01", "FL02", "FL03", "FL04"],
            "Routes map a URL rule and allowed methods to an endpoint function.",
            "Without a routing table, every request becomes a manual tree of path and method checks that grows harder to test and rename.",
            "Flask registers routes declaratively through decorators or `add_url_rule()`, while Werkzeug keeps the actual URL map and endpoint resolution.",
            "Decorators eventually call `add_url_rule()`, which creates `Rule` objects stored in the app's `url_map`.",
            """from flask import Flask

app = Flask(__name__)

@app.get("/products")
def list_products():
    return {"items": []}

@app.post("/products")
def create_product():
    return {"ok": True}, 201
""",
            extra_examples=[
                ex(
                    "Decorator and `add_url_rule()` are the same mechanism",
                    "The decorator is just nicer syntax around explicit URL rule registration.",
                    code="""def health():
    return {"status": "ok"}

app.add_url_rule("/health", view_func=health, methods=["GET"])
""",
                    note="GET is the default because it is the safest and most cache-friendly method for browsers to prefetch or revisit.",
                )
            ],
        ),
        c(
            "FL07",
            1,
            "routing",
            "URL Variables",
            ["FL06"],
            "URL converters turn path segments into typed Python values before your view runs.",
            "If every route receives only strings, validation and path parsing leak into every view function.",
            "Flask lets you declare converters like `int`, `uuid`, or custom regex-backed converters on the route itself.",
            "Werkzeug's router matches the path, validates converter rules, and passes typed arguments into the endpoint function.",
            """from werkzeug.routing import BaseConverter

class SlugConverter(BaseConverter):
    regex = r"[a-z0-9-]+"

app.url_map.converters["slug"] = SlugConverter

@app.get("/blog/<slug:post_slug>")
def post_detail(post_slug):
    return {"slug": post_slug}
""",
        ),
        c(
            "FL08",
            1,
            "routing",
            "URL Building",
            ["FL06"],
            "`url_for()` resolves endpoint names into URLs so route refactors do not become search-and-replace exercises.",
            "Hardcoded paths drift from the actual router quickly, especially once blueprints, prefixes, or external URLs appear.",
            "Flask stores endpoint names for every rule and `url_for()` asks the router to build the correct path with variables and query strings.",
            "URL generation needs an app or request context because Flask resolves the active URL adapter from current application state.",
            """from flask import redirect, url_for

@app.post("/checkout")
def checkout():
    return redirect(url_for("order_success", order_id=42, coupon="SAVE10"))

@app.get("/orders/<int:order_id>/success")
def order_success(order_id):
    return {"order_id": order_id}
""",
            extra_examples=[
                ex(
                    "External URLs for emails",
                    "Emails and webhooks usually need fully qualified links instead of relative paths.",
                    code="""with app.app_context():
    reset_link = url_for("auth.reset_password", token="abc", _external=True, _scheme="https")
""",
                    note="Calling `url_for()` outside a context raises a runtime error because no URL adapter is available.",
                )
            ],
        ),
        c(
            "FL09",
            1,
            "routing",
            "Blueprints",
            ["FL06", "FL07", "FL08"],
            "Blueprints are deferred collections of routes, templates, and static assets that let a Flask app grow past a single file.",
            "A 500-line `app.py` quickly turns into a circular-import and ownership problem once auth, admin, and API routes multiply.",
            "Blueprints let features register themselves against the application later, usually inside the factory.",
            "A blueprint stores registration operations until `app.register_blueprint()` attaches them to the final URL map and template loader.",
            """from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")

@auth_bp.get("/login")
def login():
    return "login page"

def register_blueprints(app):
    app.register_blueprint(auth_bp)
""",
            extra_examples=[
                ex(
                    "Blueprint-specific templates and errors",
                    "Feature packages can keep their templates and handlers close to the routes they serve.",
                    code="""@auth_bp.app_errorhandler(401)
def unauthorized(error):
    return {"error": "login required"}, 401

# package layout
# auth/templates/auth/login.html
""",
                    note="Blueprint endpoint names are prefixed, so `url_for('auth.login')` stays unambiguous.",
                )
            ],
        ),
        c(
            "FL10",
            1,
            "routing",
            "Application Factory Pattern",
            ["FL09"],
            "The app factory pattern builds a new Flask app on demand so tests, CLI commands, and different configs do not share one mutable singleton.",
            "A global app object and import-time extension binding create circular imports fast, especially once models and blueprints grow.",
            "With `create_app()`, extensions are created once without an app and initialized later with `init_app()` inside the factory.",
            "The factory delays configuration, blueprint registration, and extension initialization until the application is fully constructed.",
            """from flask import Flask
from .extensions import db, migrate

def create_app(config_object="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)
    from .routes import web_bp
    app.register_blueprint(web_bp)
    return app
""",
            extra_examples=[
                ex(
                    "Circular import that breaks",
                    "This is the classic failure the factory pattern avoids.",
                    code="""# app.py
db = SQLAlchemy(app)
from .models import Product

# models.py
from .app import db
""",
                    note="Move extension objects to `extensions.py`, keep them unbound, and initialize them inside `create_app()`.",
                )
            ],
            version="The factory pattern works the same in Flask 2.x and 3.x. What changed over time is CLI/debug behavior around startup, not the pattern itself.",
        ),
    ]
)

CONCEPTS.extend(
    [
        c(
            "FL54",
            11,
            "production",
            "Flask Security Hardening",
            ["FL32", "FL34", "FL39", "FL53"],
            "Flask security hardening is the disciplined combination of framework defaults, browser headers, TLS, cookie settings, and input validation.",
            "Security bugs rarely come from one missing line; they come from leaving trust boundaries implicit across templates, forms, cookies, and deployment.",
            "Flask gives good primitives, but you must wire the final policy: HTTPS redirects, CSP, secure cookies, CSRF, XSS defense, and SQL injection prevention.",
            "Most hardening lives in config and `after_request` hooks because the browser enforces headers only when the server sends them consistently.",
            """@app.after_request
def apply_security_headers(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data:; script-src 'self'"
    return response
""",
            extra_examples=[
                ex(
                    "Cookie and CSRF settings",
                    "These settings close off a large class of browser-side attacks when used together.",
                    code="""app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    WTF_CSRF_TIME_LIMIT=3600,
)
""",
                    note="Jinja autoescaping helps with XSS, Flask-WTF helps with CSRF, and SQLAlchemy parameter binding helps with injection. They work best together, not in isolation.",
                )
            ],
            security="Use HTTPS everywhere, strong secret keys, secure cookie flags, CSRF protection for browser forms, parameterized queries, CSP, and frame-busting headers. A single missing piece weakens the rest.",
        ),
        c(
            "FL55",
            11,
            "production",
            "Performance Optimization",
            ["FL24", "FL25", "FL26", "FL47", "FL53"],
            "Flask performance work usually means measuring SQL, controlling cache behavior, compressing responses, and tuning the serving stack rather than micro-optimizing Python syntax.",
            "The biggest latency wins usually come from fewer queries, fewer bytes, and fewer repeated computations, not from rewriting a list comprehension.",
            "Flask gives you clean places to add caching, ETags, compression, and profiling once you have measured a real bottleneck.",
            "Werkzeug can profile requests, SQLAlchemy exposes the generated SQL, and HTTP caching headers let browsers and CDNs do work for you.",
            """app.config.update(
    SQLALCHEMY_ENGINE_OPTIONS={"pool_size": 10, "pool_recycle": 1800},
)

@app.get("/products/<int:product_id>")
def product_detail(product_id):
    response = make_response(product_schema.dump(db.session.get(Product, product_id)))
    response.set_etag(f"product-{product_id}")
    response.cache_control.max_age = 60
    return response
""",
            extra_examples=[
                ex(
                    "Measure the query plan",
                    "Query tuning starts with the database's explanation of the SQL you actually generated.",
                    code="""rows = db.session.execute(text("EXPLAIN ANALYZE SELECT * FROM product WHERE sku = :sku"), {"sku": "LAMP-01"}).all()
for row in rows:
    print(row[0])
""",
                    note="Compression and caching can help a lot, but they do not excuse slow query plans or N+1 relationships.",
                )
            ],
        ),
        c(
            "FL56",
            11,
            "production",
            "Production Deployment",
            ["FL10", "FL45", "FL54", "FL55"],
            "Production Flask deployment is the disciplined assembly of a WSGI server, reverse proxy, configuration, containers, health checks, and graceful shutdown behavior.",
            "A Flask app that works on `localhost` is not yet a reliable service. Deployment adds worker management, TLS termination, secrets, readiness, and surrounding infrastructure.",
            "Gunicorn, nginx, Docker, and environment-based config are a common Flask deployment stack because Flask intentionally leaves those choices to you.",
            "Gunicorn imports the WSGI app, forks worker processes, and lets nginx handle TLS termination, buffering, and static files before requests reach Flask.",
            """gunicorn -w 4 -k gthread --threads 4 --bind 0.0.0.0:8000 "shop:create_app()"
""",
            sample_lang="bash",
            extra_examples=[
                ex(
                    "Multi-stage Dockerfile",
                    "A small runtime image reduces attack surface and build drift.",
                    code="""FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
CMD ["gunicorn", "-w", "4", "wsgi:app"]
""",
                    lang="docker",
                    note="Worker math depends on workload. If each request blocks for 200ms and you have 4 CPUs, 4-8 workers is a common starting point before measurement.",
                ),
                ex(
                    "Compose the stack",
                    "The app rarely runs alone in production; it needs a database, cache, and worker processes around it.",
                    code="""services:
  web:
    build: .
    command: gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
  db:
    image: postgres:17
  redis:
    image: redis:7
  worker:
    build: .
    command: celery -A shop.celery_app worker -l info
""",
                    lang="yaml",
                    note="Expose `/health` for liveness checks and let Gunicorn handle graceful worker shutdown instead of killing requests mid-flight.",
                ),
            ],
        ),
        c(
            "FL57",
            11,
            "production",
            "Logging & Monitoring",
            ["FL10", "FL45", "FL53"],
            "Logging and monitoring turn a Flask app from something that runs into something you can actually operate during failures.",
            "Without request IDs, structured logs, error reporting, and metrics, every incident becomes guesswork.",
            "Flask exposes `app.logger`, but production observability usually adds JSON logs, error aggregation, tracing IDs, and metrics exporters.",
            "The logger hangs off the app object, so factory-created apps can still attach structured handlers and middleware during startup.",
            """from pythonjsonlogger import jsonlogger
import logging

handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(message)s %(request_id)s"))
app.logger.handlers = [handler]
app.logger.setLevel(logging.INFO)
""",
            extra_examples=[
                ex(
                    "Install observability stack",
                    "These packages cover errors, metrics, and structured output without changing Flask's core model.",
                    code=OBSERVABILITY_REQUIREMENTS,
                    lang="text",
                    note="Pair JSON logs with stdout/stderr collection in containers and include a request ID in every log line for traceability.",
                ),
                ex(
                    "Sentry and Prometheus hooks",
                    "Production monitoring should include both errors and service-level metrics.",
                    code="""sentry_sdk.init(dsn=app.config["SENTRY_DSN"], integrations=[FlaskIntegration()])
PrometheusMetrics(app, group_by="endpoint")
""",
                    note="Logs tell you what happened; metrics tell you how often and how badly. You need both.",
                ),
            ],
        ),
        c(
            "FL58",
            12,
            "architecture",
            "Application Architecture Patterns",
            ["FL10", "FL24", "FL37", "FL53"],
            "Large Flask apps need explicit architectural boundaries because the framework deliberately does not impose many of them for you.",
            "Without a plan, views become fat orchestrators that validate input, query models, mutate state, call third-party APIs, and render responses all in one place.",
            "Patterns like feature-based packages, service layers, repositories, and dependency injection keep Flask apps testable as they grow.",
            "The app factory helps architecture because extensions, blueprints, and services can be wired in one place instead of imported through a mutable global app.",
            """# views.py
@app.post("/orders")
def create_order():
    payload = order_schema.load(request.get_json())
    order = order_service.create_order(user_id=current_user.id, payload=payload)
    return order_schema.dump(order), 201

# services/orders.py
def create_order(*, user_id, payload):
    ...
""",
            extra_examples=[
                ex(
                    "Feature-based package layout",
                    "Ownership is clearer when routes, schemas, services, and tests for one feature live together.",
                    code="""shop/
  auth/
    routes.py
    services.py
    schemas.py
  orders/
    routes.py
    services.py
    models.py
    tests/
""",
                    lang="text",
                    note="Dependency injection in Flask is usually simple constructor or function injection, not a heavy DI container.",
                )
            ],
        ),
        c(
            "FL59",
            12,
            "architecture",
            "Flask Anti-Patterns & Gotchas",
            ["FL10", "FL24", "FL32", "FL37", "FL53", "FL58"],
            "Flask anti-patterns usually come from treating its flexibility as a reason to skip boundaries, validation, or deployment discipline.",
            "Because Flask lets you do almost anything, it also lets bad patterns survive for a long time before they become obviously expensive.",
            "A mature Flask codebase is mostly the result of avoiding the common traps: global apps, hidden side effects, context misuse, and production shortcuts.",
            "Most Flask 'gotchas' are really lifecycle misunderstandings: import time versus request time, app context versus request context, session versus token, dev server versus WSGI server.",
            """# anti-pattern: import-time app and extension binding
app = Flask(__name__)
db = SQLAlchemy(app)

# anti-pattern: view doing everything
@app.post("/orders")
def create_order():
    ...
""",
            extra_examples=[
                ex(
                    "A few fixes in one pass",
                    "The safest Flask refactors usually restore explicit boundaries instead of adding more magic.",
                    code="""# better
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

@app.post("/orders")
def create_order():
    payload = order_schema.load(request.get_json())
    order = order_service.create_order(user_id=current_user.id, payload=payload)
    return order_schema.dump(order), 201
""",
                    note="Avoid `debug=True` in production, never hardcode URLs, do not catch every exception in views, and do not use `g` as a cache for work that belongs in Redis or the database.",
                ),
                ex(
                    "Flask vs Django for the same shop app",
                    "This comparison clarifies where Flask gives freedom and where Django gives defaults.",
                    code="""Flask:
- choose ORM, auth add-ons, admin add-on, API stack, task queue, cache layer
- explicit factory, explicit extensions, explicit architecture

Django:
- ORM, migrations, auth, admin, templates, forms in core
- less assembly, more framework defaults
""",
                    lang="text",
                    note="Neither choice is universally better; the right answer depends on how much structure your app needs on day one.",
                ),
            ],
        ),
    ]
)

CONCEPTS.extend(
    [
        c(
            "FL46",
            9,
            "extensions",
            "Flask Extension Architecture",
            ["FL10"],
            "A Flask extension is usually an object with optional state plus an `init_app()` method that binds it to a specific app instance later.",
            "If an extension binds itself at import time, factories, tests, and multiple configs all become harder immediately.",
            "The `init_app()` pattern keeps extensions reusable across app instances and aligns with Flask's factory-first composition style.",
            "Extensions typically stash state in `app.extensions[...]`, register teardown hooks or CLI commands, and expose helpers through an object created before any app exists.",
            """class FlaskAudit:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions["audit"] = self

        @app.after_request
        def log_request(response):
            app.logger.info("audit %s %s %s", request.method, request.path, response.status_code)
            return response

audit = FlaskAudit()
""",
            extra_examples=[
                ex(
                    "Custom extension init in the factory",
                    "The extension object is created once and bound per app instance.",
                    code="""def create_app():
    app = Flask(__name__)
    audit.init_app(app)
    return app
""",
                    note="This same pattern is why Flask-SQLAlchemy, Flask-Login, Flask-Caching, and similar packages cooperate well with factories.",
                )
            ],
        ),
        c(
            "FL47",
            9,
            "extensions",
            "Flask-Caching",
            ["FL10"],
            "Caching stores expensive computed results so repeated requests do not redo the same work every time.",
            "If every request recalculates the same product list or dashboard summary, latency and database load rise together.",
            "Flask-Caching adds decorator-based and imperative cache access while keeping backend choice explicit.",
            "The extension keys values by function arguments or explicit cache keys and delegates persistence to a backend like Redis or Memcached.",
            """from flask_caching import Cache

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
    cache.init_app(app)
    return app

@cache.cached(timeout=60, key_prefix="products:index")
def expensive_product_listing():
    return db.session.execute(select(Product).order_by(Product.name)).scalars().all()
""",
            extra_examples=[
                ex(
                    "Install cache tooling",
                    "Cache bugs are hard to diagnose when versions and backends drift between environments.",
                    code=EXTENSION_REQUIREMENTS,
                    lang="text",
                    note="Use `cache.delete_memoized()` or explicit key invalidation when product data changes, otherwise your app serves stale results confidently.",
                )
            ],
        ),
        c(
            "FL48",
            9,
            "extensions",
            "Flask-Mail",
            ["FL10"],
            "Email helpers keep message assembly and SMTP configuration out of views, but delivery should still move to background work for real systems.",
            "Sending mail inline makes request latency unpredictable and turns transient SMTP errors into user-facing failures.",
            "Flask-Mail centralizes SMTP settings and message objects, while Celery or another worker should handle delivery for non-trivial apps.",
            "The extension wraps a configured mail client and uses app config for server, TLS, credentials, and defaults when sending a Message object.",
            """from flask_mail import Mail, Message

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.update(MAIL_SERVER="smtp.example.com", MAIL_PORT=587, MAIL_USE_TLS=True)
    mail.init_app(app)
    return app

def send_welcome_email(user):
    message = Message("Welcome", recipients=[user.email], html=render_template("emails/welcome.html", user=user))
    mail.send(message)
""",
            extra_examples=[
                ex(
                    "Queue email instead of blocking the request",
                    "Delivery belongs in a worker because SMTP is slow and failure-prone compared with ordinary request latency budgets.",
                    code="""@celery_app.task
def send_welcome_email_task(user_id):
    user = db.session.get(User, user_id)
    send_welcome_email(user)
""",
                    note="Pin Flask-Mail and your worker stack together so the integration stays reproducible across environments.",
                )
            ],
        ),
        c(
            "FL49",
            9,
            "extensions",
            "Flask-Admin",
            ["FL10"],
            "Flask-Admin generates an internal CRUD/admin surface from model metadata and custom view classes.",
            "Business teams often need internal data tooling long before you can justify building a bespoke admin application.",
            "Flask-Admin is a fast path for trusted internal operators, but it still needs authentication, authorization, and operational hardening.",
            "The extension registers admin views against an app and uses model metadata plus `ModelView` configuration to build listings, forms, and detail screens.",
            """from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(name="Acme Admin", template_mode="bootstrap4")

class ProductAdmin(ModelView):
    column_list = ("sku", "name", "price", "inventory")
    column_searchable_list = ("sku", "name")

def create_app():
    app = Flask(__name__)
    admin.init_app(app)
    admin.add_view(ProductAdmin(Product, db.session))
    return app
""",
            extra_examples=[
                ex(
                    "Protect the admin",
                    "Admin tooling is powerful, which is exactly why it must sit behind explicit auth checks.",
                    code="""class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
""",
                    note="Use Flask-Admin when you need trusted internal CRUD quickly. Build custom admin UX when workflows or security controls outgrow the generic surface.",
                )
            ],
        ),
        c(
            "FL50",
            9,
            "extensions",
            "Flask-CORS",
            ["FL10"],
            "CORS is a browser security policy about which origins may read cross-origin responses; it is not a server-to-server auth mechanism.",
            "If a browser frontend and Flask API live on different origins, the browser will block responses unless the API sends the correct CORS headers.",
            "Flask-CORS automates the right response headers and preflight behavior, but you still decide which origins and credentials are safe.",
            "Browsers send an `OPTIONS` preflight for many cross-origin writes; Flask-CORS adds the allow-origin, allow-methods, and allow-headers responses needed for the browser to continue.",
            """from flask_cors import CORS

cors = CORS()

def create_app():
    app = Flask(__name__)
    cors.init_app(app, resources={r"/api/*": {"origins": ["https://shop.example.com"]}}, supports_credentials=True)
    return app
""",
            extra_examples=[
                ex(
                    "What the preflight looks like",
                    "Understanding the browser's OPTIONS request makes CORS errors much less mysterious.",
                    code="""OPTIONS /api/products HTTP/1.1
Origin: https://shop.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type, authorization
""",
                    kind="http",
                    note="Never default to `origins='*'` with credentials in production. CORS is part of your browser trust boundary.",
                )
            ],
            security="CORS controls browser reads, not authentication. Restrict origins intentionally, be careful with credentials, and remember that `origin='*'` is usually the wrong production answer.",
        ),
        c(
            "FL51",
            10,
            "testing",
            "Flask Test Client",
            ["FL10", "FL15", "FL37"],
            "The Flask test client issues in-process HTTP requests against the app without running a real server.",
            "Without a test client, route tests either hit a live server or bypass the request lifecycle entirely.",
            "Flask's client exercises routing, request parsing, response creation, and error handling while staying fast enough for ordinary unit and integration tests.",
            "The client builds WSGI environ dictionaries under the hood, so your tests still travel through the same request pipeline as production code.",
            """app.config["TESTING"] = True

with app.test_client() as client:
    response = client.post("/api/products", json={"sku": "LAMP-01", "name": "Desk Lamp", "price": "49.99", "inventory": 8})
    assert response.status_code == 201
    assert response.get_json()["id"] is not None
""",
            extra_examples=[
                ex(
                    "Request context without a client",
                    "Sometimes you want to test context-bound helpers directly rather than round-tripping through a route.",
                    code="""with app.test_request_context("/products?page=2"):
    assert request.args["page"] == "2"
""",
                    note="The test client supports headers, form data, file uploads, cookies, redirects, and every ordinary HTTP method.",
                )
            ],
        ),
        c(
            "FL52",
            10,
            "testing",
            "pytest With Flask",
            ["FL10", "FL24", "FL51"],
            "pytest fixtures make Flask app, client, database, and authenticated-user setup composable instead of repetitive.",
            "If every test bootstraps the app and database manually, test code becomes harder to read than the behavior being asserted.",
            "Flask works especially well with pytest because factories and fixtures line up naturally.",
            "A fixture can create an app, push an app context, initialize a temporary database, and tear it all back down after each test.",
            """import pytest

@pytest.fixture
def app():
    app = create_app("config.TestingConfig")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
""",
            extra_examples=[
                ex(
                    "Testing stack snapshot",
                    "Keep the test tools explicit so the suite behaves the same in CI and locally.",
                    code=TESTING_REQUIREMENTS,
                    lang="text",
                    note="Prefer rollback or recreate-the-db strategies that keep tests isolated. Order-dependent tests are a code smell.",
                )
            ],
        ),
        c(
            "FL53",
            10,
            "testing",
            "Testing Strategies",
            ["FL10", "FL24", "FL37", "FL51", "FL52"],
            "A healthy Flask test suite mixes unit tests, integration tests, and a few higher-level end-to-end checks.",
            "If every test is a full-stack request, the suite gets slow; if every test is isolated mocking, the real integrations never get exercised.",
            "Choose the thinnest test that can prove the behavior: model/service rules in unit tests, request wiring in integration tests, and user journeys sparingly.",
            "Mocks should replace unstable boundaries like third-party APIs, not your own business logic and database semantics everywhere.",
            """def test_product_price_validation():
    with pytest.raises(ValueError):
        ProductService.validate_price(-1)

def test_create_product_endpoint(client):
    response = client.post("/api/products", json={"sku": "L1", "name": "Lamp", "price": "10.00", "inventory": 2})
    assert response.status_code == 201
""",
            extra_examples=[
                ex(
                    "Mocking an external payment API",
                    "This is the kind of boundary mock that keeps tests deterministic without lying about your own code.",
                    code="""@responses.activate
def test_capture_payment():
    responses.post("https://payments.example.com/capture", json={"status": "captured"}, status=200)
    result = payment_service.capture("pay_123")
    assert result["status"] == "captured"
""",
                    note="Coverage numbers tell you what was executed, not whether you tested the right behavior. Treat 80% as a smoke signal, not a trophy.",
                )
            ],
        ),
    ]
)

CONCEPTS.extend(
    [
        c(
            "FL37",
            7,
            "rest",
            "Building REST APIs In Flask",
            ["FL15", "FL28", "FL35"],
            "A REST-style Flask API is just request parsing, validation, business logic, and consistent JSON responses layered over ordinary routes.",
            "If API endpoints start as 'just another route', inconsistent content types and ad-hoc status codes appear immediately.",
            "Pure Flask is enough for a clean API if you enforce JSON input, schema validation, and explicit response envelopes.",
            "A JSON response is still just a Response object with `application/json`; Flask's `jsonify` and dict return values are convenience, not a different runtime path.",
            """@app.get("/api/products")
def list_products():
    products = db.session.execute(select(Product).order_by(Product.name)).scalars().all()
    return {"items": [{"id": p.id, "name": p.name, "price": str(p.price)} for p in products]}

@app.post("/api/products")
def create_product():
    payload = request.get_json()
    product = Product(**payload)
    db.session.add(product)
    db.session.commit()
    return {"id": product.id}, 201
""",
            extra_examples=[
                ex(
                    "Enforce JSON content type",
                    "Rejecting the wrong content type early makes API behavior predictable.",
                    code="""@app.before_request
def require_json_for_api():
    if request.path.startswith("/api/") and request.method in {"POST", "PUT", "PATCH"} and not request.is_json:
        abort(415, description="application/json required")
""",
                    note="Even with pure Flask, every endpoint should return an intentional error body instead of falling through to HTML errors.",
                )
            ],
        ),
        c(
            "FL38",
            7,
            "rest",
            "Flask-RESTX Or Flask-Smorest",
            ["FL37"],
            "REST-focused extensions add request parsing, schema integration, namespacing, and generated OpenAPI documentation on top of ordinary Flask routes.",
            "Pure Flask APIs are fine until consistency, documentation, and repetitive schema wiring start taking more time than the actual business logic.",
            "Flask-Smorest is a strong schema-first option; Flask-RESTX is a resource-class option. Both reduce repetitive API plumbing.",
            "These extensions still sit on Flask's routing and request lifecycle. They add higher-level decorators and metadata, not a new server model.",
            """from flask_smorest import Api, Blueprint

api = Api()
products_blp = Blueprint("products", __name__, url_prefix="/api/products", description="Product operations")

@products_blp.route("/")
class ProductsResource(MethodView):
    @products_blp.response(200, ProductSchema(many=True))
    def get(self):
        return db.session.execute(select(Product)).scalars().all()
""",
            extra_examples=[
                ex(
                    "Install schema-first API tooling",
                    "Documentation and validation are strongest when the schema package versions are pinned with the API extension.",
                    code=REST_REQUIREMENTS,
                    lang="text",
                    note="Whichever extension you choose, keep the `init_app()` pattern so the factory can create different app instances cleanly.",
                )
            ],
        ),
        c(
            "FL39",
            7,
            "rest",
            "Request Validation & Error Handling",
            ["FL37", "FL38"],
            "API validation should reject malformed or impossible input before it reaches persistence or service code.",
            "Without strict validation, bad payloads trigger deep tracebacks, partial writes, and inconsistent client-facing errors.",
            "Flask APIs stay sane when schemas validate types and constraints, and a global handler turns validation failures into one error format.",
            "Marshmallow raises structured validation errors; Flask can catch them and normalize the output into one JSON envelope.",
            """from marshmallow import ValidationError

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return {
        "error": {
            "code": 422,
            "message": "validation failed",
            "details": error.messages,
        }
    }, 422
""",
            extra_examples=[
                ex(
                    "Schema-first create endpoint",
                    "The database should only see already-validated input.",
                    code="""@app.post("/api/products")
def create_product():
    payload = product_schema.load(request.get_json())
    product = Product(**payload)
    db.session.add(product)
    db.session.commit()
    return product_schema.dump(product), 201
""",
                    note="Reject unknown fields or impossible values before business logic. Chaos at the edge becomes chaos everywhere else.",
                )
            ],
        ),
        c(
            "FL40",
            7,
            "rest",
            "API Versioning In Flask",
            ["FL37"],
            "Versioning lets an API evolve without breaking existing clients that rely on older URL and response contracts.",
            "If you change field names or semantics in place, client breakage becomes invisible until production traffic starts failing.",
            "Flask usually versions APIs explicitly with URL prefixes and version-specific blueprints.",
            "Blueprint prefixes make versioned routing straightforward because `/api/v1` and `/api/v2` can register separate handlers cleanly.",
            """api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v2 = Blueprint("api_v2", __name__, url_prefix="/api/v2")

@api_v1.get("/products/<int:product_id>")
def product_v1(product_id):
    return {"id": product_id, "price": "49.99"}

@api_v2.get("/products/<int:product_id>")
def product_v2(product_id):
    return {"id": product_id, "price": {"amount": "49.99", "currency": "USD"}}
""",
            extra_examples=[
                ex(
                    "Deprecation response header",
                    "Versioning is not only routing; it is also communication with client teams.",
                    code="""response = jsonify({"items": []})
response.headers["Sunset"] = "Wed, 31 Dec 2026 23:59:59 GMT"
response.headers["Deprecation"] = "true"
return response
""",
                    note="Prefer additive changes when possible. Versioning is expensive, so use it for real contract breaks rather than every small tweak.",
                )
            ],
        ),
        c(
            "FL41",
            7,
            "rest",
            "OpenAPI / Swagger Documentation",
            ["FL38", "FL39", "FL40"],
            "API docs are part of the product: clients need discoverable endpoints, schemas, auth rules, and error shapes.",
            "If documentation is manual and separate from code, it drifts as soon as the first endpoint changes.",
            "Flask-Smorest and similar tools can generate OpenAPI docs from schemas and view metadata so documentation stays close to the code.",
            "The extension records route metadata during registration, then serves a generated OpenAPI spec and optional Swagger UI or ReDoc frontend.",
            """api = Api(app)
app.config["API_TITLE"] = "Acme Shop API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
""",
            extra_examples=[
                ex(
                    "Schema-driven docs",
                    "The same Marshmallow schema that validates a payload can define the documented request and response contract.",
                    code=REST_REQUIREMENTS,
                    lang="text",
                    note="Generated docs do not replace examples and prose, but they do stop your path, parameter, and schema listings from drifting.",
                )
            ],
        ),
        c(
            "FL42",
            8,
            "async",
            "Async Support In Flask 2.0+",
            ["FL10", "FL13"],
            "Flask supports `async def` view functions, but that does not make the whole framework ASGI-native.",
            "Developers often assume async Flask behaves like FastAPI or Quart and are surprised when the deployment and concurrency model still looks WSGI-first.",
            "Async views help when your view needs to await real async I/O, but Flask's overall request lifecycle and extension ecosystem remain mostly synchronous.",
            "Flask detects coroutine views and awaits them, but the surrounding request handling still runs within the server model you deploy, typically WSGI workers unless you change more of the stack.",
            """@app.get("/quote")
async def quote():
    data = await http_client.get("https://example.com/quote")
    return {"quote": data.json()["quote"]}
""",
            extra_examples=[
                ex(
                    "When async does not help",
                    "Blocking code inside an async view is still blocking code.",
                    code="""@app.get("/report")
async def report():
    pdf = requests.get("https://example.com/report.pdf")  # blocking client
    return {"size": len(pdf.content)}
""",
                    note="If your workload is mostly long-lived async I/O, Quart is usually a better fit because its entire stack is ASGI-native.",
                )
            ],
            version="Async views arrived in Flask 2.0 and remain available in Flask 3.x, but Flask 3.x still is not 'FastAPI with a different decorator set'.",
        ),
        c(
            "FL43",
            8,
            "async",
            "Async Database Access",
            ["FL42"],
            "Async database access in Flask typically means using SQLAlchemy's async session directly rather than Flask-SQLAlchemy's synchronous helpers.",
            "If the rest of the request path is async but the database client is still sync, the async view loses most of its value.",
            "Flask can host async views that use async DB drivers, but you should keep that boundary explicit instead of assuming Flask-SQLAlchemy is async-aware.",
            "SQLAlchemy async uses an async engine and `AsyncSession`; it is a parallel API surface, not just a flag on the synchronous session.",
            """from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://shop:secret@localhost/shop")
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@app.get("/async-products")
async def async_products():
    async with AsyncSessionLocal() as session:
        rows = await session.execute(select(Product).order_by(Product.name))
        return {"items": [p.name for p in rows.scalars()]}
""",
            extra_examples=[
                ex(
                    "Keep sync and async sessions separate",
                    "Mixing them casually makes transaction and lifecycle bugs hard to diagnose.",
                    code="""# sync extension-backed session for regular views
db.session.execute(select(Product))

# async session for async views
await session.execute(select(Product))
""",
                    note="Choose one model per execution path; do not pretend a sync extension magically becomes async because the view is `async def`.",
                )
            ],
        ),
        c(
            "FL44",
            8,
            "async",
            "Background Tasks - Simple",
            ["FL42"],
            "Small background jobs can be started from a view with threads, but that is a stopgap, not a job system.",
            "A detached thread hides failures, drops application context, and disappears on process restarts.",
            "Flask can support small in-process task launches when you explicitly copy context and accept the limitations, but durable work should move to a queue.",
            "The new thread is outside the request lifecycle, so `current_app`, `g`, and database handles are not automatically available there.",
            """from threading import Thread

def send_receipt_email(app, order_id):
    with app.app_context():
        current_app.logger.info("sending receipt for order %s", order_id)

@app.post("/orders/<int:order_id>/receipt")
def receipt(order_id):
    Thread(target=send_receipt_email, args=(current_app._get_current_object(), order_id), daemon=True).start()
    return {"queued": True}
""",
            extra_examples=[
                ex(
                    "Copying request context",
                    "Use this sparingly; it is a convenience, not a full job runner.",
                    code="""from flask import copy_current_request_context

@app.post("/audit")
def audit():
    @copy_current_request_context
    def write_log():
        current_app.logger.info("audit for %s", request.path)
    Thread(target=write_log, daemon=True).start()
    return {"queued": True}
""",
                    note="Threads do not give you retries, durability, scheduling, or central visibility. Celery exists for those reasons.",
                )
            ],
        ),
        c(
            "FL45",
            8,
            "async",
            "Celery With Flask",
            ["FL42", "FL44"],
            "Celery moves slow or retryable work out of the request cycle and into workers that can retry, schedule, and monitor tasks independently.",
            "Email, image processing, webhooks, and scheduled jobs become fragile when they live inside request threads.",
            "Flask integrates with Celery by sharing config and explicitly pushing an app context inside tasks when they need Flask resources.",
            "A Celery worker is a separate process. If task code wants `current_app`, database config, or templates, you must bridge Flask context into that worker code explicitly.",
            """from celery import Celery

celery_app = Celery(__name__)

def init_celery(app):
    celery_app.conf.update(app.config["CELERY"])

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
""",
            extra_examples=[
                ex(
                    "Install queue tooling",
                    "Pin the worker stack because task serialization and broker behavior are operational dependencies.",
                    code=EXTENSION_REQUIREMENTS,
                    lang="text",
                    note="Use `celery beat` for scheduled tasks and keep the app-factory integration explicit instead of importing a global Flask app from the worker.",
                ),
                ex(
                    "Declaring a task",
                    "Tasks should be regular functions with clean inputs so retries and monitoring stay understandable.",
                    code="""@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def send_order_receipt(self, order_id):
    order = db.session.get(Order, order_id)
    current_app.logger.info("sending receipt to %s", order.user.email)
""",
                    note="A task queue is the right tool when failure handling matters. Threads are the wrong abstraction for business-critical background work.",
                )
            ],
        ),
    ]
)

CONCEPTS.extend(
    [
        c(
            "FL29",
            5,
            "forms",
            "WTForms With Flask-WTF",
            ["FL16", "FL24"],
            "Flask-WTF layers CSRF handling and Flask integration on top of WTForms so forms become typed, validated Python objects.",
            "Parsing POST fields manually spreads validation rules across views and templates and makes redisplaying errors tedious.",
            "Flask-WTF centralizes field definitions, validators, and CSRF checks in a form class that the view can validate in one step.",
            "WTForms coerces incoming strings into typed fields, runs validators, and stores error lists for templates to display after failed validation.",
            """from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

class ProductForm(FlaskForm):
    sku = StringField("SKU", validators=[DataRequired(), Length(max=32)])
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    price = DecimalField("Price", validators=[DataRequired(), NumberRange(min=0.01)])
    inventory = IntegerField("Inventory", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Save")
""",
            extra_examples=[
                ex(
                    "Package versions for forms",
                    "WTForms and Flask-WTF move together in practice, so pinning them reduces upgrade surprises.",
                    code="""Flask-WTF==1.2.2
WTForms==3.2.1
""",
                    lang="text",
                    note="Use `validate_on_submit()` in the view to combine method checking and validation in one place.",
                ),
                ex(
                    "Custom validator hitting the database",
                    "Cross-field or uniqueness validation usually needs application data.",
                    code="""def validate_sku(self, field):
    exists = db.session.execute(select(Product).where(Product.sku == field.data)).scalar_one_or_none()
    if exists:
        raise ValidationError("SKU already exists")
""",
                    note="The CSRF token is derived from a secret and session context, so missing or forged form submissions fail validation before your business logic runs.",
                ),
            ],
        ),
        c(
            "FL30",
            5,
            "forms",
            "File Upload",
            ["FL16", "FL24"],
            "File uploads arrive in `request.files` as `FileStorage` objects and need validation before they ever reach disk.",
            "If you trust the browser-supplied filename or MIME type, path traversal and disguised executable payloads become easy attacks.",
            "Flask exposes uploads cleanly, but safe handling is your responsibility: sanitize names, restrict types, and store outside the code tree.",
            "Werkzeug streams multipart uploads into `FileStorage`, which gives you metadata and a file-like stream without automatically making the file safe.",
            """from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

@app.post("/products/<int:product_id>/image")
def upload_image(product_id):
    file = request.files["image"]
    filename = secure_filename(file.filename)
    file.save(Path(app.config["UPLOAD_FOLDER"]) / filename)
    return {"filename": filename}, 201
""",
            extra_examples=[
                ex(
                    "Checking extension and magic bytes",
                    "Extensions help, but content sniffing is what catches a `.jpg` full of non-image bytes.",
                    code="""def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

signature = file.stream.read(8)
file.stream.seek(0)
if signature.startswith(b"\\x89PNG") is False:
    abort(400, description="invalid image bytes")
""",
                    note="Save uploads outside the package directory and serve them through a controlled media path, not directly from source folders.",
                )
            ],
        ),
        c(
            "FL31",
            5,
            "forms",
            "Flash Messages",
            ["FL16"],
            "Flash messages are one-request-later notifications stored in the session, ideal for post-redirect-get feedback.",
            "Without flash messages, successful form submissions and validation feedback either disappear after a redirect or get awkwardly shoved into query strings.",
            "Flask stores flash messages in the session so the next request can render them and then consume them.",
            "A flash entry is serialized into session state, which is why flashing depends on the session system and a valid secret key.",
            """from flask import flash, redirect, render_template, url_for

@app.post("/profile")
def update_profile():
    flash("Profile updated", "success")
    return redirect(url_for("profile"))

@app.get("/profile")
def profile():
    return render_template("profile.html")
""",
            extra_examples=[
                ex(
                    "Template rendering of flash messages",
                    "Categories let templates style success, warning, and error messages consistently.",
                    code="""{% with messages = get_flashed_messages(with_categories=True) %}
  {% for category, message in messages %}
    <div class="flash flash-{{ category }}">{{ message }}</div>
  {% endfor %}
{% endwith %}
""",
                    lang="jinja",
                    note="Because flashes ride in the session, very large messages are a bad fit for cookie-backed sessions.",
                )
            ],
        ),
        c(
            "FL32",
            6,
            "auth",
            "Flask Sessions",
            ["FL12", "FL24"],
            "Flask sessions keep per-browser state across requests, usually in a signed client-side cookie unless you switch to a server-side extension.",
            "Without sessions, login state, CSRF state, carts, and post-redirect messages disappear after each request.",
            "Flask signs session cookies with `SECRET_KEY`, letting the browser store session data while the server verifies it was not tampered with.",
            "The default session implementation serializes data, signs it with itsdangerous, and sends it back as a cookie on each response.",
            """app.config.update(
    SECRET_KEY="change-me",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

@app.post("/cart")
def add_to_cart():
    session.setdefault("cart", []).append({"product_id": 1, "qty": 2})
    session.modified = True
    return {"items": session["cart"]}
""",
            extra_examples=[
                ex(
                    "Server-side sessions with Redis",
                    "Client-side signed cookies are fine for small state, but Redis-backed sessions keep large or sensitive server-managed data off the client.",
                    code=AUTH_REQUIREMENTS + "\n" + """from flask_session import Session

server_session = Session()

def create_app():
    app = Flask(__name__)
    app.config["SESSION_TYPE"] = "redis"
    server_session.init_app(app)
    return app
""",
                    lang="text",
                    note="A signed cookie is not encrypted. Users cannot safely change it, but they can still inspect its contents.",
                )
            ],
            security="`SECRET_KEY` must be high-entropy and private because it protects session integrity, CSRF tokens, and other signed data. Also set `Secure`, `HttpOnly`, and `SameSite` cookie flags deliberately.",
        ),
        c(
            "FL33",
            6,
            "auth",
            "Flask-Login",
            ["FL12", "FL24"],
            "Flask-Login manages browser login state, `current_user`, login-required routes, and remember-me behavior.",
            "Hand-rolling session-backed auth invites bugs around user loading, unauthorized redirects, and stale session state.",
            "Flask-Login focuses only on session authentication and leaves registration, password reset, and roles to your application or other extensions.",
            "The extension stores user IDs in the session and resolves them through `user_loader` on each request to populate `current_user`.",
            """from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.post("/auth/login")
def login():
    user = db.session.execute(select(User).where(User.email == request.form["email"])).scalar_one_or_none()
    login_user(user, remember=True)
    return redirect(url_for("dashboard"))
""",
            extra_examples=[
                ex(
                    "Install auth stack",
                    "Pin the packages around login, JWT, and OAuth together so auth flows stay reproducible.",
                    code=AUTH_REQUIREMENTS,
                    lang="text",
                    note="`fresh_login_required` is useful for sensitive actions like changing an email or password after a remembered session restores the user.",
                )
            ],
        ),
        c(
            "FL34",
            6,
            "auth",
            "Password Security",
            ["FL24", "FL33"],
            "Passwords must be stored as one-way hashes, not plaintext or decryptable values.",
            "If the user table leaks and you stored plaintext or weak hashes, the breach becomes immediate credential compromise everywhere those users reused passwords.",
            "Flask apps usually rely on Werkzeug's password hashing helpers or Bcrypt wrappers so verification stays slow and one-way.",
            "Hash functions like scrypt or PBKDF2 intentionally cost time and CPU; verification compares the submitted password against the stored hash, not the original password.",
            """from werkzeug.security import check_password_hash, generate_password_hash

password_hash = generate_password_hash("super-secret-password")

if check_password_hash(password_hash, "super-secret-password"):
    print("valid")
""",
            extra_examples=[
                ex(
                    "Constant-time secret comparison",
                    "Timing differences in naive string comparison can leak information about secrets.",
                    code="""import hmac

if hmac.compare_digest(expected_reset_token, submitted_reset_token):
    rotate_password()
""",
                    note="Password policy, rate limiting, and breach-password checks matter too, but none of them replace proper hashing.",
                )
            ],
            security="Never store plaintext passwords. Use a slow password hash, rate-limit login attempts, rotate reset tokens, and compare sensitive values with constant-time functions where appropriate.",
        ),
        c(
            "FL35",
            6,
            "auth",
            "JWT Authentication",
            ["FL24", "FL33"],
            "JWT auth is a stateless token strategy that often fits APIs, but it trades the simplicity of sessions for explicit token lifecycle management.",
            "Teams often reach for JWT because it sounds modern, then discover refresh flows, revocation, storage rules, and rotation policies are now their problem.",
            "Flask-JWT-Extended gives access and refresh token helpers, decorators, and callbacks so stateless auth stays explicit instead of ad hoc.",
            "JWTs are signed payloads, not sessions. Validation checks signature, expiry, and claims on every request, often without any database hit unless you add revocation checks.",
            """from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required

jwt = JWTManager()

@app.post("/api/login")
def api_login():
    identity = {"user_id": 7, "role": "customer"}
    return {
        "access": create_access_token(identity=identity),
        "refresh": create_refresh_token(identity=identity),
    }

@app.get("/api/me")
@jwt_required()
def me():
    return {"identity": get_jwt_identity()}
""",
            extra_examples=[
                ex(
                    "Blocklist-based revocation",
                    "Once you mint long-lived tokens, you need a story for invalidating them early.",
                    code="""BLOCKLIST = set()

@jwt.token_in_blocklist_loader
def token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST
""",
                    note="Use short-lived access tokens and longer-lived refresh tokens. JWT is not automatically better than sessions for browser apps.",
                )
            ],
            security="JWTs are signed, not magically safe. Store them carefully, rotate refresh tokens, validate audience/issuer claims when relevant, and keep a revocation strategy for logout or compromise.",
        ),
        c(
            "FL36",
            6,
            "auth",
            "OAuth2 / Social Login",
            ["FL24", "FL33"],
            "OAuth2 lets a Flask app delegate authentication to another provider using a well-defined redirect and token exchange flow.",
            "Implementing OAuth by hand is easy to get wrong because state verification, callback URLs, token storage, and provider quirks all matter.",
            "Authlib or Flask-Dance wrap the authorization code flow so your Flask app can redirect, validate state, exchange codes, and store provider tokens safely.",
            "The browser never gets the client secret. The app sends the user to the provider, verifies the returned state and code, then exchanges the code server-to-server for tokens.",
            """from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def create_app():
    app = Flask(__name__)
    oauth.init_app(app)
    oauth.register(
        name="github",
        client_id=app.config["GITHUB_CLIENT_ID"],
        client_secret=app.config["GITHUB_CLIENT_SECRET"],
        access_token_url="https://github.com/login/oauth/access_token",
        authorize_url="https://github.com/login/oauth/authorize",
        client_kwargs={"scope": "user:email"},
    )
    return app
""",
            extra_examples=[
                ex(
                    "Authorization code callback",
                    "The callback must verify state before trusting the returned code.",
                    code="""@app.get("/auth/github")
def github_login():
    redirect_uri = url_for("github_callback", _external=True, _scheme="https")
    return oauth.github.authorize_redirect(redirect_uri)

@app.get("/auth/github/callback")
def github_callback():
    token = oauth.github.authorize_access_token()
    profile = oauth.github.get("user").json()
    return profile
""",
                    note="Store provider tokens carefully and treat the `state` parameter as a CSRF defense, not an optional extra.",
                )
            ],
        ),
    ]
)

CONCEPTS.extend(
    [
        c(
            "FL23",
            4,
            "data",
            "Connecting To A Database - Options",
            ["FL10", "FL13"],
            "Flask can talk to a database directly with `sqlite3` or through a higher-level ORM; the right starting point is understanding the lifecycle cost of manual connections.",
            "Opening connections ad hoc inside views leads to leaked handles, repeated boilerplate, and code that does not scale beyond a toy SQLite app.",
            "Flask's app and request contexts make manual connection management possible, but the pain is exactly what motivates an ORM and proper extension wiring.",
            "Using `g` plus `teardown_appcontext` creates a per-request connection lifecycle, which is the same resource pattern many extensions automate.",
            """import sqlite3
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db:
        db.close()
""",
            extra_examples=[
                ex(
                    "A route using the manual connection",
                    "This is workable for SQLite demos and teaching, but it becomes repetitive quickly.",
                    code="""@app.get("/products")
def products():
    rows = get_db().execute("SELECT id, name, price FROM product ORDER BY id").fetchall()
    return {"items": [dict(row) for row in rows]}
""",
                    note="PostgreSQL, MySQL, pooling, migrations, and relationships all push you toward a richer data layer.",
                )
            ],
        ),
        c(
            "FL24",
            4,
            "data",
            "Flask-SQLAlchemy",
            ["FL23"],
            "Flask-SQLAlchemy integrates SQLAlchemy's engine, session, and model base with the app factory and request lifecycle.",
            "Manual SQL quickly turns into duplicated connection, transaction, and row-mapping code once the app gains relationships and business rules.",
            "Flask-SQLAlchemy gives a request-aware session and a model base while still leaving the actual ORM behavior to SQLAlchemy 2.0.",
            "The extension stores state on the app, exposes a scoped session per context, and bridges Flask config into SQLAlchemy engine creation.",
            ECOMMERCE_MODELS,
            extra_examples=[
                ex(
                    "Installing the data stack",
                    "Pinning the ORM and migration stack matters because SQLAlchemy 2.x style is different from many old tutorials.",
                    code=DATA_REQUIREMENTS,
                    lang="text",
                    note="Use `db.init_app(app)` inside the factory; do not bind the extension to the app at import time.",
                ),
                ex(
                    "Unit of Work in practice",
                    "SQLAlchemy stages changes in memory until you commit or roll back.",
                    code="""product = Product(sku="LAMP-01", name="Desk Lamp", price=49.99, inventory=25)
db.session.add(product)
db.session.commit()

product.inventory -= 1
db.session.rollback()
""",
                    note="Nothing becomes durable until `commit()`. That explicit boundary is why rollbacks work cleanly.",
                ),
            ],
            version="Flask-SQLAlchemy 3.x aligns with SQLAlchemy 2.0 patterns. `Model.query` still exists, but `select()` plus `session.execute()` is the preferred long-term direction.",
        ),
        c(
            "FL25",
            4,
            "data",
            "SQLAlchemy Relationships",
            ["FL24"],
            "Relationships describe how ORM objects connect so SQLAlchemy can lazy-load, eager-load, and cascade related rows correctly.",
            "Without declared relationships, every join and child-row lookup becomes manual and repeated across the codebase.",
            "SQLAlchemy relationships let the e-commerce models navigate users, orders, items, and products as object graphs while still generating SQL intentionally.",
            "Lazy loading issues a query when an attribute is first accessed; eager loading options like `joinedload()` and `subqueryload()` change that behavior deliberately.",
            """from sqlalchemy.orm import joinedload, subqueryload

orders = db.session.execute(
    select(Order).options(joinedload(Order.user), subqueryload(Order.items))
).scalars().all()
""",
            extra_examples=[
                ex(
                    "Seeing the N+1 problem",
                    "This is the classic performance failure that relationship loading strategies solve.",
                    code="""# bad: 101 queries for 100 orders
orders = db.session.execute(select(Order)).scalars().all()
for order in orders:
    print(order.user.email)
""",
                    note="`joinedload()` is great for small related objects; `subqueryload()` or `selectinload()` can be better when joins would duplicate too much data.",
                )
            ],
        ),
        c(
            "FL26",
            4,
            "data",
            "SQLAlchemy Queries",
            ["FL24", "FL25"],
            "Flask-SQLAlchemy 3.x sits on SQLAlchemy 2.0, so the most future-proof query style uses `select()` and `session.execute()`.",
            "Legacy query APIs work, but mixing styles blindly makes codebases inconsistent and hides what SQL is actually being generated.",
            "Flask can still support legacy `Model.query`, but 2.0-style selects make joins, subqueries, and result handling easier to reason about.",
            "The session compiles `select()` objects into SQL only when executed, then returns row objects or scalar ORM results depending on how you consume them.",
            """from sqlalchemy import func, select

statement = (
    select(User.email, func.count(Order.id), func.sum(OrderItem.quantity * OrderItem.unit_price))
    .join(Order, Order.user_id == User.id)
    .join(OrderItem, OrderItem.order_id == Order.id)
    .group_by(User.email)
)
rows = db.session.execute(statement).all()
""",
            extra_examples=[
                ex(
                    "Pagination",
                    "Pagination is just limit/offset plus metadata, but a helper keeps your API shape consistent.",
                    code="""page = db.paginate(
    select(Product).order_by(Product.name),
    page=request.args.get("page", 1, type=int),
    per_page=20,
)
return {"items": [product.name for product in page.items], "pages": page.pages}
""",
                    note="Offset pagination is simple, but large datasets and unstable ordering may push you toward cursor-based approaches later.",
                )
            ],
            version="Flask-SQLAlchemy 3.x encourages SQLAlchemy 2.0 style. If a tutorial leans entirely on `Model.query`, treat it as legacy-compatible rather than current best practice.",
        ),
        c(
            "FL27",
            4,
            "data",
            "Alembic Migrations",
            ["FL24"],
            "Migrations are version-controlled programs that evolve a production schema safely and reproducibly.",
            "Running `db.create_all()` in production skips history, review, downgrade paths, and careful data migration work.",
            "Flask-Migrate wires Alembic into Flask so the app factory, config, and SQLAlchemy metadata all feed the migration environment.",
            "Alembic compares model metadata with the current schema, generates revision scripts, and then executes upgrade or downgrade steps transactionally where possible.",
            """from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    return app
""",
            extra_examples=[
                ex(
                    "Install and operate migrations",
                    "This is the deployment-safe path for schema changes.",
                    code=DATA_REQUIREMENTS + "\n" + """# commands
# flask db init
# flask db migrate -m "add inventory column"
# flask db upgrade
""",
                    lang="text",
                    note="Edit autogenerated revisions when you need data movement or safer DDL choices.",
                ),
                ex(
                    "Data migration inside a revision",
                    "Schema changes and data backfills often need to ship together.",
                    code="""def upgrade():
    op.add_column("product", sa.Column("slug", sa.String(length=120), nullable=True))
    op.execute("UPDATE product SET slug = lower(replace(name, ' ', '-'))")
    op.alter_column("product", "slug", nullable=False)
""",
                    note="Resolve multi-head conflicts deliberately; they are a sign that concurrent branches changed schema independently.",
                ),
            ],
        ),
        c(
            "FL28",
            4,
            "data",
            "Marshmallow For Serialization",
            ["FL24"],
            "Marshmallow turns Python objects into validated JSON-friendly data structures and back again.",
            "Manual `dict()` conversion grows brittle the moment nested objects, validation rules, or separate input/output shapes appear.",
            "Marshmallow keeps schema rules explicit so APIs can validate inputs before touching business logic or the database.",
            "Schemas declare fields and validators, then `load()` performs coercion and validation while `dump()` handles output formatting.",
            """from marshmallow import Schema, fields, post_load, validates_schema, ValidationError

class OrderItemSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)

class OrderSchema(Schema):
    user_id = fields.Int(required=True, load_only=True)
    items = fields.List(fields.Nested(OrderItemSchema), required=True)
    total = fields.Decimal(dump_only=True)

    @post_load
    def build_order(self, data, **kwargs):
        return data
""",
            extra_examples=[
                ex(
                    "Install schema tooling",
                    "Schema validation is much easier to keep consistent when the package versions are explicit.",
                    code=DATA_REQUIREMENTS,
                    lang="text",
                    note="If you use Flask-Marshmallow, initialize it with `ma = Marshmallow()` and `ma.init_app(app)` inside the factory.",
                ),
                ex(
                    "Business validation before order creation",
                    "Schema validation is not only about types; it can enforce domain constraints too.",
                    code="""@validates_schema
def validate_inventory(self, data, **kwargs):
    for item in data["items"]:
        product = Product.query.get(item["product_id"])
        if product is None or product.inventory < item["quantity"]:
            raise ValidationError("insufficient inventory", field_name="items")
""",
                    note="Use `dump_only` and `load_only` to keep secrets and server-calculated fields out of the wrong side of the API boundary.",
                ),
            ],
        ),
    ]
)

CONCEPTS.extend(
    [
        c(
            "FL16",
            3,
            "templates",
            "Jinja2 Fundamentals",
            ["FL11", "FL15"],
            "Flask renders HTML with Jinja2: variables use `{{ ... }}`, statements use `{% ... %}`, and autoescaping protects ordinary text output.",
            "If you build HTML with Python string concatenation, duplication grows fast and escaping mistakes become XSS bugs.",
            "Flask points Jinja2 at the `templates/` folder and passes view data into a template environment that escapes output by default.",
            "Jinja2 compiles templates to Python bytecode, and Flask injects helpers like `url_for`, `request`, `session`, and `g` into the template context.",
            """from flask import render_template

@app.get("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name)

# templates/hello.html
# <h1>Hello {{ name }}</h1>
""",
            extra_examples=[
                ex(
                    "Autoescaping prevents obvious XSS",
                    "This is one of Jinja2's best defaults and one you should preserve unless content is truly trusted.",
                    code="""@app.get("/preview")
def preview():
    return render_template("preview.html", body='<script>alert(1)</script>')

# preview.html
# {{ body }}
""",
                    note="Rendered output becomes literal text, not executable script, unless you deliberately disable escaping with `safe`.",
                )
            ],
        ),
        c(
            "FL17",
            3,
            "templates",
            "Jinja2 Control Flow",
            ["FL16"],
            "Jinja2 supports conditionals, loops, loop metadata, and recursion so templates can shape presentation without embedding full Python.",
            "Without template control flow, simple lists, empty states, zebra striping, and recursive menus get pushed into awkward string-building code.",
            "Jinja2 gives a restricted control-flow language designed for presentation concerns rather than arbitrary application logic.",
            "Loop helpers like `loop.index`, `loop.first`, `loop.last`, and `loop.cycle()` are generated by the template runtime while rendering.",
            """{% if products %}
  <ul>
  {% for product in products %}
    <li class="{{ loop.cycle('odd', 'even') }}">{{ loop.index }}. {{ product.name }}</li>
  {% endfor %}
  </ul>
{% else %}
  <p>No products yet.</p>
{% endif %}
""",
            sample_lang="jinja",
            extra_examples=[
                ex(
                    "Recursive category tree",
                    "Tree-shaped data is the classic case where template recursion is simpler than flattening in advance.",
                    code="""<ul>
{% for node in tree recursive %}
  <li>{{ node.name }}
    {% if node.children %}
      <ul>{{ loop(node.children) }}</ul>
    {% endif %}
  </li>
{% endfor %}
</ul>
""",
                    lang="jinja",
                    note="Jinja2 intentionally does not provide `while`; repeated arbitrary logic belongs in Python, not templates.",
                )
            ],
        ),
        c(
            "FL18",
            3,
            "templates",
            "Jinja2 Filters & Tests",
            ["FL16"],
            "Filters transform values for display and tests answer questions about values inside a template.",
            "If every template repeats formatting logic inline, presentation code becomes noisy and inconsistent quickly.",
            "Jinja2 ships many useful filters and lets Flask register custom filters for recurring display rules.",
            "A filter is just a Python callable added to the Jinja environment; Jinja resolves it by name at render time.",
            """@app.template_filter("currency")
def currency(value):
    return f"${value:,.2f}"

# template
# {{ product.price|currency }}
# {{ user.email is string }}
""",
            extra_examples=[
                ex(
                    "Built-in filters worth knowing",
                    "These cover most day-to-day formatting without custom code.",
                    code="""{{ body|truncate(120) }}
{{ description|wordcount }}
{{ rows|groupby("status") }}
{{ users|selectattr("is_active")|map(attribute="email")|list }}
""",
                    lang="jinja",
                    note="Use `safe` only after sanitization or when the HTML is generated by trusted code you control.",
                )
            ],
        ),
        c(
            "FL19",
            3,
            "templates",
            "Jinja2 Template Inheritance",
            ["FL16"],
            "Template inheritance lets a base layout define shared structure while children override named blocks.",
            "Copy-pasting full HTML pages means navigation, `<head>` tags, and footers drift immediately.",
            "Flask encourages a `base.html` plus child-template architecture so each page only owns the blocks that change.",
            "Jinja composes templates during render by resolving `{% extends %}`, then filling block placeholders from child templates.",
            """<!-- templates/base.html -->
<!doctype html>
<title>{% block title %}Shop{% endblock %}</title>
<main>{% block content %}{% endblock %}</main>

<!-- templates/products/list.html -->
{% extends "base.html" %}
{% block title %}Products{% endblock %}
{% block content %}<h1>Products</h1>{% endblock %}
""",
            sample_lang="jinja",
            extra_examples=[
                ex(
                    "Include, import, and `super()`",
                    "Inheritance handles page shells; includes and macros handle reusable fragments.",
                    code="""{% extends "base.html" %}
{% block content %}
  {{ super() }}
  {% include "partials/flash_messages.html" %}
{% endblock %}
""",
                    lang="jinja",
                    note="Use includes for fragments and macros for reusable components; keep block inheritance for layout structure.",
                )
            ],
        ),
        c(
            "FL20",
            3,
            "templates",
            "Jinja2 Macros",
            ["FL16"],
            "Macros are reusable template functions, useful for form fields, tables, badges, and repeated HTML structures.",
            "Without macros, the same label-input-error markup gets duplicated across login, register, and checkout pages.",
            "Jinja macros package view-agnostic presentation patterns into reusable components while still staying plain templates.",
            "Macros are compiled once with the template and imported where needed; `call` lets a macro accept a block of caller-supplied content.",
            """{# templates/macros/forms.html #}
{% macro form_field(name, label, errors=[]) %}
  <label for="{{ name }}">{{ label }}</label>
  <input id="{{ name }}" name="{{ name }}">
  {% if errors %}
    <ul>{% for error in errors %}<li>{{ error }}</li>{% endfor %}</ul>
  {% endif %}
{% endmacro %}
""",
            sample_lang="jinja",
            extra_examples=[
                ex(
                    "Using the macro in two templates",
                    "Macros are the easiest way to build a small component system without a frontend framework.",
                    code="""{% from "macros/forms.html" import form_field %}
{{ form_field("email", "Email", form.email.errors) }}
{{ form_field("password", "Password", form.password.errors) }}
""",
                    lang="jinja",
                    note="A macro should stay presentation-focused; database lookups and auth rules still belong in Python code.",
                )
            ],
        ),
        c(
            "FL21",
            3,
            "templates",
            "Template Context",
            ["FL16"],
            "Context processors inject shared values into every template render, such as site metadata, utility functions, or the current user.",
            "Repeating the same `site_name`, `year`, or helper function in every `render_template()` call is noisy and easy to forget.",
            "Flask lets you centralize global template context in one place while still keeping route-specific data explicit.",
            "Context processors run on every template render and merge dictionaries into the template context, so heavy work here hurts every request.",
            """@app.context_processor
def inject_globals():
    return {
        "site_name": "Acme Shop",
        "current_year": 2026,
        "current_user": getattr(g, "current_user", None),
    }
""",
            extra_examples=[
                ex(
                    "The performance trap",
                    "Context processors feel invisible, which is exactly why they are dangerous for heavy work.",
                    code="""@app.context_processor
def inject_globals():
    return {"popular_products": Product.query.order_by(Product.sales.desc()).limit(10).all()}
""",
                    note="This query now runs for every template render. Cache or precompute it instead of hiding it in a global injector.",
                )
            ],
        ),
        c(
            "FL22",
            3,
            "templates",
            "Static Files",
            ["FL16"],
            "Static assets should be referenced through `url_for('static', filename=...)` so paths and versioning stay consistent.",
            "Hardcoded `/static/...` paths break behind prefixes, CDNs, or versioned asset strategies.",
            "Flask gives the app and blueprints predictable static endpoints, and production servers or CDNs usually serve the actual files.",
            "During development Flask can serve static files directly, but production typically hands that job to nginx, a CDN, or object storage.",
            """<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css', v=config['VERSION']) }}">
<script src="{{ url_for('static', filename='js/app.js', v=config['VERSION']) }}"></script>
""",
            sample_lang="jinja",
            extra_examples=[
                ex(
                    "Flask-Assets style bundling hook",
                    "Versioned URLs and bundling become more important as the frontend grows.",
                    code="""assets = Environment()
assets.init_app(app)
assets.register("shop_css", Bundle("scss/main.scss", filters="libsass", output="gen/main.css"))
""",
                    note="Development can serve files directly, but production should serve immutable versioned assets through a dedicated static pipeline.",
                )
            ],
        ),
    ]
)

CONCEPTS.extend(
    [
        c(
            "FL11",
            2,
            "request",
            "The Request Object",
            ["FL06", "FL07", "FL08"],
            "`flask.request` is the parsed view of the current HTTP request: method, query args, form fields, files, JSON, headers, cookies, and URL metadata.",
            "If you guess where incoming data lives, you'll read the wrong field, mishandle content types, and spend hours debugging `None` values.",
            "Flask gives each request a rich object so your view code can read the exact HTTP surface it needs without reparsing raw bytes.",
            "Werkzeug parses the WSGI environ into a Request object lazily, so headers, form data, files, and JSON are exposed as high-level properties.",
            """from flask import request

@app.post("/login")
def login():
    return {
        "method": request.method,
        "args": request.args.to_dict(),
        "json": request.get_json(silent=True),
        "headers": dict(request.headers),
        "cookies": request.cookies,
        "content_type": request.content_type,
    }
""",
            extra_examples=[
                ex(
                    "POST with files and form fields",
                    "Multipart requests expose files separately from ordinary form fields.",
                    code="""@app.post("/upload")
def upload():
    photo = request.files["photo"]
    title = request.form["title"]
    return {"filename": photo.filename, "title": title}
""",
                    note="`request.form` only works for form encodings. JSON requests should use `request.get_json()` instead.",
                )
            ],
        ),
        c(
            "FL12",
            2,
            "request",
            "The Response Object",
            ["FL06", "FL07", "FL08"],
            "A Flask response wraps status, headers, cookies, and body bytes; return-value shortcuts are just convenience around that object.",
            "If you treat responses as plain strings, you'll eventually need headers, cookies, status codes, or post-processing and discover the hidden response lifecycle too late.",
            "Flask accepts concise return values but normalizes them into a Response object you can inspect or mutate.",
            "Flask calls `make_response()` internally to convert strings, dicts, tuples, generators, and Response objects into one consistent response interface.",
            """from flask import jsonify, make_response

@app.get("/demo")
def demo():
    response = make_response(jsonify({"ok": True}), 201)
    response.headers["X-App-Version"] = "3.1"
    response.set_cookie("session", "abc", httponly=True, secure=True, samesite="Lax")
    return response
""",
            extra_examples=[
                ex(
                    "Tuple shortcuts",
                    "These are the four most common return forms Flask upgrades into a Response object.",
                    code="""return "plain body"
return {"ok": True}, 201
return {"ok": True}, 200, {"X-Trace": "abc"}
return make_response("ready", 202)
""",
                    note="`after_this_request()` is useful when the response object needs late mutation after the view returns.",
                )
            ],
        ),
        c(
            "FL13",
            2,
            "request",
            "Request Context",
            ["FL11"],
            "The request context is the per-request stack frame that makes `request`, `session`, and `g` resolve to the correct in-flight request.",
            "If `request` were a real global, concurrent requests would overwrite each other immediately.",
            "Flask uses context-local proxies so code can reference `request` naturally while still remaining request-safe.",
            "When a request begins, Flask pushes a RequestContext and AppContext; when it ends, teardown handlers run and those contexts are popped.",
            """from flask import request

@app.get("/whoami")
def whoami():
    return {"path": request.path}

with app.test_request_context("/whoami?debug=1"):
    print(request.path)
""",
            extra_examples=[
                ex(
                    "The runtime error",
                    "This is the failure every Flask developer eventually hits in a shell, script, or background task.",
                    code="""from flask import request

print(request.path)
# RuntimeError: Working outside of request context.
""",
                    note="Use `app.test_request_context()` or redesign the function to accept explicit values instead of relying on the proxy.",
                )
            ],
        ),
        c(
            "FL14",
            2,
            "request",
            "Application Context",
            ["FL11"],
            "The application context gives access to `current_app` and `g` even when there is no active request.",
            "Code that needs config or shared per-request resources outside a view often fails because it expects `request` when it only needs the app context.",
            "Flask separates app-level state from request-level state so CLI commands, scripts, and teardown hooks can still use config safely.",
            "An AppContext is pushed for every request and can also be pushed manually; `g` lives for that context lifetime and is cleared on teardown.",
            """from flask import current_app, g
import sqlite3

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
""",
            extra_examples=[
                ex(
                    "Using app context in a script",
                    "This is the safe way to access config, extensions, and `g` outside a request cycle.",
                    code="""with app.app_context():
    print(current_app.config["SQLALCHEMY_DATABASE_URI"])
""",
                    note="Request context implies app context, but app context alone does not give you `request` or `session`.",
                )
            ],
        ),
        c(
            "FL15",
            2,
            "request",
            "Error Handling",
            ["FL11", "FL12", "FL13", "FL14"],
            "Flask lets you intercept exceptions and HTTP errors so browsers and API clients get intentional responses instead of tracebacks or inconsistent JSON.",
            "Without centralized error handling, every route invents its own error shape and operational failures leak straight to users.",
            "Flask maps exceptions through registered handlers, with `abort()` as a convenient way to raise an HTTPException intentionally.",
            "Handlers are resolved by exception class, so a handler for `HTTPException` can standardize API errors broadly while specific handlers override it.",
            """from flask import jsonify
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_http_error(error):
    return jsonify({"error": error.description, "code": error.code}), error.code

@app.get("/missing")
def missing():
    abort(404, description="product not found")
""",
            extra_examples=[
                ex(
                    "Custom HTML errors and JSON APIs can coexist",
                    "Return HTML to browsers and JSON to API prefixes instead of choosing one format globally.",
                    code="""@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return {"error": {"code": 404, "message": "not found"}}, 404
    return render_template("404.html"), 404
""",
                    note="A catch-all `Exception` handler should log loudly and avoid swallowing real programming errors during development.",
                )
            ],
        ),
    ]
)

CONCEPTS.sort(key=lambda item: int(item["id"][2:]))


def validate_graph() -> None:
    ids = [item["id"] for item in CONCEPTS]
    if len(ids) != 59:
        raise ValueError(f"Expected 59 concepts, found {len(ids)}")
    seen = set()
    for item in CONCEPTS:
        for prereq in item["prereqs"]:
            if prereq not in ids:
                raise ValueError(f"Unknown prerequisite {prereq} for {item['id']}")
            if prereq not in seen:
                raise ValueError(f"Prerequisite {prereq} appears after {item['id']}")
        seen.add(item["id"])


def build_document() -> str:
    validate_graph()
    dependents = build_dependents()
    task_close_markers = {
        "FL05": "<!-- TASK-3 END -->\n<!-- TASK-4 START -->",
        "FL10": "<!-- TASK-4 END -->\n<!-- TASK-5 START -->",
        "FL15": "<!-- TASK-5 END -->\n<!-- TASK-6 START -->",
        "FL22": "<!-- TASK-6 END -->\n<!-- TASK-7 START -->",
        "FL28": "<!-- TASK-7 END -->\n<!-- TASK-8 START -->",
        "FL36": "<!-- TASK-8 END -->\n<!-- TASK-9 START -->",
        "FL50": "<!-- TASK-9 END -->\n<!-- TASK-10 START -->",
        "FL59": "<!-- TASK-10 END -->",
    }
    sections = ["<!-- TASK-3 START -->"]
    for index, item in enumerate(CONCEPTS):
        sections.append(render_section(item, dependents, index))
        marker = task_close_markers.get(item["id"])
        if marker:
            sections.append(marker)
    appendix = (
        "<!-- TASK-11 START -->"
        + render_ecosystem_map()
        + render_quick_reference()
        + "<!-- TASK-11 END --><button class='back-to-top' id='backToTop' aria-label='Back to top'>↑ Top</button>"
    )
    return render_shell(dependents) + "".join(sections) + appendix + tail_script()


def render_dependency_table(dependents):
    rows = "".join(
        "<tr>"
        f"<td><a href='#{item['id']}'>{item['id']}</a></td>"
        f"<td>{escape(item['title'])}</td>"
        f"<td>{item['layer']}</td>"
        f"<td>{', '.join(item['prereqs']) or 'None'}</td>"
        f"<td>{', '.join(dependents.get(item['id'], [])) or 'None'}</td>"
        "</tr>"
        for item in CONCEPTS
    )
    return f"""
<section class='concept-section' id='dependency-table' data-title='Concept DAG & Dependency Table'>
  <div class='section-kicker'>Task 2 &middot; Concept DAG</div>
  <h2>Flask Concept DAG</h2>
  <p>The order of the document follows this dependency graph exactly, so each section appears after the ideas it depends on.</p>
  <div class='diagram-actions'><button class='diagram-action dag-download-btn' type='button' aria-label='Download Flask concept DAG'>Download DAG</button></div>
  <div class='er-diagram'><div class='mermaid'>{escape(render_dag())}</div></div>
  <h3>All 59 Concepts</h3>
  <div class='table-wrap'><table><thead><tr><th>ID</th><th>Concept</th><th>Layer</th><th>Prerequisites</th><th>Dependents</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
"""


def render_nav():
    by_layer = defaultdict(list)
    for item in CONCEPTS:
        by_layer[item["layer"]].append(item)
    parts = [
        "<section class='nav-group' data-layer='ref'>"
        "<button class='group-toggle' type='button' data-layer='R' aria-expanded='true'><span>References</span><span>&#9662;</span></button>"
        "<div class='group-links'>"
        + "".join(
            f"<a href='#{target}' data-id='{target}'><span class='nav-dot'>R</span><span>{escape(label)}</span></a>"
            for target, label in REFERENCE_SECTIONS
        )
        + "</div></section>"
    ]
    for layer in sorted(LAYER_NAMES):
        links = "".join(
            f"<a href='#{item['id']}' data-id='{item['id']}'><span class='nav-dot'>{layer}</span><span>{escape(item['id'])} &middot; {escape(item['title'])}</span></a>"
            for item in by_layer[layer]
        )
        parts.append(
            f"<section class='nav-group' data-layer='{layer}'>"
            f"<button class='group-toggle' type='button' data-layer='{layer}' aria-expanded='true'><span>{escape(NAV_LABELS[layer])}</span><span>&#9662;</span></button>"
            f"<div class='group-links'>{links}</div></section>"
        )
    return "".join(parts)


def render_shell(dependents):
    return f"""<!DOCTYPE html>
<html lang='en' data-theme='dark'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>{TITLE}</title>
<link rel='preconnect' href='https://fonts.googleapis.com'>
<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>
<link href='https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Lora:wght@400;500;600;700&family=Syne:wght@600;700;800&display=swap' rel='stylesheet'>
<link id='darkThemeStylesheet' rel='stylesheet' href='styles-dark.css'>
<link id='lightThemeStylesheet' rel='stylesheet' href='styles-light.css' media='not all'>
<link rel='preload' href='styles.css' as='style'>
<link rel='stylesheet' href='styles.css'>
<style>
html[data-theme='dark'] {{ --void:#0b0d11; --obsidian:#090b10; --deep:#0f141b; --surface:#141b24; --surface2:#1b2530; --surface3:#233241; --violet:#e34f26; --violet-dim:#7d2a14; --gold:#7fffd4; --text-1:#f4efe5; --text-2:#c2c7ce; --font-head:'Syne',serif; --font-body:'Lora',serif; --font-code:'IBM Plex Mono',monospace; }}
html[data-theme='light'] {{ --paper:#f7f3ec; --paper2:#eef2ef; --surface:#fbfdfb; --surface2:#f3f6f3; --surface3:#e7ece9; --forest:#163242; --terra:#e34f26; --font-head:'Syne',serif; --font-body:'Lora',serif; --font-code:'IBM Plex Mono',monospace; }}
.diagram-actions{{display:flex;justify-content:flex-end;margin:.85rem 0 1rem}} .diagram-action,.aux-toggle{{appearance:none;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);color:inherit;padding:.6rem .9rem;border-radius:10px;cursor:pointer;font-family:var(--font-code);font-size:.76rem}} html[data-theme='light'] .diagram-action,html[data-theme='light'] .aux-toggle{{border-color:rgba(22,50,66,.16);background:rgba(22,50,66,.04)}}
.sidebar-nav .group-links a{{display:grid;grid-template-columns:auto 1fr;gap:.6rem;align-items:start}} .nav-dot{{display:inline-flex;align-items:center;justify-content:center;min-width:1.5rem;height:1.5rem;border-radius:999px;font-size:.68rem;font-family:var(--font-code);border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04)}} html[data-theme='light'] .nav-dot{{border-color:rgba(22,50,66,.18);background:rgba(22,50,66,.06)}}
.hero-grid{{display:grid;grid-template-columns:1.3fr .9fr;gap:1.2rem;align-items:start}} .hero-card,.comparison-box,.example-card,.gotcha-box,.mermaid-wrap,.er-diagram,.extension-card{{border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:1rem;background:rgba(255,255,255,.02)}} html[data-theme='light'] .hero-card,html[data-theme='light'] .comparison-box,html[data-theme='light'] .example-card,html[data-theme='light'] .gotcha-box,html[data-theme='light'] .mermaid-wrap,html[data-theme='light'] .er-diagram,html[data-theme='light'] .extension-card{{border-color:rgba(22,50,66,.12);background:rgba(255,255,255,.74)}}
.lead{{font-size:1.04rem}} .section-meta,.forward-links{{display:flex;flex-wrap:wrap;gap:.7rem 1rem;align-items:center;margin:.75rem 0 1rem}} .forward-links>div{{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}}
.cluster-pill{{display:inline-flex;align-items:center;border-radius:999px;padding:.2rem .6rem;font-family:var(--font-code);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em}} .cluster-foundation{{background:rgba(227,79,38,.14);color:#ffcabd}} .cluster-routing{{background:rgba(255,138,101,.14);color:#ffd9d0}} .cluster-request{{background:rgba(86,214,255,.14);color:#d8f7ff}} .cluster-templates{{background:rgba(127,255,212,.14);color:#d9fff0}} .cluster-data{{background:rgba(255,207,112,.14);color:#ffe7a6}} .cluster-forms{{background:rgba(255,179,71,.14);color:#ffe0b3}} .cluster-auth{{background:rgba(140,210,255,.14);color:#d9f0ff}} .cluster-rest{{background:rgba(101,196,255,.14);color:#def4ff}} .cluster-async{{background:rgba(220,182,255,.14);color:#f0ddff}} .cluster-extensions{{background:rgba(255,159,128,.14);color:#ffe0d6}} .cluster-testing{{background:rgba(140,230,193,.14);color:#ddfff0}} .cluster-production{{background:rgba(242,210,139,.14);color:#fff2cf}} .cluster-architecture{{background:rgba(182,178,255,.14);color:#eeedff}} html[data-theme='light'] .cluster-pill{{color:var(--forest)}}
.why-box{{border-left:4px solid #e34f26;background:rgba(227,79,38,.1)}} .wsgi-box{{border-left:4px solid #7fffd4;background:rgba(127,255,212,.08)}} .security-box{{border-left:4px solid #ffcf70;background:rgba(255,207,112,.09)}} .version-box{{border-left:4px solid #8cd2ff;background:rgba(140,210,255,.09)}} .wsgi-title{{font-family:var(--font-code);font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.35rem}}
.http-display{{border:1px solid rgba(227,79,38,.18);border-radius:16px;background:rgba(227,79,38,.05);padding:.2rem}} html[data-theme='light'] .http-display{{border-color:rgba(227,79,38,.18);background:rgba(227,79,38,.05)}}
.tab-buttons{{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.8rem}} .tab-btn{{appearance:none;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);color:inherit;border-radius:999px;padding:.45rem .7rem;cursor:pointer;font:600 .74rem var(--font-code)}} .tab-btn.is-active{{background:rgba(227,79,38,.14);border-color:rgba(227,79,38,.34)}} html[data-theme='light'] .tab-btn{{border-color:rgba(22,50,66,.15);background:rgba(22,50,66,.04)}} html[data-theme='light'] .tab-btn.is-active{{background:rgba(227,79,38,.1);border-color:rgba(227,79,38,.24)}} .tab-panel{{display:none}} .tab-panel.is-active{{display:block}}
.mistake-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}} .extension-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}} .extension-type{{font-family:var(--font-code);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:#e34f26}}
.sidebar-aux{{display:grid;gap:.55rem;margin-top:.75rem}} .aux-toggle.is-active{{background:rgba(227,79,38,.14);border-color:rgba(227,79,38,.34)}} html[data-theme='light'] .aux-toggle.is-active{{background:rgba(227,79,38,.1);border-color:rgba(227,79,38,.24)}}
.layer-skeleton{{height:320px;border-radius:14px;background:linear-gradient(90deg,rgba(255,255,255,.03) 25%,rgba(255,255,255,.07) 50%,rgba(255,255,255,.03) 75%);background-size:200% 100%;animation:skeleton-sweep 1.4s ease infinite;border:1px solid rgba(255,255,255,.06);margin-bottom:1.4rem}} @keyframes skeleton-sweep{{0%{{background-position:200% 0}}100%{{background-position:-200% 0}}}}
@media (max-width:1100px){{.hero-grid,.extension-grid{{grid-template-columns:1fr}}}} @media (max-width:900px){{.mistake-grid{{grid-template-columns:1fr}}}}
</style>
<!-- REVIEW: Keep this inline theme bootstrap in <head>; moving it to the end of <body> would cause the wrong theme to flash before styles apply. -->
<script>
try {{
  const savedTheme = localStorage.getItem('flask-reference-theme');
  const theme = savedTheme === 'light' ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme;
  window.__initialTheme = theme;
  if (theme === 'light') {{
    document.getElementById('darkThemeStylesheet').media = 'not all';
    document.getElementById('lightThemeStylesheet').media = 'all';
  }}
}} catch (error) {{
  document.documentElement.dataset.theme = 'dark';
  window.__initialTheme = 'dark';
}}
</script>
</head>
<body>
<button class='mobile-toggle' id='mobileToggle' aria-label='Toggle navigation'>&#9776;</button>
<div class='app-shell'>
<aside class='sidebar' id='sidebar'>
  <div class='sidebar-top'>
    <div class='theme-switch'>
      <div class='theme-meta'>
        <span class='theme-label'>Color Theme</span>
        <span class='theme-shortcut'><kbd>D</kbd> Toggle</span>
      </div>
      <div class='theme-toggle' role='group' aria-label='Color theme'>
        <button class='theme-option' id='themeLight' type='button' data-theme='light' aria-pressed='false'>Light</button>
        <button class='theme-option is-active' id='themeDark' type='button' data-theme='dark' aria-pressed='true'>Dark</button>
      </div>
    </div>
    <div class='sidebar-aux'>
      <button class='aux-toggle' id='wsgiToggle' type='button' aria-pressed='false'>Show WSGI equivalents</button>
    </div>
  </div>
  <nav class='sidebar-nav' aria-label='Flask concept navigation'>{render_nav()}</nav>
</aside>
<main>
<!-- TASK-1 START -->
<section class='hero' id='top'>
  <div class='section-kicker'>Flask Complete Reference</div>
  <div class='hero-grid'>
    <div>
      <h1>{SUBTITLE}</h1>
      <p>This document assumes Python fundamentals but no prior framework knowledge. It starts from raw HTTP, sockets, and WSGI, then climbs through routing, request handling, templates, persistence, sessions, auth, REST APIs, async trade-offs, testing, and production deployment.</p>
      <p>The running product is a small e-commerce system with <code>User</code>, <code>Product</code>, <code>Order</code>, and <code>OrderItem</code>. The same domain appears through SQLAlchemy, forms, login flows, APIs, background work, and tests so the examples stay coherent.</p>
    </div>
    <div class='hero-card'>
      <h3>Baseline Core Packages</h3>
      {render_pre(CORE_REQUIREMENTS, "text")}
    </div>
  </div>
</section>
<!-- TASK-1 END -->
<div id='sectionMount' hidden aria-hidden='true'></div>
<!-- TASK-2 START -->
{render_dependency_table(dependents)}
{render_wsgi_flow()}
{render_context_stack()}
<!-- TASK-2 END -->
"""


def tail_script():
    return r"""
</main>
</div>
<button class='back-to-top' id='backToTop' aria-label='Back to top'>&uarr; Top</button>
<script defer src='https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  const navLinks = [...document.querySelectorAll('.group-links a')];
  const sidebar = document.getElementById('sidebar');
  const mobileToggle = document.getElementById('mobileToggle');
  const wsgiToggle = document.getElementById('wsgiToggle');
  const backToTop = document.getElementById('backToTop');
  const darkThemeStylesheet = document.getElementById('darkThemeStylesheet');
  const lightThemeStylesheet = document.getElementById('lightThemeStylesheet');
  const themeButtons = [...document.querySelectorAll('.theme-option')];
  const main = document.querySelector('main');
  const sectionMount = document.getElementById('sectionMount');
  const virtualSections = [...document.querySelectorAll("main .concept-section[id]")];
  const sectionMarkupById = new Map(virtualSections.map((section) => [section.id, { id: section.id, html: section.outerHTML }]));
  const orderedIds = navLinks.map((link) => link.dataset.id).filter(Boolean);
  const sectionIdSet = new Set(sectionMarkupById.keys());
  const THEME_STORAGE_KEY = 'flask-reference-theme';
  let currentTheme = window.__initialTheme === 'light' ? 'light' : 'dark';
  let currentSectionId = virtualSections[0]?.id || orderedIds[0] || '';
  let activeObserver = null;
  let renderToken = 0;
  let mermaidRenderToken = 0;
  let wsgiVisible = false;
  document.body.dataset.theme = currentTheme;
  function isTypingTarget(target) {
    return target instanceof HTMLElement && (target.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName));
  }
  function syncThemeButtons(theme) {
    themeButtons.forEach((button) => {
      const active = button.dataset.theme === theme;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
  }
  function initMermaid(root) {
    if (!window.mermaid || typeof window.mermaid.initialize !== 'function') return;
    const blocks = [...root.querySelectorAll('.mermaid')];
    if (!blocks.length) return;
    blocks.forEach((block) => {
      const source = (block.dataset.mermaidSource || block.textContent || '').trim();
      if (!source) return;
      block.dataset.mermaidSource = source;
      block.textContent = source;
      block.removeAttribute('data-processed');
    });
    window.mermaid.initialize({ startOnLoad: false, securityLevel: 'loose', theme: currentTheme === 'dark' ? 'dark' : 'neutral' });
    if (typeof window.mermaid.run === 'function') {
      window.mermaid.run({ nodes: blocks });
    } else if (typeof window.mermaid.init === 'function') {
      window.mermaid.init(undefined, blocks);
    }
  }
  function queueMermaidRender(root = document) {
    const token = ++mermaidRenderToken;
    const run = () => {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          if (token !== mermaidRenderToken) return;
          initMermaid(root);
        });
      });
    };
    if (document.fonts && typeof document.fonts.ready?.then === 'function') {
      document.fonts.ready.then(run, run);
    } else {
      run();
    }
  }
  function applyTheme(theme, persist = true) {
    const nextTheme = theme === 'light' ? 'light' : 'dark';
    currentTheme = nextTheme;
    document.documentElement.dataset.theme = nextTheme;
    document.body.dataset.theme = nextTheme;
    darkThemeStylesheet.media = nextTheme === 'dark' ? 'all' : 'not all';
    lightThemeStylesheet.media = nextTheme === 'light' ? 'all' : 'not all';
    syncThemeButtons(nextTheme);
    if (persist) {
      try { localStorage.setItem(THEME_STORAGE_KEY, nextTheme); } catch (error) {}
    }
    queueMermaidRender(document);
  }
  function copyBlockText(pre) {
    const lineTexts = [...pre.querySelectorAll('.line-text')];
    if (lineTexts.length) {
      return lineTexts.map((line) => line.textContent || '').join('\n');
    }
    return pre.querySelector('code')?.textContent || '';
  }
  async function handleCopyButtonClick(event) {
    const button = event.currentTarget;
    const pre = button.closest('pre[data-lang]');
    if (!pre) return;
    await navigator.clipboard.writeText(copyBlockText(pre));
    button.textContent = 'Copied';
    setTimeout(() => { button.textContent = 'Copy'; }, 1200);
  }
  function bindCopyButtons(root) {
    root.querySelectorAll('pre[data-lang]').forEach((pre) => {
      let button = pre.querySelector('.copy-btn');
      if (!button) {
        button = document.createElement('button');
        button.className = 'copy-btn';
        button.type = 'button';
        button.textContent = 'Copy';
        button.setAttribute('aria-label', 'Copy code block');
        pre.appendChild(button);
      }
      if (button.dataset.copyBound === 'true') return;
      button.addEventListener('click', handleCopyButtonClick);
      button.dataset.copyBound = 'true';
    });
  }
  function bindTabs(root) {
    root.querySelectorAll('.tabbed-code').forEach((tabRoot) => {
      const buttons = [...tabRoot.querySelectorAll('.tab-btn')];
      buttons.forEach((button) => {
        if (button.dataset.tabBound === 'true') return;
        button.addEventListener('click', () => {
          const panelId = button.dataset.panel;
          buttons.forEach((candidate) => {
            const active = candidate === button;
            candidate.classList.toggle('is-active', active);
            candidate.setAttribute('aria-pressed', String(active));
          });
          tabRoot.querySelectorAll('.tab-panel').forEach((panel) => {
            panel.classList.toggle('is-active', panel.id === panelId);
          });
        });
        button.dataset.tabBound = 'true';
      });
    });
  }
  function handleDagDownloadClick(event) {
    const button = event.currentTarget;
    const section = button.closest('.concept-section') || document;
    const svg = section.querySelector('.mermaid svg');
    if (!svg) return;
    const clone = svg.cloneNode(true);
    if (!clone.getAttribute('xmlns')) {
      clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    }
    const source = new XMLSerializer().serializeToString(clone);
    const blob = new Blob([source], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'flask-concept-dag.svg';
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 0);
  }
  function bindDagDownloads(root) {
    root.querySelectorAll('.dag-download-btn').forEach((button) => {
      if (button.dataset.downloadBound === 'true') return;
      button.addEventListener('click', handleDagDownloadClick);
      button.dataset.downloadBound = 'true';
    });
  }
  function applyWsgiState(root = document) {
    root.querySelectorAll('.wsgi-box').forEach((box) => {
      box.hidden = !wsgiVisible;
    });
    if (wsgiToggle) {
      wsgiToggle.classList.toggle('is-active', wsgiVisible);
      wsgiToggle.setAttribute('aria-pressed', String(wsgiVisible));
      wsgiToggle.textContent = wsgiVisible ? 'Hide WSGI equivalents' : 'Show WSGI equivalents';
    }
  }
  function updateProgress(sectionId = currentSectionId) {
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    if (!progressBar || !progressText) return;
    const total = orderedIds.length || 1;
    const index = Math.max(0, orderedIds.indexOf(sectionId));
    const pct = Math.round(((index + 1) / total) * 100);
    progressBar.style.width = `${pct}%`;
    progressText.textContent = `${pct}%`;
  }
  function setActiveNavLink(sectionId) {
    navLinks.forEach((link) => {
      const active = link.dataset.id === sectionId;
      link.classList.toggle('active', active);
      link.setAttribute('aria-current', active ? 'location' : 'false');
      if (active) {
        const group = link.closest('.nav-group');
        group?.classList.remove('collapsed');
        group?.querySelector('.group-toggle')?.setAttribute('aria-expanded', 'true');
      }
    });
    updateProgress(sectionId);
  }
  function observeTrackedSections() {
    activeObserver?.disconnect();
    activeObserver = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (!visible.length) return;
      const current = visible[0].target;
      if (current.id) {
        currentSectionId = current.id;
        setActiveNavLink(current.id);
      }
    }, { rootMargin: '-18% 0px -58% 0px', threshold: [0.2, 0.45, 0.65] });
    [...document.querySelectorAll("main .concept-section[id]")].forEach((section) => activeObserver.observe(section));
  }
  function ensureLayerSkeleton() {
    let skeleton = main.querySelector('.layer-skeleton');
    if (!skeleton) {
      skeleton = document.createElement('div');
      skeleton.className = 'layer-skeleton';
    }
    return skeleton;
  }
  function reinitializeSection(section) {
    bindCopyButtons(section);
    bindTabs(section);
    bindDagDownloads(section);
    applyWsgiState(section);
    queueMermaidRender(section);
    observeTrackedSections();
  }
  function renderSection(sectionId, options = {}) {
    if (!sectionMarkupById.has(sectionId) || !sectionMount?.parentNode) return null;
    const { pushHistory = true, scrollBehavior = 'smooth' } = options;
    const existing = main.querySelector(`[id="${sectionId}"]`);
    if (existing && currentSectionId === sectionId) {
      setActiveNavLink(sectionId);
      if (pushHistory) history.pushState({ sectionId }, '', `#${sectionId}`);
      existing.scrollIntoView({ behavior: scrollBehavior, block: 'start' });
      return existing;
    }
    const token = ++renderToken;
    main.classList.add('is-loading');
    const skeleton = ensureLayerSkeleton();
    if (!skeleton.isConnected) sectionMount.parentNode.insertBefore(skeleton, sectionMount);
    main.querySelectorAll(".concept-section[id]").forEach((section) => section.remove());
    const data = sectionMarkupById.get(sectionId);
    if (!data) {
      skeleton.remove();
      main.classList.remove('is-loading');
      return null;
    }
    requestAnimationFrame(() => {
      if (token !== renderToken) return;
      const template = document.createElement('template');
      template.innerHTML = data.html.trim();
      const section = template.content.firstElementChild;
      sectionMount.parentNode.insertBefore(section, sectionMount);
      currentSectionId = sectionId;
      setActiveNavLink(sectionId);
      reinitializeSection(section);
      if (pushHistory) history.pushState({ sectionId }, '', `#${sectionId}`);
      skeleton.remove();
      main.classList.remove('is-loading');
      section.scrollIntoView({ behavior: scrollBehavior, block: 'start' });
    });
    return null;
  }
  bindCopyButtons(document);
  bindTabs(document);
  bindDagDownloads(document);
  queueMermaidRender(document);
  applyWsgiState(document);
  virtualSections.forEach((section) => { if (section.id !== currentSectionId) section.remove(); });
  if (currentSectionId) setActiveNavLink(currentSectionId);
  observeTrackedSections();
  themeButtons.forEach((button) => button.addEventListener('click', () => applyTheme(button.dataset.theme || 'dark')));
  document.querySelectorAll('.group-toggle').forEach((button) => {
    button.addEventListener('click', () => {
      const collapsed = button.parentElement.classList.toggle('collapsed');
      button.setAttribute('aria-expanded', String(!collapsed));
    });
  });
  wsgiToggle?.addEventListener('click', () => {
    wsgiVisible = !wsgiVisible;
    applyWsgiState(document);
  });
  mobileToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
  document.addEventListener('click', (event) => {
    const link = event.target.closest("a[href^='#']");
    if (!link) return;
    const sectionId = (link.getAttribute('href') || '').slice(1);
    if (!sectionId || !sectionIdSet.has(sectionId)) return;
    event.preventDefault();
    if (window.innerWidth < 769) sidebar.classList.remove('open');
    renderSection(sectionId, { pushHistory: true, scrollBehavior: 'smooth' });
  });
  window.addEventListener('popstate', (event) => {
    const fallback = orderedIds[0] || '';
    const sectionId = event.state?.sectionId || window.location.hash.slice(1) || fallback;
    if (!sectionIdSet.has(sectionId)) return;
    renderSection(sectionId, { pushHistory: false, scrollBehavior: 'smooth' });
  });
  const initialSectionId = window.location.hash.slice(1);
  if (sectionIdSet.has(initialSectionId)) {
    history.replaceState({ sectionId: initialSectionId }, '', `#${initialSectionId}`);
    if (initialSectionId !== currentSectionId) renderSection(initialSectionId, { pushHistory: false, scrollBehavior: 'auto' });
  } else if (currentSectionId) {
    history.replaceState({ sectionId: currentSectionId }, '', `${window.location.pathname}${window.location.search}`);
  }
  function updateScrollState() { backToTop.classList.toggle('visible', window.scrollY > 600); }
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  document.addEventListener('keydown', (event) => {
    if (event.defaultPrevented || event.ctrlKey || event.metaKey || event.altKey) return;
    const key = event.key.toLowerCase();
    if (key === 'd' && !isTypingTarget(event.target)) {
      event.preventDefault();
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    }
  });
  window.addEventListener('scroll', updateScrollState, { passive: true });
  updateScrollState();
  updateProgress(currentSectionId);
  syncThemeButtons(currentTheme);
});
</script>
</body>
</html>
"""


def build_document() -> str:
    validate_graph()
    dependents = build_dependents()
    task_close_markers = {
        "FL05": "<!-- TASK-3 END -->\n<!-- TASK-4 START -->",
        "FL10": "<!-- TASK-4 END -->\n<!-- TASK-5 START -->",
        "FL15": "<!-- TASK-5 END -->\n<!-- TASK-6 START -->",
        "FL22": "<!-- TASK-6 END -->\n<!-- TASK-7 START -->",
        "FL28": "<!-- TASK-7 END -->\n<!-- TASK-8 START -->",
        "FL36": "<!-- TASK-8 END -->\n<!-- TASK-9 START -->",
        "FL50": "<!-- TASK-9 END -->\n<!-- TASK-10 START -->",
        "FL59": "<!-- TASK-10 END -->",
    }
    sections = ["<!-- TASK-3 START -->"]
    for index, item in enumerate(CONCEPTS):
        sections.append(render_section(item, dependents, index))
        marker = task_close_markers.get(item["id"])
        if marker:
            sections.append(marker)
    appendix = "<!-- TASK-11 START -->" + render_ecosystem_map() + render_quick_reference() + "<!-- TASK-11 END -->"
    return render_shell(dependents) + "".join(sections) + appendix + tail_script()


def main() -> None:
    OUTFILE.write_text(build_document(), encoding="utf-8")
    print(f"Wrote {OUTFILE}")


if __name__ == "__main__":
    main()
