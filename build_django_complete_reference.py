from __future__ import annotations

from collections import defaultdict
from html import escape
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
OUTFILE = ROOT / "django_complete_reference.html"

LAYER_NAMES = {
    0: "Web Foundations",
    1: "Models & Database",
    2: "URLs & Views",
    3: "Templates",
    4: "Forms",
    5: "Authentication & Authorization",
    6: "REST API",
    7: "Caching, Signals & Async Work",
    8: "Admin, Commands & Apps",
    9: "Testing",
    10: "Performance, Security & Deployment",
}

NAV_LABELS = {
    0: "Layer 0: Web & Django Foundations",
    1: "Layer 1: Models & Database",
    2: "Layer 2: URLs & Views",
    3: "Layer 3: Templates",
    4: "Layer 4: Forms",
    5: "Layer 5: Auth & Sessions",
    6: "Layer 6: Django REST Framework",
    7: "Layer 7: Caching, Signals, Celery",
    8: "Layer 8: Admin, Commands, Apps",
    9: "Layer 9: Testing",
    10: "Layer 10: Performance & Deployment",
}

CLUSTER_CLASS = {
    "foundation": "cluster-foundation",
    "orm": "cluster-orm",
    "views": "cluster-views",
    "templates": "cluster-templates",
    "forms": "cluster-forms",
    "auth": "cluster-auth",
    "rest": "cluster-rest",
    "async": "cluster-async",
    "admin": "cluster-admin",
    "testing": "cluster-testing",
    "ops": "cluster-ops",
}

REFERENCE_SECTIONS = [
    ("dependency-table", "Concept DAG & Dependencies"),
    ("request-lifecycle", "Request / Response Lifecycle"),
    ("ecosystem-map", "Django Ecosystem Map"),
    ("quick-reference", "Quick Reference"),
]

REQUEST_SEQUENCE = """
sequenceDiagram
    participant Browser
    participant DNS
    participant Proxy as Reverse Proxy
    participant Adapter as WSGI / ASGI
    participant Middleware
    participant Router
    participant View
    participant ORM
    participant DB

    Browser->>DNS: Resolve blog.example.com
    DNS-->>Browser: IP address
    Browser->>Proxy: HTTPS GET /articles/42/
    Proxy->>Adapter: Forward request bytes
    Adapter->>Middleware: Build HttpRequest
    Middleware->>Router: Pass request through stack
    Router->>View: Resolve URL + kwargs
    View->>ORM: Query models
    ORM->>DB: SQL
    DB-->>ORM: Rows
    ORM-->>View: Objects / values
    View-->>Middleware: HttpResponse
    Middleware-->>Adapter: Response with headers/cookies
    Adapter-->>Proxy: HTTP response bytes
    Proxy-->>Browser: Final response
"""


def x(title, body, *, code=None, lang="python", compare=None, diagram=None, sql=None, observe=""):
    return {
        "title": title,
        "body": body,
        "code": code,
        "lang": lang,
        "compare": compare,
        "diagram": diagram,
        "sql": sql,
        "observe": observe,
    }


def c(
    id,
    layer,
    cluster,
    title,
    prereqs,
    quick,
    problem,
    mental,
    learn,
    design,
    avoid,
    interview,
    docs,
    sample,
    *,
    sample_lang="python",
    comparison=None,
    diagram=None,
    mistakes=None,
    version=None,
    extras=None,
    sample_sql=None,
):
    return {
        "id": id,
        "layer": layer,
        "cluster": cluster,
        "title": title,
        "prereqs": prereqs,
        "quick": quick,
        "problem": problem,
        "mental": mental,
        "learn": learn,
        "design": design,
        "avoid": avoid,
        "interview": interview,
        "docs": docs,
        "sample": sample,
        "sample_lang": sample_lang,
        "comparison": comparison or [("Without Django", problem), ("Django way", design)],
        "diagram": diagram,
        "mistakes": mistakes or [
            ("Using the feature without understanding the boundary it controls.", "Trace the request, data shape, and framework hook before customizing."),
            ("Treating the abstraction as magic instead of generated behavior.", "Inspect the underlying request, SQL, or response contract."),
        ],
        "version": version,
        "extras": extras or [],
        "sample_sql": sample_sql,
    }


CONCEPTS = [
    c(
        "DJ01", 0, "foundation", "How the Web Works", [],
        "HTTP is the request/response protocol that browsers and servers use to exchange data.",
        "Without a wire-level model of requests and responses, Django request objects feel magical and debugging headers, cookies, redirects, or caching becomes guesswork.",
        "Browser -> DNS -> TCP/TLS -> HTTP request bytes -> server -> HTTP response bytes -> browser render.",
        ["What a browser actually sends on the wire", "How methods, headers, cookies, and status codes fit together", "Why Django wraps raw HTTP into HttpRequest and HttpResponse"],
        "Django models web work around explicit request and response objects because the protocol contract stays stable even when the server stack changes.",
        "Do not memorize status codes or headers as trivia; tie them back to browser behavior.",
        "Why are GET and HEAD safe methods, and why does that matter for view design?",
        "https://docs.djangoproject.com/en/4.2/ref/request-response/",
        """GET /articles/42/ HTTP/1.1
Host: blog.example.com
Accept: text/html
Cookie: sessionid=abc123; csrftoken=xyz789
""",
        sample_lang="http",
        extras=[
            x("Raw POST request", "Form data lives in the request body, not in the path.", code="""POST /posts/create/ HTTP/1.1
Host: blog.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 23

title=Hello&status=draft
""", lang="http", observe="Django turns form-encoded bodies into request.POST."),
            x("Raw HTTP response", "Responses are protocol text too: status line, headers, then body.", code="""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: sessionid=abc123; HttpOnly; SameSite=Lax

<h1>Hello Django</h1>
""", lang="http", observe="Headers like Set-Cookie and Location change browser behavior.")
        ],
        mistakes=[
            ("Treating HTTP as something the framework hides forever.", "Check method, headers, cookies, and status codes first when browser and server disagree."),
            ("Using POST for every write without understanding semantics.", "Choose methods by side effect and idempotency, not habit."),
        ],
    ),
    c(
        "DJ02", 0, "foundation", "What is a Web Framework?", [],
        "A web framework packages the repeated chores of web development so each product team does not reinvent routing, parsing, rendering, auth, and persistence.",
        "A raw socket server teaches the protocol, but it is a terrible base for product code because every feature starts with infrastructure work before the business logic appears.",
        "Frameworks sit between raw network bytes and your application code, standardizing the request pipeline and centralizing cross-cutting behavior.",
        ["Why raw socket or WSGI code is repetitive", "Which repetitive tasks Django removes", "How batteries-included differs from a microframework"],
        "Django chose an integrated stack so teams could move quickly without assembling routing, ORM, forms, admin, auth, and migrations from unrelated packages.",
        "Do not judge a framework only by lines of code saved; the bigger win is consistent security and conventions.",
        "What responsibilities would you still need to implement if you replaced Django with a raw WSGI app?",
        "https://docs.djangoproject.com/en/4.2/intro/overview/",
        """import socket

server = socket.socket()
server.bind(("127.0.0.1", 8000))
server.listen(1)
conn, _ = server.accept()
raw = conn.recv(4096).decode()
method, path, _ = raw.splitlines()[0].split()
""",
        comparison=[
            ("Without Django", "You hand-roll request parsing, route matching, error handling, sessions, templates, auth, SQL access, and tests."),
            ("With Django", "You start from django-admin startproject and plug business logic into a stable pipeline."),
        ],
        extras=[
            x("The same route in Django", "The application code starts near the business intent instead of the protocol plumbing.", code="""from django.http import HttpResponse

def hello(request):
    return HttpResponse("<h1>Hello from Django</h1>")
""", observe="The view is tiny because Django already parsed the request and knows how to build the response."),
            x("Subsystem map", "Each repeated pain point has a corresponding Django subsystem.", compare=[
                ("Routing", "DJ16 URLconf"),
                ("HTML rendering", "DJ21-DJ24 templates"),
                ("SQL generation", "DJ06-DJ15 ORM"),
                ("CSRF and forms", "DJ26-DJ31"),
                ("Auth and sessions", "DJ32-DJ36"),
                ("Admin and testing", "DJ50, DJ53"),
            ], observe="The value is the integration between these pieces, not any one piece alone."),
        ],
        mistakes=[
            ("Thinking frameworks only reduce typing.", "Judge them by the bugs they prevent and the conventions they unify."),
            ("Assuming every framework makes the same trade-offs.", "Django is intentionally opinionated around data-backed business apps."),
        ],
    ),
    c(
        "DJ03", 0, "foundation", "Django's Design Philosophy", [],
        "Django is an opinionated, batteries-included framework built around DRY, explicit configuration, and rapid delivery of data-backed applications.",
        "If you treat Django as a random bag of utilities, its conventions feel arbitrary and you will fight the framework instead of aligning with its design center.",
        "URLconf + views coordinate flow, models describe data, templates render presentation, and built-in apps cover common business application needs.",
        ["Why Django says MTV instead of MVC", "How DRY and explicit configuration shape the stack", "What batteries included means in practice"],
        "Django prefers one integrated path for common work so teams spend less time on glue code and more time on product behavior.",
        "Do not read opinionated as inflexible; start with the defaults, then customize when the product truly differs.",
        "How does Django's MTV terminology map to classic MVC?",
        "https://docs.djangoproject.com/en/4.2/misc/design-philosophies/",
        """INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
""",
        diagram="""flowchart LR
    Browser --> URLconf
    URLconf --> View
    View --> Model
    View --> Template
    Template --> Browser
""",
        mistakes=[
            ("Putting rich business logic into templates because the site still renders.", "Keep presentation limited and move real branching into views, forms, or model/queryset methods."),
            ("Replacing every Django default immediately.", "Use the built-ins first and customize only where the product genuinely needs it."),
        ],
    ),
    c(
        "DJ04", 0, "foundation", "Django Installation & Project Setup", [],
        "A Django project is the deployment shell and configuration container, while apps are reusable feature modules inside that project.",
        "The generated files look small, but if you do not know what each one does you will edit settings, URLs, apps, and deployment entry points blindly.",
        "Project = config shell and runtime entry points. App = cohesive feature module. manage.py = local command launcher.",
        ["What startproject and startapp generate", "Why manage.py, settings.py, urls.py, wsgi.py, and asgi.py exist", "How project and app boundaries differ"],
        "Django separates project-level configuration from app-level features so code can remain reusable and deployment entry points stay centralized.",
        "Do not collapse everything into one app just because the project is small today.",
        "What is the difference between manage.py, django-admin, WSGI, and ASGI?",
        "https://docs.djangoproject.com/en/4.2/intro/tutorial01/",
        """python -m venv .venv
pip install "django>=4.2,<5.2"
django-admin startproject config .
python manage.py startapp blog
python manage.py runserver
""",
        sample_lang="bash",
        extras=[
            x("Project tree", "This scaffold is the first mental map to memorize.", code="""config/
    __init__.py
    asgi.py
    settings.py
    urls.py
    wsgi.py
manage.py
blog/
    admin.py
    apps.py
    migrations/
    models.py
    tests.py
    views.py
""", lang="text", observe="manage.py is local command entry. settings.py is configuration. urls.py is routing. wsgi.py / asgi.py are deployment entry points."),
            x("manage.py bootstraps settings", "It is tiny, but it is the bridge between your shell and Django's command system.", code="""import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
""", observe="os.environ.setdefault tells Django which settings module to load."),
        ],
    ),
    c(
        "DJ05", 0, "foundation", "Django's Request/Response Lifecycle", [],
        "Every request passes through a server adapter, middleware, URL resolution, view code, optional database work, and then the reverse response path.",
        "Without a lifecycle model, middleware order, auth state, CSRF, exceptions, and headers all seem unpredictable.",
        "Request flows down the middleware stack to the view; response climbs back through middleware in reverse order.",
        ["Where WSGI or ASGI stops and Django begins", "How middleware, URLconf, views, templates, and ORM cooperate", "Why order matters in the request path"],
        "Django's lifecycle is layered so cross-cutting behavior can wrap the request once instead of being duplicated in every view.",
        "Do not think of middleware as random hooks; it is a decorator stack whose order changes behavior.",
        "What happens between GET /articles/42/ and the final HTML response?",
        "https://docs.djangoproject.com/en/4.2/topics/http/middleware/",
        """def article_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related("author"), pk=pk)
    return render(request, "blog/article_detail.html", {"post": post})
""",
        diagram=REQUEST_SEQUENCE,
        version="Django 4.2 is the LTS baseline. Django 5.x keeps the same lifecycle model while widening async support across more internals.",
        extras=[
            x("The full sequence diagram", "This is the pipeline you should picture when debugging auth, sessions, middleware, and ORM timing.", diagram=REQUEST_SEQUENCE, observe="Each arrow is a real boundary: socket bytes, HttpRequest, SQL, HttpResponse."),
            x("Inspecting request and response objects", "The request and response types carry more debugging information than most teams use.", code="""def debug_view(request):
    print(request.method, request.path, request.user)
    print(request.GET, request.POST, request.META.get("HTTP_USER_AGENT"))
    response = HttpResponse("ok", status=201)
    response["X-Debug"] = "request-traced"
    return response
""", observe="Request exposes method, path, GET, POST, FILES, user, session, and META. Response exposes status_code, content, headers, and cookies."),
        ],
    ),
    c(
        "DJ06", 1, "orm", "What is an ORM?", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "An ORM maps tables and rows to Python classes and objects so most application queries can be expressed in Python instead of handwritten SQL everywhere.",
        "Raw SQL gives full control, but every feature team then repeats connection setup, parameter binding, row mapping, and transaction handling.",
        "Models describe schema, QuerySets describe SQL lazily, and evaluated QuerySets become Python objects or projected values.",
        ["How models map to tables and QuerySets map to SQL", "What boilerplate the ORM removes", "Why ORM convenience does not eliminate the need to understand SQL"],
        "Django's ORM is designed for everyday business queries first while still letting you inspect generated SQL or drop down to raw SQL when needed.",
        "Do not use the ORM as an excuse to ignore SQL; performance work always returns to query shape and indexes.",
        "What does the ORM buy you, what does it cost you, and when should you drop to raw SQL?",
        "https://docs.djangoproject.com/en/4.2/topics/db/models/",
        """posts = (
    Post.objects
    .filter(status="published")
    .select_related("author")
)
for post in posts:
    print(post.title, post.author.name)
""",
        sample_sql="""SELECT p.*, a.*
FROM blog_post p
JOIN blog_author a ON p.author_id = a.id
WHERE p.status = 'published';
""",
        extras=[
            x("Raw psycopg2 path", "This is the kind of boilerplate the ORM replaces for ordinary create and read flows.", code="""import psycopg2

conn = psycopg2.connect("dbname=blog user=blog")
cur = conn.cursor()
cur.execute(
    "SELECT p.title, a.name FROM blog_post p "
    "JOIN blog_author a ON a.id = p.author_id "
    "WHERE p.status = %s",
    ["published"],
)
rows = cur.fetchall()
""", observe="The business intent is buried under connection handling and manual row mapping."),
            x("Inspecting generated SQL", "The ORM is only safe when you can inspect the query it emits.", code="""from django.db import connection
connection.queries_log.clear()
list(Post.objects.filter(status="published")[:2])
for query in connection.queries:
    print(query["sql"])
""", observe="connection.queries is useful for teaching and debugging under DEBUG mode."),
        ],
    ),
    c(
        "DJ07", 1, "orm", "Defining Models", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "A Django model is a Python class that describes schema, constraints, field behavior, and domain methods for one table-like entity.",
        "If schema is scattered across raw SQL and ad-hoc query strings, the application loses a single authoritative description of its data model.",
        "Each model class is a schema contract plus a Python API for rows in that table.",
        ["How field declarations map to columns and constraints", "Why null, blank, default, unique, and db_index exist", "How the Blog models fit together before deeper ORM topics"],
        "Django puts schema near behavior so migrations, forms, admin, and QuerySets can all share one source of truth.",
        "Do not conflate null and blank. One is database storage, the other is validation behavior.",
        "What is the difference between null=True, blank=True, default=..., unique=True, and db_index=True?",
        "https://docs.djangoproject.com/en/4.2/topics/db/models/",
        """class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="posts")
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    status = models.CharField(max_length=20, default="draft")
    published_at = models.DateTimeField(null=True, blank=True)
""",
        sample_sql="""CREATE TABLE blog_post (
    id uuid PRIMARY KEY,
    title varchar(200) NOT NULL,
    slug varchar(50) NOT NULL UNIQUE,
    body text NOT NULL,
    status varchar(20) NOT NULL DEFAULT 'draft',
    published_at timestamp with time zone NULL
);
""",
        version="Django 5.0 added db_default for database-side defaults when the database, not Python, should own the default value.",
        mistakes=[
            ("Using null=True on CharField because the field is optional in forms.", "For text fields, prefer blank=True unless NULL has a real semantic meaning."),
            ("Adding db_index=True everywhere just to be safe.", "Index fields that actually participate in measured lookups, joins, or ordering."),
        ],
    ),
    c(
        "DJ08", 1, "orm", "Field Types Deep-Dive", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "Field classes encode both data meaning and storage behavior, so field choice affects schema, validation, widgets, and performance.",
        "Picking the wrong field type leaks domain bugs into storage: floats where decimals belong, text where relations belong, or JSON where schema should be explicit.",
        "A field type is a contract between Python values, database storage, forms, admin, and serialization.",
        ["Which field types fit common data", "Why DecimalField beats FloatField for money", "Where auto_now, JSONField, UUIDField, FileField, and ImageField shine or backfire"],
        "Django offers many field classes because storage shape, validation rules, and UI behavior should align with the meaning of the data.",
        "Do not reach for JSONField as a schema escape hatch when the data has stable relational structure.",
        "Why is DecimalField preferred over FloatField for prices, and what do auto_now and auto_now_add really do?",
        "https://docs.djangoproject.com/en/4.2/ref/models/fields/",
        """class Profile(models.Model):
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metadata = models.JSONField(default=dict, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
""",
        mistakes=[
            ("Using TextField everywhere because it feels flexible.", "Choose the narrowest field type that describes the domain honestly."),
            ("Dumping relational data into JSONField to avoid a migration.", "Use JSONField for flexible metadata, not for core structured relationships."),
        ],
    ),
    c(
        "DJ09", 1, "orm", "Relationships", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "Django relationships describe one-to-many, many-to-many, and one-to-one links so the ORM can join, prefetch, and reverse-traverse data safely.",
        "Without first-class relationships, every join and reverse lookup becomes manual SQL knowledge spread across the codebase.",
        "ForeignKey points to one parent, ManyToManyField creates a junction table, and OneToOneField is a unique foreign key.",
        ["How ForeignKey, ManyToManyField, and OneToOneField differ", "What on_delete choices actually do to your data", "Why related_name matters for reverse access and query readability"],
        "Django bakes relationships into model definitions so reverse accessors, admin, forms, and QuerySets all share the same relationship contract.",
        "Do not leave on_delete choices on autopilot. Each option encodes a real business rule about deletion.",
        "What is the practical difference between select_related and prefetch_related, and how does that connect to relationship type?",
        "https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_one/",
        """class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

class Post(models.Model):
    tags = models.ManyToManyField(Tag, related_name="posts")
""",
        diagram="""erDiagram
    AUTHOR ||--o{ POST : writes
    POST ||--o{ COMMENT : receives
    POST }o--o{ TAG : labeled_with
    USER ||--|| PROFILE : owns
""",
        mistakes=[
            ("Accepting the default reverse name everywhere.", "Set related_name intentionally for relationships you will query or render."),
            ("Choosing CASCADE just because it is easy.", "Pick the on_delete behavior that matches the business rule and test it."),
        ],
    ),
    c(
        "DJ10", 1, "orm", "Migrations", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "Migrations are version-controlled schema change programs that let Django evolve the database incrementally and reproducibly.",
        "Without migrations, schema changes live in tribal knowledge and manual SQL scripts, which is how teams end up with different databases and broken deploys.",
        "Model changes become migration operations, and Django executes the migration graph in dependency order.",
        ["How makemigrations and migrate work together", "What migration files actually contain", "How to handle data migrations and conflicts in a team"],
        "Django treats schema changes as code so application state and database state can evolve together under version control.",
        "Do not edit a migration already applied in shared environments unless you are deliberately creating a corrective migration.",
        "Why are migrations a graph instead of a simple linear history?",
        "https://docs.djangoproject.com/en/4.2/topics/migrations/",
        """python manage.py makemigrations blog
python manage.py showmigrations --plan
python manage.py migrate
""",
        sample_lang="bash",
        extras=[
            x("Migration file anatomy", "A migration is plain Python with dependencies and operations.", code="""class Migration(migrations.Migration):
    dependencies = [("blog", "0004_post_status")]
    operations = [
        migrations.AddField(
            model_name="post",
            name="published_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
""", observe="Dependencies keep the graph consistent. Operations define schema or data changes in order."),
            x("Data migration", "RunPython backfills existing rows safely when schema changes need historical data updates.", code="""def backfill_published_at(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.filter(status="published", published_at__isnull=True).update(
        published_at=timezone.now()
    )
""", observe="Use apps.get_model inside migrations instead of importing live models."),
        ],
        mistakes=[
            ("Changing models and forgetting to create a migration.", "Run makemigrations whenever model definitions change and review the generated operations."),
            ("Importing live models directly in a data migration.", "Use historical models from apps.get_model inside RunPython."),
        ],
    ),
    c(
        "DJ11", 1, "orm", "QuerySet API - Basic", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "A QuerySet is a lazy database query builder that executes only when the result is actually needed.",
        "If you treat QuerySets like in-memory lists, you will trigger unnecessary queries and miss where SQL is really executed.",
        "QuerySets are composable SQL blueprints that become results only when evaluated.",
        ["How common QuerySet methods map to SQL operations", "What lazy evaluation means in practice", "How to read simple SQL from QuerySet output"],
        "Django makes QuerySets chainable and lazy so filtering, ordering, and projection stay declarative until the result is needed.",
        "Do not evaluate the same QuerySet repeatedly inside one code path without noticing the extra queries.",
        "What operations cause a QuerySet to execute?",
        "https://docs.djangoproject.com/en/4.2/topics/db/queries/",
        """posts = Post.objects.filter(status="published").order_by("-published_at")
first_post = posts.first()
titles = posts.values_list("title", flat=True)
exists = posts.exists()
count = posts.count()
""",
        sample_sql="""SELECT * FROM blog_post
WHERE status = 'published'
ORDER BY published_at DESC;
""",
        extras=[
            x("Lazy evaluation proof", "Building the QuerySet does not hit the database yet.", code="""connection.queries_log.clear()
qs = Post.objects.filter(status="published")
print(len(connection.queries))  # 0
list(qs[:2])
print(len(connection.queries))  # 1
""", observe="Iteration, list(), len(), bool(), count(), exists(), and many terminal methods force evaluation."),
            x("Projection with values()", "Not every read needs full model objects.", code="""rows = Post.objects.values("title", "slug")[:3]
titles = Post.objects.values_list("title", flat=True)
""", observe="Projection can reduce object construction and serialization overhead."),
        ],
        mistakes=[
            ("Calling len(qs), exists(), and then iterating qs again.", "Choose the result shape once and reuse it intentionally."),
            ("Using get() where uniqueness is not guaranteed.", "Use get() only when the database or business rule guarantees one row."),
        ],
    ),
    c(
        "DJ12", 1, "orm", "QuerySet API - Advanced", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "Advanced QuerySet features let you shape SQL intentionally with joins, prefetches, annotations, expressions, subqueries, and windows.",
        "Knowing only the basic ORM is how teams ship N+1 queries, race-prone counters, and expensive reporting queries without noticing.",
        "Advanced QuerySets move more work into one carefully shaped SQL query or a small controlled set of queries.",
        ["How to fix N+1 patterns with select_related and prefetch_related", "How annotations and expressions map to SQL features", "Why advanced QuerySets still need SQL inspection"],
        "Django exposes advanced SQL features through Python expressions so most optimization work can stay in application code while remaining inspectable.",
        "Do not chain advanced ORM features blindly. Inspect the generated SQL and row counts.",
        "When do you use select_related versus prefetch_related?",
        "https://docs.djangoproject.com/en/4.2/ref/models/querysets/",
        """posts = (
    Post.objects.published()
    .select_related("author")
    .prefetch_related("tags", "comments")
)
""",
        sample_sql="""SELECT p.*, a.*
FROM blog_post p
JOIN blog_author a ON p.author_id = a.id
WHERE p.status = 'published';
""",
        extras=[
            x("N+1 proof", "Without select_related, each post.author access can trigger another query.", code="""with CaptureQueriesContext(connection) as ctx:
    for post in Post.objects.filter(status="published")[:10]:
        print(post.author.name)
print(len(ctx.captured_queries))
""", observe="One query for posts plus many queries for authors is the classic N+1 smell."),
            x("Expressions and subqueries", "The ORM can express much richer SQL than many teams assume.", code="""qs = Post.objects.annotate(
    comment_count=Count("comments"),
    latest_comment=Subquery(
        Comment.objects.filter(post=OuterRef("pk")).order_by("-created_at").values("body")[:1]
    ),
)
""", observe="annotate(), F(), Q(), Subquery(), OuterRef(), and Window let you keep serious query logic in QuerySets."),
        ],
        mistakes=[
            ("Using select_related for many-to-many or reverse FK collections.", "Use prefetch_related for collections and select_related for single-valued joins."),
            ("Incrementing counters with obj.count += 1; obj.save() under concurrency.", "Use F expressions or row locks when consistency matters."),
        ],
    ),
    c(
        "DJ13", 1, "orm", "Model Methods & Managers", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "Models can hold domain behavior while managers and QuerySets package repeated query logic behind readable APIs.",
        "If every view rebuilds the same filters and display logic, the codebase leaks business rules across many layers.",
        "Put row-level behavior on model methods and query-level behavior on managers or QuerySets.",
        ["What belongs on model methods versus managers", "Why __str__, clean, and Meta matter", "How indexes and constraints encode business rules"],
        "Django encourages reusable data logic near the models so views and serializers can stay thin and consistent.",
        "Do not bury side effects in save() overrides if an explicit function would be easier to trace.",
        "When should logic live on a model method, manager, view, or service function?",
        "https://docs.djangoproject.com/en/4.2/topics/db/managers/",
        """class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published")

class Post(models.Model):
    objects = PostQuerySet.as_manager()
""",
        extras=[
            x("__str__ and clean()", "Readable model objects and cross-field validation pay off immediately in admin and tests.", code="""def __str__(self):
    return f"{self.title} [{self.status}]"

def clean(self):
    if self.status == "published" and self.published_at is None:
        raise ValidationError("Published posts need a timestamp.")
""", observe="clean() is for validation across fields; __str__ affects shell, admin, and debugging."),
            x("Meta indexes and constraints", "Database constraints protect integrity even if one code path forgets a check.", code="""class Meta:
    indexes = [models.Index(fields=["author", "-published_at"])]
    constraints = [
        models.UniqueConstraint(fields=["author", "slug"], name="unique_slug_per_author"),
    ]
""", observe="Meta is not decoration; it shapes ordering, indexes, and uniqueness."),
        ],
    ),
    c(
        "DJ14", 1, "orm", "Database Transactions", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "Transactions group multiple writes into an all-or-nothing unit so partial failures do not corrupt application state.",
        "Multi-step writes that partially succeed create the nastiest bugs because the database looks valid row by row but inconsistent at the workflow level.",
        "A transaction is a protected block: either all its operations commit together or none of them persist.",
        ["How atomic(), savepoints, select_for_update, and on_commit() work", "Where race conditions appear in ordinary Django code", "Why side effects should wait until after commit"],
        "Django exposes transactions explicitly so correctness-sensitive workflows can state their consistency boundaries in application code.",
        "Do not wrap every request in a transaction by default without measuring the trade-off.",
        "Why is sending email in post_save often wrong when the surrounding transaction has not committed yet?",
        "https://docs.djangoproject.com/en/4.2/topics/db/transactions/",
        """@transaction.atomic
def publish_post(post):
    post.status = "published"
    post.save(update_fields=["status"])
    AuditLog.objects.create(action="publish", post=post)
""",
        extras=[
            x("on_commit for side effects", "Queue external work only after the database state is durable.", code="""transaction.on_commit(lambda: send_publication_email.delay(post.id))
""", observe="If the transaction rolls back, the task or email should never escape."),
            x("select_for_update", "Locks are sometimes the simplest way to protect a hot row.", code="""with transaction.atomic():
    post = Post.objects.select_for_update().get(pk=post_id)
    post.view_count = F("view_count") + 1
    post.save(update_fields=["view_count"])
""", observe="select_for_update prevents concurrent workers from racing through the same row."),
        ],
    ),
    c(
        "DJ15", 1, "orm", "Raw SQL", ["DJ01", "DJ02", "DJ03", "DJ04"],
        "Raw SQL is the escape hatch for queries that are clearer, faster, or only possible at the SQL level.",
        "Some queries involve recursive CTEs, vendor-specific operators, or reporting logic that stretch the ORM past readability.",
        "Use the ORM by default, inspect SQL often, and drop to raw SQL only when it is the clearer and safer representation.",
        ["When raw() and cursor() are appropriate", "How to avoid SQL injection", "How to mix raw SQL responsibly with ORM-managed models"],
        "Django keeps raw SQL available because no abstraction should pretend every database capability fits one clean API.",
        "Do not interpolate user input into SQL strings, even in internal tools.",
        "When is raw SQL the right tool in a Django app?",
        "https://docs.djangoproject.com/en/4.2/topics/db/sql/",
        """sql = '''
SELECT *
FROM blog_post
WHERE status = %s
ORDER BY published_at DESC
'''
for post in Post.objects.raw(sql, ["published"]):
    print(post.title)
""",
        sample_sql="""SELECT *
FROM blog_post
WHERE status = 'published'
ORDER BY published_at DESC;
""",
        extras=[
            x("connection.cursor()", "Cursor access is lower-level and ideal for arbitrary reports or vendor-specific features.", code="""with connection.cursor() as cursor:
    cursor.execute(
        "SELECT date_trunc('day', created_at) AS day, COUNT(*) FROM blog_comment GROUP BY day"
    )
    rows = cursor.fetchall()
""", observe="Rows come back as tuples unless you map them yourself."),
            x("Parameter binding blocks injection", "Pass parameters separately so the driver handles quoting.", compare=[
                ("Unsafe", "sql = f\"SELECT * FROM blog_post WHERE author_id = {request.GET['author']}\""),
                ("Safe", "cursor.execute(\"SELECT * FROM blog_post WHERE author_id = %s\", [author])"),
            ], observe="Never concatenate attacker-controlled text into SQL strings."),
        ],
    ),
    c(
        "DJ16", 2, "views", "URL Configuration", ["DJ05", "DJ11"],
        "URLconf maps incoming paths to callables and gives routes stable names so code can reverse URLs instead of hardcoding paths.",
        "If paths are scattered through templates, redirects, and JS as raw strings, route changes become fragile search-and-replace exercises.",
        "urlpatterns is an ordered list; Django scans for the first matching pattern and then calls the associated view.",
        ["How path(), re_path(), include(), name, and app_name work together", "Why reverse() and {% url %} beat hardcoded URLs", "How path converters feed typed parameters into views"],
        "Django keeps routing declarative and name-based so navigation can be refactored safely across templates, redirects, and tests.",
        "Do not build URL strings manually when the route already has a name.",
        "How does Django resolve a URL, and what breaks when developers hardcode paths?",
        "https://docs.djangoproject.com/en/4.2/topics/http/urls/",
        """urlpatterns = [
    path("blog/", include(("blog.urls", "blog"), namespace="blog")),
]
""",
        extras=[
            x("App-level namespacing", "include() keeps large projects modular and gives route names a safe namespace.", code="""app_name = "blog"
urlpatterns = [
    path("", views.post_list, name="post-list"),
    path("<slug:slug>/", views.post_detail, name="post-detail"),
]
""", observe="reverse('blog:post-detail', kwargs={'slug': post.slug}) is safer than hardcoding paths."),
            x("Custom path converter", "Converters keep parsing logic near routing instead of burying it in the view body.", code="""class DateConverter:
    regex = r"\\d{4}-\\d{2}-\\d{2}"
    def to_python(self, value):
        return datetime.date.fromisoformat(value)
""", observe="The converter validates and transforms the path segment before the view receives it."),
        ],
    ),
    c(
        "DJ17", 2, "views", "Function-Based Views", ["DJ05", "DJ11"],
        "A function-based view is the most direct way to receive an HttpRequest, perform work, and return an HttpResponse.",
        "If you do not know the request object well, you will miss built-in helpers for data access, auth, files, headers, and error responses.",
        "A function-based view is just Python with a disciplined input and output: request in, response out.",
        ["How to read request.method, GET, POST, FILES, META, user, and session", "When to use HttpResponse, render, redirect, and Http404 helpers", "Why FBVs are often the clearest starting point"],
        "Django keeps FBVs simple because explicit request-in / response-out functions are easy to debug, test, and reason about.",
        "Do not reach for class-based views before you understand the plain function flow they abstract.",
        "When is a function-based view clearer than a class-based view?",
        "https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/",
        """def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("author"), slug=slug)
    return render(request, "blog/post_detail.html", {"post": post})
""",
        extras=[
            x("Touring the request object", "The request already exposes parsed query params, form data, files, headers, auth, and session state.", code="""def inspect_request(request):
    print(request.method, request.GET, request.POST)
    print(request.user, request.session.session_key)
    print(request.META.get("HTTP_REFERER"))
    return HttpResponse("inspected")
""", observe="Django has already done the protocol parsing work for you by the time the view runs."),
            x("Method guards and redirects", "Protocol behavior belongs in the view contract too.", code="""@require_http_methods(["POST"])
def publish_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.status = "published"
    post.save(update_fields=["status"])
    return redirect("blog:post-detail", slug=post.slug)
""", observe="A 301 and 302 are not interchangeable; redirects are part of HTTP semantics."),
        ],
    ),
    c(
        "DJ18", 2, "views", "Class-Based Views - Generic", ["DJ05", "DJ11"],
        "Generic class-based views package recurring patterns such as list, detail, create, update, delete, and form handling into reusable classes.",
        "Many CRUD views differ only in model, template, form, and success URL, so writing every view as a custom function repeats a lot of ceremony.",
        "A CBV is a small inheritance tree that turns request methods into hooks you can override selectively.",
        ["What View, TemplateView, ListView, DetailView, and editing views provide", "How generic views reduce CRUD boilerplate", "When the abstraction helps and when it hides too much"],
        "Django's generic views remove repetitive scaffolding while still leaving clear hooks for queryset selection, context building, and form handling.",
        "Do not use a generic view if you cannot explain which method is responsible for the behavior you are customizing.",
        "What work does ListView do automatically, and when would you replace it with an FBV?",
        "https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/",
        """class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "post_list"
""",
        extras=[
            x("FBV vs ListView", "The generic view earns its keep when the workflow is actually generic.", compare=[
                ("FBV", "Explicit control, best for unusual flows or multiple forms."),
                ("ListView", "Less boilerplate for standard list pages with predictable hooks."),
            ], observe="Use the smallest abstraction that stays readable."),
            x("CreateView inheritance chain", "The class hierarchy explains where behavior and override hooks come from.", diagram="""flowchart TD
    CreateView --> BaseCreateView
    BaseCreateView --> ModelFormMixin
    ModelFormMixin --> FormMixin
    BaseCreateView --> ProcessFormView
    ProcessFormView --> View
""", observe="Know the parent classes before overriding methods in a deep CBV."),
        ],
    ),
    c(
        "DJ19", 2, "views", "Class-Based Views - Mixins", ["DJ05", "DJ11"],
        "Mixins let CBVs compose cross-cutting behavior such as login requirements, permission checks, and context helpers through Python's method resolution order.",
        "The power of mixins is composition; the danger of mixins is not understanding the order in which their methods run.",
        "A mixin is a parent class that contributes methods to the MRO. Leftmost bases usually run first.",
        ["How LoginRequiredMixin, PermissionRequiredMixin, and UserPassesTestMixin work", "Why MRO determines whether a mixin actually intercepts dispatch()", "How to build small custom mixins without hiding the control flow"],
        "Django uses mixins for reusable behavior because they fit Python's class model and keep view concerns composable without giant base classes.",
        "Do not pile on mixins if you cannot trace the MRO on paper.",
        "Why must LoginRequiredMixin usually appear before the view base class?",
        "https://docs.djangoproject.com/en/4.2/topics/auth/default/#the-loginrequiredmixin-mixin",
        """class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "body"]
    permission_required = "blog.change_post"
""",
        extras=[
            x("A custom author-only mixin", "Small mixins work best when they enforce one narrow rule.", code="""class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author_id != request.user.author_id:
            raise PermissionDenied("Only the author may edit this post.")
        return super().dispatch(request, *args, **kwargs)
""", observe="dispatch() is the right hook when access should be checked before the main handler."),
            x("Mixin order rule", "If the mixin sits after the concrete view, its dispatch often does not intercept the request the way you expect.", compare=[
                ("Correct", "class GoodView(LoginRequiredMixin, DetailView): ..."),
                ("Risky", "class BadView(DetailView, LoginRequiredMixin): ..."),
            ], observe="Read the inheritance list left to right and verify the MRO when behavior disappears."),
        ],
    ),
    c(
        "DJ20", 2, "views", "Middleware", ["DJ05", "DJ11"],
        "Middleware wraps the request/response cycle to apply cross-cutting concerns such as security headers, sessions, auth, caching, and CSRF.",
        "Without middleware, every view would need to repeat the same checks and response mutations, which guarantees inconsistency.",
        "Middleware is a decorator stack around the view: request flows down, response flows back up.",
        ["How request, response, and exception middleware fit together", "Why middleware ordering changes behavior", "What key built-in middleware classes do"],
        "Django centralizes cross-cutting behavior in middleware so individual views can focus on feature logic and the pipeline stays configurable in one place.",
        "Do not put feature-specific business logic into middleware just because it runs globally.",
        "Why does middleware order matter so much in Django?",
        "https://docs.djangoproject.com/en/4.2/topics/http/middleware/",
        """class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        started = time.perf_counter()
        response = self.get_response(request)
        return response
""",
        extras=[
            x("Middleware as a wrapper stack", "Visualizing the stack makes request and response flow concrete.", diagram="""flowchart TD
    Request --> Security
    Security --> Session
    Session --> Auth
    Auth --> View
    View --> Auth
    Auth --> Session
    Session --> Security
    Security --> Response
""", observe="Request and response both traverse middleware; the response comes back in reverse order."),
            x("Maintenance mode middleware", "Global policy decisions belong in middleware when they truly apply to every request.", code="""class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if cache.get("maintenance_mode") and not request.user.is_staff:
            return HttpResponse("Temporarily unavailable", status=503)
        return self.get_response(request)
""", observe="This is appropriate because it is a cross-cutting request gate, not feature-specific business logic."),
        ],
    ),
    c(
        "DJ21", 3, "templates", "Django Template Language (DTL)", ["DJ17"],
        "DTL is a presentation-focused language for rendering HTML safely from context data passed by the view.",
        "If templates can execute arbitrary Python, presentation code becomes a security and maintainability trap.",
        "Templates should display prepared data, not become a second application layer with unrestricted logic.",
        ["How variables, tags, filters, and context rendering work", "Why auto-escaping is a default security feature", "How DTL differs from raw string formatting or unrestricted Python templating"],
        "Django intentionally keeps templates limited and auto-escaped so designers and backend developers can collaborate without turning HTML into uncontrolled business logic.",
        "Do not disable autoescape casually; most uses of safe are XSS bugs waiting to happen.",
        "What problem does Django's auto-escaping solve, and when is safe actually justified?",
        "https://docs.djangoproject.com/en/4.2/topics/templates/",
        """<h1>{{ post.title }}</h1>
<p>By {{ post.author.name|upper }}</p>
{% for tag in post.tags.all %}
  <span>{{ tag.name }}</span>
{% empty %}
  <span>No tags yet.</span>
{% endfor %}
""",
        sample_lang="html",
        extras=[
            x("Auto-escaping stops XSS by default", "User content is escaped unless you explicitly mark it safe.", compare=[
                ("Stored value", "<script>alert('pwnd')</script>"),
                ("Rendered output", "&lt;script&gt;alert('pwnd')&lt;/script&gt;"),
            ], observe="The browser sees HTML entities, not executable script tags."),
            x("render() prepares context", "The view should shape data; the template should display it.", code="""def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post_detail.html", {"post": post, "comment_count": post.comments.count()})
""", observe="This separation keeps templates simple and secure."),
        ],
    ),
    c(
        "DJ22", 3, "templates", "Template Inheritance", ["DJ17"],
        "Template inheritance lets child templates extend a shared base layout and override only named blocks.",
        "Copy-pasting the full HTML shell into every template guarantees drift and turns global design changes into a slog.",
        "base.html owns the stable page frame; child templates fill specific placeholders.",
        ["How extends, block, and include compose templates", "Why base.html is a core DRY pattern", "How fragment caching fits into shared template structure"],
        "Django makes inheritance a first-class template feature because most products share a global shell with varying page content.",
        "Do not turn include files into hidden control-flow mazes; keep them presentational and local.",
        "What is the difference between extends and include?",
        "https://docs.djangoproject.com/en/4.2/ref/templates/language/#template-inheritance",
        """<!doctype html>
<html>
  <head>
    <title>{% block title %}Blog{% endblock %}</title>
  </head>
  <body>
    <main>{% block content %}{% endblock %}</main>
  </body>
</html>
""",
        sample_lang="html",
        extras=[
            x("Child template", "The child focuses on content because the shared shell already lives in base.html.", code="""{% extends "base.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
  <article>{{ post.body }}</article>
{% endblock %}
""", lang="html", observe="Inheritance centralizes the repeated shell and exposes only the changing blocks."),
            x("Fragment caching", "Cache expensive partials without caching the entire page.", code="""{% load cache %}
{% cache 600 "sidebar-top-tags" request.user.is_authenticated %}
  {% include "blog/_tag_cloud.html" %}
{% endcache %}
""", lang="html", observe="Vary the cache key when personalized content is involved."),
        ],
    ),
    c(
        "DJ23", 3, "templates", "Custom Template Tags & Filters", ["DJ17"],
        "Custom template tags and filters package repeated presentation logic into explicit reusable components.",
        "If views and templates repeat the same formatting or pagination link logic, the HTML layer accumulates copy-paste bugs.",
        "A filter transforms one value; a tag can perform richer template-side presentation work with controlled inputs.",
        ["How to build simple_tag, inclusion_tag, and custom filters", "Why tags beat complex inline template logic", "How to build reusable pagination or query-string helpers"],
        "Django extends the template language through explicit libraries so presentation helpers stay discoverable instead of hiding in ad-hoc HTML snippets.",
        "Do not move business rules into template tags just because the result ends up in HTML.",
        "When would you write a filter versus a simple_tag or inclusion_tag?",
        "https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/",
        """@register.filter
def reading_minutes(text):
    words = len(text.split())
    return max(1, round(words / 200))
""",
        extras=[
            x("query_string helper", "Classic pagination and filtering UIs need to preserve existing params while changing one or two.", code="""@register.simple_tag(takes_context=True)
def query_string(context, **kwargs):
    params = context["request"].GET.copy()
    for key, value in kwargs.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value
    return params.urlencode()
""", observe="The tag prevents filter and pagination links from discarding the user's current state."),
            x("Inclusion tag", "An inclusion tag renders a small template with prepared context.", code="""@register.inclusion_tag("blog/_pagination.html", takes_context=True)
def pagination(context, page_obj):
    return {"request": context["request"], "page_obj": page_obj}
""", observe="Use inclusion tags when repeated markup deserves one source of truth."),
        ],
    ),
    c(
        "DJ24", 3, "templates", "Template Context Processors", ["DJ17"],
        "Context processors inject shared context into templates so site-wide data does not need to be added manually by every view.",
        "Without context processors, repeated global data such as request, auth state, messages, or site settings gets copied into many views.",
        "A context processor is a function that returns a small dictionary merged into template context during render.",
        ["Which built-in context processors are common", "How to add safe site-wide context", "Why context processors should stay small and cheap"],
        "Django makes global template context explicit through settings so shared data is centralized instead of copied view by view.",
        "Do not load expensive query results in a context processor that runs on every request.",
        "Why can a context processor become a hidden performance problem?",
        "https://docs.djangoproject.com/en/4.2/ref/templates/api/#writing-your-own-context-processors",
        """TEMPLATES = [
    {
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
""",
        extras=[
            x("Custom site-wide context", "This is the right place for cheap global display data.", code="""def site_context(request):
    return {
        "site_name": "Acme Django Blog",
        "support_email": "support@example.com",
    }
""", observe="Return a small dictionary with values many templates need."),
            x("Using request and messages", "Shared context is most useful in layout templates.", code="""{% if request.user.is_authenticated %}
  <p>Signed in as {{ request.user.username }}</p>
{% endif %}
{% for message in messages %}
  <div class="flash">{{ message }}</div>
{% endfor %}
""", lang="html", observe="auth, request, and messages are commonly surfaced through context processors."),
        ],
    ),
    c(
        "DJ25", 3, "templates", "Static Files", ["DJ17"],
        "Django distinguishes application code from static assets so CSS, JavaScript, and images can be discovered, versioned, and served correctly.",
        "Static files seem simple until production: collectstatic, cache busting, WhiteNoise or CDN serving, and uploaded media are all different concerns.",
        "Static assets are deploy-time files; media files are user uploads. Treat them differently.",
        ["What STATIC_URL, STATIC_ROOT, and STATICFILES_DIRS mean", "How {% static %} and collectstatic fit together", "Why WhiteNoise or a CDN is common in production"],
        "Django separates static assets from media uploads so deployment tooling can optimize and cache each category differently.",
        "Do not serve user uploads with the same assumptions as versioned static assets.",
        "What does collectstatic do, and why are STATIC_ROOT and MEDIA_ROOT not interchangeable?",
        "https://docs.djangoproject.com/en/4.2/howto/static-files/",
        """STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
""",
        extras=[
            x("Template usage", "The static tag decouples HTML from the physical asset path.", code="""{% load static %}
<link rel="stylesheet" href="{% static 'css/site.css' %}">
<img src="{% static 'img/logo.svg' %}" alt="Acme logo">
""", lang="html", observe="Do not hardcode /static/... when the storage backend may rewrite names."),
            x("WhiteNoise production setup", "For many deployments, WhiteNoise is the simplest way to serve immutable assets from the app container.", code="""MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
""", observe="High-volume sites often move static files to object storage or a CDN instead."),
        ],
    ),
    c(
        "DJ26", 4, "forms", "HTML Forms vs Django Forms", ["DJ21", "DJ17"],
        "Django Forms centralize validation, coercion, CSRF handling, error rendering, and redisplay of invalid input.",
        "Hand-parsing HTML forms quickly turns into repetitive code for required fields, type conversion, error messages, and preserving user input after validation fails.",
        "A Django Form is a schema and validation pipeline for user input, separate from the HTML tag that submits it.",
        ["Why raw HTML forms are only half the problem", "How Django Forms reduce repetition", "Where forms fit relative to models and views"],
        "Django separates HTML form rendering from Python-side validation so the same validation logic can be reused across views and templates.",
        "Do not think 'I already wrote the HTML' means the form problem is solved.",
        "What repeated problems do Django Forms solve beyond generating input tags?",
        "https://docs.djangoproject.com/en/4.2/topics/forms/",
        """def submit_comment(request):
    errors = {}
    author_name = request.POST.get("author_name", "").strip()
    body = request.POST.get("body", "").strip()
    if not author_name:
        errors["author_name"] = "Required"
""",
        comparison=[
            ("Manual handling", "Read request.POST, cast strings, validate fields, repopulate old values, and render errors yourself."),
            ("Django Form", "Declare fields and validation once, then let is_valid(), cleaned_data, and errors drive the flow."),
        ],
        extras=[
            x("The same intent as a Form class", "Validation now lives in a reusable Python object instead of an ad-hoc view branch.", code="""class CommentForm(forms.Form):
    author_name = forms.CharField(max_length=120)
    body = forms.CharField(min_length=10, widget=forms.Textarea)
""", observe="The view can focus on control flow because the form owns coercion and errors."),
            x("Clean POST branch", "The form instance supports both initial render and POST validation.", code="""def submit_comment(request):
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Comment.objects.create(**form.cleaned_data)
        return redirect("blog:post-list")
    return render(request, "blog/comment_form.html", {"form": form})
""", observe="The same form instance feeds errors back into the template when invalid."),
        ],
    ),
    c(
        "DJ27", 4, "forms", "Django Forms", ["DJ21", "DJ17"],
        "A Django Form declares fields, widgets, coercion, and validation logic for user input independent of persistence.",
        "Input arrives as strings, but applications need typed, validated data with coherent error messages.",
        "A Form instance is a stateful validator: bound forms validate submitted data, unbound forms render empty defaults.",
        ["How field definitions, validators, clean_<field>(), and clean() interact", "What is_valid() actually does", "How form rendering and errors work in templates"],
        "Django Forms turn input handling into a reusable object so validation rules stay close to the fields they govern.",
        "Do not access cleaned_data before calling is_valid().",
        "What is the difference between clean_<field>() and clean()?",
        "https://docs.djangoproject.com/en/4.2/ref/forms/api/",
        """class NewsletterForm(forms.Form):
    email = forms.EmailField()
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        return email
""",
        extras=[
            x("Cross-field validation", "clean() is for constraints involving multiple fields together.", code="""class PublishForm(forms.Form):
    status = forms.ChoiceField(choices=[("draft", "Draft"), ("published", "Published")])
    published_at = forms.DateTimeField(required=False)
    def clean(self):
        data = super().clean()
        if data.get("status") == "published" and not data.get("published_at"):
            raise forms.ValidationError("published_at is required.")
        return data
""", observe="Use clean_<field>() for one field and clean() for cross-field rules."),
            x("Bound versus unbound", "The same Form class supports initial render and POST validation.", code="""form = NewsletterForm(request.POST or None)
if request.method == "POST" and form.is_valid():
    subscribe(form.cleaned_data["email"])
""", observe="Bound forms remember submitted values and errors for re-rendering."),
        ],
    ),
    c(
        "DJ28", 4, "forms", "ModelForms", ["DJ21", "DJ17"],
        "A ModelForm derives fields and save behavior from a model, making CRUD forms much smaller and more consistent.",
        "For data that already maps closely to a model, hand-declaring every form field duplicates the schema and drifts over time.",
        "ModelForm is a form adapter around a model: it maps form fields to model fields and can save an instance.",
        ["How Meta.model, fields, exclude, save(), and commit=False work", "When ModelForm is the right choice", "How inline formsets build on ModelForm relationships"],
        "Django derives form structure from model metadata to keep CRUD-heavy applications DRY and aligned with the domain schema.",
        "Do not blindly expose __all__ fields on externally facing forms.",
        "Why is commit=False useful in ModelForms?",
        "https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/",
        """class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "body", "tags"]
""",
        extras=[
            x("save(commit=False)", "Attach request-owned data before saving the instance.", code="""def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user.author
        post.save()
        form.save_m2m()
""", observe="Call save_m2m() after save(commit=False) when the form includes many-to-many fields."),
            x("Inline formsets build on ModelForms", "Editing a parent and its children together is a major ModelForm productivity win.", code="""CommentFormSet = inlineformset_factory(
    Post, Comment, fields=["author_name", "body", "is_public"], extra=1, can_delete=True
)
""", observe="The relationship metadata lets Django build repeated child forms from one definition."),
        ],
    ),
    c(
        "DJ29", 4, "forms", "Form Widgets", ["DJ21", "DJ17"],
        "Widgets control how form fields render and parse HTML, bridging Django's typed fields with concrete browser inputs.",
        "A field's validation rules are not enough; users still need appropriate controls and sane rendering defaults.",
        "Fields define validation semantics, widgets define HTML shape and browser interaction.",
        ["How built-in widgets map to common controls", "How to customize attrs and write a custom widget", "Why widget choice affects both UX and submitted data shape"],
        "Django separates widgets from fields so one validation rule can be rendered differently in different UI contexts.",
        "Do not confuse widget-level HTML attributes with authoritative validation rules.",
        "What is the difference between a Form field and a widget?",
        "https://docs.djangoproject.com/en/4.2/ref/forms/widgets/",
        """class ProfileForm(forms.Form):
    display_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your name"}))
    timezone = forms.ChoiceField(choices=TIMEZONE_CHOICES, widget=forms.Select)
    avatar = forms.ImageField(required=False, widget=forms.FileInput)
""",
        extras=[
            x("SplitDateTimeWidget", "One logical value can be rendered as multiple HTML inputs.", code="""published_at = forms.DateTimeField(
    required=False,
    widget=forms.SplitDateTimeWidget(date_attrs={"type": "date"}, time_attrs={"type": "time"}),
)
""", observe="The widget controls presentation while the field still yields one Python datetime."),
            x("Custom widget", "Custom widgets are justified when repeated HTML structure deserves a reusable component.", code="""class TagListWidget(forms.TextInput):
    template_name = "widgets/tag_list.html"
    def format_value(self, value):
        return ", ".join(value) if isinstance(value, (list, tuple)) else value
""", observe="Keep widgets small and presentation-focused."),
        ],
    ),
    c(
        "DJ30", 4, "forms", "Formsets", ["DJ21", "DJ17"],
        "Formsets let you manage multiple copies of the same form in one request, which is essential for bulk edit and parent-child edit screens.",
        "Hand-processing a dynamic number of repeated forms leads to brittle naming conventions and error handling logic.",
        "A formset is a managed collection of forms plus metadata describing how many forms were sent.",
        ["What the management form does", "How formset_factory, modelformset_factory, and inline formsets differ", "How to validate and save repeated forms safely"],
        "Django formalizes repeated-form input so the server can validate counts, deletion flags, and ordering without ad-hoc conventions.",
        "Do not strip out the management form because it looks like hidden boilerplate.",
        "Why is the management form mandatory in a Django formset?",
        "https://docs.djangoproject.com/en/4.2/topics/forms/formsets/",
        """InviteFormSet = formset_factory(InviteForm, extra=3, can_delete=True)
""",
        extras=[
            x("The management form", "These hidden fields tell Django how many forms were rendered and submitted.", code="""<form method="post">
  {% csrf_token %}
  {{ formset.management_form }}
  {% for form in formset %}
    {{ form.as_p }}
  {% endfor %}
</form>
""", lang="html", observe="If you omit management_form, the formset cannot trust the submitted payload shape."),
            x("Inline formset", "Inline formsets connect a parent model to related child rows cleanly.", code="""CommentFormSet = inlineformset_factory(
    Post, Comment, fields=["author_name", "body", "is_public"], extra=0, can_delete=True
)
""", observe="This is a common parent-child bulk edit pattern outside the admin too."),
        ],
    ),
    c(
        "DJ31", 4, "forms", "CSRF Protection", ["DJ21", "DJ17"],
        "CSRF protection stops a malicious site from tricking a browser into sending state-changing requests to your app with the user's cookies attached.",
        "Cookie-based auth is convenient, but browsers attach cookies automatically on cross-site requests, which creates a forgery risk for unsafe methods.",
        "The session cookie authenticates the browser; the CSRF token proves the request came from your own site.",
        ["How CSRF tokens are generated and validated", "Which attack CSRF prevents and which it does not", "How AJAX requests send the token header"],
        "Django ships CSRF middleware by default because cookie-based sessions are common and forgery attacks are subtle but severe.",
        "Do not disable CSRF on ordinary forms or JSON endpoints just to make a failing request 'work'.",
        "Why is CSRF mostly a cookie-auth problem, and how does Django validate the token?",
        "https://docs.djangoproject.com/en/4.2/ref/csrf/",
        """<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>
""",
        sample_lang="html",
        extras=[
            x("What the attack looks like", "Without a token, another site can submit a hidden form to your app and the browser still attaches the victim's session cookie.", code="""<!-- evil.example -->
<form action="https://blog.example.com/posts/42/delete/" method="post">
  <input type="hidden" name="confirm" value="yes">
</form>
<script>document.forms[0].submit()</script>
""", lang="html", observe="The attacker does not need to read the response. They only need the browser to send the forged write request."),
            x("AJAX requests need the header", "JavaScript clients must send the token explicitly on unsafe requests under session auth.", code="""fetch("/api/posts/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": getCookie("csrftoken"),
  },
  body: JSON.stringify({title: "Hello"}),
})
""", observe="The token is commonly read from the csrftoken cookie or rendered into the page."),
        ],
        mistakes=[
            ("Confusing CSRF with XSS or authentication.", "Treat CSRF, XSS, auth, and CORS as separate concerns that solve different problems."),
            ("Marking endpoints csrf_exempt to fix a broken client.", "Fix the client or move to a different auth architecture instead of removing the protection."),
        ],
    ),
    c(
        "DJ32", 5, "auth", "Django's Auth System", ["DJ18", "DJ26"],
        "Django's auth system provides users, passwords, permissions, groups, login state, and pluggable user-model customization.",
        "Authentication looks simple until you need password hashing, permission checks, admin integration, user references, and session-aware logins everywhere.",
        "Auth is not just a User table; it is models, middleware, backends, permission checks, and session state working together.",
        ["What the built-in auth app provides", "When to extend AbstractUser versus AbstractBaseUser", "Why AUTH_USER_MODEL must be chosen before the first migration"],
        "Django centralizes auth in a first-class app because identity, passwords, permissions, and sessions are cross-cutting platform concerns.",
        "Do not start a new project with hardcoded auth.User references if you already know a custom user model is likely.",
        "Why is changing AUTH_USER_MODEL after the first migration painful?",
        "https://docs.djangoproject.com/en/4.2/topics/auth/customizing/",
        """AUTH_USER_MODEL = "accounts.User"
""",
        extras=[
            x("Extending AbstractUser", "AbstractUser is the pragmatic choice when you only need extra fields and want to keep Django's default auth behavior.", code="""class User(AbstractUser):
    display_name = models.CharField(max_length=120, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
""", observe="You keep username/password/permission machinery and add project-specific fields."),
            x("Referencing the user model safely", "Reusable code should not hardcode auth.User.", code="""class AuditLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

User = get_user_model()
""", observe="Use settings.AUTH_USER_MODEL in model fields and get_user_model() elsewhere."),
        ],
        mistakes=[
            ("Leaving auth.User hardcoded in reusable code.", "Reference settings.AUTH_USER_MODEL and get_user_model() instead."),
            ("Choosing AbstractBaseUser for a modest customization.", "Prefer AbstractUser unless you truly need to replace Django's identity fields and manager behavior."),
        ],
    ),
    c(
        "DJ33", 5, "auth", "Authentication Views", ["DJ18", "DJ26"],
        "Django ships reusable login, logout, password change, and password reset views so ordinary authentication flows do not need reinvention.",
        "Auth flows are full of subtle security and UX details, especially email-based password reset.",
        "Authentication views are configured workflows around forms, tokens, sessions, templates, and email.",
        ["How the built-in auth views fit into URLconf and templates", "What the password reset email flow actually does", "Which pieces you customize through templates and settings"],
        "Django provides standard auth views because login and password reset flows are security-sensitive and repeated across most applications.",
        "Do not build a bespoke password reset flow unless you can justify and audit every security detail.",
        "What are the steps in Django's password reset flow?",
        "https://docs.djangoproject.com/en/4.2/topics/auth/default/",
        """urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
]
""",
        extras=[
            x("Custom login template", "You can still use the built-in views without accepting the defaults blindly.", code="""urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
]
""", observe="Templates and redirects are the main customization points."),
            x("Password reset flow", "Trace the full email-token-reset cycle so the security boundaries stay concrete.", diagram="""sequenceDiagram
    participant User
    participant Browser
    participant Django
    participant Email
    User->>Browser: Submit email
    Browser->>Django: POST password reset
    Django->>Email: Send signed reset link
    Email-->>User: Reset message
    User->>Browser: Open reset link
    Browser->>Django: GET confirm form
    Browser->>Django: POST new password
    Django-->>Browser: Success page
""", observe="The reset token rides in the email link and is checked by Django before accepting the new password."),
        ],
    ),
    c(
        "DJ34", 5, "auth", "Permissions & Groups", ["DJ18", "DJ26"],
        "Permissions and groups let Django express coarse-grained authorization rules across models, views, and admin actions.",
        "Authentication answers who the user is; authorization answers what they are allowed to do. Mixing the two creates insecure views.",
        "Users inherit permissions directly and through groups, and code asks explicit permission questions at the point of action.",
        ["How model permissions, custom permissions, and groups work", "How to enforce permissions in views and templates", "Where object-level permissions need extra tooling"],
        "Django models authorization explicitly because permission checks should be declarative and auditable instead of hidden in scattered conditionals.",
        "Do not mistake is_staff for a fine-grained permission system.",
        "What is the difference between model permissions and object-level permissions?",
        "https://docs.djangoproject.com/en/4.2/topics/auth/default/#permissions-and-authorization",
        """@permission_required("blog.change_post")
def publish_post(request, slug):
    ...
""",
        extras=[
            x("Custom permissions", "Django auto-creates add/change/delete/view permissions and lets you define more.", code="""class Post(models.Model):
    class Meta:
        permissions = [
            ("publish_post", "Can publish post"),
            ("feature_post", "Can mark post as featured"),
        ]
""", observe="Custom permissions map well to domain actions such as publish or feature."),
            x("Object-level permissions", "Per-object authorization is not built into core Django, which is why packages such as guardian exist.", code="""assign_perm("change_post", user, post)
if request.user.has_perm("change_post", post):
    ...
""", observe="Object-level rules matter when one editor may change only their own or their tenant's records."),
        ],
    ),
    c(
        "DJ35", 5, "auth", "Sessions", ["DJ18", "DJ26"],
        "Sessions store per-browser state on the server or in signed cookies so Django can remember login state and small user-specific values across requests.",
        "HTTP is stateless, but logins, carts, flash messages, and multi-step forms all need continuity across requests.",
        "The browser carries a session identifier cookie; Django maps it to stored session data via the configured backend.",
        ["What session backends trade off", "How session fixation and cookie settings affect security", "Why sessions remain Django's default web auth mechanism"],
        "Django defaults to sessions because server-rendered web apps naturally benefit from browser cookie plus server-side state authentication.",
        "Do not treat sessions as a general-purpose cache or a place to dump large arbitrary objects.",
        "How do Django sessions work, and what is session fixation?",
        "https://docs.djangoproject.com/en/4.2/topics/http/sessions/",
        """def set_timezone(request):
    request.session["timezone"] = "Asia/Kolkata"
""",
        extras=[
            x("Session backend selection", "Backends trade off speed, persistence, and operational complexity.", code="""SESSION_ENGINE = "django.contrib.sessions.backends.db"
# alternatives:
# django.contrib.sessions.backends.cache
# django.contrib.sessions.backends.cached_db
# django.contrib.sessions.backends.signed_cookies
""", observe="Database sessions are easy to reason about. Cache and signed-cookie sessions change durability and revocation trade-offs."),
            x("Session cookie hardening", "Cookie flags matter because sessions ride on browser cookies.", code="""SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
""", observe="Secure, HttpOnly, and SameSite reduce theft and cross-site abuse risk."),
        ],
    ),
    c(
        "DJ36", 5, "auth", "JWT & Token Auth", ["DJ18", "DJ26"],
        "JWT and token-based auth are alternative stateless or API-centric authentication strategies layered onto Django when browser sessions are not the right fit.",
        "Browser sessions are excellent for server-rendered apps, but APIs consumed by mobile apps or third parties often need header-based credentials.",
        "Sessions are browser-first and cookie-based; token auth moves proof of identity into Authorization headers or signed tokens.",
        ["Why Django defaults to sessions instead of JWT", "When DRF TokenAuthentication or SimpleJWT make sense", "What token lifecycle and revocation trade-offs look like"],
        "Django defaults to sessions because they fit classic web apps and keep logout and revocation straightforward on the server side.",
        "Do not adopt JWT just because it sounds modern; it adds token issuance, refresh, and revocation complexity.",
        "Why would a classic Django app prefer sessions over JWT?",
        "https://www.django-rest-framework.org/api-guide/authentication/",
        """REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}
""",
        comparison=[
            ("Sessions", "Cookie-based, server-side revocation, natural for browser flows and admin."),
            ("JWT", "Header-based, explicit refresh strategy, useful for mobile or third-party API clients."),
        ],
        extras=[
            x("SimpleJWT setup", "JWT introduces access and refresh token lifecycle concerns.", code="""REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}
""", observe="The strength is client independence from server session storage. The cost is revocation and rotation complexity."),
            x("Architecture fit", "Choose the credential style that matches the client, not the hype cycle.", compare=[
                ("Browser-backed app", "Sessions plus CSRF usually keep the stack simpler."),
                ("Mobile or partner API", "Bearer tokens or JWT may fit better."),
            ], observe="The question is client architecture, not trendiness."),
        ],
    ),
    c(
        "DJ37", 6, "rest", "Why DRF?", ["DJ32", "DJ13"],
        "Django REST Framework packages serialization, API views, auth, permissions, pagination, and browsable tooling for APIs on top of Django.",
        "A manual JSON API quickly repeats body parsing, validation, serialization, status handling, auth, and error formatting.",
        "DRF is to APIs what Django Forms and generic views are to HTML workflows: a structured stack around common patterns.",
        ["What work DRF removes from hand-written JSON views", "How serializers and API views mirror forms and generic views", "Why DRF is usually the default for serious Django APIs"],
        "DRF layers on top of Django so API development can reuse models, auth, permissions, and request/response infrastructure instead of inventing a separate stack.",
        "Do not start with DRF ViewSets if you do not understand the lower-level request and serializer flow first.",
        "What does DRF add beyond plain JsonResponse views?",
        "https://www.django-rest-framework.org/",
        """class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
""",
        comparison=[
            ("Manual JSON views", "You parse request.body, validate payloads, serialize objects, and choose status codes by hand."),
            ("DRF", "Serializers, generic views, permissions, throttles, and routers turn repeated API concerns into explicit building blocks."),
        ],
        extras=[
            x("Manual JSON endpoint", "This is the repeated API plumbing DRF is designed to remove.", code="""def post_list(request):
    if request.method == "GET":
        data = [{"id": str(post.id), "title": post.title} for post in Post.objects.all()]
        return JsonResponse(data, safe=False)
""", observe="Validation, serialization, and error handling all become custom work quickly."),
            x("DRF request cycle", "The API stack is layered just like Django's HTML stack.", diagram="""flowchart LR
    Client --> DRFRequest[DRF Request]
    DRFRequest --> Auth[Authentication]
    Auth --> Perm[Permissions]
    Perm --> Throttle[Throttles]
    Throttle --> Serializer[Serializer validation]
    Serializer --> ViewSet[APIView or ViewSet]
    ViewSet --> Response[DRF Response renderer]
    Response --> Client
""", observe="Authentication, permissions, throttles, serializers, and rendering are explicit API layers."),
        ],
    ),
    c(
        "DJ38", 6, "rest", "Serializers", ["DJ32", "DJ13"],
        "Serializers translate between Python objects and primitive API representations while also validating incoming API payloads.",
        "Model instances alone are not an API contract. APIs need clear output shape and input validation rules.",
        "A serializer is the API equivalent of a form plus a representation layer.",
        ["How Serializer and ModelSerializer validate and transform data", "How nested serializers and SerializerMethodField shape responses", "Where validate_<field>(), validate(), and to_representation() fit"],
        "DRF separates serialization from transport so one object defines API shape independent of the view logic.",
        "Do not put heavy database work into SerializerMethodField without understanding the query cost.",
        "What is the serializer validation flow from is_valid() to save()?",
        "https://www.django-rest-framework.org/api-guide/serializers/",
        """class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["id", "title", "slug", "comment_count"]
""",
        extras=[
            x("Field and object validation", "Validation flows through field coercion, validate_<field>(), and validate().", code="""class PublishSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["draft", "published"])
    published_at = serializers.DateTimeField(required=False)
    def validate(self, attrs):
        if attrs["status"] == "published" and "published_at" not in attrs:
            raise serializers.ValidationError("published_at is required.")
        return attrs
""", observe="Use field validators for one field and validate() for cross-field rules."),
            x("Nested output customization", "Serializers can expose richer representations than raw columns.", code="""class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name"]

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
""", observe="to_representation() is the last stop before the payload is returned."),
        ],
    ),
    c(
        "DJ39", 6, "rest", "Views in DRF", ["DJ32", "DJ13"],
        "DRF offers a spectrum from low-level APIView to high-level ModelViewSet so you can choose the right abstraction for each endpoint.",
        "One API endpoint might be custom business logic while another is standard CRUD, so one abstraction level does not fit every case.",
        "Move upward in abstraction only while the endpoint still matches the abstraction's assumptions.",
        ["How APIView, GenericAPIView, mixins, generics, and ViewSets differ", "What behavior each level adds", "How to decide between explicitness and terseness"],
        "DRF exposes multiple levels deliberately so teams can choose the smallest abstraction that still keeps the code clear.",
        "Do not choose ModelViewSet for endpoints with non-resource-shaped workflows just because it is short.",
        "What do you gain and lose as you move from APIView to ModelViewSet?",
        "https://www.django-rest-framework.org/api-guide/generic-views/",
        """class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
""",
        extras=[
            x("Same endpoint, different abstraction levels", "Seeing one endpoint at multiple levels makes the trade-off concrete.", compare=[
                ("APIView", "Most explicit, best for custom flows."),
                ("GenericAPIView + mixins", "Middle ground with reusable pieces."),
                ("ListCreateAPIView", "Concise for standard list/create resources."),
                ("ModelViewSet", "Best when the resource is fully CRUD-shaped."),
            ], observe="Choose the smallest abstraction that stays readable."),
            x("@action on a ViewSet", "Resource-adjacent custom behaviors fit naturally with @action.", code="""class PostViewSet(ModelViewSet):
    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.status = "published"
        post.save(update_fields=["status"])
        return Response({"status": post.status})
""", observe="detail=True creates an object-level custom endpoint such as POST /posts/{id}/publish/."),
        ],
    ),
    c(
        "DJ40", 6, "rest", "Authentication in DRF", ["DJ32", "DJ13"],
        "DRF authentication classes determine how request.user and request.auth are established for API requests.",
        "API clients are not all browsers, so session cookies are not always the right auth mechanism.",
        "Authentication classes inspect the incoming request, attempt to identify the client, and attach the result to request.user.",
        ["What SessionAuthentication, BasicAuthentication, TokenAuthentication, and JWTAuthentication imply", "How DEFAULT_AUTHENTICATION_CLASSES sets the baseline", "Why browser and third-party APIs often choose different auth styles"],
        "DRF keeps authentication pluggable because API clients and trust boundaries vary much more than classic server-rendered pages.",
        "Do not enable BasicAuthentication over plain HTTP or browser-heavy flows without understanding the UX and security implications.",
        "How do DRF authentication classes interact with request.user and permission checks?",
        "https://www.django-rest-framework.org/api-guide/authentication/",
        """REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}
""",
        extras=[
            x("Session auth fits browser-backed APIs", "If the same site serves HTML and JSON to an authenticated browser session, session auth is often the simplest choice.", code="""class BrowserOnlyAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
""", observe="SessionAuthentication still expects CSRF validation on unsafe methods."),
            x("JWT auth for non-browser clients", "Bearer tokens are common when mobile or third-party clients cannot rely on your site's session cookie.", code="""class PartnerAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
""", observe="The bearer token travels in the Authorization header instead of a Django session cookie."),
        ],
    ),
    c(
        "DJ41", 6, "rest", "Permissions in DRF", ["DJ32", "DJ13"],
        "DRF permissions decide whether the authenticated or anonymous request may access the endpoint or object.",
        "Authentication identifies the caller, but it does not tell you whether the action is allowed.",
        "Permissions are policy objects checked before or during object access, separate from serializer validation.",
        ["How built-in permission classes behave", "How object-level checks differ from view-level checks", "How to write custom permission classes"],
        "DRF separates authentication from authorization so API code can compose identity and policy independently.",
        "Do not rely on frontend behavior or serializer field omission as an authorization boundary.",
        "What is the difference between has_permission() and has_object_permission()?",
        "https://www.django-rest-framework.org/api-guide/permissions/",
        """class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
""",
        extras=[
            x("A custom object permission", "Safe methods can stay public while writes require ownership.", code="""class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author.user_id == request.user.id
""", observe="Object-level permissions matter when the endpoint is visible generally but individual objects have ownership rules."),
            x("Global defaults", "A project can define strict defaults and override them only when necessary.", code="""REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}
""", observe="Defaults reduce the chance of accidentally exposing a new endpoint with no policy."),
        ],
    ),
    c(
        "DJ42", 6, "rest", "Filtering, Searching, Ordering in DRF", ["DJ32", "DJ13"],
        "DRF integrates filtering, search, ordering, and pagination so collection endpoints remain predictable and scalable.",
        "List endpoints look simple until clients need multiple filters, keyword search, ordering, and stable pagination.",
        "Filtering narrows the queryset, ordering changes row order, and pagination slices the final result set in a consistent contract.",
        ["How django-filter, SearchFilter, and OrderingFilter compose", "Why filter backends belong with collection endpoints", "How page-number and cursor pagination trade off"],
        "DRF turns collection controls into explicit backends so the API contract stays discoverable and consistent across resources.",
        "Do not expose unrestricted ordering or filtering on sensitive or expensive fields casually.",
        "Why is cursor pagination better than page-number pagination for append-heavy feeds?",
        "https://www.django-rest-framework.org/api-guide/filtering/",
        """class PostViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "body", "author__name"]
    ordering_fields = ["published_at", "view_count"]
""",
        extras=[
            x("FilterSet for Blog posts", "django-filter keeps collection filtering declarative and testable.", code="""class PostFilter(django_filters.FilterSet):
    published_after = django_filters.DateTimeFilter(field_name="published_at", lookup_expr="gte")
    published_before = django_filters.DateTimeFilter(field_name="published_at", lookup_expr="lte")
    tag = django_filters.CharFilter(field_name="tags__slug")
""", observe="The filter definitions become part of the endpoint contract instead of ad-hoc request parsing."),
            x("Pagination trade-off", "Pagination is part of correctness as much as performance.", compare=[
                ("PageNumberPagination", "Simple and human-friendly, but unstable if rows are inserted between requests."),
                ("CursorPagination", "Stable for append-heavy feeds, but requires deterministic ordering."),
            ], observe="Choose the pagination style that matches the data and client expectations."),
        ],
    ),
    c(
        "DJ43", 6, "rest", "Throttling & Rate Limiting in DRF", ["DJ32", "DJ13"],
        "DRF throttles limit request rates to protect APIs from abuse, accidental floods, and expensive repeated access.",
        "Authentication and permissions do not stop a client from making too many legitimate-looking requests.",
        "Throttle classes count requests per identity scope over time and reject excess traffic with 429 responses.",
        ["How AnonRateThrottle, UserRateThrottle, and ScopedRateThrottle behave", "Where project-wide and per-view limits live", "How throttling complements infrastructure limits"],
        "DRF includes throttles because API abuse control belongs near the application boundary, even if stronger enforcement also exists upstream.",
        "Do not rely on application throttles alone for serious abuse protection.",
        "What is the difference between authorization and throttling?",
        "https://www.django-rest-framework.org/api-guide/throttling/",
        """REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
}
""",
        extras=[
            x("Scoped throttles", "Hot endpoints often need tighter limits than the global default.", code="""class SearchView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "search"
""", observe="Scopes let you name an endpoint class and give it a custom rate budget."),
            x("Custom throttle", "Custom throttles are useful for tenant-aware or plan-aware limits.", code="""class PartnerPlanThrottle(SimpleRateThrottle):
    scope = "partner"
    def get_cache_key(self, request, view):
        return f"partner:{request.user.id}"
""", observe="Throttle state usually lives in cache, so cache design affects behavior."),
        ],
    ),
    c(
        "DJ44", 6, "rest", "Versioning in DRF", ["DJ32", "DJ13"],
        "API versioning lets a service evolve without breaking existing clients that depend on older response shapes or behavior.",
        "Once APIs have external consumers, changing fields or semantics carelessly becomes a compatibility bug, not just a refactor.",
        "Versioning makes compatibility explicit at the API boundary rather than implicit in release notes.",
        ["How URL path, query parameter, and namespace versioning work", "When versioning is worth the overhead", "How version-aware views and serializers branch behavior safely"],
        "DRF supports multiple versioning schemes because different API ecosystems place the version marker in different places.",
        "Do not add versioning ceremony to a tiny internal API if the team can coordinate changes directly.",
        "When should you version an API, and what trade-offs come with URLPathVersioning?",
        "https://www.django-rest-framework.org/api-guide/versioning/",
        """REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
}
""",
        extras=[
            x("Version-aware serializer selection", "One ViewSet can branch representation by request version.", code="""class PostViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == "v2":
            return PostV2Serializer
        return PostV1Serializer
""", observe="Version-aware branching belongs at the API boundary, not scattered through clients."),
            x("Scheme trade-offs", "Different schemes optimize for different consumers and tooling.", compare=[
                ("URLPathVersioning", "/api/v1/posts/ is explicit and cache-friendly."),
                ("QueryParameterVersioning", "/api/posts/?version=v2 is easy to add but easy to forget."),
                ("NamespaceVersioning", "Fits projects already split by URL namespaces."),
            ], observe="Version only meaningful contract changes, not every internal refactor."),
        ],
    ),
    c(
        "DJ45", 6, "rest", "DRF Routers & URL Patterns", ["DJ32", "DJ13"],
        "Routers generate consistent REST-style URL patterns for ViewSets so resource endpoints remain predictable and concise.",
        "Hand-writing standard list/detail/update/delete patterns for every resource is repetitive and easy to make inconsistent.",
        "A router maps ViewSet actions to URL patterns and named routes in a convention-based way.",
        ["How SimpleRouter and DefaultRouter differ", "Which routes router.register() generates", "How @action adds custom endpoints"],
        "DRF uses routers because resource-oriented endpoints usually follow a stable pattern that should not be rewritten in every project.",
        "Do not force non-resource workflows into a router just because other endpoints use one.",
        "What URL patterns does router.register('posts', PostViewSet) generate?",
        "https://www.django-rest-framework.org/api-guide/routers/",
        """router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
urlpatterns = [path("api/", include(router.urls))]
""",
        extras=[
            x("Generated routes", "The main value is consistent list/detail/update/delete patterns.", code="""GET    /api/posts/
POST   /api/posts/
GET    /api/posts/{pk}/
PUT    /api/posts/{pk}/
PATCH  /api/posts/{pk}/
DELETE /api/posts/{pk}/
""", lang="text", observe="Routers make resource endpoints predictable for humans and clients."),
            x("@action", "Custom resource-adjacent behaviors still fit under the same router-driven resource.", code="""class PostViewSet(ModelViewSet):
    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        ...
""", observe="detail=True binds the action to one object. detail=False creates a collection-level action."),
        ],
    ),
    c(
        "DJ46", 7, "async", "Django Caching Framework", ["DJ12", "DJ14"],
        "Django's caching framework stores expensive computed results so repeated requests can avoid repeating the same work.",
        "Some pages are slow not because the code is complex, but because the same expensive query or render runs over and over for identical results.",
        "Cache keys map a stable input to a previously computed output for a limited period of time.",
        ["How per-site, per-view, fragment, and low-level caching differ", "Which cache backends Django supports", "Why cache invalidation and auth-aware caching need discipline"],
        "Django exposes caching at multiple layers because some optimizations belong around whole responses and others around specific expensive fragments or objects.",
        "Do not cache personalized responses without varying on the right dimensions.",
        "What is the cache-aside pattern, and why is invalidation harder than lookup?",
        "https://docs.djangoproject.com/en/4.2/topics/cache/",
        """def top_posts():
    key = "blog:top-posts:v1"
    data = cache.get(key)
    if data is None:
        data = list(Post.objects.published().order_by("-view_count")[:10])
        cache.set(key, data, timeout=300)
    return data
""",
        extras=[
            x("Per-view caching", "This is great for expensive public pages whose content is identical across many users.", code="""@cache_page(60 * 5)
def public_homepage(request):
    ...
""", observe="Be careful not to cache authenticated or personalized variants under one shared key."),
            x("Fragment caching", "Fragment caching is safer than whole-response caching when only one region is expensive.", code="""{% load cache %}
{% cache 300 "sidebar-top-posts" %}
  {% include "blog/_top_posts.html" %}
{% endcache %}
""", lang="html", observe="Vary keys carefully and invalidate fragments when the underlying data changes."),
        ],
    ),
    c(
        "DJ47", 7, "async", "Django Signals", ["DJ12", "DJ14"],
        "Signals let one part of the application react to events in another part without a direct function call, but that indirection is both the power and the trap.",
        "Some events need side effects in multiple places, yet hard-coded direct calls create coupling. Signals offer decoupling at the cost of traceability.",
        "A signal is an event broadcast. Receivers subscribe and run when the signal fires.",
        ["How built-in model and request signals work", "When signals help and when they hide control flow", "Why AppConfig.ready() is the right place to register receivers"],
        "Django includes signals as an optional decoupling mechanism, not as the default architecture for ordinary business workflows.",
        "Do not hide core multi-step workflows behind signals if explicit function calls would be easier to trace.",
        "What is the downside of signals, and when is an explicit service function better?",
        "https://docs.djangoproject.com/en/4.2/topics/signals/",
        """@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
""",
        extras=[
            x("Register receivers in AppConfig.ready()", "Import timing matters because receivers must be registered when the app is ready.", code="""class BlogConfig(AppConfig):
    name = "blog"
    def ready(self):
        import blog.signals  # noqa: F401
""", observe="Avoid scattering signal registration side effects across arbitrary imports."),
            x("Explicit alternative", "For core business workflows, explicit orchestration is often easier to reason about.", code="""@transaction.atomic
def register_user(*, email, password):
    user = User.objects.create_user(email=email, password=password)
    Profile.objects.create(user=user)
    return user
""", observe="When tracing behavior matters more than decoupling, explicit functions win."),
        ],
    ),
    c(
        "DJ48", 7, "async", "Celery with Django", ["DJ12", "DJ14"],
        "Celery moves slow or retry-prone work such as email, webhooks, image processing, and scheduled jobs out of the request cycle.",
        "If a view waits on network calls or expensive processing, the user pays that latency directly and transient failures are harder to retry cleanly.",
        "The web app enqueues a task to a broker; workers consume and execute it asynchronously.",
        ["How Celery fits with Redis as broker and beat for schedules", "What @shared_task, delay(), apply_async(), and retries do", "Why background work should usually start after transaction commit"],
        "Django stays request-centric; Celery handles work that should not block the response path or that needs independent retry semantics.",
        "Do not treat Celery as a fix for bad synchronous code design; decide which work truly belongs off-request.",
        "Why is Celery usually paired with transaction.on_commit()?",
        "https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html",
        """@shared_task(bind=True, autoretry_for=(ConnectionError,), retry_backoff=True)
def send_welcome_email(self, user_id):
    user = User.objects.get(pk=user_id)
    mail.send_mail("Welcome", "...", "noreply@example.com", [user.email])
""",
        extras=[
            x("Queue on commit", "External work that depends on new rows should wait for the transaction to commit.", code="""transaction.on_commit(lambda: send_welcome_email.delay(user.id))
""", observe="The worker should not race ahead of the database commit."),
            x("Periodic task", "Beat schedules recurring jobs and workers execute them like ordinary tasks.", code="""app.conf.beat_schedule = {
    "daily-digest": {
        "task": "blog.tasks.send_daily_digest",
        "schedule": crontab(hour=7, minute=0),
    },
}
""", observe="Daily digests, cleanup, and report generation are typical periodic-task candidates."),
        ],
    ),
    c(
        "DJ49", 7, "async", "Django Channels", ["DJ12", "DJ14"],
        "Django Channels extends Django into ASGI-based real-time protocols such as WebSockets so apps can handle bidirectional communication.",
        "Classic WSGI request/response handling cannot keep long-lived socket connections open for real-time updates.",
        "Channels adds consumers and channel layers on top of ASGI so events can move between clients and server processes in real time.",
        ["Why WebSockets require ASGI instead of pure WSGI", "How consumers and channel layers fit together", "When real-time channels are better than polling"],
        "Channels exists because HTTP request/response and WebSocket event streams are different protocols that need different runtime assumptions.",
        "Do not use WebSockets when low-frequency polling is simpler and good enough.",
        "Why can't classic WSGI handle WebSockets well?",
        "https://channels.readthedocs.io/en/stable/",
        """class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
    async def receive_json(self, content):
        await self.send_json({"echo": content})
""",
        extras=[
            x("WebSocket routing", "Channels uses a separate ASGI routing tree for non-HTTP protocols.", code="""websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_slug>[-\\w]+)/$", ChatConsumer.as_asgi()),
]
""", observe="The route points to a consumer instead of a view function."),
            x("Channel layer with Redis", "Redis-backed channel layers let multiple worker processes broadcast to the same room group.", code="""CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    },
}
""", observe="Without a shared channel layer, each process only knows about its own socket connections."),
        ],
    ),
    c(
        "DJ50", 8, "admin", "Django Admin", ["DJ13"],
        "The Django admin is a metadata-driven internal CRUD and workflow surface that can make trusted staff dramatically more productive.",
        "Internal operators still need management interfaces, and building them by hand for every model is slow and repetitive.",
        "Admin is a configurable site generated from model metadata plus ModelAdmin classes and inline definitions.",
        ["How to register models and customize list display, filters, search, readonly fields, and inlines", "Why admin is powerful for internal tools but risky on the public internet", "How to add custom admin actions"],
        "Django ships admin because many business apps need a trusted internal back office long before they need a polished custom CMS.",
        "Do not expose the admin on the public internet without strong authentication and operational hardening.",
        "What kinds of product needs fit the admin well, and when should you build a custom internal UI instead?",
        "https://docs.djangoproject.com/en/4.2/ref/contrib/admin/",
        """@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at")
    list_filter = ("status", "author")
    search_fields = ("title", "body", "author__name")
""",
        extras=[
            x("Inline comments", "Inlines are one of the biggest admin productivity wins for parent-child editing.", code="""class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
""", observe="Operators can inspect and edit related rows without leaving the parent page."),
            x("Custom action", "Admin actions let operators perform controlled bulk workflows.", code="""@admin.action(description="Mark selected posts as featured")
def mark_featured(modeladmin, request, queryset):
    queryset.update(status="featured")
""", observe="Admin actions are ideal for trusted internal bulk operations."),
        ],
    ),
    c(
        "DJ51", 8, "admin", "Management Commands", ["DJ13"],
        "Management commands package repeatable operational or data tasks behind the same settings and model context as the app.",
        "Teams always need imports, backfills, cleanup, and maintenance scripts, but random standalone files drift away from project configuration and safety checks.",
        "A management command is an executable entry point inside the Django project with parsed arguments and full app context.",
        ["How BaseCommand, add_arguments(), and handle() work", "Why commands beat ad-hoc scripts", "How dry-run flags and verbosity improve operational safety"],
        "Django packages project-aware automation behind manage.py so operations run with the same settings, models, and logging environment as the app.",
        "Do not hide destructive data changes behind a command without a dry-run or clear confirmation model.",
        "Why is a management command usually safer than a random standalone script?",
        "https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/",
        """class Command(BaseCommand):
    help = "Import posts from a CSV file"
    def add_arguments(self, parser):
        parser.add_argument("csv_path")
        parser.add_argument("--dry-run", action="store_true")
""",
        extras=[
            x("CSV import loop", "Commands should make safe rehearsal easy before changing data.", code="""def handle(self, *args, **options):
    with open(options["csv_path"], newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if options["dry_run"]:
                self.stdout.write(f"Would import: {row['title']}")
            else:
                Post.objects.update_or_create(slug=row["slug"], defaults={"title": row["title"]})
""", observe="Dry-run mode lets you validate parsing and counts before any write occurs."),
            x("call_command", "Commands are CLI entry points, but they can be reused from orchestrating code when appropriate.", code="""call_command("import_posts_from_csv", "seed/posts.csv", dry_run=True)
""", observe="Direct function reuse is often cleaner, but call_command exists when CLI parity matters."),
        ],
    ),
    c(
        "DJ52", 8, "admin", "App Architecture", ["DJ13"],
        "Django apps are feature modules, not necessarily deployable services, and their boundaries shape imports, ownership, and code reuse.",
        "Poor app boundaries create giant god-apps, circular imports, and confusion over where new code belongs.",
        "A Django app is a cohesive package around one domain area or reusable capability inside a larger project.",
        ["How apps.py, AppConfig, and ready() fit into app structure", "When to keep one app versus split into multiple apps", "Which common architecture anti-patterns make large projects painful"],
        "Django apps are intended as composable building blocks, which is why configuration, model registration, and discovery live at the app boundary.",
        "Do not split apps by technical layer alone if the domain boundaries remain tangled.",
        "How do you decide whether a Django project should be one app or many?",
        "https://docs.djangoproject.com/en/4.2/ref/applications/",
        """blog/
    admin.py
    apps.py
    forms.py
    models.py
    services.py
    urls.py
    views.py
""",
        sample_lang="text",
        extras=[
            x("AppConfig is the app boundary hook", "AppConfig carries metadata and startup hooks such as signal registration.", code="""class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
    verbose_name = "Blog"
""", observe="ready() should stay small because it runs during startup."),
            x("Architecture anti-patterns", "It is easier to avoid these early than to untangle them later.", compare=[
                ("Healthy split", "Apps reflect domains such as blog, accounts, billing, analytics."),
                ("Unhealthy split", "One giant core app or many tiny apps with constant cross-imports and no real ownership."),
            ], observe="Refactor toward domain ownership when the wrong shape becomes obvious."),
        ],
    ),
    c(
        "DJ53", 9, "testing", "Django Test Client", ["DJ18", "DJ26"],
        "The Django test client lets tests issue in-process HTTP requests against the project without running a real server.",
        "Without a framework-aware client, every integration-style test would need either a live server or direct function calls that skip routing and middleware.",
        "The test client simulates requests through the Django stack and returns real response objects for assertions.",
        ["How TestCase and Client exercise views and templates", "Which response assertions are most useful", "How login helpers and response.context accelerate tests"],
        "Django keeps the test client in-process so tests stay fast while still exercising URL routing, middleware, and view logic realistically.",
        "Do not use the test client as a substitute for lower-level unit tests when a function can be tested directly.",
        "What parts of the stack does the Django test client exercise?",
        "https://docs.djangoproject.com/en/4.2/topics/testing/tools/",
        """class PostListTests(TestCase):
    def setUp(self):
        self.client = Client()
    def test_list_page(self):
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)
""",
        extras=[
            x("POST and redirect flows", "The client can exercise form workflows and redirect chains too.", code="""response = self.client.post(
    "/accounts/login/",
    {"username": "alice", "password": "secret"},
    follow=True,
)
""", observe="follow=True is useful when you want to assert the destination page instead of only the redirect response."),
            x("JSON responses", "The test client can authenticate a user and inspect JSON payloads cleanly.", code="""user = User.objects.create_user(username="editor", password="secret")
self.client.login(username="editor", password="secret")
response = self.client.get("/api/health/")
self.assertEqual(response.json()["ok"], True)
""", observe="Use response.context, response.json(), and template assertions to prove behavior, not only status codes."),
        ],
    ),
    c(
        "DJ54", 9, "testing", "Factory Pattern for Test Data", ["DJ18", "DJ26"],
        "Factories build test data with clear defaults and composable relationships so tests stay focused on behavior instead of setup noise.",
        "Static fixtures become hard to read and brittle as the schema evolves, especially when relationships deepen.",
        "Factories are parameterized object builders with sensible defaults and override points.",
        ["Why factories usually age better than fixtures", "How SubFactory and LazyAttribute reduce setup duplication", "How to keep test data expressive instead of incidental"],
        "Factories keep tests local and intention-revealing because each test can shape only the parts of the data that matter.",
        "Do not build giant global fixture files for active application domains.",
        "Why do factories usually produce more maintainable tests than fixtures?",
        "https://factoryboy.readthedocs.io/en/stable/",
        """class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    name = factory.Sequence(lambda n: f"Author {n}")

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    author = factory.SubFactory(AuthorFactory)
""",
        extras=[
            x("LazyAttribute", "Factories can express relationships between fields without forcing every test to spell everything out.", code="""class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
    name = factory.Sequence(lambda n: f"Tag {n}")
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(" ", "-"))
""", observe="Derived defaults keep test data realistic while staying concise."),
            x("Readable tests", "Only the meaningful differences should be visible in the test body.", code="""post = PostFactory(status="published")
CommentFactory.create_batch(3, post=post, is_public=True)
response = self.client.get(post.get_absolute_url())
self.assertContains(response, post.title)
""", observe="Factories make the setup describe intent instead of construction mechanics."),
        ],
    ),
    c(
        "DJ55", 9, "testing", "Testing Views, Models, Forms", ["DJ18", "DJ26"],
        "Effective Django testing mixes unit tests for local behavior with integration tests for the paths where framework components cooperate.",
        "If every test hits the full stack, the suite gets slow and unclear. If every test is microscopic, integration regressions slip through.",
        "Test the smallest meaningful unit, then add targeted integration tests where components interact.",
        ["How to separate unit and integration concerns", "When TestCase versus TransactionTestCase matters", "How to mock external services without mocking the whole app"],
        "Django's testing tools support multiple levels so teams can balance speed, isolation, and realistic framework behavior.",
        "Do not mock Django itself when the framework behavior is part of what you need confidence in.",
        "What is the practical difference between TestCase and TransactionTestCase?",
        "https://docs.djangoproject.com/en/4.2/topics/testing/overview/",
        """class PostModelTests(TestCase):
    def test_published_post_requires_timestamp(self):
        post = Post(title="x", slug="x", status="published")
        with self.assertRaises(ValidationError):
            post.full_clean()
""",
        extras=[
            x("Form test", "Forms deserve direct tests because they own validation semantics.", code="""form = PublishForm(data={"status": "published"})
self.assertFalse(form.is_valid())
self.assertIn("published_at", form.errors.as_text())
""", observe="Keep view tests focused on control flow rather than validation minutiae."),
            x("Mock external boundaries", "Patch where the code under test looks up the dependency, not where the library originally lives.", code="""@patch("blog.services.mail.send_mail")
def test_welcome_email_sent(mock_send_mail):
    register_user(email="a@example.com", password="secret")
    mock_send_mail.assert_called_once()
""", observe="Mock only true boundaries or nondeterministic collaborators."),
        ],
    ),
    c(
        "DJ56", 9, "testing", "API Testing with DRF", ["DJ18", "DJ26"],
        "DRF adds API-focused test tools such as APIClient, APITestCase, and force_authenticate so JSON endpoints can be tested naturally.",
        "JSON APIs need different request bodies, auth helpers, and response assertions than ordinary HTML views.",
        "API tests should verify transport details, auth behavior, permissions, filtering, and pagination together.",
        ["How APIClient differs from Django's Client", "How to test auth, permissions, filters, and pagination", "Where force_authenticate is useful"],
        "DRF extends Django's test stack so API behavior can be asserted with the same clarity as HTML behavior.",
        "Do not assert only status codes on API tests; response shapes and permission edges matter too.",
        "When should you use APIClient.login(), credentials(), or force_authenticate()?",
        "https://www.django-rest-framework.org/api-guide/testing/",
        """class PostAPITests(APITestCase):
    def test_list_posts(self):
        PostFactory.create_batch(2, status="published")
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
""",
        extras=[
            x("force_authenticate", "This bypasses the full auth flow when the test is specifically about permission or view behavior.", code="""request = APIRequestFactory().get("/api/posts/")
force_authenticate(request, user=user)
response = PostViewSet.as_view({"get": "list"})(request)
""", observe="Useful for focused API tests that do not need the whole login flow."),
            x("Pagination and filtering", "Collection behavior is part of the public contract and deserves assertions.", code="""response = self.client.get("/api/posts/?page=2&ordering=-published_at&status=published")
self.assertIn("results", response.data)
self.assertIn("next", response.data)
""", observe="A list endpoint can be 'working' while still ignoring filters or pagination incorrectly."),
        ],
    ),
    c(
        "DJ57", 10, "ops", "Query Optimization", ["DJ53", "DJ54", "DJ55", "DJ56"],
        "Query optimization is the practice of measuring SQL behavior, fixing N+1 patterns, adding the right indexes, and reducing unnecessary data transfer.",
        "The most expensive Django pages usually fail because of query shape, not because Python is too slow.",
        "Measure first, then reduce query count, row count, transferred columns, and missing-index scans.",
        ["How Debug Toolbar and query inspection expose ORM problems", "When select_related, prefetch_related, only(), defer(), and indexes help", "How to validate improvements with EXPLAIN"],
        "Django keeps query inspection accessible because ORM ergonomics are only safe when developers can still see and measure the SQL underneath.",
        "Do not micro-optimize Python code before measuring database behavior on the endpoint.",
        "How would you take a Django page from 23 queries to 2?",
        "https://docs.djangoproject.com/en/4.2/topics/db/optimization/",
        """INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", *MIDDLEWARE]
INTERNAL_IPS = ["127.0.0.1"]
""",
        extras=[
            x("Reducing 23 queries to 2", "One query loads posts and authors; one more prefetches tags or comments.", code="""posts = (
    Post.objects.published()
    .select_related("author")
    .prefetch_related("tags")
)
""", observe="Fewer queries help only when the resulting SQL shape is still sane."),
            x("Indexes and projection", "Query count is not the whole story; a single unindexed or over-wide query can still be slow.", code="""class Post(models.Model):
    slug = models.SlugField(unique=True)
    class Meta:
        indexes = [models.Index(fields=["slug"])]

posts = Post.objects.only("id", "title", "slug")
""", observe="EXPLAIN should confirm that the database actually uses the new index."),
        ],
    ),
    c(
        "DJ58", 10, "ops", "Django Security Checklist", ["DJ53", "DJ54", "DJ55", "DJ56"],
        "Django ships strong security defaults, but production safety still depends on correct settings, deployment, and disciplined coding.",
        "Many serious breaches happen not because the framework lacks a feature, but because DEBUG stayed on, SECRET_KEY leaked, or HTTPS settings were incomplete.",
        "Security is layered: framework defaults, secure coding, headers, cookies, transport security, rate limiting, and operational hygiene all matter together.",
        ["What the major Django and browser-facing security settings do", "Which attacks Django mitigates automatically and which still require discipline", "How to turn the checklist into repeatable configuration"],
        "Django's security posture is strongest when its defaults are respected and the project finishes the last mile with correct production settings.",
        "Do not assume using Django means security is automatic regardless of settings and custom code.",
        "What does Django protect you from by default, and what still depends on your deployment and coding choices?",
        "https://docs.djangoproject.com/en/4.2/topics/security/",
        """DEBUG = False
ALLOWED_HOSTS = ["blog.example.com"]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
""",
        extras=[
            x("Production security settings", "These settings should look unsurprising in a serious HTTPS deployment.", code="""SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
""", observe="Most of these only make sense when the site is truly served over HTTPS end to end."),
            x("CSP and edge limits", "Security hardening spans both Django and the reverse proxy.", compare=[
                ("Django layer", "CSRF, permissions, session security, input validation, app-level throttles."),
                ("Edge layer", "HTTPS termination, request size limits, IP rate limiting, header normalization, WAF rules."),
            ], observe="Application and infrastructure controls should reinforce each other."),
        ],
        mistakes=[
            ("Leaving DEBUG=True in a deployed environment.", "Treat DEBUG=False as a hard production rule and test with it before deployment."),
            ("Committing SECRET_KEY or other secrets to source control.", "Load secrets from environment-specific secure stores, not the repository."),
        ],
    ),
    c(
        "DJ59", 10, "ops", "Deployment", ["DJ53", "DJ54", "DJ55", "DJ56"],
        "Django deployment is about turning a project into a reliable service: process model, static/media handling, secrets, health checks, logging, background workers, and rollout strategy.",
        "A locally working project is not a deployed system until web server, app server, database, cache, queues, storage, and observability all fit together.",
        "Deployments are pipelines of cooperating processes: reverse proxy, app server, database, cache, workers, and monitoring.",
        ["How WSGI or ASGI servers sit behind nginx or another reverse proxy", "What a practical Docker Compose stack looks like", "Why health checks, environment variables, and structured logging matter"],
        "Django stays deployment-agnostic at the code level while exposing WSGI and ASGI entry points so the runtime stack can fit the platform and protocols required.",
        "Do not hardcode secrets or environment-specific hostnames in settings.py.",
        "How would you deploy a production Django stack with background workers, health checks, and zero-downtime restarts?",
        "https://docs.djangoproject.com/en/4.2/howto/deployment/",
        """services:
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
  db:
    image: postgres:16
  redis:
    image: redis:7
""",
        sample_lang="yaml",
        extras=[
            x("Environment-driven settings and health check", "Production settings should be environment-aware and observable.", code="""SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool, default=False)

def healthz(request):
    db_ok = Post.objects.exists() or True
    cache_ok = cache.get_or_set("healthz", "ok", 5) == "ok"
    return JsonResponse({"ok": db_ok and cache_ok})
""", observe="A health endpoint is useful for load balancers and deployment systems."),
            x("Structured logging", "Operational excellence is mostly about visibility and safe rollouts.", code="""LOGGING = {
    "version": 1,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(levelname)s %(name)s %(message)s %(request_id)s",
        }
    },
}
""", observe="JSON logs make production events easier to search, aggregate, and alert on."),
        ],
        mistakes=[
            ("Serving Django directly to the internet with runserver.", "Use Gunicorn or Uvicorn behind a real reverse proxy or managed equivalent."),
            ("Treating deployment as only 'start the web process'.", "Think in terms of the full service topology: web, workers, db, cache, static files, migrations, and observability."),
        ],
    ),
]


def build_dependents():
    deps = defaultdict(list)
    for item in CONCEPTS:
        for prereq in item["prereqs"]:
            deps[prereq].append(item["id"])
    return dict(deps)


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


def render_compare(rows):
    cards = "".join(
        f"<article class='comparison-card'><h5>{escape(title)}</h5><p>{escape(text)}</p></article>"
        for title, text in rows
    )
    return f"<div class='comparison-grid'>{cards}</div>"


def render_mistakes(items):
    cards = "".join(
        "<article class='mistake-card'>"
        f"<h4>{escape(wrong)}</h4><p><strong>Right move:</strong> {escape(right)}</p>"
        "</article>"
        for wrong, right in items
    )
    return f"<div class='mistake-grid'>{cards}</div>"


def render_example(example, section_id, index):
    parts = [
        "<article class='example-card'>",
        f"<h4>Example {index}. {escape(example['title'])}</h4>",
        f"<p><strong>Why it matters:</strong> {escape(example['body'])}</p>",
    ]
    if example.get("compare"):
        parts.append(render_compare(example["compare"]))
    if example.get("diagram"):
        parts.append(f"<div class='mermaid-wrap'><div class='mermaid'>{escape(dedent(example['diagram']).strip())}</div></div>")
    if example.get("code"):
        parts.append(render_pre(example["code"], example.get("lang", "python")))
    if example.get("sql"):
        sql_id = f"{section_id}-sql-{index}"
        parts.append(
            f"<button class='sql-toggle' type='button' aria-expanded='false' aria-controls='{sql_id}'>Show generated SQL</button>"
            f"<div class='sql-panel' id='{sql_id}' hidden>{render_pre(example['sql'], 'sql', 'sql-block')}</div>"
        )
    if example.get("observe"):
        parts.append(f"<p><strong>What to observe:</strong> {escape(example['observe'])}</p>")
    parts.append("</article>")
    return "".join(parts)


def default_examples(item):
    examples = [
        x(
            "Minimal working shape",
            f"A compact snippet that shows the core shape of {item['title']}.",
            code=item["sample"],
            lang=item["sample_lang"],
            observe=item["mental"],
            sql=item.get("sample_sql"),
        ),
        x(
            "Without Django vs Django way",
            "This contrast makes the framework decision visible instead of treating it as convention.",
            compare=item["comparison"],
            observe=item["design"],
        ),
        x(
            "Common edge or failure mode",
            f"The dangerous path is usually using {item['title']} without understanding what it does at the boundary.",
            compare=[("Wrong move", item["mistakes"][0][0]), ("Better move", item["mistakes"][0][1])],
            observe=item["avoid"],
        ),
    ]
    examples.extend(item["extras"])
    return examples[:3]


def checks(item):
    return [
        (f"What problem does {item['title']} solve?", item["problem"]),
        (f"What mental model should you keep for {item['title']}?", item["mental"]),
        (f"When should you limit or avoid {item['title']}?", item["avoid"]),
    ]


def render_badges(ids):
    if not ids:
        return "<span class='badge badge-foundation'>No prerequisites</span>"
    return "".join(f"<a class='badge' href='#{escape(i)}'>{escape(i)}</a>" for i in ids)


def render_section(item, dependents, index):
    next_id = CONCEPTS[index + 1]["id"] if index + 1 < len(CONCEPTS) else "quick-reference"
    used_later = dependents.get(item["id"], [])
    version_html = ""
    if item.get("version"):
        version_html = (
            "<aside class='callout callout-version'>"
            "<div class='callout-title'>Version Note</div>"
            f"<div class='callout-body'>{escape(item['version'])}</div>"
            "</aside>"
        )
    if item.get("diagram"):
        diagram_html = f"<div class='mermaid-wrap'><div class='mermaid'>{escape(dedent(item['diagram']).strip())}</div></div>"
    else:
        diagram_html = f"<pre class='mental-model'><code>{escape(item['mental'])}</code></pre>"
    example_html = "".join(render_example(example, item["id"], i) for i, example in enumerate(default_examples(item), 1))
    check_html = "".join(
        f"<details class='self-check'><summary>{escape(q)}</summary><div>{escape(a)}</div></details>"
        for q, a in checks(item)
    )
    used_html = "".join(f"<a class='badge badge-subtle' href='#{escape(cid)}'>{escape(cid)}</a>" for cid in used_later[:8]) or "<span class='badge badge-subtle'>No direct dependents listed</span>"
    return f"""
<section id="{item['id']}" class="concept-section" data-layer="{item['layer']}" data-title="{escape(item['title'])}">
  <div class="section-kicker">{item['id']} &middot; Layer {item['layer']} &middot; {escape(LAYER_NAMES[item['layer']])}</div>
  <h2>{escape(item['title'])}</h2>
  <div class="section-meta">
    <div class="prereq-wrap"><span class="meta-label">Cluster</span><span class="cluster-pill {CLUSTER_CLASS[item['cluster']]}">{escape(item['cluster'].title())}</span></div>
    <div class="prereq-wrap"><span class="meta-label">Anchor</span><span class="badge badge-subtle">{item['id']}</span></div>
  </div>
  <div class="forward-links">
    <div class="prereq-wrap"><span class="meta-label">Read first</span>{render_badges(item['prereqs'])}</div>
    <div class="prereq-wrap"><span class="meta-label">Used later in</span>{used_html}</div>
    <p class="docs-link"><strong>Reference:</strong> <a href="{escape(item['docs'])}">{escape(item['docs'])}</a></p>
  </div>
  <div class="what-youll-learn"><h3>What you'll learn</h3><ul>{''.join(f"<li>{escape(line)}</li>" for line in item['learn'])}</ul></div>
  <h3>The Problem</h3>
  <aside class="callout callout-why"><div class="callout-title">Why this exists</div><div class="callout-body">{escape(item['problem'])}</div></aside>
  <h3>Concept Explanation</h3>
  <p>{escape(item['quick'])}</p>
  <p>{escape(item['problem'])} This section builds on {', '.join(item['prereqs']) or 'no earlier concept IDs'} and prepares you for {', '.join(used_later[:4]) or 'the later synthesis sections'}.</p>
  {version_html}
  <h3>Mental Model / Diagram</h3>
  {diagram_html}
  <h3>Worked Examples</h3>
  {example_html}
  <h3>Django-Specific Design Decision</h3>
  <aside class="callout callout-tip"><div class="callout-title">Why Django chose this</div><div class="callout-body">{escape(item['design'])}</div></aside>
  <h3>Common Mistakes</h3>
  {render_mistakes(item['mistakes'])}
  <aside class="callout callout-warning interview-card"><div class="callout-title">Common Interview Question</div><div class="callout-body">{escape(item['interview'])}</div></aside>
  <h3>Self-Check</h3>
  {check_html}
  <h3>Forward Links</h3>
  <p>This concept is used in: {used_html}</p>
  <div class="section-footer"><a class="prev-link" href="#dependency-table">Back to Dependency Table</a><a class="next-link" href="#{next_id}">Next concept &rarr; {next_id}</a></div>
</section>
"""


def render_dag():
    nodes = []
    edges = []
    for item in CONCEPTS:
        nodes.append(f'    {item["id"]}["{item["id"]} {item["title"]}"]:::{item["cluster"]}')
        for prereq in item["prereqs"]:
            edges.append(f"    {prereq} --> {item['id']}")
    return """graph TD
{nodes}
{edges}
    classDef foundation fill:#123526,stroke:#44b78b,color:#f5f3ea;
    classDef orm fill:#13332a,stroke:#64c8a2,color:#f5f3ea;
    classDef views fill:#153d2f,stroke:#89d7b6,color:#f5f3ea;
    classDef templates fill:#1a4735,stroke:#9de5c2,color:#f5f3ea;
    classDef forms fill:#20523c,stroke:#b7efd2,color:#f5f3ea;
    classDef auth fill:#18434e,stroke:#8bd0ff,color:#f5f3ea;
    classDef rest fill:#4a3a16,stroke:#ffcf70,color:#f5f3ea;
    classDef async fill:#54321b,stroke:#f3a771,color:#f5f3ea;
    classDef admin fill:#443058,stroke:#dcb6ff,color:#f5f3ea;
    classDef testing fill:#18494b,stroke:#90ddda,color:#f5f3ea;
    classDef ops fill:#2f6148,stroke:#f5f3ea,color:#f5f3ea;
""".format(nodes="\n".join(nodes), edges="\n".join(edges))


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
<section class='concept-section' id='dependency-table' data-title='Concept DAG & Dependencies'>
  <div class='section-kicker'>Task 2 &middot; Concept DAG</div>
  <h2>Django Concept DAG</h2>
  <p>The HTML section order follows this dependency graph. Each DJ identifier appears only after its prerequisites.</p>
  <div class='diagram-actions'><button class='diagram-action dag-download-btn' type='button' aria-label='Download Django concept DAG'>Download DAG</button></div>
  <div class='er-diagram'><div class='mermaid'>{escape(render_dag())}</div></div>
  <h3>All 59 Concepts</h3>
  <div class='table-wrap'><table><thead><tr><th>ID</th><th>Concept</th><th>Layer</th><th>Prerequisites</th><th>Dependents</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
"""


def render_lifecycle_ref():
    return f"""
<section class='concept-section' id='request-lifecycle' data-title='Request / Response Lifecycle'>
  <div class='section-kicker'>Task 2 &middot; Lifecycle</div>
  <h2>Django Request / Response Lifecycle</h2>
  <p>This diagram traces Browser to DNS to server adapter to middleware to URL resolution to view to ORM to database and back again.</p>
  <div class='er-diagram'><div class='mermaid'>{escape(REQUEST_SEQUENCE)}</div></div>
</section>
"""


def render_ecosystem_map():
    rows = [
        ("API", "Django REST Framework", "Serializers, viewsets, auth, and pagination."),
        ("Background work", "Celery", "Task queue for retries and schedules."),
        ("Realtime", "Channels", "ASGI + WebSockets for event streams."),
        ("Auth", "django-allauth", "Account workflows and social login."),
        ("Storage", "django-storages", "S3 and cloud storage backends."),
        ("Filtering", "django-filter", "Declarative filtering for DRF."),
        ("Testing", "factory_boy", "Factories for expressive test data."),
        ("Testing", "pytest-django", "pytest integration for Django."),
        ("Permissions", "django-guardian", "Object-level permissions."),
        ("Security", "django-csp", "Content Security Policy integration."),
    ]
    table = "".join(f"<tr><td>{escape(a)}</td><td>{escape(b)}</td><td>{escape(c)}</td></tr>" for a, b, c in rows)
    return f"""
<section class='concept-section' id='ecosystem-map' data-title='Django Ecosystem Map'>
  <div class='section-kicker'>Task 10 &middot; Ecosystem</div>
  <h2>Django Ecosystem Map</h2>
  <div class='table-wrap'><table><thead><tr><th>Category</th><th>Package</th><th>Why it exists</th></tr></thead><tbody>{table}</tbody></table></div>
</section>
"""


def render_quick_reference():
    rows = "".join(
        "<tr>"
        f"<td><a href='#{item['id']}'>{item['id']}</a></td>"
        f"<td>{item['layer']}</td>"
        f"<td>{escape(item['title'])}</td>"
        f"<td>{escape(item['quick'])}</td>"
        "</tr>"
        for item in CONCEPTS
    )
    return f"""
<section class='concept-section quick-reference' id='quick-reference' data-title='Quick Reference'>
  <div class='section-kicker'>Task 10 &middot; Quick Reference</div>
  <h2>All 59 Concepts at a Glance</h2>
  <div class='table-wrap'><table><thead><tr><th>ID</th><th>Layer</th><th>Concept</th><th>One-line Summary</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>
"""


def render_nav():
    by_layer = defaultdict(list)
    for item in CONCEPTS:
        by_layer[item["layer"]].append(item)
    parts = []
    parts.append(
        "<section class='nav-group' data-layer='ref'>"
        "<button class='group-toggle' type='button' data-layer='R' aria-expanded='true'><span>References</span><span>&#9662;</span></button>"
        "<div class='group-links'>"
        + "".join(
            f"<a href='#{target}' data-id='{target}'><span class='nav-dot'>R</span><span>{escape(label)}</span></a>"
            for target, label in REFERENCE_SECTIONS
        )
        + "</div></section>"
    )
    for layer in range(11):
        links = "".join(
            f"<a href='#{item['id']}' data-id='{item['id']}'><span class='nav-dot'>{layer}</span><span>{escape(item['id'] + ' · ' + item['title'])}</span></a>"
            for item in by_layer[layer]
        )
        parts.append(
            f"<section class='nav-group' data-layer='{layer}'>"
            f"<button class='group-toggle' type='button' data-layer='{layer}' aria-expanded='true'><span>{escape(NAV_LABELS[layer])}</span><span>&#9662;</span></button>"
            f"<div class='group-links'>{links}</div></section>"
        )
    return "".join(parts)


def render_shell(dependents):
    sections = "".join(render_section(item, dependents, index) for index, item in enumerate(CONCEPTS))
    return f"""<!DOCTYPE html>
<html lang='en' data-theme='dark'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Django Complete Reference</title>
<link rel='preconnect' href='https://fonts.googleapis.com'>
<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>
<link href='https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Lora:wght@400;500;600;700&family=Syne:wght@600;700;800&display=swap' rel='stylesheet'>
<link id='darkThemeStylesheet' rel='stylesheet' href='styles-dark.css'>
<link id='lightThemeStylesheet' rel='stylesheet' href='styles-light.css' media='not all'>
<link rel='preload' href='styles.css' as='style'>
<link rel='stylesheet' href='styles.css'>
<style>
html[data-theme='dark'] {{ --void:#092e20; --obsidian:#061f16; --deep:#0a261b; --surface:#103326; --surface2:#154433; --surface3:#1d5a45; --violet:#44b78b; --violet-dim:#28664f; --gold:#d9f5e7; --text-1:#f4efe5; --text-2:#bfd7c9; --font-head:'Syne',serif; --font-body:'Lora',serif; --font-code:'IBM Plex Mono',monospace; }}
html[data-theme='light'] {{ --paper:#f3f6f2; --paper2:#ecf2ec; --surface:#fbfdfb; --surface2:#f2f6f2; --surface3:#e7efe7; --forest:#0f5c40; --terra:#2d7c60; --font-head:'Syne',serif; --font-body:'Lora',serif; --font-code:'IBM Plex Mono',monospace; }}
.diagram-actions{{display:flex;justify-content:flex-end;margin:.85rem 0 1rem}} .diagram-action{{appearance:none;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);color:inherit;padding:.6rem .9rem;border-radius:10px;cursor:pointer;font-family:var(--font-code);font-size:.76rem}} html[data-theme='light'] .diagram-action{{border-color:rgba(26,74,46,.18);background:rgba(26,74,46,.04)}}
.sidebar-nav .group-links a{{display:grid;grid-template-columns:auto 1fr;gap:.6rem;align-items:start}} .nav-dot{{display:inline-flex;align-items:center;justify-content:center;min-width:1.5rem;height:1.5rem;border-radius:999px;font-size:.68rem;font-family:var(--font-code);border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04)}} html[data-theme='light'] .nav-dot{{border-color:rgba(26,74,46,.18);background:rgba(26,74,46,.06)}}
.cluster-pill{{display:inline-flex;align-items:center;border-radius:999px;padding:.2rem .6rem;font-family:var(--font-code);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em}} .cluster-foundation{{background:rgba(68,183,139,.14);color:#9df0ca}} .cluster-orm{{background:rgba(91,192,160,.14);color:#9df0ca}} .cluster-views{{background:rgba(127,208,178,.14);color:#c7f0de}} .cluster-templates{{background:rgba(152,219,191,.14);color:#d5f3e4}} .cluster-forms{{background:rgba(176,229,202,.14);color:#def7ea}} .cluster-auth{{background:rgba(140,210,255,.14);color:#d9f0ff}} .cluster-rest{{background:rgba(255,207,112,.14);color:#ffe4a2}} .cluster-async{{background:rgba(241,157,107,.14);color:#ffd6ba}} .cluster-admin{{background:rgba(220,182,255,.14);color:#f0ddff}} .cluster-testing{{background:rgba(140,215,211,.14);color:#d6f5f3}} .cluster-ops{{background:rgba(244,239,229,.14);color:#f4efe5}} html[data-theme='light'] .cluster-pill{{color:var(--forest)}}
.callout.callout-why,.callout.callout-warning,.callout.callout-tip,.callout.callout-version{{border-left-width:4px}} .callout.callout-why{{border-left-color:#44b78b}} .callout.callout-warning{{border-left-color:#ffcf70}} .callout.callout-tip{{border-left-color:#8cd2ff}} .callout.callout-version{{border-left-color:#dcb6ff}}
.comparison-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}} .comparison-card,.mistake-card,.mermaid-wrap,.er-diagram{{border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:1rem;background:rgba(255,255,255,.02)}} html[data-theme='light'] .comparison-card,html[data-theme='light'] .mistake-card,html[data-theme='light'] .mermaid-wrap,html[data-theme='light'] .er-diagram{{border-color:rgba(26,74,46,.14);background:rgba(255,255,255,.72)}} .mistake-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}} .docs-link{{margin-top:.85rem}}
.sql-toggle{{appearance:none;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.03);color:inherit;padding:.55rem .8rem;border-radius:10px;cursor:pointer;font-family:var(--font-code);font-size:.76rem;margin-top:.65rem}} html[data-theme='light'] .sql-toggle{{border-color:rgba(26,74,46,.18);background:rgba(26,74,46,.04)}} .sql-panel{{margin-top:.65rem}}
.layer-skeleton{{height:320px;border-radius:14px;background:linear-gradient(90deg,rgba(255,255,255,.03) 25%,rgba(255,255,255,.07) 50%,rgba(255,255,255,.03) 75%);background-size:200% 100%;animation:skeleton-sweep 1.4s ease infinite;border:1px solid rgba(255,255,255,.06);margin-bottom:1.4rem}} @keyframes skeleton-sweep{{0%{{background-position:200% 0}}100%{{background-position:-200% 0}}}}
@media (max-width:900px){{.comparison-grid,.mistake-grid{{grid-template-columns:1fr}}}}
</style>
<!-- REVIEW: Keep this inline theme bootstrap in <head>; moving it to the end of <body> would cause the wrong theme to flash before styles apply. -->
<script>
try {{
  const savedTheme = localStorage.getItem('django-reference-theme');
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
  </div>
  <nav class='sidebar-nav' aria-label='Django concept navigation'>{render_nav()}</nav>
</aside>
<main>
<section class='hero' id='top'>
  <div class='section-kicker'>Django Complete Reference</div>
  <h1>Django from HTTP Basics to Production Deployment</h1>
  <p>This document assumes Python fundamentals but no prior web-framework, HTTP, database, or backend architecture knowledge. The concept order follows the dependency graph so later sections never rely on unexplained earlier anchors.</p>
  <p>The running domain is a Blog application with Author, Profile, Post, Tag, and Comment models. That same domain reappears through ORM, views, templates, forms, auth, DRF, admin, testing, performance, and deployment.</p>
</section>
<div id='sectionMount' hidden aria-hidden='true'></div>
{render_dependency_table(dependents)}
{render_lifecycle_ref()}
{sections}
{render_ecosystem_map()}
{render_quick_reference()}
</main></div><button class='back-to-top' id='backToTop' aria-label='Back to top'>&uarr; Top</button>
<script defer src='https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'></script>
"""


def tail_script():
    return r"""
<script>
document.addEventListener('DOMContentLoaded', () => {
  const navLinks = [...document.querySelectorAll('.group-links a')];
  const sidebar = document.getElementById('sidebar');
  const mobileToggle = document.getElementById('mobileToggle');
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
  const THEME_STORAGE_KEY = 'django-reference-theme';
  let currentTheme = window.__initialTheme === 'light' ? 'light' : 'dark';
  let currentSectionId = virtualSections[0]?.id || orderedIds[0] || '';
  let activeObserver = null;
  let renderToken = 0;
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
    if (window.mermaid && typeof window.mermaid.initialize === 'function') {
      window.mermaid.initialize({ startOnLoad: false, securityLevel: 'loose', theme: nextTheme === 'dark' ? 'dark' : 'neutral' });
    }
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
  function bindSqlToggles(root) {
    root.querySelectorAll('.sql-toggle').forEach((button) => {
      if (button.dataset.toggleBound === 'true') return;
      button.addEventListener('click', () => {
        const panel = document.getElementById(button.getAttribute('aria-controls'));
        if (!panel) return;
        const expanded = button.getAttribute('aria-expanded') === 'true';
        button.setAttribute('aria-expanded', String(!expanded));
        button.textContent = expanded ? 'Show generated SQL' : 'Hide generated SQL';
        panel.hidden = expanded;
      });
      button.dataset.toggleBound = 'true';
    });
  }
  function initMermaid(root) {
    if (!window.mermaid || typeof window.mermaid.initialize !== 'function') return;
    window.mermaid.initialize({ startOnLoad: false, securityLevel: 'loose', theme: currentTheme === 'dark' ? 'dark' : 'neutral' });
    const blocks = [...root.querySelectorAll('.mermaid')];
    if (!blocks.length) return;
    blocks.forEach((block) => {
      block.textContent = (block.textContent || '').trim();
      block.removeAttribute('data-processed');
    });
    if (typeof window.mermaid.run === 'function') {
      window.mermaid.run({ nodes: blocks });
    } else if (typeof window.mermaid.init === 'function') {
      window.mermaid.init(undefined, blocks);
    }
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
    link.download = 'django-concept-dag.svg';
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
    bindSqlToggles(section);
    bindDagDownloads(section);
    initMermaid(section);
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
  bindSqlToggles(document);
  bindDagDownloads(document);
  initMermaid(document);
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
</body></html>
"""


def build_document():
    dependents = build_dependents()
    return render_shell(dependents) + tail_script()


def main():
    OUTFILE.write_text(build_document(), encoding="utf-8")
    print(f"Wrote {OUTFILE}")


if __name__ == "__main__":
    main()
