
#' Title plots a subset of segments from a specified cluster
#'
#' @param features The dataset of features from which to select the segments
#' @param xy The entire set of x, y coordinates for each segment
#' @param nSegments The number of segments to randomly draw
#'
#' @export
#'
#' @examples
plot_cluster <- function(features, xy, nSegments){

  clusters_vector <- sort(unique(features$cluster))
  
  plots <- list()  # new empty list
  iPlot <- 0
  
  for(iCluster in clusters_vector){
    
    arena <- draw_arena(xy)
    features_cluster_selected <- features[cluster == iCluster]
    features_cluster_selected <- features_cluster_selected[sample(x = dim(features_cluster_selected)[1], size = nSegments)]
    
    for(iSegmentID in features_cluster_selected$SegmentID){
      iPlot <- iPlot + 1
      data_to_plot <- xy[SegmentID == iSegmentID]
      plots[[iPlot]] <- ggplot(data = data_to_plot, aes(x_mm, y_mm)) + 
              geom_path() + 
              xlim(60, 240) + ylim(0,200) +
              list(geom_path(data = arena, aes_string(x = "x", y = "y"))) + 
              ggtitle(paste0("Cluster: ", iCluster)) +
              theme(text = element_text(size = 6))
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