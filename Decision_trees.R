install.packages("FSelector")
install.packages("caret")

library("dplyr")
library("FSelector")
library("rpart")
library("caret")
library("rpart.plot")

set.seed(123)



## Type of Surface

df = data.frame(read.csv("Surface_Results.csv"))

#Remove 6th column which is not informative (all values are "1")
df = df[,-6]


#First subset: including only "Entropy" and "Result" columns 
df1 = df[,5:6]
df1 = mutate(df1, Result=as.factor(Result), Entropy=as.numeric(Entropy))


best.tree = NA
best.prediction = NA
check = 0
test.results = c()

for (i in 1:1000) {
  samp = sample(as.numeric(rownames(df1)), round(length(df1[,1]) * 0.7))
  
  train = df1[samp,]
  test = df1[-samp,]
  
  tree = rpart(Result~., data = train)
  tree.predicted = predict(tree, test, type="class")
  precision = sum(tree.predicted == test$Result)/length(test$Result)
  if (as.numeric(precision) > check) {
    best.tree = tree
    best.prediction = tree.predicted
    check = precision
    test.results = test$Result
  }
}


check

confusionMatrix(best.prediction, test.results)

prp(best.tree)




#Second subset: including all initial columns (except for the one removed at the start)
df$Result = as.factor(df$Result)

for (i in 1:5) {
  df[,i] = as.numeric(df[,i])
}



best.tree2 = NA
best.prediction2 = NA
check2 = 0
test.results2 = c()


for (i in 1:1000) {
  samp = sample(as.numeric(rownames(df)), round(length(df[,1]) * 0.7))
  
  train = df[samp,]
  test = df[-samp,]
  
  tree = rpart(Result~., data = train)
  tree.predicted = predict(tree, test, type="class")
  precision = sum(tree.predicted == test$Result)/length(test$Result)
  if (as.numeric(precision) > check2) {
    best.tree2 = tree
    best.prediction2 = tree.predicted
    check2 = precision
    test.results2 = test$Result
  }
}


check2

confusionMatrix(best.prediction2, test.results2)

prp(best.tree2)





## Form (not enough data)

df = data.frame(read.csv("Form_Results.csv"))

df1 = df[,c("Circ.","Round","Result")] #Using "circularity" results also

df1 = mutate(df1, Result=as.factor(Result), Round=as.numeric(Round), Circ.=as.numeric(Circ.))


best.tree = NA
best.prediction = NA
check = 0
test.results = NA

for (i in 1:1000) {
  samp = sample(as.numeric(rownames(df1)), round(length(df1[,1]) * 0.7))
  
  train = df1[samp,]
  test = df1[-samp,]
  
  tree = rpart(Result~., data = train)
  tree.predicted = predict(tree, test, type="class")
  precision = sum(tree.predicted == test$Result)/length(test$Result)
  if (as.numeric(precision) > check) {
    best.tree = tree
    best.prediction = tree.predicted
    check = precision
    test.results = test$Result
  }
}

#Not possible to optimize tree model due to lack of "irregular" colonies (only 3)

#check
#confusionMatrix(best.prediction, test.results)
#prp(best.tree)