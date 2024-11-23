import unittest
from app import app

#Verifica se as rotas que não requerem autenticação (/ e /items) respondem corretamente com status 200 e os dados esperados.

class TestPublicRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"API is running by Frank", response.data)

    def test_get_items(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"item1", response.data)
        self.assertIn(b"item2", response.data)



#Garante que o endpoint /login gera um token de acesso JWT válido.
class TestJWTFunctionality(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_login_creates_token(self):
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)
        self.assertTrue(len(response.json["access_token"]) > 0)


#Certifica-se de que a rota protegida (/protected) exige autenticação e responde corretamente com um token válido.
class TestProtectedRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_protected_route_without_token(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)  # Unauthorized
        self.assertIn(b"Missing Authorization Header", response.data)

    def test_protected_route_with_token(self):
        # Obtenha o token primeiro
        login_response = self.client.post('/login')
        token = login_response.json["access_token"]

        # Acesse a rota protegida com o token
        response = self.client.get('/protected', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Protected route", response.data)