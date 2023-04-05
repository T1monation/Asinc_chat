# Задание 6.
from chardet.universaldetector import UniversalDetector


detector = UniversalDetector()
with open('test_file.txt', 'rb') as f:
    for line in f:
        detector.feed(line)
        if detector.done:
            break
        detector.close()
print(detector.result)

with open('test_file.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line)
