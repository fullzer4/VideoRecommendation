{ config, pkgs, ... }:

{
  imports =
    [ 
      ./hardware-configuration.nix
      <home-manager/nixos>
    ];

  boot.loader.grub.enable = true;
  boot.loader.grub.device = "/dev/nvme0n1";
  boot.loader.grub.useOSProber = true;

  networking.hostName = "deskfull";
  
  networking.networkmanager.enable = true;

  time.timeZone = "America/Sao_Paulo";
  i18n.defaultLocale = "en_US.UTF-8";
  i18n.extraLocaleSettings = {
    LC_ADDRESS = "pt_BR.UTF-8";
    LC_IDENTIFICATION = "pt_BR.UTF-8";
    LC_MEASUREMENT = "pt_BR.UTF-8";
    LC_MONETARY = "pt_BR.UTF-8";
    LC_NAME = "pt_BR.UTF-8";
    LC_NUMERIC = "pt_BR.UTF-8";
    LC_PAPER = "pt_BR.UTF-8";
    LC_TELEPHONE = "pt_BR.UTF-8";
    LC_TIME = "pt_BR.UTF-8";
  };

  environment.pathsToLink = ["/libexec"];

  hardware.pulseaudio.enable = true;
  nixpkgs.config.pulseaudio = true;

  programs.dconf.enable = true;
  services.xserver = {
    enable = true;
    layout = "us";
    xkbVariant = "";
    
    desktopManager = {
      xterm.enable = true;
    };
    
    displayManager = {
      defaultSession = "none+i3";
    };
    
    windowManager.i3 = {
      enable = true;
      extraPackages = with pkgs; [
        dmenu
        i3lock
        i3-gaps
        i3blocks
      ];
    };
  };

  users.users.fullzer4 = {
    isNormalUser = true;
    description = "fullzer4";
    extraGroups = [ "networkmanager" "wheel" "docker"];
    packages = with pkgs; [];
  };
  services.getty.autologinUser = "fullzer4";

  home-manager.users.fullzer4 = { pkgs, ... }: {
    home.packages = [ pkgs.atool pkgs.httpie];
    programs.bash.enable = true;

    home.stateVersion = "23.05";
  };

  nixpkgs.config.allowUnfree = true;

  environment.systemPackages = with pkgs; [
     git
     vim
     neovim     
     wget
     neofetch
     kitty
     firefox
     pavucontrol
     vscode
     docker
     docker-compose
     podman
     podman-compose
  ];

  virtualisation.docker.enable = true;
  virtualisation.docker.enableOnBoot = true;
  virtualisation.podman.enable = true;

  programs.mtr.enable = true;
  programs.gnupg.agent = {
    enable = true;
    enableSSHSupport = true;
  };

  services.openssh.enable = true;

  # networking.firewall.allowedTCPPorts = [ ... ];
  # networking.firewall.allowedUDPPorts = [ ... ];
  networking.firewall.enable = true;

  system.copySystemConfiguration = true;
  system.autoUpgrade.enable = true;  
  system.autoUpgrade.allowReboot = true; 
  system.stateVersion = "23.05";
}
