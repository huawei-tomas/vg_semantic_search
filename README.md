# Visual Genome Semantic Search

Steps to install:
1. Run `python setup.py` to download a pre-processed minimal visual genome graph.

2. Run
```
docker run -d -p 5000:5000 \
-e GES_API_TOKEN=`cat /path/to/token` \
odellus/vg_semsearch:version0
```
to start the demo in a docker container stored on dockerhub.


Please don't hesitate to contact me @thomas.wood AT huawei.com.
