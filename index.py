import pprint as pp

# get array data from csv
def getDataFromCsv(filename: str) -> list:
    file = open(filename, 'r')
    file.readline()
    rowsStringData = file.readlines()
    rowsStringData = [rowStringDatum.strip().lower().split(';') for rowStringDatum in rowsStringData]
    data = []
    for rowStringDatum in rowsStringData:
        datum = [float(feature) for feature in rowStringDatum]
        data.append(datum)
    return data

# normalization data
def normalization(data: list) -> list:
    # iterate per feature
    for i in range(1, len(data[0])):
        # get max and min
        feature = [datum[i] for datum in data]
        maxValue = max(feature)
        minValue = min(feature)
        # iterate per data and normalize its feature
        for j in range(0, len(data)):
            data[j][i] = ( data[j][i] - minValue ) / ( maxValue - minValue )
    return data

# get centroids of data
def randomClustering(data: list, K: int) -> list:
    # create variable for storing K cluster data
    indexClusters = [[]] * K
    # clustering data based on modulus
    for idx in range(0, len(data)):
        indexClusters[ idx % K ] = indexClusters[ idx % K ] + [idx]
    return indexClusters

#get centroid of data
def getCentroid(indexCluster: list, data: list) -> list:
    # remove first element of data (data number)
    featureData = [datum[1:] for datum in data]
    # get number of feature
    featureCount = len(featureData[0])
    # set 0 elements of array that represent feature
    centroid = [ 0 ] * featureCount
    # iterate each data in cluster
    for IndexData in indexCluster:
        # iterate each feature in a data
        for featureIndex in range(0, featureCount):
            centroid[featureIndex] += ( featureData[IndexData][featureIndex] / len(indexCluster) )
    return centroid

# get all cluster centroids -- centroid index represents index of cluster
def getCentroids(indexClusters: list, data: list) -> list:
    centroids = []
    for indexCluster in indexClusters:
        centroids.append(getCentroid(indexCluster, data))
    return centroids

# get clostest distance
def getEuclideanDistance(centroid: list, datum: list) -> float:
    # remove first element of data (data number)
    featureData = datum[1:]
    total = 0.0
    for idx in range(len(centroid)) :
        diff = abs(featureData[idx] - centroid[idx])**2
        total += diff
    return total**0.5

# array2 are equal or not
def equal(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2):
        return False
    else:
        flag = True
        for i in range(0, len(arr1)):
            flag = flag and (arr1[i] == arr2[i])
        return flag

# check whether there is a moving data to another cluster or not
def isMoving(clusters1: list, clusters2: list) -> bool:
    flag = False
    for i in range(0, len(clusters1)):
        flag = flag or not (equal(clusters1[i], clusters2[i]))
    return flag

# get shortest distance to centroid
def getNewClusters(centroids: list, data: list) -> dict:
    indexClusters = [[]] * len(centroids)
    objective = 0
    for dataIndex in range(0, len(data)):
        minValue = float('inf')
        newCluster = 0
        for centroidIndex in range(0, len(centroids)):
            distance = getEuclideanDistance(centroids[centroidIndex], data[dataIndex])
            if(distance < minValue):
                newCluster = centroidIndex
                minValue = distance
        objective += minValue
        indexClusters[newCluster] = indexClusters[newCluster] + [dataIndex]
    return {
        'indexClusters': indexClusters,
        'objective': objective
    }


def main():
    # STEP 1 - get number of cluster(K) from user input
    K = int(input("Masukkan Jumlah Cluster : "))
    # filename
    filename = 'dataset.csv'
    # get aray of data from csv
    data = getDataFromCsv(filename)
    # normalize data
    data = normalization(data)
    # STEP 2 - get clustered Data
    indexClusters = randomClustering(data, K)
    # STEP 3 - get centroids each cluster
    centroids = getCentroids(indexClusters, data)

    threshold = 0.1
    objective = 0
    diff = float('inf')
    moving = True
    nextClusters = []
    nextCentroids = []
    numberOfIteration = 0
    # STEP 5 - iterate until stable
    while moving or diff > threshold:
        # STEP 4 - move data to clostest centroid
        next = getNewClusters(centroids, data)
        nextObjective = next['objective']
        nextIndexClusters = next['indexClusters']
        moving = isMoving(indexClusters, nextIndexClusters)
        diff = abs(objective - nextObjective)
        # set previous value
        objective = nextObjective
        centroids = getCentroids(nextIndexClusters, data)
        indexClusters = nextIndexClusters
        numberOfIteration += 1

    print('\n-----Clustering Result----\n')
    print('Treshold  : 0.1')
    print('Iteration : ', numberOfIteration)
    for i in range(0, len(indexClusters)):
        print('\nData Number in Cluster ', i + 1 ,' :')
        print('[ ', end='')
        for indexData in indexClusters[i]:
            print(int(data[indexData][0]),', ', end='')
        print('\b\b]', end='')
    print('\n')

main()