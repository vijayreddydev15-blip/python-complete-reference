from __future__ import annotations

from collections import defaultdict
from html import escape
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
OUTFILE = ROOT / "fastapi_complete_reference.html"

TITLE = "FastAPI Complete Reference"
SUBTITLE = "FastAPI 0.110+ and Pydantic v2 from ASGI and asyncio first principles to testing, scaling, and production delivery"

LAYER_NAMES = {
    0: "ASGI & Async Foundations",
    1: "Routing & Parameters",
    2: "Pydantic Deep-Dive",
    3: "Dependency Injection",
    4: "Responses & Error Handling",
    5: "Routing, APIRouter & OpenAPI",
    6: "Middleware & Lifecycle",
    7: "Authentication & Security",
    8: "Database Integration",
    9: "WebSockets & Advanced Async",
    10: "Performance & Optimization",
    11: "Testing",
    12: "Production & Advanced Patterns",
}

NAV_LABELS = {
    0: "Layer 0: ASGI & Async Foundations",
    1: "Layer 1: Routing & Parameters",
    2: "Layer 2: Pydantic Deep-Dive",
    3: "Layer 3: Dependency Injection",
    4: "Layer 4: Responses & Error Handling",
    5: "Layer 5: APIRouter & OpenAPI",
    6: "Layer 6: Middleware & Lifecycle",
    7: "Layer 7: Authentication & Security",
    8: "Layer 8: Database Integration",
    9: "Layer 9: WebSockets & Advanced Async",
    10: "Layer 10: Performance & Optimization",
    11: "Layer 11: Testing",
    12: "Layer 12: Production & Advanced Patterns",
}

REFERENCE_SECTIONS = [
    ("dependency-table", "Concept DAG & Dependency Table"),
    ("request-lifecycle", "FastAPI Request Lifecycle"),
    ("concurrency-timeline", "WSGI vs ASGI Timeline"),
    ("pydantic-pipeline", "Pydantic Validation Pipeline"),
    ("ecosystem-map", "FastAPI Ecosystem Map"),
    ("quick-reference", "Quick Reference"),
]

CLUSTER_CLASS = {
    "foundation": "cluster-foundation",
    "routing": "cluster-routing",
    "request": "cluster-request",
    "pydantic": "cluster-pydantic",
    "di": "cluster-di",
    "responses": "cluster-responses",
    "openapi": "cluster-openapi",
    "middleware": "cluster-middleware",
    "auth": "cluster-auth",
    "database": "cluster-database",
    "advanced": "cluster-advanced",
    "performance": "cluster-performance",
    "testing": "cluster-testing",
    "deployment": "cluster-deployment",
}

OTHER_LABELS = {
    "foundation": "Flask / Django",
    "routing": "Flask / Django",
    "request": "Starlette / Flask",
    "pydantic": "Manual dict validation",
    "di": "Flask globals",
    "responses": "Flask / Django",
    "openapi": "Hand-written docs",
    "middleware": "Starlette / Django",
    "auth": "Flask / Django",
    "database": "Sync ORM stack",
    "advanced": "Raw asyncio / Celery",
    "performance": "Blocking stack",
    "testing": "requests + manual fixtures",
    "deployment": "Gunicorn / containers",
}

CLUSTER_COMPARISON = {
    "foundation": (
        "You own the socket protocol boundary, concurrency model, and request scheduling details directly.",
        "FastAPI builds on Starlette's ASGI contract so one worker can overlap large amounts of network wait time.",
        "Flask and Django stay simpler to reason about when async throughput is not the bottleneck.",
    ),
    "routing": (
        "You parse method, path, and payload shapes manually and keep docs in sync by hand.",
        "FastAPI turns type-annotated functions into routes, validation rules, and OpenAPI operations together.",
        "Flask and Django route cleanly too, but they do not make typed schema generation the default.",
    ),
    "request": (
        "Headers, cookies, bodies, and files remain untyped byte streams until you normalize them yourself.",
        "FastAPI promotes request pieces into annotated parameters and validated response contracts.",
        "Starlette is the lower-level ASGI toolkit; Flask stays more permissive and manual at the boundary.",
    ),
    "pydantic": (
        "Dicts, casts, and ad-hoc validators drift over time and fail late in the DB or business layer.",
        "Pydantic v2 centralizes coercion, validation, serialization, and JSON Schema generation in one model system.",
        "Manual validation can be lighter, but it scales badly once payloads become nested or reused.",
    ),
    "di": (
        "Globals and implicit imports make tests brittle because state leaks across requests and modules.",
        "Depends builds a request-scoped graph so settings, auth, sessions, and caches are explicit and overridable.",
        "Flask tends to lean on app globals or extensions; FastAPI makes dependency graphs a first-class feature.",
    ),
    "responses": (
        "You serialize data and map errors to status codes manually, so contracts drift and edge cases leak fields.",
        "FastAPI combines response classes, response models, and exception handlers into a consistent API surface.",
        "Flask and Django can do the same, but more of the response contract is policy rather than default behavior.",
    ),
    "openapi": (
        "Docs become stale prose and client teams reverse-engineer your API from trial and error.",
        "FastAPI emits OpenAPI from code so docs, generated SDKs, and request validation stay aligned.",
        "Hand-written docs can be flexible, but they are much harder to keep correct under change.",
    ),
    "middleware": (
        "Cross-cutting behavior becomes wrapper soup with no shared lifecycle ordering story.",
        "FastAPI inherits Starlette middleware and lifespan hooks for headers, metrics, startup, shutdown, and mounted apps.",
        "Django has a rich middleware stack too, but FastAPI keeps the ASGI request pipeline more visible.",
    ),
    "auth": (
        "Parsing tokens, checking scopes, and preventing data leaks by hand leads to inconsistent access checks.",
        "FastAPI turns auth into dependencies that can guard routes, enrich docs, and standardize failures.",
        "Django favors session auth; Flask composes extensions; FastAPI is strongest when APIs are the center.",
    ),
    "database": (
        "Sync DB calls inside async handlers quietly block the event loop and erase concurrency gains.",
        "FastAPI works best with async sessions, yield dependencies, and explicit eager-loading in async ORM flows.",
        "A sync ORM stack can still be fine for smaller systems, but it needs honest throughput expectations.",
    ),
    "advanced": (
        "Long-lived sockets and background work are easy to start but hard to supervise or scale safely.",
        "FastAPI gives you WebSockets, SSE, and lightweight background tasks while leaving heavy job reliability to external workers.",
        "Raw asyncio or a dedicated worker system can be a better fit once coordination or durability dominates.",
    ),
    "performance": (
        "Async apps still lose badly when they create new pools and clients per request or serialize inefficiently.",
        "FastAPI can stay fast when I/O is pooled, responses are slim, and blocking work moves off the loop.",
        "A simpler sync stack can outperform a misused async stack, so architecture still matters more than branding.",
    ),
    "testing": (
        "Without structured overrides, every test boots too much of the real system and becomes fragile.",
        "FastAPI lets tests replace dependencies cleanly while keeping the real routing and validation path intact.",
        "Plain requests-based testing works, but it is slower and less precise for isolated API contracts.",
    ),
    "deployment": (
        "A fast local server does not become production-ready by itself: health checks, metrics, workers, and shutdown matter.",
        "FastAPI pairs cleanly with uvicorn workers, async DB pools, Redis, reverse proxies, and structured settings.",
        "Framework choice matters less than whether the deployment model respects async semantics and operational discipline.",
    ),
}

CLUSTER_SECURITY = {
    "foundation": "Blocking the event loop is a reliability bug and, under load, a denial-of-service vector you created yourself.",
    "routing": "Typed parameters reduce accidental over-trust, but you still need explicit authorization before returning sensitive resources.",
    "request": "Response models, strict parsing, and explicit headers prevent accidental data exposure and weak boundary handling.",
    "pydantic": "Validation closes whole classes of malformed-input bugs before they can turn into persistence or auth problems.",
    "di": "Dependencies are where auth, rate limits, and tenancy checks become reusable security boundaries rather than repeated controller code.",
    "responses": "The most common FastAPI leak is returning internal models directly; response_model is a security boundary, not just docs sugar.",
    "openapi": "OpenAPI improves client trust, but public docs still reveal contract surface, so decide deliberately what should be exposed in production.",
    "middleware": "CORS, request IDs, security headers, and lifespan-managed secrets all live here; bad defaults propagate to every route.",
    "auth": "JWT scope checks, API key hashing, and 401 vs 403 discipline are central to preventing broken object and function-level authorization.",
    "database": "Async does not change SQL injection rules or tenancy boundaries; always bind parameters and filter by the authenticated principal.",
    "advanced": "WebSockets and background workers open new trust boundaries because connections live longer and tasks can outlive the request that started them.",
    "performance": "Caching, compression, and worker tuning all trade speed against correctness; cache keys and shared state must respect identity and permissions.",
    "testing": "Security regressions usually happen in unhappy paths; tests need to cover forbidden, malformed, stale-token, and cross-tenant access.",
    "deployment": "Production hardening means HTTPS, secret rotation, least privilege, health probes, and observability that catches attacks before customers do.",
}

CLUSTER_WHEN_NOT = {
    "foundation": "If you are building a mostly synchronous admin site or server-rendered app, the async mental overhead may not buy enough value.",
    "routing": "If the API is tiny and unlikely to evolve, you may not need the full weight of typed route surface design yet.",
    "request": "If your boundary is internal and trusted, strict request modeling can be overkill compared with a lighter transport layer.",
    "pydantic": "For ultra-hot internal loops with trusted data, repeated validation can be unnecessary overhead compared with plain dataclasses or model_construct().",
    "di": "If the application is a single script with no testing or reuse needs, the dependency graph may feel heavier than direct calls.",
    "responses": "If you are returning a stream or proxying another service verbatim, a rich response model may be the wrong abstraction.",
    "openapi": "If the system is not an external API and client generation is irrelevant, heavy OpenAPI customization may not justify the effort.",
    "middleware": "If only one route needs behavior, a dependency or helper is usually simpler than global middleware.",
    "auth": "If you only need trusted internal service auth, a smaller mTLS or network-level approach may be better than full OAuth scope design.",
    "database": "If the workload is CPU-heavy or the DB driver is sync-only, a sync stack or worker queue can be a more honest fit.",
    "advanced": "If messages must survive restarts or require retries, in-process background patterns are not enough; use a real queue.",
    "performance": "If the system is nowhere near saturation, premature optimization adds complexity without improving user outcomes.",
    "testing": "If the change is pure presentation or docs, spinning up full async integration paths may be more than the risk warrants.",
    "deployment": "If the project is a local-only tool, Docker, Redis, Celery, and reverse proxies may be operational theater.",
}

CLUSTER_MISTAKES = {
    "foundation": [
        ("Calling time.sleep() inside async code", "The event loop cannot switch tasks while Python is blocked in a synchronous sleep.", "Use await asyncio.sleep() or move blocking work to a thread or worker."),
        ("Treating ASGI as just faster WSGI", "The interface and failure modes change; cancellation, connection lifetime, and shared pools matter.", "Design for async I/O explicitly instead of sprinkling async keywords over sync architecture."),
    ],
    "routing": [
        ("Encoding validation in docstrings instead of types", "The OpenAPI schema and runtime parser only know what the annotations declare.", "Move constraints into Path(), Query(), Header(), Cookie(), and response_model."),
        ("Hardcoding URLs into clients and examples", "Path changes break consumers and stale docs survive unnoticed.", "Use generated docs, endpoint cards, and consistent versioned routers."),
    ],
    "request": [
        ("Mixing JSON and multipart assumptions in one handler", "HTTP has one request Content-Type, so parsing rules conflict.", "Split endpoints or use UploadFile/Form explicitly for multipart routes."),
        ("Returning ORM objects directly", "Internal fields and lazy-loaded relationships leak or fail at serialization time.", "Project the response through a public schema."),
    ],
    "pydantic": [
        ("Using mutable defaults directly", "One shared list or dict leaks state across model instances.", "Use Field(default_factory=list) or dict."),
        ("Migrating v1 validators mechanically", "validator and root_validator semantics changed in v2.", "Use field_validator, model_validator, and field_serializer intentionally."),
    ],
    "di": [
        ("Importing a global session everywhere", "Tests cannot isolate state and request cleanup becomes accidental.", "Provide the session through a yield dependency."),
        ("Doing expensive setup inside every endpoint", "Repeated client and settings construction burns latency and hides lifecycle rules.", "Inject cached settings and shared clients through dependencies."),
    ],
    "responses": [
        ("Raising raw exceptions from business code", "Clients get inconsistent failure shapes and observability becomes noisy.", "Normalize failures through HTTPException or a custom handler."),
        ("Returning 200 for every outcome", "Clients cannot safely branch on success, creation, validation, or absence.", "Use accurate status codes and model the error payload."),
    ],
    "openapi": [
        ("Treating /docs as enough design", "The schema still needs curated summaries, examples, and version boundaries.", "Add operation metadata and keep old versions visible on purpose."),
        ("Publishing every internal route", "OpenAPI becomes an accidental reconnaissance surface.", "Disable or restrict docs where exposure is not acceptable."),
    ],
    "middleware": [
        ("Putting DB work in middleware without limits", "Every request pays the cost, even routes that do not need it.", "Reserve middleware for cross-cutting concerns and keep business I/O in dependencies."),
        ("Using allow_origins=['*'] with credentials=True", "Browsers reject it because wildcard origins cannot safely carry credentials.", "List trusted origins explicitly."),
    ],
    "auth": [
        ("Confusing 401 and 403", "Clients cannot tell whether they need to authenticate or whether access is forbidden.", "Use 401 for missing or invalid auth and 403 for authenticated but disallowed actions."),
        ("Storing plaintext API keys or JWT secrets", "A single leak becomes a full trust collapse.", "Hash API keys at rest and keep secrets in managed settings."),
    ],
    "database": [
        ("Using sync DB drivers inside async routes", "Every awaited path still blocks on the driver and collapses concurrency.", "Use AsyncSession, async drivers, or isolate sync work in executors."),
        ("Relying on lazy loading after the session closes", "DetachedInstanceError appears only after serialization or templating begins.", "Eager-load relationships with selectinload or joinedload."),
    ],
    "advanced": [
        ("Using BackgroundTasks for durable jobs", "Tasks vanish on process crash or restart because they stay in-process.", "Use Celery or another queue when reliability matters."),
        ("Accepting every WebSocket blindly", "Long-lived connections amplify auth and rate-limit mistakes.", "Authenticate before accept and track connection lifecycle explicitly."),
    ],
    "performance": [
        ("Creating a new AsyncClient or Redis connection per request", "Connection setup dominates the latency you were trying to save.", "Reuse pooled clients through lifespan or cached dependencies."),
        ("Compressing or caching without measurement", "CPU cost or stale data can outweigh any throughput win.", "Profile first, then tune the hot path with evidence."),
    ],
    "testing": [
        ("Hitting production dependencies in tests", "Tests become slow, flaky, and destructive.", "Override dependencies and use isolated test stores."),
        ("Only testing the happy path", "Validation and auth regressions slip through because failure cases are unverified.", "Exercise malformed, unauthorized, forbidden, and conflict paths."),
    ],
    "deployment": [
        ("Running uvicorn --reload in production", "Reload mode is a developer convenience, not a hardened process model.", "Use production workers, probes, and structured shutdown."),
        ("Treating async workers like CPU workers", "Worker counts and pool sizes diverge when the workload is I/O heavy.", "Tune with actual latency, DB pool sizes, and backpressure in mind."),
    ],
}

CLUSTER_PERF = {
    "foundation": ("4 sync workers ~= 40 RPS", "1 async worker ~= 400 RPS"),
    "routing": ("sync parsing ~= 180 RPS", "typed async handler ~= 320 RPS"),
    "request": ("manual boundary ~= 150 RPS", "validated boundary ~= 300 RPS"),
    "pydantic": ("manual checks ~= 1x baseline", "pydantic-core ~= 5-50x v1-era parsing"),
    "di": ("global setup repeated", "request graph cached once"),
    "responses": ("manual serialization ~= 1x", "orjson + response_model ~= 1.6x"),
    "openapi": ("docs drift over time", "schema stays generated on every change"),
    "middleware": ("blocking wrappers add queueing", "pure ASGI path keeps the loop clear"),
    "auth": ("hand-rolled guards drift", "dependency auth stays consistent"),
    "database": ("sync driver blocks loop", "async driver overlaps I/O"),
    "advanced": ("fire-and-forget loses work", "queue-backed work survives restarts"),
    "performance": ("new client per call", "pooled clients cut latency"),
    "testing": ("real services slow feedback", "dependency overrides keep tests fast"),
    "deployment": ("reload server only", "worker pool + probes + telemetry"),
}

FASTAPI_CORE_REQUIREMENTS = """fastapi==0.110.*
uvicorn[standard]==0.29.*
pydantic-settings==2.*
sqlalchemy[asyncio]==2.*
alembic==1.13.*
redis==5.*
httpx==0.27.*
pytest-asyncio==0.23.*
beanie==1.25.*
celery==5.4.*
"""

MINIMAL_ASGI_APP = """import json

async def app(scope, receive, send):
    assert scope["type"] == "http"
    body = json.dumps({"path": scope["path"], "method": scope["method"]}).encode()
    headers = [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())]
    await send({"type": "http.response.start", "status": 200, "headers": headers})
    await send({"type": "http.response.body", "body": body})
"""

DEFAULT_SYNC_EQUIVALENTS = {
    "foundation": MINIMAL_ASGI_APP,
    "routing": """from flask import Flask

app = Flask(__name__)

@app.get("/items/<int:item_id>")
def read_item(item_id):
    return {"item_id": item_id, "source": "sync"}
""",
    "request": """from flask import Flask, request

app = Flask(__name__)

@app.post("/upload")
def upload():
    return {"content_type": request.content_type, "header": request.headers.get("X-Token")}
""",
    "pydantic": """payload = {"name": "Keyboard", "price": "19.99"}
if not isinstance(payload.get("name"), str):
    raise ValueError("name must be text")
price = float(payload["price"])
""",
    "di": """settings = {"db_url": "postgresql://..."}
db = make_session(settings["db_url"])

def create_order(payload):
    return save_order(db, payload)
""",
    "responses": """from flask import jsonify

def create_product():
    return jsonify({"id": 1, "name": "Keyboard"}), 201
""",
    "openapi": """openapi = {
    "paths": {
        "/products": {
            "get": {"summary": "List products", "responses": {"200": {"description": "OK"}}}
        }
    }
}
""",
    "middleware": """class TimingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)
""",
    "auth": """def decode_bearer(header):
    if not header or not header.startswith("Bearer "):
        raise PermissionError("missing token")
    token = header.split(" ", 1)[1]
    return verify(token)
""",
    "database": """from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg://...")
with Session(engine) as session:
    rows = session.execute(select(Product)).scalars().all()
""",
    "advanced": """import asyncio

clients = set()

async def broadcast(message):
    await asyncio.gather(*(client.send_text(message) for client in clients))
""",
    "performance": """import requests

def fetch_user(user_id):
    return requests.get(f"https://api.example.com/users/{user_id}", timeout=5).json()
""",
    "testing": """import requests

response = requests.get("http://localhost:8000/health")
assert response.status_code == 200
""",
    "deployment": """gunicorn -k uvicorn.workers.UvicornWorker -w 4 app.main:app""",
}

SCHEMA_SNIPPETS = {
    "FA13": """{
  "title": "Product",
  "type": "object",
  "properties": {
    "id": {"title": "Id", "type": "integer"},
    "name": {"title": "Name", "type": "string"},
    "price": {"anyOf": [{"type": "number"}, {"type": "string"}], "title": "Price"}
  },
  "required": ["id", "name", "price"]
}""",
    "FA14": """{
  "title": "ProductInput",
  "type": "object",
  "properties": {
    "name": {"type": "string", "minLength": 3, "maxLength": 80},
    "price": {"type": "number", "exclusiveMinimum": 0},
    "tags": {"type": "array", "items": {"type": "string"}, "default": []}
  },
  "required": ["name", "price"]
}""",
    "FA15": """{
  "title": "OrderWindow",
  "type": "object",
  "properties": {
    "start_at": {"type": "string", "format": "date-time"},
    "end_at": {"type": "string", "format": "date-time"}
  },
  "required": ["start_at", "end_at"]
}""",
    "FA16": """{
  "oneOf": [
    {"$ref": "#/$defs/CreditCardPayment"},
    {"$ref": "#/$defs/BankTransferPayment"},
    {"$ref": "#/$defs/CryptoPayment"}
  ],
  "discriminator": {"propertyName": "kind"}
}""",
    "FA17": """{
  "title": "AccountSettings",
  "type": "object",
  "properties": {
    "email": {"type": "string", "format": "email"},
    "callback_url": {"type": "string", "format": "uri"},
    "api_key": {"type": "string", "writeOnly": true}
  },
  "required": ["email", "callback_url", "api_key"]
}""",
    "FA18": """{
  "title": "Settings",
  "type": "object",
  "properties": {
    "app_name": {"type": "string"},
    "database_url": {"type": "string"},
    "redis_url": {"type": "string"}
  },
  "required": ["database_url", "redis_url"]
}""",
    "FA19": """{
  "title": "TrustedInternalOrder",
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "total": {"type": "number"},
    "validated": {"type": "boolean", "default": false}
  },
  "required": ["id", "total"]
}""",
}

VERSION_NOTES = {
    "FA13": "Pydantic v2 replaces parse_obj and dict() era APIs with model_validate() and model_dump(); v1 examples on blogs need translation.",
    "FA15": "The v1 validator and root_validator decorators changed to field_validator and model_validator in v2. The modes are clearer, but migration is not a search-and-replace.",
    "FA18": "Settings now live in pydantic-settings rather than BaseSettings inside core Pydantic. Older tutorials often miss this split.",
    "FA36": "lifespan supersedes the older on_event startup and shutdown style for new FastAPI apps and gives one place to manage startup and teardown together.",
    "FA43": "FastAPI 0.110+ works cleanly with SQLAlchemy 2.0 async style. Old 1.4 transitional snippets often mix sync and async patterns badly.",
}

ENDPOINT_META = {
    "FA06": ("GET", "/products"),
    "FA07": ("GET", "/products/{product_id}"),
    "FA08": ("GET", "/products?category=keyboards&limit=20"),
    "FA09": ("POST", "/products"),
    "FA10": ("GET", "/profile"),
    "FA11": ("POST", "/upload"),
    "FA12": ("GET", "/users/me"),
    "FA25": ("GET", "/exports/orders.csv"),
    "FA26": ("POST", "/orders"),
    "FA27": ("GET", "/orders/{order_id}"),
    "FA28": ("POST", "/emails/welcome"),
    "FA29": ("POST", "/webhooks/order-paid"),
    "FA30": ("GET", "/v1/orders"),
    "FA31": ("GET", "/docs"),
    "FA32": ("GET", "/openapi.json"),
    "FA33": ("GET", "/v2/products"),
    "FA38": ("POST", "/token"),
    "FA39": ("GET", "/users/me"),
    "FA40": ("GET", "/reports"),
    "FA41": ("GET", "/partners/inventory"),
    "FA49": ("WS", "/ws/chat"),
    "FA50": ("GET", "/events"),
    "FA56": ("GET", "/health"),
    "FA57": ("GET", "/products/stream"),
    "FA59": ("GET", "/health"),
}


def spec(id, layer, cluster, title, prereqs, summary, detail):
    return {
        "id": id,
        "layer": layer,
        "cluster": cluster,
        "title": title,
        "prereqs": prereqs,
        "summary": summary,
        "detail": detail,
    }


CONCEPT_SPECS = [
    spec("FA01", 0, "foundation", "WSGI vs ASGI - The Fundamental Difference", [], "ASGI keeps connections in an event loop so one worker can overlap many I/O waits instead of dedicating a blocking thread or process to each request.", "Understand scope receive send, why I/O-bound APIs benefit from async concurrency, and why WSGI remains acceptable for CPU-heavy or template-heavy workloads."),
    spec("FA02", 0, "foundation", "asyncio Foundations for FastAPI", [], "FastAPI's performance story only holds if you understand coroutines, await points, and the rule that blocking the event loop blocks every other request on that worker.", "Cover tasks, gather, cancellation, thread executors for blocking code, and the difference between yielding control and finishing CPU work."),
    spec("FA03", 0, "foundation", "Starlette Under the Hood", [], "FastAPI is a higher-level layer over Starlette, so Starlette's ASGI request, response, routing, and middleware model explains most of FastAPI's runtime behavior.", "FastAPI inherits Starlette primitives and adds validation, dependency injection, and docs rather than replacing the ASGI foundation underneath."),
    spec("FA04", 0, "foundation", "What is FastAPI? Why FastAPI?", [], "FastAPI combines async-first request handling, Pydantic validation, and auto-generated OpenAPI so API contracts, docs, and runtime parsing stay aligned.", "Contrast FastAPI with Flask and Django honestly: FastAPI wins for typed APIs and I/O-bound concurrency, not for built-in admin or full-stack HTML workflows."),
    spec("FA05", 0, "foundation", "FastAPI Application Setup", [], "The minimum app is tiny, but production-ready structure still needs uvicorn, modular routers, settings, and a project layout that separates schemas, routes, and persistence.", "Explain FastAPI(), uvicorn.run(), reload mode, package layout, and why gunicorn needs uvicorn workers rather than plain sync workers for async apps."),
    spec("FA06", 1, "routing", "Path Operations", ["FA01", "FA02", "FA03", "FA04", "FA05"], "A type-annotated function plus an HTTP method decorator becomes a routed operation, an input parser, and an OpenAPI operation object at the same time.", "Show GET POST PUT PATCH DELETE semantics, async def versus def handlers, and the contract surface FastAPI derives from each declaration."),
    spec("FA07", 1, "routing", "Path Parameters", ["FA06"], "Path parameters are validated from the URL itself, with types, constraints, enums, and ordering rules that also feed directly into the generated schema.", "Use Annotated with Path(), explain why /users/me must appear before /users/{user_id}, and show how special path converters affect routing precedence."),
    spec("FA08", 1, "routing", "Query Parameters", ["FA06"], "Parameters not claimed by the path become query parameters, so defaults, Optional values, aliases, and typed lists shape both runtime parsing and the docs surface.", "Cover Query() constraints, repeated parameters like ?id=1&id=2, and how deprecation flags show up in Swagger UI."),
    spec("FA09", 1, "request", "Request Body", ["FA06"], "Pydantic models turn JSON bodies into validated Python objects, letting one handler cleanly combine body, path, and query data without hand-written parsing.", "Explain Body(), embed=True, multiple body parameters, and Field() metadata that becomes JSON Schema."),
    spec("FA10", 1, "request", "Headers & Cookies", ["FA06"], "Header() and Cookie() promote transport metadata into typed parameters so auth, tracing, and feature flags stay explicit instead of buried in manual request access.", "Show underscore-to-dash conversion, repeated headers, response header mutation, and the difference between request cookies and response cookies."),
    spec("FA11", 1, "request", "Form Data & File Upload", ["FA09"], "multipart/form-data has different parsing rules from JSON, so forms and file uploads need explicit Form(), File(), and UploadFile boundaries.", "Show why JSON and multipart cannot share one body parser, why UploadFile streams better than raw bytes, and how to process multiple files safely."),
    spec("FA12", 1, "responses", "Response Model", ["FA09"], "response_model is both documentation and a security boundary because it filters output fields before they leave the API.", "Cover exclude and include switches, input versus output schemas, and the common mistake of leaking hashed_password or internal flags by returning DB models directly."),
    spec("FA13", 2, "pydantic", "Pydantic v2 Fundamentals", ["FA09"], "Pydantic v2 uses pydantic-core for fast parsing, validation, serialization, and schema generation, so one model definition drives runtime behavior and documentation.", "Use model_validate(), model_dump(), model_dump_json(), and model_json_schema() while noting the shift from older v1-era API names."),
    spec("FA14", 2, "pydantic", "Pydantic Field Validation", ["FA13"], "Field() centralizes numeric, string, alias, and default rules so business input constraints stop being scattered across route handlers.", "Explain gt ge lt le, min_length, regex patterns, default_factory, and the difference between alias, validation_alias, and serialization_alias."),
    spec("FA15", 2, "pydantic", "Pydantic Custom Validators", ["FA14"], "field_validator, model_validator, and serializer hooks let you express preprocessing, cross-field validation, and controlled output formatting inside the schema layer.", "Show before after wrap modes, cross-field date checks, serializer hooks, and the migration path away from validator and root_validator."),
    spec("FA16", 2, "pydantic", "Pydantic Nested Models", ["FA13"], "Nested models, unions, discriminators, and forward references let one API contract describe realistic payloads instead of flat demo objects.", "Cover recursive comments, oneOf schemas, discriminated payment models, and model_rebuild() for circular type references."),
    spec("FA17", 2, "pydantic", "Pydantic Types", ["FA13"], "Built-in types like EmailStr, SecretStr, UUID, timezone-aware datetime, and constrained annotated types prevent common data-shape bugs with almost no extra route code.", "Explain why SecretStr protects logs, when Decimal beats float, and how annotated constraints replace older helper classes cleanly."),
    spec("FA18", 2, "pydantic", "Pydantic Settings", ["FA13"], "pydantic-settings turns environment variables and .env files into validated app configuration so secrets and deployment-specific values stop living in code.", "Show nested settings, env precedence, cached get_settings(), and why a dependency-based settings singleton is easier to test than a raw global."),
    spec("FA19", 2, "pydantic", "Pydantic Performance", ["FA13"], "Validation is cheap enough for request boundaries, but internal hot paths still need judgment about revalidation, discriminated unions, and trusted data shortcuts.", "Explain model_construct(), validate_assignment overhead, v2 benchmark gains, and where schema complexity can still cost real CPU."),
    spec("FA20", 3, "di", "Dependency Injection Fundamentals", ["FA05", "FA13"], "Depends lets handlers declare needs instead of reaching for globals, and FastAPI resolves that graph per request with caching and teardown support.", "Use a request graph like get_db to get_current_user to create_order to explain why explicit dependencies make testing and authorization simpler."),
    spec("FA21", 3, "di", "Simple Dependencies", ["FA20"], "Function, class, and Annotated dependencies turn shared parsing or setup logic into reusable building blocks without hiding what each route needs.", "Show common query params, class-based dependencies with __call__, and why Annotated syntax reads better in larger codebases."),
    spec("FA22", 3, "di", "Dependencies with yield", ["FA20"], "yield dependencies are FastAPI's setup and teardown primitive for DB sessions, clients, and file handles because finally blocks still run after endpoint errors.", "Explain exception flow, nested yield ordering, and why session-per-request works naturally with AsyncSession."),
    spec("FA23", 3, "di", "Global & Scoped Dependencies", ["FA20"], "Dependencies can be attached at app, router, or route scope so auth, tenancy, and settings stay close to the surface they guard.", "Show app-level defaults, router-level admin checks, and test overrides through app.dependency_overrides."),
    spec("FA24", 3, "di", "Advanced DI Patterns", ["FA20", "FA21", "FA22", "FA23"], "Dependency caching, use_cache=False, dependency-based lookup helpers, and lru_cache settings singletons let FastAPI compose rich application state without hidden globals.", "Use dependencies for security, object loading, expensive config, and per-request memoization while keeping object lifetimes explicit."),
    spec("FA25", 4, "responses", "Response Classes", ["FA06", "FA13"], "FastAPI can return plain JSON by default, but explicit response classes matter for files, streams, redirects, HTML, and custom media types.", "Cover Response, JSONResponse, FileResponse, StreamingResponse, RedirectResponse, and background tasks attached to responses."),
    spec("FA26", 4, "responses", "Status Codes", ["FA25"], "Accurate status codes are part of the API contract, not decoration, so creation, emptiness, validation, and deletion should all communicate intent precisely.", "Explain 200 versus 201, 204 No Content, status_code on decorators, and why POST does not magically imply 201 unless you declare it."),
    spec("FA27", 4, "responses", "HTTPException", ["FA25", "FA13"], "HTTPException and custom handlers keep failure shapes predictable, while RequestValidationError handlers let you transform raw validation detail into friendlier client contracts.", "Show route-level errors, global exception handlers, and validation error reshaping without losing the underlying data."),
    spec("FA28", 4, "responses", "Background Tasks", ["FA25", "FA20"], "BackgroundTasks are convenient for tiny post-response work, but they stay in the same process and die with that process, so they are not a durable job queue.", "Use email or audit logging examples and draw the line where Celery or another worker system becomes necessary."),
    spec("FA29", 4, "responses", "Webhooks", ["FA25", "FA13"], "Webhook declarations document the outbound calls your API will make, which matters when external integrators depend on your event payload contract.", "Use app.webhooks to publish callback schemas and treat outbound event shapes as public API surface too."),
    spec("FA30", 5, "openapi", "APIRouter", ["FA06", "FA25"], "APIRouter groups paths, prefixes, dependencies, and tags so large APIs stay modular without giving up a single combined OpenAPI schema.", "Show separate auth, products, and orders routers, router-level dependencies, and versioned routers living side by side."),
    spec("FA31", 5, "openapi", "OpenAPI & Swagger UI", ["FA30", "FA12"], "FastAPI turns route metadata and Pydantic models into live /docs and /redoc output, which means the docs become a direct reflection of the running contract.", "Explain schema generation, docs_url, redoc_url, openapi_url customization, and what changes when docs are disabled in production."),
    spec("FA32", 5, "openapi", "OpenAPI Customization", ["FA31"], "Operation summaries, descriptions, response metadata, examples, and tags turn auto-generated docs into an API product teams can actually consume.", "Show summary, description, deprecated, operation_id, custom response descriptions, and extra responses with models."),
    spec("FA33", 5, "openapi", "API Versioning", ["FA30", "FA31"], "Versioning is a routing and client-communication problem, not just a URL trick, so routers, docs, and deprecation strategy need to move together.", "Compare path and header versioning, explain coexistence of v1 and v2 routers, and show how to phase out old clients without breaking them blindly."),
    spec("FA34", 6, "middleware", "Middleware in FastAPI", ["FA05", "FA30"], "Middleware handles cross-cutting concerns around the request pipeline, but the wrong abstraction or ordering choice can add latency to every route.", "Contrast decorator-style HTTP middleware with BaseHTTPMiddleware and pure ASGI middleware, including request ID and timing examples."),
    spec("FA35", 6, "middleware", "CORS Middleware", ["FA34"], "CORS is a browser policy negotiation, not a FastAPI feature, so CORSMiddleware exists to emit the exact headers browsers require for cross-origin calls.", "Explain preflight OPTIONS requests, credentials restrictions, allowed origins, and why wildcard origins and credentials cannot be combined."),
    spec("FA36", 6, "middleware", "Lifespan Events", ["FA05", "FA22"], "lifespan is the application-wide setup and teardown boundary for pools, clients, models, and caches, replacing scattered startup and shutdown hooks.", "Use an asynccontextmanager to open DB pools, warm caches, and close resources deterministically when the process stops."),
    spec("FA37", 6, "middleware", "Mounting Sub-Applications", ["FA34", "FA36"], "Mounted ASGI apps let one process serve static files, admin tools, SPAs, or other ASGI apps under clean URL boundaries.", "Show StaticFiles, mounted Starlette apps, and the pattern of serving a React frontend beside an API."),
    spec("FA38", 7, "auth", "Security Utilities", ["FA20", "FA27"], "FastAPI's built-in security helpers model auth schemes as dependencies so the docs and the runtime both understand what credentials a route expects.", "Cover OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBearer, APIKeyHeader, and APIKeyCookie with the trade-offs of each."),
    spec("FA39", 7, "auth", "JWT Authentication", ["FA38"], "JWT auth in FastAPI is usually a dependency chain: extract bearer token, decode, validate claims, fetch user, then reject or enrich the request.", "Explain access and refresh tokens, sub exp scopes, get_current_user, and the exact difference between invalid authentication and insufficient permission."),
    spec("FA40", 7, "auth", "OAuth2 Scopes", ["FA39"], "Scopes let tokens describe what they may do, and SecurityScopes makes those requirements visible in code and Swagger UI authorization flows.", "Show read versus write scopes, hierarchical checks, and token endpoints that issue scope-aware claims."),
    spec("FA41", 7, "auth", "API Keys", ["FA38"], "API keys are still useful for server-to-server trust, but they need rotation, hashing, tracking, and rate limits to avoid becoming invisible root passwords.", "Model APIKeyHeader dependencies, hash keys at rest, and treat every key as an auditable principal."),
    spec("FA42", 7, "auth", "Security Best Practices", ["FA38", "FA39", "FA41"], "Framework features help, but API security still comes down to object authorization, data minimization, rate limits, HTTPS, and explicit trust boundaries.", "Map OWASP API risks to FastAPI examples, especially broken object level authorization, excessive exposure, and missing throttling."),
    spec("FA43", 8, "database", "Async Database Options", ["FA22", "FA36"], "The first database decision is not ORM brand but whether the driver truly matches your async request model.", "Compare async SQLAlchemy 2.0, Beanie for MongoDB, Redis for ephemeral state, and the cost of keeping sync drivers inside async APIs."),
    spec("FA44", 8, "database", "Async SQLAlchemy Setup", ["FA43"], "Async SQLAlchemy needs an async engine, async_sessionmaker, and a yield dependency so each request gets a clean AsyncSession lifecycle.", "Show create_async_engine, async_sessionmaker, get_db, and session-per-request with proper cleanup."),
    spec("FA45", 8, "database", "Async SQLAlchemy Models & Queries", ["FA44"], "Querying with AsyncSession is explicit: await execute(select(...)), project scalars, and eager-load relationships because implicit lazy loading breaks in async flows.", "Cover selects, updates, deletes, scalars(), scalar_one_or_none(), and the DetachedInstanceError trap."),
    spec("FA46", 8, "database", "Alembic with Async SQLAlchemy", ["FA44"], "Migrations remain synchronous in spirit even when the app is async, so Alembic needs a clear async engine configuration rather than magical runtime reuse.", "Show env.py wiring, run_migrations_online, autogenerate, and why schema migration discipline still matters in async apps."),
    spec("FA47", 8, "database", "MongoDB with Beanie ODM", ["FA43"], "Beanie gives FastAPI a document-model option when flexible schema, embedded documents, or geospatial-style workloads fit MongoDB better than a relational model.", "Use AsyncIOMotorClient, Document classes, queries, and an example aggregation pipeline for analytics."),
    spec("FA48", 8, "database", "Redis with FastAPI", ["FA43"], "Redis is the usual companion for caching, sliding-window rate limits, pub-sub, and small cross-worker coordination in FastAPI deployments.", "Show async redis clients, cache-aside reads, invalidation on writes, and a sorted-set rate limit pattern."),
    spec("FA49", 9, "advanced", "WebSockets in FastAPI", ["FA03", "FA36"], "WebSockets let one HTTP upgrade become a long-lived duplex channel, which changes connection lifecycle, auth timing, and broadcast design completely.", "Use WebSocket.accept(), receive_text(), send_text(), connection managers, and token checks during the upgrade path."),
    spec("FA50", 9, "advanced", "Server-Sent Events (SSE)", ["FA25", "FA36"], "SSE is often enough for one-way live updates and stays simpler than a full WebSocket channel when the server only needs to push data out.", "Show event-stream responses, generator functions, and when browser-native EventSource beats a heavier bidirectional socket."),
    spec("FA51", 9, "advanced", "Background Processing Patterns", ["FA28", "FA36"], "FastAPI offers lightweight in-process work, but real systems need a clear line between trivial callbacks, supervised tasks, and durable job queues.", "Compare BackgroundTasks, asyncio.create_task, and Celery with an emphasis on supervision, retries, and shutdown behavior."),
    spec("FA52", 10, "performance", "Profiling FastAPI", ["FA44", "FA49"], "Performance work starts with measurement: profile the event loop, observe blocking calls, and load-test the real API shape rather than optimizing by instinct.", "Use py-spy, asyncio debug mode, and Locust to find where time is actually spent in an async service."),
    spec("FA53", 10, "performance", "Connection Pooling", ["FA44", "FA48"], "Async performance collapses when DB, Redis, or HTTP clients are created per request because setup cost replaces the concurrency win you expected.", "Tune pool_size, max_overflow, pre_ping, Redis pools, and httpx.AsyncClient reuse through lifespan or cached dependencies."),
    spec("FA54", 10, "performance", "Response Optimization", ["FA25", "FA52"], "Fast handlers can still waste time serializing too much JSON, compressing the wrong payloads, or returning uncached responses for immutable data.", "Show ORJSONResponse, GZipMiddleware, ETags, and the trade-offs around HTTP2 and alternative payload encodings."),
    spec("FA55", 10, "performance", "Scaling FastAPI", ["FA34", "FA53", "FA54"], "Scaling is a composition problem: workers, pools, stateless design, and background job boundaries all have to agree with the async request model.", "Explain uvicorn workers under gunicorn, readiness and liveness probes, shared Redis state, and when CPU-bound work belongs in executors or separate services."),
    spec("FA56", 11, "testing", "Testing with TestClient", ["FA20", "FA30", "FA44"], "TestClient drives the real routing and validation stack synchronously, which makes it ideal for fast request-level tests around a mostly async app.", "Show dependency overrides, authentication setup, and an in-memory test DB while noting that the client itself hides the async internals."),
    spec("FA57", 11, "testing", "Async Testing with pytest-asyncio", ["FA56", "FA44"], "Once the test itself needs await or direct async clients, pytest-asyncio and httpx.AsyncClient let you exercise the ASGI app without flattening async behavior.", "Cover anyio backends, async fixtures, event loop scope, and websocket or streaming tests."),
    spec("FA58", 11, "testing", "Testing Strategies", ["FA56", "FA57", "FA31"], "A reliable FastAPI test suite mixes unit, integration, auth, schema, and contract tests instead of assuming one tool covers every risk.", "Use dependency overrides for unit isolation, real stores for integration confidence, and schemathesis for OpenAPI-based fuzzing."),
    spec("FA59", 12, "deployment", "Production Deployment", ["FA36", "FA44", "FA48", "FA55", "FA58"], "A production FastAPI stack needs async-safe workers, health checks, structured settings, metrics, tracing, and clean shutdown around the app itself.", "Tie together uvicorn workers, Docker, PostgreSQL async, Redis, Celery, Prometheus, OpenTelemetry, and graceful rolling deploy behavior."),
]

SAMPLES = {
    "FA01": """import asyncio

async def app(scope, receive, send):
    assert scope["type"] == "http"
    await asyncio.sleep(0.1)  # pretend this is a database call
    body = b'{"message":"ASGI kept the worker free while waiting"}'
    await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"application/json")]})
    await send({"type": "http.response.body", "body": body})
""",
    "FA02": """import asyncio

async def fetch_price(source):
    await asyncio.sleep(0.1)
    return {source: 19.99}

async def main():
    prices = await asyncio.gather(fetch_price("db"), fetch_price("redis"), fetch_price("api"))
    return prices
""",
    "FA03": """from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/debug")
async def debug(request: Request):
    return {"path": request.url.path, "client": request.client.host}
""",
    "FA04": """from fastapi import FastAPI

app = FastAPI(title="Store API", version="1.0.0")

@app.get("/health")
async def health():
    return {"status": "ok", "framework": "FastAPI"}
""",
    "FA05": """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"docs": "/docs"}

# uvicorn app.main:app --reload
""",
    "FA06": """from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
async def list_products():
    return [{"id": 1, "name": "Keyboard"}]
""",
    "FA07": """from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/products/{product_id}")
async def get_product(product_id: Annotated[int, Path(ge=1, title="Database id")]):
    return {"product_id": product_id}
""",
    "FA08": """from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/products")
async def search_products(limit: Annotated[int, Query(ge=1, le=100)] = 20, q: str | None = None):
    return {"limit": limit, "query": q}
""",
    "FA09": """from pydantic import BaseModel
from fastapi import Body, FastAPI

class ProductCreate(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.post("/products")
async def create_product(product: ProductCreate, notify: bool = Body(default=False)):
    return {"created": product.model_dump(), "notify": notify}
""",
    "FA10": """from typing import Annotated
from fastapi import Cookie, FastAPI, Header, Response

app = FastAPI()

@app.get("/profile")
async def profile(x_request_id: Annotated[str | None, Header()] = None, session_id: Annotated[str | None, Cookie()] = None, response: Response = None):
    response.headers["X-Handled-By"] = "fastapi"
    return {"request_id": x_request_id, "session_id": session_id}
""",
    "FA11": """from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

@app.post("/upload")
async def upload_avatar(user_id: Annotated[str, Form()], avatar: Annotated[UploadFile, File()]):
    content = await avatar.read()
    return {"user_id": user_id, "filename": avatar.filename, "bytes": len(content)}
""",
    "FA12": """from pydantic import BaseModel, EmailStr
from fastapi import FastAPI

class UserInternal(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str

class UserPublic(BaseModel):
    id: int
    email: EmailStr

app = FastAPI()

@app.get("/users/me", response_model=UserPublic)
async def read_me():
    return UserInternal(id=1, email="dev@example.com", hashed_password="secret")
""",
    "FA13": """from decimal import Decimal
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: Decimal

payload = {"id": "1", "name": "Keyboard", "price": "19.99"}
product = Product.model_validate(payload)
schema = Product.model_json_schema()
""",
    "FA14": """from pydantic import BaseModel, Field

class ProductInput(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    price: float = Field(gt=0)
    tags: list[str] = Field(default_factory=list)
""",
    "FA15": """from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator

class OrderWindow(BaseModel):
    start_at: datetime
    end_at: datetime

    @field_validator("start_at", "end_at", mode="before")
    @classmethod
    def parse_dates(cls, value):
        return value

    @model_validator(mode="after")
    def ensure_order(self):
        if self.end_at <= self.start_at:
            raise ValueError("end_at must be after start_at")
        return self
""",
    "FA16": """from typing import Literal
from pydantic import BaseModel

class CreditCardPayment(BaseModel):
    kind: Literal["card"]
    last4: str

class BankTransferPayment(BaseModel):
    kind: Literal["bank"]
    iban: str

Payment = CreditCardPayment | BankTransferPayment
""",
    "FA17": """from datetime import datetime
from decimal import Decimal
from pydantic import AnyHttpUrl, BaseModel, EmailStr, SecretStr

class AccountSettings(BaseModel):
    email: EmailStr
    callback_url: AnyHttpUrl
    api_key: SecretStr
    credit_limit: Decimal
    created_at: datetime
""",
    "FA18": """from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    database_url: str
    redis_url: str
    app_name: str = "Store API"

@lru_cache
def get_settings() -> Settings:
    return Settings()
""",
    "FA19": """from pydantic import BaseModel

class TrustedInternalOrder(BaseModel):
    id: str
    total: float

order = TrustedInternalOrder.model_construct(id="ord_1", total=42.0)
""",
    "FA20": """from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

async def get_settings():
    return {"currency": "USD"}

@app.get("/orders")
async def list_orders(settings: Annotated[dict, Depends(get_settings)]):
    return {"currency": settings["currency"]}
""",
    "FA21": """from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 20):
        self.skip = skip
        self.limit = limit

@app.get("/products")
async def list_products(params: Annotated[CommonQueryParams, Depends()]):
    return {"skip": params.skip, "limit": params.limit}
""",
    "FA22": """from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncIterator[AsyncSession]:
    session = async_sessionmaker()
    try:
        yield session
    finally:
        await session.close()
""",
    "FA23": """from fastapi import APIRouter, Depends, FastAPI

async def require_admin():
    return {"role": "admin"}

router = APIRouter(prefix="/admin", dependencies=[Depends(require_admin)])
app = FastAPI(dependencies=[Depends(lambda: {"app": "store"})])
app.include_router(router)
""",
    "FA24": """from functools import lru_cache
from typing import Annotated
from fastapi import Depends

@lru_cache
def get_settings():
    return {"feature_flag": True}

async def get_item_or_404(item_id: int, settings: Annotated[dict, Depends(get_settings)]):
    return {"item_id": item_id, "feature_flag": settings["feature_flag"]}
""",
    "FA25": """from fastapi import FastAPI
from fastapi.responses import FileResponse, ORJSONResponse, StreamingResponse

app = FastAPI()

@app.get("/exports/orders.csv", response_class=FileResponse)
async def download_orders():
    return "exports/orders.csv"
""",
    "FA26": """from fastapi import FastAPI, status

app = FastAPI()

@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order():
    return {"id": "ord_1", "status": "created"}
""",
    "FA27": """from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponse(status_code=422, content={"errors": exc.errors()})

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    raise HTTPException(status_code=404, detail="order not found")
""",
    "FA28": """from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def send_email(address: str) -> None:
    print("sending", address)

@app.post("/emails/welcome")
async def welcome(address: str, tasks: BackgroundTasks):
    tasks.add_task(send_email, address)
    return {"queued": True}
""",
    "FA29": """from fastapi import FastAPI
from pydantic import BaseModel

class OrderPaid(BaseModel):
    order_id: str
    total: float

app = FastAPI()
app.webhooks.post("order-paid")(lambda payload: payload)
""",
    "FA30": """from fastapi import APIRouter, FastAPI

products_router = APIRouter(prefix="/products", tags=["products"])

@products_router.get("/")
async def list_products():
    return []

app = FastAPI()
app.include_router(products_router, prefix="/v1")
""",
    "FA31": """from fastapi import FastAPI

app = FastAPI(
    title="Store API",
    version="1.0.0",
    description="Typed e-commerce API",
    contact={"name": "API Team", "email": "api@example.com"},
)
""",
    "FA32": """from fastapi import FastAPI
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    code: int
    message: str

app = FastAPI()

@app.get("/products/{product_id}", summary="Read one product", responses={404: {"model": ErrorDetail, "description": "Product missing"}})
async def read_product(product_id: int):
    return {"id": product_id}
""",
    "FA33": """from fastapi import APIRouter, FastAPI

v1 = APIRouter(prefix="/v1")
v2 = APIRouter(prefix="/v2")

@v2.get("/products")
async def list_products_v2():
    return [{"version": 2}]

app = FastAPI()
app.include_router(v1)
app.include_router(v2)
""",
    "FA34": """import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
    return response
""",
    "FA35": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)
""",
    "FA36": """from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = build_http_client()
    yield
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)
""",
    "FA37": """from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/app", StaticFiles(directory="frontend/dist", html=True), name="spa")
""",
    "FA38": """from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
app = FastAPI()

@app.get("/me")
async def me(token: str = Depends(oauth2_scheme)):
    return {"token_preview": token[:6]}
""",
    "FA39": """from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "change-me"

def create_access_token(sub: str) -> str:
    payload = {"sub": sub, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
""",
    "FA40": """from typing import Annotated
from fastapi import Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", scopes={"read:reports": "Read reports"})

async def require_scopes(security_scopes: SecurityScopes, token: Annotated[str, Security(oauth2_scheme, scopes=["read:reports"])]):
    return {"required": security_scopes.scopes, "token": token}
""",
    "FA41": """from fastapi import Depends, FastAPI
from fastapi.security import APIKeyHeader

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)
app = FastAPI()

@app.get("/partners/inventory")
async def partner_inventory(api_key: str | None = Depends(api_key_scheme)):
    return {"api_key_present": bool(api_key)}
""",
    "FA42": """from typing import Annotated
from fastapi import Depends, HTTPException

async def require_order_owner(order_id: str, user=Depends(get_current_user)):
    order = await load_order(order_id)
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="forbidden")
    return order
""",
    "FA43": """from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from beanie import init_beanie
from redis.asyncio import Redis

engine = create_async_engine("postgresql+asyncpg://...")
redis = Redis.from_url("redis://localhost:6379/0")
""",
    "FA44": """from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine("postgresql+asyncpg://app:pass@db/store")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
""",
    "FA45": """from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def list_orders(session):
    stmt = select(Order).options(selectinload(Order.items)).order_by(Order.id.desc())
    result = await session.execute(stmt)
    return result.scalars().all()
""",
    "FA46": """from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

def run_migrations_online():
    connectable = async_engine_from_config(context.config.get_section(context.config.config_ini_section))
    # asyncio.run(run_async_migrations(connectable))
""",
    "FA47": """from beanie import Document
from pydantic import Field

class ProductDocument(Document):
    sku: str = Field(index=True)
    title: str
    tags: list[str] = []

docs = await ProductDocument.find(ProductDocument.tags == "keyboard").to_list()
""",
    "FA48": """from redis.asyncio import Redis

redis = Redis.from_url("redis://localhost:6379/0", decode_responses=True)

async def cache_aside(key: str, loader):
    cached = await redis.get(key)
    if cached:
        return cached
    value = await loader()
    await redis.set(key, value, ex=60)
    return value
""",
    "FA49": """from fastapi import FastAPI, WebSocket

app = FastAPI()
connections: list[WebSocket] = []

@app.websocket("/ws/chat")
async def chat(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    while True:
        text = await ws.receive_text()
        for conn in connections:
            await conn.send_text(text)
""",
    "FA50": """import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def event_stream():
    while True:
        yield "data: price-updated\\n\\n"
        await asyncio.sleep(1)

@app.get("/events")
async def events():
    return StreamingResponse(event_stream(), media_type="text/event-stream")
""",
    "FA51": """import asyncio
from fastapi import BackgroundTasks

async def refresh_cache():
    await asyncio.sleep(0.1)

async def handle_checkout(tasks: BackgroundTasks):
    tasks.add_task(write_audit_log, "checkout")
    asyncio.create_task(refresh_cache())
""",
    "FA52": """# locustfile.py
from locust import HttpUser, task

class ApiUser(HttpUser):
    @task
    def products(self):
        self.client.get("/products")
""",
    "FA53": """import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=5.0)
    yield
    await app.state.http.aclose()
""",
    "FA54": """from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)
app.add_middleware(GZipMiddleware, minimum_size=1000)
""",
    "FA55": """# gunicorn_conf.py
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 30

# health probes
# GET /health -> checks db, redis, and app readiness
""",
    "FA56": """from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
""",
    "FA57": """import pytest
from httpx import ASGITransport, AsyncClient

@pytest.mark.anyio
async def test_products():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/products")
    assert response.status_code == 200
""",
    "FA58": """def test_read_order_forbidden(client, forbidden_token):
    response = client.get("/orders/ord_2", headers={"Authorization": f"Bearer {forbidden_token}"})
    assert response.status_code == 403

# schemathesis run http://localhost:8000/openapi.json
""",
    "FA59": """services:
  api:
    command: gunicorn -k uvicorn.workers.UvicornWorker -w 4 app.main:app
  db:
    image: postgres:16
  redis:
    image: redis:7
  worker:
    command: celery -A app.worker worker -l info
""",
}


def concept_openapi(item) -> str:
    endpoint = ENDPOINT_META.get(item["id"])
    if not endpoint:
        return "{}"
    method, path = endpoint
    method_key = "get" if method == "WS" else method.lower()
    response_code = "201" if method == "POST" else "200"
    return dedent(
        f"""\
        {{
          "paths": {{
            "{path}": {{
              "{method_key}": {{
                "summary": "{item['title']}",
                "operationId": "{item['id'].lower()}",
                "responses": {{
                  "{response_code}": {{"description": "Successful response"}}
                }}
              }}
            }}
          }}
        }}"""
    )


def concept_curl(item) -> str:
    endpoint = ENDPOINT_META.get(item["id"])
    if not endpoint:
        return "curl -X GET http://localhost:8000/health"
    method, path = endpoint
    url = f"http://localhost:8000{path}"
    if method == "POST":
        return f"curl -X POST {url} -H 'Content-Type: application/json' -d '{{}}'"
    if method == "WS":
        return f"wscat -c ws://localhost:8000{path}"
    return f"curl -X {method} {url}"


def concept_sync_code(item) -> str:
    return DEFAULT_SYNC_EQUIVALENTS[item["cluster"]]


def concept_perf(item):
    return CLUSTER_PERF[item["cluster"]]


def build_concepts():
    concepts = []
    for item in CONCEPT_SPECS:
        data = dict(item)
        data["sample"] = SAMPLES[item["id"]]
        data["sample_lang"] = "yaml" if item["id"] == "FA59" else "python"
        data["sync_code"] = concept_sync_code(item)
        data["openapi"] = concept_openapi(item)
        data["curl"] = concept_curl(item)
        data["schema"] = SCHEMA_SNIPPETS.get(item["id"])
        data["version"] = VERSION_NOTES.get(item["id"])
        data["perf"] = concept_perf(item)
        data["endpoint"] = ENDPOINT_META.get(item["id"])
        concepts.append(data)
    concepts.sort(key=lambda value: int(value["id"][2:]))
    return concepts


CONCEPTS = build_concepts()


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


def build_examples(item):
    examples = [
        ex(
            "Minimal Working Shape",
            item["summary"],
            code=item["sample"],
            lang=item["sample_lang"],
            note=item["detail"],
        ),
    ]
    if item.get("schema"):
        examples.append(
            ex(
                "Pydantic Model | JSON Schema",
                "FastAPI leans on Pydantic models because one declaration drives validation, serialization, and OpenAPI.",
                kind="tabs",
                tabs=[
                    ("Model", "python", item["sample"]),
                    ("JSON Schema", "json", item["schema"]),
                ],
                note="The generated schema is what client tools and /docs consume.",
            )
        )
    elif item.get("endpoint"):
        examples.append(
            ex(
                "Code | Generated OpenAPI | cURL",
                "A path operation should be easy to view in source, docs, and client form without rewriting the contract three times.",
                kind="tabs",
                tabs=[
                    ("Code", item["sample_lang"], item["sample"]),
                    ("Generated OpenAPI", "json", item["openapi"]),
                    ("cURL", "bash", item["curl"]),
                ],
                note="The same declaration feeds runtime parsing and the OpenAPI output.",
            )
        )
    else:
        examples.append(
            ex(
                "Lower-level or blocking equivalent",
                "Seeing the manual or blocking shape makes the framework boundary explicit.",
                code=item["sync_code"],
                lang="python",
                note="This is the style of code FastAPI is helping you avoid or isolate.",
            )
        )
    wrong = CLUSTER_MISTAKES[item["cluster"]][0]
    examples.append(
        ex(
            "Common Mistake / Fix",
            "Most FastAPI production bugs come from boundary misuse, not from syntax.",
            kind="tabs",
            tabs=[
                ("Wrong", "python", f"# {wrong[0]}\n{item['sync_code']}"),
                ("Fix", item["sample_lang"], item["sample"]),
            ],
            note=f"{wrong[1]} Fix: {wrong[2]}",
        )
    )
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
    else:
        body.append(render_pre(example["code"], example["lang"]))
    if example.get("note"):
        body.append(f"<p><strong>What to observe:</strong> {escape(example['note'])}</p>")
    body.append("</article>")
    return "".join(body)


def render_badges(ids):
    if not ids:
        return "<span class='badge subtle'>None</span>"
    return "".join(f"<a class='badge' href='#{escape(i)}'>{escape(i)}</a>" for i in ids)


def render_comparison(item):
    raw_text, fastapi_text, other_text = CLUSTER_COMPARISON[item["cluster"]]
    return (
        "<div class='comparison-box'>"
        "<table><thead><tr>"
        "<th>Raw / Blocking</th>"
        "<th>FastAPI</th>"
        f"<th>{escape(OTHER_LABELS[item['cluster']])}</th>"
        "</tr></thead><tbody><tr>"
        f"<td>{escape(raw_text)}</td>"
        f"<td>{escape(fastapi_text)}</td>"
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


def build_dependents():
    deps = defaultdict(list)
    for item in CONCEPTS:
        for prereq in item["prereqs"]:
            deps[prereq].append(item["id"])
    return deps


def render_endpoint_card(item):
    endpoint = item.get("endpoint")
    if not endpoint:
        return ""
    method, path = endpoint
    description = item["summary"]
    badge_class = method.lower().replace("ws", "get")
    return (
        "<div class='endpoint-card'>"
        f"<span class='method-badge method-{escape(badge_class)}'>{escape(method)}</span>"
        f"<code>{escape(path)}</code>"
        f"<p>{escape(description)}</p>"
        "</div>"
    )


def render_sync_compare(item):
    sync_label, async_label = item["perf"]
    return f"""
<div class='sync-async-box'>
  <div class='sync-async-panel'>
    <div class='sync-async-head'><span>Blocking / manual shape</span><span class='perf-badge'>{escape(sync_label)}</span></div>
    {render_pre(item['sync_code'], 'python')}
  </div>
  <div class='sync-async-panel'>
    <div class='sync-async-head'><span>FastAPI / async shape</span><span class='perf-badge'>{escape(async_label)}</span></div>
    {render_pre(item['sample'], item['sample_lang'])}
  </div>
</div>
"""


def render_section(item, dependents, index):
    next_id = CONCEPTS[index + 1]["id"] if index + 1 < len(CONCEPTS) else "quick-reference"
    used_later = dependents.get(item["id"], [])
    version_html = ""
    if item.get("version"):
        version_html = f"<aside class='callout callout-pydantic'><strong>Version note:</strong> {escape(item['version'])}</aside>"
    problem = f"If the team treats {item['title'].lower()} as optional, the API boundary becomes implicit and the hard failure shows up later under load, in validation, or in operational drift."
    checks = [
        ("What failure mode is this concept preventing?", problem),
        ("What does FastAPI or Starlette actually do here?", item["detail"]),
        ("What is the main security or reliability concern?", CLUSTER_SECURITY[item["cluster"]]),
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
  {render_endpoint_card(item)}
  <div class="forward-links">
    <div><span class="meta-label">Read first</span>{render_badges(item['prereqs'])}</div>
    <div><span class="meta-label">Used in</span>{used_html}</div>
  </div>
  <h3>The Problem</h3>
  <aside class="callout callout-pitfall">{escape(problem)}</aside>
  <h3>FastAPI's Solution</h3>
  <p>{escape(item['summary'])}</p>
  <h3>Under The Hood</h3>
  <p>{escape(item['detail'])}</p>
  <aside class="callout callout-async sync-box" hidden>
    <div class="wsgi-title">Sync / lower-level equivalent</div>
    <p>This is the blocking or manual version of the same idea. It is useful for contrast, not as the default FastAPI architecture.</p>
    {render_pre(item['sync_code'], 'python')}
  </aside>
  <h3>Code Examples</h3>
  <div class="example-grid">{examples}</div>
  <h3>Sync vs Async Comparison</h3>
  {render_sync_compare(item)}
  <h3>Comparison</h3>
  {render_comparison(item)}
  <h3>Common Mistakes</h3>
  {render_mistakes(CLUSTER_MISTAKES[item['cluster']])}
  <h3>Security Implications</h3>
  <aside class="callout callout-security">{escape(CLUSTER_SECURITY[item['cluster']])}</aside>
  <h3>When Not To Use This</h3>
  <aside class="callout callout-perf">{escape(CLUSTER_WHEN_NOT[item['cluster']])}</aside>
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
    classDef foundation fill:#07253a,stroke:#00e5ff,color:#ecf0f1;
    classDef routing fill:#0b3146,stroke:#00bcd4,color:#ecf0f1;
    classDef request fill:#10384a,stroke:#2de2e6,color:#ecf0f1;
    classDef pydantic fill:#2a2c3f,stroke:#ffd166,color:#ecf0f1;
    classDef di fill:#133043,stroke:#63f5c7,color:#ecf0f1;
    classDef responses fill:#173347,stroke:#4dd0e1,color:#ecf0f1;
    classDef openapi fill:#163b4f,stroke:#80deea,color:#ecf0f1;
    classDef middleware fill:#12354e,stroke:#89ddff,color:#ecf0f1;
    classDef auth fill:#20304e,stroke:#ffa7c4,color:#ecf0f1;
    classDef database fill:#21343d,stroke:#9fe870,color:#ecf0f1;
    classDef advanced fill:#1f2949,stroke:#c792ea,color:#ecf0f1;
    classDef performance fill:#1e3444,stroke:#62f7ff,color:#ecf0f1;
    classDef testing fill:#17382f,stroke:#7fffd4,color:#ecf0f1;
    classDef deployment fill:#233244,stroke:#ff9f6e,color:#ecf0f1;
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
  <h2>FastAPI Concept DAG</h2>
  <p>The document order follows this dependency graph, so each FA identifier appears only after the concepts it depends on.</p>
  <div class='diagram-actions'><button class='diagram-action dag-download-btn' type='button' aria-label='Download FastAPI concept DAG'>Download DAG</button></div>
  <div class='er-diagram'><div class='mermaid-diagram'>{escape(render_dag())}</div></div>
  <h3>All 59 Concepts</h3>
  <div class='table-wrap'><table><thead><tr><th>ID</th><th>Concept</th><th>Layer</th><th>Prerequisites</th><th>Dependents</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
"""


def render_request_lifecycle():
    diagram = """
sequenceDiagram
    participant C as Client
    participant U as Uvicorn
    participant A as ASGI scope receive send
    participant F as FastAPI app
    participant M as Middleware
    participant D as Dependency graph
    participant P as Pydantic
    participant V as Path operation
    participant DB as Async database
    C->>U: HTTP request bytes
    U->>A: scope receive send
    A->>F: call ASGI app
    F->>M: inbound middleware chain
    M->>D: resolve dependencies
    D->>P: validate params and body
    P->>V: typed Python objects
    V->>DB: await query or command
    DB-->>V: rows or result
    V->>P: response payload
    P->>M: serialized response data
    M->>U: response status headers body
    U->>C: HTTP response bytes
"""
    return f"""
<section class='concept-section' id='request-lifecycle' data-title='FastAPI Request Lifecycle'>
  <div class='section-kicker'>Task 2 &middot; Lifecycle</div>
  <h2>FastAPI Request Lifecycle</h2>
  <p>FastAPI request handling is an ASGI pipeline: server, middleware, dependency resolution, validation, business logic, serialization, then response writing.</p>
  <div class='mermaid-wrap'><div class='mermaid-diagram'>{escape(diagram)}</div></div>
</section>
"""


def render_concurrency_timeline():
    diagram = """
gantt
    title WSGI vs ASGI for eight concurrent IO bound requests
    dateFormat X
    axisFormat %L ms
    section WSGI sync workers
    Request 1 worker 1 :a1, 0, 100
    Request 2 worker 2 :a2, 0, 100
    Request 3 worker 3 :a3, 0, 100
    Request 4 worker 4 :a4, 0, 100
    Request 5 waits then runs :a5, 100, 100
    Request 6 waits then runs :a6, 100, 100
    Request 7 waits then runs :a7, 100, 100
    Request 8 waits then runs :a8, 100, 100
    section ASGI event loop worker
    All sockets wait concurrently :b1, 0, 100
    Loop resumes each task briefly :b2, 0, 15
"""
    return f"""
<section class='concept-section' id='concurrency-timeline' data-title='WSGI vs ASGI Timeline'>
  <div class='section-kicker'>Task 2 &middot; Concurrency</div>
  <h2>WSGI vs ASGI Concurrency Timeline</h2>
  <p>This is the core mental model behind FastAPI: async wins when requests mostly wait on network or database I/O and the event loop can reuse that wait time.</p>
  <div class='mermaid-wrap'><div class='mermaid-diagram'>{escape(diagram)}</div></div>
</section>
"""


def render_pydantic_pipeline():
    diagram = """
flowchart LR
    A[raw request data] --> B[coerce primitive types]
    B --> C[field validators]
    C --> D[model validator]
    D --> E[model instance]
    E --> F[model_dump and serialization]
    F --> G[JSON Schema and OpenAPI reuse]
"""
    return f"""
<section class='concept-section' id='pydantic-pipeline' data-title='Pydantic Validation Pipeline'>
  <div class='section-kicker'>Task 2 &middot; Validation</div>
  <h2>Pydantic v2 Validation Pipeline</h2>
  <p>Pydantic does more than type checking. The same model definition powers coercion, custom validators, serialization, and schema generation.</p>
  <div class='mermaid-wrap'><div class='mermaid-diagram'>{escape(diagram)}</div></div>
</section>
"""


def render_ecosystem_map():
    cards = [
        ("Core", "Pydantic", "Typed validation, serialization, and JSON Schema generation."),
        ("Database", "SQLAlchemy", "Async relational persistence and query composition."),
        ("Database", "Alembic", "Migration history for SQLAlchemy-backed data stores."),
        ("Tasks", "Celery", "Durable background jobs, retries, and scheduled work."),
        ("Cache", "redis-py", "Async Redis clients for cache, rate limit, and pub-sub patterns."),
        ("HTTP", "httpx", "Async outbound HTTP with pooled clients and test tools."),
        ("Testing", "pytest-asyncio", "Async test execution and fixtures."),
        ("Testing", "schemathesis", "OpenAPI-driven contract and fuzz testing."),
        ("Observability", "prometheus-fastapi-instrumentator", "Metrics export for latency, throughput, and error counts."),
        ("Security", "slowapi", "Rate limiting patterns built over Starlette and FastAPI."),
        ("Auth", "fastapi-users", "Opinionated auth flows when you need more than the built-ins."),
        ("Caching", "fastapi-cache2", "Decorator-based cache integration for FastAPI endpoints."),
        ("Pagination", "fastapi-pagination", "Ready-made page and cursor pagination schemas."),
        ("Database", "Beanie", "MongoDB document models with async query support."),
    ]
    rendered = "".join(
        f"<article class='extension-card'><div class='extension-type'>{escape(cat)}</div><h3>{escape(name)}</h3><p>{escape(desc)}</p></article>"
        for cat, name, desc in cards
    )
    return f"""
<section class='concept-section' id='ecosystem-map' data-title='FastAPI Ecosystem Map'>
  <div class='section-kicker'>Task 11 &middot; Ecosystem</div>
  <h2>FastAPI Ecosystem Map</h2>
  <p>FastAPI is strongest when you pair it with the right async-safe companions rather than forcing the framework to solve every adjacent problem alone.</p>
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
  <h2>FA01-FA59 At A Glance</h2>
  <div class='table-wrap'><table><thead><tr><th>ID</th><th>Layer</th><th>Concept</th><th>One-line Summary</th></tr></thead><tbody>{rows}</tbody></table></div>
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
<link href='https://fonts.googleapis.com/css2?family=Karla:wght@400;500;700;800&family=Playfair+Display:wght@600;700;800&family=Space+Mono:wght@400;700&display=swap' rel='stylesheet'>
<link id='darkThemeStylesheet' rel='stylesheet' href='styles-dark.css'>
<link id='lightThemeStylesheet' rel='stylesheet' href='styles-light.css' media='not all'>
<link rel='preload' href='styles.css' as='style'>
<link rel='stylesheet' href='styles.css'>
<style>
html[data-theme='dark'] {{ --void:#040d21; --obsidian:#051127; --deep:#08162f; --surface:#0c1b35; --surface2:#102241; --surface3:#173153; --violet:#00bcd4; --violet-dim:#0d6b77; --gold:#ffd166; --text-1:#ecf0f1; --text-2:#b8c7d1; --font-head:'Playfair Display',serif; --font-body:'Karla',sans-serif; --font-code:'Space Mono',monospace; }}
html[data-theme='light'] {{ --paper:#f5fbfc; --paper2:#edf6f7; --surface:#fcffff; --surface2:#f1f7f8; --surface3:#e4eef0; --forest:#0c3142; --terra:#009688; --font-head:'Playfair Display',serif; --font-body:'Karla',sans-serif; --font-code:'Space Mono',monospace; }}
.diagram-actions{{display:flex;justify-content:flex-end;margin:.85rem 0 1rem}} .diagram-action,.aux-toggle{{appearance:none;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);color:inherit;padding:.6rem .9rem;border-radius:10px;cursor:pointer;font-family:var(--font-code);font-size:.76rem}} html[data-theme='light'] .diagram-action,html[data-theme='light'] .aux-toggle{{border-color:rgba(12,49,66,.16);background:rgba(12,49,66,.04)}}
.sidebar-nav .group-links a{{display:grid;grid-template-columns:auto 1fr;gap:.6rem;align-items:start}} .nav-dot{{display:inline-flex;align-items:center;justify-content:center;min-width:1.5rem;height:1.5rem;border-radius:999px;font-size:.68rem;font-family:var(--font-code);border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04)}} html[data-theme='light'] .nav-dot{{border-color:rgba(12,49,66,.18);background:rgba(12,49,66,.06)}}
.hero-grid{{display:grid;grid-template-columns:1.3fr .9fr;gap:1.2rem;align-items:start}} .hero-card,.comparison-box,.example-card,.gotcha-box,.mermaid-wrap,.er-diagram,.extension-card,.endpoint-card,.sync-async-panel{{border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:1rem;background:rgba(255,255,255,.02)}} html[data-theme='light'] .hero-card,html[data-theme='light'] .comparison-box,html[data-theme='light'] .example-card,html[data-theme='light'] .gotcha-box,html[data-theme='light'] .mermaid-wrap,html[data-theme='light'] .er-diagram,html[data-theme='light'] .extension-card,html[data-theme='light'] .endpoint-card,html[data-theme='light'] .sync-async-panel{{border-color:rgba(12,49,66,.12);background:rgba(255,255,255,.74)}}
.lead{{font-size:1.04rem}} .section-meta,.forward-links{{display:flex;flex-wrap:wrap;gap:.7rem 1rem;align-items:center;margin:.75rem 0 1rem}} .forward-links>div{{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}}
.cluster-pill{{display:inline-flex;align-items:center;border-radius:999px;padding:.2rem .6rem;font-family:var(--font-code);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em}}
.cluster-foundation{{background:rgba(0,229,255,.14);color:#d9fdff}} .cluster-routing{{background:rgba(0,188,212,.14);color:#dffcff}} .cluster-request{{background:rgba(45,226,230,.14);color:#dfffff}} .cluster-pydantic{{background:rgba(255,209,102,.14);color:#fff1bf}} .cluster-di{{background:rgba(99,245,199,.14);color:#d9fff1}} .cluster-responses{{background:rgba(77,208,225,.14);color:#ddfbff}} .cluster-openapi{{background:rgba(128,222,234,.14);color:#e6fbff}} .cluster-middleware{{background:rgba(137,221,255,.14);color:#e5f9ff}} .cluster-auth{{background:rgba(255,167,196,.14);color:#ffe3ef}} .cluster-database{{background:rgba(159,232,112,.14);color:#efffd7}} .cluster-advanced{{background:rgba(199,146,234,.14);color:#f4e7ff}} .cluster-performance{{background:rgba(98,247,255,.14);color:#e0feff}} .cluster-testing{{background:rgba(127,255,212,.14);color:#ddfff0}} .cluster-deployment{{background:rgba(255,159,110,.14);color:#ffe4d4}} html[data-theme='light'] .cluster-pill{{color:var(--forest)}}
.callout-async{{border-left:4px solid #00e5ff;background:rgba(0,229,255,.08)}} .callout-pydantic{{border-left:4px solid #ffd166;background:rgba(255,209,102,.08)}} .callout-perf{{border-left:4px solid #63f5c7;background:rgba(99,245,199,.08)}} .callout-security{{border-left:4px solid #ff8a65;background:rgba(255,138,101,.1)}} .callout-pitfall{{border-left:4px solid #ff6b6b;background:rgba(255,107,107,.1)}} .wsgi-title{{font-family:var(--font-code);font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.35rem}}
.tab-buttons{{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.8rem}} .tab-btn{{appearance:none;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);color:inherit;border-radius:999px;padding:.45rem .7rem;cursor:pointer;font:600 .74rem var(--font-code)}} .tab-btn.is-active{{background:rgba(0,229,255,.14);border-color:rgba(0,229,255,.34)}} html[data-theme='light'] .tab-btn{{border-color:rgba(12,49,66,.15);background:rgba(12,49,66,.04)}} html[data-theme='light'] .tab-btn.is-active{{background:rgba(0,188,212,.1);border-color:rgba(0,188,212,.24)}} .tab-panel{{display:none}} .tab-panel.is-active{{display:block}}
.mistake-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}} .extension-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}} .extension-type{{font-family:var(--font-code);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:#00e5ff}}
.sidebar-aux{{display:grid;gap:.55rem;margin-top:.75rem}} .aux-toggle.is-active{{background:rgba(0,229,255,.14);border-color:rgba(0,229,255,.34)}} html[data-theme='light'] .aux-toggle.is-active{{background:rgba(0,188,212,.1);border-color:rgba(0,188,212,.24)}}
.layer-skeleton{{height:320px;border-radius:14px;background:linear-gradient(90deg,rgba(255,255,255,.03) 25%,rgba(255,255,255,.07) 50%,rgba(255,255,255,.03) 75%);background-size:200% 100%;animation:skeleton-sweep 1.4s ease infinite;border:1px solid rgba(255,255,255,.06);margin-bottom:1.4rem}} @keyframes skeleton-sweep{{0%{{background-position:200% 0}}100%{{background-position:-200% 0}}}}
.sync-async-box{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}} .sync-async-head{{display:flex;justify-content:space-between;gap:.75rem;align-items:center;font-family:var(--font-code);font-size:.76rem;margin-bottom:.7rem;text-transform:uppercase;letter-spacing:.08em}} .perf-badge{{display:inline-flex;align-items:center;border-radius:999px;padding:.2rem .5rem;background:rgba(0,229,255,.12);color:#aefaff;border:1px solid rgba(0,229,255,.24)}} html[data-theme='light'] .perf-badge{{color:#0c3142}}
.endpoint-card{{display:grid;gap:.45rem;margin:1rem 0}} .method-badge{{display:inline-flex;align-items:center;justify-content:center;min-width:3.2rem;border-radius:999px;padding:.2rem .6rem;font-family:var(--font-code);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;background:rgba(255,255,255,.07)}} .method-get{{color:#8df7ff}} .method-post{{color:#ffe7a8}} .method-put{{color:#d1ffc1}} .method-patch{{color:#ffcfe0}} .method-delete{{color:#ffb8b8}}
@media (max-width:1100px){{.hero-grid,.extension-grid,.sync-async-box{{grid-template-columns:1fr}}}} @media (max-width:900px){{.mistake-grid{{grid-template-columns:1fr}}}}
</style>
<!-- REVIEW: Keep this inline theme bootstrap in <head>; moving it to the end of <body> would cause the wrong theme to flash before styles apply. -->
<script>
try {{
  const savedTheme = localStorage.getItem('fastapi-reference-theme');
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
      <button class='aux-toggle' id='syncToggle' type='button' aria-pressed='false'>Show sync equivalents</button>
    </div>
  </div>
  <nav class='sidebar-nav' aria-label='FastAPI concept navigation'>{render_nav()}</nav>
</aside>
<main>
<!-- TASK-1 START -->
<section class='hero' id='top'>
  <div class='section-kicker'>FastAPI Complete Reference</div>
  <div class='hero-grid'>
    <div>
      <h1>{SUBTITLE}</h1>
      <p>This document assumes Python basics only. It builds the missing web stack from the bottom: WSGI vs ASGI, asyncio, Starlette internals, typed request boundaries, Pydantic models, dependency injection, authentication, async databases, WebSockets, testing, and deployment.</p>
      <p>The running domain is an e-commerce API with <code>User</code>, <code>Product</code>, <code>Order</code>, and <code>OrderItem</code>. The same model surface appears in schemas, routes, auth checks, persistence, live updates, and tests so the examples stay coherent.</p>
    </div>
    <div class='hero-card'>
      <h3>Baseline Core Packages</h3>
      {render_pre(FASTAPI_CORE_REQUIREMENTS, "text")}
    </div>
  </div>
</section>
<!-- TASK-1 END -->
<div id='sectionMount' hidden aria-hidden='true'></div>
<!-- TASK-2 START -->
{render_dependency_table(dependents)}
{render_request_lifecycle()}
{render_concurrency_timeline()}
{render_pydantic_pipeline()}
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
  const syncToggle = document.getElementById('syncToggle');
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
  const THEME_STORAGE_KEY = 'fastapi-reference-theme';
  let currentTheme = window.__initialTheme === 'light' ? 'light' : 'dark';
  let currentSectionId = virtualSections[0]?.id || orderedIds[0] || '';
  let activeObserver = null;
  let renderToken = 0;
  let mermaidRenderToken = 0;
  let syncVisible = false;
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
    const blocks = [...root.querySelectorAll('.mermaid-diagram')];
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
    const svg = section.querySelector('.mermaid-diagram svg');
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
    link.download = 'fastapi-concept-dag.svg';
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
  function applySyncState(root = document) {
    root.querySelectorAll('.sync-box').forEach((box) => {
      box.hidden = !syncVisible;
    });
    if (syncToggle) {
      syncToggle.classList.toggle('is-active', syncVisible);
      syncToggle.setAttribute('aria-pressed', String(syncVisible));
      syncToggle.textContent = syncVisible ? 'Hide sync equivalents' : 'Show sync equivalents';
    }
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
    applySyncState(section);
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
  applySyncState(document);
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
  syncToggle?.addEventListener('click', () => {
    syncVisible = !syncVisible;
    applySyncState(document);
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
        "FA05": "<!-- TASK-3 END -->\n<!-- TASK-4 START -->",
        "FA12": "<!-- TASK-4 END -->\n<!-- TASK-5 START -->",
        "FA19": "<!-- TASK-5 END -->\n<!-- TASK-6 START -->",
        "FA24": "<!-- TASK-6 END -->\n<!-- TASK-7 START -->",
        "FA33": "<!-- TASK-7 END -->\n<!-- TASK-8 START -->",
        "FA42": "<!-- TASK-8 END -->\n<!-- TASK-9 START -->",
        "FA48": "<!-- TASK-9 END -->\n<!-- TASK-10 START -->",
        "FA59": "<!-- TASK-10 END -->",
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
