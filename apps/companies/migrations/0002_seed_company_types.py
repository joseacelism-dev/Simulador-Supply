from django.db import migrations


COMPANY_TYPES = [
    (
        "Empresa de alimentos procesados",
        "Compra de materias primas perecederas, produccion por lotes, cadena de frio, almacenamiento, distribucion y devoluciones.",
    ),
    (
        "Empresa de confecciones",
        "Gestion de telas e insumos, tallas, colores, corte, confeccion, calidad, empaque, distribucion y devoluciones.",
    ),
    (
        "Empresa farmaceutica",
        "Proveedores certificados, materias primas controladas, trazabilidad por lote, vencimientos, calidad y retiros de producto.",
    ),
    (
        "Empresa de comercio electronico",
        "Centros de distribucion, inventarios de alta variedad, pedidos en linea, ultima milla, cambios y garantias.",
    ),
    (
        "Empresa agroindustrial y exportadora",
        "Abastecimiento rural, transformacion, empaque, transporte nacional, exportacion, logistica internacional y desperdicios.",
    ),
]


def seed_company_types(apps, schema_editor):
    CompanyType = apps.get_model("companies", "CompanyType")
    for name, description in COMPANY_TYPES:
        CompanyType.objects.get_or_create(
            name=name,
            defaults={"description": description, "is_active": True},
        )


def remove_company_types(apps, schema_editor):
    CompanyType = apps.get_model("companies", "CompanyType")
    CompanyType.objects.filter(name__in=[name for name, _ in COMPANY_TYPES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_company_types, remove_company_types),
    ]

