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


def forwardSelection(data, num_instances, num_features):

    encountered = {-5: '001'}
    del encountered[-5]
    final_set = {-5: '001'}
    del final_set[-5]

    topAccuracy = 0.0

    for i in range(num_features):
        add_this = 0
        local_add = 0
        localAccuracy = 0.0
        j=1
        while j <= num_features:
            
            
            if encountered.get(j) == None:
                
                temp_subset = (list(encountered.keys()))
                
                temp_subset.append(j)

                accuracy = oneOutValidator(data, temp_subset, num_instances)
                print '\tUsing feature(s) ', temp_subset, ' accuracy is ', accuracy, '%'
                if accuracy > topAccuracy:
                    topAccuracy = accuracy
                    add_this = j
                else:
                    localAccuracy = accuracy
                    local_add = j
            j = j+1
        if add_this != 0:
            encountered[add_this] = '001'
            final_set[add_this] = '001'
            print '\n\nFeature set ', (list(encountered.keys())), ' was best, accuracy is ', topAccuracy, '%\n\n'
        else:
            print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)'
            encountered[local_add] = '001'
            print 'Feature set ', (list(encountered.keys())), ' was best, accuracy is ', localAccuracy, '%\n\n'
        

    print 'Finished search!! The best feature subset is', list(final_set.keys()), ' which has an accuracy of accuracy: ', topAccuracy, '%'

def backwardElimination(data, num_instances, num_features, topAcc):

    encountered = {-1: '001'}
    final_set = {-1: '001'}
    for i in range(num_features):
        encountered[i+1] = '001'
        final_set[i+1] = '001'
    
    del encountered[-1]
    del final_set[-1]
    for i in range(num_features):
        remove_this = 0
        local_remove = 0
        localAccuracy = 0.0
        
        for j in range(num_features):
            
            if encountered.get(j+1) != None:
                temp_subset = (list(encountered.keys()))
                temp_subset.remove(j+1)
                accuracy = oneOutValidator(data, temp_subset, num_instances)
                
                if accuracy > topAcc:
                    topAcc = accuracy
                    remove_this = j+1
                else:
                    localAccuracy = accuracy
                    local_remove = j+1
                    
                print '\tUsing feature(s) ', temp_subset, ' accuracy is ', accuracy, '%'
                    
        if remove_this != 0:
            del encountered[remove_this]
            del final_set[remove_this]
            print '\n\nFeature set ', (list(encountered.keys())), ' was best, accuracy is ', topAcc, '%\n\n'
        else:
            print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)'
            del encountered[local_remove]
            print 'Feature set ', (list(encountered.keys())), ' was best, accuracy is ', localAccuracy, '%\n\n'

    print 'Finished search!! The best feature subset is', list(final_set.keys()), ' which has an accuracy of accuracy: ', topAcc, '%'














if __name__ == '__main__':
    main()




