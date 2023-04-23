#%%
# dataloader source code
import gzip
import numpy as np
from pathlib import Path
import math

class Dataloader():
    def __init__(self, path, is_train=True, shuffle=True, batch_size=8):
        path = Path(path)
        imagePath = Path(path/'train-images-idx3-ubyte.gz') if is_train else Path(path/'t10k-images-idx3-ubyte.gz')
        labelPath = Path(path/'train-labels-idx1-ubyte.gz') if is_train else Path(path/'t10k-labels-idx1-ubyte.gz')

        self.batch_size = batch_size
        self.images = self.loadImages(imagePath)
        self.labels = self.loadLabels(labelPath)
        self.index = 0
        self.idx = np.arange(0, self.images.shape[0])
        if shuffle: np.random.shuffle(self.idx) # shuffle images

    def __len__(self):
        n_images, _, _, _ = self.images.shape
        n_images = math.ceil(n_images / self.batch_size)
        return n_images

    def __iter__(self):
        return datasetIterator(self)

    def __getitem__(self, index):
        image = self.images[self.idx[index * self.batch_size:(index + 1) * self.batch_size]]
        label = self.labels[self.idx[index * self.batch_size:(index + 1) * self.batch_size]]
        image = image/255.0
        return image, label

    def loadImages(self, path):
        with gzip.open(path) as f:
            images = np.frombuffer(f.read(), 'B', offset=16)
            images = images.reshape(-1, 1, 28, 28).astype(np.float32)
            return images

    def loadLabels(self, path):
        with gzip.open(path) as f:
            labels = np.frombuffer(f.read(), 'B', offset=8)
            rows = len(labels)
            cols = labels.max() + 1
            one_hot = np.zeros((rows, cols)).astype(np.uint8)
            one_hot[np.arange(rows), labels] = 1
            one_hot = one_hot.astype(np.float64)
            return one_hot

# for enumerate magic python function returns Iterator
class datasetIterator():
    def __init__(self, dataloader):
        self.index = 0
        self.dataloader = dataloader

    def __next__(self):
        if self.index < len(self.dataloader):
            item = self.dataloader[self.index]
            self.index += 1
            return item
        # end of iteration
        raise StopIteration

#%%
# load data
trainLoad = Dataloader(path = '/home/artiv', is_train = True)
testLoad = Dataloader(path = '/home/artiv', batch_size = 1, is_train = False, shuffle=False)

#%%
import numpy as np
import matplotlib.pyplot as plt

# 3-Layer NN
class NN3:
    def __init__(self, h1_num, h2_num, n_features, n_classes, lr =0.01, batch_size = 8):
        np.random.seed(5)
        self.w1 = np.random.normal(0,pow((n_features+h1_num)/2, -0.5), size = (n_features, h1_num))    # weight of first layer
        self.w2 = np.random.normal(0,pow((h1_num+h2_num)/2, -0.5), size = (h1_num, h2_num))    # weight of second layer
        self.w3 = np.random.normal(0,pow((h2_num+n_classes)/2, -0.5), size = (h2_num, n_classes)) # weight of third layer. initialized with random normal
        self.b1 = np.zeros(h1_num)
        self.b2 = np.zeros(h2_num)
        self.b3 = np.zeros(n_classes)

        #중간값 저장을 위한 변수
        self.a1 = None
        self.a2 = None
        self.a3 = None

        # for making log file
        self.loss_log = []
        self.test_loss_log = []
        self.lr = lr
        self.batch_size = batch_size

    def relu(self, x):
        return np.maximum(0, x)

    def relu_dev(self, x):
        return 1*(x>0) + 0.01*(x<0)
    
    def softmax(self, x):
        max_val = np.max(x)
        exp_x = np.exp(x-max_val)
        return exp_x / np.sum(exp_x) #.reshape(-1,1)

    def forward_prop(self, x):
        #x = np.resize(x, (1, len(x)))
        self.a1 = self.relu(np.dot(x, self.w1) + self.b1)
        self.a2 = self.relu(np.dot(self.a1, self.w2) + self.b2)
        self.a3 = self.softmax(np.dot(self.a2, self.w3) + self.b3)

    def backward_prop(self, x, y):
        #x = np.resize(x, (1, len(x)))
        
        dev3 = self.a3 - y
        w3_update= np.dot(self.a2.T, dev3)  # gard 1 of cce
        b3_update= np.mean(dev3, axis = 1)

        dev2 = np.dot(dev3, self.w3.T) * self.relu_dev(self.a2)
        w2_update = np.dot(self.a1.T, dev2)
        b2_update = np.mean(dev2, axis = 1)

        dev1 = np.dot(dev2, self.w2.T) * self.relu_dev(self.a1)
        w1_update = np.dot(x.T, dev1)
        b1_update = np.mean(dev1, axis = 1)
        return w1_update, w2_update, w3_update, b1_update, b2_update, b3_update

    def train_model_batch(self,trainLoader, testLoader, epochs = 10):
        for i in range(epochs):
            cnt=0
            train_loss =0 
            for iter in range(len(trainLoader)):     # per every iteration
                w1_grad, w2_grad, w3_grad, b1_grad, b2_grad, b3_grad = (0,0,0,0,0,0)
                x_batch, y_batch = trainLoader[iter]
                for j in range(len(x_batch)):
                    cnt+=1
                    x_inst = x_batch[j].reshape(1, 28*28)
                    y_inst = y_batch[j]
                    self.forward_prop(x_inst)    # forward calculation -> get output
                    y_hat = np.clip(self.a3, 1e-10, 1-1e-10)
                    w1, w2, w3, b1, b2, b3 = self.backward_prop(x_inst, y_inst)  # backpropagate -> update weights.
                    w1_grad+=w1
                    w2_grad+=w2
                    w3_grad+=w3
                    b1_grad+=b1
                    b2_grad+=b2
                    b3_grad+=b3
                    train_loss += np.sum(-y_inst * np.log(y_hat))  # for visualization, record loss
                self.w1 -= w1_grad/len(x_batch) * self.lr
                self.w2 -= w2_grad/len(x_batch) * self.lr
                self.w3 -= w3_grad/len(x_batch) * self.lr
                self.b1 -= b1_grad/len(x_batch) * self.lr
                self.b2 -= b2_grad/len(x_batch) * self.lr
                self.b3 -= b3_grad/len(x_batch) * self.lr

                if((iter+1) % (len(trainLoader)/10)  == 0):
                    test_loss = 0
                    for j in range(len(testLoader)):
                        x_test_inst, y_test_inst = testLoader[j]
                        x_test_inst = x_test_inst.reshape(1, 28*28)
                        self.forward_prop(x_test_inst)
                        y_hat = np.clip(self.a3, 1e-10, 1-1e-10)
                        test_loss += np.sum(-y_test_inst * np.log(y_hat))
                    self.loss_log.append(train_loss / (len(x_batch)*(len(trainLoader)/10)))
                    self.test_loss_log.append(test_loss / len(testLoader))
                    print("epoch: ", i , ", images: ", cnt, ", train loss: ", train_loss / (len(x_batch)*(len(trainLoader)/10)), 
                          ", test loss: ",test_loss/len(testLoader))
                    train_loss = 0

#%%
# train model with SGD
mymodel = NN3(n_features = 784, h1_num = 300, h2_num = 100, n_classes = 10, lr = 0.01, batch_size=1)
mymodel.train_model_batch(trainLoader = trainLoad, testLoader = testLoad, epochs = 10)

#%%
# plot loss graph
plt.plot(mymodel.loss_log)
plt.plot(mymodel.test_loss_log)
plt.xlabel('epoch X 10')
plt.ylabel('loss')
plt.legend(['train_loss', 'test_loss'])
plt.title('Loss graph', fontsize = 20)
plt.show()

#%%
# draw confusion matrix
confusion_matrix = np.zeros((10,10))
for j in range(len(testLoad)):
    x_test_inst, y_test_inst = testLoad[j]
    x_test_inst = x_test_inst.reshape(1, 28*28)
    mymodel.forward_prop(x_test_inst)
    prediction = np.argmax(mymodel.a3)
    confusion_matrix[np.argmax(y_test_inst), prediction] +=1

for k in range(10):
    confusion_matrix[k] = confusion_matrix[k]/np.sum(confusion_matrix[k])

confusion_matrix = confusion_matrix.T
plt.figure(figsize=(10,10))
plt.imshow(confusion_matrix, cmap="Blues")
plt.xticks(np.arange(0, confusion_matrix.shape[0])) # 행, predicted value
plt.yticks(np.arange(0, confusion_matrix.shape[1])) # 열, truth value
plt.title('Confusion matrix ', fontsize=20)
plt.xlabel('Prediction', fontsize=20)
plt.ylabel('Truth', fontsize=20)
for i in range(10):
    for j in range(10):
        if i==j:
            plt.text(i, j, round(confusion_matrix[i,j],3), horizontalalignment='center',color = 'white' )
            continue
        plt.text(i, j, round(confusion_matrix[i,j],3), horizontalalignment='center')
plt.colorbar()
plt.show()

#%%
# print score
sum = 0
for j in range(len(testLoad)):
    x_test_inst, y_test_inst = testLoad[j]
    x_test_inst = x_test_inst.reshape(1, 28*28)
    mymodel.forward_prop(x_test_inst)
    prediction = mymodel.a3
    if (np.argmax(prediction)== np.argmax(y_test_inst)):
        sum += 1
score = sum/len(testLoad)
print(score)

#%%
lst=[]
for i in range(10):
    lst.append([])

for j in range(len(testLoad)):
    x_test_inst, y_test_inst = testLoad[j]
    x_test_inst = x_test_inst.reshape(1, 28*28)
    mymodel.forward_prop(x_test_inst)
    prediction = np.argmax(mymodel.a3)
    
    if(prediction == np.argmax(y_test_inst)):
        lst[prediction].append((np.max(mymodel.a3), j))

images = testLoad.images

for i in range(10):
    lst[i].sort(key = lambda x:x[0], reverse = True)
    
    fig = plt.figure()
    plt.title("Top 3 images with probability, label:" + str(i))

    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)

    ax1.imshow(images[lst[i][0][1]][0], 'gray')
    ax1.set_title(str(round(lst[i][0][0]*100,1)) + '%')
    ax2.imshow(images[lst[i][1][1]][0], 'gray')
    ax2.set_title(str(round(lst[i][1][0]*100,1)) + '%')
    ax3.imshow(images[lst[i][2][1]][0], 'gray')
    ax3.set_title(str(round(lst[i][2][0]*100,1)) + '%')
    plt.show()