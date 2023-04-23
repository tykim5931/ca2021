import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml

from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import SpectralClustering

from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score

from sklearn.neighbors import KNeighborsClassifier


# UTILITES
def fix_labels(cluster, truth):
    table = np.zeros(shape=(10,10))
    for i, c_label in enumerate(cluster):
        table[c_label,truth[i]]+=1

    ans = np.zeros(shape=(10,))
    for j in range(0,10):
        ans[j] = np.argmax(table[j])
    return ans

def get_centers(dataset, cluster):
    centers = np.zeros(shape=(10,784))
    counts = np.zeros(shape=(10,))
    for imgs, clst in zip(dataset, cluster):
        centers[clst] += imgs
        counts[clst] += 1
    for i in range(10):
        centers[i] /= counts[i]
    return centers


# Questions
def num1():
    import time
    import warnings

    import numpy as np
    import matplotlib.pyplot as plt

    from sklearn import cluster, datasets, mixture
    from sklearn.neighbors import kneighbors_graph
    from sklearn.preprocessing import StandardScaler
    from itertools import cycle, islice

    np.random.seed(0)

    # ============
    # Generate datasets. We choose the size big enough to see the scalability
    # of the algorithms, but not too big to avoid too long running times
    # ============
    n_samples = 500
    noisy_circles = datasets.make_circles(n_samples=n_samples, factor=0.5, noise=0.05)
    noisy_moons = datasets.make_moons(n_samples=n_samples, noise=0.05)
    blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
    no_structure = np.random.rand(n_samples, 2), None

    # Anisotropicly distributed data
    random_state = 170
    X, y = datasets.make_blobs(n_samples=n_samples, random_state=random_state)
    transformation = [[0.6, -0.6], [-0.4, 0.8]]
    X_aniso = np.dot(X, transformation)
    aniso = (X_aniso, y)

    # blobs with varied variances
    varied = datasets.make_blobs(
        n_samples=n_samples, cluster_std=[1.0, 2.5, 0.5], random_state=random_state
    )

    # ============
    # Set up cluster parameters
    # ============
    plt.figure(figsize=(9 * 2 + 3, 13))
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.001, top=0.95, wspace=0.05, hspace=0.01
    )

    plot_num = 1

    default_base = {
        "quantile": 0.3,
        "eps": 0.3,
        "damping": 0.9,
        "preference": -200,
        "n_neighbors": 3,
        "n_clusters": 3,
        "min_samples": 7,
        "xi": 0.05,
        "min_cluster_size": 0.1,
    }

    datasets = [
        (
            noisy_circles,
            {
                "damping": 0.77,
                "preference": -240,
                "quantile": 0.2,
                "n_clusters": 2,
                "min_samples": 7,
                "xi": 0.08,
            },
        ),
        (
            noisy_moons,
            {
                "damping": 0.75,
                "preference": -220,
                "n_clusters": 2,
                "min_samples": 7,
                "xi": 0.1,
            },
        ),
        (
            varied,
            {
                "eps": 0.18,
                "n_neighbors": 2,
                "min_samples": 7,
                "xi": 0.01,
                "min_cluster_size": 0.2,
            },
        ),
        (
            aniso,
            {
                "eps": 0.15,
                "n_neighbors": 2,
                "min_samples": 7,
                "xi": 0.1,
                "min_cluster_size": 0.2,
            },
        ),
        (blobs, {"min_samples": 7, "xi": 0.1, "min_cluster_size": 0.2}),
        (no_structure, {}),
    ]

    for i_dataset, (dataset, algo_params) in enumerate(datasets):
        # update parameters with dataset-specific values
        params = default_base.copy()
        params.update(algo_params)

        X, y = dataset

        # normalize dataset for easier parameter selection
        X = StandardScaler().fit_transform(X)

        # estimate bandwidth for mean shift
        bandwidth = cluster.estimate_bandwidth(X, quantile=params["quantile"])

        # connectivity matrix for structured Ward
        connectivity = kneighbors_graph(
            X, n_neighbors=params["n_neighbors"], include_self=False
        )
        # make connectivity symmetric
        connectivity = 0.5 * (connectivity + connectivity.T)

        # ============
        # Create cluster objects
        # ============
        ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
        two_means = cluster.MiniBatchKMeans(n_clusters=params["n_clusters"])
        ward = cluster.AgglomerativeClustering(
            n_clusters=params["n_clusters"], linkage="ward", connectivity=connectivity
        )
        spectral = cluster.SpectralClustering(
            n_clusters=params["n_clusters"],
            eigen_solver="arpack",
            affinity="nearest_neighbors",
        )
        dbscan = cluster.DBSCAN(eps=params["eps"])
        optics = cluster.OPTICS(
            min_samples=params["min_samples"],
            xi=params["xi"],
            min_cluster_size=params["min_cluster_size"],
        )
        affinity_propagation = cluster.AffinityPropagation(
            damping=params["damping"], preference=params["preference"], random_state=0
        )
        average_linkage = cluster.AgglomerativeClustering(
            linkage="average",
            affinity="cityblock",
            n_clusters=params["n_clusters"],
            connectivity=connectivity,
        )
        birch = cluster.Birch(n_clusters=params["n_clusters"])
        gmm = mixture.GaussianMixture(
            n_components=params["n_clusters"], covariance_type="full"
        )

        clustering_algorithms = (
            ("MiniBatch\nKMeans", two_means),
            ("Affinity\nPropagation", affinity_propagation),
            ("MeanShift", ms),
            ("Spectral\nClustering", spectral),
            ("Ward", ward),
            ("Agglomerative\nClustering", average_linkage),
            ("DBSCAN", dbscan),
            ("OPTICS", optics),
            ("BIRCH", birch),
            ("Gaussian\nMixture", gmm),
        )

        for name, algorithm in clustering_algorithms:
            t0 = time.time()

            # catch warnings related to kneighbors_graph
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="the number of connected components of the "
                    + "connectivity matrix is [0-9]{1,2}"
                    + " > 1. Completing it to avoid stopping the tree early.",
                    category=UserWarning,
                )
                warnings.filterwarnings(
                    "ignore",
                    message="Graph is not fully connected, spectral embedding"
                    + " may not work as expected.",
                    category=UserWarning,
                )
                algorithm.fit(X)

            t1 = time.time()
            if hasattr(algorithm, "labels_"):
                y_pred = algorithm.labels_.astype(int)
            else:
                y_pred = algorithm.predict(X)

            plt.subplot(len(datasets), len(clustering_algorithms), plot_num)
            if i_dataset == 0:
                plt.title(name, size=18)

            colors = np.array(
                list(
                    islice(
                        cycle(
                            [
                                "#377eb8",
                                "#ff7f00",
                                "#4daf4a",
                                "#f781bf",
                                "#a65628",
                                "#984ea3",
                                "#999999",
                                "#e41a1c",
                                "#dede00",
                            ]
                        ),
                        int(max(y_pred) + 1),
                    )
                )
            )
            # add black color for outliers (if any)
            colors = np.append(colors, ["#000000"])
            plt.scatter(X[:, 0], X[:, 1], s=10, color=colors[y_pred])

            plt.xlim(-2.5, 2.5)
            plt.ylim(-2.5, 2.5)
            plt.xticks(())
            plt.yticks(())
            plt.text(
                0.99,
                0.01,
                ("%.2fs" % (t1 - t0)).lstrip("0"),
                transform=plt.gca().transAxes,
                size=15,
                horizontalalignment="right",
            )
            plot_num += 1

    plt.show()

def num2():
    # fetch mnist data
    mnist = fetch_openml('mnist_784')

    mnist_df = pd.DataFrame(mnist.data)
    mnist_df['label'] = mnist.target

    sample_df = pd.DataFrame(columns=mnist_df.columns)
    for i in range(10):
        temp_df = mnist_df[(mnist_df['label'] == f"{i}" )].sample(n=100)
        sample_df = pd.concat([sample_df,temp_df])
    sample_df = sample_df.sample(frac=1).reset_index(drop=True)
    print(sample_df['label'].value_counts())

    Y = sample_df['label'].astype(int).to_numpy()
    sample_df_img = sample_df.drop('label', axis = 1)
    X = sample_df_img.to_numpy()
    print(X.shape)
    print(Y.shape)

    return X, Y

def num3(X):
    agg = AgglomerativeClustering(n_clusters=10).fit(X)
    kmeans = KMeans(n_clusters=10, random_state=822).fit(X)
    gmm = GaussianMixture(n_components=10, n_init = 10, random_state=717).fit(X)
    spectral = SpectralClustering(n_clusters = 10).fit(X)

    print("Ground Truth\n",Y[:30])
    print("Agg\n", agg.labels_[:30])
    print("Kmeans\n",kmeans.predict(X)[:30])
    print("Gmm\n",gmm.predict(X)[:30])
    print("Spectral\n",spectral.labels_[:30])

    return agg, kmeans, gmm, spectral

def num4(agg, kmeans, gmm, spectral):
    # compute rand index
    print("Agglomerative clustering RI: ", adjusted_rand_score(Y, agg.labels_))
    print("K-means clustering RI:       ", adjusted_rand_score(Y, kmeans.predict(X)))
    print("Gaussian mixture model RI:   ", adjusted_rand_score(Y,gmm.predict(X)))
    print("Spectral clustering RI:      ", adjusted_rand_score(Y, spectral.labels_))
    print()

    # compute mutual information based score
    print("Agglomerative clustering MI: ", adjusted_mutual_info_score(Y, agg.labels_))
    print("K-means clustering MI:       ", adjusted_mutual_info_score(Y, kmeans.predict(X)))
    print("Gaussian mixture model MI:   ", adjusted_mutual_info_score(Y,gmm.predict(X)))
    print("Spectral clustering MI:      ", adjusted_mutual_info_score(Y, spectral.labels_))

def num5(agg, kmeans, gmm, spectral , X, Y):
    # GET center and labels
    # agglomerative
    a_centers = get_centers(X, agg.labels_)
    a_labels = fix_labels(agg.labels_, Y)
    # kmeans
    k_centers = get_centers(X, kmeans.predict(X))
    k_labels = fix_labels(kmeans.predict(X), Y)
    # gaussian
    g_centers = get_centers(X, gmm.predict(X))
    g_labels = fix_labels(gmm.predict(X), Y)
    # spectral
    s_centers = get_centers(X, spectral.labels_)
    s_labels = fix_labels(spectral.labels_, Y)

    print(a_labels,k_labels, g_labels, s_labels, sep='\n')

    # 1-NN
    centers = [a_centers, k_centers, g_centers, s_centers]
    labels = [a_labels, k_labels, g_labels, s_labels]
    for center, label in zip(centers, labels):
        knn_1 = KNeighborsClassifier(n_neighbors=1)
        knn_1.fit(center, label)
        score = knn_1.score(X, Y)
        print(score)  
        


if __name__=='__main__':
    num1()
    X, Y = num2()
    agg, kmeans, gmm, spectral = num3(X)
    num4(agg, kmeans, gmm, spectral)
    num5(agg, kmeans, gmm, spectral , X, Y)