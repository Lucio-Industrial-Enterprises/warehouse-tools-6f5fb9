import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_explicit_standard_matches_default(self):
        for zone in ("local", "regional"):
            for weight in (0.1, 2, 3.125):
                with self.subTest(zone=zone, weight=weight):
                    self.assertEqual(
                        shipping_quote(weight, zone, service="standard"),
                        shipping_quote(weight, zone),
                    )

    def test_express_rates(self):
        self.assertEqual(shipping_quote(2, "local", "express"), 15.0)
        self.assertEqual(shipping_quote(2, "regional", service="express"), 18.0)

    def test_fractional_weight_rounding(self):
        for zone, standard in (("local", 6.85), ("regional", 9.85)):
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(1.234, zone), standard)
                self.assertEqual(shipping_quote(1.234, zone, "express"), standard + 7)

    def test_invalid_weight(self):
        for service in ("standard", "express"):
            for weight in (0, -1):
                with self.subTest(service=service, weight=weight):
                    with self.assertRaisesRegex(ValueError, "weight must be positive"):
                        shipping_quote(weight, "local", service)

    def test_unknown_zone(self):
        for service in ("standard", "express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown zone"):
                    shipping_quote(2, "international", service)

    def test_unknown_service(self):
        for service in ("overnight", "", "EXPRESS"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown service"):
                    shipping_quote(2, "local", service)
