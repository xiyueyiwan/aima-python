from learning import parse_csv, weighted_mode, weighted_replicate, DataSet, \
                     PluralityLearner, NaiveBayesLearner, NearestNeighborLearner, \
                     NeuralNetLearner, PerceptronLearner, DecisionTreeLearner, \
                     euclidean_distance, grade_learner
from utils import DataFile



def test_euclidean():
    distance = euclidean_distance([1, 2], [3, 4])
    assert round(distance, 2) == 2.83

    distance = euclidean_distance([1, 2, 3], [4, 5, 6])
    assert round(distance, 2) == 5.2

    distance = euclidean_distance([0, 0, 0], [0, 0, 0])
    assert distance == 0


def test_exclude():
    iris = DataSet(name='iris', exclude=[3])
    assert iris.inputs == [0, 1, 2]


def test_parse_csv():
    Iris = DataFile('iris.csv').read()
    assert parse_csv(Iris)[0] == [5.1, 3.5, 1.4, 0.2,'setosa']


def test_weighted_mode():
    assert weighted_mode('abbaa', [1, 2, 3, 1, 2]) == 'b'


def test_weighted_replicate():
    assert weighted_replicate('ABC', [1, 2, 1], 4) == ['A', 'B', 'B', 'C']


def test_plurality_learner():
    zoo = DataSet(name="zoo")

    pL = PluralityLearner(zoo)
    assert pL([1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 1]) == "mammal"


def test_naive_bayes():
    iris = DataSet(name="iris")

    # Discrete
    nBD = NaiveBayesLearner(iris)
    assert nBD([5, 3, 1, 0.1]) == "setosa"


def test_k_nearest_neighbors():
    iris = DataSet(name="iris")

    kNN = NearestNeighborLearner(iris,k=3)
    assert kNN([5, 3, 1, 0.1]) == "setosa"
    assert kNN([6, 5, 3, 1.5]) == "versicolor"
    assert kNN([7.5, 4, 6, 2]) == "virginica"


def test_decision_tree_learner():
    iris = DataSet(name="iris")

    dTL = DecisionTreeLearner(iris)
    assert dTL([5, 3, 1, 0.1]) == "setosa"
    assert dTL([6, 5, 3, 1.5]) == "versicolor"
    assert dTL([7.5, 4, 6, 2]) == "virginica"


def test_neural_network_learner():
    iris = DataSet(name="iris")

    classes = ["setosa","versicolor","virginica"]
    iris.classes_to_numbers(classes)

    nNL = NeuralNetLearner(iris, [5], 0.15, 75)
    tests = [([5, 3, 1, 0.1], 0),
             ([6, 3, 3, 1.5], 1),
             ([7.5, 4, 6, 2], 2)]

    assert grade_learner(nNL, tests) >= 2


def test_perceptron():
    iris = DataSet(name="iris")
    iris.classes_to_numbers()

    classes_number = len(iris.values[iris.target])

    perceptron = PerceptronLearner(iris)
    tests = [([5, 3, 1, 0.1], 0),
             ([6, 3, 4, 1.1], 1),
             ([7.5, 4, 6, 2], 2)]

    assert grade_learner(perceptron, tests) >= 2
