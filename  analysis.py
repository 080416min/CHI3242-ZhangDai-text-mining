import jieba
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

# 读取文本，这里是你的txt路径
text = open('/Users/minn/Desktop/taoanmengyi.txt', encoding="utf-8").read()

# 分词 + 停用词过滤
words = jieba.lcut(text)
stopwords = {"，", "。", "、", "？", "！", "：", "；", "“", "”", "《", "》", " ", "\n", "\t",
             "之", "而", "其", "以", "于", "是", "也", "者", "矣", "则", "乃", "夫", "的"}
clean_words = [w for w in words if w not in stopwords]

# 搭配词分析 目标词：梦忆，窗口=4
target = "梦忆"
window = 4
collocate = []

for i, w in enumerate(clean_words):
    if w == target:
        left = clean_words[max(0, i-window):i]
        right = clean_words[i+1 : i+1+window]
        collocate.extend(left + right)

count = Counter(collocate)
df = pd.DataFrame(count.items(), columns=["搭配词", "频次"]).sort_values("频次", ascending=False)
print(df.head(15))

# 保存csv
df.to_csv("taoan_collocation_梦忆_window4.csv", index=False, encoding="utf-8-sig")

# 画图
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

top10 = df.head(10)
plt.bar(top10["搭配词"], top10["频次"], color="#6082B6")
plt.xticks(rotation=45)
plt.title("与「梦忆」共现的高频搭配词（窗口=4）")
plt.ylabel("频次")
plt.tight_layout()
plt.savefig("collocation_梦忆.png", dpi=300)
plt.show()