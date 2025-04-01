# Methplotter 用户手册

## 前言

欢迎使用 Methplotter！本手册旨在指导您快速了解和使用该工具，用于 DNA 甲基化数据的可视化与处理。您能通过本手册掌握 MethPlotter 的各项功能。

## 安装指南

### 环境要求

  * **操作系统** ：Windows、MacOS、Linux 均可，推荐使用Windows
  * **Python 版本** ：3.6 及以上
  * **依赖库** ：NumPy、pandas、Matplotlib、seaborn

### 安装步骤

  1. **安装 Python**
     * 访问 [Python 官方网站](https://www.python.org/)，下载并安装与您操作系统匹配的 Python 3.6 或更高版本。
     * 安装过程中，确保勾选 “Add Python to PATH” 选项，以便在命令行中能够直接使用 Python 命令。

  2. **安装 Methplotter**
     * 打开命令行工具（Windows 的命令提示符、MacOS 或 Linux 的终端）。
     * 输入以下命令并按回车键：
`pip install Methplotter`
     * 等待安装过程完成，这可能需要几分钟时间，具体取决于您的网络连接速度。

  3. **验证安装**
     * 在命令行中输入以下命令并按回车键：
`python -c "import Methplotter; print(Methplotter.__version__)"`

     * 如果安装成功，将显示 Methplotter 的版本号。


## 功能介绍

### 1\. 数据读取

Methplotter 接受两种类型的文件：CX_report.txt 文件和 gff 文件，分别有对应的函数进行数据读取。

#### 函数列表

  * **read_CX_file(path)**
    * **参数** ：path（CX_report.txt 文件的路径）
    * **返回值** ：CX_file_df（dataframe 格式，包含 CX_report.txt 文件的数据）

  * **read_gff_file(path)**
    * **参数** ：path（gff 文件的路径）
    * **返回值** ：gff_file_df（dataframe 格式，包含 gff 文件的数据）

### 2\. 数据可视化

#### 功能 1：绘制染色体 DNA 甲基化总体趋势折线图

##### 相关函数

  * **GenerateFileToDrawLineplot(CX_file_df)**
    * **参数** ：CX_file_df（dataframe 格式，经过数据读取得到）
    * **返回值** ：Stage_result（list 格式，里面装了多个 dataframe，每一个 df 代表一条染色体）

  * **Draw_line(CX_report_list, index, window_size, color)**
    * **参数** ：
      * CX_report_list（list 格式，来自执行 GenerateFileToDrawLineplot 函数的结果）
      * index（int 格式，代表想展示那一条染色体）
      * window_size（int 格式，影响折线图效果的参数）
      * color（list 格式，折线的颜色）

    * **返回值** ：无（直接绘制折线图）

##### 示例代码

```python
tem = GenerateFileToDrawLineplot(CX_file_df)
Draw_line(tem, 2, 80000, ['red', 'green', 'blue'])
```

#### 功能 2：绘制指定染色体片段前后指定长度的折线图

##### 相关函数

  * **GenerateFileToDrawLineExtraplot(CX_file, gff_file, UpAndDown)**
    * **参数** ：
      * CX_file（dataframe 格式，经过数据读取得到）
      * gff_file（经过数据读取得到）
      * UpAndDown（int 格式，代表片段前后多少长度）

    * **返回值** ：Stage_result（list 格式，里面装了多个 dataframe，每一个 df 代表一条染色体）

  * **Draw_lineExtra(CX_file, gene_string, UpAndDown, window_size, color)**
    * **参数** ：
      * CX_file（由 GenerateFileToDrawLineExtraplot 的执行结果得到）
      * gene_string（字符串类型，代表为这个片段所取的名字）
      * UpAndDown（int 格式，代表片段前后多少长度）
      * window_size（int 格式，影响折线图效果的参数）
      * color（list 格式，折线的颜色）

    * **返回值** ：无（直接绘制折线图）

##### 示例代码

```python
gff_file_fragment = gff_file[(gff_file['seqid'] == 'Chr1') & (gff_file['start'] > 18330) & (gff_file['end'] < 18643)]
tem = GenerateFileToDrawLineExtraplot(CX_file_df, gff_file_fragment, 100)
Draw_lineExtra(tem, 'typical phrase', 100, 5, ['red', 'green', 'blue'])
```

#### 功能 3：绘制多个片段的 DNA 甲基化率的聚类热图

##### 相关函数

  * **GenerateFileToDrawClusterplot(CX_file, gene_list, given_size)**
    * **参数** ：
      * CX_file（dataframe 格式，经过数据读取得到）
      * gene_list（list 格式，list 里面包含多个 gff 格式的文件）
      * given_size（int 格式，聚类的个数）

    * **返回值** ：处理后的数据（用于绘制聚类热图）

  * **Draw_cluster(file, cmap_kind, row_cluster, col_cluster)**
    * **参数** ：
      * file（由 GenerateFileToDrawClusterplot 的执行结果得到）
      * cmap_kind（聚类的方式，默认值为 "YlGnBu"）
      * row_cluster（bool 类型，是否对行进行聚类，默认为 True）
      * col_cluster（bool 类型，是否对列进行聚类，默认为 False）

    * **返回值** ：无（直接绘制聚类热图）

##### 示例代码

```python
# 生成测试数据
gff_file_fragment1 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[:5000]
gff_file_fragment1['phrase_name'] = 'fragment1'
gff_file_fragment2 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[5000:10000]
gff_file_fragment2['phrase_name'] = 'fragment2'
gff_file_fragment3 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[10000:15000]
gff_file_fragment3['phrase_name'] = 'fragment3'
gff_file_fragment4 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[15000:20000]
gff_file_fragment4['phrase_name'] = 'fragment4'
gff_file_fragment_list = [gff_file_fragment1, gff_file_fragment2, gff_file_fragment3, gff_file_fragment4]
tem = GenerateFileToDrawClusterplot(CX_file_df, gff_file_fragment_list, 20)
# 绘制聚类热力图
Draw_cluster(tem, "YlGnBu", True, False)
```

#### 功能 4：绘制多个片段的 DNA 甲基化率的箱型图

##### 相关函数

  * **GenerateFileToDrawBoxplot(CX_file, gff_file_list, context)**
    * **参数** ：
      * CX_file（dataframe 格式，经过数据读取得到）
      * gff_file_list（list 格式，list 里面包含多个 gff 格式的文件）
      * context（string 格式，CG CHG CHH）

    * **返回值** ：处理后的数据（用于绘制箱型图）

  * **Draw_box(file, context)**
    * **参数** ：
      * file（由 GenerateFileToDrawBoxplot 的执行结果得到）
      * context（string 格式，CG CHG CHH）

    * **返回值** ：无（直接绘制箱型图）

##### 示例代码

```python
# 生成测试数据
gff_file_fragment1 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[:1000]
gff_file_fragment1['phrase_name'] = 'fragment1'
gff_file_fragment2 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[1000:2000]
gff_file_fragment2['phrase_name'] = 'fragment2'
gff_file_fragment3 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[2000:3000]
gff_file_fragment3['phrase_name'] = 'fragment3'
gff_file_fragment4 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[3000:4000]
gff_file_fragment4['phrase_name'] = 'fragment4'
gff_file_fragment_list = [gff_file_fragment1, gff_file_fragment2, gff_file_fragment3, gff_file_fragment4]
tem = GenerateFileToDrawBoxplot(CX_file_df, gff_file_fragment_list, 'CHG')
# 生成随机值，范围在 - 0.5 到 0.5 之间
random_values = numpy.random.uniform(0, 1, size=len(tem))
# 将随机值应用到 ratio 列
tem['ratio'] = tem['ratio'] + random_values
Draw_box(tem, 'CHG')
```

#### 功能 5：绘制多个片段的 DNA 甲基化率的柱形图

##### 相关函数

  * **GenerateFileToDrawBarplot(CX_file, gff_file_list, context)**
    * **参数** ：
      * CX_file（dataframe 格式，经过数据读取得到）
      * gff_file_list（list 格式，list 里面包含多个 gff 格式的文件）
      * context（string 格式，CG CHG CHH）

    * **返回值** ：处理后的数据（用于绘制柱形图）

  * **Draw_bar(file, errorbar_plot, context)**
    * **参数** ：
      * file（由 GenerateFileToDrawBarplot 的执行结果得到）
      * errorbar_plot（bool 格式，是否绘制误差线，默认为 True）
      * context（string 格式，CG CHG CHH）

    * **返回值** ：无（直接绘制柱形图）

##### 示例代码

```python
# 生成测试数据
gff_file_fragment1 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[:1000]
gff_file_fragment1['phrase_name'] = 'fragment1'
gff_file_fragment2 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[1000:2000]
gff_file_fragment2['phrase_name'] = 'fragment2'
gff_file_fragment3 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[2000:3000]
gff_file_fragment3['phrase_name'] = 'fragment3'
gff_file_fragment4 = gff_file[gff_file['seqid'] == 'Chr1'].iloc[3000:4000]
gff_file_fragment4['phrase_name'] = 'fragment4'
gff_file_fragment_list = [gff_file_fragment1, gff_file_fragment2, gff_file_fragment3, gff_file_fragment4]
tem = GenerateFileToDrawBarplot(CX_file_df, gff_file_fragment_list, 'CHG')
Draw_bar(tem, True, 'CHG')
```