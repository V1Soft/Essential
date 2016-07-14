# Essential
A **High-Level Compiled** Programming Language with **elegance** and **efficiency** all rolled into one...

## Dependencies  
- [**Python**](https://www.python.org)
  - How to get **Python**:
    - **pacman** ([**Arch Linux**](https://www.archlinux.org)) ` $ sudo pacman -S python3 `
    - **apt** ([**Debian**](https://www.debian.org) or [similar](https://en.wikipedia.org/wiki/Deb_(file_format)), some distros claim it doesn't work) ` $ sudo apt-get install python3 `
    - **yum** (**Red Hat** ([**Fedora**](https://getfedora.org)) or [similar](https://en.wikipedia.org/wiki/RPM_Package_Manager)) ` $ yum -y install python33 `
    - **other**:
      ```sh
      $ wget https://www.python.org/ftp/python/3.4.5/Python-3.4.5.tar.xz
      ```

      ```sh
      $ xz -d Python-3.4.5.tar.xz
      ```

      ```sh
      $ tar -xf Python-3.4.5.tar
      ```

      ```sh
      $ cd Python-3.4.5/
      ```

      ```sh
      $ ./configure && make && make install
      ```

- [**NASM**](http://www.nasm.us)
  - How to get **NASM**:
    - **pacman** ([**Arch Linux**](https://www.archlinux.org)) ` $ sudo pacman -S nasm `
    - **apt** ([**Debian**](https://www.debian.org) or [similar](https://en.wikipedia.org/wiki/Deb_(file_format))) ` $ sudo apt-get install nasm `
    - **yum** (**Red Hat** ([**Fedora**](https://getfedora.org)) or [similar](https://en.wikipedia.org/wiki/RPM_Package_Manager)) ` $ yum -y install nasm `
    - **other**:
      ```sh
      $ wget http://www.nasm.us/pub/nasm/releasebuilds/2.12.02/nasm-2.12.02.tar.xz
      ```
      
      ```sh
      $ xz -d nasm-2.12.02.tar.xz
      ```
      
      ```sh
      $ tar -xf nasm-2.12.02.tar
      ```
      
      ```sh
      $ cd nasm-2.12.02
      ```
      
      ```sh
      $ ./configure && make && make install
      ```

## What is Essential?  
Essential is a programming language geared toward **simplicity** and **convenience**. It specifically targets **data use**, and features *no* **typing system**.  

## Why another language?  
I have encountered more languages than I know how to deal with, and I have seen good features and bad. **High-level** languages were always my favorite, as they are easy to program in; however, most are not **compiled** to **native** code. Essential tries to provide a **high-level** *and* **compiled** alternative for all programmers.  

## Is Essential Compatible with C?  
No. Essential allows **header** and **source** files to be combined. Unlike **packages**, Essential allows the importing of specific **functions**, like a **header** file would. Also, C is **low-level** in today's **standards**; therefore, Essential has a simplified **standard** to follow **modern** uses.  

## What is some example code?
Currently, the **compiler** is problematic; however, eventually the following **code** will be an accurate **example**.  
```
use essl.system.io: print() # Actual Location may change

subroutine main # A subroutine is a function, a just had a problem with the definition
  print("Hello World!\n")
end
```

## How do I start?
**Documentation** is still in the works. While the **code** is **commented** explaining each **process**, it has recently become out of control. If you would like to help, let me know at software.vector1@gmail.com and wait until full, concise **documentation** is produced.  
