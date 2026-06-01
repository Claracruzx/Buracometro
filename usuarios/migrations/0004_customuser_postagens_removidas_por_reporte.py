from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0003_customuser_foto"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="postagens_removidas_por_reporte",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
