from django.db import models

from apps.companies.models import Company


class Simulation(models.Model):
    class Status(models.TextChoices):
        CONFIGURATION = "configuracion", "Configuracion"
        READY = "lista", "Lista para iniciar"
        IN_PROGRESS = "en_curso", "En curso"
        PERIOD_OPEN = "periodo_abierto", "Periodo abierto"
        DECISIONS_REGISTERED = "decisiones_registradas", "Decisiones registradas"
        PROCESSING = "procesando", "Procesando"
        PERIOD_CLOSED = "periodo_cerrado", "Periodo cerrado"
        FINISHED = "finalizada", "Finalizada"
        CANCELLED = "cancelada", "Cancelada"

    class Periodicity(models.TextChoices):
        DAYS = "dias", "Dias"
        WEEKS = "semanas", "Semanas"
        MONTHS = "meses", "Meses"
        QUARTERS = "trimestres", "Trimestres"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="simulations",
        verbose_name="empresa",
    )
    name = models.CharField("nombre", max_length=160)
    scenario = models.CharField("escenario", max_length=160, default="Demanda estable")
    total_periods = models.PositiveIntegerField("periodos totales", default=6)
    periodicity = models.CharField(
        "periodicidad",
        max_length=20,
        choices=Periodicity.choices,
        default=Periodicity.MONTHS,
    )
    status = models.CharField(
        "estado",
        max_length=40,
        choices=Status.choices,
        default=Status.PERIOD_OPEN,
    )
    current_period_number = models.PositiveIntegerField("periodo actual", default=1)
    created_at = models.DateTimeField("creada", auto_now_add=True)
    updated_at = models.DateTimeField("actualizada", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "simulacion"
        verbose_name_plural = "simulaciones"

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.company.owner

    @property
    def is_finished(self):
        return self.status == self.Status.FINISHED

    def get_current_period(self):
        return self.periods.filter(number=self.current_period_number).first()


class SimulationPeriod(models.Model):
    class Status(models.TextChoices):
        OPEN = "abierto", "Abierto"
        DECISIONS_REGISTERED = "decisiones_registradas", "Decisiones registradas"
        PROCESSING = "procesando", "Procesando"
        CLOSED = "cerrado", "Cerrado"

    simulation = models.ForeignKey(
        Simulation,
        on_delete=models.CASCADE,
        related_name="periods",
        verbose_name="simulacion",
    )
    number = models.PositiveIntegerField("numero")
    status = models.CharField(
        "estado",
        max_length=40,
        choices=Status.choices,
        default=Status.OPEN,
    )
    opened_at = models.DateTimeField("apertura", auto_now_add=True)
    closed_at = models.DateTimeField("cierre", null=True, blank=True)

    class Meta:
        ordering = ["number"]
        verbose_name = "periodo de simulacion"
        verbose_name_plural = "periodos de simulacion"
        constraints = [
            models.UniqueConstraint(
                fields=["simulation", "number"],
                name="unique_period_number_per_simulation",
            )
        ]

    def __str__(self):
        return f"{self.simulation} - periodo {self.number}"

    @property
    def is_open(self):
        return self.status in {
            self.Status.OPEN,
            self.Status.DECISIONS_REGISTERED,
        }


class Decision(models.Model):
    class Area(models.TextChoices):
        GENERAL = "general", "General"
        DEMAND = "demanda", "Demanda"
        PURCHASING = "compras", "Compras"
        INVENTORY = "inventarios", "Inventarios"
        PRODUCTION = "produccion", "Produccion"
        DISTRIBUTION = "distribucion", "Distribucion"
        FINANCE = "finanzas", "Finanzas"

    period = models.ForeignKey(
        SimulationPeriod,
        on_delete=models.CASCADE,
        related_name="decisions",
        verbose_name="periodo",
    )
    area = models.CharField("area", max_length=30, choices=Area.choices, default=Area.GENERAL)
    title = models.CharField("titulo", max_length=160)
    description = models.TextField("descripcion")
    created_at = models.DateTimeField("registrada", auto_now_add=True)
    locked = models.BooleanField("bloqueada", default=False)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "decision"
        verbose_name_plural = "decisiones"

    def __str__(self):
        return self.title


class SimulationEvent(models.Model):
    class Severity(models.TextChoices):
        INFO = "informativa", "Informativa"
        PREVENTIVE = "preventiva", "Preventiva"
        IMPORTANT = "importante", "Importante"
        CRITICAL = "critica", "Critica"

    period = models.ForeignKey(
        SimulationPeriod,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name="periodo",
    )
    name = models.CharField("nombre", max_length=160)
    description = models.TextField("descripcion")
    severity = models.CharField(
        "severidad",
        max_length=30,
        choices=Severity.choices,
        default=Severity.INFO,
    )
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "evento de simulacion"
        verbose_name_plural = "eventos de simulacion"

    def __str__(self):
        return self.name


class PeriodResult(models.Model):
    period = models.OneToOneField(
        SimulationPeriod,
        on_delete=models.CASCADE,
        related_name="result",
        verbose_name="periodo",
    )
    available_capital = models.DecimalField(
        "capital disponible",
        max_digits=14,
        decimal_places=2,
    )
    product_count = models.PositiveIntegerField("productos", default=0)
    raw_material_count = models.PositiveIntegerField("materias primas", default=0)
    supplier_count = models.PositiveIntegerField("proveedores", default=0)
    customer_count = models.PositiveIntegerField("clientes", default=0)
    decision_count = models.PositiveIntegerField("decisiones", default=0)
    operational_score = models.DecimalField(
        "puntaje operacional",
        max_digits=6,
        decimal_places=2,
        default=0,
    )
    summary = models.TextField("resumen")
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        verbose_name = "resultado de periodo"
        verbose_name_plural = "resultados de periodo"

    def __str__(self):
        return f"Resultado {self.period}"

