# -*- coding: utf-8 -*-
"""AnamolyDetection_Techs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uWQoxDbeS6Aaruna-KN5bw0yVB5bcmg4
"""

from google.colab import drive
drive.mount('/content/gdrive')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_table('/content/gdrive/My Drive/NetworkData_Anamoly/Train.txt',sep=",",header=None)

columns=["duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
"wrong_fragment","urgent","hot","num_failed_logins","logged_in",
"num_compromised","root_shell","su_attempted","num_root","num_file_creations",
"num_shells","num_access_files","num_outbound_cmds","is_host_login",
"is_guest_login","count","srv_count","serror_rate", "srv_serror_rate",
"rerror_rate","srv_rerror_rate","same_srv_rate", "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
"dst_host_diff_srv_rate","dst_host_same_src_port_rate",
"dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
"dst_host_rerror_rate","dst_host_srv_rerror_rate","attack", "last_flag"]

data.columns=columns

cat_data=data.select_dtypes('object').copy()
cat_columns=cat_data.columns

cat_columns=cat_data.columns

cat_data.attack.unique()



num_data=data[data.columns[~data.columns.isin(cat_columns)]]

cat_data

from sklearn.preprocessing import LabelEncoder
hot_encoder=LabelEncoder()

cat_data['protocol_type']=hot_encoder.fit_transform(cat_data.protocol_type)
cat_data['flag']=hot_encoder.fit_transform(cat_data.flag)
#cat_data['attack']=hot_encoder.fit_transform(cat_data.attack)
cat_data['service']=hot_encoder.fit_transform(cat_data.service)

cat_data['attack']=cat_data.attack.replace( ['neptune', 'warezclient', 'ipsweep', 'portsweep',
       'teardrop', 'nmap', 'satan', 'smurf', 'pod', 'back',
       'guess_passwd', 'ftp_write', 'multihop', 'rootkit',
       'buffer_overflow', 'imap', 'warezmaster', 'phf', 'land',
       'loadmodule', 'spy', 'perl'],1)

cat_data.replace('normal',0,inplace=True)

cat_data.attack.value_counts()



train_1=pd.concat([cat_data,num_data],axis=1)

train=train_1.drop('attack',axis=1)

train.shape
train_col=train.columns

#Feature Scaling

from sklearn.preprocessing import MinMaxScaler
sc=MinMaxScaler()
train=sc.fit_transform(train)

train=pd.DataFrame(train,columns=train_col)

#Implementation of DBSCAN
from sklearn.cluster import DBSCAN
outlier_detection=DBSCAN(eps=0.5,metric='euclidean',min_samples=5,n_jobs=-1)

clusters=outlier_detection.fit_predict(train)

clusters

train.columns

plt.(t)





from matplotlib import cm
cmap = cm.get_cmap('Set1')
train.plot.scatter(x='num_failed_logins',y='num_access_files', c=clusters, cmap=cmap,
 colorbar = False)

from matplotlib import cm
cmap = cm.get_cmap('Accent')
train.plot.scatter(
  x = "num_failed_logins",
  y = "num_access_files",
  c = clusters,
  cmap = cmap,
  colorbar = False
)

"""**IsolationForests**"""

cols=train.columns

X_train, y_train = train[cols][:300000], data["attack"][:300000].values
X_valid, y_valid = train[cols][300000:500000], data["attack"][300000:500000].values
X_test, y_test = train[cols][500000:], data["attack"][500000:].values

from sklearn.ensemble  import IsolationForest
rs=np.random.RandomState(0)
clf=IsolationForest(max_samples=100,random_state=rs,contamination=0.2)
clf.fit(X_train)

if_scores=clf.decision_function(train)

plt.figure(figsize=(12, 8))
plt.hist(if_scores, bins=50);





plt.figure(figsize=(12,8))
plt.hist(if_scores);
plt.title("Histogram of Avg Anomaly Scores: Lower => More Anomalous")

from sklearn.metrics import roc_auc_score

print("AUC: {:.1%}".format(roc_auc_score((-0.2 < scores), y_valid == list(encs["label"].classes_).index("normal."))))

scores_test = clf.decision_function(X_test)







"""**Elliptic Envelope**
The Elliptic Envelope method fits a multivariate gaussian distribution to the dataset. Use the contamination hyperparameter to specify the percentage of observations the algorithm will assign as outliers.
"""

from sklearn.covariance import EllipticEnvelope
clf=EllipticEnvelope(contamination=.1,random_state=0)

clf.fit(train)

ee_scores=pd.Series(clf.decision_function(train))

ee_predict=clf.predict(train)

ee_predict.shape