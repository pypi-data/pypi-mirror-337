class Velocidade:
    @staticmethod
    def kmh_a_ms(kmh):
        return (f"Conversão de kilometro/h a Metro/s: ({kmh} / 3.6) = {(kmh / 3.6):.2f}")

    @staticmethod
    def ms_a_kmh(ms):
        return (f"Conversão de Metro/s a kilometro/h: ({ms} / 3.6) = {(ms * 3.6):.2f}")

    @staticmethod
    def kmh_a_mph(kmh):
        return (f"Conversão de kilometro/h a Millas/h: ({kmh} * 0.621371) = {(kmh * 0.621371):.2f}")
