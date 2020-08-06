#The following code was written based off of the knowledge provided by both Professor Memo and the Human Activity
# recognition case
# found @ https://machinelearningmastery.com/cnn-models-for-human-activity-recognition-time-series-classification/
# we based our model on their work with time series recognition for gyroscopic and acceleration data.
#
# Imports for the CNN model
from IPython.display import SVG
import pydot
import graphviz
from numpy import mean
from numpy import std
from numpy import dstack
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from tensorflow.python.keras.utils.vis_utils import plot_model, model_to_dot

# load a CSV file as an array for use
def load_data_file(path):
    data_frame = read_csv(path, header=None, delim_whitespace=True)
    return data_frame.values

# reformats the data from load_data_file() into a 3d array
def load_file_group(file_names, prefix_variable=''):
    loaded_data = list()
    for names in file_names:
        data = load_data_file(prefix_variable + names)
        loaded_data.append(data)
    # Uses dstack to create a 3d array of features
    loaded_data = dstack(loaded_data)
    return loaded_data


# loads a series of data set files from the directories they are stored in based on the group tag(test or train)
def load_dataset_group(group, group_2, prefix_variable=''):
    path = prefix_variable + group_2 + r'\EEG Signals'
    # we have 8 channels that we recorded data from and the data from these 8 channels are held in files, this loads those
    # files as an array
    file_names = list()
    #The name of the file for the respective test and train datasets found in their respective train and test folders
    file_names += [r'\masterFile.txt']
    # loads the input data we are using
    X_variable = load_file_group(file_names, path)
    # loads the output
    y_variable = load_data_file(prefix_variable + group_2 + r'\y_' + group + '.txt')
    return X_variable, y_variable


# loads the data set returning the elements of the respective arrays as x or y for the respective groups test and train
def load_dataset(prefix_variable=''):
    # loads all of the training data from the directory
    train_set_X, train_set_y = load_dataset_group('train', r"\train",
                                        prefix_variable + r'C:\Users\DesTech\Downloads\Final_Data\Final_Data')
    print(train_set_X.shape, train_set_y.shape)
    # loads all of the testing data from the directory
    test_set_X, test_set_y = load_dataset_group('test', r"\test", prefix_variable + r'C:\Users\DesTech\Downloads\Final_Data\Final_Data')
    print(test_set_X.shape, test_set_y.shape)
    print(train_set_X.shape, train_set_y.shape, test_set_X.shape, test_set_y.shape)
    return train_set_X, train_set_y, test_set_X, test_set_y


# runs and tests the model, this is where the neural network is actually instantiated
def test_model(train_set_X, train_set_y, test_set_X, test_set_y):
    #sets required variables for the keras.fit() method, the batch size is how many samples are processed at one time,
    #epochs are how long the neural network trains for and verbose is for trouble shooting and debugging
    verbose, epochs, batch_size = 0, 1000, 10
    number_of_timesteps, number_of_features, number_of_outputs = train_set_X.shape[1], train_set_X.shape[2], train_set_y.shape[1]
    #instantiates the model as a keras.Sequential() model
    test_CNN = Sequential()

    #input layer
    test_CNN.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(number_of_timesteps, number_of_features)))
    #test_CNN.add(Dropout(0.5))

    #hidden layers
    test_CNN.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
    #test_CNN.add(Conv1D(filters=64, kernel_size=3, activation='tanh'))

    #the drop out layer, this is used to help prevent overfitting by randomly dropping nodes in the network, in the case
    # of the max pooling it downsamples the data we have to only include maximum values, or the most present features
    # and then creates an array holding those features and passes it on to the next layer
    test_CNN.add(Dropout(0.5))
    test_CNN.add(MaxPooling1D(pool_size=60))
    test_CNN.add(Flatten())
    test_CNN.add(Dense(100, activation='sigmoid'))
    test_CNN.add(Dropout(0.5))

    #output layer
    test_CNN.add(Dense(number_of_outputs, activation='sigmoid'))

    #This is a keras method designed to plot the model as a diagram
    #plot_model(test_CNN, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
    #SVG(model_to_dot(test_CNN).create(prog='dot', format='svg'))
    #print(test_CNN.summary())

    #Compiles the model to run takes a series of metrics used while training the CNN, in this case we use Binary_Cross Entropy
    # as the loss function, adam as the optimizer, and accuracy as the evaluation metric used to judge success
    test_CNN.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # .fit() is used to actually train the CNN epochs being how long the neural network trains, batch_size being how
    # many samples are processed before updating the weights
    test_CNN.fit(train_set_X, train_set_y, epochs=epochs, batch_size=batch_size, verbose=verbose)

    # .evaluate() is used to do just that to verify the accuracy of the corellation found by the CNN and then return it
    _, accuracy = test_CNN.evaluate(test_set_X, test_set_y, batch_size=batch_size, verbose=0)
    return accuracy


# this takes the accuraccy scores generated from .test_model() and makes them readable by finding the mean of the scores
# and the standard deviation of the scores
def results_summary(scores_list):
    print(scores_list)
    m_variable, s_variable = mean(scores_list), std(scores_list)
    print('Accuracy: %.3f%% (+/-%.3f)' % (m_variable, s_variable))


# this is used to initialize the network and variables and then test then CNN
def run_network(repeats=10):
    # calls load_dataset() to load the data into the required variables
    train_set_X, train_set_y, test_set_X, test_set_y = load_dataset()
    # runs the network a number of times equal to repeats, in this case it is set to 10
    scores_list = list()
    for r in range(repeats):
        results = test_model(train_set_X, train_set_y, test_set_X, test_set_y)
        results = results * 100.0
        print('>#%d: %.3f' % (r + 1, results))
        scores_list.append(results)
    # summarizes the scores for greater readability and understanding
    results_summary(scores_list)


#without this the CNN won't run, calling run_network() is required for the network to function
run_network()
