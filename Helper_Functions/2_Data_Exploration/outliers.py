import numpy as np
import pandas as pd


############################################
# Based on distribution
############################################
def three_sigma(s):
    mu, std = np.mean(s), np.std(s)
    lower, upper = mu-3*std, mu+3*std
    return lower, upper

def outlier_detect_arbitrary(df, col, upper_fence, lower_fence):
    '''
    identify outliers based on arbitrary boundaries passed to the function.
    '''

    para = (upper_fence, lower_fence)
    tmp = pd.concat([df[col] > upper_fence, df[col] < lower_fence], axis=1)
    outlier_index = tmp.any(axis=1)
    print('Num of outlier detected:', outlier_index.value_counts()[1])
    print('Proportion of outlier detected', outlier_index.value_counts()[1] / len(outlier_index))
    return outlier_index, para

def z_score(s):
  z_score = (s - np.mean(s)) / np.std(s)
  return z_score

def outlier_detect_mean_std(df, col, threshold=3):
    '''
    outlier detection by Mean and Standard Deviation Method.
    If a value is a certain number(called threshold) of standard deviations away
    from the mean, that data point is identified as an outlier.
    Default threshold is 3.

    This method can fail to detect outliers because the outliers increase the standard deviation.
    The more extreme the outlier, the more the standard deviation is affected.
    '''

    Upper_fence = df[col].mean() + threshold * df[col].std()
    Lower_fence = df[col].mean() - threshold * df[col].std()
    para = (Upper_fence, Lower_fence)
    tmp = pd.concat([df[col] > Upper_fence, df[col] < Lower_fence], axis=1)
    outlier_index = tmp.any(axis=1)
    print('Num of outlier detected:', outlier_index.value_counts()[1])
    print('Proportion of outlier detected', outlier_index.value_counts()[1] / len(outlier_index))
    return outlier_index, para


def boxplot(s):
    q1, q3 = s.quantile(.25), s.quantile(.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
    return lower, upper


def outlier_detect_IQR(df, col, threshold=3):
    '''
    outlier detection by Interquartile Ranges Rule, also known as Tukey's test.
    calculate the IQR ( 75th quantile - 25th quantile)
    and the 25th 75th quantile.
    Any value beyond:
        upper bound = 75th quantile + （IQR * threshold）
        lower bound = 25th quantile - （IQR * threshold）
    are regarded as outliers. Default threshold is 3.
    '''

    IQR = df[col].quantile(0.75) - df[col].quantile(0.25)
    Lower_fence = df[col].quantile(0.25) - (IQR * threshold)
    Upper_fence = df[col].quantile(0.75) + (IQR * threshold)
    para = (Upper_fence, Lower_fence)
    tmp = pd.concat([df[col] > Upper_fence, df[col] < Lower_fence], axis=1)
    outlier_index = tmp.any(axis=1)
    print('Num of outlier detected:', outlier_index.value_counts()[1])
    print('Proportion of outlier detected', outlier_index.value_counts()[1] / len(outlier_index))
    return outlier_index, para


from outliers import smirnov_grubbs as grubbs

def grubbs_test(s, alpha=0.05):
    print(grubbs.test(s, alpha=0.05))
    # print(grubbs.min_test_outliers([8, 9, 10, 1, 9], alpha=0.05))
    # print(grubbs.max_test_outliers([8, 9, 10, 1, 9], alpha=0.05))
    # print(grubbs.max_test_indices([8, 9, 10, 50, 9], alpha=0.05))
    return 

def outlier_detect_MAD(df, col, threshold=3.5):
    """
    outlier detection by Median and Median Absolute Deviation Method (MAD)
    The median of the residuals is calculated. Then, the difference is calculated between each historical value and this median.
    These differences are expressed as their absolute values, and a new median is calculated and multiplied by
    an empirically derived constant to yield the median absolute deviation (MAD).
    If a value is a certain number of MAD away from the median of the residuals,
    that value is classified as an outlier. The default threshold is 3 MAD.

    This method is generally more effective than the mean and standard deviation method for detecting outliers,
    but it can be too aggressive in classifying values that are not really extremely different.
    Also, if more than 50% of the data points have the same value, MAD is computed to be 0,
    so any value different from the residual median is classified as an outlier.
    """

    median = df[col].median()
    median_absolute_deviation = np.median([np.abs(y - median) for y in df[col]])
    modified_z_scores = pd.Series([0.6745 * (y - median) / median_absolute_deviation for y in df[col]])
    outlier_index = np.abs(modified_z_scores) > threshold
    print('Num of outlier detected:', outlier_index.value_counts()[1])
    print('Proportion of outlier detected', outlier_index.value_counts()[1] / len(outlier_index))
    return outlier_index

############################################
# Based on distance
############################################

from pyod.models.knn import KNN

def knn():
    clf = KNN( method='mean', n_neighbors=3, )
    clf.fit(X_train)
    y_train_pred = clf.labels_
    y_train_scores = clf.decision_scores_


############################################
# Based on density
############################################
from sklearn.neighbors import LocalOutlierFactor as LOF

def LOF():
    X = [[-1.1], [0.2], [100.1], [0.3]]
    clf = LOF(n_neighbors=2)
    res = clf.fit_predict(X)
    print(res)
    print(clf.negative_outlier_factor_)


from pyod.models.cof import COF

def COF(df):
    cof = COF(contamination = 0.06, 
            n_neighbors = 20,      
            )
    cof_label = cof.fit_predict(df.values)
    print(np.sum(cof_label == 1))


from sksos import SOS

def SOS(df):
    X = df.values
    detector = SOS()
    df["score"] = detector.predict(X)
    df.sort_values("score", ascending=False).head(10)

from sklearn.cluster import DBSCAN

def DBSCAN(df):
    clustering = DBSCAN(eps=3, min_samples=2).fit(df)
    clustering.labels_
    array([ 0,  0,  0,  1,  1, -1])
    # 0，,0，,0：same group
    # 1, 1：middle group
    # -1：outlier


############################################
# Based on tree
############################################

from sklearn.ensemble import IsolationForest

def isolation_forest(data):
    X,y = df.data,data.target 
    df = data.frame 
    iforest = IsolationForest(n_estimators=100, max_samples='auto',  
                            contamination=0.05, max_features=4,  
                            bootstrap=False, n_jobs=-1, random_state=1)
    #  fit_predict 1 for inliers and -1 for outliers
    df['label'] = iforest.fit_predict(X) 
    # decision_function: The higher, the more abnormal
    df['scores'] = iforest.decision_function(X)


############################################
# Based on dimension reduction
############################################
from sklearn.decomposition import PCA

def PCA (df):
    pca = PCA()
    pca.fit(centered_training_data)
    transformed_data = pca.transform(training_data)
    y = transformed_data

    lambdas = pca.singular_values_
    M = ((y*y)/lambdas)

    q = 5
    print "Explained variance by first q terms: ", sum(pca.explained_variance_ratio_[:q])
    q_values = list(pca.singular_values_ < .2)
    r = q_values.index(True)


    major_components = M[:,range(q)]
    minor_components = M[:,range(r, len(features))]
    major_components = np.sum(major_components, axis=1)
    minor_components = np.sum(minor_components, axis=1)

    components = pd.DataFrame({'major_components': major_components, 
                                'minor_components': minor_components})
    c1 = components.quantile(0.99)['major_components']
    c2 = components.quantile(0.99)['minor_components']

    def classifier(major_components, minor_components):  
        major = major_components > c1
        minor = minor_components > c2    
        return np.logical_or(major,minor)

    results = classifier(major_components=major_components, minor_components=minor_components)
    return results

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense

def autoencoder(df):

    # Split data into training and testing
    scaler = preprocessing.MinMaxScaler()
    X_train = pd.DataFrame(scaler.fit_transform(dataset_train),
                                columns=dataset_train.columns,
                                index=dataset_train.index)
    # Random shuffle training data
    X_train.sample(frac=1)
    X_test = pd.DataFrame(scaler.transform(dataset_test),
                                columns=dataset_test.columns,
                                index=dataset_test.index)

    tf.random.set_seed(10)
    act_func = 'relu'
    # Input layer:
    model=Sequential()
    # First hidden layer, connected to input vector X.
    model.add(Dense(10,activation=act_func,
                    kernel_initializer='glorot_uniform',
                    kernel_regularizer=regularizers.l2(0.0),
                    input_shape=(X_train.shape[1],)
                )
            )
    model.add(Dense(2,activation=act_func,
                    kernel_initializer='glorot_uniform'))
    model.add(Dense(10,activation=act_func,
                    kernel_initializer='glorot_uniform'))
    model.add(Dense(X_train.shape[1],
                    kernel_initializer='glorot_uniform'))
    model.compile(loss='mse',optimizer='adam')
    print(model.summary())

    # Train model for 100 epochs, batch size of 10:
    NUM_EPOCHS=100
    BATCH_SIZE=10
    history=model.fit(np.array(X_train),np.array(X_train),
                    batch_size=BATCH_SIZE,
                    epochs=NUM_EPOCHS,
                    validation_split=0.05,
                    verbose = 1)

    plt.plot(history.history['loss'],
            'b',
            label='Training loss')
    plt.plot(history.history['val_loss'],
            'r',
            label='Validation loss')
    plt.legend(loc='upper right')
    plt.xlabel('Epochs')
    plt.ylabel('Loss, [mse]')
    plt.ylim([0,.1])
    plt.show()

    # check the distribution of the loss on the training data
    X_pred = model.predict(np.array(X_train))
    X_pred = pd.DataFrame(X_pred,
                        columns=X_train.columns)
    X_pred.index = X_train.index

    scored = pd.DataFrame(index=X_train.index)
    scored['Loss_mae'] = np.mean(np.abs(X_pred-X_train), axis = 1)
    plt.figure()
    sns.distplot(scored['Loss_mae'],
                bins = 10,
                kde= True,
                color = 'blue')
    plt.xlim([0.0,.5])

    # calculate the loss on the test set
    X_pred = model.predict(np.array(X_test))
    X_pred = pd.DataFrame(X_pred,
                        columns=X_test.columns)
    X_pred.index = X_test.index
    threshod = 0.3
    scored = pd.DataFrame(index=X_test.index)
    scored['Loss_mae'] = np.mean(np.abs(X_pred-X_test), axis = 1)
    scored['Threshold'] = threshod
    scored['Anomaly'] = scored['Loss_mae'] > scored['Threshold']
    scored.head()


############################################
# Based on classification
############################################
from sklearn import svm
def svm_one_class(df):
    X = df.values
    # fit the model
    clf = svm.OneClassSVM(nu=0.1, kernel='rbf', gamma=0.1)
    clf.fit(X)
    y_pred = clf.predict(X)
    n_error_outlier = y_pred[y_pred == -1].size
    return n_error_outlier



def impute_outlier_with_arbitrary(df, outlier_index, value, col=[]):
    """
    impute outliers with arbitrary value
    """

    for i in col:
        df.loc[outlier_index, i] = value
    return df


def windsorization(df, col, para, strategy='both'):
    """
    top-coding & bottom coding (capping the maximum of a distribution at an arbitrarily set value,vice versa)
    """

    if strategy == 'both':
        df.loc[df[col] > para[0], col] = para[0]
        df.loc[df[col] < para[1], col] = para[1]
    elif strategy == 'top':
        df.loc[df[col] > para[0], col] = para[0]
    elif strategy == 'bottom':
        df.loc[df[col] < para[1], col] = para[1]
    return df


def drop_outlier(df, outlier_index):
    """
    drop the cases that are outliers
    """

    df = df[~outlier_index]
    return df


def impute_outlier_with_avg(df, col, outlier_index, strategy='mean'):
    """
    impute outlier with mean/median/most frequent values of that variable.
    """

    if strategy == 'mean':
        df.loc[outlier_index, col] = df[col].mean()
    elif strategy == 'median':
        df.loc[outlier_index, col] = df[col].median()
    elif strategy == 'mode':
        df.loc[outlier_index, col] = df[col].mode()[0]

    return df
