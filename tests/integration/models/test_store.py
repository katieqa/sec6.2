from models.store import StoreModel
from models.item import ItemModel
from tests.integration.integration_base_test import BaseTest

class StoreTest(BaseTest):

    #item is empty
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [],"Store item list not empty but should be")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(store.find_by_name('test'), "Store exists when should not be present in db")

            store.save_to_db()

            self.assertIsNotNone(store.find_by_name('test'), "Store should be present in the db, but is not")

            store.delete_from_db()

            self.assertIsNone(store.find_by_name('test'), "Store exists when should be deleted in db")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json(self):
        store = StoreModel('test')
        expected = { 'name': 'test',
                     'items': []}
        self.assertDictEqual(store.json(), expected)


    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {'name': 'test',
                        'items': [{'name': 'test_item',
                                   'price': 19.99}]}

            self.assertDictEqual(store.json(), expected)

