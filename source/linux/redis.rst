Redis
#####
 redis基本概念
  
 - redis初始化的时候会默认创建16个数据库（这个配置可以在redis配置文件中修改）
 
 - 每一个数据库都有一个id号，默认的数据库id为0；

 - 各个数据库之间是相互隔离的，当然也可以在不同数据库之间复制数据

 - 可以使用select命令选择当前使用的数据库：

 - Redis五种数据类型：string,hash,list,set,zset.
    
      - string
    
       ::
        
        增加、修改
        set [key] <seconds> [value]
        mset [key1] [value] [key2] [value]...
        exprie [key] [seconds]

        追加
        append [key] [value]  

        获取
        get [key]
        mget [key1] [key2] ...

        删除
        del [key]

        查看key
        select [index]
        keys *`
        ttl key
    
    
      - hash
    
       ::
    
        增加、修改
        hset [key] [field] [value]

        获取
        hkeys [key]
        hget [key] [field]
        hmget [key] [field1] <field2> ...
        hvals [key]

        删除
        hdel key field1 field2 ...
    
      - list
    
       ::
        
        增加、修改
        lpush [key] [value1] [value2]
        rpush [key] [value1] [value2]
        linsert [key] [before/after] [value] [newvalue]
        lset [key] [index] [value]
        
        获取
        lrange key start stop
        lrange key 0 -1

        删除
        lrem [key] [count] [value]
    
      - set
    
       ::
    
        增加、修改
        sadd key m1 m2 ...

        获取
        smembers key

        删除
        srem key value
    
    
      - zset
      
       ::
        
        增加、修改
        zadd key m1 score1  m2 score2 ...
        
        获取
        zrange key start stop
        zrangebyscore key min max
        zscore key member

        删除
        zrem key m1 m2 ...
        zremrangebyscore key min max
    
