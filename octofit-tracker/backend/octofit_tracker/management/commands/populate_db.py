from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear collections
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User(email='tony@marvel.com', name='Tony Stark', team='Marvel'),
            User(email='steve@marvel.com', name='Steve Rogers', team='Marvel'),
            User(email='clark@dc.com', name='Clark Kent', team='DC'),
            User(email='diana@dc.com', name='Diana Prince', team='DC'),
        ]
        for user in users:
            user.save()

        # Create activities
        activities = [
            Activity(user_email='tony@marvel.com', type='Running', duration=30),
            Activity(user_email='steve@marvel.com', type='Cycling', duration=45),
            Activity(user_email='clark@dc.com', type='Swimming', duration=60),
            Activity(user_email='diana@dc.com', type='Yoga', duration=50),
        ]
        for activity in activities:
            activity.save()

        # Create leaderboard
        Leaderboard.objects.create(team='Marvel', points=75)
        Leaderboard.objects.create(team='DC', points=110)

        # Create workouts
        workouts = [
            Workout(name='HIIT', difficulty='Hard'),
            Workout(name='Cardio Blast', difficulty='Medium'),
            Workout(name='Strength Training', difficulty='Hard'),
            Workout(name='Yoga Flow', difficulty='Easy'),
        ]
        for workout in workouts:
            workout.save()


        # Ensure unique index on email using pymongo
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
