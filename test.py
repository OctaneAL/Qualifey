# Load library
from d3blocks import D3Blocks
import os

#
# Initialize
d3 = D3Blocks()
#
# Import example
df = d3.import_example('energy') # 'bigbang', 'stormofswords'
print(df)
#
# Create network using default
path1 = os.path.join(os.getcwd(), 'test', 'd3graph1.html') 
path2 = os.path.join(os.getcwd(), 'test', 'd3graph2.html') 
path3 = os.path.join(os.getcwd(), 'test', 'd3graph3.html') 
path4 = os.path.join(os.getcwd(), 'test', 'd3graph4.html') 
path5 = os.path.join(os.getcwd(), 'test', 'd3graph5.html') 
d3.d3graph(df, filepath=path1)
d3.d3graph()
#
# Change scaler
# d3.d3graph(df, scaler='minmax', filepath=path2)
#
# Change node properties
d3.D3graph.set_node_properties(color=None)
d3.D3graph.node_properties['Solar']['size']=30
d3.D3graph.node_properties['Solar']['color']='#FF0000'
d3.D3graph.node_properties['Solar']['edge_color']='#000000'
d3.D3graph.node_properties['Solar']['edge_size']=5
# d3.D3graph.show(filepath=path3)
#
# Change edge properties
d3.D3graph.set_edge_properties(directed=True, marker_end='arrow')
# d3.D3graph.show(filepath=path4)
#
# Node properties
d3.D3graph.node_properties
#
# Node properties
d3.D3graph.edge_properties
#
# After making changes, show the graph again using show()
# d3.D3graph.show(filepath=path5)