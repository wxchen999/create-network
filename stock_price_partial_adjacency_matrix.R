library(openxlsx)
data1 <- read.xlsx('/Users/chenweixun/Desktop/coding/論文/資料/20200905_20210904.xlsx',rowNames = TRUE)
data2 <- read.xlsx('/Users/chenweixun/Desktop/coding/論文/資料/20210905_20220905.xlsx',rowNames = TRUE)
data2 <- data2[,-1]
data2 <- data2[complete.cases(data1),]
data1 <- read.xlsx('/Users/chenweixun/Desktop/coding/論文/資料/20200905_20210904.xlsx',rowNames = TRUE)
data1 <- data1[complete.cases(data1),]
market_index <- read.xlsx('/Users/chenweixun/Desktop/coding/論文/資料/market_index.xlsx')



data1 <- t(data1)
data2 <- t(data2)

stock50 <- rbind(data2, data1)

stock50 <- cbind(market_index[,2], stock50)
row.names(stock50) <- market_index[,1]
colnames(stock50)[1] <- "大盤指數"
stock50 <- as.data.frame(stock50)

adjacency_matrix_partial <- matrix(rep(0,(ncol(stock50)-1)*(ncol(stock50)-1)), ncol = ncol(stock50)-1)


a = 0
b = 1
for (j in 2:ncol(stock50)) {
  for (i in 2:ncol(stock50)) {
    a = a + 1
    adjacency_matrix_partial[a,b] <- (cor(stock50[,i],stock50[,j]) - cor(stock50[,i], stock50[,1])*cor(stock50[,j], stock50[,1]))/sqrt((1-(cor(stock50[,i], stock50[,1]))^2)*(1-(cor(stock50[,j], stock50[,1]))^2))
  }
  b = b + 1
  a = 0
}

abs_adjacency_matrix_partial <- abs(adjacency_matrix_partial)
adjacency_matrix_partial_0.3 <- ifelse(abs_adjacency_matrix_partial > 0.3, 1, 0)

degree_0.3 <- array(0, 950)
for (i in 1:950) {
  degree_0.3[i] <- sum(adjacency_matrix_partial_0.3[,i])
}


adjacency_matrix_partial_0.4 <- ifelse(adjacency_matrix_partial > 0.4, 1, 0)
degree_0.4 <- array(0, 950)
for (i in 1:950) {
  degree_0.4[i] <- sum(adjacency_matrix_partial_0.4[,i])
}


adjacency_matrix_partial_0.5 <- ifelse(adjacency_matrix_partial> 0.5, 1, 0)
degree_0.5 <- array(0, 950)
for (i in 1:950) {
  degree_0.5[i] <- sum(adjacency_matrix_partial_0.5[,i])
}


adjacency_matrix_partial_0.6 <- ifelse(abs_adjacency_matrix_partial > 0.6, 1, 0)
degree_0.6 <- array(0, 950)
for (i in 1:950) {
  degree_0.6[i] <- sum(adjacency_matrix_partial_0.6[,i])
}


adjacency_matrix_partial_0.7 <- ifelse(abs_adjacency_matrix_partial > 0.7, 1, 0)
degree_0.7 <- array(0, 950)
for (i in 1:950) {
  degree_0.7[i] <- sum(adjacency_matrix_partial_0.7[,i])
}
degree_dataframe <- data.frame(degree_0.3, degree_0.4, degree_0.5, degree_0.6, degree_0.7)
write.xlsx(degree_dataframe, file = 'degree_dataframe.xlsx')
adjacency_matrix_partial_0.7 <- as.data.frame(adjacency_matrix_partial_0.7)
write.xlsx(adjacency_matrix_partial_0.7, file = 'adjacency_matrix_partial_0.7.xlsx')
