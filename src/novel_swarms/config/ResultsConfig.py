class ResultsConfig:
    def __init__(self,
                 tsne_perplexity=20,
                 k_clusters=10,
                 tsne_early_exaggeration=12.0,
                 archive=None,
                 world_config=None,
                 display_trends=False,
                 clustering_type="k-medoids",
                 eps=None,
             ):
        # Eps is a parameter that is exclusively for r-disk instantiations of clustering (DBSCAN)
        if clustering_type not in ["dbscan"] and eps is not None:
            print("Warning: EPS parameter defined on results config but the clustering type does not require an eps value")

        self.perplexity = tsne_perplexity
        self.k = k_clusters
        self.early_exaggeration = tsne_early_exaggeration
        self.archive = archive
        self.world = world_config
        self.show_trends = display_trends
        self.clustering_type = clustering_type
        self.eps = eps
