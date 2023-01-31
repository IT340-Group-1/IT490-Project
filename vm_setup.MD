- Download Ubuntu Desktop ISO image
	- https://ubuntu.com/download/desktop
	- Not sure if it would be better to download [Ubuntu Server](https://ubuntu.com/download/server) (?)
	- 22.04.1 LTS
-
- Install VirtualBox
	- https://www.virtualbox.org/
- Create a new virtual machine
	- **M**achine - > **N**ew...
		- **N**ame:
			- UbuntuBackend490
			- UbuntuFrontend490
			- UbuntuDatabase490
			- UbuntuMessaging490
		- **I**SO Image: ubuntu-22.04.1-desktop-amd64.iso file downloaded above
		- **N**ext
		- Pass**w**ord and **R**epeat Password:
		- **N**ext
		- Base **M**emory: 4096 MB
		- **P**rocessors: 2
		- **N**ext
		- D**i**sk Size: 100 GB
		- **N**ext
		- **F**inish
		- Wait without touching for a long time until you see vboxuser in the middle of the virtual machine screen.
		- Log in as vboxuser using the password from above.
-
- Set up Ubuntu including installing Guest Additions...
	- In Terminal:
	  ```
	  su -
	  sudo adduser vboxuser sudo
	  exit
	  ```
	- Devices -> Insert Guest Additions CD image...
	- In Terminal:
	  ```
	  cd /media
	  cd vboxuser
	  cd VBOX_GA*
	  sudo ./VBoxLinuxAdditions.run
	  ```