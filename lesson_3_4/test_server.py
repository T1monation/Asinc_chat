import unittest
import json
from server import *


class TestServer(unittest.TestCase):

    def testdataloadsmsg(self):
        test_json = {
            'action': 'msg',
            'text message': 'now'
        }
        r = data_loads(json.dumps(test_json).encode('utf-8'))
        self.assertEqual(r, 'input message: now')

    def testdataloadspresence(self):
        test_json = {
            'action': 'presense',
            'type': 'now'
        }
        r = data_loads(json.dumps(test_json).encode('utf-8'))
        self.assertEqual(r, 'client status: now')

    def testdataloadswrongtype1(self):
        test_json = {
            'wrong': 'presense',
            'type': 'now'
        }
        r = data_loads(json.dumps(test_json).encode('utf-8'))
        self.assertEqual(r, 'Invalid message!')

    def testdataloadswrongtype2(self):
        test_json = {
            'action': 'presense',
            'text message': 'now'
        }
        r = data_loads(json.dumps(test_json).encode('utf-8'))
        self.assertEqual(r, 'Invalid message!')

    def testdataloadswrongtype3(self):
        test_json = {
            'action': 'msg',
            'type': 'now'
        }
        r = data_loads(json.dumps(test_json).encode('utf-8'))
        self.assertEqual(r, 'Invalid message!')

    def testserveranswer(self):
        r = json.loads(server_answer().decode(encoding='utf-8'))
        self.assertEqual(r['alert'], 'message recived')

    def testserveranswerencoding(self):
        r = json.loads(server_answer(
            encoding='utf-16').decode(encoding='utf-16'))
        self.assertEqual(r['alert'], 'message recived')

    def testserveranswertext(self):
        r = json.loads(server_answer(
            text_msg='some text').decode(encoding='utf-8'))
        self.assertEqual(r['alert'], 'some text')

    def testserveranswerresponse(self):
        r = json.loads(server_answer(response=404).decode(encoding='utf-8'))
        self.assertEqual(r['response'], 404)


if __name__ == '__main__':
    unittest.main()
