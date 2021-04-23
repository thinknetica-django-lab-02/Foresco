from django.test import Client, TestCase


class GetPagesTestCase(TestCase):
    fixtures = ["category.json", "price.json", "product.json", "permission.json", "group.json",
                "user.json", "profile.json", "seller.json", "tag.json"]

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail(self):
        response = self.client.get('/products/13/')
        self.assertEqual(response.status_code, 200)

    def test_product_list(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_profile_detail(self):
        response = self.client.get('/profile/1/')
        self.assertEqual(response.status_code, 200)
