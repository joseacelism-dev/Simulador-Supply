from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.companies.models import Company, CompanyType

from .models import Decision, PeriodResult, Simulation, SimulationEvent, SimulationPeriod


class SimulationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        self.company_type = CompanyType.objects.create(name="Alimentos", description="Prueba")
        self.company = Company.objects.create(
            owner=self.user,
            company_type=self.company_type,
            name="Alimentos Ana",
            city="Bogota",
            target_market="Supermercados",
            initial_capital="1000000",
        )

    def test_student_can_create_simulation_for_own_company(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("simulations:create_for_company", args=[self.company.pk]),
            {
                "name": "Simulacion base",
                "scenario": "Demanda estable",
                "total_periods": 3,
                "periodicity": Simulation.Periodicity.MONTHS,
            },
        )

        simulation = Simulation.objects.get(name="Simulacion base")
        self.assertRedirects(response, reverse("simulations:detail", args=[simulation.pk]))
        self.assertEqual(simulation.status, Simulation.Status.PERIOD_OPEN)
        self.assertEqual(simulation.periods.count(), 1)

    def test_student_cannot_view_another_student_simulation(self):
        other = User.objects.create_user(username="luis", password="ClaveSegura123!")
        simulation = Simulation.objects.create(company=self.company, name="Privada")
        SimulationPeriod.objects.create(simulation=simulation, number=1)
        self.client.force_login(other)

        response = self.client.get(reverse("simulations:detail", args=[simulation.pk]))

        self.assertEqual(response.status_code, 404)

    def test_student_can_register_decision_in_open_period(self):
        simulation = Simulation.objects.create(company=self.company, name="Simulacion")
        SimulationPeriod.objects.create(simulation=simulation, number=1)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("simulations:decision_create", args=[simulation.pk]),
            {
                "area": Decision.Area.GENERAL,
                "title": "Mantener estrategia",
                "description": "Decision inicial para validar el motor.",
            },
        )

        self.assertRedirects(response, reverse("simulations:detail", args=[simulation.pk]))
        self.assertEqual(Decision.objects.filter(period__simulation=simulation).count(), 1)

    def test_process_period_generates_result_event_and_next_period(self):
        simulation = Simulation.objects.create(
            company=self.company,
            name="Simulacion",
            total_periods=2,
        )
        period = SimulationPeriod.objects.create(simulation=simulation, number=1)
        Decision.objects.create(
            period=period,
            area=Decision.Area.GENERAL,
            title="Decision",
            description="Prueba",
        )
        self.client.force_login(self.user)

        response = self.client.post(reverse("simulations:process_period", args=[simulation.pk]))

        simulation.refresh_from_db()
        period.refresh_from_db()
        self.assertRedirects(response, reverse("simulations:detail", args=[simulation.pk]))
        self.assertEqual(period.status, SimulationPeriod.Status.CLOSED)
        self.assertEqual(simulation.current_period_number, 2)
        self.assertEqual(simulation.status, Simulation.Status.PERIOD_OPEN)
        self.assertTrue(PeriodResult.objects.filter(period=period).exists())
        self.assertTrue(SimulationEvent.objects.filter(period=period).exists())

    def test_teacher_can_view_simulation_list(self):
        teacher = User.objects.create_user(
            username="docente",
            password="ClaveSegura123!",
            role=User.Role.ADMIN_DOCENTE,
            is_staff=True,
        )
        self.client.force_login(teacher)

        response = self.client.get(reverse("simulations:teacher_list"))

        self.assertEqual(response.status_code, 200)

