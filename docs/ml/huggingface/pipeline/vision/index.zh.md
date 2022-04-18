在本教程中，我们将探讨如何使用 Hugging Face Pipeline，以及如何使用 [Pinferencia](https://github.com/underneathall/pinferencia) 作为 REST API 部署它。

---

## 先决条件

请访问 [依赖项](/ml/huggingface/dependencies/)

## 下载模型并预测

模型将自动下载。

```python linenums="1"
from transformers import pipeline
vision_classifier = pipeline(task="image-classification")

vision_classifier(
    images="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"
)
```

![hfimg](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg)

结果:

```python
[{'label': 'lynx, catamount', 'score': 0.4403027892112732},
 {'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor',
  'score': 0.03433405980467796},
 {'label': 'snow leopard, ounce, Panthera uncia',
  'score': 0.032148055732250214},
 {'label': 'Egyptian cat', 'score': 0.02353910356760025},
 {'label': 'tiger cat', 'score': 0.023034192621707916}]
```

让我们尝试另一个图像，让我们尝试在一批中预测两个图像：

```python linenums="1"
image = "https://cdn.pixabay.com/photo/2018/08/12/16/59/parrot-3601194_1280.jpg"
vision_classifier(
    images=[image, image]
)
```
![parrot](https://cdn.pixabay.com/photo/2018/08/12/16/59/parrot-3601194_1280.jpg)

结果:

```python
[[{'score': 0.9489120244979858, 'label': 'macaw'},
  {'score': 0.014800671488046646, 'label': 'broom'},
  {'score': 0.009150494821369648, 'label': 'swab, swob, mop'},
  {'score': 0.0018255198374390602, 'label': "plunger, plumber's helper"},
  {'score': 0.0017631321679800749,
   'label': 'African grey, African gray, Psittacus erithacus'}],
 [{'score': 0.9489120244979858, 'label': 'macaw'},
  {'score': 0.014800671488046646, 'label': 'broom'},
  {'score': 0.009150494821369648, 'label': 'swab, swob, mop'},
  {'score': 0.0018255198374390602, 'label': "plunger, plumber's helper"},
  {'score': 0.0017631321679800749,
   'label': 'African grey, African gray, Psittacus erithacus'}]]
```

出乎意料的容易！ 现在让我们试试：

## 部署模型

没有部署，机器学习教程怎么可能完整？

首先，让我们安装 [Pinferencia](https://github.com/underneathall/pinferencia)。

```bash
pip install "pinferencia[uvicorn]"
```
Now let's create an app.py file with the codes:

```python title="app.py" linenums="1" hl_lines="2 10-11"
from transformers import pipeline
from pinferencia import Server


vision_classifier = pipeline(task="image-classification")

def predict(data):
    return vision_classifier(images=data)

service = Server()
service.register(model_name="vision", model=predict)
```

小菜一碟，对吧？

## 预测

=== "Curl"

    ```bash
    curl --location --request POST 'http://127.0.0.1:8000/v1/models/vision/predict' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "data": "https://cdn.pixabay.com/photo/2018/08/12/16/59/parrot-3601194_1280.jpg"
    }'
    ```

    Result:
    ```
    Prediction: [
        {'score': 0.433499813079834, 'label': 'lynx, catamount'},
        {'score': 0.03479616343975067, 'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor'},
        {'score': 0.032401904463768005, 'label': 'snow leopard, ounce, Panthera uncia'},
        {'score': 0.023944756016135216, 'label': 'Egyptian cat'},
        {'score': 0.022889181971549988, 'label': 'tiger cat'}
    ]
    ```

=== "Python requests"

    ```python title="test.py" linenums="1"
    import requests

    response = requests.post(
        url="http://localhost:8000/v1/models/vision/predict",
        json={
            "data": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"  # noqa
        },
    )
    print("Prediction:", response.json()["data"])
    ```

    Run `python test.py` and result:

    ```
    Prediction: [
        {'score': 0.433499813079834, 'label': 'lynx, catamount'},
        {'score': 0.03479616343975067, 'label': 'cougar, puma, catamount, mountain lion, painter, panther, Felis concolor'},
        {'score': 0.032401904463768005, 'label': 'snow leopard, ounce, Panthera uncia'},
        {'score': 0.023944756016135216, 'label': 'Egyptian cat'},
        {'score': 0.022889181971549988, 'label': 'tiger cat'}
    ]
    ```

更酷的是，访问 http://127.0.0.1:8000，您将拥有一个交互式UI。

您可以在那里发送预测请求！