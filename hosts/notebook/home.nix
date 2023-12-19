{ config, pkgs, ... }:

{
  home.username = "fullzer4";
  home.homeDirectory = "/home/fullzer4";

  fonts.fontconfig.enable = true;
  home.packages = [
    pkgs.git
    pkgs.nerdfonts
  ];

  home.sessionVariables = {
    EDITOR = "nvim";
  };

  home.file = {

  };

  programs.git = {
    enable = true;
    userName = "fullzer4";
    userEmail = "gabrielpelizzaro@gmail.com";
    aliases = {
      pu = "push";
      co = "checkout";
      cm = "commit";
    };
  };

  programs.zsh = {
    enable = true;
    enableAutosuggestions = true;
    enableCompletion = true;
    #envExtra = ''
    #  export SOMEZSHVARIABLE="something"
    #'';
  };

  programs.neovim = {
    enable = true;
    defaultEditor = true;
    viAlias = true;
    vimAlias = true;
    vimdiffAlias = true;
  };

  
  home.stateVersion = "22.11";

  programs.home-manager.enable = true;
}
