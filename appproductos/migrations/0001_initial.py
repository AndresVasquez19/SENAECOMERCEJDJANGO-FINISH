# Generated by Django 4.1.6 on 2023-03-30 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripCategoria', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'categoría',
                'verbose_name_plural': 'categorías de productos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=300, null=True)),
                ('precioUnitario', models.DecimalField(decimal_places=2, max_digits=8)),
                ('unidad', models.CharField(max_length=10)),
                ('existencia', models.IntegerField(null=True)),
                ('imgGrande', models.ImageField(null=True, upload_to='productos')),
                ('imgPeque', models.ImageField(null=True, upload_to='iconos')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appproductos.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Carro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('valUnit', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estado', models.CharField(choices=[('activo', 'activo'), ('comprado', 'comprado'), ('anulado', 'anulado')], default='activo', max_length=20)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appproductos.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
