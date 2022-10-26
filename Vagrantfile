# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANT_BOX="debian/bullseye64"

CPUS_WORKER_NODE    = 1
CPUS_PYTHON_NODE    = 2
MEMORY_WORKER_NODE  = 1024
WORKER_NODES_COUNT  = 2
HOSTS=[]
PORTS=["22", "22"]

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|


  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL


  $script = <<-EOF
  apt update && apt install -y openssh-server
  useradd -m -p mla_password -s /bin/bash mla_agent
  usermod -aG sudo mla_agent
  EOF

  # Hosts
  (1..WORKER_NODES_COUNT).each do |i|
    config.vm.define "server-#{i}" do |node|

      node.vm.box               = VAGRANT_BOX
      node.vm.box_check_update  = false
      #node.vm.box_version       = VAGRANT_BOX_VERSION
      node.vm.hostname          = "server-#{i}"

      node.vm.network "private_network", ip: "10.0.100.10#{i}"

      node.vm.provider :virtualbox do |v|
        v.name    = "server-#{i}"
        v.memory  = MEMORY_WORKER_NODE
        v.cpus    = CPUS_WORKER_NODE
      end

      node.vm.provider :libvirt do |v|
        v.memory  = MEMORY_WORKER_NODE
        v.nested  = true
        v.cpus    = CPUS_WORKER_NODE
      end
      node.vm.provision "shell", inline: $script
      node.vm.provision "file", source: "./mla_key.pub", destination: "/tmp/mla_key.pub"
      node.vm.provision "shell", inline: "mkdir /home/mla_agent/.ssh \
       && mv /tmp/mla_key.pub /home/mla_agent/.ssh/mla_key.pub \
       && cat /home/mla_agent/.ssh/mla_key.pub >> /home/mla_agent/.ssh/authorized_keys \
       && chown -R mla_agent:mla_agent /home/mla_agent/.ssh"
    end
  end

  (1..WORKER_NODES_COUNT).each do |i|
    HOSTS.push("10.0.100.10#{i}")
  end
  # Python executer
  config.vm.define "python" do |node|

    node.vm.box               = VAGRANT_BOX
    node.vm.box_check_update  = false
    # node.vm.box_version       = VAGRANT_BOX_VERSION
    node.vm.hostname          = "python"

    node.vm.network "private_network", ip: "10.0.100.100"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
    node.vm.network "forwarded_port", guest: 22, host: 2333

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
    node.vm.provider :virtualbox do |v|
      v.name    = "python"
      v.memory  = MEMORY_WORKER_NODE
      v.cpus    = CPUS_PYTHON_NODE
    end

    node.vm.provider :libvirt do |v|
      v.memory  = MEMORY_WORKER_NODE
      v.nested  = true
      v.cpus    = CPUS_PYTHON_NODE
    end

    node.vm.provision "shell", path: "python.sh"
    node.vm.provision "file", source: "./mla_key", destination: "/tmp/mla_key"
    node.vm.provision "file", source: "./mla_key.pub", destination: "/tmp/mla_key.pub"
    node.vm.provision "shell", inline: "mkdir /home/vagrant/.ssh \
        && mv /tmp/mla_key.pub /tmp/mla_key /home/vagrant/.ssh/ \
        && chown -R vagrant:vagrant /home/vagrant/.ssh \
        && chmod 400 /home/vagrant/.ssh/mla_key.pub /home/vagrant/.ssh/mla_key \
        && mkdir /home/vagrant/mla \
        && chown -R vagrant:vagrant /home/vagrant/mla"
  end

end
