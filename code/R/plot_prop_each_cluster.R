library(ggplot2)
library(here)

plot_prop_each_cluster <- function(segment_length, n_clusters){

  path <- paste0("Data/length", segment_length, "/")
  df <- read.csv(paste0(path, "xy_voted_", n_clusters, "_clusters.csv"))
  df$Cluster <- as.factor(df$cluster_won + 1)
  ggplot(data = df, aes(x = Experiment, fill = Cluster)) +
    geom_bar(position = "fill") +
    ggtitle(paste0("Segment Length: ", segment_length)) +
    coord_flip() + labs(x = "Percentage of path")

}

# plot_prop_each_cluster(segment_length = 100, n_clusters = 5)
# plot_prop_each_cluster(segment_length = 150, n_clusters = 5)
# plot_prop_each_cluster(segment_length = 200, n_clusters = 4)
# plot_prop_each_cluster(segment_length = 250, n_clusters = 4)
# plot_prop_each_cluster(segment_length = 300, n_clusters = 2)
