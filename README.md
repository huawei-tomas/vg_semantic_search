# Visual Genome Semantic Search

Steps to install:

0. Get me to send you a token. Or generate one yourself by following the steps [here](https://gist.github.com/huawei-tomas/a454db26e1dc08fa151807671be7ed6f). Caveat: You probably need get access to the project and domain I'm working under.

1. Run
```
docker run -d -p 5000:5000 \
-e GES_API_TOKEN=`cat /path/to/token` \
odellus/vg_semsearch:version0.1
```
to start the demo in a docker container stored on dockerhub.

2. Navigate to `0.0.0.0:5000` with your browser and have fun!

Please don't hesitate to contact me @thomas.wood AT huawei.com.
