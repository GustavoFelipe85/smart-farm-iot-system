"""Teste de integração da API do Smart Farm IoT System."""

import pytest
import requests


@pytest.mark.integration
def test_api_current():
    """Verifica o endpoint quando a API estiver em execução."""
    response = requests.get(
        "http://localhost:8000/api/v1/sensors/current",
        timeout=5,
    )

    assert response.status_code == 200
