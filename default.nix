{ pkgs ? import <nixpkgs> {} }:

let
  inherit (pkgs) fetchFromGitHub callPackage;

  poetry2nix-src = fetchFromGitHub {
      owner = "nix-community";
      repo = "poetry2nix";
      rev = "3c92540";
      sha256 = "sha256-2GOiFTkvs5MtVF65sC78KNVxQSmsxtk0WmV1wJ9V2ck=";
  };
  poetry2nix = callPackage poetry2nix-src { };
in
  poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    preferWheels = true; # todo use overrides to fix this
    # it has to do with the maturin rust dependencies
  }
