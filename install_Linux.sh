#!/bin/bash
####################################################################################################
echo "Checking for Anaconda ..."
if command -v anaconda >/dev/null 2>&1; then
	echo $(anaconda -V)
	echo ""
	# installation path
	cond=0
	while [ $cond -eq 0 ]; do
		echo "--------------------------------------------------------------------------------------"
		echo "The default path to install Tiitba is " $HOME ", press [ENTER] to accept or type the new installation path: "
		read npath
		if [ -z "$npath" ]; then 
			inpath=$HOME
			tiitba=$inpath/tiitba
			mkdir -p $tiitba
			cond=1
		else
			inpath=$npath
			if [ -d $inpath ]; then
				tiitba=$inpath/tiitba
				mkdir -p $tiitba
				cond=1
			else
				cond=0
				echo "Type a correct installation path"
			fi
		fi
	done

	cp -fr bin/ Images/ LICENSE tiitba_env.yml README.md  $tiitba
	# Python dependences for Anaconda Users 
	echo "--------------------------------------------------------------------------------------"
	echo 'Creating python environment and Installing Dependencies"'

	conda env create -f tiitba_env.yml

	echo "--------------------------------------------------------------------------------------"
	echo ""
	echo 'Ready!'
	cd 
	echo '# Add by Tiitba MX' >> .bashrc && echo 'export PATH=$PATH:'$inpath'/tiitba/bin' >> .bashrc
	cd $tiitba/bin
	chmod +x execute.sh tiitbaGUI.py AdditionalModules.py && cd 
	echo "--------------------------------------------------------------------------------------" 
	##  Desktop application
	read -p  "Do you want to create a desktop application [tiitba will be appear on the menu and the search manager] (y/n)" yn
	yn=${yn,,}
	if [ $yn == y ] ; then
		echo [Desktop Entry] >> tiitba.desktop
		echo Type=Application >> tiitba.desktop
		echo Terminal=false >> tiitba.desktop
		echo Name=Tiitba-GUI >> tiitba.desktop
		echo Icon=$tiitba/Images/logo.png >> tiitba.desktop
		echo Exec=$tiitba/bin/execute.sh >> tiitba.desktop
		mv tiitba.desktop $HOME/.local/share/applications/
		echo "Tiitba successfully installed"
	elif [ $yn == n ] ; then
		echo "To run Tiitba GUI, activate environment with :"
		echo " # conda activate tiitba"
		echo "Then run the command tiibaGUI.py to start the GUI"
	else
		echo "Please answer 'y' or 'n'"
	fi

else
	echo >&2 "Anaconda required and it's not installed "
	echo 'Did you want to install it now? (y/n) : '
	read ans
	ans=${ans,,}
	if [ $ans == y ] ; then
		file=$(curl -s https://repo.anaconda.com/archive/ | grep Anaconda3- | grep Linux-x86_64 | cut -d\" -f2)
		url='https://repo.anaconda.com/archive/'$file
		wget $url
		bash Anaconda3*-Linux-x86_64*
		rm Anaconda*
		########################################
	# installation path
	cond=0
	while [ $cond -eq 0 ]; do
		echo "--------------------------------------------------------------------------------------"
		echo "The default path to install Tiitba is " $HOME ", press [ENTER] to accept or type the new installation path: "
		read npath

		if [ -z "$npath" ]; then 
			inpath=$HOME
			tiitba=$inpath/tiitba
			mkdir -p $tiitba
			cond=1
		else
			inpath=$npath
			if [ -d $inpath ]; then
				tiitba=$inpath/tiitba
				mkdir -p $tiitba
				cond=1
			else
				cond=0
				echo "Type a correct installation path"
			fi
		fi
	done

	cp -fr bin/ Images/ LICENSE tiitba_env.yml README.md  $tiitba
	# Python dependences for Anaconda Users 
	echo "--------------------------------------------------------------------------------------"
	echo 'Creating python environment and Installing Dependencies"'

	conda env create -f tiitba_env.yml

	echo "--------------------------------------------------------------------------------------"
	echo ""
	echo 'Ready!'
	cd 
	echo '# Add by Tiitba MX' >> .bashrc && echo 'export PATH=$PATH:'$inpath'/tiitba/bin' >> .bashrc
	cd $tiitba/bin
	chmod +x execute.sh tiitbaGUI.py AdditionalModules.py && cd 
	echo "--------------------------------------------------------------------------------------"
	##  Desktop application
	read -p  "Do you want to create a desktop application [tiitba will be appear on the menu and the search manager] (y/n)" yn
	yn=${yn,,}
	if [ $yn == y ] ; then
		echo [Desktop Entry] >> tiitba.desktop
		echo Type=Application >> tiitba.desktop
		echo Terminal=false >> tiitba.desktop
		echo Name=Tiitba-GUI >> tiitba.desktop
		echo Icon=$tiitba/Images/logo.png >> tiitba.desktop
		echo Exec=$tiitba/bin/execute.sh >> tiitba.desktop
		mv tiitba.desktop $HOME/.local/share/applications/
		echo "Tiitba successfully installed"
	elif [ $yn == n ] ; then
		echo "To run Tiitba GUI, activate environment with :"
		echo " # conda activate tiitba"
		echo "Then run the command tiibaGUI.py to start the GUI"
	else
		echo "Please answer 'y' or 'n'"
	fi

	else 
		echo "<---We strongly suggest install it to run Tiitba GUI, otherwise it may not work properly--->"
		echo "<---You can download it from: https://www.anaconda.com/distribution/ --->"
		echo "<---Also install OpenCV, pillow, and Obpsy libraries--->"
	 	exit 1; 
	fi

fi
