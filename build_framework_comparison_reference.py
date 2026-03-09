from __future__ import annotations

from collections import defaultdict
from html import escape
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
OUTFILE = ROOT / "framework_comparison_reference.html"

TITLE = "Django vs Flask vs FastAPI - Complete Comparison Reference"
SUBTITLE = "A decision-focused engineering reference for choosing Django, Flask, or FastAPI with evidence, trade-offs, and migration costs"
VERSION_BASELINE = """Django 4.2 LTS
Flask 3.x
FastAPI 0.110+
Pydantic v2"""

FRAMEWORKS = ("django", "flask", "fastapi")
FRAMEWORK_LABELS = {
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
}

MODE_LABELS = {
    "all": "All",
    "api": "APIs",
    "full-stack": "Full-stack",
    "ml": "ML",
}

LAYER_NAMES = {
    0: "Philosophy, Origins & Spectrum",
    1: "Architecture & Structure",
    2: "Data Layer",
    3: "API Development",
    4: "Authentication & Security",
    5: "Performance",
    6: "Developer Experience",
    7: "Async & Concurrency",
    8: "Ecosystem & Integration",
    9: "Operations & Deployment",
    10: "Decision Framework",
}

NAV_LABELS = {
    0: "Layer 0: Philosophy, Origins & Spectrum",
    1: "Layer 1: Architecture & Structure",
    2: "Layer 2: Data Layer",
    3: "Layer 3: API Development",
    4: "Layer 4: Authentication & Security",
    5: "Layer 5: Performance",
    6: "Layer 6: Developer Experience",
    7: "Layer 7: Async & Concurrency",
    8: "Layer 8: Ecosystem & Integration",
    9: "Layer 9: Operations & Deployment",
    10: "Layer 10: Decision Framework",
}

REFERENCE_SECTIONS = [
    ("dependency-table", "Comparison DAG & Dependency Table"),
    ("decision-tree", "Decision Tree"),
    ("request-sequence", "Same Request in All 3"),
    ("ecosystem-diagram", "Framework Ecosystem"),
    ("project-matrix", "Project Type Matrix"),
    ("master-summary", "The One-Paragraph Answer"),
    ("score-cards", "Framework Score Cards"),
    ("interview-questions", "Interview Questions"),
    ("quick-reference", "Quick Reference"),
    ("recommended-reading", "Recommended Reading"),
]

CLUSTER_CLASS = {
    "architecture": "cluster-architecture",
    "performance": "cluster-performance",
    "data": "cluster-data",
    "auth": "cluster-auth",
    "async": "cluster-async",
    "testing": "cluster-testing",
    "dx": "cluster-dx",
    "ops": "cluster-ops",
    "decision": "cluster-decision",
}

VERDICT_CLASS = {
    "django": "winner-django",
    "flask": "winner-flask",
    "fastapi": "winner-fastapi",
    "tie": "winner-tie",
    "conditional": "winner-conditional",
}


def sec(
    id,
    layer,
    cluster,
    title,
    prereqs,
    summary,
    dimension,
    django,
    flask,
    fastapi,
    code_django,
    code_flask,
    code_fastapi,
    tradeoff,
    evidence,
    verdict,
    verdict_text,
    dissent,
    *,
    frameworks=("django", "flask", "fastapi"),
    modes=("api", "full-stack"),
):
    return {
        "id": id,
        "layer": layer,
        "cluster": cluster,
        "title": title,
        "prereqs": prereqs,
        "summary": summary,
        "dimension": dimension,
        "django": django,
        "flask": flask,
        "fastapi": fastapi,
        "code_django": code_django,
        "code_flask": code_flask,
        "code_fastapi": code_fastapi,
        "tradeoff": tradeoff,
        "evidence": evidence,
        "verdict": verdict,
        "verdict_text": verdict_text,
        "dissent": dissent,
        "frameworks": frameworks,
        "modes": modes,
    }


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


def render_tabs(section_id, tabs):
    buttons = []
    panels = []
    for index, (label, framework, lang, code) in enumerate(tabs):
        active = " is-active" if index == 0 else ""
        panel_id = f"{section_id}-tab-{index}"
        buttons.append(
            f"<button class='tab-btn framework-{escape(framework)}{active}' type='button' data-panel='{panel_id}' aria-pressed='{'true' if index == 0 else 'false'}'>{escape(label)}</button>"
        )
        panels.append(
            "<div class='tab-panel{active}' id='{panel_id}'>"
            "<div class='framework-code-label framework-{framework}'>{label}</div>"
            "{code}"
            "</div>".format(
                active=active,
                panel_id=panel_id,
                framework=escape(framework),
                label=escape(label),
                code=render_pre(code, lang),
            )
        )
    return f"<div class='tabbed-code'><div class='tab-buttons'>{''.join(buttons)}</div><div class='tab-panels'>{''.join(panels)}</div></div>"


def framework_badge(name: str) -> str:
    return f"<span class='framework-badge framework-{escape(name)}'>{escape(FRAMEWORK_LABELS[name])}</span>"


def verdict_badge(verdict: str) -> str:
    label = {
        "django": "Winner: Django",
        "flask": "Winner: Flask",
        "fastapi": "Winner: FastAPI",
        "tie": "Tie",
        "conditional": "Conditional",
    }[verdict]
    return f"<span class='winner-badge {VERDICT_CLASS[verdict]}'>{escape(label)}</span>"


SECTIONS = [
    sec(
        "CM01",
        0,
        "architecture",
        "Framework Lineage & Philosophy",
        [],
        "Origins matter because each framework still optimizes for the problem that created it: Django for full-stack publishing systems, Flask for minimal surface area, FastAPI for typed async APIs.",
        "This dimension compares why the frameworks were born, because those origins still explain their defaults, extension stories, and failure modes in 2026.",
        "Django came out of a newspaper CMS, so admin, content management, auth, and batteries are native rather than bolted on. The result is heavy, opinionated, and extremely productive for business software.",
        "Flask began as the smallest useful WSGI layer and stayed that way. Its philosophy is not 'Django but smaller'; it is 'give the engineer the fewest rules possible.'",
        "FastAPI arrived when ASGI, asyncio, OpenAPI, and typed validation were finally mature enough to converge. Its philosophy is API contracts first, especially for I/O-bound systems.",
        """# Django's origin still shows in defaults
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
]
""",
        """from flask import Flask

app = Flask(__name__)  # core surface stays intentionally tiny
""",
        """from fastapi import FastAPI

app = FastAPI(title="Typed API first")
""",
        "Django optimizes for shipping complete products quickly, Flask optimizes for engineering freedom, and FastAPI optimizes for typed APIs and async throughput. Those are incompatible priorities, which is why the frameworks feel so different under pressure.",
        "Dates and lineage are objective: Django 2005, Flask 2010, FastAPI 2018. The code surface also proves the point: Django starts with subsystems loaded, Flask with almost none, FastAPI with request validation and docs built into the entry point.",
        "conditional",
        "Use this as a framing section, not as a winner-takes-all decision. Origins explain defaults; they do not override project fit.",
        "A senior engineer may still pick Flask or FastAPI for a CMS-adjacent project if the system is really an API platform with only thin admin needs.",
        frameworks=("django", "flask", "fastapi"),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM02",
        0,
        "architecture",
        "What Each Framework Actually Is",
        [],
        "Django is a platform, Flask is a microframework, and FastAPI is an API framework; treating them as interchangeable is the first framework-selection mistake.",
        "This compares the actual product surface each framework gives you on day one, because package count and integration burden are hidden project costs.",
        "Django ships ORM, migrations, admin, auth, templates, forms, CSRF, sessions, email, and caching hooks. That means a SaaS back office is one installation away from moving.",
        "Flask gives routing, request and response objects, Jinja templates, and not much else. Almost every business feature becomes a dependency decision.",
        "FastAPI gives routing, validation, dependency injection, response modeling, and OpenAPI generation. It is maximal for APIs and minimal for everything around them.",
        """# Django SaaS baseline
python -m pip install django psycopg[binary]
django-admin startproject config
""",
        """# Flask SaaS baseline
python -m pip install flask flask-sqlalchemy flask-login flask-migrate flask-wtf
""",
        """# FastAPI SaaS baseline
python -m pip install fastapi uvicorn sqlalchemy[asyncio] alembic pydantic-settings python-jose
""",
        "Django's hidden cost is framework weight and conventions. Flask's hidden cost is integration work. FastAPI's hidden cost is that non-API features remain your problem.",
        "A realistic SaaS with auth, admin, REST API, migrations, and background tasks usually needs two core packages in Django, five to seven in Flask, and five to eight in FastAPI. That is real maintenance surface, not abstract philosophy.",
        "django",
        "For a mixed product with admin, auth, and business CRUD, Django wins because it deletes whole categories of setup work.",
        "A senior engineer may still choose FastAPI if the business value lives almost entirely in the API and the admin surface can remain separate or thin.",
        frameworks=("django",),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM03",
        0,
        "architecture",
        "The Batteries Included Spectrum",
        [],
        "Django sits at the far end of the batteries-included spectrum, Flask at the minimal end, and FastAPI is maximal only for API concerns.",
        "This dimension matters because built-in capability directly changes time to market, integration risk, and how many decisions a team must get right early.",
        "Django's defaults cover the typical needs of internal tools, B2B platforms, editorial sites, and enterprise back offices. The price is more framework to learn and more conventions to accept.",
        "Flask keeps the center empty on purpose. That is freedom for senior engineers and a trap for teams that mistake fewer defaults for lower long-term complexity.",
        "FastAPI is an interesting middle case: it includes much more than Flask for APIs, but almost nothing for CMS, admin, forms-based HTML, or session-heavy browser apps.",
        """FEATURES = {
    "orm": True, "admin": True, "auth": True, "templates": True,
    "forms": True, "csrf": True, "sessions": True, "migrations": True,
}
""",
        """FEATURES = {
    "orm": False, "admin": False, "auth": False, "templates": True,
    "forms": False, "csrf": False, "sessions": True,
}
""",
        """FEATURES = {
    "orm": False, "admin": False, "auth_utilities": True, "openapi": True,
    "pydantic": True, "templates": False, "sessions": False,
}
""",
        "The winning framework depends on whether your missing features are product requirements or optional add-ons. The more business features you already know you need, the more Django's opinionated bulk becomes an advantage.",
        "The feature matrix is objective. Django ships the most built-ins, Flask the fewest, FastAPI the most API-specific value. That is why FastAPI is not a clean drop-in substitute for Django outside API-centric systems.",
        "conditional",
        "Django wins the full-stack end of the spectrum, FastAPI wins the API-only interpretation, and Flask wins only if the team truly wants to assemble the stack itself.",
        "A senior Flask team may prefer Flask here because the absence of batteries avoids deleting or working around features they never wanted in the first place.",
        frameworks=("django", "fastapi"),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM04",
        1,
        "architecture",
        "Request/Response Architecture Comparison",
        ["CM01", "CM02", "CM03"],
        "The request path tells you where hidden work, latency, and framework magic live before your code runs.",
        "This compares the lifecycle of the same POST /users request with validation and persistence, because framework overhead is about architecture, not just raw benchmarks.",
        "Django routes through middleware, URLconf, view dispatch, forms or serializers, ORM, and response middleware. That is a lot of machinery, but it also means common concerns already have a home.",
        "Flask goes through Werkzeug routing and request context, then whatever extensions you wired in. The path is shorter, but the missing layers become your integration responsibility.",
        "FastAPI resolves dependencies, validates through Pydantic, and serializes the response through the declared model, all inside an ASGI-native path. The pipeline is explicit once you understand Depends.",
        """# Django view + serializer path
class UserCreate(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=201)
""",
        """# Flask + marshmallow path
@bp.post("/users")
def create_user():
    payload = UserSchema().load(request.get_json())
    user = User(**payload)
    db.session.add(user)
    db.session.commit()
    return UserSchema().dump(user), 201
""",
        """# FastAPI path
@router.post("/users", response_model=UserPublic, status_code=201)
async def create_user(payload: UserCreate, session: AsyncSession = Depends(get_db)):
    user = User(**payload.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
""",
        "Django does the most before your code but gives the most integration points. Flask does the least but makes architecture a team discipline problem. FastAPI sits in the middle with a narrower, API-centric path.",
        "The same endpoint is typically shortest in FastAPI for typed APIs, medium in Flask with schemas, and longest in Django REST Framework. The length is not accidental: DRF buys ecosystem maturity and policy hooks, not terseness.",
        "fastapi",
        "For API-centric request pipelines, FastAPI wins because validation, dependency resolution, and serialization stay in one coherent path without the DRF ceremony.",
        "A senior engineer may still choose Django here if policy hooks, permissions, throttling, and browsable admin-like API ergonomics are worth the extra machinery.",
        frameworks=("fastapi", "django"),
        modes=("api",),
    ),
    sec(
        "CM05",
        1,
        "architecture",
        "URL Routing Comparison",
        ["CM04"],
        "All three frameworks route cleanly, but Django emphasizes URL configuration modules, Flask emphasizes decorators plus blueprints, and FastAPI emphasizes typed path operations plus routers.",
        "Routing style matters because it affects modularity, reverse resolution, route conflicts, and how much metadata the framework can derive from the declaration itself.",
        "Django's URLconf keeps routing explicit and centralized. Large teams benefit because app boundaries and includes are visible in one place rather than scattered across files.",
        "Flask routing is easy to read when the codebase is small. Without blueprint discipline it becomes harder to understand the full URL surface of a large system.",
        "FastAPI gets the best ergonomics for APIs because the route decorator, type annotations, and docs metadata all live together in the handler declaration.",
        """# Django
urlpatterns = [
    path("users/<int:user_id>/", views.user_detail, name="user-detail"),
]
""",
        """# Flask
@bp.get("/users/<int:user_id>")
def user_detail(user_id: int):
    return {"user_id": user_id}
""",
        """# FastAPI
@router.get("/users/{user_id}")
async def user_detail(user_id: int):
    return {"user_id": user_id}
""",
        "Django optimizes for route inventory control, Flask for minimalism, and FastAPI for API readability plus schema generation. The more routing metadata matters, the more FastAPI pulls ahead for APIs.",
        "Line counts are close for simple handlers, but route metadata grows much more cleanly in FastAPI because path, query, and response contract stay adjacent instead of split across routing plus serializer declarations.",
        "conditional",
        "FastAPI wins for API routing ergonomics, Django wins for large multi-app full-stack projects, and Flask is acceptable when the route surface stays intentionally small.",
        "A senior Flask engineer may still prefer Flask here because decorators inside blueprints keep business behavior close to route code and avoid a separate URLconf layer.",
        frameworks=("fastapi", "django", "flask"),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM06",
        1,
        "architecture",
        "Configuration & Project Structure",
        ["CM04"],
        "Config style becomes an operational concern once environments, secrets, and deployment overrides appear.",
        "This compares how each framework loads a secret key, database URL, and debug flag because environment handling quality shows up in every deploy pipeline.",
        "Django typically starts with a monolithic settings.py and improves only if the team deliberately splits it. It is workable but ages badly in larger deployments.",
        "Flask's config object and init_app pattern are flexible, but that flexibility means every team invents its own conventions for structure and secret loading.",
        "FastAPI with Pydantic settings is the cleanest modern approach: config is typed, environment-driven, testable, and explicit without much boilerplate.",
        """import os

SECRET_KEY = os.environ["SECRET_KEY"]
DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", "NAME": os.environ["DB_NAME"]}}
DEBUG = False
""",
        """import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    DEBUG = False
""",
        """from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    database_url: str
    debug: bool = False
""",
        "Django's weakness is settings sprawl, Flask's weakness is convention drift, and FastAPI's strength is that typed settings are both cleaner and harder to misconfigure accidentally.",
        "Typed config is an evidence-based advantage: it fails fast on bad values and gives IDE and test support. This is where FastAPI's modern Python foundation is clearly ahead of Django and Flask defaults.",
        "fastapi",
        "FastAPI wins this comparison because Pydantic settings provide the most reliable and maintainable production configuration story of the three.",
        "A senior Django team may still prefer Django's familiar settings module if the rest of the platform benefits outweigh the less elegant config story.",
        frameworks=("fastapi",),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM07",
        1,
        "architecture",
        "Application Architecture Scalability",
        ["CM04", "CM05", "CM06"],
        "The real test of framework structure is not the first ten routes; it is what the codebase looks like at fifty routes, five developers, and three bounded contexts.",
        "This compares how a growing codebase stays organized, because large applications fail from import tangles and unclear boundaries more often than from raw framework performance.",
        "Django's app pattern is a genuine scaling tool. It nudges teams toward bounded contexts with their own models, views, templates, and admin integration.",
        "Flask can scale, but only if the team imposes architecture through blueprints, services, repositories, and extension wiring. Flask does not protect you from spaghetti.",
        "FastAPI routers keep API modules clean, but outside routing there is little architectural enforcement. That is powerful, but it still depends on disciplined engineers.",
        """# Django app structure
users/
  models.py
  views.py
  urls.py
  admin.py
""",
        """# Flask blueprint structure
users/
  routes.py
  schemas.py
  services.py
  models.py
""",
        """# FastAPI router structure
users/
  router.py
  schemas.py
  service.py
  repository.py
""",
        "Django gives the strongest default guardrails, Flask the weakest, and FastAPI a clean but unenforced middle ground. Architecture quality in Flask and FastAPI is far more team-dependent.",
        "Teams that hit the Flask trap usually do not fail because Flask is incapable; they fail because nothing stopped route files from becoming god modules. Django's opinionated app structure prevents that class of drift earlier.",
        "django",
        "For large, long-lived, many-developer applications, Django wins because the framework enforces the most durable default structure.",
        "A senior FastAPI team may still prefer FastAPI here if the system is API-only and they already have strong service-layer and module conventions.",
        frameworks=("django", "fastapi"),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM08",
        2,
        "data",
        "ORM Comparison",
        ["CM04"],
        "ORM choice matters more than framework brand once queries become complex, reporting-heavy, or performance-sensitive.",
        "This dimension compares Django ORM, SQLAlchemy ORM, and SQLAlchemy Core using the same analytics-flavored business query.",
        "Django ORM is excellent for ordinary CRUD and relationship traversal, especially because it is integrated with admin, forms, and migrations. The trade-off is reduced expressiveness for the nastier end of SQL.",
        "Flask typically uses SQLAlchemy, so it inherits the power and complexity of SQLAlchemy rather than owning a distinct ORM story. That is both a strength and a setup cost.",
        "FastAPI also typically rides on SQLAlchemy for relational data, so its ORM story is really a story about whether your team wants Django integration or SQLAlchemy power.",
        """from django.db.models import Count, Sum

top_users = (
    User.objects.filter(is_banned=False, orders__created_at__gte=cutoff)
    .annotate(total_value=Sum("orders__total"), recent_items=Count("orders__items"))
    .filter(total_value__gt=100)
    .order_by("-total_value")[:10]
)
""",
        """from sqlalchemy import func, select

stmt = (
    select(User, func.sum(Order.total).label("total_value"))
    .join(Order)
    .where(User.is_banned.is_(False), Order.created_at >= cutoff)
    .group_by(User.id)
)
""",
        """from sqlalchemy import func, select

stmt = (
    select(User, func.sum(Order.total).label("total_value"))
    .join(Order)
    .where(User.is_banned.is_(False), Order.created_at >= cutoff)
    .group_by(User.id)
)
""",
        "Django ORM is faster to learn and nicer for integrated product work. SQLAlchemy is more expressive, especially when you need Core, vendor-specific SQL, or async-native control.",
        "The evidence here is ergonomic, not just benchmark-based. Teams hit the ceiling of Django ORM when advanced SQL shapes appear. Teams hit the ceiling of SQLAlchemy when onboarding junior developers who just need CRUD and an admin.",
        "conditional",
        "Django wins for integrated business CRUD. SQLAlchemy wins for expressive power, async support, and framework portability.",
        "A senior Django team may still choose Django ORM for ninety percent CRUD workloads because the integrated developer experience beats theoretical query elegance.",
        frameworks=("django", "fastapi", "flask"),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM09",
        2,
        "data",
        "Migrations Comparison",
        ["CM08"],
        "Schema change tooling is one of the biggest hidden productivity multipliers in a framework stack.",
        "This compares renaming a column, adding an index, and handling concurrent developer changes, because migration tooling quality determines whether schema evolution feels safe or fragile.",
        "Django migrations are still the best integrated Python migration experience. Autogeneration, data migrations, dependency tracking, and team conflict handling are good enough for most business systems.",
        "Flask with Alembic is powerful but less magical. You get more control and more manual responsibility, especially around env.py, script organization, and rename semantics.",
        "FastAPI inherits the same Alembic story as Flask when paired with SQLAlchemy. FastAPI itself adds nothing special here.",
        """python manage.py makemigrations
python manage.py migrate
# optional: python manage.py makemigrations --merge
""",
        """flask db migrate -m "rename sku to external_sku"
flask db upgrade
""",
        """alembic revision --autogenerate -m "add product index"
alembic upgrade head
""",
        "Django optimizes for developer throughput, Alembic for explicit control. The more the team wants framework help, the more Django wins this category.",
        "In real teams, Django's migration graph and data migration support save hours every month. Alembic is completely viable, but it asks for more expertise and review discipline on every non-trivial change.",
        "django",
        "Django wins because migrations are integrated, ergonomic, and harder to misuse for the common cases that dominate business applications.",
        "A senior SQLAlchemy team may still choose Alembic because the migration layer then stays consistent across Flask, FastAPI, and even non-web services.",
        frameworks=("django",),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM10",
        2,
        "data",
        "Admin Interface",
        ["CM08"],
        "Admin surfaces are either a force multiplier or an ongoing tax depending on whether the framework gives you one.",
        "This compares how much work it takes to get a usable CRUD admin for a Product model, because internal tooling is often a large fraction of real product development.",
        "Django admin is unmatched for time-to-value. Register a model, tweak a ModelAdmin, and the business already has search, filters, forms, and permissions.",
        "Flask-Admin is capable, but it is still a separate dependency that must be configured model by model. That is fine, but it is not free.",
        "FastAPI has no native admin story. You either add SQLAdmin or build a separate admin interface, which is a meaningful product cost if internal tools matter.",
        """from django.contrib import admin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "is_active")
""",
        """from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Product, db.session))
""",
        """@router.get("/admin/products")
async def admin_products(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Product))
    return result.scalars().all()
""",
        "Django buys speed and governance immediately. Flask buys flexibility with moderate setup. FastAPI buys nothing here unless you consciously add another admin technology.",
        "If even twenty to thirty percent of team time is spent in back-office CRUD, Django admin usually repays the entire framework choice quickly. That is a business outcome, not just a developer convenience.",
        "django",
        "Django wins decisively. If admin matters, it is often the end of the framework debate.",
        "A senior engineer may still reject Django admin if the internal workflow is highly custom and a generated CRUD surface would be discarded anyway.",
        frameworks=("django",),
        modes=("full-stack",),
    ),
    sec(
        "CM11",
        3,
        "architecture",
        "REST API Development Comparison",
        ["CM04", "CM08"],
        "API development is where Django, Flask, and FastAPI are compared most often, so this dimension has to separate maturity, verbosity, and performance honestly.",
        "This builds the same protected user CRUD API in DRF, Flask-Smorest, and FastAPI to compare code volume, dependency surface, docs quality, and validation behavior.",
        "Django REST Framework is still the most mature and policy-rich API toolkit in Python. It is also the most verbose for small endpoints.",
        "Flask-Smorest keeps the API stack light and understandable, but the team still decides more of the architecture and validation story manually than in DRF or FastAPI.",
        "FastAPI is usually the shortest path to a high-quality typed API with accurate docs. Its weakness is everything surrounding the API rather than the API layer itself.",
        """class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
""",
        """@blp.route("/users")
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return User.query.all()
""",
        """@router.get("/users", response_model=list[UserPublic])
async def list_users(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User))
    return result.scalars().all()
""",
        "DRF wins on completeness, Flask on minimalism, and FastAPI on clarity plus contract generation. The right answer depends on whether the API is one feature or the product itself.",
        "Common code-count comparisons put simple CRUD lowest in FastAPI, middle in Flask-Smorest, highest in DRF. But DRF usually repays some verbosity with stronger permissions, throttling, pagination, and ecosystem maturity.",
        "fastapi",
        "For greenfield typed APIs, FastAPI wins because it minimizes glue while keeping docs and validation synchronized with code.",
        "A senior team may still choose DRF if the API is part of a larger Django platform and shared auth, admin, and governance matter more than terseness.",
        frameworks=("fastapi", "django"),
        modes=("api",),
    ),
    sec(
        "CM12",
        3,
        "architecture",
        "Input Validation & Serialization",
        ["CM11"],
        "Validation strategy affects reuse, error quality, and whether the same business rules get reimplemented at multiple layers.",
        "This compares DRF serializers, Marshmallow schemas, and Pydantic models on the same invalid user payload.",
        "DRF serializers are explicit and powerful, but they are a separate validation layer rather than the core type system of the application.",
        "Marshmallow in Flask is similarly explicit and flexible. The cost is another schema layer that still needs to stay aligned with models and API docs.",
        "Pydantic makes validation type-driven. The same model can validate input in the HTTP layer, the service layer, and tests without rewriting the rules.",
        """class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    age = serializers.IntegerField(min_value=18)
""",
        """class UserSchema(Schema):
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=18))
""",
        """class UserCreate(BaseModel):
    email: EmailStr
    age: int = Field(ge=18)
""",
        "DRF and Marshmallow are explicit schema tools. Pydantic is closer to a shared type system. That is why FastAPI validation often feels more reusable and less repetitive.",
        "Pydantic v2 error messages are currently the clearest default validation errors in the Python web ecosystem. That matters for client teams and for debugging, not just for developer aesthetics.",
        "fastapi",
        "FastAPI wins because Pydantic turns type definitions into reusable validation contracts across HTTP, services, and tests.",
        "A senior DRF team may still prefer serializers when they want maximum explicit control over read and write behavior tightly coupled to Django models and permissions.",
        frameworks=("fastapi",),
        modes=("api", "ml"),
    ),
    sec(
        "CM13",
        3,
        "async",
        "WebSocket Support",
        ["CM11"],
        "Real-time features expose the real async story of each framework more honestly than CRUD endpoints do.",
        "This compares a minimal chat setup because WebSockets immediately reveal whether async and connection management are first-class or bolt-on concerns.",
        "Django relies on Channels for serious WebSocket work. That adds complexity, but it also adds a production-grade pub-sub and consumer model.",
        "Flask can do WebSockets through extensions or by switching to Quart, but the real-time story is more fragmented and less standardized.",
        "FastAPI inherits Starlette WebSocket support directly, so simple real-time features are clean. The missing piece is built-in multi-process pub-sub.",
        """class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(text_data=text_data)
""",
        """@sock.route("/ws")
def chat(ws):
    while True:
        message = ws.receive()
        ws.send(message)
""",
        """@app.websocket("/ws")
async def chat(ws: WebSocket):
    await ws.accept()
    while True:
        await ws.send_text(await ws.receive_text())
""",
        "Django Channels is the heaviest path, Flask the least standardized, and FastAPI the cleanest for simple cases. At scale, the question becomes pub-sub strategy rather than decorator syntax.",
        "For small real-time features, FastAPI usually gives the cleanest implementation. For large multi-process WebSocket systems, Django Channels has the most battle-tested built-in architecture in Python.",
        "conditional",
        "FastAPI wins for simple native WebSockets; Django Channels wins when the real-time system itself is a major subsystem with pub-sub, groups, and operational rigor.",
        "A senior engineer may still choose Flask if the team already standardized on Socket.IO or Quart and values ecosystem continuity more than framework purity.",
        frameworks=("fastapi", "django"),
        modes=("api",),
    ),
    sec(
        "CM14",
        4,
        "auth",
        "Built-in Authentication Comparison",
        ["CM11"],
        "Authentication is where hidden framework cost becomes painfully visible because a complete login system is far more work than most teams estimate.",
        "This compares email and password auth with verification and reset flows, because that is the real product requirement people under-scope when choosing frameworks.",
        "Django ships almost the whole browser-auth stack already: user model, password hashing, sessions, auth views, forms, permissions, and reset flows.",
        "Flask can absolutely do auth well, but the stack is assembled from extensions such as Flask-Login, Flask-Mail, bcrypt, and token utilities. The integration burden is real.",
        "FastAPI provides security utilities, not a finished auth system. JWT examples are common, but complete product auth still means substantial custom code or third-party packages.",
        """from django.contrib.auth.views import LoginView, PasswordResetView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("password-reset/", PasswordResetView.as_view()),
]
""",
        """login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
""",
        """oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_token(token)
""",
        "Django's auth is a product feature. Flask and FastAPI auth are integration projects. That difference dominates schedule and security risk more than most feature matrices admit.",
        "Estimated custom code for full email verification plus reset is often measured in tens of lines on Django and hundreds in Flask or FastAPI. That is years of framework history cashing out into present-day delivery speed.",
        "django",
        "Django wins decisively for standard product authentication because the framework already contains most of the hard parts.",
        "A senior API platform team may still choose FastAPI because browser-oriented auth is not the product and machine-to-machine auth is the real requirement.",
        frameworks=("django",),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM15",
        4,
        "auth",
        "Permission Systems",
        ["CM14"],
        "Permission systems are where simple auth stops and real business policy begins.",
        "This compares built-in permissions, groups, and object-level checks because business software rarely stops at 'is logged in.'",
        "Django has model permissions, groups, decorators, and ecosystem extensions like django-guardian for object-level policy. It is the most complete default permission story here.",
        "Flask can implement role-based access cleanly, but you are building the abstraction yourself or choosing a third-party library that your team must own operationally.",
        "FastAPI turns permissions into dependencies, which is elegant and testable, but the actual policy model is still yours to design.",
        """@permission_required("shop.change_product")
def edit_product(request, pk):
    ...
""",
        """def require_role(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
""",
        """async def require_admin(user = Depends(get_current_user)):
    if "admin" not in user.scopes:
        raise HTTPException(status_code=403, detail="forbidden")
""",
        "Django treats permissions as a first-class subsystem. Flask and FastAPI treat them as application code patterns. That distinction matters enormously in enterprise apps.",
        "Object-level permissions and group integration are product features in Django, not optional architecture add-ons. In Flask and FastAPI, equivalent capability usually means more custom code and more consistency risk.",
        "django",
        "Django wins because it gives the deepest permission system with the least custom engineering.",
        "A senior FastAPI team may still prefer dependency-based authorization when the auth model is token-scope-centric and the system is API-only.",
        frameworks=("django",),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM16",
        4,
        "auth",
        "Security Defaults",
        ["CM14", "CM15"],
        "Security defaults matter because most incidents come from what teams forgot to configure, not from what they intentionally built.",
        "This compares the out-of-the-box security posture of the frameworks for their natural use cases.",
        "Django starts from the safest default position for full-stack apps: CSRF, secure password hashing, template auto-escaping, clickjacking headers, and security middleware patterns are already present.",
        "Flask starts nearly empty. That is not a flaw if you want a tiny core, but it means the framework does not save you from missing CSRF, headers, or secure session configuration.",
        "FastAPI helps at the validation boundary, but APIs still need explicit rate limiting, auth discipline, CORS configuration, and response-model data minimization. It is not secure by magic.",
        """MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
""",
        """app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
)
# add Flask-WTF, Talisman, and CSRF deliberately
""",
        """app.add_middleware(CORSMiddleware, allow_origins=["https://app.example.com"])
# response_model and auth dependencies prevent overexposure
""",
        "Django wins on secure-by-default full-stack behavior. Flask and FastAPI can be hardened well, but they demand more deliberate engineering.",
        "This is not ideology. Django literally enables more defensive features by default. Flask and FastAPI are lighter frameworks with different threat-model assumptions, especially for API-only services.",
        "django",
        "Django wins for default security posture, especially when browser sessions, forms, and templates are in scope.",
        "A senior API engineer may still prefer FastAPI because API threat models differ from HTML threat models and the lighter stack can reduce unrelated attack surface.",
        frameworks=("django",),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM17",
        5,
        "performance",
        "Synchronous Performance Comparison",
        ["CM04"],
        "Sync performance is where most framework debates become exaggerated because the numbers are closer than internet arguments suggest.",
        "This compares identical sync-style endpoints under the same hardware and load assumptions to show how little the framework brand matters for most CRUD apps.",
        "Django sync performance is lower than Flask or FastAPI sync in simple benchmarks, but usually not by enough to matter for standard business traffic.",
        "Flask is usually a bit leaner than Django in sync mode because it runs less framework machinery around each request.",
        "FastAPI with sync handlers is also competitive, but the headline point is that sync-mode framework differences are small compared with query efficiency and caching.",
        """# Django sync endpoint
def users(request):
    return JsonResponse({"users": list(User.objects.values("id", "email")[:20])})
""",
        """# Flask sync endpoint
@app.get("/users")
def users():
    return {"users": [u.to_dict() for u in User.query.limit(20)]}
""",
        """# FastAPI sync endpoint
@app.get("/users")
def users(session: Session = Depends(get_sync_db)):
    return session.execute(select(User).limit(20)).scalars().all()
""",
        "The truth is boring: Flask and FastAPI usually edge Django in sync microbenchmarks, but all three are fast enough for the majority of internal tools and CRUD apps when the database work is sane.",
        "Representative numbers for 100 concurrent users and a small DB-backed JSON endpoint often look like Django about 800 RPS, Flask about 1000 RPS, and FastAPI sync about 1100 RPS. That is a measurable but rarely decisive gap.",
        "tie",
        "Treat sync performance as effectively a tie for normal business workloads. Architecture fit dominates once traffic is not extreme.",
        "A senior platform engineer may still choose Flask or FastAPI here if memory footprint and container density matter more than integrated full-stack features.",
        frameworks=("flask", "fastapi", "django"),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM18",
        5,
        "performance",
        "Asynchronous Performance Comparison",
        ["CM04", "CM17"],
        "Async performance is the one category where FastAPI can deliver a genuinely different operating envelope for I/O-bound APIs.",
        "This compares async-capable setups because concurrency behavior matters only when the workload spends meaningful time waiting on I/O.",
        "Django's async story is improving, but it remains a mixed sync and async ecosystem where some parts are modern and others still lag or need careful isolation.",
        "Flask is fundamentally a WSGI-first framework. Async views exist, but the overall async story is not its strongest reason to exist.",
        "FastAPI was designed around ASGI and async handlers from the beginning, so it is the cleanest path when many concurrent I/O waits dominate.",
        """async def users(request):
    rows = await sync_to_async(list)(User.objects.values("id", "email")[:20])
    return JsonResponse({"users": rows})
""",
        """@app.get("/users")
def users():
    # commonly still served with sync workers or gevent
    return {"users": service.list_users()}
""",
        """@app.get("/users")
async def users(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).limit(20))
    return result.scalars().all()
""",
        "FastAPI wins when the workload is I/O-bound and the team actually understands async. If the workload is CPU-bound, the async advantage disappears and the complexity remains.",
        "Representative async benchmark numbers for a DB-bound list endpoint often show FastAPI around 4500 RPS, Django async around 2800 RPS, and sync stacks far lower. The caveat is essential: those gains only appear when the whole stack is truly async.",
        "fastapi",
        "FastAPI wins for high-concurrency I/O-bound APIs because async is a first-class design decision rather than a partially retrofitted feature.",
        "A senior Django team may still choose Django async if the API is only one part of a much larger Django platform and the performance envelope is already sufficient.",
        frameworks=("fastapi",),
        modes=("api", "ml"),
    ),
    sec(
        "CM19",
        5,
        "performance",
        "Memory & Startup Performance",
        ["CM17", "CM18"],
        "Cold start time and idle memory decide whether a framework is viable for serverless, dense container packing, or edge-style deployments.",
        "This compares import time and idle worker footprint because those costs are paid before the first useful request even arrives.",
        "Django carries the most startup work because apps, models, settings, and ORM subsystems load eagerly. That is fine on long-lived servers and bad in cold-start-heavy environments.",
        "Flask starts quickly and stays light because the core surface is small. That makes it attractive for tiny services and serverless functions.",
        "FastAPI is also relatively light, though Pydantic and docs generation add some startup overhead compared with bare Flask. It is still much lighter than Django for cold starts.",
        """time python -c "import django; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings'); django.setup()"
""",
        """time python -c "from flask import Flask; Flask(__name__)"
""",
        """time python -c "from fastapi import FastAPI; FastAPI()"
""",
        "Django pays the highest fixed platform cost. Flask is the lightest. FastAPI stays closer to Flask than to Django, which is one reason it fits serverless and microservice workloads well.",
        "Representative cold-start numbers often look roughly like Flask about 0.1s, FastAPI about 0.3s, and Django about 1.2s on simple local measurements, with Django also consuming notably more idle memory per worker.",
        "fastapi",
        "For serverless or density-sensitive deployments, FastAPI and Flask both beat Django. FastAPI gets the nod when you also need a serious API contract layer.",
        "A senior engineer may still choose Django if the service is long-lived and the operational cost of cold starts is irrelevant compared with the product features Django deletes.",
        frameworks=("fastapi", "flask"),
        modes=("api", "ml"),
    ),
    sec(
        "CM20",
        5,
        "data",
        "Database Query Performance",
        ["CM08", "CM17"],
        "The database layer is where framework arguments usually disappear, because query shape beats framework overhead by an order of magnitude.",
        "This compares the same N+1 problem and its fix because bad query planning destroys performance in every framework equally.",
        "Django gives select_related and prefetch_related, which are simple and effective, but the team still has to remember to use them.",
        "Flask with SQLAlchemy has joinedload and selectinload, and the same truth applies: the ORM is not slow, the careless query pattern is slow.",
        "FastAPI inherits SQLAlchemy behavior, so its DB performance story is really a story about whether the async session and loading strategy are configured correctly.",
        """users = User.objects.select_related("profile").prefetch_related("orders")[:100]
""",
        """users = db.session.execute(select(User).options(joinedload(User.profile), selectinload(User.orders))).scalars().all()
""",
        """users = (await session.execute(select(User).options(joinedload(User.profile), selectinload(User.orders)))).scalars().all()
""",
        "All three frameworks lose badly with N+1 queries and all three recover dramatically when the query shape is fixed. The framework choice is secondary to query literacy.",
        "Typical demonstrations show 100 parent rows with children taking around two seconds with 101 queries and around a tenth of a second once eager loading reduces the work to one or two queries. That gap dwarfs framework-level overhead.",
        "tie",
        "This is a tie. Query design matters far more than framework choice.",
        "A senior engineer may still prefer SQLAlchemy here because Core plus ORM gives them more expressive escape hatches for the ugly twenty percent of queries.",
        frameworks=("django", "flask", "fastapi"),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM21",
        6,
        "dx",
        "Learning Curve Comparison",
        ["CM01", "CM02", "CM03"],
        "The best framework for a team is often the one that fails in the most understandable way for that team's skill profile.",
        "This compares how each framework feels over the first weeks of adoption, not just the first hello world.",
        "Django is steep but predictable. The early experience is good, then the team eventually meets the wall of CBVs, ORM subtleties, middleware, signals, and DRF complexity.",
        "Flask feels easiest at the beginning. The trap is that teams mistake low initial friction for low total complexity and discover too late that they have been rebuilding framework features.",
        "FastAPI is approachable until async, dependency graphs, and database lifecycles get real. The async cliff is smaller if the team already knows modern Python typing and asyncio.",
        """# Django first success usually comes fast
def home(request):
    return render(request, "home.html")
""",
        """# Flask first success is even faster
@app.get("/")
def home():
    return "ok"
""",
        """# FastAPI first success is clean, but async is new to many teams
@app.get("/")
async def home():
    return {"ok": True}
""",
        "Django teaches convention, Flask teaches composition, and FastAPI teaches modern async API design. The pain arrives at different times in each framework.",
        "Time to first working feature is often fastest in Flask, slightly slower in Django, and slower again in FastAPI for developers who are new to asyncio and type-driven design. Time to long-term maintainability often flips those rankings.",
        "conditional",
        "For junior generalists, Django usually wins. For experienced API engineers, FastAPI often wins. Flask is best only when the team really wants the composition burden.",
        "A senior Flask team may prefer Flask precisely because its learning curve is front-loaded into normal Python rather than framework-specific magic.",
        frameworks=("django", "fastapi", "flask"),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM22",
        6,
        "dx",
        "Documentation & Error Message Quality",
        ["CM21"],
        "Documentation quality changes both onboarding speed and the cost of debugging under pressure.",
        "This compares the quality of the official docs plus the default error surfaces developers and API consumers actually see.",
        "Django documentation is still the most complete and historically deep. It explains not only how but often why.",
        "Flask documentation is clear and concise, which fits its smaller surface area. The downside is that the ecosystem story is more fragmented across extension docs.",
        "FastAPI has the most modern docs experience, and Pydantic validation errors are the clearest machine-and-human-friendly error payloads of the three.",
        """try:
    user = User.objects.get(pk=1)
except User.DoesNotExist:
    ...
""",
        """payload = request.get_json()
if payload is None:
    raise BadRequest("JSON body required")
""",
        """class UserCreate(BaseModel):
    email: EmailStr
    age: int = Field(ge=18)
""",
        "Django wins for breadth and reference depth. FastAPI wins for live interactive API docs and validation feedback. Flask is good, but smaller and more dependent on extension quality.",
        "The evidence is practical: Django docs remain the benchmark for framework documentation, while FastAPI plus Pydantic currently provide the best default developer-facing and client-facing validation experience.",
        "conditional",
        "Django wins on documentation depth; FastAPI wins on API docs and error clarity.",
        "A senior engineer may still prefer Flask docs because the smaller surface area means the framework itself is rarely the confusing part.",
        frameworks=("django", "fastapi"),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM23",
        6,
        "testing",
        "Testing Experience",
        ["CM11"],
        "Test quality is where architecture discipline becomes measurable rather than aspirational.",
        "This compares the same auth plus CRUD test because frameworks feel very different once you try to isolate dependencies and failure cases.",
        "Django TestCase is integrated and complete. The downside is that fixtures are painful and the framework stack can make narrow tests feel heavier than necessary.",
        "Flask is comfortable with pytest and app factories, but extension setup still determines how cleanly dependencies can be isolated.",
        "FastAPI's dependency_overrides model is currently the cleanest isolation mechanism of the three for HTTP-level tests.",
        """class UserTests(TestCase):
    def test_list_requires_auth(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, 403)
""",
        """def test_list_requires_auth(client):
    response = client.get("/users")
    assert response.status_code == 401
""",
        """def test_list_requires_auth(client, app):
    app.dependency_overrides[get_current_user] = lambda: None
    assert client.get("/users").status_code == 401
""",
        "Django gives the deepest integrated test world, Flask gives a pleasant pytest story, and FastAPI gives the cleanest explicit override mechanism for isolated API tests.",
        "Many senior Python teams consider FastAPI the most testable API framework because dependency injection is not an afterthought. Django still wins where full-stack integration testing of templates, auth, admin, and ORM all matter together.",
        "fastapi",
        "FastAPI wins for API testability because dependency overrides make isolation explicit and cheap.",
        "A senior Django team may still prefer Django because the framework can test the entire integrated product stack in one place without assembling external test scaffolding.",
        frameworks=("fastapi", "django"),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM24",
        6,
        "dx",
        "Code Generation & Scaffolding",
        ["CM21"],
        "Scaffolding affects how quickly a team reaches the first stable baseline rather than hand-assembling project shape from memory.",
        "This compares what the official tooling gives you in the first hour of a new project.",
        "Django has the strongest official project scaffolding by far. startproject and startapp codify a default project shape that thousands of teams recognize.",
        "Flask intentionally does very little here, so real scaffolding usually comes from cookiecutter templates and team conventions.",
        "FastAPI has strong example templates, but no equivalent official CLI scaffolding story for a full production stack.",
        """django-admin startproject config
python manage.py startapp users
""",
        """pip install cookiecutter-flask
cookiecutter https://github.com/cookiecutter-flask/cookiecutter-flask
""",
        """# official fastapi full-stack template
cookiecutter gh:fastapi/full-stack-fastapi-template
""",
        "Django reduces blank-page decision fatigue the most. Flask and FastAPI both rely more heavily on template ecosystems and team taste.",
        "That productivity difference is real: Django scaffolding can save a couple of days at the start of a project because the app structure, commands, and defaults already exist.",
        "django",
        "Django wins because its official project scaffolding is the most mature and least ambiguous.",
        "A senior FastAPI team may still choose the official full-stack template because it reflects a modern API-first deployment model better than Django's older assumptions.",
        frameworks=("django",),
        modes=("api", "full-stack"),
    ),
    sec(
        "CM25",
        7,
        "async",
        "Async Story Completeness",
        ["CM17", "CM18"],
        "Async support is not binary; the real question is whether the entire request stack wants async or merely tolerates it.",
        "This compares how complete each framework's async story is in practice, including middleware, ORM, and third-party package reality.",
        "Django's async capabilities are real but partial. It is catching up, but the ecosystem still contains many sync assumptions and caveats.",
        "Flask supports async views, but the wider architecture remains WSGI-first unless you move to Quart or another ASGI-native sibling.",
        "FastAPI is async-native across routing, middleware, dependencies, and the common API-centric ecosystem around it. That coherence is the real win.",
        """async def dashboard(request):
    profile = await request.auser()
    return JsonResponse({"email": profile.email})
""",
        """@app.get("/status")
async def status():
    return {"ok": True}  # view can be async, stack is still mostly WSGI-shaped
""",
        """@app.get("/status")
async def status():
    await asyncio.sleep(0)
    return {"ok": True}
""",
        "Django async is improving, Flask async is partial, FastAPI async is the default mental model. If true async is a first-order requirement, the difference is material.",
        "The main evidence is architectural: FastAPI and Starlette were designed for ASGI first. Django and Flask added async later, which means their ecosystems still reflect older sync assumptions.",
        "fastapi",
        "FastAPI wins because its async story is the most coherent from the entry point down to common API libraries.",
        "A senior Django engineer may still choose Django async if the project already needs Django's full-stack capabilities and the async workload is meaningful but not extreme.",
        frameworks=("fastapi",),
        modes=("api", "ml"),
    ),
    sec(
        "CM26",
        7,
        "async",
        "WebSocket & Real-time at Scale",
        ["CM13", "CM25"],
        "Ten thousand connections care less about syntax and more about pub-sub, process coordination, and operational simplicity.",
        "This compares the frameworks when real-time is not a toy feature but a major operational concern.",
        "Django Channels is the heaviest option, but also the most complete Python-native answer for serious multi-process WebSocket systems.",
        "Flask can support real-time traffic, but it tends to rely on more fragmented extension choices and external coordination patterns.",
        "FastAPI makes the simple case elegant and the scaled case manual: WebSockets are easy, distributed fan-out is your job.",
        """# Django Channels routing
websocket_urlpatterns = [
    path("ws/chat/", ChatConsumer.as_asgi()),
]
""",
        """# Flask-Sock or Socket.IO often becomes the real-time entry point
sock = Sock(app)
""",
        """manager = ConnectionManager()
@app.websocket("/ws/chat")
async def chat(ws: WebSocket):
    await manager.connect(ws)
""",
        "Django Channels optimizes for operational completeness, FastAPI for simplicity, and Flask for doing only what the team chooses to assemble.",
        "For very high concurrent WebSocket counts, the decision is usually Django Channels or FastAPI plus Redis-backed coordination. Flask is valid, but less commonly the first serious recommendation at that scale.",
        "conditional",
        "Django wins when the real-time layer is itself a subsystem. FastAPI wins when the team wants a simpler native WebSocket surface and is willing to own the distributed coordination story.",
        "A senior team may still choose FastAPI here because direct Starlette WebSocket primitives are easier to reason about than Channels consumers and channel layers.",
        frameworks=("django", "fastapi"),
        modes=("api",),
    ),
    sec(
        "CM27",
        8,
        "dx",
        "Third-Party Ecosystem Maturity",
        ["CM01", "CM02", "CM03"],
        "Ecosystem maturity changes how often you have to build or own infrastructure features yourself.",
        "This compares package maturity, breadth, and abandonment risk because package count alone is not enough.",
        "Django's ecosystem is the deepest and most battle-tested. There is usually a maintained package for the obvious enterprise or product feature.",
        "Flask's ecosystem is broad and pragmatic, but more fragmented. You can find a package for most things, though maintenance quality varies more.",
        "FastAPI's ecosystem is younger and smaller, but modern in shape. The biggest gap is not package absence; it is that the ecosystem has fewer decade-old battle scars.",
        """INSTALLED_APPS += ["rest_framework", "allauth", "storages", "channels"]
""",
        """# common Flask add-ons
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
""",
        """# common FastAPI add-ons
from fastapi_cache import FastAPICache
from prometheus_fastapi_instrumentator import Instrumentator
""",
        "Django wins on ecosystem maturity, Flask on breadth plus simplicity, FastAPI on modern API-focused integrations. The more odd enterprise requirements you expect, the more Django's age becomes an asset.",
        "Approximate ecosystem size tells part of the story: Django-style packages vastly outnumber FastAPI-specific packages, but age also means more abandoned projects. Senior teams evaluate maintenance health, not just download counts.",
        "django",
        "Django wins because the ecosystem is the deepest and the most production-proven across the widest range of business requirements.",
        "A senior FastAPI team may still prefer the smaller ecosystem because fewer choices can mean less legacy baggage and more modern async-friendly packages.",
        frameworks=("django",),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM28",
        8,
        "dx",
        "CMS & Content Management",
        ["CM01", "CM10"],
        "Content management is one of the clearest objective decision points in the entire framework comparison.",
        "This dimension compares what happens when the product includes editors, workflows, previews, and content governance rather than just APIs.",
        "Django dominates CMS use cases because Wagtail, Django CMS, and the admin ecosystem all assume Django's full-stack model.",
        "Flask can back a CMS, but the usual pattern is building a custom admin or going headless. That is more engineering work for less out-of-the-box leverage.",
        "FastAPI is not a CMS framework. It can serve a headless content API, but the editorial experience must come from somewhere else.",
        """# Django + Wagtail is a standard CMS path
INSTALLED_APPS += ["wagtail", "wagtail.admin", "wagtail.users"]
""",
        """# Flask typically needs a custom content admin
admin.add_view(ModelView(Article, db.session))
""",
        """@router.get("/articles/{slug}")
async def article(slug: str):
    return await article_service.read(slug)
""",
        "If content management is a requirement, the comparison is nearly over. Django has a real CMS ecosystem; Flask and FastAPI mostly have headless API stories.",
        "This is not a close category. The strongest Python CMS products are built on Django, not on Flask or FastAPI. That is decisive evidence about ecosystem fit.",
        "django",
        "Django wins outright for CMS and content-heavy products.",
        "A senior engineer may still choose FastAPI if the system is intentionally headless and the editorial tooling will live in a separate SaaS or frontend-managed platform.",
        frameworks=("django",),
        modes=("full-stack",),
    ),
    sec(
        "CM29",
        8,
        "async",
        "Machine Learning & Data Science Integration",
        ["CM18", "CM27"],
        "ML serving wants typed inputs, good concurrency for model I/O, and clear API contracts more than it wants a batteries-included web stack.",
        "This compares serving a trained model because the ML use case exposes one of FastAPI's strongest natural fits.",
        "Django is usually overkill for pure model serving, though it is fine when the ML feature sits inside a broader product with users, admin, and workflows.",
        "Flask has a long history in ML tutorials and small inference services. It still works well, especially for simple sync-serving use cases.",
        "FastAPI is the current default recommendation for many ML APIs because typed validation, async capability, and auto-generated docs fit model serving exceptionally well.",
        """def predict(request):
    features = json.loads(request.body)
    return JsonResponse({"score": model.predict([features])[0]})
""",
        """@app.post("/predict")
def predict():
    payload = request.get_json()
    return {"score": model.predict([payload])[0]}
""",
        """class Features(BaseModel):
    age: int
    balance: float

@app.post("/predict")
async def predict(payload: Features):
    return {"score": float(model.predict([[payload.age, payload.balance]])[0])}
""",
        "Flask is serviceable, Django is situational, and FastAPI is the cleanest fit when the deliverable is an inference API or model-serving gateway.",
        "FastAPI's popularity in ML serving is not hype alone. Pydantic contracts, OpenAPI docs, and async-friendly serving patterns map naturally to inference endpoints and data APIs.",
        "fastapi",
        "FastAPI wins decisively for ML model serving and typed data APIs.",
        "A senior engineer may still choose Flask if the serving stack is tiny, synchronous, and already embedded in a mature Flask-oriented internal platform.",
        frameworks=("fastapi",),
        modes=("api", "ml"),
    ),
    sec(
        "CM30",
        9,
        "ops",
        "Deployment Complexity",
        ["CM17", "CM18", "CM19"],
        "Deployment complexity is where framework choice turns into image size, config sprawl, and operator burden.",
        "This compares a production Docker setup because deployment cost is part of framework cost.",
        "Django deployments usually include more config for static files, media handling, migrations, admin security, and larger startup footprints. That complexity is justified when those features matter.",
        "Flask deployments are operationally smaller, though the final complexity depends heavily on which extensions the team adopted.",
        "FastAPI deployments are small and API-friendly, but ASGI worker configuration, lifespan correctness, and async dependency setup must be done carefully.",
        """CMD ["gunicorn", "config.wsgi:application", "--workers", "4"]
""",
        """CMD ["gunicorn", "app:create_app()", "--workers", "4"]
""",
        """CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--workers", "4"]
""",
        "Django is usually the heaviest to deploy, Flask the simplest, and FastAPI close to Flask but with ASGI-specific operational detail. Simplicity wins only if you do not later need the features Django front-loads.",
        "Container sizes and cold-start profiles generally reinforce the same picture: Django images and workers are heavier, Flask and FastAPI lighter. The important caveat is that package selection often dominates framework-only size differences.",
        "fastapi",
        "For API deployments, FastAPI usually wins because it stays operationally light while still providing a strong contract layer.",
        "A senior platform team may still choose Django because the deployment is only slightly heavier than Flask once the product already needs the many features Django provides.",
        frameworks=("fastapi", "flask"),
        modes=("api", "ml"),
    ),
    sec(
        "CM31",
        9,
        "ops",
        "Horizontal Scaling Patterns",
        ["CM30"],
        "Most horizontal scaling advice is framework-independent, but session and state handling still create framework-specific pain points.",
        "This compares how stateless scaling changes depending on whether the framework prefers sessions, JWTs, or explicit shared state stores.",
        "Django can scale horizontally well, but session-backed browser apps often need sticky sessions or a shared session backend such as Redis or the database.",
        "Flask has the same issue whenever server-side or signed session state matters, though many Flask APIs avoid sessions entirely.",
        "FastAPI often ends up with JWT-based API auth and stateless services, which makes horizontal scaling particularly natural when the system is API-only.",
        """SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
""",
        """app.config["SESSION_TYPE"] = "redis"
""",
        """@app.get("/health")
async def health():
    return {"state": "stateless", "ready": True}
""",
        "Statefulness, not framework speed, is the real scaling constraint. FastAPI often wins simply because API-first designs lean toward statelessness by default.",
        "All three frameworks scale well behind a load balancer when the service is stateless. The difference is that Django and Flask full-stack apps more often carry session and media concerns that complicate the story.",
        "fastapi",
        "FastAPI wins slightly because JWT-oriented API services are usually the easiest to scale horizontally.",
        "A senior Django engineer may still choose Django here because Redis-backed sessions and a disciplined stateless edge design solve the operational issue just fine.",
        frameworks=("fastapi",),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM32",
        9,
        "ops",
        "Monitoring & Observability",
        ["CM30", "CM31"],
        "Observability quality affects not only debugging but also whether a framework fits a modern platform engineering environment.",
        "This compares instrumentation, metrics, tracing, and profiling because modern web services are judged partly by how observable they are in production.",
        "Django has good tooling like debug-toolbar and Sentry integration, but OpenTelemetry tends to feel more additive than native.",
        "Flask also instruments cleanly, though the ecosystem is scattered across exporter packages and middleware integrations.",
        "FastAPI has particularly good modern tracing and metrics integrations because the ASGI ecosystem and Starlette middleware model align well with current observability tooling.",
        """MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
""",
        """from prometheus_flask_exporter import PrometheusMetrics
PrometheusMetrics(app)
""",
        """from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
""",
        "All three can be observed well, but FastAPI and the ASGI stack feel most aligned with present-day tracing and metrics conventions for microservices.",
        "FastAPI often wins in OpenTelemetry and Prometheus ergonomics, while Django still offers strong debugging tooling for full-stack application development. The winner depends on whether you are instrumenting APIs or integrated product apps.",
        "fastapi",
        "FastAPI wins for modern API observability and tracing integration.",
        "A senior Django team may still prefer Django here because debug-toolbar plus mature Sentry usage can be more useful day to day than raw tracing elegance.",
        frameworks=("fastapi",),
        modes=("api", "ml"),
    ),
    sec(
        "CM33",
        10,
        "decision",
        "Decision Tree: Framework Selection",
        ["CM01", "CM02", "CM03", "CM30", "CM32"],
        "Most framework debates end once you ask the questions in the right order: full-stack needs first, then API shape, then async need, then team skill.",
        "This section turns the whole document into a practical decision sequence rather than a pile of disconnected opinions.",
        "Django should be the default answer when the product needs admin, forms, sessions, templates, and built-in governance. That is not nostalgia; it is fit.",
        "Flask is a valid answer when the team knows exactly what it wants to assemble and values minimalism over integrated platform features.",
        "FastAPI should be the default answer when the deliverable is an API, async concurrency matters, or ML/data-serving needs dominate.",
        """# Django starter for product apps
django-admin startproject config
python manage.py startapp billing
""",
        """# Flask starter for deliberately minimal services
python -m pip install flask
flask --app app run
""",
        """# FastAPI starter for typed APIs
python -m pip install fastapi uvicorn
uvicorn app.main:app --reload
""",
        "The decision order matters more than individual framework strengths. If you ask 'which is fastest' before 'do we need an admin', you will choose badly.",
        "The strongest evidence in this document is cumulative: Django dominates full-stack and admin-heavy business apps, FastAPI dominates typed async APIs and ML-serving, and Flask wins only where deliberate minimalism is the real requirement rather than an aesthetic preference.",
        "conditional",
        "Use the decision tree, not a single slogan. Django for product platforms, FastAPI for APIs, Flask for intentionally minimal custom stacks.",
        "A senior engineer may still choose the non-obvious option if organization constraints, hiring reality, or existing platform investment dominate the technical ideal.",
        frameworks=("django", "fastapi", "flask"),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM34",
        10,
        "decision",
        "Project Type -> Framework Matrix",
        ["CM33"],
        "A good framework recommendation is never universal; it is conditional on the project type and business outcome.",
        "This compares the most common project types because many teams do not need a perfect framework, only the least wrong one for their actual business shape.",
        "Django consistently wins content-heavy platforms, e-commerce back offices, internal tools, and enterprise apps because integrated features cut delivery time dramatically.",
        "Flask is strongest in deliberately minimal custom services, prototypes where the team really knows its stack, and cases where existing Flask expertise is already a strategic asset.",
        "FastAPI wins REST APIs, ML serving, microservices, and modern typed service contracts where docs, async, and validation are primary requirements.",
        """# Django example projects
BLOG = "Django + Wagtail"
ERP = "Django + admin + DRF"
""",
        """# Flask example projects
INTERNAL_API = "Flask + SQLAlchemy"
CUSTOM_GATEWAY = "Flask + bespoke middleware"
""",
        """# FastAPI example projects
MODEL_API = "FastAPI + Pydantic + async DB"
MICROSERVICE = "FastAPI + Redis + OpenAPI"
""",
        "This matrix is not a spreadsheet game. It is the business-facing summary of the architectural comparisons that came earlier.",
        "The evidence behind the matrix links back to specific sections: admin cost, auth cost, async throughput, CMS support, and observability fit all push different project types toward different winners.",
        "conditional",
        "Use the matrix as the fastest route to a defensible default recommendation, then verify the edge cases in CM35 and CM36.",
        "A senior team may still break the matrix deliberately if organizational alignment, platform reuse, or hiring constraints make the technically second-best option the practically best one.",
        frameworks=("django", "fastapi", "flask"),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM35",
        10,
        "decision",
        "Team Skill -> Framework Recommendation",
        ["CM33"],
        "Team capability changes framework fitness because a good architecture in the wrong hands is still the wrong architecture.",
        "This compares which framework best matches junior teams, enterprise teams, async-native teams, and data-science-heavy teams.",
        "Django is the safest choice for junior-heavy teams and organizations that value strong guardrails, documentation, and predictable conventions.",
        "Flask fits best when the team is experienced, already knows Flask deeply, and intentionally wants to control the stack rather than inherit defaults.",
        "FastAPI is best when the team is strong in modern Python typing, async thinking, API design, or model-serving workflows.",
        """# Django guardrails help junior-heavy teams
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status")
""",
        """# Flask rewards teams with strong discipline
def create_app(config_obj) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_obj)
    return app
""",
        """# FastAPI rewards async-native teams
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode(token)
""",
        "Framework choice is also a hiring and onboarding decision. The framework that matches the team's actual strengths usually outperforms the theoretically better framework the team misuses.",
        "Junior Python teams usually do better in Django. Strong async backend teams often do best in FastAPI. A company with years of Flask knowledge may rationally stay on Flask because switching cost is real engineering cost.",
        "conditional",
        "Choose the framework your team can use correctly under deadline pressure, not the one that wins abstract internet arguments.",
        "A senior engineer may still choose a steeper framework if the project horizon is long and the team can afford to invest in learning the better long-term fit.",
        frameworks=("django", "fastapi", "flask"),
        modes=("api", "full-stack", "ml"),
    ),
    sec(
        "CM36",
        10,
        "decision",
        "Cost of Wrong Choice",
        ["CM33", "CM34", "CM35"],
        "The true cost of a framework is often paid later, when the system outgrows the reason it was chosen.",
        "This compares what happens when you outgrow Flask, Django, or FastAPI, and what migration paths actually look like.",
        "Outgrowing Django usually means extracting API-heavy or real-time pieces into lighter services, not throwing Django away. The migration is often a strangler pattern, not a rewrite.",
        "Outgrowing Flask often means the team has recreated pieces of Django poorly. The cost is untangling architecture debt and deciding whether to add discipline or migrate to a more opinionated platform.",
        "Outgrowing FastAPI often means stakeholders now want admin, back-office workflows, and content tooling. The answer is usually adding a separate admin service or a Django sidecar, not forcing FastAPI to become Django.",
        """# Django -> extract API
urlpatterns = [
    path("api/", include("api.urls")),
]
""",
        """# Flask -> impose structure or migrate
def create_app():
    register_extensions(app)
    register_blueprints(app)
""",
        """# FastAPI -> add admin sidecar
services:
  api: fastapi
  admin: django
""",
        "The wrong choice is not fatal if the team migrates incrementally. The strangler pattern is the adult answer in all three cases.",
        "Real migration cost comes from domain coupling, not route syntax. Django to FastAPI is usually API extraction, Flask to Django is usually paying down architecture debt, and FastAPI to Django is usually adding a separate back-office surface.",
        "conditional",
        "The best framework choice is the one whose future escape hatch your team can actually afford.",
        "A senior engineer may knowingly choose a framework with a visible future migration path because shipping now is worth more than theoretical permanence.",
        frameworks=("django", "fastapi", "flask"),
        modes=("api", "full-stack", "ml"),
    ),
]

SECTIONS.sort(key=lambda item: int(item["id"][2:]))

PROJECT_MATRIX = [
    ("Content/CMS website", "django", 1, "CM28"),
    ("REST API low traffic", "fastapi", 2, "CM11"),
    ("REST API high traffic", "fastapi", 2, "CM18"),
    ("ML model serving", "fastapi", 1, "CM29"),
    ("E-commerce platform", "django", 2, "CM10"),
    ("Real-time app", "conditional", 3, "CM26"),
    ("Microservice", "fastapi", 1, "CM33"),
    ("Startup MVP", "django", 2, "CM02"),
    ("Enterprise app", "django", 2, "CM15"),
    ("Internal tooling", "django", 1, "CM10"),
    ("GraphQL API", "conditional", 3, "CM34"),
    ("Serverless/FaaS", "fastapi", 1, "CM19"),
]

SCORE_CARDS = {
    "django": [("Learning Curve", 4), ("API Dev", 4), ("Full-stack", 5), ("Performance", 3), ("Auth", 5), ("Admin", 5), ("Ecosystem", 5), ("Testing", 4), ("Async", 3), ("Documentation", 5)],
    "flask": [("Learning Curve", 3), ("API Dev", 3), ("Full-stack", 2), ("Performance", 4), ("Auth", 2), ("Admin", 2), ("Ecosystem", 4), ("Testing", 4), ("Async", 2), ("Documentation", 4)],
    "fastapi": [("Learning Curve", 3), ("API Dev", 5), ("Full-stack", 2), ("Performance", 5), ("Auth", 3), ("Admin", 1), ("Ecosystem", 3), ("Testing", 5), ("Async", 5), ("Documentation", 4)],
}

INTERVIEW_QA = [
    ("When would you choose Django over FastAPI even for an API?", "When the API is only one subsystem inside a larger full-stack product that also needs admin, auth, ORM, back-office workflows, and strong framework guardrails."),
    ("Why is Flask still a valid choice in 2026?", "Because deliberate minimalism, existing team expertise, and a controlled dependency story can beat both Django's weight and FastAPI's async complexity for the right service."),
    ("Is FastAPI always faster than Django?", "No. It is usually much faster only for genuinely async I/O-bound APIs. For sync CRUD, the differences are much smaller and rarely business-decisive."),
    ("What is Django's biggest hidden advantage?", "Admin plus auth plus migrations plus permissions. Those are years of product engineering hidden behind configuration."),
    ("What is Flask's biggest hidden cost?", "Architecture debt. Teams often discover they have rebuilt half of Django badly after the route count and feature count grow."),
    ("What is FastAPI's biggest hidden cost?", "Everything outside the API: admin, browser auth flows, CMS needs, and async expertise still have to come from elsewhere."),
    ("Which framework is most secure by default?", "Django, especially for full-stack apps, because CSRF, secure auth defaults, and security middleware are part of the platform."),
    ("Which framework is best for ML serving?", "FastAPI, because typed validation, OpenAPI docs, and async-friendly serving patterns fit inference APIs extremely well."),
    ("Can Django do async well enough now?", "Often yes, but its async story is still less coherent than FastAPI's and more sensitive to sync ecosystem edges."),
    ("What is the adult migration strategy if you chose wrong?", "Use the strangler pattern: extract the parts that need a different framework while keeping the original system alive long enough to de-risk the move."),
]

READING = [
    ("Django documentation", "https://docs.djangoproject.com/en/4.2/"),
    ("Flask documentation", "https://flask.palletsprojects.com/en/3.0.x/"),
    ("FastAPI documentation", "https://fastapi.tiangolo.com/"),
    ("Django REST Framework", "https://www.django-rest-framework.org/"),
    ("SQLAlchemy 2.0", "https://docs.sqlalchemy.org/en/20/"),
    ("Pydantic v2", "https://docs.pydantic.dev/latest/"),
    ("Django Channels", "https://channels.readthedocs.io/"),
    ("Alembic", "https://alembic.sqlalchemy.org/"),
    ("TechEmpower benchmarks methodology", "https://www.techempower.com/benchmarks/"),
]


def validate_graph() -> None:
    ids = [item["id"] for item in SECTIONS]
    if len(ids) != 36:
        raise ValueError(f"Expected 36 sections, found {len(ids)}")
    seen = set()
    for item in SECTIONS:
        for prereq in item["prereqs"]:
            if prereq not in ids:
                raise ValueError(f"Unknown prerequisite {prereq} for {item['id']}")
            if prereq not in seen:
                raise ValueError(f"Prerequisite {prereq} appears after {item['id']}")
        seen.add(item["id"])


def build_dependents():
    deps = defaultdict(list)
    for item in SECTIONS:
        for prereq in item["prereqs"]:
            deps[prereq].append(item["id"])
    return deps


def render_badges(ids):
    if not ids:
        return "<span class='badge subtle'>None</span>"
    return "".join(f"<a class='badge' href='#{escape(i)}'>{escape(i)}</a>" for i in ids)


def render_framework_cards(item):
    cards = []
    for framework in FRAMEWORKS:
        cards.append(
            f"""
<article class='approach-card framework-{framework}'>
  <h4>{framework_badge(framework)} {escape(FRAMEWORK_LABELS[framework])}'s Approach</h4>
  <p>{escape(item[framework])}</p>
  <div class='framework-code-label framework-{framework}'>{escape(FRAMEWORK_LABELS[framework])}</div>
  {render_pre(item[f'code_{framework}'], 'python')}
</article>
"""
        )
    return f"<div class='approach-grid'>{''.join(cards)}</div>"


def render_three_way_tabs(item):
    return render_tabs(
        item["id"],
        [
            ("Django", "django", "python", item["code_django"]),
            ("Flask", "flask", "python", item["code_flask"]),
            ("FastAPI", "fastapi", "python", item["code_fastapi"]),
        ],
    )


def render_svg_bar_chart(title, values):
    max_value = max(v for _, v, _ in values)
    bars = []
    labels = []
    for index, (label, value, framework) in enumerate(values):
        width = 520 * (value / max_value)
        y = 24 + index * 38
        bars.append(
            f"<rect x='140' y='{y}' width='{width:.1f}' height='24' rx='8' class='chart-bar framework-{framework}'></rect>"
            f"<text x='{150 + width:.1f}' y='{y + 17}' class='chart-value'>{escape(str(value))}</text>"
        )
        labels.append(f"<text x='16' y='{y + 17}' class='chart-label'>{escape(label)}</text>")
    return f"""
<div class='svg-chart'>
  <div class='chart-title'>{escape(title)}</div>
  <svg viewBox='0 0 700 180' role='img' aria-label='{escape(title)}'>
    {''.join(labels)}
    {''.join(bars)}
  </svg>
</div>
"""


def render_feature_matrix():
    rows = [
        ("ORM", "Yes", "No", "No"),
        ("Admin", "Yes", "No", "No"),
        ("Auth system", "Yes", "Via extensions", "Utilities only"),
        ("Templates", "Yes", "Yes", "Minimal support"),
        ("Forms", "Yes", "Via extensions", "Request forms only"),
        ("CSRF", "Yes", "Via extensions", "No"),
        ("Sessions", "Yes", "Client sessions", "No default"),
        ("Migrations", "Yes", "Via Alembic", "Via Alembic"),
        ("OpenAPI docs", "Via DRF", "Via extension", "Yes"),
        ("Async-first", "Partial", "No", "Yes"),
    ]
    body = "".join(
        f"<tr><td>{escape(name)}</td><td class='framework-django'>{escape(dj)}</td><td class='framework-flask'>{escape(fl)}</td><td class='framework-fastapi'>{escape(fa)}</td></tr>"
        for name, dj, fl, fa in rows
    )
    return f"<div class='table-wrap comparison-table-wrap'><table class='comparison-table'><thead><tr><th>Feature</th><th class='framework-django'>Django</th><th class='framework-flask'>Flask</th><th class='framework-fastapi'>FastAPI</th></tr></thead><tbody>{body}</tbody></table></div>"


def render_cm03_extra():
    return """
<div class='spectrum-box'>
  <div class='spectrum-title'>Batteries Included Spectrum</div>
  <div class='spectrum-track'>
    <span class='spectrum-stop spectrum-flask'>Flask</span>
    <span class='spectrum-stop spectrum-fastapi'>FastAPI</span>
    <span class='spectrum-stop spectrum-django'>Django</span>
  </div>
</div>
""" + render_feature_matrix()


def render_cm17_extra():
    return render_svg_bar_chart(
        "Sync benchmark, 100 concurrent users, 30 seconds",
        [("Django", 800, "django"), ("Flask", 1000, "flask"), ("FastAPI sync", 1100, "fastapi")],
    )


def render_cm18_extra():
    return render_svg_bar_chart(
        "Async benchmark, I/O-bound endpoint",
        [("Django async", 2800, "django"), ("FastAPI async", 4500, "fastapi"), ("Flask sync/gevent", 1000, "flask")],
    )


SECTION_EXTRAS = {
    "CM03": render_cm03_extra,
    "CM17": render_cm17_extra,
    "CM18": render_cm18_extra,
}


def render_section(item, dependents, index):
    next_id = SECTIONS[index + 1]["id"] if index + 1 < len(SECTIONS) else "quick-reference"
    used_later = dependents.get(item["id"], [])
    extra_html = SECTION_EXTRAS[item["id"]]() if item["id"] in SECTION_EXTRAS else ""
    return f"""
<section id="{item['id']}" class="concept-section comparison-section" data-layer="{item['layer']}" data-title="{escape(item['title'])}" data-frameworks="{' '.join(item['frameworks'])}" data-modes="{' '.join(item['modes'])}">
  <div class="section-kicker">{item['id']} &middot; Layer {item['layer']} &middot; {escape(LAYER_NAMES[item['layer']])}</div>
  <h2>{escape(item['title'])}</h2>
  <div class="section-meta">
    <span class="cluster-pill {CLUSTER_CLASS[item['cluster']]}">{escape(item['cluster'].title())}</span>
    {verdict_badge(item['verdict'])}
  </div>
  <p class="lead">{escape(item['summary'])}</p>
  <div class="forward-links">
    <div><span class="meta-label">Read first</span>{render_badges(item['prereqs'])}</div>
    <div><span class="meta-label">Used in</span>{''.join(f"<a class='badge subtle' href='#{escape(cid)}'>{escape(cid)}</a>" for cid in used_later[:10]) or "<span class='badge subtle'>None</span>"}</div>
  </div>
  <h3>The Dimension</h3>
  <aside class="callout fact-box">{escape(item['dimension'])}</aside>
  <h3>Approaches</h3>
  {render_framework_cards(item)}
  <h3>Side-by-Side Code</h3>
  {render_three_way_tabs(item)}
  {extra_html}
  <h3>Trade-off Analysis</h3>
  <aside class="callout opinion-box">{escape(item['tradeoff'])}</aside>
  <h3>Data / Evidence</h3>
  <aside class="callout data-box">{escape(item['evidence'])}</aside>
  <h3>Verdict</h3>
  <aside class="callout verdict-box">{verdict_badge(item['verdict'])}<p>{escape(item['verdict_text'])}</p></aside>
  <h3>Dissenting View</h3>
  <p>{escape(item['dissent'])}</p>
  <div class="section-footer"><a class="prev-link" href="#dependency-table">Back to references</a><a class="next-link" href="#{next_id}">Next dimension &rarr; {next_id}</a></div>
</section>
"""


def render_dag():
    nodes = []
    edges = []
    for item in SECTIONS:
        nodes.append(f'    {item["id"]}["{item["id"]} {item["title"]}"]:::{item["cluster"]}')
        for prereq in item["prereqs"]:
            edges.append(f"    {prereq} --> {item['id']}")
    class_defs = """
    classDef architecture fill:#18231f,stroke:#7bb1ff,color:#f6f7f8;
    classDef performance fill:#13262c,stroke:#00e5ff,color:#f6f7f8;
    classDef data fill:#1d2820,stroke:#9fe870,color:#f6f7f8;
    classDef auth fill:#2a1e1e,stroke:#ff9b8f,color:#f6f7f8;
    classDef async fill:#14272d,stroke:#00c8b4,color:#f6f7f8;
    classDef testing fill:#1d232b,stroke:#b8b8ff,color:#f6f7f8;
    classDef dx fill:#261f19,stroke:#ffd166,color:#f6f7f8;
    classDef ops fill:#272226,stroke:#ffb88c,color:#f6f7f8;
    classDef decision fill:#202c22,stroke:#8de2b5,color:#f6f7f8;
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
        for item in SECTIONS
    )
    return f"""
<section class='concept-section reference-section' id='dependency-table' data-title='Comparison DAG & Dependency Table' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 2 &middot; Comparison DAG</div>
  <h2>Django vs Flask vs FastAPI Comparison DAG</h2>
  <p>The document order follows this dependency graph. Each comparison dimension appears only after the reader has the background needed to judge it correctly.</p>
  <div class='diagram-actions'><button class='diagram-action dag-download-btn' type='button' aria-label='Download framework comparison DAG'>Download DAG</button></div>
  <div class='er-diagram'><div class='mermaid-diagram'>{escape(render_dag())}</div></div>
  <h3>All 36 Comparison Dimensions</h3>
  <div class='table-wrap'><table class='comparison-table'><thead><tr><th>ID</th><th>Dimension</th><th>Layer</th><th>Prerequisites</th><th>Dependents</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
"""


def render_decision_tree():
    diagram = """
flowchart TD
    A[Need full stack product with admin templates and auth] -->|Yes| D1[Django]
    A -->|No| B[Primary deliverable is API or service]
    B -->|No| B2[Mostly HTML pages and forms]
    B2 -->|Yes| D2[Django]
    B2 -->|No| C[Need minimal custom internal tool]
    C -->|Yes| D3[Flask]
    C -->|No| D4[Reevaluate product scope]
    B -->|Yes| E[Need high concurrency for IO heavy traffic]
    E -->|Yes| F[Team understands async and event loop]
    E -->|No| G[Need mature full stack integrations too]
    G -->|Yes| D5[Django with DRF]
    G -->|No| H[Prefer smallest controllable surface area]
    H -->|Yes| D6[Flask]
    H -->|No| D7[FastAPI]
    F -->|No| I[Need fastest time to competent delivery]
    F -->|Yes| J[Serving ML models or data APIs]
    I -->|Yes| K[Need batteries for auth admin and permissions]
    I -->|No| L[Existing Flask expertise on team]
    K -->|Yes| D8[Django]
    K -->|No| D9[Flask]
    L -->|Yes| D10[Flask]
    L -->|No| D11[Invest in FastAPI]
    J -->|Yes| D12[FastAPI]
    J -->|No| M[Need WebSockets or large concurrent fanout]
    M -->|Yes| N[Need Redis backed pub sub built in]
    M -->|No| O[Is strict schema validation a top priority]
    N -->|Yes| D13[Django Channels]
    N -->|No| D14[FastAPI]
    O -->|Yes| D15[FastAPI]
    O -->|No| P[Need email password flows and back office soon]
    P -->|Yes| D16[Django]
    P -->|No| Q[Microservice in larger platform]
    Q -->|Yes| R[Mostly sync CRUD and small team]
    Q -->|No| S[Low traffic API and team knows Flask]
    R -->|Yes| D17[Flask or FastAPI]
    R -->|No| D18[FastAPI]
    S -->|Yes| D19[Flask]
    S -->|No| T[Need strongest OpenAPI and client generation]
    T -->|Yes| D20[FastAPI]
    T -->|No| U[Need CMS content workflows]
    U -->|Yes| D21[Django]
    U -->|No| V[Need serverless friendly cold starts]
    V -->|Yes| D22[FastAPI or Flask]
    V -->|No| W[Team is junior and needs guardrails]
    W -->|Yes| D23[Django]
    W -->|No| D24[Choose by existing stack fit]
    class D1,D2,D5,D8,D13,D16,D21,D23 django;
    class D3,D6,D9,D10,D17,D19,D22 flask;
    class D7,D11,D12,D14,D15,D18,D20,D22 fastapi;
    class D4,D24 neutral;
    classDef django fill:#0C4B33,stroke:#84d2a9,color:#f6f7f8;
    classDef flask fill:#C0392B,stroke:#ffb3aa,color:#f6f7f8;
    classDef fastapi fill:#009688,stroke:#8ef7ec,color:#f6f7f8;
    classDef neutral fill:#2a2f35,stroke:#9aa4af,color:#f6f7f8;
"""
    return f"""
<section class='concept-section reference-section' id='decision-tree' data-title='Decision Tree' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 2 &middot; Decision Tree</div>
  <h2>Framework Selection Decision Tree</h2>
  <p>This is the elimination path the rest of the document justifies. It is deliberately opinionated, but every branch is grounded in the evidence covered by the CM sections.</p>
  <div class='mermaid-wrap'><div class='mermaid-diagram'>{escape(diagram)}</div></div>
</section>
"""


def render_request_sequence():
    diagram = """
sequenceDiagram
    participant C as Client
    participant DJ as Django stack
    participant FL as Flask stack
    participant FA as FastAPI stack
    participant DB as Database
    C->>DJ: POST users JSON
    DJ->>DJ: middleware session csrf auth
    DJ->>DJ: serializer validation
    DJ->>DB: ORM insert
    DB-->>DJ: row persisted
    DJ-->>C: JSON response
    C->>FL: POST users JSON
    FL->>FL: route function extension hooks
    FL->>FL: schema validation if installed
    FL->>DB: SQLAlchemy insert
    DB-->>FL: row persisted
    FL-->>C: JSON response
    C->>FA: POST users JSON
    FA->>FA: dependency graph and Pydantic validation
    FA->>DB: async session insert
    DB-->>FA: row persisted
    FA-->>C: filtered response model
"""
    return f"""
<section class='concept-section reference-section' id='request-sequence' data-title='Same Request in All 3' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 2 &middot; Request Path</div>
  <h2>Identical Request in Django, Flask, and FastAPI</h2>
  <p>The same endpoint reveals where each framework adds value and overhead: Django does more before your code runs, Flask does less, and FastAPI invests early in validation and contract generation.</p>
  <div class='mermaid-wrap'><div class='mermaid-diagram'>{escape(diagram)}</div></div>
</section>
"""


def render_ecosystem_diagram():
    diagram = """
flowchart LR
    DJ[Django core] --> DJ1[Admin core]
    DJ --> DJ2[Auth core]
    DJ --> DJ3[ORM core]
    DJ --> DJ4[Templates core]
    DJ --> DJ5[Forms core]
    DJ --> DJ6[Migrations core]
    DJ --> DJ7[Sessions core]
    DJ --> DJ8[Security middleware core]
    DJ --> DJ9[DRF community]
    DJ --> DJ10[Channels community]
    DJ --> DJ11[Celery community]
    DJ --> DJ12[allauth community]
    DJ --> DJ13[Wagtail community]
    FL[Flask core] --> FL1[Routing core]
    FL --> FL2[Jinja templates core]
    FL --> FL3[SQLAlchemy community]
    FL --> FL4[Flask Login community]
    FL --> FL5[Flask WTF community]
    FL --> FL6[Flask Admin community]
    FL --> FL7[Flask Smorest community]
    FL --> FL8[Flask Caching community]
    FL --> FL9[Flask Mail community]
    FA[FastAPI core] --> FA1[Starlette dependency]
    FA --> FA2[Pydantic dependency]
    FA --> FA3[OpenAPI docs core]
    FA --> FA4[SQLAlchemy community]
    FA --> FA5[Alembic community]
    FA --> FA6[fastapi users community]
    FA --> FA7[slowapi community]
    FA --> FA8[fastapi cache2 community]
    FA --> FA9[prometheus instrumentator]
    class DJ,DJ1,DJ2,DJ3,DJ4,DJ5,DJ6,DJ7,DJ8,DJ9,DJ10,DJ11,DJ12,DJ13 django;
    class FL,FL1,FL2,FL3,FL4,FL5,FL6,FL7,FL8,FL9 flask;
    class FA,FA1,FA2,FA3,FA4,FA5,FA6,FA7,FA8,FA9 fastapi;
    classDef django fill:#0C4B33,stroke:#84d2a9,color:#f6f7f8;
    classDef flask fill:#C0392B,stroke:#ffb3aa,color:#f6f7f8;
    classDef fastapi fill:#009688,stroke:#8ef7ec,color:#f6f7f8;
"""
    return f"""
<section class='concept-section reference-section' id='ecosystem-diagram' data-title='Framework Ecosystem' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 2 &middot; Ecosystem</div>
  <h2>Ecosystem Shape</h2>
  <p>Django owns more of the stack itself, Flask delegates quickly to extensions, and FastAPI stands on Starlette plus Pydantic while relying on surrounding libraries for everything beyond the API core.</p>
  <div class='mermaid-wrap'><div class='mermaid-diagram'>{escape(diagram)}</div></div>
</section>
"""


def render_project_matrix():
    verdict_order = {"django": "Django wins", "flask": "Flask wins", "fastapi": "FastAPI wins", "conditional": "Depends"}

    def cells_for(verdict):
        if verdict == "django":
            return ("✓✓✓", "✓", "✗")
        if verdict == "flask":
            return ("✓", "✓✓✓", "✓")
        if verdict == "fastapi":
            return ("✓", "✓", "✓✓✓")
        return ("✓✓", "✓✓", "✓✓")

    rows = []
    for name, verdict, complexity, ref in PROJECT_MATRIX:
        dj, fl, fa = cells_for(verdict)
        rows.append(
            "<tr "
            f"data-name='{escape(name.lower())}' "
            f"data-verdict='{escape(verdict)}' "
            f"data-complexity='{complexity}' "
            f"data-ref='{escape(ref)}'>"
            f"<td>{escape(name)}</td>"
            f"<td class='framework-django'>{dj}</td>"
            f"<td class='framework-flask'>{fl}</td>"
            f"<td class='framework-fastapi'>{fa}</td>"
            f"<td><span class='winner-badge {VERDICT_CLASS[verdict]}'>{escape(verdict_order[verdict])}</span></td>"
            f"<td><a href='#{escape(ref)}'>{escape(ref)}</a></td>"
            "</tr>"
        )
    sort_controls = (
        "<div class='matrix-sort'>"
        "<button class='sort-btn is-active' type='button' data-sort='alphabetical'>Alphabetical</button>"
        "<button class='sort-btn' type='button' data-sort='verdict'>By verdict</button>"
        "<button class='sort-btn' type='button' data-sort='complexity'>By complexity</button>"
        "</div>"
    )
    return f"""
<section class='concept-section reference-section' id='project-matrix' data-title='Project Type Matrix' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 10 &middot; Matrix</div>
  <h2>Project Type to Framework Matrix</h2>
  <p>This table compresses the comparison into a quick decision surface. Use it for triage, not for skipping the rationale behind the verdicts.</p>
  {sort_controls}
  <div class='table-wrap'><table class='comparison-table project-matrix-table'><thead><tr><th>Project Type</th><th class='framework-django'>Django</th><th class='framework-flask'>Flask</th><th class='framework-fastapi'>FastAPI</th><th>Verdict</th><th>Evidence</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</section>
"""


def render_master_summary():
    cards = [
        (
            "django",
            "Choose Django when the product is bigger than the API. If you need admin, mature auth, permissions, templates, ORM, migrations, and team guardrails, Django turns years of platform engineering into configuration. The hidden cost is weight: more startup, more memory, and more framework surface area to understand.",
        ),
        (
            "flask",
            "Choose Flask when deliberate minimalism is a feature, not an accident. It stays valuable for small services, custom internal tools, and teams that already know exactly which extensions and architecture rules they want. The hidden cost is governance: if nobody enforces structure, Flask becomes a pile of local conventions quickly.",
        ),
        (
            "fastapi",
            "Choose FastAPI when the main deliverable is a typed API and concurrency actually matters. FastAPI shines for async I O heavy services, ML inference APIs, and teams that want validation and OpenAPI docs generated directly from code. The hidden cost is everything outside the API core: admin, browser auth flows, and async expertise are still your problem.",
        ),
    ]
    body = "".join(
        f"<article class='summary-card framework-{name}'><h3>{framework_badge(name)} {escape(FRAMEWORK_LABELS[name])}</h3><p>{escape(text)}</p></article>"
        for name, text in cards
    )
    return f"""
<section class='concept-section reference-section' id='master-summary' data-title='The One-Paragraph Answer' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 10 &middot; Summary</div>
  <h2>The One-Paragraph Answer</h2>
  <div class='summary-grid'>{body}</div>
</section>
"""


def render_score_cards():
    justifications = {
        "django": "Best when product breadth matters more than raw minimalism.",
        "flask": "Best when you want a thin layer and already know your architecture discipline.",
        "fastapi": "Best when async APIs, typed contracts, and testability are the main job.",
    }
    cards = []
    for framework in FRAMEWORKS:
        rows = []
        for label, score in SCORE_CARDS[framework]:
            dots = "".join(
                f"<span class='score-dot{' is-filled' if index < score else ''}'></span>"
                for index in range(5)
            )
            rows.append(
                f"<div class='score-row'><span>{escape(label)}</span><span class='score-dots'>{dots}</span></div>"
            )
        cards.append(
            f"<article class='score-card framework-{framework}'><h3>{framework_badge(framework)} {escape(FRAMEWORK_LABELS[framework])}</h3><p>{escape(justifications[framework])}</p>{''.join(rows)}</article>"
        )
    return f"""
<section class='concept-section reference-section' id='score-cards' data-title='Framework Score Cards' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 10 &middot; Score Cards</div>
  <h2>Framework Score Cards</h2>
  <div class='score-grid'>{''.join(cards)}</div>
</section>
"""


def render_interview_questions():
    items = "".join(
        f"<details class='qa-item'><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>"
        for question, answer in INTERVIEW_QA
    )
    return f"""
<section class='concept-section reference-section' id='interview-questions' data-title='Interview Questions' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 10 &middot; Interview Questions</div>
  <h2>Common Interview Questions</h2>
  <div class='qa-grid'>{items}</div>
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
        for item in SECTIONS
    )
    return f"""
<section class='concept-section reference-section quick-reference' id='quick-reference' data-title='Quick Reference' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 10 &middot; Quick Reference</div>
  <h2>CM01-CM36 At A Glance</h2>
  <div class='table-wrap'><table class='comparison-table'><thead><tr><th>ID</th><th>Layer</th><th>Dimension</th><th>One-line Summary</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
"""


def render_recommended_reading():
    items = "".join(
        f"<li><a href='{escape(url)}' target='_blank' rel='noreferrer'>{escape(label)}</a></li>"
        for label, url in READING
    )
    return f"""
<section class='concept-section reference-section' id='recommended-reading' data-title='Recommended Reading' data-frameworks='django flask fastapi' data-modes='api full-stack ml'>
  <div class='section-kicker'>Task 10 &middot; Reading</div>
  <h2>Recommended Reading</h2>
  <p>These are the sources worth keeping open while you use this comparison: official docs first, then benchmarking methodology and ecosystem documentation where trade-offs get concrete.</p>
  <ul class='reading-list'>{items}</ul>
</section>
"""


def render_nav():
    by_layer = defaultdict(list)
    for item in SECTIONS:
        by_layer[item["layer"]].append(item)
    parts = [
        "<section class='nav-group' data-layer='ref'>"
        "<button class='group-toggle' type='button' data-layer='R' aria-expanded='true'><span>References</span><span>&#9662;</span></button>"
        "<div class='group-links'>"
        + "".join(
            f"<a href='#{target}' data-id='{target}' data-frameworks='django flask fastapi' data-modes='api full-stack ml' data-reference='true'><span class='nav-dot'>R</span><span>{escape(label)}</span></a>"
            for target, label in REFERENCE_SECTIONS
        )
        + "</div></section>"
    ]
    for layer in sorted(LAYER_NAMES):
        links = "".join(
            f"<a href='#{item['id']}' data-id='{item['id']}' data-frameworks='{' '.join(item['frameworks'])}' data-modes='{' '.join(item['modes'])}'><span class='nav-dot'>{layer}</span><span>{escape(item['id'])} &middot; {escape(item['title'])}</span></a>"
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
<link href='https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inconsolata:wght@400;600;700&family=Libre+Baskerville:wght@400;700&display=swap' rel='stylesheet'>
<link id='darkThemeStylesheet' rel='stylesheet' href='styles-dark.css'>
<link id='lightThemeStylesheet' rel='stylesheet' href='styles-light.css' media='not all'>
<link rel='preload' href='styles.css' as='style'>
<link rel='stylesheet' href='styles.css'>
<style>
html[data-theme='dark'] {{ --void:#111318; --obsidian:#171b21; --deep:#1c2027; --surface:#20252d; --surface2:#262c35; --surface3:#2f3641; --text-1:#f2eee8; --text-2:#c6c1b7; --framework-django:#0C4B33; --framework-flask:#C0392B; --framework-fastapi:#009688; --framework-neutral:#7bb1ff; --font-head:'Bebas Neue',sans-serif; --font-body:'Libre Baskerville',serif; --font-code:'Inconsolata',monospace; background:#111318; color:var(--text-1); }}
html[data-theme='light'] {{ --paper:#f7f5f1; --paper2:#efebe5; --surface:#ffffff; --surface2:#f5f1ea; --surface3:#eae4db; --text-1:#1f1d1a; --text-2:#5a554d; --framework-django:#0C4B33; --framework-flask:#C0392B; --framework-fastapi:#009688; --framework-neutral:#345d8f; --font-head:'Bebas Neue',sans-serif; --font-body:'Libre Baskerville',serif; --font-code:'Inconsolata',monospace; background:#f7f5f1; color:var(--text-1); }}
.sidebar-tools{{display:grid;gap:.85rem;margin-top:.8rem}} .tool-panel,.hero-card,.comparison-box,.callout,.approach-card,.mermaid-wrap,.er-diagram,.summary-card,.score-card,.qa-item,.svg-chart,.spectrum-box{{border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:1rem;background:rgba(255,255,255,.025)}} html[data-theme='light'] .tool-panel,html[data-theme='light'] .hero-card,html[data-theme='light'] .comparison-box,html[data-theme='light'] .callout,html[data-theme='light'] .approach-card,html[data-theme='light'] .mermaid-wrap,html[data-theme='light'] .er-diagram,html[data-theme='light'] .summary-card,html[data-theme='light'] .score-card,html[data-theme='light'] .qa-item,html[data-theme='light'] .svg-chart,html[data-theme='light'] .spectrum-box{{border-color:rgba(31,29,26,.12);background:rgba(255,255,255,.82)}}
.tool-title,.chart-title,.spectrum-title{{font-family:var(--font-code);font-size:.76rem;letter-spacing:.12em;text-transform:uppercase;color:var(--text-2)}}
.filter-strip{{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.55rem}} .framework-filter,.sort-btn,.diagram-action{{appearance:none;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);color:inherit;padding:.55rem .8rem;border-radius:999px;cursor:pointer;font:600 .76rem var(--font-code)}} html[data-theme='light'] .framework-filter,html[data-theme='light'] .sort-btn,html[data-theme='light'] .diagram-action{{border-color:rgba(31,29,26,.14);background:rgba(31,29,26,.04)}} .framework-filter.is-active,.sort-btn.is-active{{box-shadow:inset 0 0 0 1px currentColor}} .framework-filter[data-framework='django'].is-active{{color:#8de2b5}} .framework-filter[data-framework='flask'].is-active{{color:#ffb3aa}} .framework-filter[data-framework='fastapi'].is-active{{color:#8ef7ec}}
.sidebar-nav .group-links a{{display:grid;grid-template-columns:auto 1fr;gap:.6rem;align-items:start;transition:opacity .18s ease,border-color .18s ease,transform .18s ease}} .nav-dot{{display:inline-flex;align-items:center;justify-content:center;min-width:1.5rem;height:1.5rem;border-radius:999px;font-size:.68rem;font-family:var(--font-code);border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04)}} html[data-theme='light'] .nav-dot{{border-color:rgba(31,29,26,.16);background:rgba(31,29,26,.05)}}
.lead{{font-size:1.03rem}} .hero-grid{{display:grid;grid-template-columns:1.25fr .95fr;gap:1.2rem;align-items:start}} .hero-meta{{display:grid;gap:1rem}} .hero-stats{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem}} .stat-card{{border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:.9rem;background:rgba(255,255,255,.03)}} html[data-theme='light'] .stat-card{{border-color:rgba(31,29,26,.12);background:rgba(31,29,26,.03)}} .stat-label{{font:400 .72rem var(--font-code);letter-spacing:.08em;text-transform:uppercase;color:var(--text-2)}} .stat-value{{font:700 1.2rem var(--font-head);letter-spacing:.04em}}
.section-meta,.forward-links{{display:flex;flex-wrap:wrap;gap:.7rem 1rem;align-items:center;margin:.75rem 0 1rem}} .forward-links>div{{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}} .meta-label{{font:600 .74rem var(--font-code);letter-spacing:.08em;text-transform:uppercase;color:var(--text-2)}}
.badge,.framework-badge,.winner-badge,.cluster-pill{{display:inline-flex;align-items:center;border-radius:999px;padding:.22rem .62rem;font-family:var(--font-code);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;text-decoration:none}} .badge{{border:1px solid rgba(255,255,255,.12);color:inherit}} .badge.subtle{{opacity:.7}} html[data-theme='light'] .badge{{border-color:rgba(31,29,26,.14)}}
.framework-badge.framework-django,.framework-django{{color:var(--framework-django)}} .framework-badge.framework-flask,.framework-flask{{color:var(--framework-flask)}} .framework-badge.framework-fastapi,.framework-fastapi{{color:var(--framework-fastapi)}}
.framework-code-label{{display:inline-flex;align-items:center;border-radius:999px;padding:.18rem .55rem;border:1px solid currentColor;font:600 .74rem var(--font-code);margin-bottom:.6rem}}
.winner-badge.winner-django{{background:rgba(12,75,51,.14);color:#8de2b5}} .winner-badge.winner-flask{{background:rgba(192,57,43,.14);color:#ffb3aa}} .winner-badge.winner-fastapi{{background:rgba(0,150,136,.14);color:#8ef7ec}} .winner-badge.winner-tie{{background:rgba(255,209,102,.16);color:#ffd166}} .winner-badge.winner-conditional{{background:rgba(123,177,255,.16);color:#b6d1ff}} html[data-theme='light'] .winner-badge{{color:var(--text-1)}}
.cluster-pill{{border:1px solid rgba(255,255,255,.12)}} html[data-theme='light'] .cluster-pill{{border-color:rgba(31,29,26,.14)}} .cluster-architecture{{background:rgba(123,177,255,.12)}} .cluster-performance{{background:rgba(0,229,255,.1)}} .cluster-data{{background:rgba(159,232,112,.1)}} .cluster-auth{{background:rgba(255,155,143,.12)}} .cluster-async{{background:rgba(0,200,180,.12)}} .cluster-testing{{background:rgba(184,184,255,.12)}} .cluster-dx{{background:rgba(255,209,102,.12)}} .cluster-ops{{background:rgba(255,184,140,.12)}} .cluster-decision{{background:rgba(141,226,181,.12)}}
.approach-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}} .approach-card{{display:grid;gap:.7rem}} .approach-card h4{{margin:0}}
.tab-buttons{{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.8rem}} .tab-btn{{appearance:none;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);color:inherit;border-radius:999px;padding:.45rem .7rem;cursor:pointer;font:600 .74rem var(--font-code)}} .tab-btn.is-active{{transform:translateY(-1px)}} html[data-theme='light'] .tab-btn{{border-color:rgba(31,29,26,.14);background:rgba(31,29,26,.04)}} .tab-panel{{display:none}} .tab-panel.is-active{{display:block}}
.comparison-table-wrap td,.comparison-table td,.comparison-table th{{vertical-align:top}} .comparison-table .framework-django,.project-matrix-table .framework-django{{color:var(--framework-django)}} .comparison-table .framework-flask,.project-matrix-table .framework-flask{{color:var(--framework-flask)}} .comparison-table .framework-fastapi,.project-matrix-table .framework-fastapi{{color:var(--framework-fastapi)}}
.verdict-box{{display:grid;gap:.7rem}} .fact-box{{border-left:4px solid var(--framework-neutral)}} .opinion-box{{border-left:4px solid #ffd166}} .data-box{{border-left:4px solid var(--framework-fastapi)}}
.spectrum-track{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.8rem;margin-top:.8rem;position:relative}} .spectrum-track::before{{content:'';position:absolute;left:0;right:0;top:50%;height:6px;border-radius:999px;background:linear-gradient(90deg,var(--framework-flask),var(--framework-fastapi),var(--framework-django));transform:translateY(-50%)}} .spectrum-stop{{position:relative;z-index:1;justify-self:center;display:inline-flex;padding:.35rem .7rem;border-radius:999px;background:var(--surface);border:1px solid rgba(255,255,255,.12);font:700 .8rem var(--font-code)}} html[data-theme='light'] .spectrum-stop{{border-color:rgba(31,29,26,.14)}}
.svg-chart svg{{width:100%;height:auto}} .chart-label,.chart-value{{font:600 13px var(--font-code);fill:currentColor}}
.chart-bar.framework-django{{fill:var(--framework-django)}} .chart-bar.framework-flask{{fill:var(--framework-flask)}} .chart-bar.framework-fastapi{{fill:var(--framework-fastapi)}}
.summary-grid,.score-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}} .summary-card,.score-card{{display:grid;gap:.65rem}} .score-row{{display:flex;justify-content:space-between;gap:1rem;align-items:center;font-size:.92rem}} .score-dots{{display:inline-flex;gap:.28rem}} .score-dot{{width:11px;height:11px;border-radius:999px;border:1px solid rgba(255,255,255,.18);background:transparent}} html[data-theme='light'] .score-dot{{border-color:rgba(31,29,26,.18)}} .score-dot.is-filled{{background:currentColor;border-color:currentColor}}
.qa-grid{{display:grid;gap:.8rem}} .qa-item summary{{cursor:pointer;font-weight:700}} .qa-item p{{margin:.85rem 0 0}}
.reading-list{{display:grid;gap:.45rem;padding-left:1.1rem}} .reading-list a{{word-break:break-word}}
.matrix-sort{{display:flex;flex-wrap:wrap;gap:.45rem;margin-bottom:.9rem}} .project-matrix-table tbody tr{{transition:background .18s ease}}
.section-footer{{display:flex;justify-content:space-between;gap:1rem;margin-top:1.4rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,.08)}} html[data-theme='light'] .section-footer{{border-color:rgba(31,29,26,.1)}}
.diagram-actions{{display:flex;justify-content:flex-end;margin:.85rem 0 1rem}} .layer-skeleton{{height:320px;border-radius:14px;background:linear-gradient(90deg,rgba(255,255,255,.03) 25%,rgba(255,255,255,.07) 50%,rgba(255,255,255,.03) 75%);background-size:200% 100%;animation:skeleton-sweep 1.4s ease infinite;border:1px solid rgba(255,255,255,.06);margin-bottom:1.4rem}} @keyframes skeleton-sweep{{0%{{background-position:200% 0}}100%{{background-position:-200% 0}}}}
body[data-framework-focus='django'] [data-frameworks*='django']{{box-shadow:0 0 0 1px rgba(12,75,51,.42)}} body[data-framework-focus='flask'] [data-frameworks*='flask']{{box-shadow:0 0 0 1px rgba(192,57,43,.42)}} body[data-framework-focus='fastapi'] [data-frameworks*='fastapi']{{box-shadow:0 0 0 1px rgba(0,150,136,.42)}}
body[data-framework-focus='django'] .approach-card:not(.framework-django),body[data-framework-focus='django'] .tab-btn:not(.framework-django){{opacity:.58}} body[data-framework-focus='flask'] .approach-card:not(.framework-flask),body[data-framework-focus='flask'] .tab-btn:not(.framework-flask){{opacity:.58}} body[data-framework-focus='fastapi'] .approach-card:not(.framework-fastapi),body[data-framework-focus='fastapi'] .tab-btn:not(.framework-fastapi){{opacity:.58}}
@media (max-width:1180px){{.hero-grid,.approach-grid,.summary-grid,.score-grid{{grid-template-columns:1fr}} .hero-stats{{grid-template-columns:1fr}}}}
@media (max-width:900px){{.section-footer{{flex-direction:column}}}}
</style>
<!-- REVIEW: Keep this inline theme bootstrap in <head>; moving it to the end of <body> would cause the wrong theme to flash before styles apply. -->
<script>
try {{
  const savedTheme = localStorage.getItem('framework-comparison-theme');
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
    <div class='sidebar-tools'>
      <div class='tool-panel'>
        <div class='tool-title'>Framework Focus</div>
        <div class='filter-strip'>
          <button class='framework-filter' type='button' data-framework='django' aria-pressed='false'>Django</button>
          <button class='framework-filter' type='button' data-framework='flask' aria-pressed='false'>Flask</button>
          <button class='framework-filter' type='button' data-framework='fastapi' aria-pressed='false'>FastAPI</button>
        </div>
      </div>
    </div>
  </div>
  <nav class='sidebar-nav' aria-label='Framework comparison navigation'>{render_nav()}</nav>
</aside>
<main>
<!-- TASK-1 START -->
<section class='hero' id='top'>
  <div class='section-kicker'>Python Web Framework Comparison Reference</div>
  <div class='hero-grid'>
    <div>
      <h1>{SUBTITLE}</h1>
      <p>This document assumes Python basics only and compares Django, Flask, and FastAPI from first principles: philosophy, request lifecycle, data layer, APIs, auth, performance, async, operations, and the cost of being wrong.</p>
      <p>The point is not to crown a universal winner. It is to make the framework choice defensible for the actual business problem, the actual team, and the actual future change requests that usually arrive three months too late.</p>
      <div class='hero-stats'>
        <div class='stat-card'><div class='stat-label'>Dimensions</div><div class='stat-value'>36</div></div>
        <div class='stat-card'><div class='stat-label'>Frameworks</div><div class='stat-value'>3</div></div>
        <div class='stat-card'><div class='stat-label'>Versions</div><div class='stat-value'>4.2 / 3.x / 0.110+</div></div>
      </div>
    </div>
    <div class='hero-meta'>
      <div class='hero-card'>
        <h3>Version Baseline</h3>
        {render_pre(VERSION_BASELINE, "text")}
      </div>
      <div class='hero-card'>
        <h3>Read This Like An Engineer</h3>
        <p>Start with the DAG and decision tree, then validate the verdict against the sections that matter most for your project: auth, admin, API throughput, async, or deployment simplicity.</p>
      </div>
    </div>
  </div>
</section>
<!-- TASK-1 END -->
<div id='sectionMount' hidden aria-hidden='true'></div>
<!-- TASK-2 START -->
{render_dependency_table(dependents)}
{render_decision_tree()}
{render_request_sequence()}
{render_ecosystem_diagram()}
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
  const backToTop = document.getElementById('backToTop');
  const darkThemeStylesheet = document.getElementById('darkThemeStylesheet');
  const lightThemeStylesheet = document.getElementById('lightThemeStylesheet');
  const themeButtons = [...document.querySelectorAll('.theme-option')];
  const frameworkButtons = [...document.querySelectorAll('.framework-filter')];
  const main = document.querySelector('main');
  const sectionMount = document.getElementById('sectionMount');
  const virtualSections = [...document.querySelectorAll("main .concept-section[id]")];
  const sectionMarkupById = new Map(virtualSections.map((section) => [section.id, { id: section.id, html: section.outerHTML }]));
  const orderedIds = navLinks.map((link) => link.dataset.id).filter(Boolean);
  const sectionIdSet = new Set(sectionMarkupById.keys());
  const THEME_STORAGE_KEY = 'framework-comparison-theme';
  let currentTheme = window.__initialTheme === 'light' ? 'light' : 'dark';
  let currentSectionId = virtualSections[0]?.id || orderedIds[0] || '';
  let activeObserver = null;
  let renderToken = 0;
  let mermaidRenderToken = 0;
  let frameworkFocus = '';
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
  function syncFrameworkButtons() {
    frameworkButtons.forEach((button) => {
      const active = button.dataset.framework === frameworkFocus;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    if (frameworkFocus) {
      document.body.dataset.frameworkFocus = frameworkFocus;
    } else {
      delete document.body.dataset.frameworkFocus;
    }
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
    link.download = 'framework-comparison-dag.svg';
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
  function bindProjectMatrixSorting(root) {
    root.querySelectorAll('.project-matrix-table').forEach((table) => {
      const tbody = table.querySelector('tbody');
      const buttons = [...root.querySelectorAll('.sort-btn')];
      buttons.forEach((button) => {
        if (button.dataset.sortBound === 'true') return;
        button.addEventListener('click', () => {
          const mode = button.dataset.sort || 'alphabetical';
          buttons.forEach((candidate) => {
            const active = candidate === button;
            candidate.classList.toggle('is-active', active);
            candidate.setAttribute('aria-pressed', String(active));
          });
          const rows = [...tbody.querySelectorAll('tr')];
          const verdictRank = { django: 0, fastapi: 1, flask: 2, conditional: 3 };
          rows.sort((a, b) => {
            if (mode === 'complexity') {
              return Number(a.dataset.complexity || 0) - Number(b.dataset.complexity || 0);
            }
            if (mode === 'verdict') {
              return (verdictRank[a.dataset.verdict || 'conditional'] ?? 9) - (verdictRank[b.dataset.verdict || 'conditional'] ?? 9);
            }
            return (a.dataset.name || '').localeCompare(b.dataset.name || '');
          });
          rows.forEach((row) => tbody.appendChild(row));
        });
        button.dataset.sortBound = 'true';
      });
    });
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
    bindProjectMatrixSorting(section);
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
  bindProjectMatrixSorting(document);
  queueMermaidRender(document);
  virtualSections.forEach((section) => { if (section.id !== currentSectionId) section.remove(); });
  if (currentSectionId) setActiveNavLink(currentSectionId);
  observeTrackedSections();
  syncThemeButtons(currentTheme);
  syncFrameworkButtons();
  themeButtons.forEach((button) => button.addEventListener('click', () => applyTheme(button.dataset.theme || 'dark')));
  frameworkButtons.forEach((button) => {
    button.addEventListener('click', () => {
      frameworkFocus = frameworkFocus === button.dataset.framework ? '' : (button.dataset.framework || '');
      syncFrameworkButtons();
    });
  });
  document.querySelectorAll('.group-toggle').forEach((button) => {
    button.addEventListener('click', () => {
      const collapsed = button.parentElement.classList.toggle('collapsed');
      button.setAttribute('aria-expanded', String(!collapsed));
    });
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
});
</script>
</body>
</html>
"""


def build_document() -> str:
    validate_graph()
    dependents = build_dependents()
    task_close_markers = {
        "CM03": "<!-- TASK-3 END -->\n<!-- TASK-4 START -->",
        "CM07": "<!-- TASK-4 END -->\n<!-- TASK-5 START -->",
        "CM10": "<!-- TASK-5 END -->\n<!-- TASK-6 START -->",
        "CM16": "<!-- TASK-6 END -->\n<!-- TASK-7 START -->",
        "CM20": "<!-- TASK-7 END -->\n<!-- TASK-8 START -->",
        "CM29": "<!-- TASK-8 END -->\n<!-- TASK-9 START -->",
        "CM36": "<!-- TASK-9 END -->",
    }
    sections = ["<!-- TASK-3 START -->"]
    for index, item in enumerate(SECTIONS):
        sections.append(render_section(item, dependents, index))
        marker = task_close_markers.get(item["id"])
        if marker:
            sections.append(marker)
    appendix = (
        "<!-- TASK-10 START -->"
        + render_project_matrix()
        + render_master_summary()
        + render_score_cards()
        + render_interview_questions()
        + render_quick_reference()
        + render_recommended_reading()
        + "<!-- TASK-10 END -->"
    )
    return render_shell(dependents) + "".join(sections) + appendix + tail_script()


def main() -> None:
    OUTFILE.write_text(build_document(), encoding="utf-8")
    print(f"Wrote {OUTFILE}")


if __name__ == "__main__":
    main()
