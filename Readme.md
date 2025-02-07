
![Logo](https://via.placeholder.com/600x150?text=Your+Logo+Here+600x150)


# Server Temperature Control Using Raspberry Pi

In this project, we aim to create a temperature controlling system, which uses a Raspberry Pi to control the fan speed, according to the server's temperature. 

## Tools

- Raspberry Pi 3B
- AM2302 (DHT11) Temperature Sensor (Uses one-wire protocol)
- OpenBMC Operating System
- A 2-pin 12V DC Fan
- BC107 Transistor
- USB-UART Converter


## Implementation Details

### Compiling and Using OpenBMC
<div dir="rtl">
1. شرح پروژه

 OpenBMC یک بورد مدیریت سیستم (Baseboard Management Controller) متن‌باز است که برای نظارت و مدیریت سخت‌افزارهای سروری و سیستم‌های جاسازی‌شده استفاده می‌شود. استفاده از Raspberry Pi 3 به عنوان بستر سخت‌افزاری به دلیل هزینه پایین و قابلیت انعطاف در پروژه‌های تحقیقاتی و آموزشی، انتخاب مناسبی می‌باشد.

2. مراحل انجام پروژه

الف) آماده‌سازی محیط

1. نصب بسته‌های مورد نیاز:  
     ابتدا لازم است تا بسته‌های پیش‌نیاز جهت ساخت محیط Yocto و OpenBMC نصب شود. برای این کار از دستورات زیر استفاده می‌شود:  

   ```bash
   sudo apt-get install git-core diffstat unzip texinfo gcc-multilib build-essential chrpath wget
   sudo apt-get install libc6-dev-i386 python3-pip python3-pexpect xterm
   sudo apt-get install debhelper screen setools
   ```
   
ب) کلون کردن مخازن مورد نیاز

2. دریافت سورس OpenBMC:  
   با اجرای دستور زیر کدهای منبع OpenBMC دریافت می‌شوند:  
   ```bash
   git clone https://github.com/openbmc/openbmc.git
   cd openbmc
   ```
   
3. دریافت Yocto poky:  
   مخزن Yocto که پایه ساخت سیستم عامل است را کلون کنید:  
   ```bash
   git clone git://git.yoctoproject.org/poky
   cd poky
   ```

پ) تنظیم محیط ساخت (Build Environment)

4. راه‌اندازی محیط Yocto:  
   با اجرای دستور زیر محیط ساخت برای Raspberry Pi 3 راه‌اندازی می‌شود:
   ```bash
   source oe-init-build-env rpi-build
   ```
ت) افزودن لایه‌های مورد نیاز

5. کلون کردن لایه‌های اضافی:  
   لایه‌های ضروری برای پشتیبانی از Raspberry Pi و بسته‌های پایتون را دریافت نمایید:  
   ```bash
   git clone git://git.yoctoproject.org/meta-raspberrypi ../meta-raspberrypi
   git clone git://git.openembedded.org/meta-openembedded ../meta-openembedded
   ```
   
6. تنظیم فایل bblayers.conf:  
   در این فایل مسیرهای لایه‌های مختلف (مانند:
   - مسیر لایه اصلی Yocto (meta)
   - مسیر meta-poky
   - مسیر meta-raspberrypi  
   ) به درستی درج می‌شود تا Yocto بتواند پکیج‌ها و تنظیمات مربوطه را شناسایی کند.


   در این فایل مسیرهای لایه‌های مختلف به شرح زیر درج می‌شود. مطمئن شوید مسیرها مطابق ساختار دایرکتوری شما باشند:  

   ```bash
   #conf/bblayers.conf
   POKY_BBLAYERS_CONF_VERSION = "2"

   BBPATH = "${TOPDIR}"
   BBFILES ?= ""

   BBLAYERS ?= " \
     /home/ali/openbmc/poky/meta \
     /home/ali/openbmc/poky/meta-poky \
     /home/ali/openbmc/poky/meta-yocto-bsp \
     /home/ali/openbmc/meta-raspberrypi \
     /home/ali/openbmc/meta-openembedded/meta-python \
     /home/ali/openbmc/meta-openembedded/meta-oe \
   "
   ```
ث) پیکربندی نهایی و ساخت تصویر

7. تنظیمات پیکربندی: 
   در فایل `conf/local.conf` تغییراتی به‌منظور تعیین پلتفرم Raspberry Pi 3 اعمال می‌شود:
   - تنظیم متغیر:
     ```
     MACHINE = "raspberrypi3"
     ```
   - پذیرش مجوز مربوط به synaptics-killswitch:
     ```
     LICENSE_FLAGS_ACCEPTED = "synaptics-killswitch"
     ```
   ```bash
   #conf/local.conf
   MACHINE = "raspberrypi3"
   DISTRO = "poky"
   
   IMAGE_INSTALL += " \
       coreutils \
       python3 \
       python3-pip \
       python3-setuptools \
       python3-wheel \
       python3-dev \
       python3-venv \
       gcc \
       g++ \
       make \
       libgcc \
       libstdc++ \
       nano \
   "
   
   LICENSE_FLAGS_ACCEPTED = "synaptics-killswitch"
   ```

8. ساخت تصویر سیستم:
   با استفاده از دستور bitbake، یک تصویر ساخته می‌شود:
   ```bash
   bitbake core-image-full-cmdline
   ```

ج) انتقال تصویر به SD Card و راه‌اندازی

9. نصب تصویر بر روی SD Card:
   پس از اتمام فرایند ساخت، تصویر ساخته شده در مسیر مشخص (مثلاً `/home/ali/openbmc/poky/rpi-build/tmp/deploy/images/raspberrypi3`) قرار دارد. برای انتقال تصویر به SD Card از دستور dd به صورت زیر استفاده می‌شود:
   ```bash
   sudo dd if=/home/ali/openbmc/poky/rpi-build/tmp/deploy/images/raspberrypi3 of=/dev/sdb1 bs=4M status=progress
   ```
   (توجه: مطمئن شوید که مسیر دستگاه مقصد (/dev/sdb1) صحیح انتخاب شده تا از نوشتن تصادفی روی دیسک‌های دیگر جلوگیری شود.)

10. راه‌اندازی Raspberry Pi 3:
    پس از انتقال موفقیت‌آمیز تصویر به SD Card، این کارت را در Raspberry Pi 3 قرار داده و سیستم را روشن کنید. در صورت عدم بروز خطا، Raspberry Pi 3 با محیط OpenBMC بوت شده و آماده استفاده خواهد بود.


3. چالش‌های مواجه شده

- مدیریت وابستگی‌ها و نصب پیش‌نیازها:
  نصب و هماهنگ‌سازی کتابخانه‌های لازم (از جمله ابزارهای ساخت Yocto) ممکن است به دلیل نسخه‌های مختلف توزیع‌های لینوکسی با چالش‌هایی مواجه شود.

- پیکربندی فایل‌های build:
  تنظیم دقیق فایل‌های `bblayers.conf` و `local.conf` برای شناسایی صحیح لایه‌ها و تعیین پلتفرم (MACHINE) از مهم‌ترین مراحل است؛ هرگونه اشتباه در این فایل‌ها منجر به خطاهای ساخت می‌شود.

- مشکلات در فرایند ساخت:
  استفاده از bitbake ممکن است خطاهایی ناشی از ناسازگاری یا تنظیمات ناقص به همراه داشته باشد. بررسی لاگ‌های ساخت برای رفع اشکال الزامی است.

- انتقال تصویر به SD Card:
  استفاده از دستور dd نیازمند دقت بالایی است؛ اشتباه در انتخاب دستگاه مقصد می‌تواند منجر به از دست رفتن اطلاعات روی دیسک‌های دیگر شود.

4. توضیحات درباره کد و دستورات

- دستور git clone:
  این دستور برای دریافت کدهای منبع از مخازن GitHub و مخازن Yocto استفاده می‌شود. هر یک از این مخازن شامل بخش‌های مهم پروژه (OpenBMC، لایه‌های Yocto، پیکربندی‌های مربوط به Raspberry Pi) هستند.

- اجرای source oe-init-build-env:
  این دستور محیط ساخت Yocto را راه‌اندازی می‌کند و متغیرهای محیطی لازم برای اجرای دستور bitbake تنظیم می‌شود.

- تنظیمات در bblayers.conf و local.conf:  
  در فایل bblayers.conf مسیرهای لایه‌های مورد نیاز برای ساخت به Yocto معرفی می‌شود. در فایل local.conf نیز تنظیمات مربوط به پلتفرم هدف (مانند MACHINE) و پذیرش مجوزهای لازم انجام می‌شود.

- دستور bitbake:  
  با اجرای این دستور (به عنوان مثال `bitbake core-image-minimal`) فرایند ساخت یک تصویر سیستم عامل مینیمال آغاز می‌شود که شامل اجزای اصلی OpenBMC است.

- دستور dd: 
  این دستور برای انتقال تصویر ساخته شده به SD Card استفاده می‌شود. پارامترهای آن (bs=4M و status=progress) کمک می‌کنند تا فرایند انتقال با سرعت بالا و با نمایش وضعیت پیشرفت انجام شود.





5. تفسیر نتایج و نتیجه‌گیری

پس از اجرای موفق مراحل بالا، نتیجه مورد انتظار به شرح زیر است:

- بوت موفق سیستم:
  Raspberry Pi 3 پس از قرار دادن SD Card و روشن شدن، باید به درستی با محیط OpenBMC بوت شده و صفحه‌ی مدیریت یا پیام‌های بوت را نمایش دهد.

- بررسی لاگ‌ها: 
  مشاهده لاگ‌های سیستم می‌تواند نشان دهد که مراحل ساخت و انتقال تصویر بدون خطا انجام شده و سیستم به درستی راه‌اندازی شده است.

- رفع چالش‌ها:
  در صورت بروز هرگونه خطا در هر مرحله (ساخت، پیکربندی یا انتقال تصویر) با بررسی دقیق لاگ‌ها و مستندات مرتبط، می‌توان اقدامات اصلاحی لازم را انجام داد.

- کاربرد پروژه:
  این پروژه به عنوان یک نمونه کاربردی از استفاده از محیط Yocto برای ساخت سیستم‌های جاسازی‌شده و بهره‌گیری از OpenBMC برای مدیریت سخت‌افزار، قابلیت اطمینان و انعطاف‌پذیری را نشان می‌دهد.
</div>

#### Some notes on starting and using Raspberry Pi3 Model B with OpenBMC installed
Although the default username and password for OpenBMC are `root` and `0penBmc`, we weren't able to login with these credentials. Instead, we edited the `/etc/shadow` file so that the root does not have any password. 

### Interacting with Raspberry Pi 3 B using your system

A challenging part of the project was to connect Raspberry Pi to your PC and interact it using tools such as `PuTTY` (Windows) or `screen` (linux). Here is the descriptions for `PuTTY`, but it is not so different for other terminal emulators

Wires connection:
- Get a uart to usb converter.
- connect Rx of converter to Pin No. 8 of Rpi (Tx of Rpi)
- connect Tx of converter to Pin No. 10 of Rpi (Rx of Rpi)
- connect GND of converter to any GND of Rpi, for example Pin No. 6

Add these to config.txt of boot of rpi (in the memory card):
- `enable_uart=1`
- `dtoverlay=disable-bt`
- `core_freq=250`

Add this line somewhere in /etc/inittab:
```
T0:2345:respawn:/sbin/getty -L ttyAMA0 115200 vt100
```

also, cmdline.txt should be this:
```
console=ttyAMA0,115200 root=/dev/mmcblk0p2 rootfstype=ext4 fsck.repair=yes rootwait S
```

To connect the RPi to your pc, you can use PuTTY in windows or screen in linux.
First, turn off the rpi if it is on.
Then, connect the UART-USB converter to your PC.
Then using device manager in windows, find the COM# port corresponding to the converter (mine was COM11).
Then, connect to putty with the following configuration:


 
Now, you can turn on the rpi. You can do it by plugging its power to one of the USB ports of your own computer. Now, you can use it!


## Authors
- [Ali Ansari](https://github.com/allliance)
- [Bahar DibaeiNia](https://github.com/bhrdbn)
- [Ali Hezaveh](https://github.com/Sharif-University-ESRLab)

