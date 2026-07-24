import unittest

from app import app


class StrokeAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stroke Risk Prediction', response.data)

    def test_predict_route(self):
        response = self.client.post('/predict', data={
            'age': '45',
            'bp': 'Yes',
            'hrd': 'No',
            'glu': '120'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prediction Result', response.data)


if __name__ == '__main__':
    unittest.main()
