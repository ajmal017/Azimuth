import pandas
#filter the data based on the ten rules of investing by benjamin graham
fin_analysis = fin_analysis[fin_analysis["epsEstimate"] > 0 ]
fin_analysis = fin_analysis[(fin_analysis["price"] < 50) & (fin_analysis["price"] > 0)]
fin_analysis = fin_analysis[(fin_analysis["peRatio"] < 11) & (fin_analysis["peRatio"] != -1)]
fin_analysis = fin_analysis[fin_analysis["priceToBook"] < 10]
fin_analysis = fin_analysis[fin_analysis["priceToSales"] < 10 & (fin_analysis["priceToSales"] > 0)]
fin_analysis = fin_analysis[fin_analysis["debt"] > 0]
fin_analysis = fin_analysis[fin_analysis["day5ChangePercent"] > 0]
