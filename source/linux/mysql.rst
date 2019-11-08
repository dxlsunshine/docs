Mysql
=====


 - mysql 5.7 初始化
    
   .. code-block:: bash

    #1.安装完成后默认随机密码
    #my.cnf 文件 添加 skip-grant-tables 参数，安全模式启动。
    update mysql.user set authentication_string='' where user='root'; //设置空密码
    
    #2.密码安全策略：需要更改密码才能使用，密码复杂的策略
    #my.cnf 文件 添加 validate_password=off，default_password_lifetime=0 关闭密码复杂度要求及过期时间。
    [mysqld]
    default_password_lifetime=0
    validate_password=off
    #skip-grant-tables


 - 创建&更改用户密码

   .. code-block:: mysql

    set password for root@'%'=password('1234-abcd');
    create user 'root'@'%' identified by '123456';
    grant all privileges on *.* to 'root'@'%';

 - mysql 时区问题

   ::

    问题:
    Django 2.0 ORM操作CONVERT_TZ中传递的是时区位置，如mysql数据中无对应时区信息，将返回NULL
    如:
    SELECT CONVERT_TZ('2004-01-01 12:00:00','GMT','MET');，查询结果默认可能为null
    SELECT CONVERT_TZ('2004-01-01 12:00:00','+00:00','+10:00'); 查询结果正常
    
    解决方法：
    CONVERT_TZ(dt,from_tz,to_tz)转换datetime值dt，从 from_tz 由给定转到 to_tz 时区给出的时区，并返回的结果值。 如果参数无效该函数返回NULL。
    mysql_tzinfo_to_sql  /usr/share/zoneinfo | mysql mysql  把系统的时区信息导入


