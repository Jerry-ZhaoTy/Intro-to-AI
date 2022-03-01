import numpy as np
import random
import pandas as pd
import math


def get_dataset(filename):
    """
    INPUT: 
        filename - a string representing the path to the csv file.

    RETURNS:
        An n by m+1 array, where n is # data points and m is # features.
        The labels y should be in the first column.
    """
    
    dataset = None
    csvfile = pd.read_csv(filename)
    dataset = np.array(csvfile)
    dataset = np.delete(dataset,0,1)
    return dataset


def print_stats(dataset, col):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        col     - the index of feature to summarize on. 
                  For example, 1 refers to density.

    RETURNS:
        None
    """
    data = dataset[:,col]
    print(len(data))
    sum = 0
    for i in range (0,len(data)):
        sum += data[i]
    standard_mean = sum/len(data)
    print('{:.2f}'.format(standard_mean))
    standard_variance = 0
    for j in range (0,len(data)):
        variance = (data[j] - standard_mean)**2
        standard_variance += variance
    standard_deviation = math.sqrt(standard_variance/(len(data)-1))
    print('{:.2f}'.format(standard_deviation))
    
    pass


def regression(dataset, cols, betas):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        mse of the regression model
    """
    mse = None
    squared_errors = 0
    for i in range (0,len(dataset[:,0])):
        error = betas[0]
        for j in range (0,len(cols)):
            error = error + betas[j+1]*dataset[:,cols[j]][i]
        squared_errors += (error-dataset[:,0][i])**2
    mse = squared_errors/len(dataset[:,0])
    
    return mse


def gradient_descent(dataset, cols, betas):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        An 1D array of gradients
    """
    grads = []
    for k in range (0,len(betas)):
        errors = 0
        for i in range (0,len(dataset[:,0])):
            error = betas[0]
            for j in range (0,len(cols)):
                error = error + betas[j+1]*dataset[:,cols[j]][i]
            if k == 0:
                errors += error-dataset[:,0][i]
            else:
                errors += (error-dataset[:,0][i])*dataset[:,cols[k-1]][i]
        grads.append(errors*2/len(dataset[:,0]))
        
    return np.array(grads)


def iterate_gradient(dataset, cols, betas, T, eta):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    for i in range (0,T):
        print(i+1,end=' ')
        grads = gradient_descent(dataset, cols, betas)
        for j in range (0,len(betas)):
                betas[j] = betas[j]-eta*grads[j]
        mse = regression(dataset, cols, betas)
        print('{:.2f}'.format(mse),end=' ')
        for k in range (0,len(betas)):
            if k == len(betas)-1:
                print('{:.2f}'.format(betas[k]))
            else:
                print('{:.2f}'.format(betas[k]),end=' ')
    pass


def compute_betas(dataset, cols):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.

    RETURNS:
        A tuple containing corresponding mse and several learned betas
    """
    betas = None
    mse = 0
    X = np.ones((len(dataset[:,0]),len(cols)+1))
    Y = dataset[:,0]
    for i in range (0,len(cols)):
        X[:,i+1] = dataset[:,cols[i]]
    XT = np.transpose(X)
    betas = np.dot(np.linalg.inv(np.dot(XT,X)),np.dot(XT,Y))
    mse = regression(dataset,cols,betas)
    
    return (mse, *betas)


def predict(dataset, cols, features):
    """
    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        features- a list of observed values

    RETURNS:
        The predicted body fat percentage value
    """
    mse, *betas = compute_betas(dataset, cols)
    result = betas[0]
    for i in range (0, len(features)):
        result = result + betas[i+1]*features[i]
    
    return result


def random_index_generator(min_val, max_val, seed=42):
    """
    DO NOT MODIFY THIS FUNCTION.
    DO NOT CHANGE THE SEED.
    This generator picks a random value between min_val and max_val,
    seeded by 42.
    """
    random.seed(seed)
    while True:
        yield random.randrange(min_val, max_val)


def sgd(dataset, cols, betas, T, eta):
    """
    TODO: implement this function.
    You must use random_index_generator() to select individual data points.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """    
    random = random_index_generator(0, len(dataset))
    
    for i in range (0,T):
        
        grads = []
        n = next(random)
        
        for b in range (0,len(betas)):
            errors = 0
            error = betas[0]
            for a in range (0,len(cols)):
                error = error + betas[a+1]*dataset[:,cols[a]][n]
            if b == 0:
                errors = error-dataset[:,0][n]
            else:
                errors = (error-dataset[:,0][n])*dataset[:,cols[b-1]][n]
            grads.append(errors*2)
        grads = np.array(grads)
        
        print(i+1,end=' ')
        for j in range (0,len(betas)):
                betas[j] = betas[j]-eta*grads[j]
        mse = regression(dataset, cols, betas)
        print('{:.2f}'.format(mse),end=' ')
        for k in range (0,len(betas)):
            if k == len(betas)-1:
                print('{:.2f}'.format(betas[k]))
            else:
                print('{:.2f}'.format(betas[k]),end=' ')
                
    pass


if __name__ == '__main__':

    pass