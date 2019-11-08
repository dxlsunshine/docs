系统相关
+++++++++


SSH 协议
--------

 SSH协议是建立在不安全的网络之上的进行远程安全登陆的协议。它是一个协议族，其中有三个子协议，分别是：

 - 传输层协议 [SSH-TRANS]: 提供 服务器 验证、完整性和保密性功能,建立在传统的TCP/IP协议之上。
 - 验证协议[SSH-USERAUTH]: 向服务器验证客户端用户，有基于用户名密码和公钥两种验证方式，建立在传输层协议 [SSH-TRANS] 之上。
 - 连接协    [SSH-CONNECT: 将加密隧道复用为若干逻辑信道。它建立在验证协议之上。

  .. image:: images/ssh1.png

 **握手过程:**

  .. image:: images/ssh2.png

 - 三次握手

  .. image:: images/ssh_cap1.png
    
 - 协议交换

  .. image:: images/ssh_cap2.png
    
 - 密钥交换

  .. image:: images/ssh_cap3.png
    

SSH 免密
---------
 
 - 服务端配置

    生成公钥和私钥:ssh-keygen -t rsa 
 
 - 客户端端配置

    | 创建目录:/root/.ssh/
    | 将发送端公钥复制到此目录下，并重命名为authorized_keys
 
 .. code-block:: bash
 
   #使用ssh_copy
   ssh-copy-id -i .ssh/id_rsa.pub  用户名字@192.168.x.xxx
 
 -  SSH批量免密

   .. literalinclude:: ssh_auto.sh
      :language: bash
      :emphasize-lines: 9
      :linenos:


磁盘IO测试
----------


 .. code-block:: bash

  #使用ssh_copy
  ssh-copy-id -i .ssh/id_rsa.pub  用户名字@192.168.x.xxx
  #!/bin/bash
  #随机写:
  fio -filename-/dev/sda1 -direct-1 -iodepth 1 -thread -rw-randwrite -ioengine-psync -bs-4k -size-2G -numjobs-10 -runtime-60 -group_reporting -name-mytest
  #随机读:
  fio -filename-/2G.fille  -direct-1 -iodepth 1 -thread -rw-randread -ioengine-psync -bs-16k -size-2G -numjobs-10 -runtime-60 -group_reporting -name-mytest
  #混合读写:
  fio -filename-/2G.fille -direct-1 -iodepth 1 -thread -rw-randrw -rwmixread-70 -ioengine-psync -bs-16k -size-2G -numjobs-10 -runtime-60 -group_reporting -name-mytest -ioscheduler-noop


 **参数说明:**

 ==================           ========================================================
 filename-/dev/sdb1           测试文件名称，通常选择需要测试的盘的data目录。
 direct-1                     测试过程绕过机器自带的buffer。使测试结果更真实。
 rw-randwrite                 测试随机写的I/O
 rw-randrw                    测试随机写和读的I/O
 bs-16k                       单次io的块文件大小为16k
 bsrange-512-2048             同上，提定数据块的大小范围
 size-5g                      本次的测试文件大小为5g，以每次4k的io进行测试。
 numjobs-30                   本次的测试线程为30.
 runtime-1000                 测试时间为1000秒，如果不写则一直将5g文件分4k每次写完为止。
 ioengine-psync               io引擎使用pync方式
 rwmixwrite-30                在混合读写的模式下，写占30%
 group_reporting              关于显示结果的，汇总每个进程的信息。
 lockmem-1g                   只使用1g内存进行测试。
 zero_buffers                 用0初始化系统buffer。
 nrfiles-8                    每个进程生成文件的数量。
 ==================           ========================================================
      

进程线程
----------
 - 查看线程

   .. code-block:: bash

      ps -Ledf | grep app1 | wc -l

   ::
     
    　-A   显示所有进程。
    　-d 　显示所有进程，但不包括阶段作业领导者的进程。
    　-e 　此参数的效果和指定"A"参数相同。
    　-f 　显示UID,PPIP,C与STIME栏位。
    　-g 　显示现行终端机下的所有进程，包括群组领导者的进程。
    　 h 　不显示标题列。
    　-j 　采用工作控制的格式显示进程状况。
    　-L 　采用详细的格式来显示进程状况。

查询编辑
----------
 - **Vim**

   .. image:: images/vim.png


 - **sed(编辑)**

    | 以行为单位的文本编辑工具 sed可以直接修改档案。
    | 基本工作方式: sed [-nef] '[动作]' [输入文本]

  :: 
    
    -n   安静模式  一般sed用法中, 来自stdin的数据一般会被列出到屏幕上, 如果使用-n参数后, 只有经过sed处理的那一行被列出来.
    -e   多重编辑  比如你同时又想删除某行, 又想改变其他行, 那么可以用 sed -e '1,5d' -e 's/abc/xxx/g' filename
    -f   首先将sed的动作写在一个档案内, 然后通过 sed -f scriptfile 就可以直接执行 scriptfile 内的sed动作 (没有实验成功, 不推荐使用)
    -i   直接编辑, 这回就是真的改变文件中的内容了, 别的都只是改变显示. (不推荐使用)
    动作:
    a 新增    后面可以接字符串, 而这个字符串会在新的一行出现. (下一行)
    c 取代    后面的字符串, 这些字符串可以取代 n1,n2之间的行
    d 删除    后面不接任何东西
    i 插入    后面的字符串, 会在上一行出现
    p 打印    将选择的资料列出, 通常和 sed -n 一起运作 sed -n '3p' 只打印第3行
    s 取代    类似vi中的取代, 1,20s/old/new/g

  **举例:**

  .. code-block:: bash

    #删除 abc 档案里的第一行, 注意, 这时会显示除了第一行之外的所有行, 因为第一行已经被删除了(实际文件并没有被删除,而只是显示的时候被删除了)
    sed '1d' abc 

    #什么内容也不显示, 因为经过sed处理的行, 是个删除操作, 所以不现实.
    sed -n '1d' abc 

    #abc 删除abc中从第二行到最后一行所有的内容, 注意, $符号正则表达式中表示行末尾, 但是这里并没有说那行末尾, 就会指最后一行末尾, ^开头, 如果没有指定哪行开头, 那么就是第一行开头
    sed '2,$d' 

    只删除了最后一行, 因为并没有指定是那行末尾, 就认为是最后一行末尾
    sed '$d' abc 

    #abc 文件中所有带 test 的行, 全部删除
    sed '/test/d'

    #abc 将 RRRRRRR 追加到所有的带 test 行的下一行 也有可能通过行 sed '1,5c RRRRRRR' abc
    sed '/test/a RRRRRRR' 

    #abc 将 RRRRRRR 替换所有带 test 的行, 当然, 这里也可以是通过行来进行替换, 比如 sed '1,5c RRRRRRR' abc
    sed '/test/c RRRRRRR' 

 - **awk(分析&处理)**

   awk '条件类型1{动作1}条件类型2{动作2}' filename, 

   ::

    awk的处理流程是:
      1. 读第一行, 将第一行资料填入变量 $0, $1... 等变量中
      2. 依据条件限制, 执行动作
      3. 接下来执行下一行
    所以, AWK一次处理是一行, 而一次中处理的最小单位是一个区域
    另外还有3个变量, NF: 每一行处理的字段数, NR 目前处理到第几行 FS 目前的分隔符
    逻辑判断 > < >= <= == !== , 赋值直接使用= 
           
   **举例:**

   .. code-block:: bash
      
     last -n 5 | awk '{print $1 "\t" $3}' 
     #这里大括号内$1"\t"$3 之间不加空格也可以, 不过最好还是加上个空格, 
     #另外注意"\t"是有双引号的, 因为本身这些内容都在单引号内
     #$0 代表整行 $1代表第一个区域, 依此类推

     cat /etc/passwd | awk '{FS=":"} $3<10 {print $1 "\t" $3}' 
     #首先定义分隔符为:, 然后判断, 注意看, 判断没有写在{}中, 然后执行动作, FS=":"这是一个动作, 赋值动作, 不是一个判断, 所以不写在{}中
     #BEGIN END , 给程序员一个初始化和收尾的工作, BEGIN之后列出的操作在{}内将在awk开始扫描输入之前执行, 而END{}内的操作, 将在扫描完输入文件后执行.

     awk '/test/ {print NR}' abc #将带有test的行的行号打印出来, 注意//之间可以使用正则表达式
     #awk {}内, 可以使用 if else ,for(i=0;i<10;i++), i=1 while(i<NF)

 - **grep(截取)**
   
   ::

    -c    只输出匹配的行
    -I    不区分大小写
    -h    查询多文件时不显示文件名
    -l    查询多文件时, 只输出包含匹配字符的文件名
    -n    显示匹配的行号及行
    -v    显示不包含匹配文本的所有行(我经常用除去grep本身)
