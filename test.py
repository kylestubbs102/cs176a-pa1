import sys

str = "I am a string"
byteStr = str.encode('utf-8')
print(str)
print(sys.getsizeof(str))
print(str[0:50])
print(sys.getsizeof(str[0:50]))
print(byteStr)
print(sys.getsizeof(byteStr))
print(byteStr[5:10])
print(sys.getsizeof(byteStr[5:10]))
print(sys.getsizeof(b' '))