# designed by CZH powered by [Hu Jianrong](https://github.com/capacitanceHu)

## celery-beat

程序启动，从pgsql中获得有效的mission列表，其中时间crontab为json格式，任务实体从MissionInterface中拿。

以后的效果就是，通过数据库更新Mission，重启beat即更新生效。

**关于redbeat**

redbeat的思路和上面类似，区别在于，通过redbeat，可以通过一个API来更新beat的数据。如何更新，和上面一样。

## MissionInterface（File）

1. 获取可用的Mission和Missionary
2. 获取可用的Mission_id
3. 根据mission id，启动MissionEngine，运行Missionary。

## Mission（ORM）

Mission起的是记录作用，负责组合一系列Task和最终的Target，比如买入卖出等等。字段包括id，一个任务队列，是否可用，can_run_before_each_task，can_run_before_aim，target（前面三个也都是Task）等等。

## Missionary（ORM）

Missionary记录着Mission的一次运行情况，字段包括mission_id，执行的周期（目前都是每小时执行），进行到哪一个了（在redis中做一个缓存），是否结束，什么时候开始的，什么时候结束的。Mission的结果。

Missionary的在运行的不同时刻有不同的运行周期，和当前的Task保持同步。（当前的Task的周期就是Missionary的周期）

Missionary结束的标志是完成了最终的Target。

## MissionEgine（Class）

MissionEgine操作着Missionary的运行。

Missionary运行的时候，判断的流程为can_run_before_each_task——》判断当前时间是否可以跑这个task——》task.can run——》task.try_pass。如果某一步不行直接结束自己的生命周期。跑过了就更新run index的缓存，同下一个task和missionry的运行。对下一个task重复上述步骤。

Missionary的所有Task都通过task id向TaskInterface要。

**判断当前时间是否可以跑这个task**，规则为，如果相同，直接跑，如果不相同，更新missionary的run time。然后判断当下是否可以跑。如果has run time set为空，或其中有一个小于task.run time，则跑，否则不跑。这样保证了[60min，1min，60min]可以跑，[60min, 4h]不可以跑。

## TaskInterface（File）

1. 根据Task id，获得对应的Task以及对应的TaskTemplate，并组装好给别人。
2. 根据Task id，获得对应的运行时间。

## TaskEngine（Class）

Task储存了运行的参数，TaskTemplate相当于运行的参数。TaskEngine就是把Task和TaskTemplate组合起来，提供了can_run和try_pass，返回Result对象。

在TaskEngine中，运行结束了就要保存ResultLog。因为要生成result，需要知道运行的环境，也就是mission的一些信息，所以TaskEngine在run之前，需要得到Mission的实例来获取信息，get_info_from_mission

## TaskTemplate（Folder/Function）

TaskTemplate是Task的模板，这些模块定义了计算规则，这个写死在代码中，但是这些模板要暴露给外部，通过在数据库中定义一些参数比如交易对，时间间隔等，实现这些task的实例化。也就是，Task的Json转给对应的TaskTemplate函数，就可以运行了。

返回的参数包括passed（bool），rule，msg_format，msg_args。

Task的有几种类型，包括计算之后的数据的比对（data），完成某个交易（trade），设置某个条件（condition），以及mix（混合）。这意味着task之间可以相互组合，成为更加高级的task。而Task最主要的目的就是运行并返回是否成功。即 run & return True/False。

在数据比对这一块，数据的获得都在Data模块中，而TaskTemplate主要负责比对。

## Data

## Task（ORM）

Task是一个model类，通过记录下TaskTemplate和一些参数，可以供TaskEngine运行起来。（这个类本身不负责组装）

Task的参数包括TaskTemplate-name（str，一个类的名字），运行参数（以json形式保存，比如match，time-interval），can_run的判断（str，是一个函数的名字），执行的周期（目前都是每小时执行）

## Data（Model）

有关数据这一块的，主要包括两个问题，一个是获取，一个是计算。

关于获取这一块，主要的参数就是交易对，size，时间粒度。

关于计算这一块，其实就是加减乘除。计算应该专注于计算的规则，而不关注数据的来源。

对外的接口包括获取数据和计算。提供简单易用的接口。主要的参数就是交易对，size，时间粒度。获取的数据主要包括布林上轨、布林下轨、交易量、均价，ma20。在获取参数时也要参数检查。

## Result（Class）

result记录着一次task运行完的结果。字段包括missionary_id，task_name，is_pass，msg。此外还两个不计入数据库的字段：type，rule。rule完整仿照task，msg由msg_format和msg_args组合形成。type是被程序用的，包括CANTRUN，DEFAULT等等。只有NORMAL这种才会被记录进数据库。

## ResultLog（ORM）

这是ORM，其根据Result生成对应的记录，也需要Missionary来添加一点信息（Mission id）。

## Timer

由于Task和Mission都有关于运行周期的概念，那么我们就将这一块给独立出来，显示给用户的是有限的str，而这些str对应了crontab或者interval，并可以比较大小等。

## Todo

1. Task和Missionary的时间变动还不能热更新到定时任务上
2. schedule和missionary还是要拆开来，两个模块的interface耦合有点深，schedule应该作为一个工具模块来使用
3. mission和missionary的概念的梳理，优化命名
4. 一键化部署
5. 增加测试用例
6. mission和missionary的概念的梳理，减少查表次数
7. 定制化管理界面，增加提示信息，修改CSS样式
