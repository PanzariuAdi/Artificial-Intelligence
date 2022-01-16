import math
from random import random, seed
_AND_FILE_ = "AND.txt"
_OR_FILE_ = "OR.txt"
_XOR_FILE_ = "XOR.txt"

def read_from_file(file_to_open):
    file = open(file_to_open)
    lines = file.readlines()
    input, output, dataset = [], [], []

    for line in lines:
        dataset.append((int(line[0]), int(line[2]), int(line[4])))
        input.append((int(line[0]), int(line[2])))
        output.append(int(line[4]))
    
    return input, output, dataset 

# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs):
	network = list()
	hidden_layer = [{'weights':[random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]
	network.append(hidden_layer)
	output_layer = [{'weights':[random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
	network.append(output_layer)
	return network

def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation

def transfer(activation):
    # return 1.0 / (1.0 + math.exp(-activation))
    return float(math.exp(activation) / (math.exp(activation) + 1))  

def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
            inputs = new_inputs
    return inputs

def trasfer_derivative(output):
    return output * (1.0 - output)

def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network) - 1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(neuron['output'] - expected[j])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * trasfer_derivative(neuron['output'])

def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
            for neuron in network[i]:
                for j in range(len(inputs)):
                    neuron['weights'][j] -= l_rate * neuron['delta'] * inputs[j]
                neuron['weights'][-1] -= l_rate * neuron['delta']

def train_network(network, train, l_rate, n_epoch, n_outputs):
    for epoch in range(n_epoch):
        sum_error = 0
        for row in train:
            outputs = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i] - outputs[i])**2 for i in range(len(expected))]) 
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)
        print(f'Epoch : {epoch}, l_rate = {l_rate}, error = {sum_error}')


def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))

if __name__ == '__main__':
    seed(1)
    number_of_epocs = int(input("Dati numarul de epoci : "))
    training_rate = float(input("Dati training rate : "))
    input, output, dataset = read_from_file(_XOR_FILE_)

    n_inputs = len(dataset[0]) - 1
    n_outputs = len(set([row[-1] for row in dataset]))
    network = initialize_network(n_inputs, 1, n_outputs)
    train_network(network, dataset, training_rate, number_of_epocs, n_outputs)

    for row in dataset:
        prediction = predict(network, row)
        print(f'Expected : {row[-1]} >>> Got : {prediction}')