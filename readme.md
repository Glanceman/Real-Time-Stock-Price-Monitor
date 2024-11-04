# Formula

## SMA

```math
    \text{SMA}=\frac{A_1+A_2+A_3+...+A_n}{n}
    \\
    \begin{split}\\
    \text{Where:}\\
    n &= \text{days}\\ 
    A &= \text{closing price}
    \end{split}
```

## EMA

```math
    \text{EMA}=(\text{Price}_{Current}\centerdot\frac{2}{n+1})+\text{EMA}_{Previous}\centerdot(1-\frac{2}{n+1}) \\

    \begin{split}\\
        \text{Where:}\\
        n &= days\\
    \end{split}
```


## MACD

```math
    \begin{alignat}{1}
    \text{MACD}(X) &= \text{EMA}_{12}(X)-\text{EMA}_{26}(X) \\
    \text{MACD}_{Signal}(X) &= \text{EMA}_9(\text{MACD}(X))
    \end{alignat}
```

## RSI
```math
    \text{RSI} = 100 - \frac{100}{1 + \frac{n_{\text{up}}}{n_{\text{down}}}}
    \\
    \begin{split}
    \text{Where:} \\
    n_{\text{up}} &= \text{avg of n-day up closes} \\
    n_{\text{down}} &= \text{avg of n-day down closes}
    \end{split}
```


## Bollinger Bands

```math
    \begin{align}
    \sigma &= \sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n}}\\
    \text{BOLU}_{\text{upper}} &= \text{
        SMA}_{\text{TP},n} + m\centerdot\sigma_{\text{TP},n}\\
    \text{BOLU}_{\text{lower}} &= \text{SMA}_{\text{TP},n} - m\centerdot\sigma_{\text{TP},n}\\
    \end{align}
```

```math
    \begin{split}\
    \text{where:}\\
    \text{TP} &= (\text{high}+\text{mid}+\text{low})/3 \\
    \text{m} &= \text{constant(2)} \\
    \text{n} &= \text{days in moving average}\\
    \end{split}
```

## On-Balance Volume(OBV)

Indicates whether this volume is flowing in or out of a given security or currency pair

```math
\begin{split}
    \text{OBV} &=\text{OBV}_\text{prev}+ 
    \begin{cases}
    & \text{volume },\text{if } \text{close} > \text{close}_\text{prev} \\
    & 0, \text{if } \text{close} = \text{close}_\text{prev} \\
    & -\text{volume }, \text{if } \text{close} < \text{close}_\text{prev}
    \end{cases}
\end{split} \\

\begin{split}\
    \text{where:}\\
    \text{OBV} &= \text{Current on-balance volume level}\\
    \text{OBV}_\text{prev} &= \text{Previous on-balance volume level}\\
    \text{volume} &= \text{Latest Trading volume amount}\\
\end{split}

```

## Annualizing votaility
```math
\begin{align}
\sigma_P &= \sqrt{\frac{\sum_{i=1}^{n}(R_i-R_p)^2}{N}} \\
\sigma_{P,T} &= \sqrt{T}\times\sigma_P \\
\end{align}\\

\begin{split}\\
e.g:& \text{daily returns}(T=252) \text{ monthly returns}(T=12)\\
& \text{standard deviation}( \sigma) = 0.001 \\
& 0.001\times\sqrt{252} \approx 1.59\%
 
\end{split}
```

## Sharpe ratio
```math
\begin{split}
    \text{Sharpe ratio} &= \frac{R_p - R_f}{\sigma_P}
\end{split}\\
\begin{split}
   &R_P:\text{avg return of portfolio}\\
    &R_P:\text{risk-free rate}(e.g:0.03)\\
    &\sigma_P:\text{the volatility of the portfolio}\\
    &\text{higher means better}
\end{split}
```



