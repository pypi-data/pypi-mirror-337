class Peso:
    @staticmethod
    def kg_a_libras(kg):
        return (f"Conversão de Kilogramo a Libra: ({kg} * 2.20462) = {(kg * 2.20462):.2f}")

    @staticmethod
    def libras_a_kg(libras):
        return (f"Conversão de Libra a Kilogramo: ({libras} / 2.20462) = {(libras / 2.20462):.2f}")

    @staticmethod
    def gramos_a_kg(gramos):
        return (f"Conversão de Gramo a Kilogramo: ({gramos} / 1000) = {(gramos / 1000):.2f}")
    
    @staticmethod
    def calcular_peso_kg(altura, comprimento, longitude):
        return (f"Kilogramo: ({altura} x {comprimento} x {longitude} ) = {(altura * comprimento * longitude):.2f}kg")