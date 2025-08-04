# kanban_app/models.py
from django.db import models
from auth_app.models import User


# -------------------------------------------------------------------------
# Board
# -------------------------------------------------------------------------
class Board(models.Model):
    """
    Kanban‑Board mit Titel, Owner, Members.
    """
    title = models.CharField(
        max_length=100,
        help_text="The title of the board (max. 100 characters)."
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_boards",
        help_text="The user who owns this board."
    )
    members = models.ManyToManyField(
        User,
        related_name="boards",
        help_text="Users who are members of this board."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -------------------------------------------------------------------------
# Task
# -------------------------------------------------------------------------
class Task(models.Model):
    """
    Einzelne Karte im Board.
    """
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    STATUS_CHOICES = [
        ("to-do",      "To Do"),
        ("in-progress","In Progress"),
        ("review",     "Review"),
        ("done",       "Done"),
    ]
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="to-do",
    )

    PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="tasks_assigned",
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="tasks_reviewing",
    )
    due_date   = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.board.title})"


# -------------------------------------------------------------------------
# Comment
# -------------------------------------------------------------------------
class Comment(models.Model):
    """
    Thread‑Kommentar zu einem Task.
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments",
    )
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        author = self.author.email if self.author else "Unknown"
        return f"Comment by {author} on task '{self.task.title}'"


# -------------------------------------------------------------------------
# Debriefing – SFL
# -------------------------------------------------------------------------
class Debriefing(models.Model):
    """
    Wöchentlicher SFL‑Rapport (Draft → Final → PDF).
    """
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        FINAL = "FINAL", "Final"

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="debriefings",
    )
    match_date   = models.DateField()
    status       = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_by   = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at   = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    # Beispiel‑Feld – zukünftige Felder analog hinzufügen
    kick_off_ok = models.BooleanField(default=True)

    def __str__(self):
        return f"Debriefing {self.match_date} ({self.board.title})"


# -------------------------------------------------------------------------
# Graphics‑Rapport – NEU
# -------------------------------------------------------------------------
class GraphicsRapport(models.Model):
    """
    Match‑bezogener GFX‑Rapport (Draft → Final → optional PDF).
    Aufbau und Status‑Flow analog zum Debriefing.
    """
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        FINAL = "FINAL", "Final"

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="graphics_rapports",
    )
    match_date   = models.DateField()
    status       = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_by   = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at   = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    # Beispiel‑Feld – kann durch echte Felder ersetzt/erweitert werden
    graphics_test_ok = models.BooleanField(default=True)

    def __str__(self):
        return f"GFX‑Rapport {self.match_date} ({self.board.title})"