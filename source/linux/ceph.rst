Ceph
=====

系统架构
--------


 1. 最底层基于RADOS（reliable，autonomous，distributed object store），其内部包括ceph-osd后台服务进程和ceph-mon监控进程。

 2. 中间层librados库用于本地或者远程通过网络访问RADOS对象存储系统。

 3. 最上层面向应用提供3种不同的存储接口：块存储接口、对象存储接口、文件系统接口。文件系统的元数据服务器MDS用于提供元数据访问。数据直接通过librados库访问。

  .. image:: images/ceph _architecture.jpg



Ceph概念
-----------

 - OSD(Object Storage Device)

 - PG (placement group)

 - Object

 - Pool

 .. image:: images/ceph1.png


基本组件
---------

 **RADOS** 主要由两种节点组成：一种是为数众多的、负责完成数据存储和维护功能的OSD（Object Storage Device），另一种则是若干个负责完成系统状态检测和维护的monitor。

   - Osd
      用于集群中所有数据与对象的存储。处理集群数据的复制、恢复、回填、再均衡。并向其他osd守护进程发送心跳，然后向Mon提供一些监控信息。当Ceph存储集群设定数据有两个副本时（一共存两份），则至少需要两个OSD守护进程即两个OSD节点，集群才能达到active+clean状态。
  
   - Mds
      为Ceph文件系统提供元数据计算、缓存与同步。在ceph中，元数据也是存储在osd节点中的，mds类似于元数据的代理缓存服务器。MDS进程并不是必须的进程，只有需要使用CEPHFS时，才需要配置MDS节点。
  
   - Monitor
      监控整个集群的状态，维护集群的cluster MAP二进制表，保证集群数据的一致性。ClusterMAP描述了对象块存储的物理位置，以及一个将设备聚合到物理位置的桶列表。 
