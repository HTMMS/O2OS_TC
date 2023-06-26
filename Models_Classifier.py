
def c45():
    ### Decision Tree Classifier
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier(criterion='entropy')
    return clf


def cart():
    ### Decision Tree Classifier
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier(criterion='gini')
    return clf


def knn():
    ### KNeighbor
    from sklearn.neighbors import KNeighborsClassifier
    clf = KNeighborsClassifier()
    return clf


def lrc():
    ### Logistic Regression Classifier    ###penalty='l2'
    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression(penalty='l2')
    return clf


def rf10(n_estimators=10):
    ### Random Forest Classifier
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=n_estimators)
    
    return clf

def rf20(n_estimators=20):
    ### Random Forest Classifier
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=n_estimators)
    
    return clf

def rf30(n_estimators=30):
    ### Random Forest Classifier
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=n_estimators)
    
    return clf


def gbdt(n_estimators=200):
    ### GBDT(Gradient Boosting Decision Tree) Classifier
    ### n_estimators = 200
    from sklearn.ensemble import GradientBoostingClassifier
    clf = GradientBoostingClassifier(n_estimators=n_estimators)
    
    return clf


def AdaBoost():
    ###AdaBoost Classifier
    from sklearn.ensemble import AdaBoostClassifier
    clf = AdaBoostClassifier()
    
    return clf


def gnb():
    ### GaussianNB
    from sklearn.naive_bayes import GaussianNB
    clf = GaussianNB()
    
    return clf


def lda():
    ### Linear Discriminant Analysis
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    clf = LinearDiscriminantAnalysis()
    
    return clf


def qda():
    ### Quadratic Discriminant Analysis
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    clf = QuadraticDiscriminantAnalysis()
    
    return clf


def svm(kernel='poly', probability=True):
    ### SVM Classifier
    from sklearn.svm import SVC
    # clf = SVC(kernel='rbf,linear,poly', probability=True)
    clf = SVC(kernel=kernel, probability=probability)
    return clf
