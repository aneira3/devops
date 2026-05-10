import pytest

class TestHealthCheck:
    
    def test_health_check_returns_healthy(self, client):
        response = client.get('/health')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['status'] == 'healthy'
        assert json_data['service'] == 'blacklist-microservice'
    
    def test_health_check_no_auth_required(self, client):
        response = client.get('/health')
        
        assert response.status_code == 200
    
    def test_health_check_method_not_allowed(self, client):
        response = client.post('/health')
        
        assert response.status_code == 405