# Generated by Django 3.1.5 on 2021-02-12 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210213_0149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'แบรนด์สินค้า', 'verbose_name_plural': 'ข้อมูลแบรนด์สินค้า'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'หมวดหมู่สินค้า', 'verbose_name_plural': 'ข้อมูลประเภทสินค้า'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'สินค้า', 'verbose_name_plural': 'ข้อมูลสินค้า'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category'),
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
