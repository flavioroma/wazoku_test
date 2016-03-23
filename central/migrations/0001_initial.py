# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('is_deleted', models.BooleanField(default=False, db_index=True)),
                ('is_private', models.BooleanField(default=False)),
                ('is_parallel', models.BooleanField(default=False)),
                ('has_stats', models.BooleanField(default=True)),
                ('is_team_enabled', models.BooleanField(default=False)),
                ('send_idea_submitted_email', models.BooleanField(default=False)),
                ('idea_submitted_email_content', models.TextField(null=True)),
                ('image_url', models.CharField(max_length=150, null=True)),
                ('is_spotlight_share_enabled', models.BooleanField(default=True)),
                ('is_yammer_share_enabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False, db_index=True)),
                ('is_external', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'Active', max_length=50, choices=[(b'Active', b'Active'), (b'Exported', b'Exported'), (b'Deleted', b'Deleted')])),
                ('type', models.CharField(default=b'Open', max_length=50, choices=[(b'Open', b'Open'), (b'By Request', b'By Request'), (b'Invite Only', b'Invite Only')])),
                ('primary_media_url', models.CharField(max_length=150, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('question', models.TextField(blank=True)),
                ('status', models.CharField(default=b'pending', max_length=50, choices=[(b'Active', b'Active'), (b'Pending', b'Pending'), (b'Closed', b'Closed')])),
                ('is_deleted', models.BooleanField(default=False, db_index=True)),
                ('image_url', models.CharField(max_length=150, null=True)),
                ('start_datetime', models.DateTimeField(null=True, blank=True)),
                ('close_datetime', models.DateTimeField(null=True, blank=True)),
                ('share_message', models.TextField(default='', blank=True)),
                ('community', models.ForeignKey(related_name='conversations', blank=True, to='central.Community', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('status', models.CharField(default=b'Concept', max_length=50, db_index=True, choices=[(b'Concept', b'Concept'), (b'In Review', b'In Review'), (b'Approved', b'Approved'), (b'Completed', b'Completed')])),
                ('is_deleted', models.BooleanField(default=False, db_index=True)),
                ('summary', models.TextField(blank=True)),
                ('image_url', models.CharField(max_length=150, null=True)),
                ('score', models.DecimalField(default=0, max_digits=20, decimal_places=15)),
                ('is_progressing', models.BooleanField(default=False, db_index=True)),
                ('is_draft', models.BooleanField(default=False, db_index=True)),
                ('popularity', models.IntegerField(default=0, db_index=True)),
                ('num_upvotes', models.PositiveIntegerField(default=0, db_index=True)),
                ('num_downvotes', models.PositiveIntegerField(default=0, db_index=True)),
                ('num_visits', models.PositiveIntegerField(default=0, db_index=True)),
                ('num_comments', models.PositiveIntegerField(default=0, db_index=True)),
                ('challenge', models.ForeignKey(related_name='ideas', to='central.Challenge', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IdeaComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False, db_index=True)),
                ('comment', models.TextField(default=b'')),
                ('edited_datetime', models.DateTimeField(null=True)),
                ('is_advisor_comment', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='IdeaVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_upvote', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_siteadmin', models.BooleanField(default=False)),
                ('is_contributor', models.BooleanField(default=True)),
                ('is_limited_contributor', models.BooleanField(default=False)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_advisor', models.BooleanField(default=False)),
                ('username', models.EmailField(max_length=254, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('first_name', models.CharField(max_length=255, blank=True)),
                ('last_name', models.CharField(max_length=255, blank=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('display_name', models.CharField(max_length=50, blank=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'db_table': 'central_user',
            },
        ),
        migrations.AddField(
            model_name='ideavote',
            name='creator',
            field=models.ForeignKey(related_name='ideavote', to='central.User'),
        ),
        migrations.AddField(
            model_name='ideavote',
            name='idea',
            field=models.ForeignKey(related_name='votes', to='central.Idea'),
        ),
        migrations.AddField(
            model_name='ideacomment',
            name='creator',
            field=models.ForeignKey(related_name='ideacomment', to='central.User'),
        ),
        migrations.AddField(
            model_name='ideacomment',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_ideacomments', to='central.User'),
        ),
        migrations.AddField(
            model_name='ideacomment',
            name='parent',
            field=models.ForeignKey(related_name='responses', blank=True, to='central.IdeaComment', help_text=b'Other comment this is responding to', null=True),
        ),
        migrations.AddField(
            model_name='ideacomment',
            name='response_to',
            field=models.ForeignKey(related_name='comments', to='central.Idea'),
        ),
        migrations.AddField(
            model_name='ideacomment',
            name='site',
            field=models.ForeignKey(to='sites.Site'),
        ),
        migrations.AddField(
            model_name='idea',
            name='creator',
            field=models.ForeignKey(related_name='ideas', to='central.User'),
        ),
        migrations.AddField(
            model_name='idea',
            name='site',
            field=models.ForeignKey(to='sites.Site'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='creator',
            field=models.ForeignKey(related_name='creator_conversations', to='central.User', null=True),
        ),
        migrations.AddField(
            model_name='conversation',
            name='followers',
            field=models.ManyToManyField(related_name='followed_conversations', to='central.User'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='site',
            field=models.ForeignKey(to='sites.Site'),
        ),
        migrations.AddField(
            model_name='community',
            name='applicants',
            field=models.ManyToManyField(related_name='applicant_communities', to='central.User'),
        ),
        migrations.AddField(
            model_name='community',
            name='banned_members',
            field=models.ManyToManyField(related_name='banned_members_communities', to='central.User'),
        ),
        migrations.AddField(
            model_name='community',
            name='creator',
            field=models.ForeignKey(related_name='creator_communities', to='central.User'),
        ),
        migrations.AddField(
            model_name='community',
            name='managers',
            field=models.ManyToManyField(related_name='manager_communities', to='central.User'),
        ),
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(related_name='member_communities', to='central.User'),
        ),
        migrations.AddField(
            model_name='community',
            name='site',
            field=models.ForeignKey(to='sites.Site'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='community',
            field=models.ForeignKey(related_name='challenges', blank=True, to='central.Community', null=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='creator',
            field=models.ForeignKey(related_name='challenges', to='central.User'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='followers',
            field=models.ManyToManyField(related_name='followed_challenges', to='central.User'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='site',
            field=models.ForeignKey(to='sites.Site'),
        ),
        migrations.AlterUniqueTogether(
            name='ideavote',
            unique_together=set([('creator', 'idea')]),
        ),
    ]
