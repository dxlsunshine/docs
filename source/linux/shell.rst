系统相关
+++++++++

BASH
------

 1. 清空文件：>file
 2. 读文件并赋值变量：var=$(<file)，忽略文件最后一个换行。
 3. BASH_REMATCH

     bash 3.0 支持进程内正则表达式 [[ string =~ regex ]]

      .. code-block::  bash
       
      
       if [[ 'abcfoobarbletch' =~ foo(bar)bl(.*) ]]
        then
          echo The regex matches!
          echo $BASH_REMATCH       # -- outputs: foobarbletch
          echo ${BASH_REPAMTCH[*]} #-- outputs: foobarbletch bar etch
          echo ${BASH_REMATCH[1]}  #-- outputs: bar
          echo ${BASH_REMATCH[2]}  #-- outputs: etch
       fi


 4. 括号
     
     - **()** 

       | 命令组。括号中的命令将会新开一个子shell顺序执行，所以括号中的变量不能够被脚本余下的部分使用。括号中多个命令之间用分号隔开，最后一个命令可以没有分号，各命令和括号之间不必有空格;
       | 命令替换。等同于`cmd`，shell扫描一遍命令行，发现了$(cmd)结构，便将$(cmd)中的cmd执行一次，得到其标准输出，再将此输出放到原来命令。有些shell不支持，如tcsh; 
       | 用于初始化数组。如：array=(a b c d). 
     - **(())** 

       | 整数扩展。这种扩展计算是整数型的计算，不支持浮点型。((exp))结构扩展并计算一个算术表达式的值，如果表达式的结果为0，那么返回的退出状态码为1，或者 是"假"，而一个非零值的表达式所返回的退出状态码将为0，或者是"true"。若是逻辑判断，表达式exp为真则为1,假则为0;
       | 只要括号中的运算符、表达式符合C语言运算规则，都可用在$((exp))中，甚至是三目运算符。作不同进位(如二进制、八进制、十六进制)运算时，输出结果全都自动转化成了十进制。如：echo $((16#5f)) 结果为95 (16进位转十进制);
       | 单纯用 (( )) 也可重定义变量值，比如 a=5; ((a++)) 可将 $a 重定义为6; 
       | 常用于算术运算比较，双括号中的变量可以不使用$符号前缀。括号内支持多个表达式用逗号分开。 只要括号中的表达式符合C语言运算规则,比如可以直接使用for((i=0;i<5;i++)), 如果不使用双括号, 则为for i in \`seq 0 4\`或者for i in {0..4}。再如可以直接使用if (($i<5)), 如果不使用双括号, 则为if [ $i -lt 5 ]。

     - **[]**

       | bash 的内部命令，[]和test是等同的。
       | Test和[]中可用的比较运算符只有==和!=，两者都是用于字符串比较的，不可用于整数比较，整数比较只能使用-eq，-gt这种形式。无论是字符串比较还是整数比较都不支持大于号小于号。
     - **[[]]**

       | bash 程序语言的关键字。并不是一个命令，[[ ]] 结构比[ ]结构更加通用。在[[和]]之间所有的字符都不会发生文件名扩展或者单词分割，但是会发生参数扩展和命令替换。
       | 支持字符串的模式匹配，使用=~操作符时甚至支持shell的正则表达式。字符串比较时可以把右边的作为一个模式，而不仅仅是一个字符串，比如[[ hello == hell? ]]，结果为真。[[ ]] 中匹配字符串或通配符，不需要引号。

     - **{}**

       | 大括号拓展  # ls {ex1,ex2}.sh 
       | 代码块，又被称为内部组,这个结构事实上创建了一个匿名函数.
  
nsenter
''''''''
 ..code-block:: bash

  nsenter [options] [program [arguments]]
    options:
    -t, --target pid：指定被进入命名空间的目标进程的pid
    -m, --mount[=file]：进入mount命令空间。如果指定了file，则进入file的命令空间
    -u, --uts[=file]：进入uts命令空间。如果指定了file，则进入file的命令空间
    -i, --ipc[=file]：进入ipc命令空间。如果指定了file，则进入file的命令空间
    -n, --net[=file]：进入net命令空间。如果指定了file，则进入file的命令空间
    -p, --pid[=file]：进入pid命令空间。如果指定了file，则进入file的命令空间
    -U, --user[=file]：进入user命令空间。如果指定了file，则进入file的命令空间
    -G, --setgid gid：设置运行程序的gid
    -S, --setuid uid：设置运行程序的uid
    -r, --root[=directory]：设置根目录
    -w, --wd[=directory]：设置工作目录
    #如果没有给出program，则默认执行$SHELL。


系统参数
--------

/proc/sys/fs/file-max：The value in file-max denotes the maximum number of file-handles that the Linux kernel will allocate. When you get lots of error messages about running out of file handles, you might want to increase this limit
/proc/sys/fs/file-nr：当前打开文件数   剩余 最大
cat /proc/sys/fs/nr_open： 单进程允许最大打开文件数
nofile: number of open files 最大可打开文件数，限制范围：用户和进程


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

 - lsof

   .. code-block:: bash
     
    lsof abc.txt                      #显示开启文件abc.txt的进程
    lsof -c abc                       #显示abc进程现在打开的文件
    lsof -c -p 1234,234               #列出进程号为1234的进程所打开的文件
    lsof -g gid                       #显示归属gid的进程情况
    lsof +d /usr/local/               #显示目录下被进程开启的文件
    lsof +D /usr/local/               #同上，但是会搜索目录下的目录，时间较长
    lsof -d 4                         #显示使用fd为4的进程
    lsof -i                           #用以显示符合条件的进程情况
    lsof -t                           #显示进程号，可以和kill配合使用
    lsof -i[46] [protocol][@hostname|hostaddr][:service|port]
    
     #COMMAND 
     #PID      
     #USER   
     #FD      File Descriptor, an abstract indicator for accessing of files. 
     #   cwd stands for Current Working Directory of the listed process. 
     #   txt is the Text Segment or the Code Segment (CS), the bit of the object containing executable instructions, or program code if you will. 
     #   mem stands for Data Segments and Shared Objects loaded into the memory. 
     #   10u refers to file descriptor 10, open for both reading and writing. 
     #   rtd stands for root directory.

     #TYPE    TYPE is directly linked to the FD column.It tells us what type of file we're working with.
     #   DIR stands for directory. 
     #   REG is a regular file or a page in memory. 
     #   FIFO is a named pipe. Symbolic links, sockets and device files (block and character) are also file types. 
     #   unknown means that the FD descriptor is of unknown type and locked. You will encounter these only with kernel threads.

     #DEVICE  The DEVICE column tells us what device we're working on. The two numbers are called major and minor numbers. The list is well known and documented.
     #   major number 8 stands for SCSI block device. 
     #   For comparison, IDE disks have a major number 3. The minor number indicates one of the 15 available partitions. Thus (8,1) tell us we're working on sda1.

     #SIZE/OFF   the file size.
     #NODE       the Inode number.
     #NAME       the name of the file.   
     

 - strace

   .. code-block:: bash

       #查看进程stdout
       strace -ewrite -p $PID
       strace -ewrite -p $PID 2>&1 | grep 'write(1,'   
   
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

dev设备查看
------------
  - 磁盘mapper关系查看
     
    .. code-block:: bash

       #查看device和mapper设备的（Major, minor）
       ls -al /dev/sd*
       dmsetup ls --tree
