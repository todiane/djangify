from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0010_alter_technology_options"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Project",
            new_name="Portfolio",
        ),
        migrations.RenameModel(
            old_name="ProjectImage",
            new_name="PortfolioImage",
        ),
        migrations.AlterModelOptions(
            name="Portfolio",
            options={"ordering": ["order", "-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="PortfolioImage",
            options={"ordering": ["order"]},
        ),
    ]
