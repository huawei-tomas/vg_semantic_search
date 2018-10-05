# Visual Genome Semantic Search

Steps to install:
1. Run `python setup.py` to download a pre-processed minimal visual genome graph and set up a TinkerPop server.

2. In a separate terminal run `cd apache-tinkerpop-gremlin-server-3.3.3 && ./bin/gremlin-server.sh conf/gremlin-server-vg-scene-graph.yaml` to get the server up and running.

3. Run `docker run -d -p 5000:5000 odellus/vg_semsearch:version0` to start the demo in a docker container stored on dockerhub.

4. Replace the tinkerpop server API with GES API. The scripts to generate the edge and vertices CSV files as well as the schema for GES are located in the current directory as vg2csv.py and vg_scene_graph_schema.xml. There have been changes made to the schema and pre-processing script which are different from the way app/search.py assumes the graph is structured.

Please don't hesitate to contact me @thomas.wood AT huawei.com.
