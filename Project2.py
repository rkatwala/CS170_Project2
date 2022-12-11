import math
import copy

def main():
    print 'Welcome to Rahul Katwala\'s Feature Selection Algorithm.'
    file = raw_input('Type in the name of the file to test: ')

    #opening the file if failed then exit
    try:
        data = open(file, 'r')
    except:
        raise IOError('Invalid file. Exiting...')

    #read the data to get the first line which will be the features
    first_line = data.readline()

    total_features = len(first_line.split()) - 1

    
    data.seek(0)
    total_instances = 0;
    #counts the total number of instances
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
    
    # chooses the alogrithm
    print 'Type the number of the algorithm you want to run.'
    print '1. Forward Selection'
    print '2. Backward Elimination'
    
    input = int(raw_input())
  
    print 'This dataset has ' + str(total_features) + ' features (not including the class attribute), with ' + str(total_instances) + ' instances.'
    #calls the normalize function to normalize all the data
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

        
def nearestNeighborClassifier(data, current_instance, features_used, total_instances):

    nearest_neighbor = 0
    shortest_distance = float('inf')
    #goes through all the instances
    for instance in range(total_instances):
        #if the current instance is the same skip over, only do the ones which have not been done
        if current_instance != instance:
            distance = 0
            #checks and updates the nearest neighbor
            for feature in features_used:
                distance = distance + ((data[instance][feature] - data[current_instance][feature]) * (data[instance][feature] - data[current_instance][feature]))

            distance = math.sqrt(distance)
            #if the shorter distance is greater than the distance then update the shorter distance to the new distance
            if shortest_distance > distance:
                nearest_neighbor = instance
                shortest_distance = distance

    return nearest_neighbor


def oneOutValidator(data, features_used, total_instances):
    correct = 0.0
    for instance in range(total_instances):
        #check the neighbor for the instance
        neighbor = nearestNeighborClassifier(data, instance, features_used, total_instances)
        #if the data values are the same add 1 to counter for match
        if data[neighbor][0] == data[instance][0]:
            correct = correct + 1
    #gets the accuracy and multiply by 100
    return ((correct / total_instances) * 100)


def normalize(data, total_features, total_instances):
    #first get the mean
    mean = []
    x = 0;
    for i in range(1, total_features + 1):
        for row in data:
            x = x + row[i]
        x = x/total_instances
        mean.append(x)
    #then get the standard deviation
    standard_deviation = []
    x=0
    for i in range(1, total_features + 1):
        for row in data:
            x = x + (row[i] - mean[i-1]) * (row[i] - mean[i-1])
        x = math.sqrt(x/total_instances)
        
        standard_deviation.append(x)

    for i in range(total_instances):
        for j in range(1, total_features + 1):
            data[i][j] = ((data[i][j] - mean[j-1]) / standard_deviation[j-1])

    return data


def forwardSelection(data, total_instances, total_features):
    
    #Initialize dicts with values that will never encounter
    features_used = {-5: '001'}
    #delete those values to get empty dict
    del features_used[-5]
    full_set = {-5: '001'}
    del full_set[-5]
    #top accuracy is 0.0 right now
    top_accuracy = 0.0
    #
    for i in range(total_features):
        #initalizing all the variables
        new_feature = 0
        feature_add = 0
        local_accuracy = 0.0
        j=1
        while j <= total_features:
            #if the feature has not been used yet
            if features_used.get(j) == None:
                #create a temp features used to check accuracy with the new feature which has not been used
                temp_features_used = (list(features_used.keys()))
                
                temp_features_used.append(j)

                accuracy = oneOutValidator(data, temp_features_used, total_instances)
                #if accuracy is higher than the previous top accuracy update the value of top accuracy to the new accuracy
                if accuracy > top_accuracy:
                    top_accuracy = accuracy
                    feature_add = j
                if accuracy > local_accuracy:
                    local_accuracy = accuracy
                    new_feature = j
                print '\tUsing feature(s) ', temp_features_used, ' accuracy is ', accuracy, '%'
            j = j+1
        #if the feature has not been used yet add it to the list of features used
        if feature_add != 0:
            features_used[feature_add] = '001'
            full_set[feature_add] = '001'
            print '\n\nFeature set ', (list(features_used.keys())), ' was best, accuracy is ', top_accuracy, '%\n\n'
        #if the accuracy decreases alert
        else:
            features_used[new_feature] = '001'
            print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)\nFeature set ', (list(features_used.keys())), ' was best, accuracy is ', local_accuracy, '%\n\n'
        
    print 'Finished search!! The best feature subset is', list(full_set.keys()), ' which has an accuracy of accuracy: ', top_accuracy, '%'

def backwardElimination(data, total_instances, total_features, top_accuracy):
    #initialize dicts with all the features
    features_left = {-1: '001'}
    full_set = {-1: '001'}
    for i in range(total_features):
        features_left[i+1] = '001'
        full_set[i+1] = '001'
    #delete the values used to initialize the dicts
    del features_left[-1]
    del full_set[-1]
    for i in range(total_features):
        explored_feature = 0
        remove_feature = 0
        local_accuracy = 0.0
        
        for j in range(total_features):
            #only if the feature already in the set
            if features_left.get(j+1) != None:
                temp_features_left = (list(features_left.keys()))
                temp_features_left.remove(j+1)
                accuracy = oneOutValidator(data, temp_features_left, total_instances)
                #if accuracy is greater than the top accuracy then swap the values to update the top accuracy
                if accuracy > top_accuracy:
                    top_accuracy = accuracy
                    explored_feature = j+1
                if accuracy > local_accuracy:
                    local_accuracy = accuracy
                    remove_feature = j+1
                    
                print '\tUsing feature(s) ', temp_features_left, ' accuracy is ', accuracy, '%'
        #delete the feature that has been used
        if explored_feature != 0:
            del features_left[explored_feature]
            del full_set[explored_feature]
            print '\n\nFeature set ', (list(features_left.keys())), ' was best, accuracy is ', top_accuracy, '%\n\n'
        else:
            del features_left[remove_feature]
            print '\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)\nFeature set ', (list(features_left.keys())), ' was best, accuracy is ', local_accuracy, '%\n\n'

    print 'Finished search!! The best feature subset is', list(full_set.keys()), ' which has an accuracy of accuracy: ', top_accuracy, '%'

if __name__ == '__main__':
    main()




