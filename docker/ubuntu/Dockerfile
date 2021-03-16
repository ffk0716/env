FROM rastasheep/ubuntu-sshd

############ zsh env setup ############ 
# Avoid "Restart services during package upgrades without asking?"
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt update && apt install -y --no-install-recommends \
        curl \
        zsh \
        git \
        powerline fonts-powerline \
        locales
# install oh-my-zsh and custom plugins
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
RUN chsh -s /bin/zsh
RUN git clone https://github.com/bhilburn/powerlevel9k.git     ~/.oh-my-zsh/custom/themes/powerlevel9k
RUN git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
# setup ssh
COPY ssh/ /root/.ssh
# setup zshrc
RUN git clone git@github.com:ffk0716/env.git /root/env
RUN echo "source /root/env/shell/zshrc.ubuntu" > /root/.zshrc
# setup lang
RUN locale-gen "en_US.UTF-8"

############ setup vim ############ 
RUN apt update && apt install -y --no-install-recommends \
        vim \
        cscope ctags
RUN /root/env/install.sh
