锐捷
====

 - IRF

  **IRF配置**

  ::

    #device1
    system-view
    irf member 1 
    irf-port 1 
     port group interface ten-gigabitethernet 3/0/1 
    irf-port 2 
     port group interface ten-gigabitethernet 3/0/1 
     quit
     quit
    save
    system-view
    chassis convert mode irf
    
    #device2
    system-view
    irf member 2 
    irf-port 1 
       port group interface ten-gigabitethernet 3/0/1 
    irf-port 2 
       port group interface ten-gigabitethernet 3/0/1 
     quit
     quit
    save
    system-view
    chassis convert mode irf
    
    
    #端口聚合及mad配置
    irf domain 1
    interface route-aggregation 2 
    link-aggregation mode dynamic 
    mad enable 
    interface gigabitethernet 1/4/0/2 
       port link-aggregation group 2  
