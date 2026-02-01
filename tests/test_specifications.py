import unittest
from modules.specifications import Module, Functionality
import os
import sqlite3

DB_PATH = 'database/is_data.db'

def clear_tables():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM functionalities')
        c.execute('DELETE FROM modules')
        conn.commit()

class TestModuleCRUD(unittest.TestCase):
    def setUp(self):
        clear_tables()

    def test_create_and_get_module(self):
        m = Module(name='TestModul', description='Popis', version='1.0')
        module_id = m.save()
        self.assertIsInstance(module_id, int)
        data = Module.get_by_id(module_id)
        self.assertIsNotNone(data)
        self.assertEqual(data['name'], 'TestModul')

    def test_update_module(self):
        m = Module(name='ModulA', description='A', version='1.0')
        module_id = m.save()
        Module.update(module_id, 'ModulB', 'B', '2.0', None)
        data = Module.get_by_id(module_id)
        self.assertEqual(data['name'], 'ModulB')
        self.assertEqual(data['version'], '2.0')

    def test_delete_module(self):
        m = Module(name='DelModul', description='Del', version='1.0')
        module_id = m.save()
        Module.delete(module_id)
        data = Module.get_by_id(module_id)
        self.assertIsNone(data)

class TestFunctionalityCRUD(unittest.TestCase):
    def setUp(self):
        clear_tables()
        self.module_id = Module(name='ModulF', description='F', version='1.0').save()

    def test_create_and_get_functionality(self):
        f = Functionality(module_id=self.module_id, name='Funkcia', description='desc')
        func_id = f.save()
        self.assertIsInstance(func_id, int)
        data = Functionality.get_by_id(func_id)
        self.assertIsNotNone(data)
        self.assertEqual(data['name'], 'Funkcia')

    def test_update_functionality(self):
        f = Functionality(module_id=self.module_id, name='F1', description='d1')
        func_id = f.save()
        Functionality.update(func_id, 'F2', 'd2', 'code')
        data = Functionality.get_by_id(func_id)
        self.assertEqual(data['name'], 'F2')
        self.assertEqual(data['description'], 'd2')

    def test_delete_functionality(self):
        f = Functionality(module_id=self.module_id, name='F3', description='d3')
        func_id = f.save()
        Functionality.delete(func_id)
        data = Functionality.get_by_id(func_id)
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
