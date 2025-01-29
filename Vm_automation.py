import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import logging

# Loglama ayarı
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vm_automation.log'),
        logging.StreamHandler()
    ]
)

# Kullanıcıya kaydetmek için bir klasör seçtirelim
def select_directory():
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    print("Select Folder for Virtual Machines: ")
    folder_selected = filedialog.askdirectory(title="Select Folder for Virtual Machines")
    root.quit()  # Pencereyi kapat
    return folder_selected

def select_iso_file():
    """ISO dosyasını seçmek için bir dosya açma penceresi gösterir."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select ISO File",
        filetypes=[("ISO Files", "*.iso"), ("All Files", "*.*")]
    )
    root.quit()  # Pencereyi kapat
    if not file_path:
        raise FileNotFoundError("No ISO file selected.")
    file_path = file_path.replace("\\", "\\\\")  # Dosya yolunu düzeltiyoruz
    return file_path

def run_powershell_script(vm_name, guest_os, num_vcpus, cores_per_socket, memory_mb, iso_path, network_type, disk_size, number_ofvm, vmDirectory):
    """PowerShell betiğini çalıştırır."""
    try:
        # PowerShell scriptini çalıştır
        result = subprocess.run(
            ["powershell", "-File", "vmautomation.ps1", 
             "-vmName", vm_name, 
             "-guestOS", guest_os,
             "-numvcpus", str(num_vcpus),
             "-coresPerSocket", str(cores_per_socket),
             "-memoryMB", str(memory_mb),
             "-isoPath", iso_path,
             "-networkType", network_type,
             "-diskSize", str(disk_size),
             "-number_ofvm", str(number_ofvm),
             "-vmDirectory", str(vmDirectory)],
            check=True, capture_output=True, text=True
        )
        logging.info("PowerShell script executed successfully.")
        logging.info(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        # Hata mesajlarını logla
        logging.error(f"PowerShell script execution failed: {e}")
        logging.error(f"Error Output: {e.stderr}")
        # Hata mesajının detaylarıyla tekrar hata fırlat
        raise RuntimeError(f"PowerShell script execution failed. See logs for details. Error: {e.stderr}")

def get_package_choice():
    """Kullanıcıya hazır paket seçeneklerini sunar ve bir seçim yapmasını ister."""
    print("\n==== Select Virtual Machine Package ====")
    packages = {
        '1': ("Lite # 2 CPU, 4GB RAM, 40GB SSD", 2, 1, 4096, 40),    # 2 CPU, 4GB RAM, 40GB SSD
        '2': ("Medium # 4 CPU, 8GB RAM, 60GB SSD", 4, 2, 8192, 60),  # 4 CPU, 8GB RAM, 60GB SSD
        '3': ("Large # 6 CPU, 16GB RAM, 120GB SSD", 6, 2, 16384, 120), # 6 CPU, 16GB RAM, 120GB SSD
        '4': ("Custom", None, None, None) # Custom (Kullanıcı tarafından girilecek)
    }
    for key, value in packages.items():
        print(f"{key}. {value[0]}")
    
    choice = input("Select an option (1-4): ").strip()

    if choice in packages:
        if choice == '4':
            print("\n==== Custom VM Configuration ====")
            # Custom configuration
            cpu_count = int(input("Enter the number of CPUs (e.g., 2, 4): ").strip())
            cores_per_socket = int(input("Enter the number of cores per socket: ").strip())

            # Memory Configuration
            print("Choose memory size (in GB):")
            memory_options = ["1 GB", "2 GB", "4 GB", "8 GB", "Custom"]
            for i, mem in enumerate(memory_options, 1):
                print(f"{i}. {mem}")
            memory_choice = int(input("Select an option (1-5): "))
            if memory_choice == len(memory_options):
                memory_gb = int(input("Enter custom memory size in GB: ").strip())
            else:
                memory_gb = int(memory_options[memory_choice - 1].split()[0])

            # Convert GB to MB
            memory_mb = memory_gb * 1024

            # Disk Size Configuration
            disk_size_options = [20, 40, 60, 80, 100]  # Sabit disk boyutu seçenekleri

            # Kullanıcıya seçenekleri sunma
            print("Choose disk size from the options below or select Custom for a custom value:")
            for i, size in enumerate(disk_size_options, 1):
                print(f"{i}. {size} GB")

            # Son olarak 'Custom' seçeneği ekliyoruz
            print(f"{len(disk_size_options) + 1}. Custom")

            # Kullanıcıdan seçim alma
            selection = input(f"Select an option (1-{len(disk_size_options) + 1}): ").strip()

            # Seçimi işleme
            if selection.isdigit():
                selection = int(selection)
                if 1 <= selection <= len(disk_size_options):  # Eğer kullanıcı seçeneklerden birini seçtiyse
                    disk_size = disk_size_options[selection - 1]
                    print(f"Disk size selected: {disk_size} GB")
                elif selection == len(disk_size_options) + 1:  # 'Custom' seçeneği seçildiyse
                    try:
                        disk_size = int(input("Enter custom disk size in GB: ").strip())
                        print(f"Custom disk size entered: {disk_size} GB")
                    except ValueError:
                        print("Invalid input. Please enter a valid number for the disk size.")
                else:
                    print("Invalid selection, please try again.")
            else:
                print("Invalid input. Please select a valid option.")
            return cores_per_socket, cpu_count, memory_mb, disk_size
        else:
            # Paket seçimi yapıldığında, uygun parametreleri döndür
            package = packages[choice]
            return package[2], package[1], package[3], package[4]  # Default 1 core per processor for these packages

def interactive_create_vm():
    """Kullanıcıdan sanal makine yapılandırması için giriş alır ve PowerShell betiğini çalıştırır."""
    print("\n=== Welcome To Create Virtual Machine Script ===\n ")
    print("# author       : Dilaver Şahin")
    print("# linkedin     : https://www.linkedin.com/in/dilaversahin")
    print("# github       : https://github.com/enesdilaversahin")
    print("# title        : vm_automation.py")
    print("# description  : Create Virtual Machine")
    print("# date         : 29.01.2025")
    print("# version      : 1.0")
    print("#==============================================================================")
    vm_name = input("\n Enter the virtual machine name: ").strip()
    if not vm_name:
        logging.error("VM name cannot be empty.")
        raise ValueError("VM name must be a non-empty string.")
    
    number_ofvm = input("How many virtual machines would you like to create ?: ")
    
    # Kullanıcıya dizin seçtir
    vmDirectory = select_directory()
    
    # Paket seçimini al
    cores_per_socket, cpu_count, memory_mb, disk_size = get_package_choice()
    
    # OS seç
    print("Choose guest OS:")
    guest_os_options = ["windows10-64", "windows11-64", "debian12-64", "ubuntu-64", "centos7-64"]
    for i, os in enumerate(guest_os_options, 1):
        print(f"{i}. {os}")
    guest_os = guest_os_options[int(input("Select an option (1-5): ")) - 1]

    # ISO dosyasını seç
    print("Please select the ISO file:")
    try:
        iso_path = select_iso_file()
        logging.info(f"ISO file selected: {iso_path}")
    except FileNotFoundError as e:
        logging.error(f"{e}")
        raise    

    # Network type seçimi
    print("Choose network type:")
    network_types = ["bridged", "nat", "hostonly"]
    for i, net in enumerate(network_types, 1):
        print(f"{i}. {net}")
    network_type = network_types[int(input("Select an option (1-3): ")) - 1]

    # PowerShell scriptini çalıştır
    run_powershell_script(vm_name, guest_os, cpu_count, cores_per_socket, memory_mb, iso_path, network_type, disk_size, number_ofvm, vmDirectory)

    print(f"Virtual machine created successfully. VM name: {vm_name}")

def main():
    interactive_create_vm()

if __name__ == "__main__":
    main()
