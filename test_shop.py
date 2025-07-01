import pytest

from models import Product, Cart

@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()

class TestProducts:
    def test_product_check_quantity(self, product):
        assert product.check_quantity(500) == True
        assert product.check_quantity(1001) == False

    def test_product_buy(self, product):
        product.buy(500)
        assert product.quantity == 500

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)

class TestCart:
    def test_add_product(self, cart, product):
        cart.add_product(product)
        assert cart.products[product] == 1

        cart.add_product(product, 5)
        assert cart.products[product] == 6

    def test_remove_product(self, cart, product):
        cart.add_product(product, 10)
        cart.remove_product(product, 5)
        assert cart.products[product] == 5

        cart.remove_product(product)
        assert product not in cart.products

    def test_clear(self, cart, product):
        cart.add_product(product, 10)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 5)
        assert cart.get_total_price() == 500.0

    def test_buy(self, cart, product):
        cart.add_product(product, 5)
        cart.buy()
        assert product.quantity == 995
        assert len(cart.products) == 0

    def test_buy_more_than_available(self, cart, product):
        product.quantity = 3
        cart.add_product(product, 5)
        with pytest.raises(ValueError):
            cart.buy()