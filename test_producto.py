import unittest
from producto import Producto
from parameterized import parameterized
from productoServices import ProductoService
from repositorios import Repositorios


class TestProducto(unittest.TestCase):
    def test_AI_uso_property(self):
        producto = Producto()
        producto.descripcion = 'acer A515'
        producto.precio = 500000
        producto.tipo = 'computadoras'
        self.assertDictEqual(producto.__dict__, {'_descripcion': 'acer A515',
                                                 '_precio': 500000,
                                                 '_tipo': 'computadoras',
                                                 '_estado': 'disponible'})

    def test_AII_constructor_con_valores_iniciales(self):
        producto = Producto("Lenovo 450", 300000, 'computadoras')
        self.assertDictEqual(producto.__dict__, {'_descripcion': 'Lenovo 450',
                                                 '_precio': 300000,
                                                 '_tipo': 'computadoras',
                                                 '_estado': 'disponible'})

    def test_AIII_validar_precio(self):
        with self.assertRaises(ValueError):
            Producto("Lenovo IdeaPad 3", -1, "laptop")

    @parameterized.expand([
            ("lenovo t490", 6000000, 'computadoras'),
            ("samsung s10", 200000, 'celular'),
            ("samsung s20", 400000, 'celular'),
            ("acer", 6000500, 'computadoras'),
            ("HP", 6000000, 'computadoras'),
        ])
    # Agregar un producto
    def test_AIV_add_producto(self, descripcion, precio, tipo):
        producto = Producto(descripcion, precio, tipo)
        productoKey = ProductoService().add_producto(producto)
        self.assertDictEqual(Repositorios.productosList[productoKey],
                             producto. __dict__)

    @parameterized.expand([
        ("ascendente",
            {0: {'_descripcion': 'samsung s10', '_precio': 200000,
             '_tipo': 'celular', '_estado': 'disponible'},
             1: {'_descripcion': 'samsung s20', '_precio': 400000,
             '_tipo': 'celular', '_estado': 'disponible'},
             2: {'_descripcion': 'lenovo t490', '_precio': 6000000,
             '_tipo': 'computadoras', '_estado': 'disponible'},
             3: {'_descripcion': 'HP', '_precio': 6000000,
             '_tipo': 'computadoras', '_estado': 'disponible'},
             4: {'_descripcion': 'acer', '_precio': 6000500,
             '_tipo': 'computadoras', '_estado': 'disponible'}}),
        ("descendente",
            {0: {'_descripcion': 'acer', '_precio': 6000500,
             '_tipo': 'computadoras', '_estado': 'disponible'},
             1: {'_descripcion': 'lenovo t490', '_precio': 6000000,
             '_tipo': 'computadoras', '_estado': 'disponible'},
             2: {'_descripcion': 'HP', '_precio': 6000000, '_tipo':
             'computadoras', '_estado': 'disponible'},
             3: {'_descripcion': 'samsung s20',
             '_precio': 400000, '_tipo': 'celular', '_estado': 'disponible'},
             4: {'_descripcion': 'samsung s10', '_precio': 200000,
             '_tipo': 'celular', '_estado': 'disponible'}}),
    ])
    # Ordenar lista
    def test_B_insertion_sort_precio(self, tipo_orden, list_ordenada):
        lista_ordenada = ProductoService().\
            insertion_sort_precio(Repositorios.productosList, tipo_orden)
        self.assertDictEqual(lista_ordenada, list_ordenada)

    @parameterized.expand([
        (200000, {'_descripcion': 'samsung s10', '_precio': 200000,
         '_tipo': 'celular', '_estado': 'disponible'}),
        (400000, {'_descripcion': 'samsung s20', '_precio': 400000,
         '_tipo': 'celular', '_estado': 'disponible'}),
    ])
    # Busqueda binaria
    def test_C_busqueda_binaria(self, precio_buscado, producto):
        busqueda = ProductoService().\
            busqueda_binaria(Repositorios.productosList, precio_buscado)
        self.assertDictEqual(busqueda, producto)

    # Eliminar un producto
    # def test_delete_producto(self):
    #    ProductoService().delete_producto(0)
    #    self.assertEqual(Repositorios.productosList.get(0), None)

    @parameterized.expand([
        ("lenovo t490", 6000000, 'computadoras')
    ])
    # Verificar la exeption al modificar un book con un legajo que no existe
    def test_D_delete_producto_value_error(self, descripcion, precio, tipo):
        long_list = len(Repositorios.productosList)
        with self.assertRaises(ValueError):
            ProductoService().delete_producto(long_list+1)

    # @parameterized.expand([("lenovo t490", 600000, 'laptop', 1)])
    # def test_update_estado(self, key, descripcion, precio, tipo, estado):
    #     producto = Producto(descripcion, precio, tipo)
    #     ProductoService().update_producto(producto, key)
    #     self.assertEqual(Repositorios.productosList[key], producto.__dict__)

    @parameterized.expand([
        (0, {'_descripcion': 'lenovo t490', '_precio': 6000000,
             '_tipo': 'computadoras', '_estado': 'vendido'}),
        (1, {'_descripcion': 'samsung s10', '_precio': 200000,
             '_tipo': 'celular', '_estado': 'vendido'}),
        (2, {'_descripcion': 'samsung s20', '_precio': 400000,
             '_tipo': 'celular', '_estado': 'vendido'})
    ])
    def test_E_vendido(self, key, update):
        prodVendido = ProductoService().vender_producto(key)
        self.assertEqual(update, prodVendido)

    @parameterized.expand([(
        {3: {'_descripcion': 'acer', '_estado': 'disponible',
         '_precio': 6000500, '_tipo': 'computadoras'},
         4: {'_descripcion': 'HP', '_estado': 'disponible',
         '_precio': 6000000, '_tipo': 'computadoras'}}, )])
    def test_FI_get_lista_estado_disponible(self, disponibles):
        prodFiltrada = ProductoService().\
            get_lista_estado(Repositorios.productosList, 'disponible')
        self.assertEqual(disponibles, prodFiltrada)

    @parameterized.expand([(
        {0: {'_descripcion': 'lenovo t490', '_estado': 'vendido',
         '_precio': 6000000, '_tipo': 'computadoras'},
         1: {'_descripcion': 'samsung s10', '_estado': 'vendido',
         '_precio': 200000, '_tipo': 'celular'},
         2: {'_descripcion': 'samsung s20', '_estado': 'vendido',
         '_precio': 400000, '_tipo': 'celular'}}, )])
    def test_FII_get_lista_estado_disponible(self, vendidos):
        prodFiltrada = ProductoService().\
            get_lista_estado(Repositorios.productosList, 'vendido')
        self.assertEqual(vendidos, prodFiltrada)


if __name__ == '__main__':
    unittest.main()
