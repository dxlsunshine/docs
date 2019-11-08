华为交换机配置
+++++++++++++++

 - BootRom重置
   ::

    出现"Press Ctrl+B to Enter Boot Menu..."打印信息时，请在5秒钟内按下"Ctrl+B"，
    输入BootROM密码"O&m15213"（USG）进入BootROM主系统菜单
    交换机V100R005的BootRom密码是huawei
    V1R6C05之后版本 BootRom密码Admin@huawei.com

 - SSH配置
   :: 

    stelnet server enable
    ssh authentication-type default password
    user-interface vty 0 4
     protocol inbound all
     rsa local-key-pair create
    aaa
     local-user admin service-type telnet http ssh

 - Tacacs配置
   ::
        
     hwtacscs-server template acs
     hwtacacs-server authentication 10.51.80.108
     hwtacacs-server authorization 10.51.80.108
     hwtacacs-server accounting 10.51.80.108
     hwtacacs-server shared-key cipher %@%@$}kNTI"@!;HLYEAz*r.OP@gt%@%@
     aaa
     authentication-scheme acs
       authentication-mode hwtacacs local
     authorization-scheme acs
       authorization-mode hwtacacs local
       authorization-cmd 0 hwtacacs local
       authorization-cmd 1 hwtacacs local
       authorization-cmd 2 hwtacacs local
       authorization-cmd 3 hwtacacs local
     accounting-scheme acs
       accounting-mode hwtacacs
     domain default_admin
       authentication-scheme acs
       accounting-scheme acs
       authorization-scheme acs
       hwtacacs-server acs     
     # usg domain 配置
     domain acs
       authentication-scheme hwtacacs
       accounting-scheme acs
       authorization-scheme acs
       hwtacacs-server acs
       service-type internetaccess ssl-vpn l2tp ike administrator-access
       internet-access mode password
       reference user current-domain
       new-user add-temporary group /acs
