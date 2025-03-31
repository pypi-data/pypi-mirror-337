import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0003_project_project_manager_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactHistory',
            fields=[
                ('pseudonym', models.CharField(editable=False, max_length=64, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactHistoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Not reached'), (1, 'Recall'), (2, 'Invited')], default=0, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('contact_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_history_items', to='subject_contact_history.contacthistory')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.project')),
            ],
        ),
    ]
