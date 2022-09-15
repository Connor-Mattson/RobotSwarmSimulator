class ResultsConfig:
    def __init__(self,
                 tsne_perplexity=20,
                 k_clusters=10,
                 tsne_early_exaggeration=12.0,
                 archive=None,
                 world_config=None,
                 display_trends=False
                 ):
        self.perplexity = tsne_perplexity
        self.k = k_clusters
        self.early_exaggeration = tsne_early_exaggeration
        self.archive = archive
        self.world = world_config
        self.show_trends = display_trends
