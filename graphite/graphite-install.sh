export GRAPHITE_DIR="/opt/graphite/webapp"
cp templates/tasseo.html $GRAPHITE_DIR/graphite/templates
mkdir $GRAPHITE_DIR/content/tasseo
cp -r ../public/* $GRAPHITE_DIR/content/tasseo
mkdir $GRAPHITE_DIR/graphite/tasseo
cp *.py $GRAPHITE_DIR/graphite/tasseo
sed -i "s#('graphlot/', include('graphite.graphlot.urls')),#('graphlot/', include('graphite.graphlot.urls')),\n  ('tasseo/', include('graphite.tasseo.urls')),#" $GRAPHITE_DIR/graphite/urls.py
echo "restart httpd before graphite-tasseo will work"