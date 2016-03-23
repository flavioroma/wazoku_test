from central.models import Challenge, Idea, IdeaVote, Site, User

from django.core import mail
from django.test import TestCase
from scripts import user_activity_export


class UserActivityExportTests(TestCase):

    def setUp(self):
        self.site, _ = Site.objects.get_or_create(domain="example.com")

        # Create some users
        self.contributor = User(
            username="contributor",
            email="contributor@example.com",
            first_name="Regular",
            last_name="User",
            is_contributor=True,
            site=self.site
        )
        self.contributor.save()

        self.manager = User(
            username="manager",
            email="manager@example.com",
            first_name="Mr",
            last_name="Manager",
            is_manager=True,
            site=self.site
        )
        self.manager.save()

        # Create a challenge and idea
        self.challenge = Challenge(
            name="Example challenge",
            description="A simple challenge for our tests",
            creator=self.manager,
            site=self.site
        )
        self.challenge.save()

        self.idea = Idea(
            name='Test idea for our challenge',
            summary='Simple idea',
            challenge=self.challenge,
            creator=self.contributor,
            site=self.site
        )
        self.idea.save()

        IdeaVote(creator=self.contributor, idea=self.idea).save()

    def test_export_script_sends_email(self):
        user_activity_export.main("example.com", "manager@example.com")

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'User Activity Export')

        # Test we have a single recipient
        self.assertEqual(len(mail.outbox[0].to), 1)

        # Verify that the recipient is the manager
        self.assertEqual(mail.outbox[0].to[0], "manager@example.com")

    def test_export_only_sends_emails_to_managers(self):
        self.manager.is_manager = False
        self.manager.save()
        user_activity_export.main("example.com", "manager@example.com")

        # Test that no message has been sent.
        self.assertEqual(len(mail.outbox), 0)
