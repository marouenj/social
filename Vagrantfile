$script = <<SCRIPT
sudo apt-get update

sudo apt-get -y install git

sudo apt-get -y install \
     build-essential \
     python3 \
     python3-dev \
     python3-pip

sudo pip3 install --upgrade pip
sudo pip3 install jellyfish
sudo pip3 install pyquery
SCRIPT

Vagrant.configure("2") do |default|
	default.vm.box = "ubuntu/trusty64"
	default.vm.hostname = "social"

	# shell provisioning
	default.vm.provision "shell", inline: $script

	# shell provisioning
	default.vm.provision "docker", images: ["mysql:5.7.16"]

	default.vm.provider "virtualbox" do |vbox|
		vbox.name = "social"
		vbox.memory = 1024
	end
end
