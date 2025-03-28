Template for .whl package file creation

Optional - run project inside docker container.

When project is created build whl file with command:

```
python setup.py bdist_wheel
```

If build is successful than new package will be created inside "dist" folder.

To install whl loacally use command:
```
pip install dist/my_package-0.1.0-py3-none-any.whl
```

Optionally can upload to PyPi:

```
pip install twine
```

```
python -m build
```

```
python -m twine upload dist/*
```