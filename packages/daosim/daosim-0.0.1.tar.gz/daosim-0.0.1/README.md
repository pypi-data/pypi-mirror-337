# DaOpy

The DAG adaptation of the Onion method


## Exmaple Usage

```python
p = 10    # number of variables
ad = 4    # average degree
n = 100   # number of samples

g = er_dag(p, ad=ad)
g = sf_out(g)
g = randomize_graph(g)

R, B, O = corr(g)
X = simulate(B, O, n)
X = standardize(X)

cols = [f"X{i + 1}" for i in range(p)]
df = pd.DataFrame(X, columns=cols)
