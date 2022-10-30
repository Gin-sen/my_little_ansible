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


  $user_script = <<-EOF
  apt update && apt install -y openssh-server

  useradd -m -s /bin/bash mla_agent
  echo -e "mla_password\nmla_password" | passwd mla_agent
  usermod -aG sudo mla_agent
  usermod -aG root mla_agent

  useradd -m -s /bin/bash nokey_user
  echo -e "nokey_password\nnokey_password" | passwd nokey_user
  usermod -aG sudo nokey_user

  useradd -m -s /bin/bash key_user
  echo -e "key_password\nkey_password" | passwd key_user
  usermod -aG sudo key_user
  EOF

    $ssh_script = <<-EOF
  mkdir -p /home/mla_agent/.ssh
  mv /tmp/mla_key.pub /home/mla_agent/.ssh/mla_key.pub
  cat /home/mla_agent/.ssh/mla_key.pub >> /home/mla_agent/.ssh/authorized_keys
  chown -R mla_agent:mla_agent /home/mla_agent/.ssh

  mkdir -p /home/nokey_user/.ssh
  chown -R nokey_user:nokey_user /home/nokey_user/.ssh
  sed -i 's/^PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config

  mkdir -p /home/key_user/.ssh
  cp /home/mla_agent/.ssh/mla_key.pub /home/key_user/.ssh/user_key.pub
  cat /home/key_user/.ssh/user_key.pub >> /home/key_user/.ssh/authorized_keys
  chown -R key_user:key_user /home/key_user/.ssh

  systemctl restart ssh.service
  EOF
  # Hosts
  (1..WORKER_NODES_COUNT).each do |i|
    config.vm.define "server-#{i}" do |node|

      node.vm.box               = VAGRANT_BOX
      node.vm.box_check_update  = false
      #node.vm.box_version       = VAGRANT_BOX_VERSION
      node.vm.hostname          = "server-#{i}"

      #node.vm.network "private_network", ip: "192.168.56.10#{i}"
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
      node.vm.provision "shell", inline: $user_script
      node.vm.provision "file", source: "./mla_key.pub", destination: "/tmp/mla_key.pub"
      node.vm.provision "file", source: "./user_key.pub", destination: "/tmp/user_key.pub"
      node.vm.provision "shell", inline: $ssh_script
    end
  end

  # Python executer
  config.vm.define "python" do |node|

    node.vm.box               = VAGRANT_BOX
    node.vm.box_check_update  = false
    # node.vm.box_version       = VAGRANT_BOX_VERSION
    node.vm.hostname          = "python"

    #node.vm.network "private_network", ip: "192.168.56.100"
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

    $python_ssh_script = <<-EOF
        mkdir -p /home/vagrant/.ssh
        mv /tmp/mla_key.pub /tmp/mla_key /home/vagrant/.ssh/
        mv /tmp/user_key.pub /tmp/user_key /home/vagrant/.ssh/

        chown -R vagrant:vagrant /home/vagrant/.ssh
        chmod 400 /home/vagrant/.ssh/mla_key.pub /home/vagrant/.ssh/mla_key \
                  /home/vagrant/.ssh/user_key.pub /home/vagrant/.ssh/user_key

        mkdir -p /home/vagrant/mla
        chown -R vagrant:vagrant /home/vagrant/mla
        EOF
    node.vm.provision "shell", path: "python.sh"
    node.vm.provision "file", source: "./mla_key", destination: "/tmp/mla_key"
    node.vm.provision "file", source: "./mla_key.pub", destination: "/tmp/mla_key.pub"
    node.vm.provision "file", source: "./user_key", destination: "/tmp/user_key"
    node.vm.provision "file", source: "./user_key.pub", destination: "/tmp/user_key.pub"
    node.vm.provision "shell", inline: $python_ssh_script
  end

end
