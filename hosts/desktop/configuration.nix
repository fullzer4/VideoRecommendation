{ config, pkgs, callPackage, inputs, ... }:

{
  imports = [
    ./hardware-configuration.nix
    inputs.home-manager.nixosModules.default
  ];

  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  networking.hostName = "fullzer4";
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

  environment.pathsToLink = [ "/libexec" ];

  services.xserver = {
    enable = true;
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
        i3status
        i3lock
        i3blocks
      ];
    };
    layout = "us";
    xkbVariant = "";
  };

  users.users.fullzer4 = {
    isNormalUser = true;
    description = "fullzer4";
    extraGroups = [ "networkmanager" "wheel" "audio" ];
    packages = with pkgs; [];
  };

  nixpkgs.config.allowUnfree = true;

  sound.enable = true;
  hardware.pulseaudio.package = pkgs.pulseaudioFull;
  hardware.pulseaudio.enable = true;
  hardware.pulseaudio.support32Bit = true;
  nixpkgs.config.pulseaudio = true;
  hardware.pulseaudio.extraConfig = "load-module module-combine-sink";

  environment.systemPackages = with pkgs; [
    manix
    vim 
    wget
    htop
    kitty
    firefox
    discord
    pavucontrol
  ];

  home-manager = {
    extraSpecialArgs = {inherit inputs; };
    users = {
      fullzer4 = import ./home.nix;
    };
  };  

  networking.firewall.allowedTCPPorts = [ 40 ];
  networking.firewall.allowedUDPPorts = [ 40 ];
  networking.firewall.enable = true;

  system.stateVersion = "23.11";

}
