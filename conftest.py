import schist
import scanpy as sc                          
sc.settings.verbosity=2                           
adata = sc.datasets.blobs() 
sc.tl.pca(adata)                                                        
try:
    sc.pp.neighbors(adata, n_neighbors=3, key_added='foo')
    schist.inference.nested_model(adata,  neighbors_key='foo')
except TypeError:
    sc.pp.neighbors(adata, n_neighbors=3)
    schist.inference.nested_model(adata,  )

adata.write('foo.h5ad')
schist.inference.leiden(adata, neighbors_key='foo', save_model='lle')
schist.tools.calculate_affinity(adata, neighbors_key='foo', group_by='leiden')
schist.tools.cell_similarity(adata, neighbors_key='foo')
sc.pp.neighbors(adata, n_neighbors=3)
schist.inference.planted_model(adata, use_weights=False, save_model='foo')
schist.inference.nested_model(adata, save_model='test', dispatch_backend='threads')
schist.tools.calculate_affinity(adata, level=0, back_prob=True)

#test label transfer
d1 = sc.datasets.blobs()
d2 = sc.datasets.blobs()
sc.pp.neighbors(d1)
sc.tl.leiden(d1)
adata = d1.concatenate(d2)
sc.pp.neighbors(d2)

schist.tools.label_transfer(d2, d1, obs='leiden')

sc.pp.neighbors(adata)
adata.obs['leiden'] = adata.obs['leiden'].cat.add_categories('unknown').fillna('unknown')

schist.tools.label_transfer(adata, obs='leiden')

