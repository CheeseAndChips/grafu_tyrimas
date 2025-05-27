# Grafų tyrimas

## Duomenys

http://mif.vu.lt/~jope9155/grafu_tyrimas/out_large.gz ir http://mif.vu.lt/~jope9155/grafu_tyrimas/out_small.gz

## Paleidimas

```
git clone https://github.com/CheeseAndChips/grafu_tyrimas.git
cd grafu_tyrimas/py
python -m venv env
source env/bin/activate
pip install networkx matplotlib numpy tqdm
wget --no-check-certificate http://mif.vu.lt/~jope9155/grafu_tyrimas/out_large.gz
wget --no-check-certificate http://mif.vu.lt/~jope9155/grafu_tyrimas/out_small.gz
gunzip out_large
gunzip out_small
python show.py out_large
```
