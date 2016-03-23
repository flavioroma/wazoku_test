from django.contrib.auth.models import AbstractBaseUser
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser):
    # Basic User fields.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Roles for users.
    is_siteadmin = models.BooleanField(default=False)
    is_contributor = models.BooleanField(default=True)
    is_limited_contributor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_advisor = models.BooleanField(default=False)

    username = models.EmailField(blank=True, null=True)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    site = models.ForeignKey(Site)
    display_name = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'central_user'
        app_label = 'central'


class TimestampModel(models.Model):
    """An abstract model that provides self-updating 'created' and 'modified' fields"""
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'central'


class Community(TimestampModel):
    """
    This model represents a community on the website.
    """

    TYPE_CHOICES = (
        ('Open', 'Open'),
        ('By Request', 'By Request'),
        ('Invite Only', 'Invite Only'),
    )

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Exported', 'Exported'),
        ('Deleted', 'Deleted')
    )
    site = models.ForeignKey(Site)

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    is_external = models.BooleanField(default=False)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Active',
    )
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='Open',
    )
    applicants = models.ManyToManyField(User, related_name='applicant_communities')
    managers = models.ManyToManyField(User, related_name='manager_communities')
    members = models.ManyToManyField(User, related_name='member_communities')
    banned_members = models.ManyToManyField(
        User,
        related_name='banned_members_communities'
    )
    creator = models.ForeignKey(User, related_name='creator_communities')
    primary_media_url = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        app_label = 'central'


class Challenge(TimestampModel):
    """
    This model represents a challenge on the site, which contains a number
    of ideas.
    """

    community = models.ForeignKey(
        Community,
        blank=True,
        null=True,
        related_name='challenges'
    )
    site = models.ForeignKey(Site)

    name = models.CharField(max_length=150)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False, db_index=True)
    is_private = models.BooleanField(default=False)
    is_parallel = models.BooleanField(default=False)

    creator = models.ForeignKey(User, related_name='challenges')
    has_stats = models.BooleanField(default=True)
    is_team_enabled = models.BooleanField(default=False)
    send_idea_submitted_email = models.BooleanField(default=False)
    idea_submitted_email_content = models.TextField(null=True)
    image_url = models.CharField(max_length=150, null=True)
    is_spotlight_share_enabled = models.BooleanField(default=True)
    is_yammer_share_enabled = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, related_name='followed_challenges')

    class Meta:
        app_label = 'central'


class Idea(TimestampModel):
    """
    This object represent an idea on the spotlight website, which is posted
    in a challenge.
    """
    STATUS_CHOICES = (
        ('Concept', 'Concept'),
        ('In Review', 'In Review'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed')
    )
    site = models.ForeignKey(Site)

    challenge = models.ForeignKey(Challenge, related_name='ideas', null=True)
    name = models.CharField(max_length=150)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Concept',
        db_index=True,
    )
    is_deleted = models.BooleanField(default=False, db_index=True)
    creator = models.ForeignKey(
        User,
        related_name='ideas',
    )
    summary = models.TextField(blank=True)
    image_url = models.CharField(max_length=150, null=True)
    score = models.DecimalField(max_digits=20, decimal_places=15, default=0)
    is_progressing = models.BooleanField(default=False, db_index=True)
    is_draft = models.BooleanField(default=False, db_index=True)
    popularity = models.IntegerField(default=0, db_index=True)
    num_upvotes = models.PositiveIntegerField(default=0, db_index=True)
    num_downvotes = models.PositiveIntegerField(default=0, db_index=True)
    num_visits = models.PositiveIntegerField(default=0, db_index=True)
    num_comments = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        app_label = 'central'


class Conversation(TimestampModel):
    """
    This model represents a conversation on the website. A conversation
    is a type of forum thread on a site, which may or may not be associated
    with a community.
    """
    ACTIVE = u'active'
    PENDING = u'pending'
    CLOSED = u'closed'

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    )
    site = models.ForeignKey(Site)

    name = models.CharField(max_length=150)
    question = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    is_deleted = models.BooleanField(default=False, db_index=True)
    community = models.ForeignKey(
        Community,
        related_name='conversations',
        blank=True,
        null=True,
    )
    image_url = models.CharField(max_length=150, null=True)
    creator = models.ForeignKey(
        User,
        related_name='creator_conversations',
        null=True
    )

    followers = models.ManyToManyField(User, related_name='followed_conversations')

    # The time a conversation should be scheduled to open.
    start_datetime = models.DateTimeField(blank=True, null=True)
    # The time a conversation should be scheduled to close.
    close_datetime = models.DateTimeField(blank=True, null=True)

    share_message = models.TextField(blank=True, default=u'')

    class Meta:
        app_label = 'central'


class Comment(TimestampModel):
    """
    This is an abstract class for comments on the spotlight website.
    """
    parent = models.ForeignKey(
        'self',
        related_name='responses',
        blank=True,
        null=True,
        help_text='Other comment this is responding to',
    )
    is_deleted = models.BooleanField(default=False, db_index=True)
    creator = models.ForeignKey(User, related_name="%(class)s")
    comment = models.TextField(default="")
    liked_by = models.ManyToManyField(User, related_name="liked_%(class)ss")
    edited_datetime = models.DateTimeField(null=True)
    site = models.ForeignKey(Site)

    class Meta:
        abstract = True
        app_label = 'central'


class IdeaComment(Comment):
    """Comment for Idea"""
    response_to = models.ForeignKey(Idea, related_name='comments')
    is_advisor_comment = models.BooleanField(default=False)

    class Meta:
        app_label = 'central'


class Vote(TimestampModel):
    """
    This model represents a vote by a particular user. The vote can either
    be an 'up vote' or a 'down vote', depending on the value of
    :py:attr:`is_upvote`.
    """
    creator = models.ForeignKey(User, related_name="%(class)s")
    is_upvote = models.BooleanField(default=True)

    class Meta:
        abstract = True
        app_label = 'central'


class IdeaVote(Vote):
    idea = models.ForeignKey(Idea, related_name='votes')

    class Meta:
        unique_together = (('creator', 'idea'),)
        app_label = 'central'
