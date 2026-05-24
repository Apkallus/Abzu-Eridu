出错时销毁vm再重新安装

安装vm后但剧本未设置时输入命令设置

网卡添加报错：

    ```log
    WARNING: The VMX file for this box contains a setting that is automatically overwritten by Vagrant
    WARNING: when started. Vagrant will stop overwriting this setting in an upcoming release which may
    WARNING: prevent proper networking setup. Below is the detected VMX setting:
    WARNING: 
    WARNING:   ethernet0.pcislotnumber = "192"
    WARNING: 
    WARNING: If networking fails to properly configure, it may require this VMX setting. It can be manually
    WARNING: applied via the Vagrantfile:
    WARNING: 
    WARNING:   Vagrant.configure(2) do |config|
    WARNING:     config.vm.provider :vmware_desktop do |vmware|
    WARNING:       vmware.vmx["ethernet0.pcislotnumber"] = "192"
    WARNING:     end
    WARNING:   end
    WARNING: 
    WARNING: For more information: www.vagrantup.com/docs/vmware/boxes.html#vmx-allowlisting
    WARNING: The VMX file for this box contains a setting that is automatically overwritten by Vagrant
    WARNING: when started. Vagrant will stop overwriting this setting in an upcoming release which may
    WARNING: prevent proper networking setup. Below is the detected VMX setting:
    WARNING: 
    WARNING:   ethernet1.pcislotnumber = "224"
    WARNING: 
    WARNING: If networking fails to properly configure, it may require this VMX setting. It can be manually
    WARNING: applied via the Vagrantfile:
    WARNING: 
    WARNING:   Vagrant.configure(2) do |config|
    WARNING:     config.vm.provider :vmware_desktop do |vmware|
    WARNING:       vmware.vmx["ethernet1.pcislotnumber"] = "224"
    WARNING:     end
    WARNING:   end
    WARNING: 
    WARNING: For more information: www.vagrantup.com/docs/vmware/boxes.html#vmx-allowlisting
    ```

    修改 lab 实例的配置文件，添加提示的修复方案

    ```ruby
    config.vm.provider "vmware_desktop" do |v|
        ...
        v.vmx["ethernet0.pcislotnumber"] = "192"
        v.vmx["ethernet1.pcislotnumber"] = "224"
        ...
    end
    ```

剧本设置报错：

    ```log
    TASK [domain_controller : Ensure that domain exists] *******************************************************
    ok: [dc03]
    fatal: [dc01]: FAILED! => {"changed": true, "msg": "Failed to install ADDSForest, DCPromo exited with 54: The operation failed with the following error:\r\n\r\nThe specified procedure could not be found.\r\n", "reboot_required": false}
    [started TASK: domain_controller : Reboot to complete domain creation on dc03]
    [started TASK: domain_controller : Ensure the server is a domain controller on dc03]

    PLAY RECAP *************************************************************************************************
    dc01                       : ok=8    changed=1    unreachable=0    failed=1    skipped=1    rescued=0    ignored=0   
    dc02                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    dc03                       : ok=12   changed=2    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0   
    srv02                      : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    srv03                      : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

    [-] 3 fails abort. 
    [-] Something wrong during the provisioning task : ad-parent_domain.yml 
    ```
    
    相同任务的错误2：

    ```log
    TASK [domain_controller : Ensure that domain exists] *****************************************************************************
    ok: [dc03]
    An exception occurred during task execution. To see the full traceback, use -vvv. The error was: requests.exceptions.ConnectionError: HTTPSConnectionPool(host='192.168.56.10', port=5986): Max retries exceeded with url: /wsman (Caused by NewConnectionError("HTTPSConnection(host='192.168.56.10', port=5986): Failed to establish a new connection: [Errno 113] 没有到主机的路由"))
    fatal: [dc01]: FAILED! => {"msg": "Unexpected failure during module execution: HTTPSConnectionPool(host='192.168.56.10', port=5986): Max retries exceeded with url: /wsman (Caused by NewConnectionError(\"HTTPSConnection(host='192.168.56.10', port=5986): Failed to establish a new connection: [Errno 113] 没有到主机的路由\"))", "stdout": ""}
    [started TASK: domain_controller : Reboot to complete domain creation on dc03]
    [started TASK: domain_controller : Ensure the server is a domain controller on dc03]
    ```
        