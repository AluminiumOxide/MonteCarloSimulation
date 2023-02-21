# MonteCarloSimulation

This repository build a simple discrete photon statistical model based with transport theory, By using Monte Carlo simulation method with python.

Similar with other Monte Carlo Method explained  in Biomedical Photonics , our method basically consistent with the model assumptions of the textbook

Since this repository currently in beta, only build a proto example and you can get more info in our [params-card](./docs/params.md)

For the reason that python is an interpreted language, and running speed is too slow compared to compiled language. If we have time left in the following works, we will consider providing a gpu version of the program.

## Install

This project build with origin python, you only need to install numpy、scipy、matplotlib now, or you can create a conda env and run following code:

```
conda create -n MCS python=3.8
conda activate MCS
pip install -r requirements.txt
```

## Simulation

After clone and config environment you can directly run following code to begin simulation.

```
python main.py --photon_number [your photon number]
```

Dont forget prepare `<\prefix\>_H.mci`、`<\prefix\>_T.bin` and `data.txt` at input file path.

```mermaid
graph LR
a1(<\prefix\>_H.mci)--control info-->b(MCS)--control info for matlab-->c1(<\prefix\>_prop.m)
a2(data.txt)--light info-->b
a3(<\prefix\>_T.bin)--Tissue info-->b--Tissue light flux-->c2(<\prefix\>_F.bin)
b-->c3(plots)
```

enjoy

### Daily update

### 2023/02/21

更新了添加探头前后的对比效果