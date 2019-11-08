pyenv安装
=========
- pyenv 安装
 
 .. code-block:: bash
 
  yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel git -y
  mkdir ~/.pyenv
  git clone git://github.com/yyuu/pyenv.git ~/.pyenv 
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc 
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc 
  echo 'eval "$(pyenv init -)"' >> ~/.bashrc 
  exec $SHELL -l
  #加速下载
  v=3.6.5;wget http://mirrors.sohu.com/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v 
  #gitlab推荐方式
  curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
  pyenv update
 
- virtualenv安装

 .. code-block:: bash
  
  git clone https://github.com/yyuu/pyenv-virtualenv.git  ~/.pyenv/plugins/pyenv-virtualenv
  echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
  source ~/.bash_profile
