library(openxlsx)
library(lubridate)
library(dplyr)
library(ggplot2)


reve_data <- read.xlsx('當月營收.xlsx',detectDates = T)
row.names(reve_data) <- paste0(reve_data[,1], reve_data[,2])
reve_data <- reve_data[,-c(1,2)]
reve_data <- t(reve_data)

for (i in 1:dim(reve_data)[2]) {
  reve_data[,i] <- as.numeric(reve_data[,i])
}

adjacency_matrix <- matrix(rep(0,ncol(reve_data)*ncol(reve_data)), ncol = ncol(reve_data))


for (j in 1:ncol(reve_data)) {
  for (i in 1:j) {
    
    data_cor = cor(reve_data[,j], reve_data[,i], use = 'complete')
    adjacency_matrix[i, j] = data_cor
  }

}

adjacency_matrix[lower.tri(adjacency_matrix)] <- t(adjacency_matrix)[lower.tri(adjacency_matrix)]

# threshold network

adjacency_matrix_0.8 <- ifelse(adjacency_matrix > 0.9 |adjacency_matrix < -0.9  ,1, 0)
adjacency_matrix_0.8 <- as.data.frame(adjacency_matrix_0.8)
diag(adjacency_matrix_0.8) <- 0 
write.xlsx(adjacency_matrix_0.8, file = 'threshold_network_0.8.xlsx')



adjacency_matrix_change <- matrix(0,ncol = dim(adjacency_matrix)[1], nrow = dim(adjacency_matrix)[2])
for (i in 1:dim(adjacency_matrix)[1]) {
  adjacency_matrix_change [,i][which(adjacency_matrix[,i]>0)] <- (2.4-adjacency_matrix[,i][which(adjacency_matrix[,i]>0)])
  adjacency_matrix_change [,i][which(adjacency_matrix[,i]<0)] <-((1.92+adjacency_matrix[,i][which(adjacency_matrix[,i]<0)])^2)
}

diag(adjacency_matrix_change)<-0

diag(adjacency_matrix) <- 0
colnames(adjacency_matrix_change)<-colnames(reve_data)
rownames(adjacency_matrix_change)<-colnames(reve_data)
colnames(adjacency_matrix)<-colnames(reve_data)
rownames(adjacency_matrix)<-colnames(reve_data)

adjacency_matrix <- as.data.frame(adjacency_matrix)


write.xlsx(adjacency_matrix, file = '營收網路.xlsx')
name <- as.data.frame(colnames(reve_data))
colnames(name) <- 'names'
write.xlsx(name, file = '營收網路名稱.xlsx')

