# GTC Object Detection Demo

## Determined AI
* [Determined AI](https://github.com/determined-ai/determined)
* [Determined AI Community Slack](https://join.slack.com/t/determined-community/shared_invite/zt-cnj7802v-KcVbaUrIzQOwmkmY7gP0Ew)

For questions or support on this notebook - please reach out to hoang@determined.ai.

## Set Up

### Install Determined
[Install Determined](https://docs.determined.ai/latest/index.html) locally. Example command:

```sh
pip install determined-cli
det deploy local cluster-up <--no-gpu if you don't have a GPU>
```

### Start Notebook

To start the demo notebook, use the following commands:

```sh
cd experiments
det notebook start --config-file support/notebook.yaml -c .
```

Once jupyter lab starts, the demo is in `GTC-Obj-Det-PyTorch.ipynb`
