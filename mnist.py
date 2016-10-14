sources = [
    "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
    "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"
]
dir = os.path.dirname(os.path.realpath(__file__))
for source in sources:
    sourceArray = source.split("/")
    filename = sourceArray[len(sourceArray) - 1]
    destName = os.path.join(dir, filename)
    print (source)
    print (destName)
    urllib.request.urlretrieve(source, destName)
