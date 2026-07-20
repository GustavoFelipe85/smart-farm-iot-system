"""
Smart Farm IoT System
Anomaly Detector

Primeiro módulo da Fase 5.

Responsável por identificar leituras anômalas dos sensores
antes do armazenamento e da tomada de decisão.
"""


class AnomalyDetector:
    """Detector inicial de anomalias."""

    def analyze(self, sensor_data: dict) -> dict:
        """
        Analisa uma leitura de sensores.

        Returns
        -------
        dict
            Resultado da análise.
        """
        raise NotImplementedError(
            "Implementação prevista para a Fase 5."
        )
