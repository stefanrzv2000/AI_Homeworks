import numpy as np

#ACTIVATION FUNCTIONS
def sigmoid(input):
      return 1 / (1 + np.exp(-input))

# def softmax(input):

#     e_x = np.exp(input - np.max(input))
#     return e_x / e_x.sum()


def init(inputs, outputs):
    w = np.random.rand(outputs, inputs)-0.5
    b = np.random.rand(outputs,1)-0.5

    return w, b


def backpropagation_alg(w1,b1, w2,b2,eta, nr_iterations, training_set,activations):
    xs, ts = training_set

    weights=[w1,w2]
    biases=[b1,b2]

    while nr_iterations > 0:
        for i in range(len(xs)):

            deltas = []
            ys = []

            x = xs[i]
            t = ts[i]
            ys.append(x)

            x=x.reshape(-1,1)
            z = w1.dot(x) + b1

            output = activations[0](z)

            ys.append(output)

            x=output
            z = w2.dot(x)+b2

            output = activations[1](z)

            ys.append(output)

            t = np.asarray([t])

            deltas = [None for i in range(3)]
            deltas[-1] = output-t.T

            nr_layers=2
            it=-1

            while nr_layers>0:

                summ = weights[it].T.dot(deltas[it])
                deltas[it-1] = (ys[it - 1] * (1 - ys[it - 1]) * summ)
                weights[it] -= eta * deltas[it].dot(ys[it - 1].reshape(1, -1))
                biases[it] -= eta * deltas[it]

                nr_layers-=1
                it-=1


        nr_iterations -= 1

    return w1,b1,w2,b2


def get_dataset(outputs : str):

    outputs = outputs.replace(" ","")
    x = np.asarray([
        [0,0],
        [0,1],
        [1,0],
        [1,1]
    ])

    y = [int(c) for c in outputs]
    y = np.asarray(y)

    return x,y

def evaluate(w1,b1,w2,b2,x):

    x = x.reshape(-1, 1)
    z1 = w1.dot(x) + b1
    z2 = sigmoid(z1)
    z2 = w2.dot(z2) + b2
    z2 = sigmoid(z2)

    z2 = 1 if z2.flatten()[0] > 0.5 else 0

    return z2
        

def train_boolean():

    func = input("Choose boolean function (insert 4 boolean values): ")
    epochs = input("Choose number of epochs: ")
    epochs = int(epochs)

    x,y = get_dataset(func)
    print("function defined:")
    for i in range(4):
        print(f"f({x[i,0]},{x[i,1]}) = {y[i]}")

    w1,b1 = init(2,2)
    w2,b2 = init(2,1)

    activations=[]
    activations.append(sigmoid)
    activations.append(sigmoid)

    w1,b1,w2,b2=backpropagation_alg(w1,b1,w2,b2,1,epochs,(x,y),activations)

    print("evaluating the network:")

    for i in range(4):
        print(f"f({x[i,0]},{x[i,1]}) = {evaluate(w1,b1,w2,b2,x[i])}")

train_boolean()