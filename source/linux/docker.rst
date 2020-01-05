Docker
======

Docker Registry
'''''''''''''''''

 - **角色1 Index**

    负责并维护有关用户帐户、镜像的校验以及公共命名空间的信息

 
 - **角色2 Register**

    registry是镜像和图表的仓库。然而，它没有一个本地数据库，也不提供用户的身份认证，由S3、云文件和本地文件系统提供数据库支持。此外，通过Index Auth service的Token方式进行身份认证。Registries可以有不同的类型。现在让我们来分析其中的几种类型：

     - Sponsor Registry：第三方的registry，供客户和Docker社区使用。
     - Mirror Registry：第三方的registry，只让客户使用。
     - Vendor Registry：由发布Docker镜像的供应商提供的registry。
     - Private Registry：通过设有防火墙和额外的安全层的私有实体提供的registry。

 - **角色3 Registry Client**

    Docker充当registry客户端来负责维护推送和拉取的任务，以及客户端的授权。

  
 - **拉起镜像流程**

    .. image:: images/pull.png



Docker ENV ARG
''''''''''''''
  - **ARG**

    The ARG instruction defines a variable that users can pass at build-time to the builder with the docker build command using the --build-arg <varname>=<value> flag.

  - **ENV**

    The ENV instruction sets the environment variable <key> to the value <value>.The environment variables set using ENV will persist when a container is run from the resulting image.

  - **combine both**

    .. code-block:: 

     ARG var
     ENV var=${var} 

常用命令
''''''''

    .. code-block:: 
    
      #删除停止的容器
      docker rm -v -f &(docker ps -qf status=exited)
      #查看容器中连接
      nsenter -t $(docker inspect -f '{{.State.Pid}}' ssr)  -n netstat -npt
