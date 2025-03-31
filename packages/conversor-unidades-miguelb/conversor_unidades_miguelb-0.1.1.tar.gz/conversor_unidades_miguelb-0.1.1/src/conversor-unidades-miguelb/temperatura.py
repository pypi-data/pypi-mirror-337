class Temperatura:
    @staticmethod
    def celsius_a_fahrenheit(celsius):
        return f"Conversão de Celsius a Fahrenheit: (({celsius} * 9/5) +32) = {((celsius * 9/5) + 32):.2f}"

    @staticmethod
    def fahrenheit_a_celsius(fahrenheit):
        return f"Conversão de Fahrenheit a Celsius: (({fahrenheit} - 32) *5/9) = {((fahrenheit - 32) * 5/9):.2f}"

    @staticmethod
    def celsius_a_kelvin(celsius):
        return f"Conversão de Celsius a Kelvin ({celsius} + 273.15) = {(celsius + 273.15):.2f}"