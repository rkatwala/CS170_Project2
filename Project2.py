import math
import copy



def main():
    print 'Welcome to Rahul Katwala\'s Feature Selection Algorithm.'
    file = raw_input('Type in the name of the file to test: ')


    try:
        data = open(file, 'r')
    except:
        raise IOError('Invalid file. Exiting...')

  
    first_line = data.readline()

    total_features = len(first_line.split()) - 1

    
    data.seek(0)
    total_instances = 0;
    for line in data:
        total_instances = total_instances + 1

   
    data.seek(0)

    # Store data into variable/array
    instances = []
    for i in range(total_instances):
        temp = [];
        for j in data.readline().split():
            temp.append(float(j))
        instances.append(temp)
    
    # Algorithm selection
    print 'Type the number of the algorithm you want to run.'
    print '1. Forward Selection'
    print '2. Backward Elimination'
    
    input = int(raw_input())
  
    print 'This dataset has ' + str(total_features) + ' features (not including the class attribute), with ' + str(total_instances) + ' instances.'

    normalized_instances = normalize(instances, total_features, total_instances)

 
    features = []
    for i in range(total_features):
        features.append(i+1)

    

    if input == 1:
        accuracy = oneOutValidator(normalized_instances, features, total_instances)
        print 'Running nearest neighbor with all ', total_features, ' features, using "leaving-one-out" evaluation, I get an accuracy of ', accuracy, '%.\nBeginning Search.\n'
        forwardSelection(normalized_instances, total_instances, total_features)
    elif input == 2:
        accuracy = oneOutValidator(normalized_instances, features, total_instances)
        print 'Running nearest neighbor with all ', total_features, ' features, using "leaving-one-out" evaluation, I get an accuracy of ', accuracy, '%.\nBeginning Search.\n'
        backwardElimination(normalized_instances, total_instances, total_features, accuracy)



def nearestNeighborClassifier(data, point, features_used, total_instances):

    nearest_neighbor = 0
    shortest_distance = float('inf')
    for instance in range(total_instances):
        
        if point != instance:
            distance = 0
            for feature in features_used:
                distance = distance + ((data[instance][feature] - data[point][feature]) * (data[instance][feature] - data[point][feature]))

            distance = math.sqrt(distance)

            if shortest_distance > distance:
                nearest_neighbor = instance
                shortest_distance = distance

    return nearest_neighbor


def oneOutValidator(data, features_used, total_instances):
    counter = 0.0
    for instance in range(total_instances):
        neighbor = nearestNeighborClassifier(data, instance, features_used, total_instances)

        if data[neighbor][0] == data[instance][0]:
            counter = counter + 1

    return ((counter / total_instances) * 100)


def forwardSelection(data, total_instances, total_features):

    features_used = {-5: '001'}
    del features_used[-5]
    full_set = {-5: '001'}
    del full_set[-5]

    top_accuracy = 0.0

    for i in range(total_features):
        new_feature = 0
        feature_add = 0
        local_accuracy = 0.0
        j=1
        while j <= total_features:
            
            
            if features_used.get(j) == None:
                
                temp_features_used = (list(features_used.keys()))
                
                temp_features_used.append(j)

                accuracy = oneOutValidator(data, temp_features_used, total_instances)
                print '\tUsing feature(s) ', temp_features_used, ' accuracy is ', accuracy, '%'
                if accuracy > top_accuracy:
                    top_accuracy = accuracy
                    feature_add = j
                if accuracy > local_accuracy:
                    local_accuracy = accuracy
                    new_feature = j
            j = j+1
        if feature_add != 0:
            features_used[feature_add] = '001'
            full_set[feature_add] = '001'
            print '\n\nFeature set ', (list(features_used.keys())), ' was best, accuracy is ', top_accuracy, '%\n\n'
        else:
            print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)'
            features_used[new_feature] = '001'
            print 'Feature set ', (list(features_used.keys())), ' was best, accuracy is ', local_accuracy, '%\n\n'
        

    print 'Finished search!! The best feature subset is', list(full_set.keys()), ' which has an accuracy of accuracy: ', top_accuracy, '%'

def backwardElimination(data, total_instances, total_features, top_accuracy):

    features_left = {-1: '001'}
    full_set = {-1: '001'}
    for i in range(total_features):
        features_left[i+1] = '001'
        full_set[i+1] = '001'
    
    del features_left[-1]
    del full_set[-1]
    for i in range(total_features):
        explored_feature = 0
        remove_feature = 0
        local_accuracy = 0.0
        
        for j in range(total_features):
            
            if features_left.get(j+1) != None:
                temp_features_left = (list(features_left.keys()))
                temp_features_left.remove(j+1)
                accuracy = oneOutValidator(data, temp_features_left, total_instances)
                
                if accuracy > top_accuracy:
                    top_accuracy = accuracy
                    explored_feature = j+1
                if accuracy > local_accuracy:
                    local_accuracy = accuracy
                    remove_feature = j+1
                    
                print '\tUsing feature(s) ', temp_features_left, ' accuracy is ', accuracy, '%'
                    
        if explored_feature != 0:
            del features_left[explored_feature]
            del full_set[explored_feature]
            print '\n\nFeature set ', (list(features_left.keys())), ' was best, accuracy is ', top_accuracy, '%\n\n'
        else:
            print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)'
            del features_left[remove_feature]
            print 'Feature set ', (list(features_left.keys())), ' was best, accuracy is ', local_accuracy, '%\n\n'

    print 'Finished search!! The best feature subset is', list(full_set.keys()), ' which has an accuracy of accuracy: ', top_accuracy, '%'












if __name__ == '__main__':
    main()




