from django.core.management.base import BaseCommand

from central.models import Challenge, Idea, IdeaVote, Site, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        site, _ = Site.objects.get_or_create(domain="example.com")

        # Create some users
        contributor = User(
            username="contributor",
            email="contributor@example.com",
            first_name="Regular",
            last_name="User",
            is_contributor=True,
            site=site
        )
        contributor.save()

        manager = User(
            username="manager",
            email="manager@example.com",
            first_name="Mr",
            last_name="Manager",
            is_manager=True,
            site=site
        )
        manager.save()

        # Create a challenge and idea
        challenge = Challenge(
            name="Example challenge",
            description="A simple challenge for our tests",
            creator=manager,
            site=site
        )
        challenge.save()

        idea = Idea(
            name='Test idea for our challenge',
            summary='Simple idea',
            challenge=challenge,
            creator=contributor,
            site=site
        )
        idea.save()

        IdeaVote(creator=contributor, idea=idea).save()
