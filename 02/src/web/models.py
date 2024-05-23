from django.db import models


class Search(models.Model):
    day_name = models.CharField(
        verbose_name="Day (name)",
        max_length=100,
        choices=(
            ("Lunes", "Lunes"),
            ("Martes", "Martes"),
            ("Miércoles", "Miércoles"),
            ("Jueves", "Jueves"),
            ("Viernes", "Viernes"),
            ("Sábado", "Sábado"),
            ("Domingo", "Domingo"),
        ),
        blank=False,
    )
    enterprise = models.CharField(
        verbose_name="Enterprise",
        max_length=100,
        choices=(
            ("Grupo LATAM", "Grupo LATAM"),
            ("Sky Airline", "Sky Airline"),
            ("Aerolineas Argentinas", "Aerolineas Argentinas"),
            ("Copa Air", "Copa Air"),
            ("Latin American Wings", "Latin American Wings"),
            ("Avianca", "Avianca"),
            ("JetSmart SPA", "JetSmart SPA"),
            ("Gol Trans", "Gol Trans"),
            ("American Airlines", "American Airlines"),
            ("Air Canada", "Air Canada"),
            ("Iberia", "Iberia"),
            ("Delta Air", "Delta Air"),
            ("Air France", "Air France"),
            ("Aeromexico", "Aeromexico"),
            ("United Airlines", "United Airlines"),
            ("Oceanair Linhas Aereas", "Oceanair Linhas Aereas"),
            ("Alitalia", "Alitalia"),
            ("K.L.M.", "K.L.M."),
            ("British Airways", "British Airways"),
            ("Qantas Airways", "Qantas Airways"),
            ("Lacsa",  "Lacsa"),
            ("Austral", "Austral"),
            ("Plus Ultra Lineas Aereas", "Plus Ultra Lineas Aereas"),
        ),
        blank=False,
    )
    month_name = models.CharField(
        verbose_name="Month (name)",
        max_length=100,
        choices=(
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ),
        blank=False,
    )
    date_to_search = models.DateTimeField(
        verbose_name="Date",
        blank=False,
    )
    type_flight = models.CharField(
        verbose_name="Type (flight)",
        max_length=100,
        choices=(
            ("I", "International"),
            ("N", "National"),
        ),
        blank=False,
    )
    prediction = models.BooleanField(
        verbose_name="has delay",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.id)