# kanban_app/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    # Boards
    BoardListCreateView,
    BoardDetailView,
    BoardCurrentDraftView,
    # Tasks
    TaskListCreateView,
    TaskDetailView,
    # Comments
    CommentListCreateView,
    CommentDeleteView,
    # User‑bezogene Task‑Filter
    AssignedToMeTaskListView,
    ReviewingTaskListView,
    # Misc
    EmailCheckView,
    # Debriefing
    DebriefingViewSet,
    # Graphics‑Rapport  ← NEU
    GraphicsRapportViewSet,
)

# ------------------------------------------------------------------
# DRF Router – registriert alle standard CRUD‑Pfad­e
# ------------------------------------------------------------------
router = DefaultRouter()
router.register(r"debriefings",        DebriefingViewSet,       basename="debriefing")
router.register(r"graphics-rapports",  GraphicsRapportViewSet,  basename="graphics-rapport")  # ← NEU

# ------------------------------------------------------------------
# API URL patterns for KanMind (Kanban) application.
# ------------------------------------------------------------------
urlpatterns = [
    # Board‑spezifische Endpunkte
    path("boards/",          BoardListCreateView.as_view(), name="board-list-create"),
    path("boards/<int:pk>/", BoardDetailView.as_view(),    name="board-detail"),

    # Draft‑Endpunkt (erstellt automatisch einen Draft, falls keiner offen)
    path(
        "boards/<int:pk>/current-draft/",
        BoardCurrentDraftView.as_view(),
        name="board-current-draft",
    ),

    # Task‑Endpunkte
    path("tasks/",       TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/assigned-to-me/",
        AssignedToMeTaskListView.as_view(),
        name="tasks-assigned-to-me",
    ),
    path(
        "tasks/reviewing/",
        ReviewingTaskListView.as_view(),
        name="tasks-reviewing",
    ),

    # Comment‑Endpunkte
    path(
        "tasks/<int:task_id>/comments/",
        CommentListCreateView.as_view(),
        name="comment-list-create",
    ),
    path(
        "tasks/<int:task_id>/comments/<int:pk>/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),

    # Email‑Check
    path("email-check/", EmailCheckView.as_view(), name="email-check"),

    # Router‑basierte Endpunkte (Debriefing & Graphics‑Rapport)
    path("", include(router.urls)),
]