# VMware Otomasyon Scripti

Bu Python scripti, **VMware Workstation** veya **VMware Player** üzerinde sanal makineleri otomatik olarak oluşturmanıza yardımcı olur. **Tam otomatik** bir kurulum yapmak için **Autounattended.xml** dosyasına ihtiyacınız olacak. Bu dosya, Windows işletim sisteminin kurulumunu tamamen otomatikleştirir.

## Gereksinimler

- **VMware Workstation** veya **VMware Player** yüklü olmalıdır.
- **Python 3.x** yüklü olmalıdır.
- **Windows ISO** dosyasına ihtiyacınız olacak.
- **Autounattended.xml** dosyasını oluşturmanız gerekmektedir.

## Kurulum

1. Bu repository'yi bilgisayarınıza **ZIP** olarak indirin veya **git clone** ile klonlayın.
2. Terminal ya da komut istemcisini açın ve script'in bulunduğu dizine gidin.

## Autounattended.xml Dosyasının Oluşturulması

**Autounattended.xml** dosyası, Windows kurulumunu tamamen otomatik hale getiren bir XML yapılandırma dosyasıdır. Bu dosya, Windows kurulumu sırasında kullanıcı etkileşimi gerektirmeden, gerekli ayarların (dil, saat dilimi, kullanıcı adı, şifre, vb.) otomatik olarak yapılmasını sağlar.

### **Nasıl Yapılır?**

1. **Autounattended.xml Dosyasını Oluşturun:**
   - [Autounattended Generator](https://schneegans.de/windows/unattend-generator/) adresine gidin.
   - Bu site, Windows kurulumunuz için gerekli tüm otomatikleştirilmiş ayarları yapmanıza yardımcı olur.
   - Siteyi kullanarak **autounattended.xml** dosyasını oluşturduktan sonra, bu dosyayı bilgisayarınıza indirin.

2. **Autounattended.xml Dosyasını ISO’ya Dahil Etme:**
   - **ISO'yu düzenlemeniz gerekiyor**. ISO içindeki kurulum dosyalarına `autounattended.xml` dosyasını yerleştirmeniz gerekecek. Bunun için **AnyBurn** veya **NTLite** gibi araçları kullanabilirsiniz.
   - **AnyBurn** kullanarak ISO dosyasını açıp, `autounattended.xml` dosyasını doğru dizine (genellikle `sources` klasörü) yerleştirebilirsiniz.
   
   **Özetle:**
   - **Autounattended.xml** dosyasını oluşturun.
   - ISO'nun içine bu dosyayı uygun klasöre ekleyin.
   - Yeni ISO’yu kaydedin ve sanal makinenizde kullanın.

## Press.ps1 Scripti ile ISO’yu Düzenleme

Windows kurulum sırasında, ISO’yu başlattığınızda **"Press any key to boot from CD or DVD"** mesajı ile karşılaşırsınız. Bu, kurulumun başlamadan önce kullanıcıdan bir tuşa basmasını isteyen bir ekran olup, tam otomatik bir kurulum için bu ekranın atlanması gerekir. Bunun için **press.ps1** adlı bir PowerShell scripti kullanılır.

### **Nasıl Yapılır?**

1. **Press.ps1 Scriptini Edinin:**
   - **press.ps1** scripti, ISO’yu düzenlemenize yardımcı olan bir PowerShell betiğidir. Bu script, ISO’nun başlangıcındaki "Press any key" ekranını atlamanızı sağlar.
   - Bu dosyayı genellikle bir kaynaktan indirmeniz gerekir. (Eğer elinizde yoksa, internette **press.ps1** scriptini bulabilirsiniz.)

2. **Press.ps1 Scriptini Çalıştırma:**
   - **PowerShell**'i açın ve **press.ps1** dosyasını çalıştırarak ISO’yu düzenleyeceksiniz.
   - PowerShell penceresine şu komutları girin (ISO'nun tam yolunu belirttiğinizden emin olun):
   
     ```powershell
     Örnek kullanım: .\press.ps1 -SourceISOPath "C:\Users\enes\Desktop\win.ISO" -UnattendedISOPath "C:\Users\enes\Desktop\unattended.ISO"
     ```

   Bu işlem, ISO içerisindeki kurulum dosyalarını değiştirerek "Press any key" ekranını atlayacak şekilde yapılandırır.

3. **Alternatif Yöntem: ISO’yu Manuel Düzenleme:**
   Eğer **press.ps1** scripti ile işlem yapmak istemiyorsanız, ISO’yu manuel olarak da düzenleyebilirsiniz:
   - ISO’yu açın ve `\efi\microsoft\boot` dizininde **efisys.bin** ve **cdboot.efi** dosyalarını silin.
   - **efisys_noprompt.bin** dosyasını **efisys.bin** olarak yeniden adlandırın.
   - **cdboot_noprompt.efi** dosyasını **cdboot.efi** olarak yeniden adlandırın.
   - Sonrasında, **NTLite** veya başka bir ISO düzenleme aracıyla yeni ISO dosyasını oluşturun.

## Kullanım

1. **Sanal Makine Oluşturma:**

   Terminalde aşağıdaki komutu çalıştırarak script'i başlatın:

   ```bash
   python vm_automation.py
