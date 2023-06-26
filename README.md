## 流量分类代码

### 上下采样
`up_down_sampling.py`用于对数据进行上下采样，所有采样方法已经写好，略微改动样本比例，再选择使用的采样方法，调用`fit_resample`函数即可

### 在线和离线二阶段分类
`OL_Classifier.py`读取csv文件，进行二阶段分类。

## OL_Classifier_ratio
用来进行二阶段分类（序列识别并统计特征识别）的代码

**modelpath**是训练好的模型存放的地方，存放模型格式为`1_XX.m`和`2_XX.m`，分别用于一阶段序列识别和二阶段统计特征识别。使用的特征为`pl_iat`和`select_features`。

**tor**和**nor**是存放tor和normal的测试集

### origin方法
原始流量识别方法。`Classifier.py`，修改读取数据部分即可运行。模型保存在models文件夹下。

### baseline方法
O2OS初始识别性能。

- 模型生成：`OL_Classifier_models.py`，修改`modelpath`，存储模型路径，修改**borderline=0**,**adaboostout = 0**。

- 模型测试：`OL_Classifier_ratio.py`，修改**ensembleout = 0**，选择测试接中的nor路径与model路径，修改lowbound与uppbound。

### borderline优化
使用borderline方法生成样本，修改测试集分布，让分类器有所偏好。

- 模型生成：`OL_Classifier_models.py`，修改`modelpath`，存储模型路径，修改**borderline=1**,**adaboostout = 0**。可以在49行和51行修改要生成的样本数量，增加哪个类，就会让分类器偏向哪个类。

- 模型测试：`OL_Classifier_ratio.py`，修改**ensembleout = 0**，选择测试接中的nor路径与model路径，修改lowbound与uppbound。

### adaboost优化
借鉴adaboost思想，让二阶段的离线分类使用的训练样本不是normal样本，而是tor样本和一阶段在线分类的错误分类样本。

- 模型生成：

1. `OL_Classifier_models.py`，**这里要保证norpath的normal训练流量很多。**这里会选择适当数量的normal样本用于训练，并把其他错误识别的结果保存下来。修改`modelpath`，存储模型路径，修改**borderline=0**,**adaboostout = 1**。修改adaboostpath用于存储错误识别的结果。

2. 运行`OL_Classifier_models_adaboost.py`,这里要修改五个*norpath*，和modelpath，modelpath应该等于刚刚的路径。运行完后到model路径下面，新生成的模型是以2_*.m的格式命名的*号是数字。顺序是c45,gbdt,knn,rf30.

- 模型测试：`OL_Classifier_ratio.py`，修改**ensembleout = 0**，选择测试接中的nor路径与model路径，修改lowbound与uppbound。

### ensembel优化
借鉴集成学习思想，对不同分类器给出的结果进行集成。

- 初步分类结果：`OL_Classifier_ratio.py`，先运行一个现成的模型，可以是上面baseline,borderline,adaboost的任何一种，但要修改**ensembleout = 1**，会把本来的label，和十六种分类结果保存到ensemble.csv。

- 分类结果集成：`ensemble.py`，修改file为ensemble.csv路径。有三种集成策略：naive,slightly,strong.分别代表不同的拒绝粒度。修改83-85页，93-95页。

1. naive：多数投票，如果2：2或者四个分类结果都不同，分类为normal。
2. slightly：弱否定，只要normal分类，就分类为normal，其他的按照多数投票原则。
3. strong：强否定，四个投票结果，只要票数不超过3票，就分类为normal。

### entirety优化
在O2OS系统中，集合borderline方法、adaboost方法、ensemble方法。使用borderline方法修改训练样本分布，让分类器偏向normal。使用adaboost方法让二阶段离线识别专注于识别一阶段错误分类的结果。使用ensemble方法集成分类结果。

- 模型生成：
1. `OL_Classifier_models.py`，修改`modelpath`，路径随意，修改**borderline=1**,**adaboostout = 1**。可以在49行和51行修改要生成的样本数量，增加哪个类，就会让分类器偏向哪个类。**这里同样要保证norpath的normal训练流量很多。**

2. 运行`OL_Classifier_models_adaboost.py`,这里要修改五个*norpath*，和modelpath，modelpath应该等于刚刚的路径。运行完后到model路径下面，新生成的模型是以2_*.m的格式命名的*号是数字。顺序是c45,gbdt,knn,rf30.

- 初步分类结果：`OL_Classifier_ratio.py`，修改相应路径，**borderline=0**,**adaboostout = 1**，输出分类标签结果。

- 分类结果集成：`ensemble.py`，修改file为ensemble.csv路径。有三种集成策略：naive,slightly,strong.分别代表不同的拒绝粒度。修改83-85页，93-95页。

1. naive：多数投票，如果2：2或者四个分类结果都不同，分类为normal。
2. slightly：弱否定，只要normal分类，就分类为normal，其他的按照多数投票原则。
3. strong：强否定，四个投票结果，只要票数不超过3票，就分类为normal。