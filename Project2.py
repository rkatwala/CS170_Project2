import math
import copy



def main():
    print 'Welcome to Rahul Katwala\'s Feature Selection Algorithm.'
    file = raw_input('Type in the name of the file to test: ')


    try:
        data = open(file, 'r')
    except:
        raise IOError('Invalid file. Exiting...')

  
    firstLine = data.readline()

    num_features = len(firstLine.split()) - 1

    
    data.seek(0)
    num_instances = 0;
    for line in data:
        num_instances = num_instances + 1

   
    data.seek(0)

    # Store data into variable/array
    instances = []
    for i in range(num_instances):
        temp = [];
        for j in data.readline().split():
            temp.append(float(j))
        instances.append(temp)
    
    # Algorithm selection
    print 'Type the number of the algorithm you want to run.'
    print '1. Forward Selection'
    print '2. Backward Elimination'
    
    choice = int(raw_input())
  
    print 'This dataset has ' + str(num_features) + ' features (not including the class attribute), with ' + str(num_instances) + ' instances.'

    normalized_instances = normalize(instances, num_features, num_instances)

 
    all_features = []
    for i in range(num_features):
        all_features.append(i+1)

    accuracy = oneOutValidator(normalized_instances, all_features, num_instances)
    print 'Running nearest neighbor with all ', num_features, ' features, using "leaving-one-out" evaluation, I get an accuracy of ', accuracy, '%.'


    print 'Beginning search.\n\n'

    if choice == 1:
        #forwardSelection(normalized_instances, num_instances, num_features)
    elif choice == 2:
        #backwardElimination(normalized_instances, num_instances, num_features, accuracy)
    

    
    
def normalize(data, num_features, num_instances):

    mean = []
    x = 0;
    for i in range(1, num_features + 1):
        for row in data:
            x = x + row[i]
        x = x/num_instances
        mean.append(x)

    std = []
    x=0
    for i in range(1, num_features + 1):
        for row in data:
            x = x + (row[i] - mean[i-1]) * (row[i] - mean[i-1])
        x = math.sqrt(x/num_instances)
        
        std.append(x)

  
  
  
    for i in range(num_instances):
        for j in range(1, num_features + 1):
            data[i][j] = ((data[i][j] - mean[j-1]) / std[j-1])

    return data



def nearestNeighborClassifier(data, point, feature_subset, num_instances):

    nearestNeighbor = 0
    shortest_distance = float('inf')
    for i in range(num_instances):
        
        if point != i:
            distance = 0
            for j in feature_subset:
                distance = distance + ((data[i][j] - data[point][j]) * (data[i][j] - data[point][j]))

            distance = math.sqrt(distance)

            if shortest_distance > distance:
                nearestNeighbor = i
                shortest_distance = distance

    return nearestNeighbor


def oneOutValidator(data, feature_subset, num_instances):
    correct = 0.0
    for i in range(num_instances):
        neighbor = nearestNeighborClassifier(data, i, feature_subset, num_instances)

        if data[neighbor][0] == data[i][0]:
            correct = correct + 1

    return ((correct / num_instances) * 100)
















if __name__ == '__main__':
    main()




