

## Documentation

```
hkubectl algorithm apply --f range.yml
hkubectl algorithm apply --f multiply.yml
hkubectl algorithm apply --f reduce.yml
```

For running our pipeline as raw we will use:

```
hkubectl exec raw --f numbers.yml
```

To store the pipeline we will have to create two different steps.  

For storing the pipeline:
```
1. hkubectl pipeline store --f numbers.yml
```
For executing the pipeline:
```
2. hkubectl exec stored --f numbers.yaml
```

You can also run each time with defferent input:  
Just create simple yaml with flowInput.
```yaml
flowInput:
  data: 5
  mul: 2
```
Run it like this:
```
hkubectl exec stored numbers --f flowInput.yaml
```
