import unittest
import json
from client import *


class TestClient(unittest.TestCase):
    def testmsgsenderpresense(self):
        r = json.loads(msg_sender(action='presense').decode('utf-8'))
        self.assertEqual(r['type'], 'status online')

    def testmsgsendermsg(self):
        r = json.loads(msg_sender(text_msg='test message').decode('utf-8'))
        self.assertEqual(r['text message'], 'test message')

    def testmsgsenderencoding(self):
        r = json.loads(msg_sender(encoding='utf-16',
                       text_msg='test message').decode('utf-16'))
        self.assertEqual(r['text message'], 'test message')

    def testincomingmsg(self):
        data = json.dumps({
            "response": 200,
            "time": time.time(),
            "alert": 'some test text'
        }).encode('utf-8')
        r = incoming_msg(data)
        self.assertEqual(r, 'server status 200, some test text')

    def testincomingmsgencoding(self):
        data = json.dumps({
            "response": 200,
            "time": time.time(),
            "alert": 'some test text'
        }).encode('utf-16')
        r = incoming_msg(data, encoding='utf-16')
        self.assertEqual(r, 'server status 200, some test text')

    def testincomingmsgkeyerror(self):
        data = json.dumps({
            "test": 200,
            "time": time.time(),
            "alert": 'some test text'
        }).encode('utf-8')
        r = incoming_msg(data)
        self.assertEqual(r, 'wrong incoming message')


if __name__ == '__main__':
    unittest.main()
