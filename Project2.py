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
    


















if __name__ == '__main__':
    main()




