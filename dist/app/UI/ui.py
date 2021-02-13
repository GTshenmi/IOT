import os
import numpy as np
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5 import QtGui, QtCore
from UI.designer.mainwindow import Ui_MainWindow
from UI.designer.videowindow import Ui_VideoWindow
from UI.designer.photowindow import Ui_PhotoWindow
from app import ThreadCap,ThreadIde,ThreadUpdateTime,ScreenShot,ThreadUpdateChart,ThreadUpdatPhoto,get_wheather
from app import WheatMaturityIndexCh
import datetime
import platform
from UI.designer.chartwindow import *

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import *
# from app import startoday
from UI.designer.wheatherwindow import *
from multiprocessing import Process

from Cloud.tcp_cloud_demo import *
from time import *
from library.Sensor.TempHumiSensor import *
from library.Sensor.PHSensor import *

rootpath='/system/ftproot/aa/MaturityRecognition/'

HIGHT = 2160
WIDTH = 3840

WheatMaturityIndex = ['成熟期','灌浆期','生长期']

WheatDiseaseIndex = ['健康','条锈病','白粉病']

WheatPestsIndex = ['有虫害', '健康']

RiceMaturityIndex =['生长期','叶功能/返青期','成熟期']

RiceDiseaseIndex = ['健康','枯纹病']

RicePestsIndex = ['有虫害','健康']

FruitTypesIndex =['苹果','香蕉','杨桃','番石榴','奇异果','芒果','橘子','桃','梨','柿子','火龙果','李子','石榴','番茄','甜瓜']

FruitStateIndex = ['苹果:新鲜', '香蕉:新鲜', '橘子:新鲜', '苹果:坏的','香蕉:坏的','橘子:坏的',]

WheatTips = {
    "白粉病":"""
 小麦白粉病是一种世界性病害，在各主要产麦国均有分布，我国山东沿海、四川、贵州、云南发生普遍，危害也重。近年来该病在东北、华北、西北麦区，亦有日趋严重之势。该病可侵害小麦植株地上部各器官，但以叶片和叶鞘为主，发病重时颖壳和芒也可受害。
 
 小麦白粉病危害症状

  该病可侵害小麦植株地上部各器官，但以叶片和叶鞘为主，发病重时颖壳和芒也可受害。初发病时，叶面出现1～1.5mm的白色斑点，后逐渐扩大为近圆形至椭圆形白色霉斑，霉斑表面有一层白粉，遇有外力或振动立即飞散。这些粉状物就是该菌的菌丝体和分生孢子。后期病部霉层变为灰白色至浅褐色，病斑上散生有针头大小的小黑粒点，即病原菌的闭囊壳。

 小麦白粉病防治方法

  （1）种植抗病品种

  （2）提倡施用酵素菌沤制的堆肥或腐熟有机肥，采用配方施肥技术，适当增施磷钾肥，根据品种特性和地力合理密植。中国南方麦区雨后及时排水，防止湿气滞留。中国北方麦区适时浇水，使寄主增强抗病力。

  （3）自生麦苗越夏地区，冬小麦秋播前要及时清除掉自生麦，可大大减少秋苗菌源。

 温馨提示

  （1）杀菌剂不能与碱性农药及生物制剂混用，以防出现药害。

  （2）喷施时要注意天气，避开高温和多雨季节，尽量选择早上或傍晚 
 
    """,

    "条锈病":"""
    
 小麦条锈病是小麦锈病之一。小麦锈病俗称"黄疸病"，分条锈病、秆锈病、叶锈病3种，是中国小麦生产上分布广、传播快，危害面积大的重要病害。其中以小麦条锈病发生最为普遍且严重。小麦条锈病主要发生在叶片上，其次是叶鞘和茎秆，穗部、颖壳及芒上也有发生。
 
 防治方法：

 （1）选用抗病品种，做到抗源布局合理及品种定期轮换。

 （2）农业防治

  ①适期播种，适当晚播，不要过早，可减轻秋苗期条锈病发生。
        
  ②清除自生麦。
        
  ③提倡施用酵素菌沤制的堆肥或腐熟有机肥，增施磷钾肥，搞好氮磷钾合理搭配，增强小麦抗病力。速效氮不宜过多、过迟，防止小麦贪青晚熟，加重受害。合理灌溉，土壤湿度大或雨后注意开沟排水，后期发病重的需适当灌水，减少产量损失。

 （3）药物防治：

  ①三唑类、烯唑类为主的高效低毒内吸杀菌剂进行大田喷药防治，每亩用15%三唑酮粉剂80-100克，或亩用25%烯唑醇粉剂30-40克，或12.5%悬浮剂40毫升喷雾防治，防效可达90%以上。
        
  ②药剂拌种用25%三唑酮可湿性粉剂15g拌麦种150kg或12.5%特谱唑可湿性粉剂60~80g拌麦种50kg。
        
  ③小麦锈病、叶枯病、纹枯病混发时，于发病初期，用12.5%特谱唑可湿性粉剂20~35g，对水50~80L喷施效果优异，既防治锈病，又可兼治叶枯病和纹枯病。
          
    """,
}
RiceTips = {
    "枯纹病":"""
纹枯病

病原形态

 纹枯病菌大多以无性世代之菌丝及菌核存在自然界，不产生分生孢子，菌丝细胞多核、隔板有隔膜孔构造、分枝经常发生于先端细胞之隔板附近、分枝菌丝基部有隘缩并与主轴成直角、分枝菌丝之隔板距主轴不远，菌丝宽度7.7-(9.0)-9.9µm 。菌核结构为原始壳皮型（Primitive rind type ）较为紧密与R.solani 其他菌群之菌核为稀松型（Loose type ）不同。寄主上形成之菌核成熟后其外层细胞含较高之二氧化碳，对其内部细胞具保护作用，亦使菌核具漂浮性，在生态上什具意义。人工培养时，菌落呈褐色，褐色浓度则因菌株不同而有差别，在培养基上所形成之菌核常互相愈合成片状。有性世代之担子器与菌丝形成子实层，担子器大小10.0-22.5 × 7.0-10.5µm ，担孢子柄大小9.0-25.0µm 常有隔膜，担孢子大小7.5-10.7 × 4.5-6.0µm 。

病原生活史

 病原菌在自然界以无性世代为主，利用菌丝行营养生长，以菌核为主要繁殖体，具残存及传播功能，菌丝在土壤中之存活力不强，但在病组织中存活期较长。高湿及低光照之环境下，纹枯病菌亦会在寄主组织表面形成有性世代之担孢子，虽有学者认为其具传播功能，但无实证。

病征

 水稻从秧苗期至成熟期整个生育期间均会被纹枯病菌感染，各生育期之病征大同小异。目前农友大多采用机械插秧，箱育秧苗时间短，秧苗期发生纹枯病的机会少。本田期水稻栽培过程中，从分 中期至成熟期为纹枯病之主要发生期。秧苗初罹患纹枯病时于叶鞘与叶片上均出现灰污绿色水浸状病斑，后期病斑中央灰白色边缘褐色。本田水稻分 中期纹枯病开始发生，纹枯病菌常从稻丛内部稻株之下位叶鞘开始感染，再向外部稻株及向上蔓延。叶鞘上病征先形成约1 公分大小的灰绿色水浸状圆形或椭圆形病斑，后逐渐扩大为长约2~3 公分，宽1 公分之病斑，病斑边缘褐色中间转成灰白色，高湿高温环境下数个病斑愈合成虎斑状。晴朗的气候下，叶鞘组织枯死，并导致水份输送不良，造成叶片黄化干枯，稻丛外围稻株之叶鞘虽然没有纹枯病斑，但内部稻株之下位叶会有枯黄现象，拨开稻株常可看见稻丛内部有纹枯病发生。斑会蔓延扩展到叶片上。分 盛期以后，稻丛之叶片相互交织，当叶片接触到邻近叶片或叶鞘之病斑亦会被传染致病。叶部受害时初呈湿润状灰绿色，病斑迅速扩大形成云纹状或不正形的枯褐色大病斑。感染纹枯病之叶片组织枯死初期不易造成卷曲，与白叶枯病引起叶片卷曲，有所不同。水稻孕穗后期遇到高温高湿之环境，农友如未采取防治纹枯病措施，发病稻丛之稻穗在抽出时就会被感染，稻穗被害部位呈污绿色，枝梗及谷粒腐朽呈灰褐色枯死。乳熟期以后之稻穗被害则局部初呈污绿色，后转为灰褐色病斑。稻纹枯病在环境适宜，温度24~28 ℃之高湿环境下，发病后约3~4 天，病斑上或附近稻表面组织上的菌丝会开始形成菌核，菌核初呈白色菌丝团，经过约2 天时间转为褐色，菌核接触寄主组织之一面常向内凹，而成不正之扁球形，纹枯病与其他菌核性病害之主要区别，为病株外表会形成菌核。
    
发生生态

由纹枯病菌生态学研究结果，发现其初次感染源（Primary inoculum ）为菌核，二次感染源（Secondary inoculum ）则以菌丝为主。吉村曾报告，推测有性世代之担孢子可为二次感染源，但尚未见试验证明。早期耕作方式，以牛耕犁并用人工除草，田间纹枯病菌菌核之消长，如堀氏之报告，纹枯病发生过程之第一阶段为" 菌核浮上期" ，由插秧至分 中期，田水中菌核量受越冬菌核量及土壤搅动次数即除草次数之影响；第二阶段为" 菌核漂流期" ，由分 中期至幼穗伸长初期。杜及张报告，目前水中菌核之漂浮量以整田后至插秧期间最多，菌核在稻田水面之分布受风向及风速影响最大，灌溉水次之，例如第一期作初期，西北季风较强，稻田东南角水面漂浮之菌核量最多，与其他角落呈极显著之差异。插秧后田水中漂浮之菌核数逐日递减，一个月后就不易由水中采集到菌核，此时大部分菌核被漂流到四周之田埂上，成为无效感染源外，少部分菌核漂流在田水中时碰到水稻植株，菌核就附着在稻叶鞘外侧，其附着位置并随水稻之生长而升高。分中期因稻丛茎数增加，稻丛间湿度加大，菌核开始发芽感染叶鞘致病，此即为第一次感染源。从插秧至分 中期在田中所采集到之菌核，其发芽率约为50~75 ％，分 期田间纹枯病之发生与附着菌核之水稻丛数及菌核发芽率有关。第一期作插秧30~45 天后或第二期作15~30 天后，即水稻分 中期，纹枯病从稻丛基部开始发生。病菌侵入水稻组织后，利用菌丝在组织中蔓延，湿度大尤其遇下雨时，病斑急速往上扩展。水稻分 盛期以后，稻株间稻叶逐渐稠密，田间交织的稻叶即为第二次感染源传播之工具，相对湿度高、有露水或下雨时，病菌之蔓延则更迅速，水稻孕穗期及抽穗期为纹枯病横向病势进展主要时期。田间观察发现，利用发病茎之病叶为传染源时，因叶片基部受害，如遇天候干燥，水份无法输送，极易干枯，传染能力随之消失；但健株之叶片伸展至发病丛受病菌感染时，无论天候干或湿，病菌之菌丝均能顺着叶片传染到健株上。此可说明，气象不适合一般菌类病害发生之年份，纹枯病发生面积率尚高达10 ％以上之原因。环境适宜时，纹枯病菌从长出菌丝至产生成熟菌核，只需80 小时。田间微气候变化很大，病菌侵入水稻组织，一般需要5~10 天，可陆续产生菌核。插秧后约70~80 天，田间病株上陆续有菌核形成，菌核因受外力振动而掉落，因此田水中之菌核量又呈不规则升高，此时田水中之菌核发芽率高达90~100 ％，但这些菌核甚少感染孕穗期或抽穗期水稻。综合上述各点，得知纹枯病以菌丝为第二次感染源，所以本病在田间之分布型态为丛集型，即由初次感染源所感染之稻丛向外蔓延成一聚落。温度低于4 ℃或高于40 ℃时，纹枯病菌即停止生长，最适生长温度为28 ℃，每小时菌丝可生长1.27 公厘，即每日可生长3 公分以上。在恒温培养箱内，利用人工接种测定病势进展，结果24~28 ℃最适合发病及病斑扩展，12 ℃以下接种7 日后尚未见发病。国外报告28~32 ℃及30~32 ℃为最适合发病之温度，菌核形成则在24~28 ℃温度下最快，接种约60 小时即有菌核形成，80 小时菌核转为褐色；以16~20 ℃之温度范围内所产生之菌核量最多。病茎上，纹枯病菌以24 ℃为最适形成菌核之温度。相对湿度对稻纹枯病之影响，杜及张报告相对湿度81~92 ％最适合稻纹枯病之发生，国外则分别有96~97 ％及95 ％左右最适合发病之报告。菌丝生长最适酸碱度为pH5.0~7.0 之间，偏酸至pH4.2时菌丝生长尚无显著影响，但pH 值升高至8.0 时，菌丝生长已显著缓慢，菌核形成则以碱性较为有利。水稻纹枯病原菌主要以菌核为残存体，简等报告，田间纹枯病发病率28.5 ％时，每公顷产生菌核量高达200 万个之多；杜等则报告，纹枯病发病率18 ％时，每公顷产生的菌核量高达300 万个之多。病株上之菌核在水稻收获后，大部份菌核掉落于稻桩上，分析稻桩上与土表面菌核量比值平均为 7.9 比1 。收获时菌核发芽率约为90~100 ％，残存至下期作插秧时降为70~80 ％，到分 期约为50~75 ％。菌核被埋入积水状况之砂土中约可存活8 个月，在土表面则可活2 年之久。
    
防治方法

（一）栽培管理
 
 1.稻种处理：真菌或细菌引起的水稻病害以及线虫白尖病，常会感染或污染稻谷，而经由稻种传播病害。病原感染稻种会造成谷粒不饱实成为秕粒，换句话说，稻谷中的秕粒带有病原菌的机率很高。病秕粒带菌量比被污染的谷粒高，病秕混在稻种中，其感染稻苗之潜势更强。因此浸种前以硫酸铵水溶液水选健谷，去除病秕，再行稻种消毒。硫酸铵水溶液之比重，蓬莱稻种采用1.13 ，在来稻种则用1.08 。
       
 2.浸种及育苗管理：稻种应充分浸水，第一期作浸种3-4 天，第二期作则浸种2-3 天，浸种后将稻种沥干再以湿麻布袋覆盖催芽，稻芽长出约1 公厘时播种，播种后覆土不要超过5 公厘厚度，如此可缩短育苗箱堆积时间，减少病菌感染机会。第一期作催芽之温度避免超过室外气温太多，以防稻种及稚苗在短时间内受温度剧变而抗病性减弱。育苗箱所用栽培土，以病原菌较少之水田心土较佳。如果无法取得水田心土，所用土壤最好阴干后存放较长时间，待土中病原菌密度降低后再使用。如使用旧育苗箱，因可能附着有病原菌，其发病率比新育苗箱者为高，所以育苗箱使用后应马上清洗，尤其育苗箱之角落需要特别注意清洗干净，洗净后应消毒，如无法消毒至少须晒干后再使用。每一育苗箱播种量以200-220 公克稻种为宜，播种太多太密易滋生病菌，发生秧苗立枯病。第一期作遇寒流时，应覆盖塑胶布保温，寒流过后温度回升时，则需将塑胶布两端打开使能通风，避免过度潮湿促进病菌滋长。第二期作最好用尼龙网覆盖，阻断媒介昆虫吸食时传染病毒。
       
 3. 整地：翻整田地，除了让我们容易插秧外，同时也可以将病虫翻埋土中，降低田间病菌及害虫的族群。整地时将田间植物残株翻埋土中，植物残株在土中会腐败酦酵，酦酵过程中会降低土壤中的氧气，也会产生一些对稻株不好的物质。因此，我们最好采取二段式整地，二次整地的时间最好有半个月以上的间隔，一方面让埋入土中的植物残体酦酵，一方面让前期作留下的过剩肥料均匀化。
       
 4. 灌排水：整地时采用浅水整地，以利将植物残株翻埋。二段整地的间隔期，则采较深的田水，可以让纹枯病菌等病原菌的菌核及植物残株漂浮至下风处，捞起漂浮物晒干烧毁，可降低病虫害密度。插秧后田中维持浅水状态。往昔人工除草翻动田土可增加土壤中的氧气，现今水稻栽培大多利用杀草剂除草，土壤未经搅动，土壤中的氧气会渐次减少，容易呈现还原态而有碍稻根生长。一期作插秧后25 天，二期作插秧后15 天，水稻分 初期至分 中期之间，即可进行晒田，晒田到田土轻微龟裂后，接着采用间歇性灌排水，如此可以强化稻根，稻株健壮增加抗病力。如果田间有病害发生时，必须保持适当的田水，不能干旱而增加稻株逆境压力。水稻抽穗期以后改以深水灌溉，水稻生育后期愈晚排水愈好。
       
 5. 行株距：行株距大，稻株比较健壮比较抗病，纵然发病也能比较耐病。那种行株距大小比较好？各地区土壤肥沃程度不同，因此，适当行株距就有不同，农友可自行测试比较。除行株距外，稻行的方向也会影响田间的通风，插秧行向采用与季节风同向，田间通风良好，可降低水稻病害的蔓延速率。
       
 6. 施肥：肥料对水稻病害的影响，氮肥最为密切，磷及钾的影响较小。多施氮肥容易发生稻热病、纹枯病及白叶枯病，氮肥多时磷肥会助长发病，钾肥则可增加稻株抗病，氮肥多会降低钾肥的效果。缺氮时容易发生胡麻叶枯病，顾及各种病害之防治，多施有机氮肥，可以避免缺氮肥，稻株也比较抗病。矽是稻株的重要元素，可以强化细胞增强抗病，施用矽酸钙可增强稻株抗病，稻壳及稻草分解后也会释出矽酸化合物。前作种植绿肥，要采用二段式整地，初整地时每公顷加施75 公斤石灰，可以促进绿肥分解。前作种植蔬菜若残留过多氮肥，亦要采用二段式整地，初整地时可加施稻壳或稻草，稻壳及稻草分解时会利用氮肥，降低氮肥过量及不均匀的风险。
       
 7. 田间卫生：水稻病害的病原常会感染田间杂草，繁殖增加病原密度，杂草也是媒介昆虫的主要栖息处，所以清除杂草是防治病害的重要工作。病株收割后长出稻桩为田间主要感染源，水稻收获后应将稻桩翻犁，降低病原密度，也可避免长出稻椿供媒介昆虫栖息。大多数病菌会残存在病组织中，所以不能留置病稻草在田间。稻草要利用为堆肥时，必须经过酦酵，完全腐熟后才能使用。 白叶枯病除了靠稻叶接触传播，人在露水未干的稻田中行走也会迅速将病害传开，因此要避免在晨间在稻田中行走。
    
（二）药剂防治
 
 稻纹枯病是水稻栽培的风土病，施用药剂防治是无可避免的。药剂防治时机可参考前述之生态研究结果，即纹枯病之初次感染源为本田初期附着在稻植株上之菌核，分 期丛间湿度增大，附着在稻植株上之菌核开始发芽感染水稻致病，发病后病菌靠菌丝在交织的稻叶间进行二次感染，所以初次感染源多寡影响分 期之发病，分蘖期之发病又直接关系到后期之发病率，由此结果推论早期防治效果较佳，由试验证明早期在分 时进行施药防治效果好。蔡氏报告，早期防治可减少产量损失，药剂防治次数与经济防治水准，则依纹枯病发生之严重性而定。彭及唐报告，分别在水稻分 期、孕穗期及抽穗期施药一次或两次，观察其防治效果，结果分期施药两次防治率达74.0 ％最好，孕穗期防治两次之防治率71.2 ％次之，分 期防治一次之防治率64.7 ％，孕穗期防治一次之防治率58.9％，抽穗期施药两次及一次之防治率则分别为27.8 及19.9 ％，显示早期防治较能控制纹枯病之病情，至抽穗期再防治则其效果甚差，因此以分 期为施药的最佳时期。换一句话说，纹枯病初发生时就要即时防治，纹枯病菌的菌核具漂浮力，农友在水稻分 期时，可留意插秧期间的风尾处，因菌核密度高，发病会比较早。 
       
    """,

}

class MainWindows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindows, self).__init__(None)

        self.humi = 0.0
        self.temp = 0.0
        self.time = ''


        # 设置UI
        self.setupUi(self)

        self.UpdateUi()

        # Button
        self.SetButtonConnected()

        self.SetLabelStyle()

        # 新的线程 更新时间
        self.InitThread()

        #self.ip = '192.168.123.106'

        if platform.system() != 'Windows':
            try:
                cmd_ip_eth0 = "ip addr show 'eth0'| grep 'inet '| awk '{print $2}'"
                eth0_content = subprocess.getstatusoutput(cmd_ip_eth0)
                if eth0_content[0] == 0:
                    if eth0_content[1] != '':
                        ip_content = eth0_content[1].split('/')
                        dev_ip = ip_content[0]
                        self.ShowIPLabel.setText(f'当前ip：\n{dev_ip}')
                    else:
                        self.ShowIPLabel.setText(f'当前ip：\n无')
                else:
                    self.ShowIPLabel.setText(f'当前ip：\n无')
            except Exception as e:
                print(e)
                self.ShowIPLabel.setText(f'当前ip：\n无')

        #self.ShowIPLabel.setText(f'当前ip：\n{dev_ip}')


    def InitThread(self):
        self.frameID = 0

        self.wthread3 = ThreadUpdateTime(self)
        self.wthread3.updatetime.connect(self.UpdateTime)
        self.wthread3.start()

    def UpdateTime(self):
        self.time = str(datetime.datetime.now())
        self.dateLable.setText('\t' + self.time[0:19]+'\t\t\t\t')

    def updatetemphumi(self):
        pass

    def SetLabelStyle(self):

        self.dateLable.setStyleSheet("QLabel{background:rgb(255,255,255,100)}")

        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        self.dateLable.setFont(font)

        self.School.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                          "QPushButton:hover{color:rgb(100,100,100,120);}")

    def SetButtonConnected(self):

        self.showchartbutton.pressed.connect(self.ShowChartButtonPressed)
        self.showlocationbutton.pressed.connect(self.ShowLocationButtonPressed)
        self.showvirusbutton.pressed.connect(self.ShowVirusButtonPressed)
        self.showperiodbutton.pressed.connect(self.ShowPeriodButtonPressed)
        self.showpestsbutton.pressed.connect(self.ShowPestsButtonPressed)
        self.exitbutton.pressed.connect(self.ExitButtonPressed)


    def setButtonStyle(self,buttonobj,path):

        pixmap = QPixmap(QImage(path))

        fixpixmap = pixmap.scaled(635, 360, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

        icon = QIcon(fixpixmap)

        buttonobj.setIcon(icon)
        buttonobj.setIconSize(QSize(435, 360))

        buttonobj.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                                "QPushButton:hover{color:rgb(100,100,100,120);}")

    def UpdateUi(self):

        #设置背景图片
        self.setStyleSheet("#MainWindow{border-image:url(UI/images/backgroundpic.png);}")

        self.backgroundlable.setPixmap(QPixmap("UI/images/backgroundpic.png"))
        self.backgroundlable.setScaledContents(True)
        # self.gif = QMovie("UI/images/backgroundpic.gif")
        # self.backgroundlable.setMovie(self.gif)
        # self.gif.start()

        self.setButtonStyle(self.showchartbutton,"UI/images/icon/chart.png")

        self.SetWheatherIcon()

        self.setButtonStyle(self.showvirusbutton, "UI/images/icon/virus.png")
        self.setButtonStyle(self.showperiodbutton, "UI/images/icon/period.png")
        self.setButtonStyle(self.showpestsbutton, "UI/images/icon/pest.png")
        self.setButtonStyle(self.exitbutton, "UI/images/icon/exit.png")

        self.School.setPixmap(QPixmap('UI/images/yzu.png'))
        self.School.setStyleSheet("QPushButton{background:rgb(255,255,255,50);}"
                                           "QPushButton:hover{color:rgb(100,100,100,120);}")

        self.School.setScaledContents(True)
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)

        self.ShowIPLabel.setFont(font)

    def SetWheatherIcon(self):

        self.weather = get_wheather()
        if '晴' in self.weather[0]:
            self.setButtonStyle(self.showlocationbutton, "UI/images/icon/sun.png")
        elif '雨' in self.weather[0] :
            self.setButtonStyle(self.showlocationbutton, "UI/images/icon/rain.png")
        elif '多云' in self.weather[0]:
            self.setButtonStyle(self.showlocationbutton, "UI/images/icon/partlycloudy.png")
        else:
            self.setButtonStyle(self.showlocationbutton,"UI/images/icon/wheather.png")

    def ShowChartButtonPressed(self):

        self.showchartbutton.setEnabled(False)
        self.box = ChartBox()
        self.box.showFullScreen()
        #self.box.show()
        self.showchartbutton.setEnabled(True)

        pass

    def ShowLocationButtonPressed(self):

        self.showlocationbutton.setEnabled(False)

        self.SetWheatherIcon()

        self.box = MapBox()
        self.box.showFullScreen()
        #self.box.show()
        self.showlocationbutton.setEnabled(True)

        pass

    def ShowVirusButtonPressed(self):

        self.showvirusbutton.setEnabled(False)
        self.box = VideoBox(HIGHT, WIDTH, 1)  # 小麦病害情况
        self.StopThread()
        self.box.showFullScreen()
        self.box.show()
        self.showvirusbutton.setEnabled(True)


    def ShowPeriodButtonPressed(self):

        self.showperiodbutton.setEnabled(False)
        self.box = VideoBox(HIGHT, WIDTH,0)  # 小麦生长状况
        self.StopThread()
        self.box.showFullScreen()
        #self.box.show()
        self.showperiodbutton.setEnabled(True)

    def ShowPestsButtonPressed(self):

        self.showpestsbutton.setEnabled(False)
        self.box = VideoBox(HIGHT, WIDTH, 2)  # 小麦虫害状况
        self.StopThread()
        self.box.showFullScreen()
        #self.box.show()
        self.showpestsbutton.setEnabled(True)
        pass

    def ExitButtonPressed(self):

        self.exitbutton.setEnabled(False)
        self.exitbutton.setEnabled(True)
        if self.wthread3:
            self.wthread3.stop()
        self.StopThread()
        qApp = QApplication.instance()
        qApp.quit()  # 关闭窗口

    def StopThread(self):
        pass



class VideoBox(QMainWindow, Ui_VideoWindow):

    def __init__(self, capWidth, capHeight,workMode):
        super(VideoBox, self).__init__(None)

        # 工作模式选择

        self.workmode=workMode
        self.isRun=False
        self.fps = 0.0
        self.trantext=''
        self.temp = 0.0
        self.humi = 0.0
        self.ph = 0.0
        self.change = False
        self.diseasegrade = 0

        self.showtipsstate = False

        self.system = platform.system()


        #设置界面
        self.setupUi(self)

        self.UpdateUi()

        self.AddFruitButton()

        self.SetButtonConnected()

        # 初始化摄像头

        if self.system == 'Windows':

            self.url = 'rtsp://192.168.123.106:554/user=admin&password=admin&channel=1&stream=0.sdp?'

        else:

            self.url = 'rtsp://192.168.123.106:554/user=admin&password=admin&channel=1&stream=0.sdp?'

        ip = '192.168.123.106'

        if self.system != 'Windows':
            backinfo = os.system('ping -c 1 -w 2 '+ip)  # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
        else:
            backinfo = os.system('ping -n 1 -w 2 ' + ip)  # 实现pingIP地址的功能，-n1指发送报文一次，-w1指等待1秒

        if backinfo:
            print(backinfo)
            self.url = 0
        else:
            print(backinfo)

        #self.url = 'C:/03.mp4'



        self.showvideo = False

        #self.url = 1


        self.cap = cv2.VideoCapture(self.url)

        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,HIGHT)

        self.StartShowVideo()

    def AddFruitButton(self):
        if self.workmode == 0 or self.workmode == 3:

            self.wheatButton.setGeometry(QtCore.QRect(0, 253, 128, 80))
            self.riceButton.setGeometry(QtCore.QRect(0, 453, 128, 80))
            self.fruitButton = QtWidgets.QPushButton(self.centralwidget)
            self.fruitButton.setGeometry(QtCore.QRect(0, 653, 128, 80))
            self.fruitButton.setFocusPolicy(QtCore.Qt.NoFocus)
            self.fruitButton.setText("")
            self.fruitButton.setObjectName("fruitButton")
            self.SetButtonIcon(self.fruitButton, "UI/images/icon/fruit.svg", 64, 64)
            self.fruitButton.setFlat(False)
            self.fruitButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                                          "QPushButton:hover{color:rgb(100,100,100,120);}")

    def SetButtonConnected(self):

        self.shotButton.clicked.connect(self.shotButtonPressed)

        self.exitButton.clicked.connect(self.exitButtonPressed)

        self.riceButton.clicked.connect(self.riceButtonPressed)

        self.wheatButton.clicked.connect(self.wheatButtonPressed)

        self.showphotobutton.clicked.connect(self.ShowPhotoButtonPressed)

        self.reversebutton.clicked.connect(self.ReverseButtonPressed)

        self.ShowButton.clicked.connect(self.ShowButtonPressed)

        self.ShowTipsButton.clicked.connect(self.ShowTipsButtonPressed)

        if self.workmode == 3 or self.workmode == 0:
            self.fruitButton.clicked.connect(self.FruitButtonPressed)

    def UpdateUi(self):

        #拍照按钮
        self.SetButtonIcon(self.shotButton,"UI/images/icon/photograph.png",96,96)

        #退出按钮
        self.SetButtonIcon(self.exitButton, "UI/images/btn_back_r_normal.png", 128, 64)

        #切换按钮

        self.SetButtonIcon(self.reversebutton, "UI/images/icon/reverse.svg", 96, 96)

        #显示图片按钮

        self.SetButtonIcon(self.showphotobutton, "UI/images/icon/pic.svg", 96, 96)

        self.SetButtonIcon(self.ShowTipsButton,"UI/images/icon/tipsoff.svg",48,48)
        self.ShowTipsButton.setFlat(True)
        self.ShowTipsButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                           "QPushButton:hover{color:rgb(100,100,100,120);}")
        self.ShowTipsButton.setEnabled(False)
        #self.ShowTipsButton.hide()


        #切换水稻按钮

        self.SetButtonIcon(self.riceButton, "UI/images/icon/rice.png", 64, 64)

        self.riceButton.setFlat(False)

        self.riceButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                           "QPushButton:hover{color:rgb(100,100,100,120);}")



        #切换小麦按钮

        self.SetButtonIcon(self.wheatButton, "UI/images/icon/wheat.png", 64, 64)

        self.wheatButton.setFlat(False)

        self.wheatButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                           "QPushButton:hover{color:rgb(100,100,100,120);}")


        self.SetButtonIcon(self.ShowButton, "UI/images/icon/show.svg", 64, 64)

        self.ShowButton.setFlat(False)

        self.ShowButton.setStyleSheet("QPushButton{background:rgb(255,255,255,0);}"
                           "QPushButton:hover{color:rgb(100,100,100,120);}")

        #状态栏
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)

        self.head.setFont(font)

        self.head.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                "QLabel:hover{color:rgb(100,100,100,120);}")

        font = QFont()
        font.setBold(True)
        font.setPointSize(20)

        self.TipsLabel.setFont(font)

        self.TipsLabel.setStyleSheet("QTextBrowser{background:rgb(255,249,222,245);}"
                                "QTextBrowser:hover{color:rgb(100,100,100);}")


        # self.TipsLabel.setStyleSheet("QTextBrowser{background:rgb(255,255,200,235);}"
        #                         "QTextBrowser:hover{color:rgb(100,100,100);}")



        #self.TipsLabel.setStyleSheet("QTextBrowser{background-image:url(UI/images/backgroundpic.png);")



        self.TipsLabel.hide()

        #设置背景
        # self.gif = QMovie("UI/images/backgroundpic.gif")
        #
        # self.backgroundlabel.setMovie(self.gif)
        #
        # self.gif.start()

        self.setStyleSheet("#VideoWindow{border-image:url(UI/images/backgroundpic.png);}")


        #视频UI
        self.pictureLabel.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件

        self.pictureLabel.setStyleSheet("QLabel{background:rgb(255,255,255,60);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        self.pictureLabelbackground.setAutoFillBackground(True)

        self.pictureLabelbackground.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        # 结果显示框
        self.resulttext.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                        "QLabel:hover{color:rgb(100,100,100,120);}")

        #设置文本框
        pixmap=QPixmap("UI/images/yzu.png")
        self.schoolbadge.setPixmap(pixmap)

        self.schoolbadge.setScaledContents(True)

        self.teammumber.setText("YZU-灵听者：\n包飞霞\r刘源\n牛恺锐\r薛鹏")


    def SetButtonIcon(self,buttonobj,path,width,hight):
        #拍照按钮
        pixmap = QPixmap(QImage(path))

        fixpixmap = pixmap.scaled(width, hight, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

        icon = QIcon(fixpixmap)


        buttonobj.setIcon(icon)

        buttonobj.setIconSize(QSize(width, hight))

        buttonobj.setFlat(True)

        buttonobj.setStyleSheet("border:none")

    def StartShowVideo(self):
        # 设置双线程
        self.frameID = 0
        self.isRun = True
        self.CapIsbasy = False
        self.AlgIsbasy = False

        # 设计视频采集参数
        self.showImage = None
        self.limg = None



        # 线程1相机采集

        # self.p = Process(target=ThreadCap,args=(self,))
        # self.p.start()
        # self.p.join()


        self.wthread = None
        self.wthread = ThreadCap(self)
        self.wthread.updatedImage.connect(self.showframe)
        self.wthread.start()

        # 线程2算法处理
        self.wthread2 = None
        self.wthread2 = ThreadIde(self)
        self.wthread2.updatedresult.connect(self.showresult)
        self.wthread2.start()

    def shotScreen(self):
        Screen = ScreenShot()

    def ShowButtonPressed(self):
        try:
            if self.isRun:
                if self.wthread:
                    while self.CapIsbasy:
                        pass

                    self.wthread.stop()
                    self.wthread2.stop()

                    if self.cap.isOpened():
                        self.cap.release()
                        self.CapIsbasy = False

                    self.isRun = False
            if self.showvideo == True:
                self.showvideo = False

                self.ClearTips()

                ip = '192.168.123.106'

                if self.system != 'Windows':
                    backinfo = os.system('ping -c 2 -w 3 ' + ip)  # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
                else:
                    backinfo = os.system('ping -n 2 -w 3 ' + ip)  # 实现pingIP地址的功能，-n1指发送报文一次，-w1指等待1秒

                if backinfo:
                    print(backinfo)
                    self.url = 0
                else:
                    print(backinfo)
                    self.url = 'rtsp://192.168.123.106:554/user=admin&password=admin&channel=1&stream=0.sdp?'
            else:
                self.ClearTips()
                self.showvideo = True
                self.url = 'C:/01.mp4'

                if platform.system() == 'Windows':
                    root = 'C:/MaturityRecognition/'
                else:
                    root = '/system/ftproot/aa/MaturityRecognition/'

                if self.workmode == 0:
                    self.url = f'{root}video/WheatMaturity.mp4'
                elif self.workmode == 1:
                    self.url = f'{root}video/Maturity.mp4'
                elif self.workmode == 2:
                    self.url = f'{root}video/Maturity.mp4'
                elif self.workmode == 3:
                    self.url = f'{root}video/Maturity.mp4'
                elif self.workmode == 4:
                    self.url = f'{root}video/Maturity.mp4'
                elif self.workmode == 5:
                    self.url = f'{root}video/Maturity.mp4'


            ##################################
            if os.path.exists(self.url):
                self.cap = cv2.VideoCapture(self.url)
            else:
                self.cap = cv2.VideoCapture(0)

            # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
            # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HIGHT)

            self.StartShowVideo()
        except Exception as e:
            print(e)

        pass
    def shotButtonPressed(self):
        ret,img = self.cap.read()
        if ret==True and self.text!='getting...' and self.trantext!='NULL':
            if self.workmode <=2:
                self.type = 'Wheat'
            elif self.workmode>=3 and self.workmode<6:
                self.type = 'Rice'
            elif self.workmode==6:
                self.type = ''

            self.img = img
            self.img = cv2.resize(self.img,(640,540))

            if self.system == "Windows":
                rootpath = 'C:/Python Code/MaturityRecognition/'
                self.imgname = f'{self.type}-{self.trantext}-{str(datetime.datetime.now()).replace(":","-")}.png'
            else:
                rootpath = '/system/ftproot/aa/MaturityRecognition/'
                if self.workmode!=6 and self.workmode != 7:
                    self.imgname = f'{self.type}:{self.trantext}-{str(datetime.datetime.now())[0:19]}.png'
                else:
                    self.imgname = f'{self.trantext}-{str(datetime.datetime.now())[0:19]}.png'

            if(os.path.exists(rootpath+'camera/')):
                cv2.imwrite(rootpath+'camera/'+self.imgname,self.img)
            else:
                print('error code -1:can not find dir')

        self.shotScreen()


    def ShowTips(self,text):
        # font = QFont()
        # font.setBold(True)
        # font.setPointSize(20)
        #
        # self.TipsLabel.setFont(font)
        #
        # self.TipsLabel.setStyleSheet("QLabel{background:rgb(255,255,255);}"
        #                         "QLabel:hover{color:rgb(100,100,100);}")

        # self.TipsLabel.hide()
        if self.showtipsstate == False:
            self.TipsLabel.show()
            self.TipsLabel.setText(text)
            self.showtipsstate = True
        elif self.showtipsstate == True:
            self.TipsLabel.setText('')
            self.TipsLabel.hide()
            self.showtipsstate = False

        pass

    def ShowTipsButtonPressed(self):
        if self.text == '健康':
            self.ClearTips()
        else:
            if self.workmode < 3:
                if self.text != 'getting...':
                    self.ShowTips(WheatTips[self.text])
            elif self.workmode <6:

                if self.text != 'getting...':
                    self.ShowTips(RiceTips[self.text])

        pass

    def ChangeTipsIcon(self):

        if self.text != '健康':
            self.SetButtonIcon(self.ShowTipsButton,"UI/images/icon/tipson.svg",48,48)
            self.ShowTipsButton.setEnabled(True)
        else :
            self.SetButtonIcon(self.ShowTipsButton,"UI/images/icon/tipsoff.svg",48,48)
            if self.showtipsstate == False:
                self.ClearTips()
            else:
                self.ShowTipsButton.setEnabled(True)


        # self.ShowTipsButton.setFlat(True)
        # self.ShowTipsButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
        #                    "QPushButton:hover{color:rgb(100,100,100,120);}")
        # #self.ShowTipsButton.hide()


    def showframe(self):

        if self.showImage != None:
            self.pictureLabel.setPixmap(self.showImage)
            self.pictureLabel.setScaledContents(True)
        self.currenttime = str(datetime.datetime.now())

        if self.temp != None and self.humi != None and self.ph != None:
            # self.head.setText('\t'+self.currenttime[0:19]+'  温度：'+str(self.temp)[0:5]+'°C'+"  湿度："+str(self.humi)[0:7]+'%'+'  PH:'+str(self.ph))
            self.head.setText(f'    {self.currenttime[0:19]}    温度：  {str(self.temp)[0:5]}°C    湿度：  {str(self.humi)[0:7]}%    PH:  {str(self.ph)}')
        else:
            #self.head.setText('\t' + self.currenttime[0:19] + '  温度：Error' + "  湿度：Error"+'PH:Error' )
            self.head.setText(f'    {self.currenttime[0:19]}    温度：Error    湿度：Error  PH:Error')

    def showresult(self):


        if self.text != 'getting...':
            self.time = f'{str(self.time)[0:8]} s'
        # self.currenttime = str(datetime.datetime.now())


        # if self.temp != None and self.humi != None and self.ph != None:
        #     # self.head.setText('\t'+self.currenttime[0:19]+'  温度：'+str(self.temp)[0:5]+'°C'+"  湿度："+str(self.humi)[0:7]+'%'+'  PH:'+str(self.ph))
        #     self.head.setText(f'    {self.currenttime[0:19]}    温度：  {str(self.temp)[0:5]}°C    湿度：  {str(self.humi)[0:7]}%    PH:  {str(self.ph)}')
        # else:
        #     #self.head.setText('\t' + self.currenttime[0:19] + '  温度：Error' + "  湿度：Error"+'PH:Error' )
        #     self.head.setText(f'    {self.currenttime[0:19]}    温度：Error    湿度：Error  PH:Error')

        if self.fps != 'getting...':
            self.fps = str(self.fps)[0:8]


        self.tips = ''
        if(self.workmode==0):
            if self.text not in WheatMaturityIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            if self.text == "生长期":

                if self.temp >= 13.0 and self.temp < 18.0:
                    self.tips = '温度适宜，小麦生长最快'
                elif self.temp >= 6.0 and self.temp < 13.0:
                    self.tips = '温度适宜,小麦生长较快'
                elif self.temp >= 3.0 and self.temp < 6.0:
                    self.tips = '温度偏低,小麦生长缓慢'
                elif self.temp >= 18.0:
                    self.tips = "温度偏高,小麦生长受到抑制"
                elif self.temp <= 0.0:
                    self.tips = "小麦停止生长,进入越冬期。"


            elif self.text == "灌浆期":

                if self.temp !=None:
                    if self.temp >= 20.0 and self.temp < 22.0:
                        self.tips = '温度适宜小麦生长'
                    elif self.temp >= 12.0 and self.temp < 20.0:
                        self.tips = '温度偏低,灌浆期可能延长,易获高产'
                    elif self.temp >= 22.0 and self.temp < 28.0:
                        self.tips = '温度偏高'
                    elif self.temp <= 12.0:
                        self.tips = "温度过低"
                    elif self.temp >= 28.0:
                        self.tips = "温度过高,植物失水加速,影响灌浆"
            else:
                self.tips = '注意及时收割。'

            self.resulttext.setText(f'小麦\n\n成熟度：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}\n\nTips:{self.tips}')

        if(self.workmode==1):
            if self.text not in WheatDiseaseIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
                self.diseasegrade = 'getting...'

            if self.text != 'getting...':
                self.ChangeTipsIcon()
            if self.text == '健康':
                #self.ClearTips()
                self.resulttext.setText(f'小麦\n\n病害情况：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')
            else:
                #self.ChangeTipsIcon()
                self.resulttext.setText(f'小麦\n\n病害情况：{self.text}\n\n病害等级：{self.diseasegrade}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if(self.workmode==2):
            if self.text not in WheatPestsIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'小麦\n\n虫害情况：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if(self.workmode==3):
            if self.text not in RiceMaturityIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'水稻\n\n成熟度：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if(self.workmode==4):
            if self.text not in RiceDiseaseIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
                self.diseasegrade = 'getting...'

            if self.text != 'getting...':
                self.ChangeTipsIcon()

            if self.text == '健康':
                #self.ClearTips()
                self.resulttext.setText(f'水稻\n\n病害情况：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')
            else:
                self.ChangeTipsIcon()
                self.resulttext.setText(f'水稻\n\n病害情况：{self.text}\n\n病害等级：{self.diseasegrade}\n\n计算用时：{self.time}\n\nfps：{self.fps}')


        if(self.workmode==5):
            if self.text not in RicePestsIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'水稻\n\n虫害情况：{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if self.workmode==6:
            if self.text not in FruitStateIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')

        if self.workmode == 7:
            if self.text not in FruitTypesIndex:
                self.text = 'getting...'
                self.fps = 'getting...'
                self.time = 'getting...'
            self.resulttext.setText(f'{self.text}\n\n计算用时：{self.time}\n\nfps：{self.fps}')


    def ShowPhotoButtonPressed(self):

        self.box = PhotoBox(self)
        self.box.showFullScreen()
        self.box.show()
        self.isRun = False
        pass

    def ClearTips(self):

        self.SetButtonIcon(self.ShowTipsButton,"UI/images/icon/tipsoff.svg",48,48)

        self.TipsLabel.hide()
        self.ShowTipsButton.setEnabled(False)
        self.TipsLabel.setText("")


    def FruitButtonPressed(self):
        lock = False

        self.ClearTips()

        self.text= 'getting...'
        self.time= 'getting...'
        self.fps = 'getting...'

        if self.workmode == 6:
            self.workmode = 7
            lock = True

        if self.workmode == 3 or self.workmode==0:
            self.workmode = 6
            lock = True

        if self.workmode==7 and not lock:
            self.workmode =6
            lock = True

    def ReverseButtonPressed(self):

        if self.isRun:
            if self.wthread:
                while self.CapIsbasy:
                    pass

                self.wthread.stop()
                self.wthread2.stop()

                if self.cap.isOpened():
                    self.cap.release()
                    self.CapIsbasy = False

                self.isRun = False

        if(self.url == 0):
            self.url = 'rtsp://192.168.123.106:554/user=admin&password=admin&channel=1&stream=0.sdp?'
            while self.CapIsbasy:
                pass
            ip = '192.168.123.106'

            if self.system != 'Windows':
                backinfo = os.system('ping -c 2 -w 3 ' + ip)  # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
            else:
                backinfo = os.system('ping -n 2 -w 3 ' + ip)  # 实现pingIP地址的功能，-n1指发送报文一次，-w1指等待1秒

            if backinfo:
                print(backinfo)
                self.url = 0
            else:
                print(backinfo)
        else:
            self.url = 0

        self.cap = cv2.VideoCapture(self.url)

        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,HIGHT)

        self.StartShowVideo()

        pass



    def wheatButtonPressed(self):

        self.ClearTips()

        if self.workmode >=3:
            self.text= 'getting...'
            self.time= 'getting...'
            self.fps = 'getting...'
        if self.workmode == 3 or self.workmode==6 or self.workmode == 7:
            self.workmode = 0

        if self.workmode == 4:
            self.workmode = 1

        if self.workmode == 5:
            self.workmode = 2




    def riceButtonPressed(self):

        self.ClearTips()

        if self.workmode <3:
            self.text= 'getting...'
            self.time= 'getting...'
            self.fps = 'getting...'

        if self.workmode == 0  or self.workmode==6 or self.workmode == 7:
            self.workmode = 3
        if self.workmode==1:
            self.workmode = 4
        if self.workmode == 2:
            self.workmode = 5




    def exitButtonPressed(self):
        self.ClearTips()
        if self.isRun:
            if self.wthread:
                self.wthread.stop()
                self.wthread2.stop()


            self.isRun=False

        while self.CapIsbasy:
            pass

        self.cap.release()



        self.CapIsbasy=False
        self.close()





class MapBox(QMainWindow,Ui_WheatherWindow):
    def __init__(self):
        super(MapBox, self).__init__(None)

        self.wheather = get_wheather ()
        self.setupUi(self)
        self.UpdateUi()
        self.exitButton.clicked.connect(self.ExitButtonPressed)
        self.wheatherbox.setText(self.wheather[0])

    def UpdateUi(self):



        #退出按钮
        self.SetButtonIcon(self.exitButton, "UI/images/btn_back_r_normal.png", 128, 64)

        #状态栏
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)

        self.head.setFont(font)

        self.head.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                "QLabel:hover{color:rgb(100,100,100,120);}")


        #设置背景
        # self.gif = QMovie("UI/images/backgroundpic.gif")
        #
        # self.backgroundlabel.setMovie(self.gif)
        #
        #
        # # self.backgroundlabel.showFullScreen()
        # #
        # # self.backgroundlabel.setFixedSize(QSize(1920,1080))
        #
        # self.gif.start()

        self.backgroundlabel.setPixmap(QPixmap("UI/images/backgroundpic.png"))
        self.backgroundlabel.setScaledContents(True)

        #self.backgroundlabel.showFullScreen()
        #self.backgroundlabel.autoFillBackground()

        self.setStyleSheet("#MapWindow{border-image:url(UI/images/backgroundpic.png);}")


        #视频UI

        self.PictureLabel.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件

        self.PictureLabel.setStyleSheet("QLabel{background:rgb(255,255,255,60);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")
        self.PictureLabel.setPixmap(QPixmap('UI/images/yzumap.png'))


        #self.Map.load(QUrl('https://zhaosiyi.github.io/demo/?tdsourcetag=s_pcqq_aiomsg'))

        self.pictureLabelbackground.setAutoFillBackground(True)

        self.pictureLabelbackground.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        # 结果显示框
        self.wheatherbox.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                        "QLabel:hover{color:rgb(100,100,100,120);}")


        self.wheatherbox.setText("YZU-灵听者：\n包飞霞\r刘源\n牛恺锐\r薛鹏")

    def SetButtonIcon(self,buttonobj,path,width,hight):
        #拍照按钮
        pixmap = QPixmap(QImage(path))

        fixpixmap = pixmap.scaled(width, hight, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)

        icon = QIcon(fixpixmap)


        buttonobj.setIcon(icon)

        buttonobj.setIconSize(QSize(width, hight))

        buttonobj.setFlat(True)

        buttonobj.setStyleSheet("border:none")

    def ExitButtonPressed(self):
        self.close()


class PhotoBox(QMainWindow,Ui_PhotoWindow):

    def __init__(self,vw):
        super(PhotoBox, self).__init__(None)

        self.trantext = ''
        self.temp = 0.0
        self.humi = 0.0
        self.vw = vw

        # 设置界面
        self.setupUi(self)

        self.UpdateUi()

        self.SetButtonConnected()



        if platform.system() == "Windows":
            rootpath = 'C:/Python Code/MaturityRecognition/'
        else:
            rootpath = '/system/ftproot/aa/MaturityRecognition/'

        self.filePath = rootpath+'camera/'

        self.piclist = os.listdir(self.filePath)
        self.piclistlen = len(self.piclist)

        print (self.piclist)
        print(self.piclistlen)

        self.picindex = 0


        if self.piclistlen!=0:
            self.pic = QtGui.QPixmap(self.filePath+self.piclist[0])
            self.resulttext.setText(self.readpicname(self.piclist[self.picindex]))
        else:
            self.pic = QtGui.QPixmap(rootpath+'UI/images/nopic.svg')
            self.resulttext.setText('No Picture.')

        self.pictureLabel.setPixmap(self.pic)

        self.pictureLabel.setScaledContents(True)





    def SetButtonConnected(self):


        self.exitButton.clicked.connect(self.exitButtonPressed)

        self.leftButton.clicked.connect(self.leftButtonPressed)

        self.rightButton.clicked.connect(self.rightButtonPressed)

        self.deleteButton.clicked.connect(self.DeleteButtonPressed)

    def UpdateUi(self):

        self.exitButton.setStyleSheet("border:none")

        # 退出按钮
        self.SetButtonIcon(self.exitButton,"UI/images/btn_back_r_normal.png",128,64)


        #左按钮
        self.SetButtonIcon(self.leftButton, "UI/images/icon/left.svg", 64, 64)

        #右按钮
        self.SetButtonIcon(self.rightButton, "UI/images/icon/right.svg", 64, 64)
        #删除
        self.SetButtonIcon(self.deleteButton, "UI/images/icon/delete.svg", 64, 64)

        self.deleteButton.setStyleSheet("QPushButton{background:rgb(255,255,255,100);}"
                                       "QPushButton:hover{color:rgb(100,100,100,120);}")
        # 状态栏
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)

        self.head.setFont(font)

        self.head.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                "QLabel:hover{color:rgb(100,100,100,120);}")

        # 设置背景
        # self.gif = QMovie("UI/images/backgroundpic.gif")
        #
        # self.backgroundlabel.setMovie(self.gif)
        #
        # self.gif.start()
        self.backgroundlabel.setPixmap(QPixmap("UI/images/backgroundpic.png"))

        self.backgroundlabel.setScaledContents(True)

        self.setStyleSheet("#VideoWindow{border-image:url(UI/images/backgroundpic.png);}")

        # 视频UI
        self.pictureLabel.setAutoFillBackground(True)  # 设置背景充满，为设置背景颜色的必要条件

        self.pictureLabel.setStyleSheet("QLabel{background:rgb(255,255,255,60);}"
                                        "QLabel:hover{color:rgb(100,100,100,120);}")

        self.pictureLabelbackground.setAutoFillBackground(True)

        self.pictureLabelbackground.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                                  "QLabel:hover{color:rgb(100,100,100,120);}")

        # 结果显示框
        self.resulttext.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                                      "QLabel:hover{color:rgb(100,100,100,120);}")

        # 设置文本框
        pixmap = QPixmap("UI/images/yzu.png")
        self.schoolbadge.setPixmap(pixmap)

        self.schoolbadge.setScaledContents(True)

        self.teammumber.setText("YZU-灵听者：\n包飞霞\r刘源\n牛凯瑞\r薛鹏")

        self.frameID = 0
        self.wthread5 = None
        self.wthread5 = ThreadUpdatPhoto(self)
        self.wthread5.updatephoto.connect(self.updatephoto)
        self.wthread5.start()

    def SetButtonIcon(self,buttonobj,path,width,hight):

        pixmap = QPixmap(QImage(path))

        fixpixmap = pixmap.scaled(width,hight,QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)

        icon = QIcon(fixpixmap)

        buttonobj.setIcon(icon)

        buttonobj.setFlat(True)

        buttonobj.setIconSize(QSize(width,hight))

    def updatephoto(self):

        self.currenttime = str(datetime.datetime.now())

        if self.temp != None and self.humi != None and self.ph != None:
            # self.head.setText('\t'+self.currenttime[0:19]+'  温度：'+str(self.temp)[0:5]+'°C'+"  湿度："+str(self.humi)[0:7]+'%'+'  PH:'+str(self.ph))
            self.head.setText(f'    {self.currenttime[0:19]}    温度：  {str(self.temp)[0:5]}°C    湿度：  {str(self.humi)[0:7]}%    PH:  {str(self.ph)}')
        else:
            #self.head.setText('\t' + self.currenttime[0:19] + '  温度：Error' + "  湿度：Error"+'PH:Error' )
            self.head.setText(f'    {self.currenttime[0:19]}    温度：Error    湿度：Error  PH:Error')

    def leftButtonPressed(self):

        if self.piclistlen!=0:

            if self.picindex==0:
                self.picindex = self.piclistlen-1
            else:
                self.picindex -= 1

            self.pic = QtGui.QPixmap(self.filePath + self.piclist[self.picindex])

            self.pictureLabel.setPixmap(self.pic)

            self.pictureLabel.setScaledContents(True)

            self.resulttext.setText(self.readpicname(self.piclist[self.picindex]))
        else:
            self.pictureLabel.setPixmap(QPixmap('UI/images/nopic.svg'))
    def rightButtonPressed(self):
        if self.piclistlen != 0:
            self.picindex += 1

            if self.picindex >self.piclistlen-1:
                self.picindex = 0

            self.pic = QtGui.QPixmap(self.filePath + self.piclist[self.picindex])

            self.pictureLabel.setPixmap(self.pic)

            self.pictureLabel.setScaledContents(True)

            self.resulttext.setText(self.readpicname(self.piclist[self.picindex]))
        else:
            self.pictureLabel.setPixmap(QPixmap('UI/images/nopic.svg'))

    def DeleteButtonPressed(self):

        if platform.system() == "Windows":
            rootpath = 'C:/Python Code/MaturityRecognition/camera'
        else:
            rootpath = '/system/ftproot/aa/MaturityRecognition/camera'
        if self.piclistlen!= 0:
            os.remove(os.path.join(rootpath, self.piclist[self.picindex]))
            print("Delete File: " + os.path.join(rootpath, self.piclist[self.picindex]))  # 控制台输出，查看删除了哪些图片
        else:
            self.pictureLabel.setPixmap(QPixmap('UI/images/nopic.svg'))
            print('Not Found Any Pic!')
            self.resulttext.setText('No Picture.')

        if platform.system() == "Windows":
            rootpath = 'C:/Python Code/MaturityRecognition/'
        else:
            rootpath = '/system/ftproot/aa/MaturityRecognition/'

        self.filePath = rootpath+'camera/'

        self.piclist = os.listdir(self.filePath)

        self.piclistlen = len(self.piclist)

        if self.piclistlen == 0:
            self.resulttext.setText('No Picture.')
        self.rightButtonPressed()

        pass
    def readpicname(self,picname):

        name = ''
        state = ''
        time = ''
        lockname = False
        lockstate = False
        locktime = False

        for s in picname:
            if s!= ':' and lockname != True:
                name = name+s
            else:
                lockname = True
                if s != '-' and lockstate != True:
                    if s!= ':':
                        state = state + s
                else:
                    lockstate = True
                    if s != '.':
                        if s == '-' and locktime !=True:
                            locktime = True
                            continue
                        else:
                            time = time +s
                    else:
                        break

        if name == 'Rice':
            name = '水稻'
            if state == 'Growing period':
                state = "成熟度：生长期"

            elif state == 'Leaf function or greening period':
                state = "成熟度：叶功能/返青期"

            elif state == 'Maturity':
                state = "成熟度：成熟期"

            elif state == 'Health':
                state = '病害情况：健康'
            elif state == 'Blight':
                state = "病害情况：枯纹病"
            elif state == 'Bugs':
                state = '虫害情况:有'

        elif name == 'Wheat' :
            name = '小麦'
            if state == 'Maturity':
                state = '成熟度：成熟期'
            elif state =='Grouting period':
                state = '成熟度：灌浆期'
            elif state =='Growing period':
                state ='成熟度：生长期'

            elif state == 'Health':
                state = '病害情况：健康'
            elif state == 'Rust':
                state = "病害情况：条锈病"
            elif state == 'powdery mildew':
                state = "病害情况：白粉病"

            elif state == 'Is_Buds':
                state = '虫害情况:有虫害'


        elif name == 'apples':
            name = '苹果'
        elif name == 'banana':
            name = '香蕉'
        elif name == 'orange':
            name = '橘子'
        else:
            name = 'Error'

        if state == 'fresh':
            state = '新鲜'
        elif state == 'rotten':
            state = '坏的'

# ###################################################
#         if platform.system() == 'Windows':
#             name = '水稻'
#             state = "成熟期"
#             time = '20200810'
# ##################################################

        if name != 'Error' and state != 'Error':
            if state == '新鲜' or state == '坏的':
                str = f'{name}:{state}\n\n记录时间:{time}'
            else:
                str = f'{name}：\n\n{state}\n\n记录时间:{time}'
        else:
            str = 'Error'

        return str

    def showpic(self):
        pass
        # self.pictureLabel.setPixmap(self.showImage)
        # self.pictureLabel.setScaledContents(True)

    def showresult(self):
        pass



    def exitButtonPressed(self):
        if self.wthread5:
            self.wthread5.stop()
        self.vw.isRun = True
        self.close()




from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

class ChartBox(QMainWindow,Ui_ChartWindow):
    def __init__(self):

        super(ChartBox, self).__init__(None)


        self.temp = 0.0
        self.itemp = 0.0
        self.humi = 0.0
        self.ph = 0.0
        self.workmode = 1


        self.maxtemp = 0.0
        self.mintemp = 0.0

        self.avetemp = 0.0

        self.maxhumi = 0.0
        self.minhumi = 0.0
        self.avehumi = 0.0

        self.setupUi(self)

        self.UpdataUI()

        self.leftButton.clicked.connect(self.LeftButtonPressed)
        self.rightButton.clicked.connect(self.RightButtonPressed)

        plt.rcParams['font.sans-serif'] = ['FangSong']
        plt.rcParams['axes.unicode_minus'] = False


        self.x = []  #建立空的x轴数组和y轴数组
        self.y = []
        self.z = []
        self.n = 0

        self.dynamic_showchart = self.dynamic_canvas.figure.subplots()
        if platform.system() =='Windows':
            self.workmode = 0
        else:
            self.workmode = 1
        self.inittimer()
        self._timer.start()
        self.showchart()



        self.frameID = 0
        self.wthread4 = None
        self.wthread4 = ThreadUpdateChart(self)
        self.wthread4.updatechart.connect(self.UpdateChart)
        self.wthread4.start()

        self.exitButton.clicked.connect(self.ExitButtonPressed)


    def inittimer(self):

        if self.workmode ==0:
            self._timer = self.dynamic_canvas.new_timer(
                1000, [(self.showchart, (), {})])
        elif self.workmode ==1:
            self._timer = self.dynamic_canvas.new_timer(
                60000, [(self.showchart, (), {})])
        elif self.workmode == 2:
            self._timer = self.dynamic_canvas.new_timer(
                3600000, [(self.showchart, (), {})])

    def UpdateChart(self):

        self.currenttime = str(datetime.datetime.now())

        if self.temp != None and self.humi != None and self.ph != None:
            # self.head.setText('\t'+self.currenttime[0:19]+'  温度：'+str(self.temp)[0:5]+'°C'+"  湿度："+str(self.humi)[0:7]+'%'+'  PH:'+str(self.ph))
            self.head.setText(f'    {self.currenttime[0:19]}    温度：  {str(self.temp)[0:5]}°C    湿度：  {str(self.humi)[0:7]}%    PH:  {str(self.ph)}')
        else:
            #self.head.setText('\t' + self.currenttime[0:19] + '  温度：Error' + "  湿度：Error"+'PH:Error' )
            self.head.setText(f'    {self.currenttime[0:19]}    温度：Error    湿度：Error  PH:Error')



    def UpdataUI(self):

        self.dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))



        self.layout = QtWidgets.QVBoxLayout(self.showchartlabel)


        self.layout.addWidget(self.dynamic_canvas)

        self.head.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        self.backlabel.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")

        self.showchartlabel.setStyleSheet("QLabel{background:rgb(255,255,255,100);}"
                           "QLabel:hover{color:rgb(100,100,100,120);}")



        #退出按钮
        self.SetButtonIcon(self.exitButton,"UI/images/btn_back_r_normal.png",128,64)


        #左按钮
        self.SetButtonIcon(self.leftButton, "UI/images/icon/left.svg", 64, 64)

        #右按钮
        self.SetButtonIcon(self.rightButton, "UI/images/icon/right.svg", 64, 64)

        #设置背景
        # self.gif = QMovie("UI/images/backgroundpic.gif")
        #
        # self.backgroundlabel.setMovie(self.gif)
        #
        # self.gif.start()

        self.backgroundlabel.setPixmap(QPixmap("UI/images/backgroundpic.png"))

        self.backgroundlabel.showFullScreen()

        self.setStyleSheet("#ChartWindow{border-image:url(UI/images/backgroundpic.png);}")



        font = QFont()

        font.setBold(True)
        font.setPointSize(20)

        self.head.setFont(font)

        font.setPointSize(15)

        self.TempLabel.setFont(font)

        self.HumiLabel.setFont(font)

    def SetButtonIcon(self,buttonobj,path,width,hight):

        pixmap = QPixmap(QImage(path))

        fixpixmap = pixmap.scaled(width,hight,QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)

        icon = QIcon(fixpixmap)

        buttonobj.setIcon(icon)

        buttonobj.setFlat(True)

        buttonobj.setIconSize(QSize(width,hight))

    def showchart(self):
        self.n += 1

        if self.workmode == 2:
            if self.n == 24:
                self.n = 0
                self.x = []
                self.y = []
                self.z = []
        else:
            if self.n == 60:
                self.n = 0
                self.x = []
                self.y = []
                self.z = []


        self.dynamic_showchart.clear()

        if self.workmode == 0:
            sec = str(datetime.datetime.now())[17:19]
            sec = int(sec)
            self.timebase = sec

            if platform.system() == 'Windows':
                self.dynamic_showchart.set_ylabel('温度(°C)/湿度(%)')
                self.dynamic_showchart.set_xlabel('时间(秒)')
            else:
                self.dynamic_showchart.set_ylabel('Temp(°C)/Humi(%)')
                self.dynamic_showchart.set_xlabel('Time(sec)')


        elif self.workmode == 1:
            min = str(datetime.datetime.now())[14:16]
            min = int(min)
            self.timebase = min
            if platform.system() == 'Windows':
                self.dynamic_showchart.set_ylabel('温度(°C)/湿度(%)')
                self.dynamic_showchart.set_xlabel('时间(分钟)')
            else:
                self.dynamic_showchart.set_ylabel('Temp(°C)/Humi(%)')
                self.dynamic_showchart.set_xlabel('Time(min)')
        elif self.workmode == 2:
            hour = str(datetime.datetime.now())[11:13]
            hour = int(hour)
            self.timebase = hour
            if platform.system() == 'Windows':
                self.dynamic_showchart.set_ylabel('温度(°C)/湿度(%)')
                self.dynamic_showchart.set_xlabel('时间(小时)')
            else:
                self.dynamic_showchart.set_ylabel('Temp(°C)/Humi(%)')
                self.dynamic_showchart.set_xlabel('Time(hour)')


        self.x.append(self.timebase)

        self.y.append(self.temp)

        self.z.append(self.humi)


        self.maxtemp = float(str(np.max(self.y))[0:5])

        self.mintemp = float(str(np.min(self.y))[0:5])

        self.avetemp = float(str(np.average(self.y))[0:5])

        self.maxhumi = float(str(np.max(self.z))[0:5])

        self.minhumi = float(str(np.min(self.z))[0:5])

        self.avehumi = float(str(np.average(self.z))[0:5])



        humistate = 'None'

        if float(self.avehumi) > 75.0:
            humistate = "湿润"
        elif float(self.avehumi) >= 50.0:
            humistate = "半湿润"
        elif float(self.avehumi) >= 25.0:
            humistate = "半干旱"
        else:
            humistate = "干旱"

        tempstate = 'None'


        if float(self.avetemp) > 40.0:
            tempstate = "超高温"
        elif float(self.avetemp) >= 28.0:
            tempstate = "高温"
        elif float(self.avetemp) >= 14.0:
            tempstate = "温和"
        elif float(self.avetemp) >= 10.0:
            tempstate = "温凉"
        elif float(self.avetemp) >= -10.0:
            tempstate = "低温"
        else:
            tempstate = "超低温"


        humitips = ''
        temptips = ''

        if self.avehumi >= 85:
            humitips = '湿度偏高,易滋生病虫害,影响光合作用。'
        elif self.avehumi <= 20:
            humitips = "湿度较低,易引发干旱,注意及时灌溉。"
        else:
            humitips = "湿度适宜作物生长。"

        hour = int(str(datetime.datetime.now())[11:13])

        if hour >= 0 and hour <= 14:

            if self.avetemp > 23.0 and self.avetemp <= 30:
                temptips = '温度适宜作物生长'
            elif self.avetemp <23.0:
                temptips = '温度偏低'
            elif self.avetemp >30:
                temptips = '温度偏高'

        elif hour > 18:

            if self.avetemp > 23.0 and self.avetemp <= 26:
                temptips = '温度适宜作物生长'
            elif self.avetemp <23.0:
                temptips = '温度偏低'
            elif self.avetemp >26:
                temptips = '温度偏高'

        else:

            if self.avetemp > 18.0 and self.avetemp <= 20:
                temptips = '温度适宜作物生长'
            elif self.avetemp <18.0:
                temptips = '温度偏低'
            elif self.avetemp >20:
                temptips = '温度偏高'


        self.itemp = ((self.maxtemp + self.mintemp)/2.0 -10)



        self.TempLabel.setText(f'当日最高温度：{str(self.maxtemp)[0:5]}°C\n当日最低温度：{str(self.mintemp)[0:5]}°C\n当日有效积温：{str(self.itemp)[0:5]}°C\n温度状况:{tempstate}\nTips：{temptips}')

        self.HumiLabel.setText(f'当日最高湿度：{str(self.maxhumi)[0:5]}%\n当日最低湿度：{str(self.minhumi)[0:5]}%\n当日平均湿度：{str(self.avehumi)[0:5]}%\n湿度状况:{humistate}\nTips：{humitips}')


        yy = np.array(self.y)

        zz = np.array(self.z)



        self.dynamic_showchart.plot(yy,color='blue',label = 'Tempture')
        self.dynamic_showchart.plot(zz, color='red', label='Humidity')

        self.dynamic_showchart.set_xlim(0,60)
        self.dynamic_showchart.set_ylim(-20, 100)

        self.dynamic_showchart.figure.legend()

        self.dynamic_showchart.figure.canvas.draw()

    def LeftButtonPressed(self):

        self.itemp = 0.0
        self._timer.stop()
        self.workmode -= 1
        if self.workmode <0:
            self.workmode = 2

        self.dynamic_showchart.clear()

        self.n = 0
        self.x = []
        self.y = []
        self.z = []

        self.inittimer()
        self._timer.start()

        self.showchart()


    def RightButtonPressed(self):

        self.itemp = 0.0
        self._timer.stop()
        self.dynamic_showchart.clear()

        self.workmode += 1
        if self.workmode >=3:
            self.workmode = 0


        self.n = 0
        self.x = []
        self.y = []
        self.z = []

        self.inittimer()
        self._timer.start()
        self.showchart()


    def ExitButtonPressed(self):
        print('exit')
        self._timer.stop()
        if self.wthread4:
            self.wthread4.stop()
        self.close()



