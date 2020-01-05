Kubernetes
++++++++++




基础
----

快速命令
''''''''
.. code-block:: bash

   
   pod=mysql
   kubectl logs $(kubectl get pod -A | grep $pod | awk '{print $2}') -nkube-system
   
   #使用nsenter进入容器net空间
   function e() {
    set -eu
    ns=${2-"default"}
    pod=`kubectl -n $ns describe pod $1 | grep -A10 "^Containers:" | grep -Eo 'docker://.*$' | head -n 1 | sed 's/docker:\/\/\(.*\)$/\1/'`
    pid=`docker inspect -f {{.State.Pid}} $pod`
    echo "entering pod netns for $ns/$1"
    cmd="nsenter -n --target $pid"
    echo $cmd
    $cmd
    }

   e podname namespace

configMap
'''''''''

 - 作用

   1. 生成容器环境变量: 环境变量热更新需要更改configMap的version

   .. code-block:: bash
     
     kubectl patch deployment my-configmap  --patch '{"spec": {"template": {"metadata": {"annotations": {"version/config": "20180715" }}}}}'

   2. 设置容器启动命令参数
   3. 挂载配置文件或目录: 热更新无需操作，约1分钟后自动更新,如果设置subPath无法热更新。
  
 - 其它

   1. **subPath** 

      * 目的是为了在单一Pod中多次使用同一个volume而设计的，即设置的path为挂载设备下的目录。
      * 如果subPath(mysql.cnf)与mountPath(/etc/mysql.cnf)子路径相同并且为文件名，表示单独挂载文件。
  

kubernetes dns 解析规则
''''''''''''''''''''''''''
  - pod:  直接访问pod name

  - rs,deploy: 目前测试只能通过service访问，无法直接解析pod

  - stafullset: 可以通过service访问，也可以通过pod.service的访问访问


    .. code-block:: yaml

     #另外pod默认会生成一个label(statefulset.kubernetes.io/pod-name),可以通过selector来匹配并暴露指定pod,如msyql的master节点。
     apiVersion: v1
     kind: Service
     metadata:
       name: app-0
     spec:
       type: LoadBalancer
       selector:
         statefulset.kubernetes.io/pod-name: app-0
       ports:
       - protocol: TCP
         port: 80
         targetPort: 80 

  - daemonset: 目前测试结果同deploy
  
  - headless(service):  通过定义spec:clusterIP: None实现dns轮询查询

POD
'''''''''
  - 容器image

    1. 容器镜像策略(**imagePullPolicy**):

       ============     ====================================
       IfNotPresent     只有当本地没有的时候才下载镜像(默认)
       Always           每次都下载最新的镜像
       Never            只使用本地镜像，从不下载
       ============     ====================================
     
    2. 容器类型

       ==========================            ====================================================================================
       containers                            普通容器
       initContainers                        和普通容器不同: 1. 总是 run to completion   2. 串行执行，当前容器执行完才能下一个。
       ephemeralContainers(alpha)            临时容器
       ==========================            ====================================================================================
    
  - lifecycle
    
    1. PostStart Hook

       该hook在容器被创建后立刻触发；并且无法保证会在容器的ENTRYPOINT之前执行。由于无法保证和容器内其它进程启动的顺序相关联，所以不是应用程序进行启动前配置的最佳解决方案。如果要在应用程序启动前配置系统，可以使用Init Container。Init Container可以按照定义串联执行，并且执行结果可以为后面的Init Container或者主容器所看到
    
    2. PreStop Hook
       
       该hook在容器被删除前触发，由于这个hook是同步执行的，所以必须在容器被删除之前执行完成这个hook。这个Hook是很适合作为应用程序优雅退出的机制的，可以定义一系列的行为来释放容器占有的资源、进行通知和告警来实现优雅退出。

    案例：

    .. literalinclude:: yaml/lifecycle-events.yaml
       :language: yaml
       

GC(垃圾回收)
'''''''''''''
   - **回收时间**

     1. Kubernetes的垃圾回收由kubelet进行管理，每1min会查询清理一次容器，每5min查询清理一次镜像。
     2. 在kubelet刚启动时并不会立即进行GC，即第一次进行容器回收为kubelet启动1min后，第一次进行镜像回收为kubelet启动5min后。


   - **回收范围**
     
     镜像的回收针对node结点上由docker管理的所有镜像，无论该镜像是否是在创建pod时pull的。而容器的回收策略只应用于通过kubelet管理的容器。

   - **回收策略**

    1. kubelet集成的cadvisor进行镜像的回收，有两个参数可以设置：

      ::
     
       --image-gc-high-threshold 当用于存储镜像的磁盘使用率达到百分之--image-gc-high-threshold时将触发镜像回收，删除最近最久未使用（LRU，Least Recently Used）的镜像
       --image-gc-low-threshold  到磁盘使用率降为百分之--image-gc-low-threshold或无镜像可删为止。
       默认--image-gc-high-threshold为85，--image-gc-low-threshold为80。
       不推荐使用其它管理工具或手工进行容器和镜像的清理，因为kubelet需要通过容器来判断pod的运行状态，如果使用其它方式清除容器有可能影响kubelet的正常工作。

    2. pod的回收有三个参数可设置：
      
       .. code-block:: bash 

        --minimum-container-ttl-duration:       #从容器停止运行时起经过--minimum-container-ttl-duration时间后，该容器标记为已过期将来可以被回收（只是标记，不是回收），默认值为1m0s。
        --maximum-dead-containers-per-container #一般情况下每个pod最多可以保留--maximum-dead-containers-per-container个已停止运行的容器集，默认值为2
        --maximum-dead-containers               #整个node节点可以保留--maximum-dead-containers个已停止运行的容器，默认值为100。
        #如果需要关闭容器的垃圾回收策略，可以将--minimum-container-ttl-duration设为0（表示无限制），--maximum-dead-containers-per-container和--maximum-dead-containers设为负数。

        #到达GC时间点时，具体的GC过程如下：
        #1）遍历所有pod，使其满足--maximum-dead-containers-per-container；
        #2）经过上一步后如果不满足--maximum-dead-containers，计算值X=（--maximum-dead-containers）/（pod总数），再遍历所有pod，使其满足已停止运行的容器集个数不大于X且至少为1；
        #3）经过以上两步后如果还不满足--maximum-dead-containers，则对所有已停止的容器排序，优先删除创建时间最早的容器直到满足--maximum-dead-containers为止。

    .. image:: images/kubelet_gc.png


安装
----

使用Kubeadm安装
'''''''''''''''

 - yum repo 配置

   .. code-block:: bash

    cat <<EOF > /etc/yum.repos.d/kubernetes.repo
    [kubernetes]
    name=Kubernetes
    baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
    enabled=1
    gpgcheck=1
    repo_gpgcheck=1
    gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
    exclude=kube*
    EOF

    yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

  
  - master节点: kubeadm init
  - worker节点: kubeadm join xxxxx


kubelet
''''''''

Kubelet组件运行在Node节点上，维持运行中的Pods以及提供kuberntes运行时环境，主要完成以下使命：

  - 监视分配给该Node节点的pods
  - 挂载pod所需要的volumes
  - 下载pod的secret
  - 通过docker/rkt来运行pod中的容器
  - 周期的执行pod中为容器定义的liveness探针
  - 上报pod的状态给系统的其他组件
  - 上报Node的状态

kubelet 核心模块
 .. image:: images/kubelet1.png
  
 - PLEG
   
   PLEG全称为PodLifecycleEvent,PLEG会一直调用container runtime获取本节点的pods,之后比较本模块中之前缓存的pods信息，比较最新的pods中的容器的状态是否发生改变，当状态发生切换的时候，生成一个eventRecord事件，输出到eventChannel中．　syncPod模块会接收到eventChannel中的event事件，来触发pod同步处理过程，调用contaiener 
 
 - cAdvisor

   cAdvisor集成在kubelet中，起到收集本Node的节点和启动的容器的监控的信息，启动一个Http Server服务器，对外接收rest api请求．cAvisor模块对外提供了interface接口，可以通过interface接口获取到node节点信息，本地文件系统的状态等信息，该接口被imageManager，OOMWatcher，containerManager等所使用


kubectl相关
''''''''''''
  - 临时映射端口
    
   .. code-block:: bash

     kubectl port-forward TYPE/NAME [options] [LOCAL_PORT:]REMOTE_PORT [...[LOCAL_PORT_N:]REMOTE_PORT_N]
     kubectl port-forward --address 0.0.0.0 pod/mypod 8888:5000
     kubectl port-forward service/myservice 5000 6000
     #默认映射为相同端口
     kubectl port-forward deployment/mydeployment 5000 6000
     
     #kubectl 下载路径
     curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
     curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.17.0/bin/windows/amd64/kubectl.exe

     #kubectl 自动补全
     yum install -y bash-completion && kubectl completion bash >/etc/bash_completion.d/kubectl


     

helm3
'''''
  - repo 添加
    
   .. code-block:: bash

    helm repo add [NAME] [URL] [flags]
    helm repo add stable  https://kubernetes-charts.storage.googleapis.com

  -  安装 & 升级 & 回退
     
   .. code-block:: bash

     #install
     helm install mydb stable/mysql

     #upgrade
     helm upgrade mydb --set imageTag=5.7.27 stable/mysql

     #rollback
     helm rollback mydb 1

     #查看
     helm history mydb
     helm status helm
  
rancher
---------
安装
''''
 - 生成证书

  .. code-block:: bash

   bash create_self-signed-cert.sh --ssl-size=2048 --ssl-date=3650 \
   --ssl-domain=www.test.com \
   --ssl-trusted-domain=www.test2.com \
   --ssl-trusted-ip=1.1.1.1,2.2.2.2,3.3.3.3 

  create_self-signed-cert.sh
   .. literalinclude:: create_self-signed-cert.sh
      :language: bash
 
 - 获取并修改value.yml

  .. code-block:: bash

   helm repo add rancher-stable https://releases.rancher.com/server-charts/stable

velero
-------

  - Minio是Apache License v2.0下发布的对象存储服务器。它与Amazon S3云存储服务兼容。
  - vsphere(vsan)平台下备份volume内容必须使用restic
  - restic是一个开源的备份工具，用于备份volume,而非pv，备份内容时需要手动为pod添加annotations backup.velero.io/backup-volumes: $volumename 
  - Limitations：hostPath volumes are not supported. Local persistent volumes are supported.
  - 文档: https://velero.io/docs/master/restic/


   .. code-block:: bash
    
    #修改minio sevice 为NodePort并安装 
    kubectl apply -f examples/minio/00-minio-deployment.yaml

    #s3 auth 添加
    cat > credentials-velero << EOF
    [default]
    aws_access_key_id = minio
    aws_secret_access_key = minio123
    EOF

    #velero server components 安装
    velero install  --provider aws --bucket velero \
    --secret-file ./credentials-velero \
    --use-volume-snapshots=false \
    --use-restic \ 
    --backup-location-config \
    region=minio,s3ForcePathStyle="true",s3Url=http://minio.velero.svc:9000,publicUrl=http://172.16.0.80:32329
    --plugins=velero/velero-plugin-for-aws:v1.0.0

    #备份
    kubectl -n YOUR_POD_NAMESPACE annotate pod/YOUR_POD_NAME backup.velero.io/backup-volumes=YOUR_VOLUME_NAME_1,YOUR_VOLUME_NAME_2,...

    velero backup create mysql-backup  --selector app.kubernetes.io/instance=mytest


应用部署
--------
 
rook-ceph 
''''''''''
   - 安装

   .. code-block:: bash

     #Operator安装
     helm install --namespace rook-ceph rook-release/rook-ceph --name rook-ceph  

     #ceph cluster安装
     kubectl apply -f cluster.yaml 

     #ceph toolbox安装
     kubectl apply -f toolbox.yaml 

     #默认dashboard http(7000)未开通,使用https;ingress https方式需要证书，故使用nodeport方式 
     kubectl apply -f  dashboard-external-https.yaml

     #获取dashboard密码
     kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode && echo
    
   - 配置rbd

   .. code-block:: bash

     #创建rbd存储策略，目前测试不支持在线扩容
     kubectl apply -f csi/rbd/storageclass.yaml  

     #创建快照策略
     csi/rbd/snapshotclass.yaml

     #创建快照
     csi/rbd/snapshot.yaml

     #克隆快照，测试挂载后无数据
     csi/rbd/pvc-restore.yaml


   - 配置object(s3)

   .. code-block:: bash

     kubectl apply -f object.yaml 
     kubectl apply -f object-user.yaml 

     #获取用户ak信息
     kubectl get secrets rook-ceph-object-user-<store>-<user> -o=jsonpath='{"Cgo="}{.data.AccessKey}{"Cgo="}{.data.SecretKey}{"Cgo="}'  -nrook-ceph | base64  -d

     #进入toolbox配置dashboard用户信息
     kubectl -n rook-ceph exec -it $(kubectl -n rook-ceph get pod -l "app=rook-ceph-tools" -o jsonpath='{.items[0].metadata.name}') bash
      radosgw-admin user modify --uid=my-user --system
      ceph dashboard set-rgw-api-access-key <access-key>
      ceph dashboard set-rgw-api-secret-key <secret-key>
      ceph dashboard set-rgw-api-host  rook-ceph-rgw-my-store.rook-ceph.svc.cluster.local

   - 卸载

   .. code-block:: bash

     helm delete --purge rook-ceph
     kubectl delete  cephcluster/rook-ceph -nrook-ceph
     kubectl delete ns rook-ceph
     kubectl api-resources --namespaced=true -o name | xargs -n 1 kubectl get --show-kind --ignore-not-found -n rook-ceph
     kubectl delete  customresourcedefinitions.apiextensions.k8s.io objectbuckets.objectbucket.io 

     #删除ceph节点的/var/lib/rook 目录
     rm -rf /var/lib/rook

     #强制删除pod
     kubectl delete pod/csi-cephfsplugin-provisioner-6c7d6f4964-sq88j --force  --grace-period=0  -nrook-ceph





TIDB
'''''
   - 安装

   .. code-block:: bash

     #修改系统内核参数&容器nofile
      sed -i 's/LimitNOFILE=infinity/LimitNOFILE=1048576/g'  /etc/systemd/system/docker.service
      sed -i 's/LimitNPROC=infinity/LimitNPROC=1048576/g'  /etc/systemd/system/docker.service
     
     #创建 TidbCluster CRD
     kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/crd.yaml && kubectl get crd tidbclusters.pingcap.com

     #获取value.yaml并更改gcr
     helm repo add pingcap https://charts.pingcap.org/
     helm inspect values pingcap/tidb-operator --version=v1.0.5 > values-tidb-operator.yaml
     更改Google image 为aliyun  registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler

     #operator安装
     helm install pingcap/tidb-operator --name=tidb-operator --namespace=tidb-admin --version=v1.0.5 -f  values-tidb-operator.yaml 
     kubectl get po -n tidb-admin -l app.kubernetes.io/name=tidb-operator

     #cluster value获取&安装
     mkdir -p tidb/v1.0.5&&helm inspect values pingcap/tidb-cluster --version=v1.0.5 > tidb/v1.0.5/values.yaml
     helm install pingcap/tidb-cluster --name=tidb-cluster  --namespace=tidb-cluster --version=v1.0.5 -f tidb/v1.0.5/values.yaml

   -  数据导入导出

   .. code-block:: bash

     #为以后方便使用syncer工具同步数据，开启mysql binlog，并设置格式为row
     #使用mysdumper工具
     mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o /data/test
      —B: database
      -T: table
      -F: 将实际的 table 切分成多大的 chunk 默认单位MB
      -t: 线程
     loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
     #同步工具
     syncer 通过binlog 同步数据
     sync-diff-inspector 用于校验 MySQL／TiDB 中两份数据是否一致的工具，测试需要提供 mysql instance_id 参数,未成功。

   -  卸载

   .. code-block:: bash

     helm delete --purge  tidb-cluster  
     helm delete --purge  tidb-operator  
     #删除pvc pv
     kubectl get pvc -ntidb-cluster | awk '{print $1}' | xargs kubectl delete pvc -ntidb-cluster


