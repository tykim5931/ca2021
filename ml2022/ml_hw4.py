import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA, KernelPCA
import matplotlib.pyplot as plt


# fetch mnist data
mnist = fetch_openml('mnist_784')
mnist_df = pd.DataFrame(mnist.data)
mnist_df['label'] = mnist.target

def sampling(numbers):
    sample_df = pd.DataFrame(columns=mnist_df.columns)
    for i in numbers:
        temp_df = mnist_df[(mnist_df['label'] == f"{i}" )].sample(n=100)
        sample_df = pd.concat([sample_df,temp_df])
    sample_df = sample_df.sample(frac=1).reset_index(drop=True)
    Y = sample_df['label'].astype(int).to_numpy()
    sample_df_img = sample_df.drop('label', axis = 1)
    X = sample_df_img.to_numpy()
    X = X/255.0 # scaling
    return X, Y


# Question 1

def visualize(pca):
    print("Mean image========================")
    # plot the mean image
    mean_img = pca.mean_.reshape(28,28)
    plt.imshow(mean_img)
    plt.show()

    # plot first 10 eigenvectors as images
    print("Eigenvectors========================")
    pca_comp10 = pca.components_[:10]
    for eigen in pca_comp10:
        eigen_img = eigen.reshape(28,28)
        plt.imshow(eigen_img)
        plt.show()

    # plot the eigenvalues in decreasing order as a fucntion of dimension.
    print("Eigenvalues========================")
    eigenvalue_10 = sorted(pca.singular_values_, reverse = True)[:10]
    x = list(range(0,10))
    plt.bar(x, eigenvalue_10)
    plt.grid(True)
    plt.xlabel("Top 10 components(eigen vectors)")
    plt.ylabel("Eigenvalues")
    plt.show()

    print("Whole eigenvalues==================")
    eigenvalues_ = sorted(pca.singular_values_, reverse=True)
    x = list(range(0,len(eigenvalues_)))
    plt.bar(x, eigenvalues_)
    plt.grid(True)
    plt.xlabel("Whole components")
    plt.ylabel("Eigenvalues")
    plt.show()  


def visualize_k(pca):
    # plot the eigenvalues in decreasing order as a fucntion of dimension.
    print("Eigenvalues========================")
    eigenvalue_10 = sorted(pca.eigenvalues_, reverse=True)[:10]
    x = list(range(0,10))
    plt.bar(x, eigenvalue_10)
    plt.grid(True)
    plt.xlabel("Top 10 components(eigen vectors)")
    plt.ylabel("Eigenvalues")
    plt.show()

    print("Whole eigenvalues==================")
    eigenvalues_ = sorted(pca.eigenvalues_, reverse=True)
    x = list(range(0,len(eigenvalues_)))
    plt.bar(x, eigenvalues_)
    plt.grid(True)
    plt.xlabel("Whole components")
    plt.ylabel("Eigenvalues")
    plt.show()  

digit_2_flat, digit_2_y = sampling([2])
pca = PCA(n_components=100)
pca.fit(digit_2_flat)
visualize(pca)

k_pca = KernelPCA(n_components=100, kernel='linear')
k_pca.fit(digit_2_flat)
visualize_k(k_pca)



# Question 2
mnist_x, mnist_y = sampling([0,1,2,3,4,5,6,7,8,9])

pca2 = PCA(n_components=100)
pca2.fit(mnist_x)
visualize(pca2)

k_pca2 = KernelPCA(n_components=100, kernel='linear')
k_pca2.fit(mnist_x)
visualize_k(k_pca2)


# Question 3
from sklearn.cluster import KMeans
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.neighbors import KNeighborsClassifier

def kmeans_score(X, Y):
    kmeans = KMeans(n_clusters=10, random_state=822).fit(X)
    label = kmeans.predict(X)
    rand_index = adjusted_rand_score(Y, label)
    mutual_info = adjusted_mutual_info_score(Y, label)
    return rand_index, mutual_info, label, kmeans


mnist_x, mnist_y = sampling([0,1,2,3,4,5,6,7,8,9])

rand_index, mutual_info, label_orig, kmeans = kmeans_score(mnist_x, mnist_y)
print(f"Original data, components 784: \nRand index: {rand_index}, Mutual information based: {mutual_info}")

for i in [2,5,10,20,100,200,500]:
    pca_test = PCA(n_components=i)
    trans_pca = pca_test.fit_transform(mnist_x)
    rand_index, mutual_info, label, kmeans = kmeans_score(trans_pca, mnist_y)
    print(f"PCA, components {i}: \nRand index: {rand_index}, Mutual information based: {mutual_info}")

    kpca_test = KernelPCA(n_components=i, kernel='linear')
    trans_kpca = kpca_test.fit_transform(mnist_x)
    rand_index, mutual_info, label, kmeans = kmeans_score(trans_kpca, mnist_y)
    print(f"Kernel PCA, components {i}: \nRand index: {rand_index}, Mutual information based: {mutual_info}")

    for j in range(0,10):
        pca_2 = PCA(n_components = 2)
        trans_pca_2 = pca_2.fit_transform(trans_kpca)
        filtered_label = trans_pca[label == j]
        plt.scatter(filtered_label[:,0] , filtered_label[:,1], s=5)
    plt.show()


# Question 4
n_clust = 15

def fix_labels(cluster, truth):
    table = np.zeros(shape=(n_clust,10))
    for i, c_label in enumerate(cluster):
        table[c_label,truth[i]]+=1

    ans = np.zeros(shape=(n_clust,))
    for j in range(0,n_clust):
        ans[j] = np.argmax(table[j])
    return ans

def get_centers(dataset, cluster):
    
    centers = np.zeros(shape=(n_clust,dataset.shape[1]))
    counts = np.zeros(shape=(n_clust,))
    for imgs, clst in zip(dataset, cluster):
        centers[clst] += imgs
        counts[clst] += 1
    for i in range(n_clust):
        centers[i] /= counts[i]
    return centers

def kmeans_score(X, Y):
    kmeans = KMeans(n_clusters=n_clust, random_state=822).fit(X)
    label = kmeans.predict(X)
    rand_index = adjusted_rand_score(Y, label)
    mutual_info = adjusted_mutual_info_score(Y, label)
    return rand_index, mutual_info, label, kmeans

# original kmeans
rand_index, mutual_info, label_orig, kmeans_orig = kmeans_score(mnist_x, mnist_y)

# Best PCA kmeans
pca_test = KernelPCA(n_components=20)
transformed = pca_test.fit_transform(mnist_x)
RI, MI, label, kmeans = kmeans_score(transformed, mnist_y)
print(f"PCA, components 20: \nRand index: {RI}, Mutual information based: {MI}")

# 1-NN classify
test_x, test_y = sampling([0,1,2,3,4,5,6,7,8,9])

# kmeans
k_centers_orig = kmeans_orig.cluster_centers_
k_labels_orig = fix_labels(label_orig, mnist_y)
print(k_labels_orig)

k_centers = kmeans.cluster_centers_
k_labels = fix_labels(label, mnist_y)
print(k_labels)

# original 784 kmeans KNN
knn_1 = KNeighborsClassifier(n_neighbors=1)
knn_1.fit(k_centers_orig, k_labels_orig)
# score = knn_1.score(test_x, test_y)
score = knn_1.score(mnist_x, mnist_y)
print("Original Score: " , score)

# transformed kmeans KNN
knn_1 = KNeighborsClassifier(n_neighbors=1)
knn_1.fit(k_centers, k_labels)
t_test = pca_test.fit_transform(test_x)
# score = knn_1.score(t_test, test_y)
score = knn_1.score(pca_test.fit_transform(mnist_x), mnist_y)
print("Dimension reduced score: ", score)



# Question 5
correct = [[],[],[],[],[],[],[],[],[],[]]
incorrect = [[],[],[],[],[],[],[],[],[],[]]
transformed = pca_test.fit_transform(test_x)
prediction = knn_1.predict(transformed) #knn_1 is fitted with pca_transformed data

for i in range(len(prediction)):
    if prediction[i] == test_y[i]:
        correct[int(prediction[i])].append(i)
    else:
        incorrect[int(prediction[i])].append(i)

for i in range(0,10):   
    correct3 = correct[i][:3]
    plt.figure()
    print(f"Classifed label {i}")
    for j, item_idx in enumerate(correct3):
        plt.subplot(2,3,j+1)
        img = test_x[int(item_idx)].reshape(28,28)
        plt.imshow(img)

    incorrect3 = incorrect[i][:3]
    for j, item_idx in enumerate(incorrect3):
        plt.subplot(2,3,j+4)
        img = test_x[int(item_idx)].reshape(28,28)
        plt.imshow(img)
    plt.show()