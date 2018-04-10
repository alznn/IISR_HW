# IISR_HW
IISR_homework

1) 利用 Regular Expression 找出年月日，並輸出ouput.txt
2) 利用 Regular Expression 找名字，並輸出ouput2.txt (不算很滿意)
3) 筆記最近 python 心得：
    i. python 為 pass by assigment，所以在一些 list 的 append操作上會需要開新的空間儲存原始資料，以免後面對資料進行clear()時，所有相關有用到的object通通會一起被clear()掉
    ii. dict包 list的用法可以參考後處理那篇
    iii. regEXP 跟結巴參考 weather
4) 刻苦銘心的實驗心得：
  LogisticRegression 中，fit()使用上有幾項注意事項
    1. 針對參數X，為所謂的測試樣本集，實驗下來發現每一筆樣本data的特徵值都要以list形式儲存，若今天只有一筆特徵值，還是要壓成一個list以後append進去      train_vec中
    2. 若依照他的特徵向量，那他會視為該向量長度的特徵值數
    3. 其train_vec中，長度必須要大於1，否則train不起來，--這點讓我卡hen久--(大哭)

