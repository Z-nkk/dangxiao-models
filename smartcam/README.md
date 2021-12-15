# smartcam

Smartly recognize actions in videos.

<img src=".github/to_label_rendered.gif" width="400" />


## Installation

```bash
pip install opencv-python sklearn
```



## API

```python
model = SinglePersonSVM(weights_path="weights/pose_svm_dangxiao_v1.pkl")
idx2act = ["", "sleep", "raise hand", "take note", "use phone"]
# pose: 25x3
label = idx2act[model.predict(pose)]
```
