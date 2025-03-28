# PUSH

```bash

python setup.py sdist bdist_wheel

pip install twine

# generate token on pypi

twine upload dist/* --verbose --skip-existing

# test whether uploading is success

pip install whru

```

```bash

# github
git commit -m "v1.2.3: read os env var"
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3
```