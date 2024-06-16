# Prediction Demo

In the following, we predict the benchmark instance labels provided by GBD's meta.db from instance feature records provided by GBD's base.db.



```python
from gbd_core.api import GBD
import pandas as pd

def get_available_features():
    with GBD([ 'data/base.db' ]) as gbd:
        return gbd.get_features('base')

def get_prediction_dataset(features, target):
    with GBD([ 'data/base.db', 'data/meta.db' ]) as gbd:
        df = gbd.query('base_features_runtime != memout', resolve=features+[target])
        df[features] = df[features].apply(pd.to_numeric)
        return df
    
print(get_available_features())
```

    ['base_features_runtime', 'clauses', 'variables', 'cls1', 'cls2', 'cls3', 'cls4', 'cls5', 'cls6', 'cls7', 'cls8', 'cls9', 'cls10p', 'horn', 'invhorn', 'positive', 'negative', 'hornvars_mean', 'hornvars_variance', 'hornvars_min', 'hornvars_max', 'hornvars_entropy', 'invhornvars_mean', 'invhornvars_variance', 'invhornvars_min', 'invhornvars_max', 'invhornvars_entropy', 'balancecls_mean', 'balancecls_variance', 'balancecls_min', 'balancecls_max', 'balancecls_entropy', 'balancevars_mean', 'balancevars_variance', 'balancevars_min', 'balancevars_max', 'balancevars_entropy', 'vcg_vdegree_mean', 'vcg_vdegree_variance', 'vcg_vdegree_min', 'vcg_vdegree_max', 'vcg_vdegree_entropy', 'vcg_cdegree_mean', 'vcg_cdegree_variance', 'vcg_cdegree_min', 'vcg_cdegree_max', 'vcg_cdegree_entropy', 'vg_degree_mean', 'vg_degree_variance', 'vg_degree_min', 'vg_degree_max', 'vg_degree_entropy', 'cg_degree_mean', 'cg_degree_variance', 'cg_degree_min', 'cg_degree_max', 'cg_degree_entropy']


### Category Prediction

Train instance category predictor once and report its accuracy.


```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

feat = get_available_features()
data = get_prediction_dataset(feat, 'family')

X_train, X_test, y_train, y_test = train_test_split(data[feat], data['family'], test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

```

    Accuracy: 0.969248670212766


### Feature Importance

Extract feature importance from category predictor.


```python
def print_feature_importances(model, feat, granularity=50):
    feature_importances = model.feature_importances_
    maximum = int(max(feature_importances) * granularity)+1
    byimp = [ [] for _ in range(maximum) ]
    for i, imp in enumerate(feature_importances):
        byimp[int(imp*granularity)].append((feat[i]))
    fimp = [ ((i/granularity, (i+1)/granularity), byimp[i]) for i in range(maximum-1, -1, -1) if len(byimp[i]) > 0 ]
    print("Feature importances:", fimp)

print_feature_importances(model, feat)
```

    Feature importances: [((0.04, 0.06), ['hornvars_variance', 'hornvars_entropy', 'balancecls_mean', 'balancecls_variance', 'balancevars_mean', 'vcg_cdegree_mean']), ((0.02, 0.04), ['hornvars_mean', 'hornvars_max', 'invhornvars_mean', 'balancevars_variance', 'balancevars_entropy', 'vcg_vdegree_mean', 'vcg_cdegree_variance', 'vcg_cdegree_entropy', 'vg_degree_mean', 'vg_degree_entropy', 'cg_degree_min']), ((0.0, 0.02), ['base_features_runtime', 'clauses', 'variables', 'cls1', 'cls2', 'cls3', 'cls4', 'cls5', 'cls6', 'cls7', 'cls8', 'cls9', 'cls10p', 'horn', 'invhorn', 'positive', 'negative', 'hornvars_min', 'invhornvars_variance', 'invhornvars_min', 'invhornvars_max', 'invhornvars_entropy', 'balancecls_min', 'balancecls_max', 'balancecls_entropy', 'balancevars_min', 'balancevars_max', 'vcg_vdegree_variance', 'vcg_vdegree_min', 'vcg_vdegree_max', 'vcg_vdegree_entropy', 'vcg_cdegree_min', 'vcg_cdegree_max', 'vg_degree_variance', 'vg_degree_min', 'vg_degree_max', 'cg_degree_mean', 'cg_degree_variance', 'cg_degree_max', 'cg_degree_entropy'])]


### Subsets

Train the category prediction model on subsets of the base features and evaluate feature importance for them.


```python
subsets = {
    'Clause Counts': ['clauses', 'variables', 'cls1', 'cls2', 'cls3', 'cls4', 'cls5', 'cls6', 'cls7',  'cls8', 'cls9', 'cls10p', 'horn', 'invhorn', 'positive', 'negative'],
    'Horn Variables': ['hornvars_mean', 'hornvars_variance', 'hornvars_min', 'hornvars_max', 'hornvars_entropy', 'invhornvars_mean', 'invhornvars_variance', 'invhornvars_min', 'invhornvars_max', 'invhornvars_entropy'],
    'Polarity Balance': ['balancecls_mean', 'balancecls_variance', 'balancecls_min', 'balancecls_max', 'balancecls_entropy', 'balancevars_mean', 'balancevars_variance', 'balancevars_min', 'balancevars_max', 'balancevars_entropy'],
    'Bipartite Graph': ['vcg_vdegree_mean', 'vcg_vdegree_variance', 'vcg_vdegree_min', 'vcg_vdegree_max', 'vcg_vdegree_entropy', 'vcg_cdegree_mean', 'vcg_cdegree_variance', 'vcg_cdegree_min', 'vcg_cdegree_max', 'vcg_cdegree_entropy'],
    'Variable Graph': ['vg_degree_mean', 'vg_degree_variance', 'vg_degree_min', 'vg_degree_max', 'vg_degree_entropy'],
    'Clause Graph': ['cg_degree_mean', 'cg_degree_variance', 'cg_degree_min', 'cg_degree_max', 'cg_degree_entropy']
}

for name, sub in subsets.items():
    submodel = RandomForestClassifier()
    submodel.fit(X_train[sub], y_train)
    y_pred_sub = submodel.predict(X_test[sub])
    accuracy_feature = accuracy_score(y_test, y_pred_sub)
    print(f"Accuracy with {name} features:", accuracy_feature)
    print_feature_importances(submodel, sub)
```

    Accuracy with Clause Counts features: 0.9498005319148937
    Feature importances: [((0.08, 0.1), ['cls2', 'cls3', 'cls10p', 'negative']), ((0.06, 0.08), ['variables', 'cls1', 'horn', 'positive']), ((0.04, 0.06), ['clauses', 'cls4', 'cls8', 'cls9', 'invhorn']), ((0.02, 0.04), ['cls5', 'cls6', 'cls7'])]
    Accuracy with Horn Variables features: 0.937998670212766
    Feature importances: [((0.18, 0.2), ['hornvars_mean']), ((0.16, 0.18), ['hornvars_variance']), ((0.14, 0.16), ['hornvars_entropy']), ((0.12, 0.14), ['invhornvars_mean']), ((0.1, 0.12), ['hornvars_max']), ((0.08, 0.1), ['invhornvars_variance', 'invhornvars_entropy']), ((0.06, 0.08), ['invhornvars_max']), ((0.0, 0.02), ['hornvars_min', 'invhornvars_min'])]
    Accuracy with Polarity Balance features: 0.9398271276595744
    Feature importances: [((0.18, 0.2), ['balancevars_mean']), ((0.14, 0.16), ['balancecls_mean']), ((0.12, 0.14), ['balancecls_variance', 'balancevars_variance']), ((0.1, 0.12), ['balancevars_entropy']), ((0.08, 0.1), ['balancecls_entropy', 'balancevars_min']), ((0.06, 0.08), ['balancecls_max']), ((0.04, 0.06), ['balancevars_max']), ((0.0, 0.02), ['balancecls_min'])]
    Accuracy with Bipartite Graph features: 0.9571143617021277
    Feature importances: [((0.2, 0.22), ['vcg_cdegree_mean']), ((0.14, 0.16), ['vcg_cdegree_variance']), ((0.12, 0.14), ['vcg_vdegree_mean']), ((0.1, 0.12), ['vcg_vdegree_entropy', 'vcg_cdegree_max', 'vcg_cdegree_entropy']), ((0.06, 0.08), ['vcg_vdegree_variance', 'vcg_vdegree_max']), ((0.04, 0.06), ['vcg_cdegree_min']), ((0.0, 0.02), ['vcg_vdegree_min'])]
    Accuracy with Variable Graph features: 0.9336768617021277
    Feature importances: [((0.32, 0.34), ['vg_degree_mean']), ((0.24, 0.26), ['vg_degree_entropy']), ((0.2, 0.22), ['vg_degree_variance', 'vg_degree_max']), ((0.0, 0.02), ['vg_degree_min'])]
    Accuracy with Clause Graph features: 0.9378324468085106
    Feature importances: [((0.22, 0.24), ['cg_degree_max']), ((0.18, 0.2), ['cg_degree_mean', 'cg_degree_variance', 'cg_degree_min', 'cg_degree_entropy'])]

