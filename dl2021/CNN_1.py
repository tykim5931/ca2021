#%%

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
trainLoad = Dataloader(path = '/home/artiv', is_train = True, batch_size = 10)
testLoad = Dataloader(path = '/home/artiv', batch_size = 1, is_train = False, shuffle=False)

#%%
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# 3-Layer CNN
class CNN3:
    def __init__(self, c1_shape=(3,3,3), c2_shape = (5,4,4), max_pool_size = (2,2), conv_stride = 1, pool_stride = 2, lr =0.01):
        
        # input is 1*28*28 image,and target number is 10. 
        self.pool_size = max_pool_size
        self.conv_stride = conv_stride
        self.pool_stride = pool_stride
        self.lr = lr

        #convolution layer
        self.conv_w1 = np.random.normal(0,1, size = (c1_shape[0], 1, c1_shape[1], c1_shape[2]))    # weight of first layer 3,1,3,3
        self.conv_w2 = np.random.normal(0,1, size = (c2_shape[0], c1_shape[0], c2_shape[1], c2_shape[2]))    # weight of second layer 5,3,4,4
        self.b1 = 0
        self.b2 = 0

        #중간값 저장을 위한 변수
        self.co1 = np.zeros((c1_shape[0],int((28-c1_shape[1])/conv_stride+1), 
                                         int((28-c1_shape[2])/conv_stride+1))) # 3, 26, 26
        self.co1_relu = self.co1
        self.mco1 = np.zeros((c1_shape[0], int((self.co1.shape[1] - max_pool_size[0])/pool_stride + 1),
                                           int((self.co1.shape[1] - max_pool_size[1])/pool_stride + 1)))    # 3, 13, 13
        
        self.co2 = np.zeros((c2_shape[0],int((self.mco1.shape[1]-c2_shape[1])/conv_stride+1), 
                                         int((self.mco1.shape[2]-c2_shape[2])/conv_stride+1)))  # 5, 10, 10
        self.co2_relu = self.co2
        self.mco2 = np.zeros((c2_shape[0], int((self.co2.shape[1] - max_pool_size[0])/pool_stride + 1),
                                           int((self.co2.shape[1] - max_pool_size[1])/pool_stride + 1)))    # 5, 5, 5
        self.out_flat = None    # 125
        
        # fully connected layer
        self.w3 = np.random.normal(0,1,size = (self.mco2.shape[0]*self.mco2.shape[1]*self.mco2.shape[2], 10)) # weight of third layer
        self.b3 = 0

        # for saving output
        self.fco = None

        # for saving maxpooling deviation
        self.mpool_dev1 = None
        self.mpool_dev2 = None

        # for making log file
        self.loss_log = []
        self.test_loss_log = []


    def relu(self, x):
        return np.maximum(0, x)

    def relu_dev(self, x):
        return 1*(x>0) + 0.01*(x<0)
    
    def softmax(self, x):
        max_val = np.max(x)
        exp_x = np.exp(x-max_val)
        return exp_x / np.sum(exp_x) #.reshape(-1,1)
    
    def conv2d(self, image, filter, output):
        c, _, r, cl = filter.shape
        for ch in range(output.shape[0]):
            for row in range(output.shape[1]):
                for col in range(output.shape[2]):
                    output[ch, row, col] = np.sum(image[:,row*self.conv_stride : row*self.conv_stride+r, 
                                                        col*self.conv_stride : col*self.conv_stride+cl] 
                                                  * filter[ch])    
        return output

    def maxpooling(self, input, output, mpool_dev):
        mpool_dev = np.zeros(shape = input.shape)
        r, cl = self.pool_size
        for ch in range(input.shape[0]):
            for row in range(output.shape[1]):
                for col in range(output.shape[2]):
                    r_start=row*self.pool_stride
                    c_start=col*self.pool_stride
                    output[ch, row, col] = (input[ch][r_start : r_start+r, c_start : c_start+cl]).max()
                    max_idx = np.argmax(input[ch][r_start : r_start+r, c_start : c_start+cl])
                    mpool_dev[ch][r_start + (max_idx // r), c_start + (max_idx % cl)] = 1
        return output, mpool_dev

    def maxpooling_dev(self,prev_dev, mpool_dev):
        r, cl = self.pool_size
        for ch in range(mpool_dev.shape[0]):
            for row in range(prev_dev.shape[0]):
                for col in range(prev_dev.shape[1]):
                    r_start=row*self.pool_stride
                    c_start=col*self.pool_stride
                    mpool_dev[ch][r_start : r_start+r, c_start : c_start+cl] *= prev_dev[ch][row,col]
        return  mpool_dev

    def forward_prop(self, x):
        self.co1 = self.conv2d(x, self.conv_w1, self.co1) + self.b1  # update self.co1
        self.co1_relu = self.relu(self.co1)
        self.mco1, self.mpool_dev1 = self.maxpooling(self.co1_relu, self.mco1, self.mpool_dev1)    # update self.mco1

        self.co2 = self.conv2d(self.mco1, self.conv_w2, self.co2) + self.b2 # update self.co2   
        self.co2_relu = self.relu(self.co2)
        self.mco2, self.mpool_dev2 = self.maxpooling(self.co2_relu , self.mco2, self.mpool_dev2)    # update self.mco2

        self.out_flat = self.mco2.reshape((1, self.mco2.shape[0]*self.mco2.shape[1]*self.mco2.shape[2]))   # flatten
        self.fco = self.softmax(np.dot(self.out_flat, self.w3) + self.b3)   # fclayer - softmax

    def backward_prop(self, x, y):
        
        # gradient for w3
        dev3 = self.fco - y     # cee~softmax deviation
        w3_grad= np.dot(self.out_flat.T, dev3)  # linear layer deviation(for weight)
        b3_grad= np.mean(dev3)

        # gradient for w2
        unflatten = np.dot(dev3, self.w3.T).reshape(self.mco2.shape) # linear layer deviation(for input), unflatten
        dev2 = self.maxpooling_dev(unflatten, self.mpool_dev2) * self.relu_dev(self.co2_relu) # maxpooling-relu deviation
        a,b,c = dev2.shape
        dev2_expand = np.zeros((a, self.conv_w2.shape[1], b, c))
        for i in range(a):
            dev2_expand[i] = np.stack([dev2[i],dev2[i],dev2[i]])
        conv2_grad = np.zeros(self.conv_w2.shape)   # conv layer deviation(for weight)
        conv2_grad = self.conv2d(self.co1, dev2_expand, conv2_grad)
        b2_grad = np.mean(dev2)

        # gradient for w1
        mco1_grad = np.zeros((dev2_expand.shape[1], self.mco1.shape[1], self.mco1.shape[2]))
        for i in range(mco1_grad.shape[0]):  # conv layer deviation(for input)
            for j in range(dev2_expand.shape[0]):
                mco1_grad[i] += signal.convolve2d(dev2_expand[j][i], self.conv_w2[j][i], mode = 'full', boundary = 'fill')
        dev1 = self.maxpooling_dev(mco1_grad, self.mpool_dev1) * self.relu_dev(self.co1_relu) # maxpooling-relu deviation
        a,b,c = dev1.shape
        dev1_expand = np.zeros((a, self.conv_w1.shape[0], b, c))
        for i in range(a):
            k = dev1[i]
            dev1_expand[i] = np.stack([k,k,k])
        conv1_grad = np.zeros(self.conv_w1.shape)   # conv layer deviation(for weight)
        conv1_grad = self.conv2d(x, dev1_expand, conv1_grad)
        b1_grad = np.mean(dev1)

        return conv1_grad, conv2_grad, w3_grad, b1_grad, b2_grad, b3_grad

    def train_model_batch(self, trainLoader, testLoader, epochs = 10):
        for i in range(epochs):
            cnt=0
            train_loss =0 
            for iter in range(len(trainLoader)):     # per every iteration
                w1_grad, w2_grad, w3_grad, b1_grad, b2_grad, b3_grad = (0,0,0,0,0,0)
                x_batch, y_batch = trainLoader[iter]
                batch_len = len(x_batch)
                for j in range(batch_len):
                    cnt+=1
                    x_inst = x_batch[j]
                    y_inst = y_batch[j]
                    self.forward_prop(x_inst)    # forward calculation -> get output
                    y_hat = np.clip(self.fco, 1e-10, 1-1e-10)
                    w1, w2, w3, b1, b2, b3 = self.backward_prop(x_inst, y_inst)  # backpropagate -> update weights.
                    w1_grad+=w1
                    w2_grad+=w2
                    w3_grad+=w3
                    b1_grad+=b1
                    b2_grad+=b2
                    b3_grad+=b3
                    train_loss += np.sum(-y_inst * np.log(y_hat))  # for visualization, record loss
                
                self.conv_w1 -= w1_grad/batch_len * self.lr
                self.conv_w2 -= w2_grad/batch_len * self.lr
                self.w3 -= w3_grad/batch_len * self.lr
                self.b1 -= b1_grad/batch_len * self.lr
                self.b2 -= b2_grad/batch_len * self.lr
                self.b3 -= b3_grad/batch_len * self.lr

                if((iter+1) % (len(trainLoader)/5)  == 0):
                    test_loss = 0
                    test_len = len(testLoader)
                    for j in range(test_len):
                        x_test_inst, y_test_inst = testLoader[j]
                        x_test_inst=x_test_inst[0]
                        y_test_inst=y_test_inst[0]
                        self.forward_prop(x_test_inst)
                        y_hat = np.clip(self.fco, 1e-10, 1-1e-10)
                        test_loss += np.sum(-y_test_inst * np.log(y_hat))
                    train_loss_tot = train_loss / (batch_len*(len(trainLoader)/5))
                    test_loss_tot = test_loss / test_len
                    self.loss_log.append(train_loss_tot)
                    self.test_loss_log.append(test_loss_tot)
                    print("epoch: ", i , ", images: ", cnt, ", train loss: ", train_loss_tot, 
                          ", test loss: ",test_loss_tot)
                    train_loss = 0

#%%
mymodel = CNN3(c1_shape=(3,3,3), c2_shape = (5,4,4), max_pool_size = (2,2), conv_stride = 1, pool_stride = 2, lr =0.001)
mymodel.train_model_batch(trainLoader = trainLoad, testLoader = testLoad, epochs = 6)

#%%
# plot loss grah
plt.plot(mymodel.loss_log)
plt.plot(mymodel.test_loss_log)
plt.xlabel('epoch X 5')
plt.ylabel('loss')
plt.legend(['train_loss', 'test_loss'])
plt.title('Loss graph', fontsize = 20)
plt.show()

#%%
# draw confusion matrix
confusion_matrix = np.zeros((10,10))
for j in range(len(testLoad)):
    x_test_inst, y_test_inst = testLoad[j]
    mymodel.forward_prop(x_test_inst[0])
    prediction = np.argmax(mymodel.fco)
    confusion_matrix[np.argmax(y_test_inst), prediction] +=1

for k in range(10):
    confusion_matrix[k] = confusion_matrix[k]/np.sum(confusion_matrix[k])

plt.figure(figsize=(10,10))
plt.imshow(confusion_matrix.T, cmap="Blues")
plt.xticks(np.arange(0, confusion_matrix.shape[0])) # 행, truth value
plt.yticks(np.arange(0, confusion_matrix.shape[1])) # 열, predicted value
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

# %%
# print score
sum = 0
for j in range(len(testLoad)):
    x_test_inst, y_test_inst = testLoad[j]
    mymodel.forward_prop(x_test_inst[0])
    prediction = np.argmax(mymodel.fco)
    if (prediction == np.argmax(y_test_inst[0])):
        sum += 1
score = sum/len(testLoad)
print(score)

#%%
# print top 3 images
lst=[]
for i in range(10):
    lst.append([])

for j in range(len(testLoad)):
    x_test_inst, y_test_inst = testLoad[j]
    mymodel.forward_prop(x_test_inst[0])
    prediction = np.argmax(mymodel.fco)
    
    if(prediction == np.argmax(y_test_inst[0])):
        lst[prediction].append((np.max(mymodel.fco), j))

images = testLoad.images

#%%
# print top 3 images
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
# %%
print(images.shape)
# %%
