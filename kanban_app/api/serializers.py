# kanban_app/api/serializers.py
from rest_framework import serializers

from kanban_app.models import (
    Board,
    Task,
    Comment,
    Debriefing,
    GraphicsRapport,           # ← NEU
)
from auth_app.models import User


# ---------------------------------------------------------------------------
#  USER
# ---------------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    """
    Gibt immer einen sprechenden Namen zurück:
    - full_name, falls vorhanden
    - sonst die E‑Mail‑Adresse
    """
    fullname = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = ("id", "email", "fullname")

    def get_fullname(self, obj):
        return getattr(obj, "full_name", obj.email)


# ---------------------------------------------------------------------------
#  COMMENT
# ---------------------------------------------------------------------------
class CommentSerializer(serializers.ModelSerializer):
    """
    Minimale Darstellung (z. B. in Task‑Detailansicht)
    """
    author  = serializers.SerializerMethodField()
    content = serializers.CharField(source="text")

    class Meta:
        model  = Comment
        fields = ("id", "created_at", "author", "content")

    def get_author(self, obj):
        if obj.author:
            return getattr(obj.author, "full_name", obj.author.email)
        return "Unknown"


# ---------------------------------------------------------------------------
#  TASK – Detail‑Serializer (inkl. Kommentare)
# ---------------------------------------------------------------------------
class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display",
                                           read_only=True)
    comments   = CommentSerializer(many=True, read_only=True)
    assignee   = UserSerializer(read_only=True)
    reviewer   = UserSerializer(read_only=True)

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        write_only=True,
        required=False,
        allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model  = Task
        read_only_fields = ("id", "created_by", "created_at", "comments")
        fields = (
            "id", "board", "title", "description",
            "status", "status_display", "priority",
            "assignee", "assignee_id",
            "reviewer", "reviewer_id",
            "due_date",
            "created_by", "created_at",
            "comments",
        )


# ---------------------------------------------------------------------------
#  TASK – Listen‑Serializer (kompakter, aber mit Comment‑Count)
# ---------------------------------------------------------------------------
class TaskListSerializer(serializers.ModelSerializer):
    assignee        = UserSerializer(read_only=True)
    reviewer        = UserSerializer(read_only=True)
    comments_count  = serializers.SerializerMethodField()

    class Meta:
        model  = Task
        fields = (
            "id", "board", "title", "description",
            "status", "priority",
            "assignee", "reviewer",
            "due_date", "comments_count",
        )

    def get_comments_count(self, obj):
        return obj.comments.count()


# ---------------------------------------------------------------------------
#  BOARD
# ---------------------------------------------------------------------------
class BoardSerializer(serializers.ModelSerializer):
    members   = UserSerializer(many=True, read_only=True)
    tasks     = TaskListSerializer(many=True, read_only=True)
    owner_id  = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model  = Board
        read_only_fields = ("id", "owner_id", "created_at")
        fields = ("id", "title", "owner_id", "members", "tasks", "created_at")


# ---------------------------------------------------------------------------
#  DEBRIEFING (bestehend)
# ---------------------------------------------------------------------------
class DebriefingSerializer(serializers.ModelSerializer):
    """
    Vollständiges CRUD‑Serializer für den SFL‑Rapport.
    `created_by`, `created_at`, `submitted_at` werden vom System gesetzt.
    """
    class Meta:
        model  = Debriefing
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "submitted_at")


# ---------------------------------------------------------------------------
#  GRAPHICS‑RAPPORT (NEU)
# ---------------------------------------------------------------------------
class GraphicsRapportSerializer(serializers.ModelSerializer):
    """
    Vollständiges CRUD‑Serializer für den Graphics‑Rapport.
    Analog zu Debriefing: System setzt created_by, created_at, submitted_at.
    """
    class Meta:
        model  = GraphicsRapport
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "submitted_at")