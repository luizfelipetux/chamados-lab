# Instalação do Alpine Linux Virtual x86_64 no Proxmox VE

Roteiro de instalação do **Alpine Linux – edição Virtual x86_64** em uma máquina virtual criada no **Proxmox VE**.

A edição **Virtual** é adequada para este laboratório por ser pequena e voltada à execução em ambientes virtualizados.

> Neste cenário, o Proxmox VE está sendo executado dentro do VirtualBox. A VM Alpine será criada dentro do Proxmox.

---

# 1. Baixar a ISO do Alpine Linux

Acesse o site oficial do Alpine Linux:

```text
https://alpinelinux.org/downloads/
```

Na seção de downloads, localize:

```text
Virtual
x86_64
```

O arquivo terá um nome semelhante a:

```text
alpine-virt-3.x.x-x86_64.iso
```

> Utilize a versão estável mais recente disponível no momento do laboratório.

---

# 2. Enviar a ISO para o Proxmox

Acesse a interface web do Proxmox.

No menu lateral:

```text
Datacenter
   ↓
Servidor Proxmox
   ↓
local
   ↓
ISO Images
```

Clique em:

```text
Upload
```

Selecione a ISO do Alpine Linux baixada anteriormente e aguarde o envio.

Ao final, confirme que a ISO aparece na lista de imagens disponíveis.

---

# 3. Criar a máquina virtual

No Proxmox, clique em:

```text
Create VM
```

## General

Defina um nome para a máquina.

Exemplo para servidor web:

```text
vm-web
```

ou para banco:

```text
vm-db
```

O campo **VM ID** pode permanecer com o valor sugerido automaticamente pelo Proxmox.

Clique em:

```text
Next
```

---

# 4. Selecionar a ISO

Na etapa **OS**, selecione:

```text
Use CD/DVD disc image file (iso)
```

Escolha a ISO:

```text
alpine-virt-...-x86_64.iso
```

Tipo do sistema operacional:

```text
Linux
```

Versão:

```text
7.x - 2.6 Kernel
```

ou a opção Linux equivalente apresentada pela versão do Proxmox utilizada no laboratório.

Clique em:

```text
Next
```

---

# 5. Configurar o sistema da VM

Na etapa **System**, as configurações padrão do Proxmox normalmente são suficientes para o laboratório.

Sugestão:

```text
Machine: padrão
BIOS: SeaBIOS
SCSI Controller: VirtIO SCSI
```

Não é necessário adicionar:

```text
TPM
EFI Disk
```

para esta atividade.

Clique em:

```text
Next
```

---

# 6. Configurar o disco

Como o Alpine é um sistema leve, não é necessário reservar muito espaço.

## VM-WEB

Sugestão:

```text
4 GB
```

## VM-DB

Sugestão:

```text
4 GB
```

Para o controlador de disco, utilize preferencialmente:

```text
SCSI
```

com controlador:

```text
VirtIO SCSI
```

Clique em:

```text
Next
```

---

# 7. Configurar CPU

Para o laboratório:

```text
Sockets: 1
Cores: 1
```

Portanto:

```text
1 vCPU
```

é suficiente para cada VM.

Clique em:

```text
Next
```

---

# 8. Configurar memória RAM

Como o Alpine possui baixo consumo de memória, utilize:

## VM-WEB

```text
512 MB
```

## VM-DB

```text
768 MB
```

Clique em:

```text
Next
```

---

# 9. Configurar a interface de rede

Durante a instalação inicial, a VM precisará de acesso à Internet para instalação de pacotes.

Selecione:

```text
Bridge: vmbr0
```

Modelo da placa de rede:

```text
VirtIO (paravirtualized)
```

Clique em:

```text
Next
```

Revise as configurações e clique em:

```text
Finish
```

---

# 10. Iniciar a VM

Selecione a VM criada.

Clique em:

```text
Start
```

Depois abra:

```text
Console
```

Aguarde a inicialização do Alpine Linux.

---

# 11. Login inicial

O Alpine executado pela ISO inicia em modo Live.

No prompt:

```text
localhost login:
```

digite:

```text
root
```

Na execução inicial normalmente não existe senha para o usuário `root`.

Após o login, será apresentado um terminal semelhante a:

```text
localhost:~#
```

---

# 12. Iniciar o instalador

Execute:

```bash
setup-alpine
```

O Alpine iniciará um processo interativo de configuração.

---

# 13. Configurar o teclado

O instalador perguntará:

```text
Select keyboard layout
```

Para teclado brasileiro, informe:

```text
br
```

Depois selecione o mapa correspondente, normalmente:

```text
br
```
---

# 14. Definir o hostname

O instalador solicitará:

```text
Enter system hostname
```

Para a VM-WEB:

```text
vm-web
```

Para a VM-DB:

```text
vm-db
```

---

# 15. Configurar a interface de rede

O instalador identificará a interface disponível.

Normalmente será algo semelhante a:

```text
eth0
```

Selecione a interface sugerida.

Quando perguntar:

```text
Ip address for eth0?
```

utilize:

```text
dhcp
```

Neste momento estamos utilizando a:

```text
vmbr0
```

e queremos que a VM receba endereço automaticamente para acessar a Internet.

---

# 16. Configurar senha do root

Defina uma senha conforme orientação do professor e confirme-a quando solicitado.

> Mesmo em laboratório, evite deixar o usuário root sem senha após a instalação.

---

# 17. Configurar fuso horário

Quando solicitado, utilize:

```text
America/Recife
```

ou outro fuso adequado ao local do laboratório (UTC).

---

# 18. Configurar proxy

Quando aparecer:

```text
HTTP/FTP proxy URL?
```

como o laboratório não utiliza proxy, pressione:

```text
Enter
```

para deixar em branco.

---

# 19. Selecionar o mirror do Alpine

O instalador perguntará qual servidor de pacotes deverá ser usado.

Uma opção prática é:

```text
f
```

para localizar automaticamente um mirror rápido.

Aguarde o teste dos repositórios.

---

# 20. Criar usuário adicional

Para manter o laboratório mais curto, pode-se optar por não criar um usuário adicional e utilizar `root` durante a atividade.

> Em ambientes reais, recomenda-se trabalhar com usuário comum e elevação de privilégios apenas quando necessário.

---

# 21. Configuração SSH

Quando o instalador perguntar pelo servidor SSH, utilize:

```text
openssh
```

Isso instala o OpenSSH e permite acesso remoto posteriormente, caso desejado.

---

# 22. Selecionar o disco de instalação

O disco virtual normalmente aparecerá como:

```text
sda
```
Selecione o disco correspondente à VM.

---

# 23. Escolher o modo de uso do disco

Quando aparecer:

```text
How would you like to use it?
```

escolha:

```text
sys
```

O modo `sys` realiza uma instalação convencional do Alpine no disco virtual.

---

# 24. Confirmar a formatação

Será exibido um aviso informando que os dados do disco serão apagados.

Confirme digitando:

```text
y
```

O instalador irá particionar, formatar e instalar o sistema.

Aguarde a conclusão.

---

# 25. Finalizar a instalação

Ao final será exibida uma mensagem semelhante a:

```text
Installation is complete. Please reboot.
```

Antes de reiniciar, volte à interface do Proxmox.

Acesse:

```text
VM
   ↓
Hardware
   ↓
CD/DVD Drive
```

Remova ou desmarque a ISO do Alpine para evitar que a VM inicialize novamente pelo instalador.

---

# 26. Reiniciar

No terminal:

```bash
reboot
```

Aguarde a inicialização.

Agora o sistema deverá iniciar pelo disco virtual.

---

# 27. Fazer login

Utilize:

```text
login: root
```

e informe a senha definida durante o `setup-alpine`.

---

# 28. Verificar a instalação

Execute:

```bash
hostname
```

Verifique a versão:

```bash
cat /etc/alpine-release
```

Verifique o kernel:

```bash
uname -a
```

Verifique o endereço IP:

```bash
ip addr
```

Verifique a rota:

```bash
ip route
```

---

# 29. Testar acesso à rede

Teste conectividade IP:

```bash
ping -c 3 8.8.8.8
```

Depois teste resolução DNS:

```bash
ping -c 3 google.com
```

Se ambos funcionarem, a VM possui acesso à Internet.

---

# 30. Atualizar os repositórios

Execute:

```bash
apk update
```

---

# 31. Instalar os pacotes da atividade

## VM-WEB

```bash
apk add nano python3 py3-pip git nginx curl
cd /opt
git clone URL_DO_REPOSITORIO chamados-lab
```

## VM-DB

```bash
apk add nano mariadb mariadb-client
wget https://raw.githubusercontent.com/luizfelipetux/chamados-lab/refs/heads/main/sql/schema.sql
```

---

# 32. Alterar a VM para a rede Host-Only

Depois que os pacotes necessários forem instalados, desligue:

```bash
poweroff
```

No Proxmox:

```text
VM
  ↓
Hardware
  ↓
Network Device
  ↓
Edit
```

Altere:

```text
Bridge: vmbr0
```

para:

```text
Bridge: vmbr1
```

A `vmbr1` corresponde à rede Host-Only:

```text
192.168.56.0/24
```

Depois ligue novamente a VM.

---

# 33. Configurar IP estático na vmbr1

Primeiro descubra o nome da interface:

```bash
ip link
```

Edite:

```bash
vi /etc/network/interfaces
```

ou, caso o `nano` esteja instalado:

```bash
nano /etc/network/interfaces
```

## VM-WEB

```text
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.56.150/24
```

## VM-DB

```text
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.56.200/24
```

> Substitua `eth0` caso a interface possua outro nome.

Reinicie a rede:

```bash
rc-service networking restart
```

---

# 34. Validar a comunicação

## Na VM-WEB

```bash
ip addr
ping -c 3 192.168.56.200
```

## Na VM-DB

```bash
ping -c 3 192.168.56.150
```

## No Linux Mint do laboratório

```bash
ping -c 3 192.168.56.150
ping -c 3 192.168.56.200
```

---

# Checklist final

## Proxmox

- [ ] ISO Alpine Virtual x86_64 enviada ao Proxmox.
- [ ] VM criada.
- [ ] CPU configurada.
- [ ] RAM configurada.
- [ ] Disco configurado.
- [ ] Interface inicialmente ligada à `vmbr0`.

## Alpine

- [ ] `setup-alpine` concluído.
- [ ] Hostname definido.
- [ ] Senha do root configurada.
- [ ] Sistema instalado no disco em modo `sys`.
- [ ] ISO removida após instalação.
- [ ] VM reiniciada pelo disco.

## Rede

- [ ] Internet funcionando inicialmente pela `vmbr0`.
- [ ] Pacotes necessários instalados.
- [ ] Interface alterada para `vmbr1`.
- [ ] IP estático configurado.
- [ ] Comunicação entre VM-WEB e VM-DB funcionando.
- [ ] Linux Mint consegue acessar as VMs.

---


Após esta etapa, as máquinas estão prontas para a instalação e configuração dos serviços da atividade de deployment.
