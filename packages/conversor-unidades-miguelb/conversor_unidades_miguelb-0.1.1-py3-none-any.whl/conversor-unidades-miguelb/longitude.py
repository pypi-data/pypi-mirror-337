class Longitude:
    @staticmethod
    def metro_a_kilometro(metro):
        return f"Conversão de Metros a Kilometros: ({metro} / 1000) = {(metro / 1000):.2f}"
    
    @staticmethod
    def kilometros_a_millas(kilometros):
        return f"Conversão Kilometros a Millas: ({kilometros} * 0.621371) = {(kilometros * 0.621371):.2f}"

    @staticmethod
    def millas_a_metros(millas):
        return (f"Conversão de Millas a Metros: ({millas} * 1609.34) = {(millas * 1609.34):.2f}")