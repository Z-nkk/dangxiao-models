"""
action models
"""

from sklearn import svm
import pickle
from datetime import datetime


class SinglePersonSVM(object):
    """
    SVM model for single-person action classification

    Args:
        weights_path (str): /path/to/saved_weights.pkl
    """
    def __init__(self, weights_path=None):
        if weights_path is not None:
            self.model = pickle.load(open(weights_path, "rb"))
            print(f"Weights loaded from {weights_path}.")
        else:
            self.model = svm.SVC()
    

    def train(self, X, Y, save_path=None):
        """
        train SVM model

        Args:
            X (list): Nx75 poses
            Y (list): Nx1 action labels
            save_path (str): /path/to/to_be_saved_weights.pkl
        """
        self.model.fit(X, Y)
        if save_path is not None:
            pickle.dump(self.model, open(save_path, "wb"))
            print(f"Weights saved to {save_path}.")


    def eval(self, X, Y, report_path=None):
        """
        train SVM model

        Args:
            X (list): Nx75 poses
            Y (list): Nx1 action labels
            report_path (str): /path/to/to_be_saved_report.txt
        """
        acc = self.model.score(X, Y)
        print(f"Test with {len(X)} samples. Accuracy={acc}.")
        if report_path is not None:
            t = datetime.now().strftime('%Y%m%d%H%M%S')
            with open(report_path, "a") as fout:
                fout.write(f"{t},{len(X)} samples,{acc} accuracy\n")

    def predict(self, x):
        """
        predict on a pose result

        Args:
            x (list): 25x3 pose (or empty list)

        Returns:
            l (int): action label index
        """
        if len(x)>0:
            #inp = []
            #for tmp in x:
            #    inp += tmp
            l = self.model.predict([x.tolist()])[0]
        else:
            l = None
        return l
