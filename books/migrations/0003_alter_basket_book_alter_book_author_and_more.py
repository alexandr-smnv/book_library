# Generated by Django 4.2.5 on 2023-10-09 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_basket"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basket",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="books.book"
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="books.author"
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="books.category"
            ),
        ),
    ]
