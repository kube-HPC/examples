

## Documentation

```
hkubectl algorithm apply --f range.yml
hkubectl algorithm apply --f multiply.yml
hkubectl algorithm apply --f reduce.yml
```

For running our pipeline as raw we will use:

```
hkubectl pipeline exec raw --f numbers.yml
```

To store the pipeline we will have to create two different steps.  

For storing the pipeline:
```
1. hkubectl pipeline store --f numbers.yml
```
For executing the pipeline:
```
2. hkubectl pipeline exec stored numbers --f flowInput.yaml
```
