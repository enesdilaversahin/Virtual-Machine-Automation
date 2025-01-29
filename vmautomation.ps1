param (
    [string]$vmName,
    [string]$guestOS,
    [int]$numvcpus,
    [int]$coresPerSocket,
    [int]$memoryMB,
    [string]$isoPath,
    [string]$networkType,
    [int]$diskSize,
    [int]$cpuCount,
    [int]$number_ofvm,
	[string]$vmDirectory
)

# Define paths to VMware Workstation Pro
$vmrunPath = "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"
$vdiskManagerPath = "C:\Program Files (x86)\VMware\VMware Workstation\vmware-vdiskmanager.exe"
$vmwarePath = "C:\Program Files (x86)\VMware\VMware Workstation\vmware.exe"

# Virtual machine configuration
$vcpuCount = $numvcpus
$memoryGB = $memoryMB  # Direct division without ceiling
$diskSizeGB = $diskSize

# Function to generate a new UUID
function Generate-NewUUID {
    [guid]::NewGuid().ToString().ToUpper()
}

# Function to generate a new genID
function Generate-NewGenID {
    [guid]::NewGuid().ToString().Replace("-", "").ToUpper()
}

# Define paths
$basePath = $vmDirectory  # Aktif kullanıcının VG0 dizini

# Loop through each virtual machine to create and configure them
for ($i = 1; $i -le $number_ofvm; $i++) {
    $currentVMName = "$vmName$i"  # Her sanal makineye benzersiz bir isim atıyoruz (ad1, ad2, ...)
    
    # Virtual machine directory path
    $vmPath = Join-Path -Path $basePath -ChildPath $currentVMName

    # Ensure VM directory exists
    if (-Not (Test-Path $vmPath)) {
        New-Item -Path $vmPath -ItemType Directory | Out-Null
        Write-Output "Created directory: $vmPath"
    } else {
        Write-Output "Directory already exists: $vmPath"
    }

    # Paths to the VMX file and VMDK file
    $vmxFilePath = Join-Path -Path $vmPath -ChildPath "$currentVMName.vmx"
    $vmdkFilePath = Join-Path -Path $vmPath -ChildPath "$currentVMName.vmdk"
    $nvramFilePath = Join-Path -Path $vmPath -ChildPath "$currentVMName.nvram"

    # Generate new UUIDs and genIDs
    $newUUID = Generate-NewUUID
    $newGenID = Generate-NewGenID
    $newGenIDX = Generate-NewGenID

    # VMX content
    $vmxContent = @"
.encoding = "windows-1254"
config.version = "8"
virtualHW.version = "21"
mks.enable3d = "TRUE"
pciBridge0.present = "TRUE"
pciBridge4.present = "TRUE"
pciBridge4.virtualDev = "pcieRootPort"
pciBridge4.functions = "8"
pciBridge5.present = "TRUE"
pciBridge5.virtualDev = "pcieRootPort"
pciBridge5.functions = "8"
pciBridge6.present = "TRUE"
pciBridge6.virtualDev = "pcieRootPort"
pciBridge6.functions = "8"
pciBridge7.present = "TRUE"
pciBridge7.virtualDev = "pcieRootPort"
pciBridge7.functions = "8"
vmci0.present = "TRUE"
hpet0.present = "TRUE"
nvram = "$nvramFilePath"
virtualHW.productCompatibility = "hosted"
powerType.powerOff = "soft"
powerType.powerOn = "soft"
powerType.suspend = "soft"
powerType.reset = "soft"
displayName = "$currentVMName"
usb.vbluetooth.startConnected = "TRUE"
firmware = "efi"
sensor.location = "pass-through"
guestOS = "$guestOS"
tools.syncTime = "FALSE"
sound.autoDetect = "TRUE"
sound.virtualDev = "hdaudio"
sound.fileName = "-1"
sound.present = "TRUE"
numvcpus = "$vcpuCount"
cpuid.coresPerSocket = "$cpuCount"
monitor.virtual_mmu = "hardware"
monitor.virtual_msr = "hardware"
memsize = "$memoryGB"
mem.hotadd = "TRUE"
sata0.present = "TRUE"
nvme0.present = "TRUE"
nvme0:0.fileName = "$currentVMName.vmdk"
nvme0:0.present = "TRUE"
sata0:1.deviceType = "cdrom-image"
sata0:1.fileName = "$isoPath"
sata0:1.present = "TRUE"
usb.present = "TRUE"
ehci.present = "TRUE"
usb_xhci.present = "TRUE"
svga.graphicsMemoryKB = "8388608"
ethernet0.addressType = "generated"
ethernet0.virtualDev = "e1000e"
ethernet0.present = "TRUE"
ethernet0.connectionType = "$networkType"
floppy0.present = "FALSE"
vmxstats.filename = "$currentVMName.scoreboard"
numa.autosize.cookie = "20022"
numa.autosize.vcpu.maxPerVirtualNode = "2"
uuid.bios = "$newUUID"
uuid.location = "$newUUID"
vm.genid = "$newGenID"
vm.genidX = "$newGenIDX"
"@

    # Create the VMX file
    try {
        Set-Content -Path $vmxFilePath -Value $vmxContent -ErrorAction Stop
        Write-Output "VMX file created: $vmxFilePath"
    } catch {
        Write-Error "Failed to create VMX file: $_"
        exit 1
    }

    # Create the disk
    try {
        $createDiskCommand = "& `"$vdiskManagerPath`" -c -s ${diskSizeGB}GB -a lsilogic -t 0 `"$vmdkFilePath`""
        Invoke-Expression $createDiskCommand
        Write-Output "Disk created: $vmdkFilePath"
    } catch {
        Write-Error "Failed to create disk: $_"
        exit 1
    }

    # Start VMware Workstation to add the VM to the library
    try {
        Start-Process -FilePath $vmwarePath -ArgumentList "`"$vmxFilePath`"" -Wait
        Start-Sleep -Seconds 6  # Wait for 5 seconds
        Write-Output "Virtual machine '$currentVMName' has been added to VMware Workstation."
    } catch {
        Write-Error "Failed to open VMware Workstation: $_"
        exit 1
    }

    # Start the virtual machine
    try {
        Start-Process -FilePath $vmrunPath -ArgumentList "start `"$vmxFilePath`" nogui" -Wait
        Write-Output "Virtual machine '$currentVMName' started."
    } catch {
        Write-Error "Failed to start virtual machine: $_"
        exit 1
    }
}

Write-Output "Script completed. Press any key to continue."
Read-Host
