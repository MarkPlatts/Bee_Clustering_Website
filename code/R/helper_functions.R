
#' Title plots a subset of segments from a specified cluster
#'
#' @param features The dataset of features from which to select the segments
#' @param xy The entire set of x, y coordinates for each segment
#' @param nSegments The number of segments to randomly draw
#'
#' @export
#'
#' @examples
plot_cluster <- function(features, xy, kmean_mod, nSegments){

  clusters_vector <- sort(unique(features$cluster))

  plots <- list()  # new empty list
  iPlot <- 0

  for(iCluster in clusters_vector){

    arena <- draw_arena(xy)

    segmentIDs <- findNNearestNeighbours(features = features,
                                         n_nearest = nSegments,
                                         kmean_mod = kmean_mod,
                                         iCluster = iCluster)

    for(iSegmentID in as.vector(as.matrix(segmentIDs))){
      # print(iSegmentID)
      iPlot <- iPlot + 1
      data_to_plot <- xy[SegmentID == iSegmentID]
      plots[[iPlot]] <- ggplot(data = data_to_plot, aes(x_mm, y_mm)) +
              geom_path() +
              xlim(60, 240) + ylim(0,200) +
              list(geom_path(data = arena, aes_string(x = "x", y = "y"))) +
              ggtitle(paste0("Cluster: ", iCluster)) +
              theme_bw(base_size = 6)
      }
  }

  multiplot(plotlist = plots, cols = length(clusters_vector))

}

# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  require(grid)

  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)

  numPlots = length(plots)

  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }

  if (numPlots==1) {
    print(plots[[1]])

  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))

      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

draw_arena <- function(xy){
  radius <- (max(xy$x_mm) - min(xy$x_mm)) / 2
  center_x <- (max(xy$x_mm) + min(xy$x_mm)) / 2
  center_y <- (max(xy$y_mm) + min(xy$y_mm)) / 2
  t <- seq(0, 2*pi, length.out = 360)
  x <- radius * cos(t) + center_x
  y <- radius * sin(t) + center_y
  return(data.frame(x = x, y = y))
}

# """Finds the segmentID's for n nearest neighbours of a given kmeans center
#
# Parameters
# df : pandas.dataframe
# A data frame where each row contains the features for a given segment
# n_nearest : integer
# The number of nearest neighbours to find.
# kmean : dict
# A dictionary containing the feature names and values for a given kmeans
# centre.
#
# Returns
# pandas.core.series.Series
# A series contain the segmentID's for the n closest neighbours to the
#         given kmeans centre.
#
#     """
findNNearestNeighbours = function(features, n_nearest, kmean_mod, iCluster){

  n_obs <- dim(features)[1]
  vec_of_sse <- vector(length = n_obs)
  n_features <- dim(features)[2] - 5

  df_temp <- features[, 5:(n_features+4), with =F]
  df_temp <- as.data.table(scale(df_temp))
  for(iFeature in 1:n_features){
    df_temp[, iFeature] <- df_temp[, iFeature, with = F] - kmean_mod$centers[iCluster,iFeature]
  }
  df_temp <- df_temp**2

  vec_of_sse <- rowSums(df_temp)

  df_sort <- features
  df_sort$sse <- vec_of_sse
  df_sort <- dplyr::arrange(df_sort, sse)

  df_top_n_value = df_sort[1:n_nearest,]

  segmentIDs <- df_top_n_value['SegmentID']

  return(segmentIDs)
}
