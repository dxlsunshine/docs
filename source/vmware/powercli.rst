PowerCLI
++++++++

- **PowerCLI安装**    

  .. code-block:: powershell

     #PowerCLI installation with admin rights:
     Install-Module VMware.PowerCLI

     #Use the -AllowClobber when you get: A command with the name 'Export-VM' is already available on this system.
     Install-Module VMware.PowerCLI -AllowClobber

     #Installation of PowerCLI without admin rights:
     Install-Module VMware.PowerCLI -Scope CurrentUser

     #These modules are installed in the %homepath%\Documents\WindowsPowerShell\Modules

     #Disable certificate checking and CEIP
     Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false -ParticipateInCeip $false


- **添加磁盘**    

  .. code-block:: powershell
  
     Connect-VIServer -Server 192.168.101.100 -Protocol https -User 'administrator' -Password '1234-abcd'-Force
     $vm = Get-VM wx-tky-ops-012
     $vm | New-HardDisk -CapacityGB 200 -Persistence persistent
    
- **获取虚拟机创建时间**    

  .. code-block:: powershell
  
     Connect-VIServer -Server 192.168.101.100 -Protocol https -User 'administrator' -Password '1234-abcd'-Force
     $vms=Get-VM
     $Report = @() 
     foreach ($vm in $vms) 
     { ,
     $Reportobj="" | Select "vmname",  "vmcreatetime"
     $Reportobj.vmname=$vm.Name
     $Reportobj.vmcreatetime=$vm.ExtensionData.Config.CreateDate 
     $Report+=$Reportobj
     }
     $Report | Export-Csv -NoTypeInformation -Encoding UTF8 -path vm-Info.csv
    
- **获取esxi主机信息**    

  .. code-block:: powershell
  
     Connect-VIServer -Server 192.168.101.100 -Protocol https -User 'administrator' -Password '1234-abcd'-Force
     #$respool = Get-ResourcePool dev
     #Get-VM -Location $respool #| Select-Object Name,NumCpu,MemoryGB,PowerState,VMHost
     get-vm | Where-Object{$_.powerstate -eq 'PoweredOn'} |Measure-Object #统计在线虚拟机数量
     $Report = @()  
     $ESXHosts = Get-VMHost   
     ForEach ($ESXHost in $ESXHosts)   
     {   
     $ReportObj = "" | Select "ESXi 主机名",  "所属群集", "VMKernel IP", "ESXi 全版本", "ESXi 主版本", "ESXi 子版本", "许可证序号", "许可证版本", "UUID", "制造商", "型号", "BIOS 版本", "BIOS 发布日期", "设备序列号", "电源状态", "连接状态", "最后一次启动时间", "vMotion 启用状态", "FaultTolerance 启用状态", "CPU 型号", "CPU 插槽数", "每 CPU 内核数", "物理 CPU 内核数", "逻辑 CPU 内核数", "超线程启用状态", "每 CPU 速度（MHz）", "CPU 总速度（MHz）", "CPU 已用速度（MHz）", "内存总容量 GB", "内存使用量 GB", "网卡数", "HBA 卡数","备注"
     $ESXHost_Temp = ($ESXHost | Get-View)  
     $ESXHost_SerialNumber=Get-EsxCli -VMHost $ESXHost
     $ReportObj."ESXi 主机名" = $ESXHost.Name  
     $ReportObj."所属群集" = $ESXHost.Parent   
     $ReportObj."ESXi 主版本" = $ESXHost.Version   
     $ReportObj."ESXi 子版本" = $ESXHost.Build   
     $ReportObj."许可证序号" = $ESXHost.LicenseKey   
     $ReportObj."制造商" = $ESXHost.Manufacturer   
     $ReportObj."型号" = $ESXHost.Model   
     $ReportObj."电源状态" = $ESXHost.PowerState   
     $ReportObj."连接状态" = $ESXHost.ConnectionState   
     $ReportObj."CPU 型号" = $ESXHost.ProcessorType   
     $ReportObj."物理 CPU 内核数" = $ESXHost.NumCpu   
     $ReportObj."超线程启用状态" = $ESXHost.HyperthreadingActive   
     $ReportObj."CPU 总速度（MHz）" = $ESXHost.CpuTotalMhz   
     $ReportObj."CPU 已用速度（MHz）" = $ESXHost.CpuUsageMhz   
     $ReportObj."内存总容量 GB" = [math]::round($ESXHost.MemoryTotalGB, 0)   
     $ReportObj."内存使用量 GB" = [math]::round($ESXHost.MemoryUsageGB, 0)   
     $ReportObj."VMKernel IP" = $ESXHost_Temp.Config.Option | ?{$_.Key -like "Vpx.Vpxa.config.vpxa.hostIp"} | % {$_.Value}   
     $ReportObj."ESXi 全版本" = $ESXHost_Temp.Config.Product.FullName   
     $ReportObj."许可证版本" = $ESXHost_Temp.Config.Product.LicenseProductVersion   
     $ReportObj."UUID" = $ESXHost_Temp.Summary.Hardware.Uuid   
     $ReportObj."BIOS 版本" = $ESXHost_Temp.Hardware.BiosInfo.BiosVersion   
     $ReportObj."BIOS 发布日期" = $ESXHost_Temp.Hardware.BiosInfo.ReleaseDate   
     $ReportObj."最后一次启动时间" = $ESXHost_Temp.Summary.Runtime.BootTime   
     $ReportObj."vMotion 启用状态" = $ESXHost_Temp.Summary.Config.VmotionEnabled   
     $ReportObj."FaultTolerance 启用状态" = $ESXHost_Temp.Summary.Config.FaultToleranceEnabled   
     $ReportObj."CPU 插槽数" = $ESXHost_Temp.Summary.Hardware.NumCpuPkgs   
     $ReportObj."每 CPU 内核数" = ($ESXHost.NumCpu / $ESXHost_Temp.Summary.Hardware.NumCpuPkgs)   
     $ReportObj."逻辑 CPU 内核数" = $ESXHost_Temp.Summary.Hardware.NumCpuThreads   
     $ReportObj."每 CPU 速度（MHz）" = $ESXHost_Temp.Summary.Hardware.CpuMhz   
     $ReportObj."网卡数" = $ESXHost_Temp.Summary.Hardware.NumNics   
     $ReportObj."HBA 卡数" = $ESXHost_Temp.Summary.Hardware.NumHBAs
     $ReportObj."设备序列号" = $ESXHost_SerialNumber.hardware.platform.get().SerialNumber
     $ReportObj."备注" = ""
     $Report += $ReportObj  
     }
     $Report | Export-Csv -NoTypeInformation -Encoding UTF8 -path Esxi-Host-Info.csv
