Updates für VMware ESXi können selbst bei der kostenlosen ESXi Hypervisor Variante einfach über die Kommandozeile eingespielt werden. In diesem Beispiel zeigen wir anhand von [VMware ESXi 6.7](https://www.thomas-krenn.com/de/wiki/VMware_ESXi_6.7 "VMware ESXi 6.7") wie Sie Updates über die Kommandozeile einspielen.[[1]](https://www.thomas-krenn.com/de/wiki/VMware_ESXi_updaten#cite_note-1)

## Inhaltsverzeichnis

-   [1 Updates herunterladen](https://www.thomas-krenn.com/de/wiki/VMware_ESXi_updaten#Updates_herunterladen)
-   [2 Updates auf ESXi Host laden](https://www.thomas-krenn.com/de/wiki/VMware_ESXi_updaten#Updates_auf_ESXi_Host_laden)
-   [3 Updates auf der Kommandozeile einspielen](https://www.thomas-krenn.com/de/wiki/VMware_ESXi_updaten#Updates_auf_der_Kommandozeile_einspielen)
-   [4 Updates überprüfen](https://www.thomas-krenn.com/de/wiki/VMware_ESXi_updaten#Updates_.C3.BCberpr.C3.BCfen)
-   [5 Reboot durchführen und Wartungsmodus beenden](https://www.thomas-krenn.com/de/wiki/VMware_ESXi_updaten#Reboot_durchf.C3.BChren_und_Wartungsmodus_beenden)
-   [6 Einzelnachweise](https://www.thomas-krenn.com/de/wiki/VMware_ESXi_updaten#Einzelnachweise)

## Updates herunterladen

Im folgenden Knowledge Base Artikel von VMware finden Sie Informationen, wie sie die aktuell verfügbaren Updates für Ihr System herunterladen können:

-   [https://kb.vmware.com/s/article/1021623](https://kb.vmware.com/s/article/1021623)

-   [![](https://www.thomas-krenn.com/de/wikiDE/images/thumb/0/01/ESXi-6.7-Update-01-Downloads.png/120px-ESXi-6.7-Update-01-Downloads.png)](https://www.thomas-krenn.com/de/wiki/Datei:ESXi-6.7-Update-01-Downloads.png)
    
    Verfügbare Updates von VMware herunterladen.
    

## Updates auf ESXi Host laden

Im nächsten Schritt laden Sie die Updates auf den ESXi Host. Dies ist beispielsweise über den Datastore Browser des vSphere Web Client möglich.

-   [![](https://www.thomas-krenn.com/de/wikiDE/images/thumb/9/90/ESXi-6.7-Update-02-Web-Client.png/120px-ESXi-6.7-Update-02-Web-Client.png)](https://www.thomas-krenn.com/de/wiki/Datei:ESXi-6.7-Update-02-Web-Client.png)
    
    Datastore Browser öffnen.
    
-   [![](https://www.thomas-krenn.com/de/wikiDE/images/thumb/4/4b/ESXi-6.7-Update-03-New-Directory.png/120px-ESXi-6.7-Update-03-New-Directory.png)](https://www.thomas-krenn.com/de/wiki/Datei:ESXi-6.7-Update-03-New-Directory.png)
    
    Neues Verzeichnis erstellen.
    
-   [![](https://www.thomas-krenn.com/de/wikiDE/images/thumb/0/0e/ESXi-6.7-Update-04-Upload.png/120px-ESXi-6.7-Update-04-Upload.png)](https://www.thomas-krenn.com/de/wiki/Datei:ESXi-6.7-Update-04-Upload.png)
    
    Auf Upload klicken und Dateien auswählen.
    
-   [![](https://www.thomas-krenn.com/de/wikiDE/images/thumb/8/8a/ESXi-6.7-Update-05-Files.png/120px-ESXi-6.7-Update-05-Files.png)](https://www.thomas-krenn.com/de/wiki/Datei:ESXi-6.7-Update-05-Files.png)
    
    Dateien wurden hochgeladen.
    

## Updates auf der Kommandozeile einspielen

Aktivieren Sie im Web Client die SSH Shell, stoppen oder migrieren Sie alle virtuellen Maschinen und setzen Sie anschließend den Host in den Wartungsmodus:

[root@localhost:~] vim-cmd hostsvc/maintenance_mode_enter

Spielen Sie anschließend die Updates mit dem esxcli Kommando wie folgt ein:

[root@localhost:~] esxcli software vib update -d /vmfs/volumes/datastore1/updates/ESXi670-201806001.zip
Installation Result
   Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
   Reboot Required: true
   VIBs Installed: VMware_bootbank_cpu-microcode_6.7.0-0.14.8941472, VMware_bootbank_esx-base_6.7.0-0.14.8941472, VMware_bootbank_vsan_6.7.0-0.14.8941472, VMware_bootbank_vsanhealth_6.7.0-0.14.8941472, VMware_locker_tools-light_10.2.1.8267844-8941472
   VIBs Removed: VMware_bootbank_cpu-microcode_6.7.0-0.0.8169922, VMware_bootbank_esx-base_6.7.0-0.0.8169922, VMware_bootbank_vsan_6.7.0-0.0.8169922, VMware_bootbank_vsanhealth_6.7.0-0.0.8169922, VMware_locker_tools-light_10.2.0.7253323-8169922
   VIBs Skipped: VMW_bootbank_ata-libata-92_3.00.9.2-16vmw.670.0.0.8169922, VMW_bootbank_ata-pata-amd_0.3.10-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-atiixp_0.4.6-4vmw.670.0.0.8169922, VMW_bootbank_ata-pata-cmd64x_0.2.5-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-hpt3x2n_0.3.4-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-pdc2027x_1.0-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-serverworks_0.4.3-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-sil680_0.4.8-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-via_0.3.3-2vmw.670.0.0.8169922, VMW_bootbank_block-cciss_3.6.14-10vmw.670.0.0.8169922, VMW_bootbank_bnxtnet_20.6.101.7-11vmw.670.0.0.8169922, VMW_bootbank_brcmfcoe_11.4.1078.0-8vmw.670.0.0.8169922, VMW_bootbank_char-random_1.0-3vmw.670.0.0.8169922, VMW_bootbank_ehci-ehci-hcd_1.0-4vmw.670.0.0.8169922, VMW_bootbank_elxiscsi_11.4.1174.0-2vmw.670.0.0.8169922, VMW_bootbank_elxnet_11.4.1094.0-5vmw.670.0.0.8169922, VMW_bootbank_hid-hid_1.0-3vmw.670.0.0.8169922, VMW_bootbank_i40en_1.3.1-18vmw.670.0.0.8169922, VMW_bootbank_iavmd_1.2.0.1011-2vmw.670.0.0.8169922, VMW_bootbank_igbn_0.1.0.0-15vmw.670.0.0.8169922, VMW_bootbank_ima-qla4xxx_2.02.18-1vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-devintf_39.1-4vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-msghandler_39.1-4vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-si-drv_39.1-4vmw.670.0.0.8169922, VMW_bootbank_iser_1.0.0.0-1vmw.670.0.0.8169922, VMW_bootbank_ixgben_1.4.1-11vmw.670.0.0.8169922, VMW_bootbank_lpfc_11.4.33.1-6vmw.670.0.0.8169922, VMW_bootbank_lpnic_11.4.59.0-1vmw.670.0.0.8169922, VMW_bootbank_lsi-mr3_7.702.13.00-4vmw.670.0.0.8169922, VMW_bootbank_lsi-msgpt2_20.00.04.00-4vmw.670.0.0.8169922, VMW_bootbank_lsi-msgpt35_03.00.01.00-10vmw.670.0.0.8169922, VMW_bootbank_lsi-msgpt3_16.00.01.00-1vmw.670.0.0.8169922, VMW_bootbank_misc-cnic-register_1.78.75.v60.7-1vmw.670.0.0.8169922, VMW_bootbank_misc-drivers_6.7.0-0.0.8169922, VMW_bootbank_mtip32xx-native_3.9.6-1vmw.670.0.0.8169922, VMW_bootbank_ne1000_0.8.3-4vmw.670.0.0.8169922, VMW_bootbank_nenic_1.0.11.0-1vmw.670.0.0.8169922, VMW_bootbank_net-bnx2_2.2.4f.v60.10-2vmw.670.0.0.8169922, VMW_bootbank_net-bnx2x_1.78.80.v60.12-2vmw.670.0.0.8169922, VMW_bootbank_net-cdc-ether_1.0-3vmw.670.0.0.8169922, VMW_bootbank_net-cnic_1.78.76.v60.13-2vmw.670.0.0.8169922, VMW_bootbank_net-e1000_8.0.3.1-5vmw.670.0.0.8169922, VMW_bootbank_net-e1000e_3.2.2.1-2vmw.670.0.0.8169922, VMW_bootbank_net-enic_2.1.2.38-2vmw.670.0.0.8169922, VMW_bootbank_net-fcoe_1.0.29.9.3-7vmw.670.0.0.8169922, VMW_bootbank_net-forcedeth_0.61-2vmw.670.0.0.8169922, VMW_bootbank_net-igb_5.0.5.1.1-5vmw.670.0.0.8169922, VMW_bootbank_net-ixgbe_3.7.13.7.14iov-20vmw.670.0.0.8169922, VMW_bootbank_net-libfcoe-92_1.0.24.9.4-8vmw.670.0.0.8169922, VMW_bootbank_net-mlx4-core_1.9.7.0-1vmw.670.0.0.8169922, VMW_bootbank_net-mlx4-en_1.9.7.0-1vmw.670.0.0.8169922, VMW_bootbank_net-nx-nic_5.0.621-5vmw.670.0.0.8169922, VMW_bootbank_net-tg3_3.131d.v60.4-2vmw.670.0.0.8169922, VMW_bootbank_net-usbnet_1.0-3vmw.670.0.0.8169922, VMW_bootbank_net-vmxnet3_1.1.3.0-3vmw.670.0.0.8169922, VMW_bootbank_nhpsa_2.0.22-1vmw.670.0.0.8169922, VMW_bootbank_nmlx4-core_3.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx4-en_3.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx4-rdma_3.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx5-core_4.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx5-rdma_4.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_ntg3_4.1.3.0-1vmw.670.0.0.8169922, VMW_bootbank_nvme_1.2.1.34-1vmw.670.0.0.8169922, VMW_bootbank_nvmxnet3-ens_2.0.0.21-1vmw.670.0.0.8169922, VMW_bootbank_nvmxnet3_2.0.0.27-1vmw.670.0.0.8169922, VMW_bootbank_ohci-usb-ohci_1.0-3vmw.670.0.0.8169922, VMW_bootbank_pvscsi_0.1-2vmw.670.0.0.8169922, VMW_bootbank_qcnic_1.0.2.0.4-1vmw.670.0.0.8169922, VMW_bootbank_qedentv_2.0.6.4-8vmw.670.0.0.8169922, VMW_bootbank_qfle3_1.0.50.11-9vmw.670.0.0.8169922, VMW_bootbank_qfle3f_1.0.25.0.2-14vmw.670.0.0.8169922, VMW_bootbank_qfle3i_1.0.2.3.9-3vmw.670.0.0.8169922, VMW_bootbank_qflge_1.1.0.11-1vmw.670.0.0.8169922, VMW_bootbank_sata-ahci_3.0-26vmw.670.0.0.8169922, VMW_bootbank_sata-ata-piix_2.12-10vmw.670.0.0.8169922, VMW_bootbank_sata-sata-nv_3.5-4vmw.670.0.0.8169922, VMW_bootbank_sata-sata-promise_2.12-3vmw.670.0.0.8169922, VMW_bootbank_sata-sata-sil24_1.1-1vmw.670.0.0.8169922, VMW_bootbank_sata-sata-sil_2.3-4vmw.670.0.0.8169922, VMW_bootbank_sata-sata-svw_2.3-3vmw.670.0.0.8169922, VMW_bootbank_scsi-aacraid_1.1.5.1-9vmw.670.0.0.8169922, VMW_bootbank_scsi-adp94xx_1.0.8.12-6vmw.670.0.0.8169922, VMW_bootbank_scsi-aic79xx_3.1-6vmw.670.0.0.8169922, VMW_bootbank_scsi-bnx2fc_1.78.78.v60.8-1vmw.670.0.0.8169922, VMW_bootbank_scsi-bnx2i_2.78.76.v60.8-1vmw.670.0.0.8169922, VMW_bootbank_scsi-fnic_1.5.0.45-3vmw.670.0.0.8169922, VMW_bootbank_scsi-hpsa_6.0.0.84-3vmw.670.0.0.8169922, VMW_bootbank_scsi-ips_7.12.05-4vmw.670.0.0.8169922, VMW_bootbank_scsi-iscsi-linux-92_1.0.0.2-3vmw.670.0.0.8169922, VMW_bootbank_scsi-libfc-92_1.0.40.9.3-5vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid-mbox_2.20.5.1-6vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid-sas_6.603.55.00-2vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid2_2.00.4-9vmw.670.0.0.8169922, VMW_bootbank_scsi-mpt2sas_19.00.00.00-2vmw.670.0.0.8169922, VMW_bootbank_scsi-mptsas_4.23.01.00-10vmw.670.0.0.8169922, VMW_bootbank_scsi-mptspi_4.23.01.00-10vmw.670.0.0.8169922, VMW_bootbank_scsi-qla4xxx_5.01.03.2-7vmw.670.0.0.8169922, VMW_bootbank_shim-iscsi-linux-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-iscsi-linux-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libata-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libata-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfc-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfc-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfcoe-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfcoe-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-3-0_6.7.0-0.0.8169922, VMW_bootbank_smartpqi_1.0.1.553-10vmw.670.0.0.8169922, VMW_bootbank_uhci-usb-uhci_1.0-3vmw.670.0.0.8169922, VMW_bootbank_usb-storage-usb-storage_1.0-3vmw.670.0.0.8169922, VMW_bootbank_usbcore-usb_1.0-3vmw.670.0.0.8169922, VMW_bootbank_vmkata_0.1-1vmw.670.0.0.8169922, VMW_bootbank_vmkfcoe_1.0.0.0-1vmw.670.0.0.8169922, VMW_bootbank_vmkplexer-vmkplexer_6.7.0-0.0.8169922, VMW_bootbank_vmkusb_0.1-1vmw.670.0.0.8169922, VMW_bootbank_vmw-ahci_1.2.0-6vmw.670.0.0.8169922, VMW_bootbank_xhci-xhci_1.0-3vmw.670.0.0.8169922, VMware_bootbank_elx-esx-libelxima.so_11.4.1184.0-0.0.8169922, VMware_bootbank_esx-dvfilter-generic-fastpath_6.7.0-0.0.8169922, VMware_bootbank_esx-ui_1.25.0-7872652, VMware_bootbank_esx-xserver_6.7.0-0.0.8169922, VMware_bootbank_lsu-hp-hpsa-plugin_2.0.0-13vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-lsi-mr3-plugin_1.0.0-12vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-lsi-msgpt3-plugin_1.0.0-8vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-megaraid-sas-plugin_1.0.0-9vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-mpt2sas-plugin_2.0.0-7vmw.670.0.0.8169922, VMware_bootbank_native-misc-drivers_6.7.0-0.0.8169922, VMware_bootbank_qlnativefc_3.0.1.0-5vmw.670.0.0.8169922, VMware_bootbank_rste_2.0.2.0088-7vmw.670.0.0.8169922, VMware_bootbank_vmware-esx-esxcli-nvme-plugin_1.2.0.32-0.0.8169922
[root@localhost:~] esxcli software vib update -d /vmfs/volumes/datastore1/updates/ESXi670-201807001.zip
Installation Result
   Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
   Reboot Required: true
   VIBs Installed: VMW_bootbank_qedentv_2.0.6.4-10vmw.670.0.17.9214924, VMware_bootbank_esx-base_6.7.0-0.17.9214924, VMware_bootbank_vsan_6.7.0-0.17.9214924, VMware_bootbank_vsanhealth_6.7.0-0.17.9214924
   VIBs Removed: VMW_bootbank_qedentv_2.0.6.4-8vmw.670.0.0.8169922, VMware_bootbank_esx-base_6.7.0-0.14.8941472, VMware_bootbank_vsan_6.7.0-0.14.8941472, VMware_bootbank_vsanhealth_6.7.0-0.14.8941472
   VIBs Skipped: VMW_bootbank_ata-libata-92_3.00.9.2-16vmw.670.0.0.8169922, VMW_bootbank_ata-pata-amd_0.3.10-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-atiixp_0.4.6-4vmw.670.0.0.8169922, VMW_bootbank_ata-pata-cmd64x_0.2.5-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-hpt3x2n_0.3.4-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-pdc2027x_1.0-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-serverworks_0.4.3-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-sil680_0.4.8-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-via_0.3.3-2vmw.670.0.0.8169922, VMW_bootbank_block-cciss_3.6.14-10vmw.670.0.0.8169922, VMW_bootbank_bnxtnet_20.6.101.7-11vmw.670.0.0.8169922, VMW_bootbank_brcmfcoe_11.4.1078.0-8vmw.670.0.0.8169922, VMW_bootbank_char-random_1.0-3vmw.670.0.0.8169922, VMW_bootbank_ehci-ehci-hcd_1.0-4vmw.670.0.0.8169922, VMW_bootbank_elxiscsi_11.4.1174.0-2vmw.670.0.0.8169922, VMW_bootbank_elxnet_11.4.1094.0-5vmw.670.0.0.8169922, VMW_bootbank_hid-hid_1.0-3vmw.670.0.0.8169922, VMW_bootbank_i40en_1.3.1-18vmw.670.0.0.8169922, VMW_bootbank_iavmd_1.2.0.1011-2vmw.670.0.0.8169922, VMW_bootbank_igbn_0.1.0.0-15vmw.670.0.0.8169922, VMW_bootbank_ima-qla4xxx_2.02.18-1vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-devintf_39.1-4vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-msghandler_39.1-4vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-si-drv_39.1-4vmw.670.0.0.8169922, VMW_bootbank_iser_1.0.0.0-1vmw.670.0.0.8169922, VMW_bootbank_ixgben_1.4.1-11vmw.670.0.0.8169922, VMW_bootbank_lpfc_11.4.33.1-6vmw.670.0.0.8169922, VMW_bootbank_lpnic_11.4.59.0-1vmw.670.0.0.8169922, VMW_bootbank_lsi-mr3_7.702.13.00-4vmw.670.0.0.8169922, VMW_bootbank_lsi-msgpt2_20.00.04.00-4vmw.670.0.0.8169922, VMW_bootbank_lsi-msgpt35_03.00.01.00-10vmw.670.0.0.8169922, VMW_bootbank_lsi-msgpt3_16.00.01.00-1vmw.670.0.0.8169922, VMW_bootbank_misc-cnic-register_1.78.75.v60.7-1vmw.670.0.0.8169922, VMW_bootbank_misc-drivers_6.7.0-0.0.8169922, VMW_bootbank_mtip32xx-native_3.9.6-1vmw.670.0.0.8169922, VMW_bootbank_ne1000_0.8.3-4vmw.670.0.0.8169922, VMW_bootbank_nenic_1.0.11.0-1vmw.670.0.0.8169922, VMW_bootbank_net-bnx2_2.2.4f.v60.10-2vmw.670.0.0.8169922, VMW_bootbank_net-bnx2x_1.78.80.v60.12-2vmw.670.0.0.8169922, VMW_bootbank_net-cdc-ether_1.0-3vmw.670.0.0.8169922, VMW_bootbank_net-cnic_1.78.76.v60.13-2vmw.670.0.0.8169922, VMW_bootbank_net-e1000_8.0.3.1-5vmw.670.0.0.8169922, VMW_bootbank_net-e1000e_3.2.2.1-2vmw.670.0.0.8169922, VMW_bootbank_net-enic_2.1.2.38-2vmw.670.0.0.8169922, VMW_bootbank_net-fcoe_1.0.29.9.3-7vmw.670.0.0.8169922, VMW_bootbank_net-forcedeth_0.61-2vmw.670.0.0.8169922, VMW_bootbank_net-igb_5.0.5.1.1-5vmw.670.0.0.8169922, VMW_bootbank_net-ixgbe_3.7.13.7.14iov-20vmw.670.0.0.8169922, VMW_bootbank_net-libfcoe-92_1.0.24.9.4-8vmw.670.0.0.8169922, VMW_bootbank_net-mlx4-core_1.9.7.0-1vmw.670.0.0.8169922, VMW_bootbank_net-mlx4-en_1.9.7.0-1vmw.670.0.0.8169922, VMW_bootbank_net-nx-nic_5.0.621-5vmw.670.0.0.8169922, VMW_bootbank_net-tg3_3.131d.v60.4-2vmw.670.0.0.8169922, VMW_bootbank_net-usbnet_1.0-3vmw.670.0.0.8169922, VMW_bootbank_net-vmxnet3_1.1.3.0-3vmw.670.0.0.8169922, VMW_bootbank_nhpsa_2.0.22-1vmw.670.0.0.8169922, VMW_bootbank_nmlx4-core_3.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx4-en_3.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx4-rdma_3.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx5-core_4.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx5-rdma_4.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_ntg3_4.1.3.0-1vmw.670.0.0.8169922, VMW_bootbank_nvme_1.2.1.34-1vmw.670.0.0.8169922, VMW_bootbank_nvmxnet3-ens_2.0.0.21-1vmw.670.0.0.8169922, VMW_bootbank_nvmxnet3_2.0.0.27-1vmw.670.0.0.8169922, VMW_bootbank_ohci-usb-ohci_1.0-3vmw.670.0.0.8169922, VMW_bootbank_pvscsi_0.1-2vmw.670.0.0.8169922, VMW_bootbank_qcnic_1.0.2.0.4-1vmw.670.0.0.8169922, VMW_bootbank_qfle3_1.0.50.11-9vmw.670.0.0.8169922, VMW_bootbank_qfle3f_1.0.25.0.2-14vmw.670.0.0.8169922, VMW_bootbank_qfle3i_1.0.2.3.9-3vmw.670.0.0.8169922, VMW_bootbank_qflge_1.1.0.11-1vmw.670.0.0.8169922, VMW_bootbank_sata-ahci_3.0-26vmw.670.0.0.8169922, VMW_bootbank_sata-ata-piix_2.12-10vmw.670.0.0.8169922, VMW_bootbank_sata-sata-nv_3.5-4vmw.670.0.0.8169922, VMW_bootbank_sata-sata-promise_2.12-3vmw.670.0.0.8169922, VMW_bootbank_sata-sata-sil24_1.1-1vmw.670.0.0.8169922, VMW_bootbank_sata-sata-sil_2.3-4vmw.670.0.0.8169922, VMW_bootbank_sata-sata-svw_2.3-3vmw.670.0.0.8169922, VMW_bootbank_scsi-aacraid_1.1.5.1-9vmw.670.0.0.8169922, VMW_bootbank_scsi-adp94xx_1.0.8.12-6vmw.670.0.0.8169922, VMW_bootbank_scsi-aic79xx_3.1-6vmw.670.0.0.8169922, VMW_bootbank_scsi-bnx2fc_1.78.78.v60.8-1vmw.670.0.0.8169922, VMW_bootbank_scsi-bnx2i_2.78.76.v60.8-1vmw.670.0.0.8169922, VMW_bootbank_scsi-fnic_1.5.0.45-3vmw.670.0.0.8169922, VMW_bootbank_scsi-hpsa_6.0.0.84-3vmw.670.0.0.8169922, VMW_bootbank_scsi-ips_7.12.05-4vmw.670.0.0.8169922, VMW_bootbank_scsi-iscsi-linux-92_1.0.0.2-3vmw.670.0.0.8169922, VMW_bootbank_scsi-libfc-92_1.0.40.9.3-5vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid-mbox_2.20.5.1-6vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid-sas_6.603.55.00-2vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid2_2.00.4-9vmw.670.0.0.8169922, VMW_bootbank_scsi-mpt2sas_19.00.00.00-2vmw.670.0.0.8169922, VMW_bootbank_scsi-mptsas_4.23.01.00-10vmw.670.0.0.8169922, VMW_bootbank_scsi-mptspi_4.23.01.00-10vmw.670.0.0.8169922, VMW_bootbank_scsi-qla4xxx_5.01.03.2-7vmw.670.0.0.8169922, VMW_bootbank_shim-iscsi-linux-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-iscsi-linux-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libata-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libata-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfc-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfc-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfcoe-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfcoe-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-3-0_6.7.0-0.0.8169922, VMW_bootbank_smartpqi_1.0.1.553-10vmw.670.0.0.8169922, VMW_bootbank_uhci-usb-uhci_1.0-3vmw.670.0.0.8169922, VMW_bootbank_usb-storage-usb-storage_1.0-3vmw.670.0.0.8169922, VMW_bootbank_usbcore-usb_1.0-3vmw.670.0.0.8169922, VMW_bootbank_vmkata_0.1-1vmw.670.0.0.8169922, VMW_bootbank_vmkfcoe_1.0.0.0-1vmw.670.0.0.8169922, VMW_bootbank_vmkplexer-vmkplexer_6.7.0-0.0.8169922, VMW_bootbank_vmkusb_0.1-1vmw.670.0.0.8169922, VMW_bootbank_vmw-ahci_1.2.0-6vmw.670.0.0.8169922, VMW_bootbank_xhci-xhci_1.0-3vmw.670.0.0.8169922, VMware_bootbank_cpu-microcode_6.7.0-0.14.8941472, VMware_bootbank_elx-esx-libelxima.so_11.4.1184.0-0.0.8169922, VMware_bootbank_esx-dvfilter-generic-fastpath_6.7.0-0.0.8169922, VMware_bootbank_esx-ui_1.25.0-7872652, VMware_bootbank_esx-xserver_6.7.0-0.0.8169922, VMware_bootbank_lsu-hp-hpsa-plugin_2.0.0-13vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-lsi-mr3-plugin_1.0.0-12vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-lsi-msgpt3-plugin_1.0.0-8vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-megaraid-sas-plugin_1.0.0-9vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-mpt2sas-plugin_2.0.0-7vmw.670.0.0.8169922, VMware_bootbank_native-misc-drivers_6.7.0-0.0.8169922, VMware_bootbank_qlnativefc_3.0.1.0-5vmw.670.0.0.8169922, VMware_bootbank_rste_2.0.2.0088-7vmw.670.0.0.8169922, VMware_bootbank_vmware-esx-esxcli-nvme-plugin_1.2.0.32-0.0.8169922, VMware_locker_tools-light_10.2.1.8267844-8941472
[root@localhost:~] esxcli software vib update -d /vmfs/volumes/datastore1/updates/ESXi670-201808001.zip
Installation Result
   Message: The update completed successfully, but the system needs to be rebooted for the changes to be effective.
   Reboot Required: true
   VIBs Installed: VMware_bootbank_cpu-microcode_6.7.0-0.20.9484548, VMware_bootbank_esx-base_6.7.0-0.20.9484548, VMware_bootbank_esx-ui_1.25.1-9210161, VMware_bootbank_vsan_6.7.0-0.20.9484548, VMware_bootbank_vsanhealth_6.7.0-0.20.9484548
   VIBs Removed: VMware_bootbank_cpu-microcode_6.7.0-0.14.8941472, VMware_bootbank_esx-base_6.7.0-0.17.9214924, VMware_bootbank_esx-ui_1.25.0-7872652, VMware_bootbank_vsan_6.7.0-0.17.9214924, VMware_bootbank_vsanhealth_6.7.0-0.17.9214924
   VIBs Skipped: VMW_bootbank_ata-libata-92_3.00.9.2-16vmw.670.0.0.8169922, VMW_bootbank_ata-pata-amd_0.3.10-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-atiixp_0.4.6-4vmw.670.0.0.8169922, VMW_bootbank_ata-pata-cmd64x_0.2.5-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-hpt3x2n_0.3.4-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-pdc2027x_1.0-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-serverworks_0.4.3-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-sil680_0.4.8-3vmw.670.0.0.8169922, VMW_bootbank_ata-pata-via_0.3.3-2vmw.670.0.0.8169922, VMW_bootbank_block-cciss_3.6.14-10vmw.670.0.0.8169922, VMW_bootbank_bnxtnet_20.6.101.7-11vmw.670.0.0.8169922, VMW_bootbank_brcmfcoe_11.4.1078.0-8vmw.670.0.0.8169922, VMW_bootbank_char-random_1.0-3vmw.670.0.0.8169922, VMW_bootbank_ehci-ehci-hcd_1.0-4vmw.670.0.0.8169922, VMW_bootbank_elxiscsi_11.4.1174.0-2vmw.670.0.0.8169922, VMW_bootbank_elxnet_11.4.1094.0-5vmw.670.0.0.8169922, VMW_bootbank_hid-hid_1.0-3vmw.670.0.0.8169922, VMW_bootbank_i40en_1.3.1-18vmw.670.0.0.8169922, VMW_bootbank_iavmd_1.2.0.1011-2vmw.670.0.0.8169922, VMW_bootbank_igbn_0.1.0.0-15vmw.670.0.0.8169922, VMW_bootbank_ima-qla4xxx_2.02.18-1vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-devintf_39.1-4vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-msghandler_39.1-4vmw.670.0.0.8169922, VMW_bootbank_ipmi-ipmi-si-drv_39.1-4vmw.670.0.0.8169922, VMW_bootbank_iser_1.0.0.0-1vmw.670.0.0.8169922, VMW_bootbank_ixgben_1.4.1-11vmw.670.0.0.8169922, VMW_bootbank_lpfc_11.4.33.1-6vmw.670.0.0.8169922, VMW_bootbank_lpnic_11.4.59.0-1vmw.670.0.0.8169922, VMW_bootbank_lsi-mr3_7.702.13.00-4vmw.670.0.0.8169922, VMW_bootbank_lsi-msgpt2_20.00.04.00-4vmw.670.0.0.8169922, VMW_bootbank_lsi-msgpt35_03.00.01.00-10vmw.670.0.0.8169922, VMW_bootbank_lsi-msgpt3_16.00.01.00-1vmw.670.0.0.8169922, VMW_bootbank_misc-cnic-register_1.78.75.v60.7-1vmw.670.0.0.8169922, VMW_bootbank_misc-drivers_6.7.0-0.0.8169922, VMW_bootbank_mtip32xx-native_3.9.6-1vmw.670.0.0.8169922, VMW_bootbank_ne1000_0.8.3-4vmw.670.0.0.8169922, VMW_bootbank_nenic_1.0.11.0-1vmw.670.0.0.8169922, VMW_bootbank_net-bnx2_2.2.4f.v60.10-2vmw.670.0.0.8169922, VMW_bootbank_net-bnx2x_1.78.80.v60.12-2vmw.670.0.0.8169922, VMW_bootbank_net-cdc-ether_1.0-3vmw.670.0.0.8169922, VMW_bootbank_net-cnic_1.78.76.v60.13-2vmw.670.0.0.8169922, VMW_bootbank_net-e1000_8.0.3.1-5vmw.670.0.0.8169922, VMW_bootbank_net-e1000e_3.2.2.1-2vmw.670.0.0.8169922, VMW_bootbank_net-enic_2.1.2.38-2vmw.670.0.0.8169922, VMW_bootbank_net-fcoe_1.0.29.9.3-7vmw.670.0.0.8169922, VMW_bootbank_net-forcedeth_0.61-2vmw.670.0.0.8169922, VMW_bootbank_net-igb_5.0.5.1.1-5vmw.670.0.0.8169922, VMW_bootbank_net-ixgbe_3.7.13.7.14iov-20vmw.670.0.0.8169922, VMW_bootbank_net-libfcoe-92_1.0.24.9.4-8vmw.670.0.0.8169922, VMW_bootbank_net-mlx4-core_1.9.7.0-1vmw.670.0.0.8169922, VMW_bootbank_net-mlx4-en_1.9.7.0-1vmw.670.0.0.8169922, VMW_bootbank_net-nx-nic_5.0.621-5vmw.670.0.0.8169922, VMW_bootbank_net-tg3_3.131d.v60.4-2vmw.670.0.0.8169922, VMW_bootbank_net-usbnet_1.0-3vmw.670.0.0.8169922, VMW_bootbank_net-vmxnet3_1.1.3.0-3vmw.670.0.0.8169922, VMW_bootbank_nhpsa_2.0.22-1vmw.670.0.0.8169922, VMW_bootbank_nmlx4-core_3.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx4-en_3.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx4-rdma_3.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx5-core_4.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_nmlx5-rdma_4.17.9.12-1vmw.670.0.0.8169922, VMW_bootbank_ntg3_4.1.3.0-1vmw.670.0.0.8169922, VMW_bootbank_nvme_1.2.1.34-1vmw.670.0.0.8169922, VMW_bootbank_nvmxnet3-ens_2.0.0.21-1vmw.670.0.0.8169922, VMW_bootbank_nvmxnet3_2.0.0.27-1vmw.670.0.0.8169922, VMW_bootbank_ohci-usb-ohci_1.0-3vmw.670.0.0.8169922, VMW_bootbank_pvscsi_0.1-2vmw.670.0.0.8169922, VMW_bootbank_qcnic_1.0.2.0.4-1vmw.670.0.0.8169922, VMW_bootbank_qedentv_2.0.6.4-10vmw.670.0.17.9214924, VMW_bootbank_qfle3_1.0.50.11-9vmw.670.0.0.8169922, VMW_bootbank_qfle3f_1.0.25.0.2-14vmw.670.0.0.8169922, VMW_bootbank_qfle3i_1.0.2.3.9-3vmw.670.0.0.8169922, VMW_bootbank_qflge_1.1.0.11-1vmw.670.0.0.8169922, VMW_bootbank_sata-ahci_3.0-26vmw.670.0.0.8169922, VMW_bootbank_sata-ata-piix_2.12-10vmw.670.0.0.8169922, VMW_bootbank_sata-sata-nv_3.5-4vmw.670.0.0.8169922, VMW_bootbank_sata-sata-promise_2.12-3vmw.670.0.0.8169922, VMW_bootbank_sata-sata-sil24_1.1-1vmw.670.0.0.8169922, VMW_bootbank_sata-sata-sil_2.3-4vmw.670.0.0.8169922, VMW_bootbank_sata-sata-svw_2.3-3vmw.670.0.0.8169922, VMW_bootbank_scsi-aacraid_1.1.5.1-9vmw.670.0.0.8169922, VMW_bootbank_scsi-adp94xx_1.0.8.12-6vmw.670.0.0.8169922, VMW_bootbank_scsi-aic79xx_3.1-6vmw.670.0.0.8169922, VMW_bootbank_scsi-bnx2fc_1.78.78.v60.8-1vmw.670.0.0.8169922, VMW_bootbank_scsi-bnx2i_2.78.76.v60.8-1vmw.670.0.0.8169922, VMW_bootbank_scsi-fnic_1.5.0.45-3vmw.670.0.0.8169922, VMW_bootbank_scsi-hpsa_6.0.0.84-3vmw.670.0.0.8169922, VMW_bootbank_scsi-ips_7.12.05-4vmw.670.0.0.8169922, VMW_bootbank_scsi-iscsi-linux-92_1.0.0.2-3vmw.670.0.0.8169922, VMW_bootbank_scsi-libfc-92_1.0.40.9.3-5vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid-mbox_2.20.5.1-6vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid-sas_6.603.55.00-2vmw.670.0.0.8169922, VMW_bootbank_scsi-megaraid2_2.00.4-9vmw.670.0.0.8169922, VMW_bootbank_scsi-mpt2sas_19.00.00.00-2vmw.670.0.0.8169922, VMW_bootbank_scsi-mptsas_4.23.01.00-10vmw.670.0.0.8169922, VMW_bootbank_scsi-mptspi_4.23.01.00-10vmw.670.0.0.8169922, VMW_bootbank_scsi-qla4xxx_5.01.03.2-7vmw.670.0.0.8169922, VMW_bootbank_shim-iscsi-linux-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-iscsi-linux-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libata-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libata-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfc-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfc-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfcoe-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-libfcoe-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-1-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-2-0_6.7.0-0.0.8169922, VMW_bootbank_shim-vmklinux-9-2-3-0_6.7.0-0.0.8169922, VMW_bootbank_smartpqi_1.0.1.553-10vmw.670.0.0.8169922, VMW_bootbank_uhci-usb-uhci_1.0-3vmw.670.0.0.8169922, VMW_bootbank_usb-storage-usb-storage_1.0-3vmw.670.0.0.8169922, VMW_bootbank_usbcore-usb_1.0-3vmw.670.0.0.8169922, VMW_bootbank_vmkata_0.1-1vmw.670.0.0.8169922, VMW_bootbank_vmkfcoe_1.0.0.0-1vmw.670.0.0.8169922, VMW_bootbank_vmkplexer-vmkplexer_6.7.0-0.0.8169922, VMW_bootbank_vmkusb_0.1-1vmw.670.0.0.8169922, VMW_bootbank_vmw-ahci_1.2.0-6vmw.670.0.0.8169922, VMW_bootbank_xhci-xhci_1.0-3vmw.670.0.0.8169922, VMware_bootbank_elx-esx-libelxima.so_11.4.1184.0-0.0.8169922, VMware_bootbank_esx-dvfilter-generic-fastpath_6.7.0-0.0.8169922, VMware_bootbank_esx-xserver_6.7.0-0.0.8169922, VMware_bootbank_lsu-hp-hpsa-plugin_2.0.0-13vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-lsi-mr3-plugin_1.0.0-12vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-lsi-msgpt3-plugin_1.0.0-8vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-megaraid-sas-plugin_1.0.0-9vmw.670.0.0.8169922, VMware_bootbank_lsu-lsi-mpt2sas-plugin_2.0.0-7vmw.670.0.0.8169922, VMware_bootbank_native-misc-drivers_6.7.0-0.0.8169922, VMware_bootbank_qlnativefc_3.0.1.0-5vmw.670.0.0.8169922, VMware_bootbank_rste_2.0.2.0088-7vmw.670.0.0.8169922, VMware_bootbank_vmware-esx-esxcli-nvme-plugin_1.2.0.32-0.0.8169922, VMware_locker_tools-light_10.2.1.8267844-8941472
[root@localhost:~]

## Updates überprüfen

Ebenfalls per esxcli können Sie die soeben eingespielten Versionen überprüfen:

[root@localhost:~] esxcli software vib list
Name                           Version                               Vendor  Acceptance Level  Install Date
-----------------------------  ------------------------------------  ------  ----------------  ------------
ata-libata-92                  3.00.9.2-16vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
ata-pata-amd                   0.3.10-3vmw.670.0.0.8169922           VMW     VMwareCertified   2018-08-27
ata-pata-atiixp                0.4.6-4vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
ata-pata-cmd64x                0.2.5-3vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
ata-pata-hpt3x2n               0.3.4-3vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
ata-pata-pdc2027x              1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
ata-pata-serverworks           0.4.3-3vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
ata-pata-sil680                0.4.8-3vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
ata-pata-via                   0.3.3-2vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
block-cciss                    3.6.14-10vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
bnxtnet                        20.6.101.7-11vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
brcmfcoe                       11.4.1078.0-8vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
char-random                    1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
ehci-ehci-hcd                  1.0-4vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
elxiscsi                       11.4.1174.0-2vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
elxnet                         11.4.1094.0-5vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
hid-hid                        1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
i40en                          1.3.1-18vmw.670.0.0.8169922           VMW     VMwareCertified   2018-08-27
iavmd                          1.2.0.1011-2vmw.670.0.0.8169922       VMW     VMwareCertified   2018-08-27
igbn                           0.1.0.0-15vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
ima-qla4xxx                    2.02.18-1vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
ipmi-ipmi-devintf              39.1-4vmw.670.0.0.8169922             VMW     VMwareCertified   2018-08-27
ipmi-ipmi-msghandler           39.1-4vmw.670.0.0.8169922             VMW     VMwareCertified   2018-08-27
ipmi-ipmi-si-drv               39.1-4vmw.670.0.0.8169922             VMW     VMwareCertified   2018-08-27
iser                           1.0.0.0-1vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
ixgben                         1.4.1-11vmw.670.0.0.8169922           VMW     VMwareCertified   2018-08-27
lpfc                           11.4.33.1-6vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
lpnic                          11.4.59.0-1vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
lsi-mr3                        7.702.13.00-4vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
lsi-msgpt2                     20.00.04.00-4vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
lsi-msgpt35                    03.00.01.00-10vmw.670.0.0.8169922     VMW     VMwareCertified   2018-08-27
lsi-msgpt3                     16.00.01.00-1vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
misc-cnic-register             1.78.75.v60.7-1vmw.670.0.0.8169922    VMW     VMwareCertified   2018-08-27
misc-drivers                   6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
mtip32xx-native                3.9.6-1vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
ne1000                         0.8.3-4vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
nenic                          1.0.11.0-1vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
net-bnx2                       2.2.4f.v60.10-2vmw.670.0.0.8169922    VMW     VMwareCertified   2018-08-27
net-bnx2x                      1.78.80.v60.12-2vmw.670.0.0.8169922   VMW     VMwareCertified   2018-08-27
net-cdc-ether                  1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
net-cnic                       1.78.76.v60.13-2vmw.670.0.0.8169922   VMW     VMwareCertified   2018-08-27
net-e1000                      8.0.3.1-5vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
net-e1000e                     3.2.2.1-2vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
net-enic                       2.1.2.38-2vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
net-fcoe                       1.0.29.9.3-7vmw.670.0.0.8169922       VMW     VMwareCertified   2018-08-27
net-forcedeth                  0.61-2vmw.670.0.0.8169922             VMW     VMwareCertified   2018-08-27
net-igb                        5.0.5.1.1-5vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
net-ixgbe                      3.7.13.7.14iov-20vmw.670.0.0.8169922  VMW     VMwareCertified   2018-08-27
net-libfcoe-92                 1.0.24.9.4-8vmw.670.0.0.8169922       VMW     VMwareCertified   2018-08-27
net-mlx4-core                  1.9.7.0-1vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
net-mlx4-en                    1.9.7.0-1vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
net-nx-nic                     5.0.621-5vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
net-tg3                        3.131d.v60.4-2vmw.670.0.0.8169922     VMW     VMwareCertified   2018-08-27
net-usbnet                     1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
net-vmxnet3                    1.1.3.0-3vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
nhpsa                          2.0.22-1vmw.670.0.0.8169922           VMW     VMwareCertified   2018-08-27
nmlx4-core                     3.17.9.12-1vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
nmlx4-en                       3.17.9.12-1vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
nmlx4-rdma                     3.17.9.12-1vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
nmlx5-core                     4.17.9.12-1vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
nmlx5-rdma                     4.17.9.12-1vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
ntg3                           4.1.3.0-1vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
nvme                           1.2.1.34-1vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
nvmxnet3-ens                   2.0.0.21-1vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
nvmxnet3                       2.0.0.27-1vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
ohci-usb-ohci                  1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
pvscsi                         0.1-2vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
qcnic                          1.0.2.0.4-1vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
qedentv                        2.0.6.4-8vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
qfle3                          1.0.50.11-9vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
qfle3f                         1.0.25.0.2-14vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
qfle3i                         1.0.2.3.9-3vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
qflge                          1.1.0.11-1vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
sata-ahci                      3.0-26vmw.670.0.0.8169922             VMW     VMwareCertified   2018-08-27
sata-ata-piix                  2.12-10vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
sata-sata-nv                   3.5-4vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
sata-sata-promise              2.12-3vmw.670.0.0.8169922             VMW     VMwareCertified   2018-08-27
sata-sata-sil24                1.1-1vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
sata-sata-sil                  2.3-4vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
sata-sata-svw                  2.3-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
scsi-aacraid                   1.1.5.1-9vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
scsi-adp94xx                   1.0.8.12-6vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
scsi-aic79xx                   3.1-6vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
scsi-bnx2fc                    1.78.78.v60.8-1vmw.670.0.0.8169922    VMW     VMwareCertified   2018-08-27
scsi-bnx2i                     2.78.76.v60.8-1vmw.670.0.0.8169922    VMW     VMwareCertified   2018-08-27
scsi-fnic                      1.5.0.45-3vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
scsi-hpsa                      6.0.0.84-3vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
scsi-ips                       7.12.05-4vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
scsi-iscsi-linux-92            1.0.0.2-3vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
scsi-libfc-92                  1.0.40.9.3-5vmw.670.0.0.8169922       VMW     VMwareCertified   2018-08-27
scsi-megaraid-mbox             2.20.5.1-6vmw.670.0.0.8169922         VMW     VMwareCertified   2018-08-27
scsi-megaraid-sas              6.603.55.00-2vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
scsi-megaraid2                 2.00.4-9vmw.670.0.0.8169922           VMW     VMwareCertified   2018-08-27
scsi-mpt2sas                   19.00.00.00-2vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
scsi-mptsas                    4.23.01.00-10vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
scsi-mptspi                    4.23.01.00-10vmw.670.0.0.8169922      VMW     VMwareCertified   2018-08-27
scsi-qla4xxx                   5.01.03.2-7vmw.670.0.0.8169922        VMW     VMwareCertified   2018-08-27
shim-iscsi-linux-9-2-1-0       6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-iscsi-linux-9-2-2-0       6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-libata-9-2-1-0            6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-libata-9-2-2-0            6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-libfc-9-2-1-0             6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-libfc-9-2-2-0             6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-libfcoe-9-2-1-0           6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-libfcoe-9-2-2-0           6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-vmklinux-9-2-1-0          6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-vmklinux-9-2-2-0          6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
shim-vmklinux-9-2-3-0          6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
smartpqi                       1.0.1.553-10vmw.670.0.0.8169922       VMW     VMwareCertified   2018-08-27
uhci-usb-uhci                  1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
usb-storage-usb-storage        1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
usbcore-usb                    1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
vmkata                         0.1-1vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
vmkfcoe                        1.0.0.0-1vmw.670.0.0.8169922          VMW     VMwareCertified   2018-08-27
vmkplexer-vmkplexer            6.7.0-0.0.8169922                     VMW     VMwareCertified   2018-08-27
vmkusb                         0.1-1vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
vmw-ahci                       1.2.0-6vmw.670.0.0.8169922            VMW     VMwareCertified   2018-08-27
xhci-xhci                      1.0-3vmw.670.0.0.8169922              VMW     VMwareCertified   2018-08-27
cpu-microcode                  6.7.0-0.0.8169922                     VMware  VMwareCertified   2018-08-27
elx-esx-libelxima.so           11.4.1184.0-0.0.8169922               VMware  VMwareCertified   2018-08-27
esx-base                       6.7.0-0.0.8169922                     VMware  VMwareCertified   2018-08-27
esx-dvfilter-generic-fastpath  6.7.0-0.0.8169922                     VMware  VMwareCertified   2018-08-27
esx-ui                         1.25.0-7872652                        VMware  VMwareCertified   2018-08-27
esx-xserver                    6.7.0-0.0.8169922                     VMware  VMwareCertified   2018-08-27
lsu-hp-hpsa-plugin             2.0.0-13vmw.670.0.0.8169922           VMware  VMwareCertified   2018-08-27
lsu-lsi-lsi-mr3-plugin         1.0.0-12vmw.670.0.0.8169922           VMware  VMwareCertified   2018-08-27
lsu-lsi-lsi-msgpt3-plugin      1.0.0-8vmw.670.0.0.8169922            VMware  VMwareCertified   2018-08-27
lsu-lsi-megaraid-sas-plugin    1.0.0-9vmw.670.0.0.8169922            VMware  VMwareCertified   2018-08-27
lsu-lsi-mpt2sas-plugin         2.0.0-7vmw.670.0.0.8169922            VMware  VMwareCertified   2018-08-27
native-misc-drivers            6.7.0-0.0.8169922                     VMware  VMwareCertified   2018-08-27
qlnativefc                     3.0.1.0-5vmw.670.0.0.8169922          VMware  VMwareCertified   2018-08-27
rste                           2.0.2.0088-7vmw.670.0.0.8169922       VMware  VMwareCertified   2018-08-27
vmware-esx-esxcli-nvme-plugin  1.2.0.32-0.0.8169922                  VMware  VMwareCertified   2018-08-27
vsan                           6.7.0-0.0.8169922                     VMware  VMwareCertified   2018-08-27
vsanhealth                     6.7.0-0.0.8169922                     VMware  VMwareCertified   2018-08-27
tools-light                    10.2.1.8267844-8941472                VMware  VMwareCertified   2018-08-27
[root@localhost:~]

## Reboot durchführen und Wartungsmodus beenden

Führen Sie nun einen Reboot durch:

[root@localhost:~] reboot

Nach dem Reboot beenden Sie den Wartungsmodus:

[root@localhost:~] vim-cmd hostsvc/maintenance_mode_exit