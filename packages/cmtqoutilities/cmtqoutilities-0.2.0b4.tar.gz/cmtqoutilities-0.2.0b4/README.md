## Publishing of pip package:

A short reminder. In [setup.py], set the version number. The numbering scheme follows the following convention: All version numbers are of the format `X.Y.Z` with `X,Y,Z` $\in \mathbb N$. Then pip will always install the highest number. Beta versions are labelled as `X.Y.ZbS` with `S` $\in \mathbb N$. Note that beta versions are only installed by pip if either there is no non-beta-version, or if you explicitly ask for it by `pip install cmtqoutilities=1.0.0b2` for example. 


First `pip install build`, `pip install twine`, and `pip install wheel`. Now we can build the package by 
```
python setup.py sdist bdist_wheel
```
Then set the environment variables`
```
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="API_KEY" 
```
Then upload the package to your PyPi account by 
```
twine upload dist/* --non-interactive
```